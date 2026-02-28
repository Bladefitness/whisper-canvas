# Training: How to Use WhisperCanvas

## From Idea to Research-Backed Visual Presentation — A Step-by-Step Guide

**Duration:** ~10 minutes
**Canvas:** `canvas.excalidraw`

---

## What Is WhisperCanvas?

WhisperCanvas is a tool you install in **Cursor, VS Code, or Claude Code**. You talk to it naturally — "Help me create a training on [topic]" — and it handles the research, outline, AI visuals, and canvas assembly for you.

**The pipeline:**
1. **Whisper** — Describe your topic in plain language
2. **Research** — AI finds real citations and structures the content
3. **Visualize** — AI generates 3D infographics (optional, requires Gemini API key)
4. **Canvas** — Auto-assembles everything into an Excalidraw presentation
5. **Share** — Export to PDF, HTML, or PNG — works on any device

**Two output modes:**
- **Canvas Only** — Pure Excalidraw diagrams. No API key. No cost. Instant.
- **Canvas + AI Visuals** — Full presentations with AI-generated 3D infographics. Requires a free Gemini API key.

---

## Step 1: Install from GitHub

Three steps. Two minutes.

### 1. Clone the repo
```bash
git clone https://github.com/Bladefitness/whisper-canvas.git
cd whisper-canvas
```

### 2. Open in your editor
- **Cursor:** `cursor .`
- **VS Code:** `code .`
- **Claude Code:** Just `cd` into the folder and start talking

### 3. Install the Excalidraw extension
Search for `pomdtr.excalidraw-editor` in the extensions panel and install it. This lets you view and edit `.excalidraw` files directly in your editor.

That's it. The `CLAUDE.md` file in the project root teaches the AI assistant how WhisperCanvas works. It knows the prompts, the styles, the layout patterns, and the build scripts. You just talk to it.

---

## Step 2: Set Up Your Gemini API Key (Optional)

**Skip this step if you only want Canvas Only mode.**

This is only needed if you want AI-generated images in your presentations.

### Get your free API key
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with any Google account
3. Navigate to the API keys section
4. Click "Create API Key" — it's free

### Add it to the project
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```

That's it. The free tier is generous — enough for dozens of presentations without paying anything.

### Example `.env` file
```
# WhisperCanvas Configuration
# Get your free key at: https://aistudio.google.com

GEMINI_API_KEY=AIzaSyC_your_actual_key_goes_here
```

> **Note:** The `.env` file is in `.gitignore` — your key will never be accidentally committed to GitHub.

---

## Step 3: Describe Your Topic

This is where the magic happens. Just talk naturally:

> "Help me come up with an outline for a training on why knee pain often starts at the hip. Base it on actual research."

### What happens next

1. **Research** — The AI searches for relevant studies, frameworks, and clinical evidence
2. **Structure** — It organizes the content into 5-7 sections, each with a clear visual concept
3. **Quality control** — The outline includes real citations, not generic AI summaries
4. **Review** — You see the outline and give feedback

### The feedback loop

You can steer the outline before anything gets generated:
- "Add more detail on ankle stiffness"
- "Include an assessment section with specific tests"
- "Make the clinical sidebar about X analogy"
- "Remove section 4, it's not relevant"

Once you approve the outline, you choose your output mode:
- **Canvas Only** → generates Excalidraw diagrams immediately
- **Canvas + AI Visuals** → generates images with Gemini, then assembles the canvas

---

## Option A: Canvas Only

**No API key needed. Instant output.**

This mode creates pure Excalidraw diagrams — flowcharts, frameworks, mind maps, process flows. No AI-generated images, no API calls, no cost.

### What you get
- Clean vector diagrams with connected shapes and arrows
- Color-coded sections with labels
- Fully editable in the Excalidraw editor
- Export to PNG or SVG

### Best for
- Quick concept diagrams
- Process flows and frameworks
- Architecture and system design
- Internal documentation
- When you need speed over visual polish

### How to use it
Just say: "Create an Excalidraw diagram showing [concept]"

The AI generates a `.excalidraw` file that opens directly in your editor. You can edit every element — move shapes, change colors, add text, adjust arrows.

---

## Option B: Canvas + AI Visuals

**Requires Gemini API key. Full presentation output.**

This is the premium mode. Each section of your outline gets a custom AI-generated 3D infographic, assembled into a polished Excalidraw canvas with text summaries.

### What you get
- AI-generated images for each section (3D, professional quality)
- Text summaries beside each image
- Title bar + 2-column layout
- Research citations embedded in the content
- Export to PDF for instant sharing

### Three visual styles

| Style | Look | Best For |
|-------|------|----------|
| **Glass Morphism** | Frosted glass, white background, isometric 3D | Clean, premium, professional |
| **Dark Holographic** | Neon glow, dark background, sci-fi | Bold, futuristic, attention-grabbing |
| **Medical Atlas** | Warm tones, Netter-style illustration | Clinical authority, medical education |

### How to use it
Say: "Generate the full presentation with AI visuals in the Glass Morphism style"

The AI will:
1. Generate an image for each section using your Gemini API key
2. Assemble all images + text into an Excalidraw canvas
3. Give you a `.excalidraw` file you can view, edit, and export

---

## Step 4: Export & Share

Your presentation is done. Now get it out into the world.

### PDF (Most Universal)
Best for sending to phones, email, or any messaging app. Everyone can open a PDF.

**How:** Open the HTML export in Chrome → Print → Save as PDF

### HTML (Self-Contained)
A single file that opens in any browser. All images embedded inside — no internet needed.

**How:** Use the export script to generate a self-contained HTML file.

### PNG (Social Media)
Individual frames extracted as images. Perfect for Instagram carousels, TikTok, LinkedIn posts, or Twitter/X threads.

**How:** Open the `.excalidraw` file → select a frame → Export as PNG.

### Excalidraw (Editable Source)
Share the raw `.excalidraw` file with collaborators. They can open it in their editor and modify anything.

---

## Why Visual Content Wins

> 🩺 **Clinical Sidebar**

### The Science

**Dual Coding Theory** (Paivio, 1971): When you combine words and visuals, you activate two separate memory systems in the brain simultaneously. Retention more than doubles compared to text alone.

### The Numbers

| Format | Retention After 3 Days | Social Media Impact |
|--------|----------------------|-------------------|
| Text only | 10% | Baseline |
| Visual + Text | 65% | 94% more views |

### The Competitive Edge

Most people in your space are posting walls of text — blog posts, long captions, bullet-point lists. When you post a polished, research-backed visual training, you immediately stand out as the expert.

Every presentation you create compounds:
- Your content library grows
- Your credibility builds
- Your audience sees you as the authority

> "Your competitors post text walls. You post research-backed visual trainings. That's the difference."

---

## Quick Reference

| What You Want | What to Say |
|---------------|-------------|
| Research outline | "Help me outline a training on [topic] with research" |
| Canvas only diagram | "Create an Excalidraw diagram showing [concept]" |
| Full AI visual presentation | "Generate the full presentation with AI visuals" |
| Specific style | "Use the Dark Holographic style" |
| Export to PDF | "Export this as a PDF" |
| Modify outline | "Add a section on [X]" or "Remove section [Y]" |

---

*WhisperCanvas by Dr. Emeka Ajufo — CC BY-NC-SA 4.0*
*github.com/Bladefitness/whisper-canvas*
