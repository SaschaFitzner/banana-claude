# Workflow: Edit

> **Prerequisites:** If not already loaded, read `references/prompt-engineering.md` before step 3. Default model: `gemini-3.1-flash-image-preview`.

## Edit Pipeline

1. **Read image** — Confirm the file path exists and is a valid image. If the user referenced an image without a path, check the conversation context for the most recently generated/edited image path. If none found, ask for the path.
2. **Analyze** — Understand what the user wants changed; check if any brand preset applies
3. **Enhance instruction** — NEVER pass raw user text. Expand the edit instruction with edge-preserving detail, positive framing, and style-consistent continuation
4. **Execute edit.py** — Run with enhanced instruction (see syntax below)
5. **Verify** — Confirm the output file exists; NEVER report success without a valid path
6. **Log cost** — `python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log --model gemini-3.1-flash-image-preview --resolution na --prompt "edit: [brief description]"`

---

## Intelligent Edit Transformations

ALWAYS enhance the user's instruction before passing to the API:

| User says | Claude crafts |
|-----------|---------------|
| "remove background" | "Remove the existing background entirely, replacing it with a clean transparent or solid white background. Preserve all edge detail and fine features like hair strands." |
| "make it warmer" | Specific color temperature shift with preservation notes for skin tones and highlights |
| "add text" | Font style, size, placement, contrast, readability notes with exact text in quotes |
| "make it pop" | Increase saturation, add contrast, enhance focal point — describe the specific visual outcome |
| "extend it" | Outpainting with style-consistent continuation description matching existing lighting and color grade |

See `references/prompt-engineering.md` → Positive Framing for rephrasing exclusions as affirmations.

---

## Execute edit.py

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/edit.py \
  --image PATH_TO_IMAGE \
  --prompt "YOUR ENHANCED EDIT INSTRUCTION" \
  --model "gemini-3.1-flash-image-preview"
```

**All flags:**

| Flag | Required | Default |
|------|:--------:|---------|
| `--image` | Yes | — |
| `--prompt` | Yes | — |
| `--model` | No | `gemini-3.1-flash-image-preview` |
| `--api-key` | No | `$GOOGLE_AI_API_KEY` env |

Note: `edit.py` does not support `--resolution` — output resolution matches the source image.

**JSON output on success:**
```json
{"path": "~/Documents/nanobanana_generated/banana_TIMESTAMP.png", "model": "...", "text": "..."}
```
On error: `{"error": true, "message": "..."}` with non-zero exit code.

See SKILL.md → Gemini-Specific Errors for `IMAGE_SAFETY` and `PROHIBITED_CONTENT` handling. HTTP 429 — scripts retry automatically (exponential backoff, 3 attempts).
