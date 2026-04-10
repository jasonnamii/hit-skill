#!/usr/bin/env python3
"""
hit-skill 정량 모델 계산기.

L3 전파 구조의 핵심 수식을 코드화하여 LLM 인라인 계산 오류를 제거.

사용법:
  python quant_models.py zm_eff 3.3
  python quant_models.py npe 2.5 1.8 1.5 0.15
  python quant_models.py npe_fandom 2.5 1.8 1.5 0.15 3.0 2.0 2.5
  python quant_models.py mcr 0.27 0.15 0.17
  python quant_models.py cse 3.0 1.8
  python quant_models.py mc_dac 0.15 3
  python quant_models.py all --pam 2.5 --irr 1.8 --zm 3.3 --dac 0.15 --fam_org 3.0 --fam_ugc 2.0 --fam_cross 2.5
"""

import sys
import math
from dataclasses import dataclass


# ─────────────────────────────────────────────
# §1. ZM 포화 보정 모델 (zm-correction-model.md)
# ─────────────────────────────────────────────
DELTA = 0.68  # 최적 δ (조건부 로그 모델)


def zm_eff(zm_raw: float) -> float:
    """ZM 포화 보정.
    ZM_raw ≤ 2.0 → ZM_eff = ZM_raw (보정 불필요)
    ZM_raw > 2.0 → ZM_eff = 2.0 + δ × ln(ZM_raw / 2.0)
    """
    if zm_raw <= 2.0:
        return zm_raw
    return 2.0 + DELTA * math.log(zm_raw / 2.0)


# ─────────────────────────────────────────────
# §2. NPE 산출 (e-propagation-model.md)
# ─────────────────────────────────────────────
def npe(pam: float, irr: float, zm_raw: float, dac: float) -> dict:
    """E 전파 정량 모델.
    NPE_gross = PAM × IRR × ZM_eff
    NPE_net = NPE_gross × (1 - DAC)

    Args:
        pam: Platform Amplification Multiplier (플랫폼 증폭 배수)
        irr: Intrinsic Resonance Rate (내재 공명률)
        zm_raw: Zeitgeist Match raw score (시대정신 일치도)
        dac: Decay Acceleration Constant (감쇠 가속 상수, 0~1)

    Returns:
        dict with zm_eff, npe_gross, npe_net
    """
    zm = zm_eff(zm_raw)
    gross = pam * irr * zm
    net = gross * (1 - dac)
    return {
        "zm_raw": zm_raw,
        "zm_eff": round(zm, 4),
        "npe_gross": round(gross, 4),
        "dac": dac,
        "npe_net": round(net, 4),
    }


# ─────────────────────────────────────────────
# §3. BFC 판정 (e-propagation-model.md)
# ─────────────────────────────────────────────
# BFC = Backflow Conversion (역류 전환율)
# 도메인별 기준값 — 레퍼런스에서 추출
BFC_TABLE = {
    "A_서사몰입": 0.25,
    "B_인터랙션": 0.20,
    "C_시각즉시": 0.15,
    "D_청각퍼포먼스": 0.35,
    "E1_숏폼": 0.05,
    "E4_롱폼바이럴": 0.30,
    "F_체험환경": 0.20,
}


def bfc_check(domain: str) -> float | None:
    """도메인별 BFC 기준값 조회."""
    return BFC_TABLE.get(domain)


# ─────────────────────────────────────────────
# §4. FAM 팬덤 가속 모델 (fandom-acceleration.md)
# ─────────────────────────────────────────────
def fam_raw(org_mob: float, ugc_amp: float, cross_plat: float) -> float:
    """FAM 원시 곱 = OrgMob × UGCamp × CrossPlat."""
    return org_mob * ugc_amp * cross_plat


def npe_fandom(pam: float, irr: float, zm_raw: float, dac: float,
               org_mob: float, ugc_amp: float, cross_plat: float) -> dict:
    """팬덤 가속 반영 NPE.
    FAM은 NPE에 직접 곱해지는 것이 아니라 "과소 추정분만 보정".
    NPE_fandom = NPE_net + (NPE_net × (sqrt(FAM) - 1))
              = NPE_net × sqrt(FAM)

    sqrt 보정 이유: FAM=7.5의 직접 곱은 실측(3~4x)과 괴리.
    sqrt(7.5)=2.74, NPE_net×2.74 ≈ 실측 범위.
    """
    base = npe(pam, irr, zm_raw, dac)
    fam = fam_raw(org_mob, ugc_amp, cross_plat)
    fam_sqrt = math.sqrt(fam)
    npe_f = base["npe_net"] * fam_sqrt

    return {
        **base,
        "fam_raw": round(fam, 4),
        "fam_sqrt": round(fam_sqrt, 4),
        "npe_fandom": round(npe_f, 4),
    }


# ─────────────────────────────────────────────
# §5. MCR 다채널 도달 배수 (multi-channel-propagation.md)
# ─────────────────────────────────────────────
def mcr(reach_nondup_pairs: list[tuple[float, float]]) -> float:
    """MCR = 1 + Σ(도달비중_i × 비중복률_i)  (i = 2번째 이후 채널).

    Args:
        reach_nondup_pairs: [(도달비중, 비중복률), ...] for 2nd+ channels
    """
    return 1 + sum(r * n for r, n in reach_nondup_pairs)


