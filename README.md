# hit-skill

**Three-layer transformation engine: human mechanisms, stimulus design, and propagation structures.**

## Prerequisites

- **Claude Cowork or Claude Code** environment

## Goal

Hit-skill solves the fundamental problem of designing for human impact. It provides a structured engine that layers scientific mechanisms of human behavior (Layer 1: why people react), stimulus design formulas (Layer 2: what to throw and how), and propagation dynamics (Layer 3: how it spreads). It bridges behavioral science and practical execution.

## When & How to Use

Invoke when designing messaging, campaigns, product narratives, or any artifact that needs to influence human perception or behavior. Works best as post-generation refinement: create your output first, then pass through hit-skill's 3-mode pipeline (Diagnose → Design → Transform). Unlike human-skill (individual psychology), hit-skill layers impact and propagation.

## Use Cases

| Scenario | Prompt | What Happens |
|---|---|---|
| Campaign not resonating | `"Diagnose why this message isn't landing"` | 16 human behavior axes→identifies missing motivations→suggests stimulus formulas |
| Product launch narrative | `"Design announcement for maximum awareness and adoption"` | Stimulus sequence→preconditions (V1~V5)→propagation across channels→domain adapters |
| Content for viral potential | `"Transform this article for social propagation"` | Multi-channel propagation axes→E-model quantification→fandom acceleration tactics |

## Key Features

- **3-layer architecture**: L1 maps 6 behavior sources to 16 axes + 13 meta-principles; L2 has 6 stimulus formulas + 5 preconditions; L3 has 5-axis propagation with E-model + ZM saturation correction
- **6 domains x 33 sub-domains** with pre-built adapters; hybrid and triple-matrix combinations
- **3 operational modes**: Diagnose (current state), Design (novel generation), Transform (refinement)

## Works With

- **[human-skill](https://github.com/jasonnamii/human-skill)** — foundational 16-axis psychology; hit-skill adds propagation
- **[biz-skill](https://github.com/jasonnamii/biz-skill)** — structures strategic narrative into human-impact sequences
- **[planning-skill](https://github.com/jasonnamii/planning-skill)** — integrates hit-pattern into ideation phases

## Installation

```bash
git clone https://github.com/jasonnamii/hit-skill.git ~/.claude/skills/hit-skill
```

## Update

```bash
cd ~/.claude/skills/hit-skill && git pull
```

Skills placed in `~/.claude/skills/` are automatically available in Claude Code and Cowork sessions.

## Part of Cowork Skills

This is one of 25+ custom skills. See the full catalog: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## License

MIT License — feel free to use, modify, and share.
