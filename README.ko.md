# 히트 패턴 아키텍처 변환 엔진

> 🇺🇸 [English README](./README.md)

**3층 구조: 인간 메커니즘, 자극 설계, 전파 구조의 통합 변환 엔진입니다.**

## 사전 요구사항

- **Claude Cowork 또는 Claude Code** 환경

## 목적

hit-skill은 인간의 영향을 미치기 위한 설계의 근본적인 문제를 해결합니다. 인간 행동의 과학적 메커니즘(1층: 사람들이 왜 반응하는가), 자극 설계 공식(2층: 무엇을 어떻게 전달할 것인가), 전파 역학(3층: 어떻게 확산되는가)을 계층화한 구조화된 엔진을 제공합니다. 행동과학과 실제 실행을 연결합니다.

## 사용 시점 및 방법

메시지, 캠페인, 제품 내러티브 또는 인간의 인식이나 행동에 영향을 미쳐야 하는 어떤 산출물을 설계할 때 발동합니다. 사후 생성 정제에 가장 효과적입니다: 먼저 산출물을 만든 후, hit-skill의 3모드 파이프라인(진단 → 설계 → 변환)을 통과시킵니다. human-skill(개인 심리학)과 달리, hit-skill은 영향력과 전파를 계층화합니다.

## 사용 예시

| 상황 | 프롬프트 | 결과 |
|---|---|---|
| 캠페인이 반응이 없음 | `"이 메시지가 먹히지 않는 이유를 진단해줘"` | 16개 인간 행동 축→부족한 동기 파악→자극 공식 제안 |
| 제품 출시 내러티브 | `"최대 인식과 채택을 위해 공지사항을 설계해줘"` | 자극 시퀀스→선행조건(V1~V5)→채널 전파→도메인 어댑터 |
| 바이럴 가능성 콘텐츠 | `"이 기사를 소셜 전파용으로 변환해줘"` | 멀티채널 전파 축→E-모델 정량화→팬덤 가속 전략 |

## 핵심 기능

- **3층 아키텍처**: L1은 6개 행동 소스를 16개 축 + 13개 메타원리로 매핑; L2는 6개 자극 공식 + 5개 선행조건 보유; L3은 5축 전파 + E-모델 + ZM 포화 수정
- **6개 도메인 x 33개 서브도메인** 사전 구축된 어댑터 포함; 하이브리드 및 3중 매트릭스 조합
- **3가지 운영 모드**: 진단(현 상태), 설계(신규 생성), 변환(정제)

## 연관 스킬

- **[human-skill](https://github.com/jasonnamii/human-skill)** — 기초 16축 심리학; hit-skill은 전파 기능 추가
- **[biz-skill](https://github.com/jasonnamii/biz-skill)** — 전략적 내러티브를 인간-영향 시퀀스로 구조화
- **[planning-skill](https://github.com/jasonnamii/planning-skill)** — 아이디어 도출 단계에 hit-pattern 통합

## 설치

```bash
git clone https://github.com/jasonnamii/hit-skill.git ~/.claude/skills/hit-skill
```

## 업데이트

```bash
cd ~/.claude/skills/hit-skill && git pull
```

`~/.claude/skills/`에 배치된 스킬은 Claude Code 및 Cowork 세션에서 자동으로 사용할 수 있습니다.

## Cowork 스킬 생태계

25개 이상의 커스텀 스킬 중 하나입니다. 전체 카탈로그: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## 라이선스

MIT 라이선스 — 자유롭게 사용, 수정, 공유하세요.