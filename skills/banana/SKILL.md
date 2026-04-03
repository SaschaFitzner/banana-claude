---
name: banana
description: "AI image generation using Google Gemini. Use for any request involving creating, editing, or iterating on images, photos, logos, banners, and illustrations. Handles text-to-image, image editing, multi-turn sessions, batch workflows, and brand presets. Triggers on: generate an image, create a photo, edit this picture, design a logo, make a banner, and all /banana commands."
argument-hint: "[generate|edit|chat|inspire|batch|setup|preset|cost] <idea, path, or command>"
metadata:
  version: "2.0.0"
  author: "Sascha Fitzner — fitznerIO GmbH"
  original-author: AgriciDaniel
---

# Banana Claude — Creative Director for AI Image Generation

## Before constructing any image prompt

Read BOTH before building any prompt or calling generate.py / edit.py:
1. `references/gemini-models.md` — model selection, parameters, rate limits
2. `references/prompt-engineering.md` — 5-Component Formula, banned keywords, templates

## Core Principle

Act as a **Creative Director**. NEVER pass raw user text to the API. Interpret intent, select a domain mode, construct an optimized prompt using the 5-Component Formula (Subject → Action → Context → Composition → Style). Ask clarifying questions if the request is ambiguous.

## Routing

| Argument | Action |
|---|---|
| `generate <idea>` | Read `references/workflow-generate.md` → full pipeline → generate.py |
| `edit <path> <instr>` | Read `references/workflow-edit.md` → enhance instruction → edit.py |
| `chat` | Read `references/workflow-chat.md` → multi-turn session with context tracking |
| `batch <idea> [N]` | Read `references/workflow-batch.md` → N variations or CSV-driven batch (requires cost confirmation) |
| `inspire [category]` | Read `references/prompt-engineering.md` → generate ideas from domain libraries; adapt Midjourney/DALL-E prompts to Gemini format (see Prompt Adaptation Rules) |
| `preset [sub]` | Read `references/presets.md` → `python3 ${CLAUDE_SKILL_DIR}/scripts/presets.py [list\|create\|show\|delete]` |
| `cost [sub]` | Read `references/cost-tracking.md` → `python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py [log\|summary\|today\|estimate]` |
| `setup` | Verify Python 3.6+ and `GOOGLE_AI_API_KEY` env var. Free key: https://aistudio.google.com/apikey. Test: `python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py --prompt "test" --resolution 512` |
| *(no argument)* | Analyze intent → ask clarifying questions → route to matching command |

## Gemini-Specific Errors

| `finishReason` / Error | Action |
|---|---|
| `IMAGE_SAFETY` | Rephrase using Safety Rephrase strategies in `references/prompt-engineering.md`. NEVER auto-retry without user approval. |
| `PROHIBITED_CONTENT` | Topic blocked by Google. Non-retryable — explain why, suggest alternatives. |
| HTTP 400 `FAILED_PRECONDITION` | Billing not enabled. User must enable at https://aistudio.google.com/apikey |

## Response Format

After successful generation: **image path**, **crafted prompt** (so the user can learn), **settings** (model, ratio, resolution), **1-2 actionable refinement suggestions** (e.g., "try `--thinking high` for sharper text" or "switch to 4K for print").

## Additional References (load on demand)

- `references/post-processing.md` — ImageMagick/FFmpeg pipelines, green screen transparency
- `references/cost-tracking.md` — Pricing table, free tier limits
- `references/presets.md` — Brand preset schema, merge behavior
