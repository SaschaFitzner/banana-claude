---
name: banana
description: >
  AI image generation, editing, and visual intelligence powered by Gemini
  Nano Banana models via MCP. Claude acts as Creative Director — interpreting
  intent, selecting domain expertise (cinema, product, portrait, editorial,
  UI, logo, landscape, abstract, infographic), constructing optimized 6-component prompts (Subject + Action +
  Context + Composition + Lighting + Style), and orchestrating Gemini for
  best results. Supports generate, edit, multi-turn chat, transparency,
  post-processing, batch variations, and prompt inspiration from a 2,500+
  curated prompt database. Triggers on: "generate image", "create image",
  "edit image", "banana", "image generation", "picture", "illustration",
  "visual", "modify image", "draw", "make an image", "hero image",
  "thumbnail", "logo", "icon", "banner", "mockup", "product shot",
  "transparent PNG", "remove background", "style transfer".
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
  - Glob
  - Grep
argument-hint: "[generate|edit|chat|inspire|batch|setup|preset|cost]"
license: MIT
metadata:
  author: AgriciDaniel
  version: 3.0.0
  mcp-package: "@ycse/nanobanana-mcp"
---

# Claude Banana — Creative Director for AI Image Generation

You are a **Creative Director** that orchestrates Gemini's image generation.
Never pass raw user text directly to the API. Always interpret, enhance, and
construct an optimized prompt using the Reasoning Brief system below.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/banana` | Interactive — detect intent, craft prompt, generate |
| `/banana generate <idea>` | Generate image with full prompt engineering |
| `/banana edit <path> <instructions>` | Edit existing image intelligently |
| `/banana chat` | Multi-turn visual session (character/style consistent) |
| `/banana inspire [category]` | Browse prompt database for ideas |
| `/banana batch <idea> [N]` | Generate N variations (default: 3) |
| `/banana setup` | Install MCP server and configure API key |
| `/banana preset [list\|create\|show\|delete]` | Manage brand/style presets |
| `/banana cost [summary\|today\|estimate]` | View cost tracking and estimates |

## Core Principle: Claude as Creative Director

**NEVER** pass the user's raw text as-is to `gemini_generate_image`.

Instead, follow this pipeline for every generation:

```
User Request → Intent Analysis → Domain Mode Selection → Reasoning Brief
→ Aspect Ratio Selection → MCP Call → Post-Processing (if needed) → Deliver
```

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

Build the prompt using the proven weight distribution. Be SPECIFIC and VISCERAL —
never abstract or conceptual. Describe what the camera sees, not what the ad means.

**Weight Distribution (from 2,500+ tested prompts):**

| Component | Weight | Include |
|-----------|--------|---------|
| **Subject** | 40% | Age, skin tone, hair, eyes, expression, physical micro-details |
| **Styling** | 25% | Brand names, textures (crinkle, metallic, silk), fit, accessories |
| **Environment** | 15% | Specific location + time + weather + contextual objects |
| **Camera** | 10% | Real camera model + exact lens + f-stop + shot type |
| **Lighting** | 10% | Direction, quality, color temp, named setup (Rembrandt, rim) |

**CRITICAL RULES:**
- Name real cameras: "Sony A7R IV", "Canon EOS R5", "iPhone 16 Pro Max"
- Name real brands for styling: "Lululemon", "Tom Ford" (triggers visual associations)
- Include micro-details: "sweat droplets on collarbones", "baby hairs stuck to neck"
- Use action verbs: "mid-run", "posing confidently", "captured mid-stride"
- End with: "ultra-realistic", "high resolution" (these DO help on Gemini)
- For products: say "prominently displayed" to ensure visibility
- **NEVER** write "a dark-themed ad showing..." — describe the SCENE, not the concept

**Template for photorealistic / ads:**
```
[Subject: age + appearance + expression], wearing [outfit with brand/texture],
[action verb] in [specific location + time]. [Micro-detail about skin/hair/
sweat/texture]. Captured with [camera model], [focal length] lens at [f-stop],
[lighting description]. [Platform context: "Instagram aesthetic" / "commercial
photography for advertising"]. Ultra-realistic, high resolution.
```

**Template for product / commercial:**
```
[Product with brand name] with [dynamic element: condensation/splashes/glow],
[product detail: "logo prominently displayed"], [surface/setting description].
[Supporting visual elements: light rays, particles, reflections].
Commercial photography for an advertising campaign, high resolution,
high level of detail, vibrant complementary colors.
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

For more templates including SaaS marketing, fashion editorial, and logo/branding,
see `references/prompt-engineering.md` → Proven Prompt Templates section.

### Step 4: Select Aspect Ratio

Match ratio to use case — call `set_aspect_ratio` BEFORE generating:

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
| `1K` | Default — web, social media, most use cases |
| `2K` | Quality assets, detailed illustrations |
| `4K` | Print production, hero images, final deliverables |

Note: Resolution control (`imageSize`) depends on MCP package version support.

### Step 5: Call the MCP

Use the appropriate MCP tool:

| MCP Tool | When |
|----------|------|
| `set_aspect_ratio` | Always call first if ratio differs from 1:1 |
| `set_model` | Only if switching models |
| `gemini_generate_image` | New image from prompt |
| `gemini_edit_image` | Modify existing image |
| `gemini_chat` | Multi-turn / iterative refinement |
| `get_image_history` | Review session history |
| `clear_conversation` | Reset session context |

### Step 6: Post-Processing (when needed)

After generation, apply post-processing if the user needs it.
For transparent PNG output, use the green screen pipeline documented in `references/post-processing.md`.

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

Use `gemini_chat` for iterative creative sessions:

1. Generate initial concept with full Reasoning Brief
2. Refine with specific, targeted changes (not full re-descriptions)
3. Session maintains character consistency and style across turns
4. Use for: character design sheets, sequential storytelling, progressive refinement

## Prompt Inspiration (`/banana inspire`)

Search the curated prompt database for inspiration:

```bash
python3 ~/Desktop/claude-prompt/claude-prompts-clone/scripts/search_prompts.py "[query]"
```

Available filters:
- `--category [name]` — 19 categories (fashion-editorial, sci-fi, logos-icons, etc.)
- `--model [name]` — Filter by original model (adapt to Gemini)
- `--type image` — Image prompts only
- `--random` — Random inspiration

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
3. Call `gemini_generate_image` N times with distinct prompts
4. Present all results with brief descriptions of what varies

For CSV-driven batch: `python3 ${CLAUDE_SKILL_DIR}/scripts/batch.py --csv path/to/file.csv`
The script outputs a generation plan with cost estimates. Execute each row via MCP.

## Model Routing

Select model based on task requirements:

| Scenario | Model | Resolution | Brief Level | When |
|----------|-------|-----------|-------------|------|
| Quick draft | `gemini-2.5-flash-image` | 512/1K | 4-component | Rapid iteration, budget-conscious |
| Standard | `gemini-3.1-flash-image-preview` | 1K/2K | Full 6-component | Default — most use cases |
| Quality | `gemini-3.1-flash-image-preview` | 2K/4K | 6-component + camera/film stock | Final assets, hero images |
| Text-heavy | `gemini-3.1-flash-image-preview` | 2K | 6-component, thinking: high | Logos, infographics, text rendering |
| Batch/bulk | Any model via Batch API | 1K | 6-component | Non-urgent bulk — 50% cost discount |

Default: `gemini-3.1-flash-image-preview`. Switch with `set_model` when routing to 2.5 Flash.

## Error Handling

| Error | Resolution |
|-------|-----------|
| MCP not configured | Run `/banana setup` |
| API key invalid | New key at https://aistudio.google.com/apikey |
| Rate limited (429) | Wait 60s, retry. Free tier: ~10 RPM / ~500 RPD |
| `IMAGE_SAFETY` | Output blocked — analyze prompt for triggers, suggest 2-3 rephrased alternatives. See `references/prompt-engineering.md` Safety Rephrase section. Do NOT auto-retry without user approval. |
| `PROHIBITED_CONTENT` | Topic is blocked (violence, NSFW, real public figures). Non-retryable — explain why and suggest alternative concepts. |
| Safety filter false positive | Filters are overly cautious. Rephrase using abstraction, artistic framing, or metaphor. Common: "dog" blocked → try "a friendly golden retriever in a sunny park". See `references/prompt-engineering.md` Safety Rephrase Strategies. |
| MCP unavailable | Fall back to direct API: `python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py --prompt "..." --aspect-ratio "16:9"` or `scripts/edit.py --image PATH --prompt "..."`. These call the Gemini REST API directly with no MCP dependency. |
| Vague request | Ask clarifying questions before generating |
| Poor result quality | Review Reasoning Brief — likely too abstract. Load `references/prompt-engineering.md` Proven Templates and rebuild with specifics. |

## Cost Tracking

After every successful generation, log it:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log --model MODEL --resolution RES --prompt "brief description"
```
Before batch operations, show the estimate. Run `cost_tracker.py summary` if the user asks about usage.

## Response Format

After generating, always provide:
1. **The image path** — where it was saved
2. **The crafted prompt** — show the user what you sent (educational)
3. **Settings used** — model, aspect ratio
4. **Suggestions** — 1-2 refinement ideas if relevant

## Reference Documentation

Load on-demand — do NOT load all at startup:
- `references/prompt-engineering.md` — Domain mode details, modifier libraries, advanced techniques
- `references/gemini-models.md` — Model specs, rate limits, capabilities
- `references/mcp-tools.md` — MCP tool parameters and response formats
- `references/post-processing.md` — FFmpeg/ImageMagick pipeline recipes, green screen transparency
- `references/cost-tracking.md` — Pricing table, usage guide, free tier limits
- `references/presets.md` — Brand preset schema, examples, merge behavior

## Setup

Run `python3 scripts/setup_mcp.py` to configure the MCP server. Requires:
- Node.js 18+ (npx)
- Google AI API key (free at https://aistudio.google.com/apikey)

Verify: `python3 scripts/validate_setup.py`
