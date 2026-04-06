# Website Design Mode -- Banana Claude

> Load this when Website Design mode is selected in Step 3.
> Adapted from established frontend design principles for image generation.

## Framing Rule

ALWAYS generate as a fullscreen website screenshot:
- Content fills the entire image edge to edge
- NEVER include browser chrome, URL bar, device frame, monitor bezel, or mockup wrapper
- The image IS the website, not a photo OF a website

## Design Thinking

Before constructing the prompt, commit to a CLEAR aesthetic direction:
- Brutally minimal (Stripe-like)
- Maximalist/editorial (Awwwards experimental)
- Retro-futuristic (Y2K revival)
- Organic/natural (wellness, eco brands)
- Luxury/refined (fashion houses)
- Playful/toy-like (consumer apps)
- Editorial/magazine (content-first)
- Brutalist/raw (developer tools)
- Art deco/geometric (premium services)
- Industrial/utilitarian (B2B SaaS)

The chosen direction drives ALL prompt decisions: typography, color, layout, details.

## Modifier Library

**Page types:** landing page, homepage, dashboard, portfolio, e-commerce PDP,
blog, pricing page, about page, SaaS feature page
**Layout patterns:** hero section + CTA, bento grid, split layout, F-pattern,
Z-pattern, full-bleed imagery, card grid, sticky nav with scroll sections,
feature comparison, testimonial carousel, multi-section scroll
**Typography:** describe characterfully, NEVER generically. "Bold geometric
sans-serif with generous letter-spacing paired with refined serif body text"
beats "clean modern font". Describe hierarchy: "oversized 72px headline,
subtle 16px subtext, micro-label navigation"
**Color strategies:** dominant + sharp accent, monochromatic + pop color,
dark mode editorial, light & airy, earth tones + neon accent, gradient-heavy,
high-contrast black & white
**Design anchors:** Stripe.com, Linear.app, Vercel.com, Pentagram, Apple.com,
Notion.so, Figma.com, Framer showcases, Awwwards winners
**Visual details:** glassmorphism cards, gradient meshes, noise/grain textures,
floating elements, depth layers with shadows, dot-grid patterns, layered
transparencies, decorative borders, grain overlays
**Content density:** dense and information-rich. Visible: navigation bar, hero
with headline + subtext + CTA, feature sections, trust signals/logos,
testimonials, pricing cards, footer. The more real-looking content sections
visible, the better.

## Anti-Patterns

NEVER use these in Website Design prompts:
- "generic website layout" -- describe the SPECIFIC aesthetic
- "professional looking" -- name the DESIGN REFERENCE
- "clean and modern" -- describe WHAT makes it clean
- Standard Bootstrap/Material Design default look
- Symmetrical, predictable layouts without visual tension
- Sparse/empty designs -- websites have content

## Prompt Templates

### SaaS Landing Page

**Pattern:** `"fullscreen website screenshot" + [page type] + [aesthetic direction]
+ [typography description] + [color system] + [layout with multiple sections]
+ [design anchor] + "NO browser chrome, content fills entire frame"`

**Example (Dark SaaS):**
```
A fullscreen website screenshot of a SaaS landing page for a project
management tool. Dark charcoal background with electric teal (#14B8A6)
accent on CTAs and interactive elements. Bold geometric sans-serif
headlines with generous letter-spacing, light gray body text. Sticky
navigation bar at top with logo and menu items, oversized hero section
with floating UI card mockup, three-column feature grid with subtle
glassmorphism cards, customer logo bar, testimonial section with avatar
and quote, pricing comparison table, and a full-width footer with
newsletter signup. In the style of Linear.app with generous whitespace
and precise grid alignment. NO browser chrome, NO device frame, content
fills entire image edge to edge.
```

### E-Commerce Homepage

**Example (Editorial):**
```
A fullscreen website screenshot of a luxury skincare brand homepage.
Warm cream background with matte gold (#C5A572) accents. Elegant serif
headlines with dramatic size contrast -- 96px hero text, 14px navigation
labels. Full-bleed hero image of product in use, asymmetric grid of
product cards below with hover-state shadows, editorial content block
with large typography pull-quote, ingredient story section with side-by-side
imagery, and a minimal footer. Inspired by Aesop.com with restrained
luxury and generous negative space. NO browser chrome, content fills
entire image edge to edge.
```

### Dashboard

**Example (Data-Dense):**
```
A fullscreen website screenshot of an analytics dashboard application.
Deep navy (#0F172A) sidebar navigation with teal (#0EA5E9) active state,
white content area with card-based layout. Compact sans-serif typography
with clear hierarchy -- bold metric numbers, subtle labels. Top bar with
search and user avatar, left sidebar with icon navigation, main area
showing KPI cards with sparkline charts, a large area chart, data table
with alternating row colors, and activity feed. Dense, information-rich,
functional. In the style of a Vercel or Datadog dashboard. NO browser
chrome, content fills entire image edge to edge.
```

### SaaS / Tech Marketing Hero Images

> These templates produce marketing hero images and component visuals
> for use ON websites -- not full-page screenshots. The framing rule
> does not apply to these.

**Pattern:** `[UI mockup or abstract visual] + "on [dark/light] background" + [specific colors with hex] + [typography description] + "clean, premium SaaS aesthetic" + [glassmorphism/gradient/glow effects]`

**Example (Dashboard Hero):**
```
A floating glassmorphism UI card on a deep charcoal background showing a
content analytics dashboard with a rising line graph in teal (#14B8A6),
bar charts in coral (#F97316), and a circular progress indicator at 94%.
Subtle grid lines, frosted glass effect with 20% opacity, teal glow
bleeding from the card edges. Clean premium SaaS aesthetic, no text
smaller than headline size.
```

**Example (Feature Highlight):**
```
An isometric 3D illustration of interconnected data nodes on a dark navy
background. Each node is a glowing teal sphere connected by thin luminous
lines, forming a constellation pattern. One central node pulses brighter
with radiating rings. Modern tech illustration style with subtle depth
of field, volumetric lighting from below.
```

**Example (Comparison/Before-After):**
```
Split-screen image: left side shows a cluttered, dim workspace with
scattered papers, red error indicators, and a frustrated expression
conveyed through a cracked coffee mug and tangled cables. Right side
shows a clean, organized dashboard interface glowing in teal and white
on a dark background, with smooth flowing lines and checkmarks. A sharp
vertical dividing line separates chaos from clarity.
```
