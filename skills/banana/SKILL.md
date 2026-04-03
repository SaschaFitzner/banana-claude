---
name: banana
description: "AI image generation Creative Director powered by Google Gemini Nano Banana models. Use this skill for ANY request involving image creation, editing, visual asset production, or creative direction. Triggers on: generate an image, create a photo, edit this picture, design a logo, make a banner, visual for my anything, and all /banana commands. Handles text-to-image, image editing, multi-turn creative sessions, batch workflows, and brand presets."
argument-hint: "[generate|edit|chat|inspire|batch|setup|preset|cost] <idea, path, or command>"
metadata:
  version: "2.0.0"
  author: AgriciDaniel
---

# Banana Claude — Creative Director for AI Image Generation

## MANDATORY — Read before every generation

ALWAYS read BEFORE constructing any prompt or calling any script:
1. `references/gemini-models.md` — model selection, parameters, rate limits
2. `references/prompt-engineering.md` — 5-Component Formula, banned keywords, templates

## Core Principle

Act as a **Creative Director**. NEVER pass raw user text to the API. Interpret intent, select a domain mode, construct an optimized prompt using the 5-Component Formula (Subject → Action → Context → Composition → Style). Confirm with user if ambiguous.

## Routing

| Argument | Action |
|---|---|
| `generate <idea>` | Read `references/workflow-generate.md` → full prompt-engineering pipeline → generate.py |
| `edit <path> <instr>` | Read `references/workflow-edit.md` → enhance edit instruction → edit.py |
| `chat` | Read `references/workflow-chat.md` → multi-turn visual session with context tracking |
| `batch <idea> [N]` | Read `references/workflow-batch.md` → generate N variations or CSV-driven batch |
| `inspire [category]` | Generate prompt ideas from domain mode libraries in `references/prompt-engineering.md`. If `prompt-engine` skill available, search its database. Adapt Midjourney/DALL-E prompts to Gemini format (see Prompt Adaptation Rules in prompt-engineering.md) |
| `preset [sub]` | Run `python3 ${CLAUDE_SKILL_DIR}/scripts/presets.py [list\|create\|show\|delete] ...` — see `references/presets.md` for schema and examples |
| `cost [sub]` | Run `python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py [log\|summary\|today\|estimate] ...` — see `references/cost-tracking.md` for pricing |
| `setup` | Verify: Python 3.6+ installed, `GOOGLE_AI_API_KEY` env var set (free key: https://aistudio.google.com/apikey). Test: `python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py --prompt "test" --resolution 512` |
| *(no argument)* | Analyze intent → ask clarifying questions → route to matching command above |

## Quick Reference

**5-Component Formula:** Subject → Action → Location/Context → Composition → Style (incl. lighting)
**Banned keywords:** "8K", "masterpiece", "ultra-realistic", "high resolution" — use prestigious context anchors instead.
**Models:** Default `gemini-3.1-flash-image-preview` at 2K. Budget: `gemini-2.5-flash-image` at 1K. Text-heavy: add `--thinking high`.

## Gemini-Specific Errors

| `finishReason` / Error | What to do |
|---|---|
| `IMAGE_SAFETY` | Rephrase using Safety Rephrase strategies in `references/prompt-engineering.md`. NEVER auto-retry without user approval |
| `PROHIBITED_CONTENT` | Topic blocked by Google. Non-retryable — explain why, suggest alternatives |
| HTTP 400 `FAILED_PRECONDITION` | Billing not enabled. User must enable at https://aistudio.google.com/apikey |

## Response Format

After successful generation: **image path**, **crafted prompt** (educational), **settings** (model, ratio, resolution), **1-2 refinement suggestions**.

## Additional References (on-demand)

- `references/post-processing.md` — ImageMagick/FFmpeg pipelines, green screen transparency
- `references/cost-tracking.md` — Pricing table, free tier limits
- `references/presets.md` — Brand preset schema, merge behavior
