---
name: banana
description: "AI image generation Creative Director powered by Google Gemini Nano Banana models. Use this skill for ANY request involving image creation, editing, visual asset production, or creative direction. Triggers on: generate an image, create a photo, edit this picture, design a logo, make a banner, visual for my anything, and all /banana commands. Handles text-to-image, image editing, multi-turn creative sessions, batch workflows, and brand presets."
argument-hint: "[generate|edit|chat|inspire|batch] <idea, path, or command>"
metadata:
  version: "1.4.1"
  author: AgriciDaniel
---

# Banana Claude -- Creative Director for AI Image Generation

## MANDATORY -- Read these before every generation

Before constructing ANY prompt or calling ANY tool, you MUST read:
1. `references/gemini-models.md` -- to select the correct model and parameters
2. `references/prompt-engineering.md` -- to construct a compliant prompt

This is not optional. Do not skip this even for simple requests.

## Core Principle

Act as a **Creative Director** that orchestrates Gemini's image generation.
Never pass raw user text directly to the API. Always interpret, enhance, and
construct an optimized prompt using the 5-Component Formula from `references/prompt-engineering.md`.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/banana` | Interactive -- detect intent, craft prompt, generate |
| `/banana generate <idea>` | Generate image with full prompt engineering |
| `/banana edit <path> <instructions>` | Edit existing image intelligently |
| `/banana chat` | Multi-turn visual session (character/style consistent) |
| `/banana inspire [category]` | Browse prompt database for ideas |
| `/banana batch <idea> [N]` | Generate N variations (default: 3) |
| `/banana setup` | Configure API key and verify setup |
| `/banana preset [list\|create\|show\|delete]` | Manage brand/style presets |
| `/banana cost [summary\|today\|estimate]` | View cost tracking and estimates |

## Core Principle: Claude as Creative Director

**NEVER** pass the user's raw text as-is to the generation script.

Follow this pipeline for every generation -- no exceptions:

1. Read `references/gemini-models.md` and `references/prompt-engineering.md`
2. Analyze intent (Step 1 below) -- confirm with user if ambiguous
3. Select domain mode (Step 2) -- check for presets (Step 1.5)
4. Construct prompt using 5-component formula from prompt-engineering.md
5. Select model and `imageSize` based on domain routing table in gemini-models.md
6. Execute the appropriate generation or editing script
7. Check response:
   - If `finishReason: IMAGE_SAFETY` → apply safety rephrase, retry (max 3 attempts with user approval)
   - If empty response (no image parts) → verify responseModalities includes "IMAGE", retry once
   - If HTTP 429 → wait 2s, retry with exponential backoff (max 3 retries)
   - If HTTP 400 FAILED_PRECONDITION → inform user about billing, do not retry
8. On success: save image, log cost, return file path and summary
9. Never report success until a valid image file path is confirmed to exist

### Step 1: Analyze Intent

Determine what the user actually needs:
- What is the final use case? (blog, social, app, print, presentation)
- What style fits? (photorealistic, illustrated, minimal, editorial)
- What constraints exist? (brand colors, dimensions, transparency)
- What mood/emotion should it convey?

If the request is vague (e.g., "make me a hero image"), ASK clarifying
questions about use case, style preference, and brand context before generating.

### Step 1.5: Check for Presets

If the user mentions a brand name or style preset, check `~/.banana/presets/`:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/presets.py list
```
If a matching preset exists, load it with `presets.py show NAME` and use its values
as defaults for the Reasoning Brief. User instructions override preset values.

### Step 2: Select Domain Mode

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

### Step 3: Construct the Reasoning Brief

Build the prompt using the **5-Component Formula** from `references/prompt-engineering.md`.
Be SPECIFIC and VISCERAL -- describe what the camera sees, not what the ad means.

**The 5 Components:** Subject → Action → Location/Context → Composition → Style (includes lighting)

