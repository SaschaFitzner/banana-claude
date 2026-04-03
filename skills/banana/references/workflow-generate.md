# Workflow: Generate

> Read `gemini-models.md` and `prompt-engineering.md` first before executing this workflow.

## Table of Contents

1. [Step 1: Analyze Intent](#step-1-analyze-intent)
2. [Step 1.5: Check for Presets](#step-15-check-for-presets)
3. [Step 2: Select Domain Mode](#step-2-select-domain-mode)
4. [Step 3: Construct Reasoning Brief](#step-3-construct-reasoning-brief)
5. [Step 4: Select Aspect Ratio](#step-4-select-aspect-ratio)
6. [Step 4.5: Select Resolution](#step-45-select-resolution)
7. [Step 5: Execute Generation](#step-5-execute-generation)
8. [Step 6: Post-Processing](#step-6-post-processing)
9. [Error Recovery](#error-recovery)
10. [Model Routing](#model-routing)
11. [Cost Tracking](#cost-tracking)

---

## Step 1: Analyze Intent

Determine what the user actually needs:
- What is the final use case? (blog, social, app, print, presentation)
- What style fits? (photorealistic, illustrated, minimal, editorial)
- What constraints exist? (brand colors, dimensions, transparency)
- What mood/emotion should it convey?

NEVER pass raw user text to the API. If request is vague (e.g., "make me a hero image"), ASK clarifying questions about use case, style preference, and brand context before generating.

---

## Step 1.5: Check for Presets

If the user mentions a brand name or style preset, check `~/.banana/presets/`:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/presets.py list
```
If a matching preset exists, load it with `presets.py show NAME` and use its values as defaults for the Reasoning Brief. User instructions override preset values. See `references/presets.md` for preset schema.

---

## Step 2: Select Domain Mode

Choose the expertise lens that best fits the request:

| Mode | When to use | Prompt emphasis |
|------|-------------|-----------------|
| **Cinema** | Dramatic scenes, storytelling, mood pieces | Camera specs, lens, film stock, lighting setup |
| **Product** | E-commerce, packshots, merchandise | Surface materials, studio lighting, angles, clean BG |
| **Portrait** | People, characters, headshots, avatars | Facial features, expression, pose, lens choice |
| **Editorial** | Fashion, magazine, lifestyle | Styling, composition, publication reference |
| **UI/Web** | Icons, illustrations, app assets | Clean vectors, flat design, brand colors, sizing |
| **Logo** | Branding, marks, identity | Geometric construction, minimal palette, scalability |
| **Landscape** | Environments, backgrounds, wallpapers | Atmospheric perspective, depth layers, time of day |
| **Abstract** | Patterns, textures, generative art | Color theory, mathematical forms, movement |
| **Infographic** | Data visualization, diagrams, charts | Layout structure, text rendering, hierarchy |

---

## Step 3: Construct Reasoning Brief

Build the prompt using the **5-Component Formula** from `references/prompt-engineering.md`.

**The 5 Components:** Subject → Action → Location/Context → Composition → Style (includes lighting)

**CRITICAL RULES:**
- Name real cameras: "Sony A7R IV", "Canon EOS R5", "iPhone 16 Pro Max"
- Name real brands for styling: "Lululemon", "Tom Ford" (triggers visual associations)
- Include micro-details: "sweat droplets on collarbones", "baby hairs stuck to neck"
- Use prestigious context anchors: "Vanity Fair editorial," "National Geographic cover"
- NEVER use banned keywords (see Quick Reference in SKILL.md) — use `imageSize` param instead
- NEVER write "a dark-themed ad showing..." — describe the SCENE, not the concept
- For critical constraints use ALL CAPS: "MUST contain exactly three figures"
- For products: say "prominently displayed" to ensure visibility

### Template — Photorealistic / Ads

```
[Subject: age + appearance + expression], wearing [outfit with brand/texture],
[action verb] in [specific location + time]. [Micro-detail about skin/hair/
sweat/texture]. Captured with [camera model], [focal length] lens at [f-stop],
[lighting description]. [Prestigious context: "Vanity Fair editorial" /
"Pulitzer Prize-winning cover photograph"].
```

### Template — Product / Commercial

```
[Product with brand name] with [dynamic element: condensation/splashes/glow],
[product detail: "logo prominently displayed"], [surface/setting description].
[Supporting visual elements: light rays, particles, reflections].
Commercial photography for an advertising campaign. [Publication reference:
"Bon Appetit feature spread" / "Wallpaper* design editorial"].
```

### Template — Illustrated / Stylized

```
A [art style] [format] of [subject with character detail], featuring
[distinctive characteristics] with [color palette]. [Line style] and
[shading technique]. Background is [description]. [Mood/atmosphere].
```

### Template — Text-Heavy Assets (keep text under 25 characters)

```
A [asset type] with the text "[exact text]" in [descriptive font style],
[placement and sizing]. [Layout structure]. [Color scheme]. [Visual
context and supporting elements].
```

For more templates see `references/prompt-engineering.md` → Proven Prompt Templates.

---

## Step 4: Select Aspect Ratio

Pass `--aspect-ratio` flag to `generate.py`:

| Use Case | Ratio |
|----------|-------|
| Social post / avatar | `1:1` |
| Blog header / YouTube thumb | `16:9` |
| Story / Reel / mobile | `9:16` |
| Portrait / book cover | `3:4` |
| Product shot | `4:3` |
| DSLR print / photo standard | `3:2` |
| Pinterest pin / poster | `2:3` |
| Instagram portrait | `4:5` |
| Large format photography | `5:4` |
| Website banner | `4:1` or `8:1` |
| Ultrawide / cinematic | `21:9` |

---

## Step 4.5: Select Resolution

| `imageSize` | When to use |
|-------------|-------------|
| `512` | Quick drafts, rapid iteration |
| `1K` | Budget-conscious, web thumbnails, social media |
| `2K` | **Default** — quality assets, most use cases |
| `4K` | Print production, hero images, final deliverables |

ALWAYS pass `imageSize` explicitly — the API defaults to `1K` if omitted. Values MUST be UPPERCASE.

---

## Step 5: Execute Generation

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py \
  --prompt "YOUR CONSTRUCTED PROMPT" \
  --aspect-ratio "16:9" \
  --resolution "2K" \
  --model "gemini-3.1-flash-image-preview"
```

**All flags:**

| Flag | Required | Default |
|------|:--------:|---------|
| `--prompt` | Yes | — |
| `--aspect-ratio` | No | `1:1` |
| `--resolution` | No | `2K` |
| `--model` | No | `gemini-3.1-flash-image-preview` |
| `--thinking` | No | none |
| `--image-only` | No | false |
| `--api-key` | No | `$GOOGLE_AI_API_KEY` env |

**JSON output on success:**
```json
{"path": "~/Documents/nanobanana_generated/banana_TIMESTAMP.png", "model": "...", "aspect_ratio": "...", "resolution": "...", "text": "..."}
```
On error: `{"error": true, "message": "..."}` with non-zero exit code.

Scripts handle 429 retries internally (exponential backoff, max 3 attempts).

NEVER report success until a valid image file path is confirmed to exist.

---

## Step 6: Post-Processing

After generation, apply post-processing if the user needs it. Check tools before running:
```bash
which magick || which convert || echo "ImageMagick not installed"
```
Use `magick` (v7) if available, fall back to `convert` (v6). See `references/post-processing.md` for full pipeline including green screen transparency workaround.

---

## Error Recovery

| Error | Action |
|-------|--------|
| `IMAGE_SAFETY` | Rephrase using Safety Rephrase strategies in `references/prompt-engineering.md`. NEVER auto-retry without user approval. Max 3 rephrase attempts. |
| `PROHIBITED_CONTENT` | Topic blocked by Google. Non-retryable — explain why, suggest alternatives. |
| Empty response (no image) | Verify `responseModalities` includes "IMAGE". Retry once. |
| HTTP 429 | Scripts retry automatically (exponential backoff, 3 attempts). If persistent, wait 60s. |
| HTTP 400 `FAILED_PRECONDITION` | Billing not enabled. User must enable at https://aistudio.google.com/apikey |

---

## Model Routing

| Scenario | Model | Resolution | Brief Level |
|----------|-------|-----------|-------------|
| Quick draft | `gemini-2.5-flash-image` | 512/1K | 3-component (Subject+Context+Style) |
| Standard | `gemini-3.1-flash-image-preview` | 2K | Full 5-component |
| Quality | `gemini-3.1-flash-image-preview` | 2K/4K | 5-component + prestigious anchors |
| Text-heavy | `gemini-3.1-flash-image-preview` | 2K | 5-component, `--thinking high` |
| Batch/bulk | Any model | 1K | 5-component, sequential generate.py calls |

Default: `gemini-3.1-flash-image-preview`. Pass `--model gemini-2.5-flash-image` for budget routing.

---

## Cost Tracking

After EVERY successful generation, log it:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log --model MODEL --resolution RES --prompt "brief description"
```
Before batch operations, show the estimate first. See `references/cost-tracking.md` for pricing table.
