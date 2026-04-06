# Workflow: Chat (Multi-turn Visual Session)

> Multi-turn creative sessions with character and style consistency across iterations. This workflow orchestrates `workflow-generate.md` (first image) and `workflow-edit.md` (refinements) — load those as needed.

## Session Rules

- ALWAYS generate the initial concept using the full pipeline in `references/workflow-generate.md`
- For EVERY refinement step, use `edit.py` with the path to the most recent image (see `references/workflow-edit.md`)
- Track the current image path across turns — each edit produces a new file; update the tracked path
- NEVER restart from text-to-image when the user asks to refine — use `edit.py` on the last output
- NEVER lose the accumulated context (style, character details, prior changes) between turns

## Context Tracking

After each generation or edit, maintain in the active conversation context (working memory):
1. **Current image path** — the last successfully generated/edited file
2. **Character anchors** — 2-3 key physical identifiers established in the first turn (hair color/style, distinctive clothing, facial feature)
3. **Style anchors** — domain mode, lighting style, color grade, aspect ratio from the initial brief
4. **Change history** — brief log of what was altered in each turn

## Character Consistency

Enrich every edit prompt with accumulated context:
- Reference "the same character" + repeat 2-3 key identifiers from the first generation
- Repeat the original style anchors in each edit instruction to prevent drift
- See `references/prompt-core.md` → Character Consistency (Multi-turn) for the technique of prepending the previous output image to the next edit call to reinforce visual continuity

**Character drift warning:** After 4+ consecutive edit turns, if character consistency breaks down, consider re-generating from text-to-image using the accumulated style anchors as the new base brief.

## Use Cases

Best suited for:
- Character design sheets (multiple angles, poses, expressions)
- Sequential storytelling (scene-to-scene with consistent characters)
- Progressive refinement (iterate toward a final approved asset)
- Style exploration (same subject, multiple style variations)

## Session End

When the user is satisfied, offer to:
- Output all prompts used across all turns as a numbered markdown list
- Log the total session cost via `references/cost-tracking.md`