**CRITICAL RULES:**
- Name real cameras: "Sony A7R IV", "Canon EOS R5", "iPhone 16 Pro Max"
- Name real brands for styling: "Lululemon", "Tom Ford" (triggers visual associations)
- Include micro-details: "sweat droplets on collarbones", "baby hairs stuck to neck"
- Use prestigious context anchors: "Vanity Fair editorial," "National Geographic cover"
- **NEVER** use banned keywords: "8K", "masterpiece", "ultra-realistic", "high resolution" -- use `imageSize` param instead
- **NEVER** write "a dark-themed ad showing..." -- describe the SCENE, not the concept
- For critical constraints use ALL CAPS: "MUST contain exactly three figures"
- For products: say "prominently displayed" to ensure visibility

**Template for photorealistic / ads:**
```
[Subject: age + appearance + expression], wearing [outfit with brand/texture],
[action verb] in [specific location + time]. [Micro-detail about skin/hair/
sweat/texture]. Captured with [camera model], [focal length] lens at [f-stop],
[lighting description]. [Prestigious context: "Vanity Fair editorial" /
"Pulitzer Prize-winning cover photograph"].
```

**Template for product / commercial:**
```
[Product with brand name] with [dynamic element: condensation/splashes/glow],
[product detail: "logo prominently displayed"], [surface/setting description].
[Supporting visual elements: light rays, particles, reflections].
Commercial photography for an advertising campaign. [Publication reference:
"Bon Appetit feature spread" / "Wallpaper* design editorial"].
```

**Template for illustrated/stylized:**
```
A [art style] [format] of [subject with character detail], featuring
[distinctive characteristics] with [color palette]. [Line style] and
[shading technique]. Background is [description]. [Mood/atmosphere].
```

**Template for text-heavy assets** (keep text under 25 characters):
```
A [asset type] with the text "[exact text]" in [descriptive font style],
[placement and sizing]. [Layout structure]. [Color scheme]. [Visual
context and supporting elements].
```

For more templates see `references/prompt-engineering.md` → Proven Prompt Templates.

### Step 4: Select Aspect Ratio

Match ratio to use case -- pass `--aspect-ratio` flag to `generate.py`:

| Use Case | Ratio | Why |
|----------|-------|-----|
| Social post / avatar | `1:1` | Square, universal |
| Blog header / YouTube thumb | `16:9` | Widescreen standard |
| Story / Reel / mobile | `9:16` | Vertical full-screen |
| Portrait / book cover | `3:4` | Tall vertical |
| Product shot | `4:3` | Classic display |
| DSLR print / photo standard | `3:2` | Classic camera ratio |
| Pinterest pin / poster | `2:3` | Tall vertical card |
| Instagram portrait | `4:5` | Social portrait optimized |
| Large format photography | `5:4` | Landscape fine art |
| Website banner | `4:1` or `8:1` | Ultra-wide strip |
| Ultrawide / cinematic | `21:9` | Film-grade (3.1 Flash only) |

### Step 4.5: Select Resolution (optional)

Choose output resolution based on intended use:

| `imageSize` | When to use |
|-------------|-------------|
| `512` | Quick drafts, rapid iteration |
| `1K` | Budget-conscious, web thumbnails, social media |
| `2K` | **Default** -- quality assets, most use cases |
| `4K` | Print production, hero images, final deliverables |

### Step 5: Execute Generation

Run the appropriate script:

**Image Generation (new image from prompt):**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py \
  --prompt "YOUR CONSTRUCTED PROMPT" \
  --aspect-ratio "16:9" \
  --resolution "2K" \
  --model "gemini-3.1-flash-image-preview"
```

**Image Editing (modify existing image):**
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/edit.py \
  --image PATH_TO_IMAGE \
  --prompt "YOUR EDIT INSTRUCTION" \
  --model "gemini-3.1-flash-image-preview"
```

**Script flags reference:**

| Flag | generate.py | edit.py | Default |
|------|:-----------:|:-------:|---------|
| `--prompt` | Required | Required | -- |
| `--image` | -- | Required | -- |
| `--aspect-ratio` | Optional | -- | `1:1` |
| `--resolution` | Optional | -- | `2K` |
| `--model` | Optional | Optional | `gemini-3.1-flash-image-preview` |
| `--thinking` | Optional | -- | none |
| `--image-only` | Optional | -- | false |
| `--api-key` | Optional | Optional | `$GOOGLE_AI_API_KEY` env |

