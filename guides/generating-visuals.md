# Generating Visuals with AI

Every infographic in this toolkit was generated using AI image generation with a consistent visual style called **Style B Enhanced**. Here's how to create your own.

---

## The Visual Style: Style B Enhanced

The style creates **isometric 3D glass morphism infographics** — frosted glass cards floating on a white background with soft gradients and clean typography. It looks premium, professional, and stands out from typical flat graphics.

**Key characteristics:**
- Isometric 3D perspective
- Frosted glass / glass morphism cards
- Soft gradients and subtle shadows
- Brand color palette (blue, purple, gold, red)
- Pure white background
- 4:3 landscape format

---

## Method: Google Gemini (Free)

### Setup

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with a Google account
3. You get free API access (generous limits for personal use)
4. Get your API key from the API keys section

### The Prompt Template

Copy this template and customize the `[TOPIC]` and `[DETAILS]` sections:

```
Create an ISOMETRIC 3D glass morphism infographic about [TOPIC].

Use frosted glass cards with soft gradients floating on layers.

Include these elements:
[DETAILS - list the specific content, stats, flow, or framework to visualize]

Style requirements:
- ISOMETRIC 3D perspective with depth
- Frosted glass / glass morphism cards
- Soft gradients, subtle drop shadows
- Color palette: blue #4A7BF7, purple #7C5CFC, gold #D4A843, red #E63946
- PURE WHITE background (#FFFFFF)
- Clean sans-serif typography
- 4:3 landscape format
- Professional, premium feel
- NO text smaller than 14pt
- Visual hierarchy with size and color contrast
```

### Example Prompts

**For a Value Equation visual:**
```
Create an ISOMETRIC 3D glass morphism infographic showing "The Value Equation."

Use frosted glass cards with soft gradients floating on layers.

Include these elements:
- Large formula at center: VALUE = (Dream Outcome x Likelihood) / (Time Delay x Effort)
- 4 floating cards around it, each showing one lever:
  1. Dream Outcome (arrow UP, blue card)
  2. Perceived Likelihood (arrow UP, purple card)
  3. Time Delay (arrow DOWN, gold card)
  4. Effort & Sacrifice (arrow DOWN, red card)
- Small icons on each card representing the concept

Style requirements:
- ISOMETRIC 3D perspective with depth
- Frosted glass / glass morphism cards
- Soft gradients, subtle drop shadows
- Color palette: blue #4A7BF7, purple #7C5CFC, gold #D4A843, red #E63946
- PURE WHITE background (#FFFFFF)
- Clean sans-serif typography
- 4:3 landscape format
```

**For a funnel diagram:**
```
Create an ISOMETRIC 3D glass morphism infographic showing a "Marketing Funnel."

Use frosted glass cards with soft gradients floating on layers.

Include these elements:
- 3-tier funnel flowing downward:
  1. TOFU (Top of Funnel) - wide, blue, "90% - Awareness"
  2. MOFU (Middle of Funnel) - medium, purple, "7% - Consideration"
  3. BOFU (Bottom of Funnel) - narrow, gold, "3% - Decision"
- Arrows flowing between tiers
- Content types listed beside each tier
- Conversion percentages

Style requirements:
- ISOMETRIC 3D perspective with depth
- Frosted glass / glass morphism cards
- Soft gradients, subtle drop shadows
- Color palette: blue #4A7BF7, purple #7C5CFC, gold #D4A843, red #E63946
- PURE WHITE background (#FFFFFF)
- Clean sans-serif typography
- 4:3 landscape format
```

### Using the API Directly

If you want to automate image generation, you can use the Gemini API:

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "YOUR PROMPT HERE"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageSizeOptions": {"aspectRatio": "LANDSCAPE_4_3"}
    }
  }'
```

The response includes the image as base64 data that you can save as a PNG.

---

## Tips for Consistent Results

1. **Always include the full style block** — Don't skip the color palette or format specifications
2. **Be specific about content** — List exactly what elements, labels, and data to include
3. **Use the same colors every time** — The palette (blue, purple, gold, red on white) creates visual consistency
4. **Specify "PURE WHITE background"** — Without this, AI models often add gradients or patterns
5. **Generate 2-3 variations** — Pick the best one. AI output varies run to run
6. **4:3 landscape format** — This works best for embedding in Excalidraw canvases side-by-side with text

---

## Saving Your Images

1. Save generated images as PNG files
2. Use a consistent naming convention: `01-topic-name.png`, `02-topic-name.png`
3. Store in a `frames/` folder alongside your canvas
4. Recommended resolution: at least 1024px wide

---

## Next Steps

- [Building Canvases](building-canvases.md) — Embed your generated images into Excalidraw canvases
- [Style B Prompts](../templates/style-b-prompts.md) — Ready-to-use prompt templates for common topics
