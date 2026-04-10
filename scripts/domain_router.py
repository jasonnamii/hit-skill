#!/usr/bin/env python3
"""
히트스킬 도메인 라우터.

사용법:
  python domain_router.py "입력 키워드"     # 도메인+세부도메인 판별
  python domain_router.py --list            # 6대 도메인+33세부도메인 목록
  python domain_router.py --border          # 접경지대 14건 판별 기준
  python domain_router.py --spokes 결과     # 스크리닝 결과→로드할 스포크 매핑
"""

import sys

DOMAINS = {
    "A": {
        "name": "서사몰입",
        "consumption": "시간축 몰입",
        "killer": "부재-반전계",
        "subs": {
            "A1": "영화",
            "A2": "드라마",
            "A3": "애니",
            "A4": "웹툰",
            "A5": "출판",
            "A6": "팟캐스트",
            "A7": "인터랙티브픽션"
        }
    },
    "B": {
        "name": "인터랙션몰입",
        "consumption": "행위 참여",
        "killer": "공백-반복계",
        "subs": {
            "B1": "게임",
            "B2": "UX/기능",
            "B3": "소셜네트워크",
            "B4": "웹/추천",
            "B5": "라이드셰어",
            "B6": "XR"
        }
    },
    "C": {
        "name": "시각즉시",
        "consumption": "공간적 즉시",
        "killer": "참조점-감각계",
        "subs": {
            "C1": "광고",
            "C2": "파인아트",
            "C3": "팝/디지털아트",
            "C4": "제품디자인",
            "C5": "패션",
            "C6": "브랜드CI",
            "C7": "건축"
        }
    },
    "D": {
        "name": "청각퍼포먼스",
        "consumption": "시간축 몰입",
        "killer": "부재-반전계",
        "subs": {
            "D1": "음악",
            "D2": "공연",
            "D3": "예능/방송",
            "D4": "ASMR·사운드"
        }
    },
    "E": {
        "name": "숏폼바이럴",
        "consumption": "행위 참여",
        "killer": "공백-반복계",
        "subs": {
            "E1": "숏폼영상",
            "E2": "소셜콘텐츠",
            "E3": "밈",
            "E4": "롱폼바이럴"
        }
    },
    "F": {
        "name": "체험환경",
        "consumption": "행위 참여",
        "killer": "공백-반복계",
        "subs": {
            "F1": "테마파크",
            "F2": "F&B/리테일",
            "F3": "페스티벌",
            "F4": "호텔·숙박",
            "F5": "설치미술·몰입전시"
        }
    },
}

BORDERS = [
    ("뮤직비디오", "3분+→D1, 1분-→E1, 중간→주소비채널"),
    ("극장 애니", "원작연속→A3, 독립작→A1"),
    ("건축 체험", "건물감상→C7, 체험프로그램→F"),
    ("게임 VR", "기존게임VR→B1, VR네이티브→B6"),
    ("브랜드 광고", "캠페인→C1, 영구심볼→C6"),
    ("음악 챌린지", "원곡→D1, 참여→E1"),
    ("팝업매장", "상시→F2, 기간한정→F3"),
    ("선택형 게임", "분기서사→A7, 게임플레이→B1"),
    ("커뮤니티 앱", "소속감→B3, 유틸리티→B2"),
    ("수면 음악", "이완수면→D4, 감상→D1"),
    ("장편 교육영상", "영상→E4, 오디오→A6"),
    ("디자인 호텔", "숙박체험→F4, 건물감상→C7"),
    ("몰입형 전시", "상설/순회→F5, 기간한정→F3"),
    ("명상 앱", "이완콘텐츠→D4, 기능UX→B2"),
]