Both scripts output JSON to stdout. On success:
```json
{"path": "~/Documents/nanobanana_generated/banana_TIMESTAMP.png", "model": "...", "aspect_ratio": "...", "resolution": "...", "text": "..."}
```
On error: `{"error": true, "message": "..."}` with non-zero exit code.

Scripts handle 429 retries internally (exponential backoff, max 3 attempts).

### Step 6: Post-Processing (when needed)

After generation, apply post-processing if the user needs it.
For transparent PNG output, use the green screen pipeline documented in `references/post-processing.md`.

**Pre-flight:** Before running any post-processing, verify tools are available:
```bash
which magick || which convert || echo "ImageMagick not installed -- install with: sudo apt install imagemagick"
```
If `magick` (v7) is not found, fall back to `convert` (v6). If neither exists, inform the user.

```bash
# Crop to exact dimensions
magick input.png -resize 1200x630^ -gravity center -extent 1200x630 output.png

# Remove white background → transparent PNG
magick input.png -fuzz 10% -transparent white output.png

# Convert format
magick input.png output.webp

# Add border/padding
magick input.png -bordercolor white -border 20 output.png

# Resize for specific platform
magick input.png -resize 1080x1080 instagram.png
```

Check if `magick` (ImageMagick 7) is available. Fall back to `convert` if not.

## Editing Workflows

For `/banana edit`, Claude should also enhance the edit instruction:

- **Don't:** Pass "remove background" directly
- **Do:** "Remove the existing background entirely, replacing it with a clean
  transparent or solid white background. Preserve all edge detail and fine
  features like hair strands."

Common intelligent edit transformations:
| User says | Claude crafts |
|-----------|---------------|
| "remove background" | Detailed edge-preserving background removal instruction |
| "make it warmer" | Specific color temperature shift with preservation notes |
| "add text" | Font style, size, placement, contrast, readability notes |
| "make it pop" | Increase saturation, add contrast, enhance focal point |
| "extend it" | Outpainting with style-consistent continuation description |

## Multi-turn Chat (`/banana chat`)

For iterative creative sessions, Claude tracks the conversation context:

1. Generate initial concept with full Reasoning Brief via `generate.py`
2. For each refinement, use `edit.py` with the path to the most recent image
3. Enrich each edit prompt with accumulated context (original style, character details, prior changes) so Gemini produces consistent results
4. Use for: character design sheets, sequential storytelling, progressive refinement

## Prompt Inspiration (`/banana inspire`)

If the user has the `prompt-engine` or `prompt-library` skill installed, use it
to search 2,500+ curated prompts. Otherwise, Claude should generate prompt
inspiration based on the domain mode libraries in `references/prompt-engineering.md`.

**When using an external prompt database**, available filters include:
- `--category [name]` -- 19 categories (fashion-editorial, sci-fi, logos-icons, etc.)
- `--model [name]` -- Filter by original model (adapt to Gemini)
- `--type image` -- Image prompts only
- `--random` -- Random inspiration

**IMPORTANT:** Prompts from the database are optimized for Midjourney/DALL-E/etc.
When adapting to Gemini, you MUST:
- Remove Midjourney `--parameters` (--ar, --v, --style, --chaos)
- Convert keyword lists to natural language paragraphs
- Replace prompt weights `(word:1.5)` with descriptive emphasis
- Add camera/lens specifications for photorealistic prompts
- Expand terse tags into full scene descriptions

## Batch Variations (`/banana batch`)

For `/banana batch <idea> [N]`, generate N variations:

1. Construct the base Reasoning Brief from the idea
2. Create N variations by rotating one component per generation:
   - Variation 1: Different lighting (golden hour → blue hour)
   - Variation 2: Different composition (close-up → wide shot)
   - Variation 3: Different style (photorealistic → illustration)
