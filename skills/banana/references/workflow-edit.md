# Workflow: Edit

> **Prerequisites:** If not already loaded, read `references/prompt-engineering.md` before step 3. Default model: `gemini-3.1-flash-image-preview`.

## Edit Pipeline

1. **Read image** — Confirm the file path exists and is a valid image. If the user referenced an image without a path, check the conversation context for the most recently generated/edited image path. If none found, ask for the path.
2. **Collect references** — If the user provides additional reference images (for style transfer, color matching, element composition, or character consistency), collect their paths. Max 13 reference images (14 total with primary).
3. **Analyze** — Understand what the user wants changed; check if any brand preset applies. If references are provided, describe in the prompt how they should influence the edit.
4. **Enhance instruction** — NEVER pass raw user text. Expand the edit instruction with edge-preserving detail, positive framing, and style-consistent continuation. When references are present, explicitly describe what to adopt from each reference (e.g., "Apply the color palette from the second image" or "Match the lighting style of the reference").
5. **Execute edit.py** — Run with enhanced instruction (see syntax below)
6. **Verify** — Confirm the output file exists; NEVER report success without a valid path
7. **Log cost** — `python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log --model gemini-3.1-flash-image-preview --resolution na --prompt "edit: [brief description]"`

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

### Basic edit (single image)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/edit.py \
  --image PATH_TO_IMAGE \
  --prompt "YOUR ENHANCED EDIT INSTRUCTION" \
  --model "gemini-3.1-flash-image-preview"
```

### Edit with reference images

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/edit.py \
  --image PATH_TO_PRIMARY_IMAGE \
  --reference PATH_TO_STYLE_REF \
  --reference PATH_TO_COLOR_REF \
  --prompt "Apply the warm color grading from the first reference and the composition style from the second reference to the primary image" \
  --model "gemini-3.1-flash-image-preview"
```

**All flags:**

| Flag | Required | Default | Notes |
|------|:--------:|---------|-------|
| `--image` | Yes | — | Primary image (highest weight) |
| `--reference` | No | — | Reference image(s), repeatable, max 13 |
| `--prompt` | Yes | — | |
| `--model` | No | `gemini-3.1-flash-image-preview` | |
| `--output-dir` | No | `./nanobanana_generated` (CWD) | |
| `--api-key` | No | `$GOOGLE_AI_API_KEY` env | |

Note: `edit.py` does not support `--resolution` — output resolution matches the source image.

**JSON output on success:**
```json
{"path": "./nanobanana_generated/banana_edit_TIMESTAMP.png", "model": "...", "source": "...", "text": "..."}
```
With references: adds `"references": ["path1", "path2"]` to the output.

On error: `{"error": true, "message": "..."}` with non-zero exit code.

See SKILL.md → Gemini-Specific Errors for `IMAGE_SAFETY` and `PROHIBITED_CONTENT` handling. HTTP 429 — scripts retry automatically (exponential backoff, 3 attempts).

---

## Multi-Image Edit Use Cases

| Use Case | Reference Strategy | Prompt Pattern |
|----------|-------------------|----------------|
| **Style transfer** | 1 style reference | "Apply the visual style, lighting, and color palette from the reference image to the primary image" |
| **Color matching** | 1 color reference | "Match the color grading and tonal range of the reference image" |
| **Element composition** | 1+ element references | "Incorporate the [object] from the reference into the primary image, matching perspective and lighting" |
| **Character consistency** | 1-4 character references | "Maintain the facial features and clothing style shown in the reference images" |
| **Brand alignment** | 1 brand reference | "Adjust the primary image to match the brand aesthetic shown in the reference" |

**Important:** Image order matters. The primary image (`--image`) is always first and has the highest weight. References are added in the order specified. Describe in the prompt which reference provides what (e.g., "first reference for style, second for color").