# ─────────────────────────────────────────────
# §6. CSE 채널 전략 효율 지수 (multi-channel-propagation.md)
# ─────────────────────────────────────────────
def cse(mcs5_base: float, mcs5_strategy: float) -> float:
    """CSE = MCS5_base / MCS5(전략). 1보다 크면 전략이 기준보다 빠름."""
    if mcs5_strategy == 0:
        return float("inf")
    return mcs5_base / mcs5_strategy


# ─────────────────────────────────────────────
# §7. MC-DAC 다채널 감쇠 (multi-channel-propagation.md)
# ─────────────────────────────────────────────
GAMMA = 0.12  # 기본 γ (레퍼런스 기준)


def mc_dac(dac_base: float, active_channels: int, gamma: float = GAMMA) -> float:
    """MC-DAC = DAC_base × (1 + γ × ln(활성채널수)).
    채널이 많을수록 감쇠가 가속됨.
    """
    if active_channels <= 1:
        return dac_base
    return dac_base * (1 + gamma * math.log(active_channels))


# ─────────────────────────────────────────────
# §8. V3-t 감쇠 반감기 (v3t-decay-model.md)
# ─────────────────────────────────────────────
def v3t_intensity(initial: float, half_life: float, time: float) -> float:
    """자극 감쇠 모델: I(t) = I_0 × 0.5^(t/t_half).
    Args:
        initial: 초기 자극 강도
        half_life: 반감기 (동일 단위)
        time: 경과 시간
    """
    if half_life <= 0:
        return 0
    return initial * (0.5 ** (time / half_life))


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "zm_eff":
        val = float(sys.argv[2])
        result = zm_eff(val)
        print(f"ZM_raw={val} → ZM_eff={result:.4f}")

    elif cmd == "npe":
        pam, irr_, zm_, dac_ = (float(x) for x in sys.argv[2:6])
        r = npe(pam, irr_, zm_, dac_)
        print(f"PAM={pam}, IRR={irr_}, ZM_raw={zm_} → ZM_eff={r['zm_eff']}")
        print(f"NPE_gross={r['npe_gross']}, DAC={dac_} → NPE_net={r['npe_net']}")

    elif cmd == "npe_fandom":
        pam, irr_, zm_, dac_ = (float(x) for x in sys.argv[2:6])
        org, ugc, cross = (float(x) for x in sys.argv[6:9])
        r = npe_fandom(pam, irr_, zm_, dac_, org, ugc, cross)
        print(f"Base NPE_net={r['npe_net']}")
        print(f"FAM_raw={r['fam_raw']}, FAM_sqrt={r['fam_sqrt']}")
        print(f"NPE_fandom={r['npe_fandom']}")

    elif cmd == "mcr":
        # 인자: 도달비중1 비중복률1 도달비중2 비중복률2 ...
        pairs = []
        args = sys.argv[2:]
        for i in range(0, len(args), 2):
            pairs.append((float(args[i]), float(args[i + 1])))
        result = mcr(pairs)
        print(f"MCR={result:.4f}")

    elif cmd == "cse":
        base, strat = float(sys.argv[2]), float(sys.argv[3])
        result = cse(base, strat)
        print(f"MCS5_base={base}, MCS5_strategy={strat} → CSE={result:.4f}")

    elif cmd == "mc_dac":
        dac_b = float(sys.argv[2])
        channels = int(sys.argv[3])
        result = mc_dac(dac_b, channels)
        print(f"DAC_base={dac_b}, channels={channels} → MC-DAC={result:.4f}")

    elif cmd == "v3t":
        initial, half, time = (float(x) for x in sys.argv[2:5])
        result = v3t_intensity(initial, half, time)
        print(f"I_0={initial}, t_half={half}, t={time} → I(t)={result:.4f}")

    elif cmd == "all":
        # --key value 파싱
        args = sys.argv[2:]
        kv = {}
        for i in range(0, len(args), 2):
            kv[args[i].lstrip("-")] = float(args[i + 1])

        pam = kv.get("pam", 1.0)
        irr_ = kv.get("irr", 1.0)
        zm_ = kv.get("zm", 1.0)
        dac_ = kv.get("dac", 0.0)

        print("=" * 50)
        print("  Hit Skill 정량 모델 종합 산출")
        print("=" * 50)

        r = npe(pam, irr_, zm_, dac_)
        print(f"\n[ZM 보정] ZM_raw={zm_} → ZM_eff={r['zm_eff']}")
        print(f"[NPE] PAM={pam} × IRR={irr_} × ZM_eff={r['zm_eff']}")
        print(f"  NPE_gross={r['npe_gross']}")
        print(f"  NPE_net={r['npe_net']} (DAC={dac_})")

        if "fam_org" in kv:
            org = kv["fam_org"]
            ugc = kv["fam_ugc"]
            cross = kv["fam_cross"]
            rf = npe_fandom(pam, irr_, zm_, dac_, org, ugc, cross)
            print(f"\n[FAM] OrgMob={org} × UGCamp={ugc} × CrossPlat={cross}")
            print(f"  FAM_raw={rf['fam_raw']}, FAM_sqrt={rf['fam_sqrt']}")
            print(f"  NPE_fandom={rf['npe_fandom']}")

        print()

    else:
        print(f"ERROR: '{cmd}' 알 수 없는 명령")
        print("사용 가능: zm_eff, npe, npe_fandom, mcr, cse, mc_dac, v3t, all")
        sys.exit(1)


if __name__ == "__main__":
    main()