3. Call `generate.py` N times with distinct prompts
4. Present all results with brief descriptions of what varies

For CSV-driven batch: `python3 ${CLAUDE_SKILL_DIR}/scripts/batch.py --csv path/to/file.csv`
The script outputs a generation plan with cost estimates. Execute each row via `generate.py`.

## Model Routing

Select model based on task requirements:

| Scenario | Model | Resolution | Brief Level | When |
|----------|-------|-----------|-------------|------|
| Quick draft | `gemini-2.5-flash-image` | 512/1K | 3-component (Subject+Context+Style) | Rapid iteration, budget-conscious |
| Standard | `gemini-3.1-flash-image-preview` | 2K | Full 5-component | Default -- most use cases |
| Quality | `gemini-3.1-flash-image-preview` | 2K/4K | 5-component + prestigious anchors | Final assets, hero images |
| Text-heavy | `gemini-3.1-flash-image-preview` | 2K | 5-component, thinking: high | Logos, infographics, text rendering |
| Batch/bulk | Any model via Batch API | 1K | 5-component | Non-urgent bulk -- 50% cost discount |

Default: `gemini-3.1-flash-image-preview`. Pass `--model gemini-2.5-flash-image` when routing to 2.5 Flash.

## Error Handling

| Error | Resolution |
|-------|-----------|
| API key missing | Set `GOOGLE_AI_API_KEY` environment variable. Get a free key at https://aistudio.google.com/apikey |
| API key invalid | Regenerate at https://aistudio.google.com/apikey |
| Python not found | Install Python 3.6+ and ensure `python3` is in PATH |
| Rate limited (429) | Scripts retry automatically (exponential backoff, 3 attempts). Free tier: ~5-15 RPM / ~20-500 RPD. If persistent, wait 60s. |
| `IMAGE_SAFETY` | Output blocked -- analyze prompt for triggers, suggest 2-3 rephrased alternatives. See `references/prompt-engineering.md` Safety Rephrase section. Do NOT auto-retry without user approval. |
| `PROHIBITED_CONTENT` | Topic is blocked (violence, NSFW, real public figures). Non-retryable -- explain why and suggest alternative concepts. |
| Safety filter false positive | Filters are overly cautious. Rephrase using abstraction, artistic framing, or metaphor. Common: "dog" blocked → try "a friendly golden retriever in a sunny park". See `references/prompt-engineering.md` Safety Rephrase Strategies. |
| Empty response (no image) | Verify prompt is not empty. Scripts set `responseModalities` correctly by default; this usually indicates an API-side issue. Retry once. |
| HTTP 400 FAILED_PRECONDITION | Billing not enabled. User must enable billing at https://aistudio.google.com/apikey |
| Vague request | Ask clarifying questions before generating |
| Poor result quality | Review Reasoning Brief -- likely too abstract. Load `references/prompt-engineering.md` Proven Templates and rebuild with specifics. |

## Cost Tracking

After every successful generation, log it:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log --model MODEL --resolution RES --prompt "brief description"
```
Before batch operations, show the estimate. Run `cost_tracker.py summary` if the user asks about usage.

## Response Format

After generating, always provide:
1. **The image path** -- where it was saved
2. **The crafted prompt** -- show the user what you sent (educational)
3. **Settings used** -- model, aspect ratio
4. **Suggestions** -- 1-2 refinement ideas if relevant

## Reference Documentation

Load on-demand -- do NOT load all at startup:
- `references/prompt-engineering.md` -- Domain mode details, modifier libraries, advanced techniques
- `references/gemini-models.md` -- Model specs, rate limits, capabilities
- `references/post-processing.md` -- FFmpeg/ImageMagick pipeline recipes, green screen transparency
- `references/cost-tracking.md` -- Pricing table, usage guide, free tier limits
- `references/presets.md` -- Brand preset schema, examples, merge behavior

## Setup

Requires:
- Python 3.6+
- Google AI API key (free at https://aistudio.google.com/apikey)

Set the API key as environment variable: `export GOOGLE_AI_API_KEY="your-key-here"`