SPOKE_MAP = {
    "L1": "layer1-mechanism.md",
    "L2": "layer2-formulas.md",
    "L3": "layer3-propagation.md",
    "공식①": "rx-absence.md",
    "공식②": "rx-void.md",
    "공식③": "rx-reference.md",
    "공식④": "rx-emotion.md",
    "공식⑤": "rx-peak.md",
    "공식⑥": "rx-repetition.md",
    "도메인": "domain-universal.md",
    "세부도메인": "subdomain-adapters.md",
    "V3-t": "v3t-decay-model.md",
    "하이브리드": "cross-domain-matrix.md",
    "하이브리드세부": "subdomain-full-matrix.md",
    "L3딜레이": "l2l3-delay-model.md",
    "트리플": "triple-hybrid-matrix.md",
    "E전파": "e-propagation-model.md",
    "팬덤": "fandom-acceleration.md",
    "다채널": "multi-channel-propagation.md",
    "IRR": "irr-calibration.md",
    "ZM": "zm-correction-model.md",
}

def list_all():
    """6대 도메인+33세부도메인 목록 출력"""
    print("=" * 70)
    print("히트스킬 6대 도메인 + 33개 세부도메인")
    print("=" * 70)
    for code, d in sorted(DOMAINS.items()):
        print(f"\n[{code}] {d['name']} ({d['consumption']})")
        print(f"    킬러 공식: {d['killer']}")
        print("    세부도메인:")
        for sub_code, sub_name in sorted(d['subs'].items()):
            print(f"      {sub_code}: {sub_name}")
    print("\n" + "=" * 70)

def show_borders():
    """접경지대 판별 기준 출력"""
    print("=" * 70)
    print("접경지대 판별 기준 (14건)")
    print("=" * 70)
    for i, (item, rule) in enumerate(BORDERS, 1):
        print(f"{i:2}. {item}")
        print(f"    → {rule}\n")

def show_spokes(keywords):
    """스크리닝 결과→로드할 스포크 매핑"""
    print("=" * 70)
    print("스크리닝 결과 → 로드할 스포크")
    print("=" * 70)
    for kw in keywords:
        matched = [(k, v) for k, v in SPOKE_MAP.items() if kw.lower() in k.lower()]
        if matched:
            print(f"\n{kw}:")
            for k, v in matched:
                print(f"  → references/{v}")
        else:
            print(f"\n{kw}: 매칭 없음")
    print()

def identify_domain(keywords):
    """도메인+세부도메인 판별"""
    kw_lower = " ".join(keywords).lower()
    matches = []

    # 세부도메인 매칭
    for code, d in DOMAINS.items():
        for sub_code, sub_name in d['subs'].items():
            if sub_name.lower() in kw_lower or sub_code.lower() in kw_lower:
                matches.append((code, sub_code, sub_name, d['name'], d['killer']))

    if matches:
        print("=" * 70)
        print("도메인 판별 결과")
        print("=" * 70)
        for code, sub_code, sub_name, dom_name, killer in matches:
            print(f"\n[{code}] {dom_name}")
            print(f"  세부도메인: {sub_code} ({sub_name})")
            print(f"  킬러 공식: {killer}")

        # 복수 도메인 감지
        unique_domains = set(m[0] for m in matches)
        if len(unique_domains) > 1:
            print("\n" + "-" * 70)
            print("⚠  복수 도메인 감지 → 하이브리드 판별 필요")
            print("  → references/cross-domain-matrix.md 로드")
        print()
    else:
        # 접경지대 매칭
        print("=" * 70)
        print("도메인 판별 결과")
        print("=" * 70)
        for item, rule in BORDERS:
            if item.replace(" ", "").lower() in kw_lower.replace(" ", ""):
                print(f"\n접경지대: {item}")
                print(f"  판별: {rule}\n")
                return
        print("\n매칭 없음. 도메인을 직접 지정하거나 --list로 목록 확인\n")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "--list":
        list_all()
    elif cmd == "--border":
        show_borders()
    elif cmd == "--spokes":
        show_spokes(sys.argv[2:])
    else:
        identify_domain(sys.argv[1:])

if __name__ == "__main__":
    main()
