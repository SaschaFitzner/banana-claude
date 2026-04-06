# Workflow: Generate

> **Prerequisites:** If not already loaded, read `references/gemini-models.md` and `references/prompt-core.md` before Step 4. After Step 3, load the matching mode file from `references/modes/`.

---

## Step 1: Analyze Intent and Determine Path

**Fast-path** (concrete subject, no brand context — skip to Step 4):
Infer smart defaults and proceed directly to prompt construction.
- Domain mode from subject: person/character → Portrait, product/packshot → Product, dramatic scene/story → Cinema, environment/nature → Landscape, fashion/lifestyle → Editorial, icon/UI element → UI/Web, brand mark → Logo, pattern/texture → Abstract, data/diagram → Infographic, website/landing page/homepage/dashboard/web design/mockup/wireframe/page layout → Website Design
- Aspect ratio: `1:1` default. Infer from keywords: banner/header → `16:9`, story/reel → `9:16`, poster/pin → `2:3`, print/photo → `3:2`, product shot → `4:3`, landing page/website/homepage/dashboard/web design → `9:16`
- Resolution: `2K` (except Website Design, UI/Web, Infographic → `1K`), Model: `gemini-3.1-flash-image-preview`

**Standard-path** (vague or abstract subject):
Ask at most 1-2 targeted questions to clarify the output type or use case, then proceed.
- What type of image? (photo, illustration, logo, icon)
- What is the primary use case? (web, social, print)

NEVER ask about use case, style, brand, AND mood all at once. Prefer generating and iterating.

---

## Step 2: Check for Presets

If the user mentions a brand name or style preset, check `~/.banana/presets/`:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/presets.py list
```
If a matching preset exists, load it with `presets.py show NAME` and use its values as defaults for the Reasoning Brief. User instructions override preset values. See `references/presets.md` for preset schema.

---

## Step 3: Select Domain Mode

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
| **Website Design** | Landing pages, homepages, dashboards, web mockups, page concepts | Layout composition, typography hierarchy, color system, design anchors, content density, fullscreen framing (no browser chrome) |

**Website Design vs. UI/Web:** UI/Web mode creates individual components
(icons, illustrations, buttons, app assets). Website Design mode creates
full-page website screenshots with dense, information-rich layouts.
Keywords: "icon", "illustration", "asset", "button" → UI/Web.
Keywords: "landing page", "website", "homepage", "dashboard" → Website Design.

---

## Step 4: Construct Reasoning Brief

Build the prompt using the **5-Component Formula** from `references/prompt-core.md`.

**The 5 Components:** Subject → Action → Location/Context → Composition → Style (includes lighting)

**CRITICAL RULES:**
- Name real cameras: "Sony A7R IV", "Canon EOS R5", "iPhone 16 Pro Max"
- Name real brands for styling: "Lululemon", "Tom Ford" (triggers visual associations)
- Include micro-details: "sweat droplets on collarbones", "baby hairs stuck to neck"
- Use prestigious context anchors: "Vanity Fair editorial", "National Geographic cover"
- NEVER use banned keywords (see `references/prompt-core.md` → BANNED PROMPT KEYWORDS) — use `imageSize` param instead
- NEVER write "a dark-themed ad showing..." — describe the SCENE, not the concept
- For critical constraints use ALL CAPS: "MUST contain exactly three figures"
- For products: say "prominently displayed" to ensure visibility

For domain-specific templates, see the mode file loaded in Step 3 (`references/modes/`) → Prompt Templates.

---

## Step 5: Select Aspect Ratio

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

## Step 6: Select Resolution

| `imageSize` | When to use |
|-------------|-------------|
| `512` | Quick drafts, rapid iteration |
| `1K` | Budget-conscious, web thumbnails, social media |
| `2K` | **Default** — quality assets, most use cases |
| `4K` | Print production, hero images, final deliverables |

ALWAYS pass `imageSize` explicitly — the API defaults to `1K` if omitted. Values MUST be UPPERCASE.

---

## Step 7: Execute Generation

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
| `--output-dir` | No | `./nanobanana_generated` (CWD) |
| `--api-key` | No | `$GOOGLE_AI_API_KEY` env |

**JSON output on success:**
```json
{"path": "./nanobanana_generated/banana_TIMESTAMP.png", "model": "...", "aspect_ratio": "...", "resolution": "...", "text": "..."}
```
On error: `{"error": true, "message": "..."}` with non-zero exit code.

NEVER report success until a valid image file path is confirmed to exist.

---

## Step 8: Post-Processing

After generation, apply post-processing if the user needs it. Check tools before running:
```bash
which magick || which convert || echo "ImageMagick not installed"
```
Use `magick` (v7) if available, fall back to `convert` (v6). See `references/post-processing.md` for full pipeline including green screen transparency workaround.

---

## Error Recovery

| Error | Action |
|-------|--------|
| `IMAGE_SAFETY` | Rephrase using Safety Rephrase strategies in `references/prompt-core.md`. NEVER auto-retry without user approval. Max 3 rephrase attempts. |
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
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log --model gemini-3.1-flash-image-preview --resolution 2K --prompt "brief description"
```
See `references/cost-tracking.md` for pricing table.
