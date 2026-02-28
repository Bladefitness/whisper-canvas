# WhisperCanvas

**Whisper an idea. Get a research-backed visual presentation.**

WhisperCanvas is an open-source toolkit for creating professional training presentations with AI-generated visuals. Give it a topic, pick a style, and get a polished canvas with 3D infographics, structured content, and exportable formats — in minutes, not weeks.

---

## What's Inside

### Example Trainings

| # | Training | Topic | Frames |
|---|----------|-------|--------|
| 0 | [How to Use WhisperCanvas](trainings/00-how-to-use-whispercanvas/) | Getting started — from idea to presentation | 8 frames |
| 1 | [Plug Your Bottlenecks](trainings/01-plug-your-bottlenecks/) | Marketing funnel optimization | 9 frames (8 regular + 1 clinical sidebar) |
| 2 | [The Knee Is the Victim](trainings/02-knee-is-the-victim/) | Kinetic chain dysfunction & knee pain | 8 frames (7 regular + 1 clinical sidebar) |

Each training includes:
- **`canvas.excalidraw`** — Visual presentation with embedded AI-generated images
- **`training.md`** — Full script with research citations, patient analogies, and action items
- **`frames/`** — Individual AI-generated infographic images

### Guides

| Guide | What You'll Learn |
|-------|-------------------|
| [Getting Started](guides/getting-started.md) | Install the editor, open your first canvas |
| [Excalidraw 101](guides/excalidraw-101.md) | Editing basics, shortcuts, exporting |
| [Generating Visuals](guides/generating-visuals.md) | AI image generation with Gemini (free) |
| [Building Canvases](guides/building-canvases.md) | Layout patterns, embedding images, automation |
| [Customizing Content](guides/customizing-for-your-clinic.md) | Adapt for your niche, brand, and audience |

### Templates

| Template | Description |
|----------|-------------|
| [Blank Canvas](templates/blank-training-canvas.excalidraw) | Pre-built title bar + 6 empty frames |
| [Style Prompts](templates/style-b-prompts.md) | Copy-paste AI image generation prompts |
| [Script Template](templates/training-script-template.md) | Markdown template for training scripts |

### Tools

| Tool | Description |
|------|-------------|
| [Fingerprint](tools/fingerprint.py) | Steganographic image fingerprinting (embed/extract ownership proof) |

---

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Bladefitness/whisper-canvas.git
cd whisper-canvas
```

### 2. Open in VS Code or Cursor
Install the [Excalidraw extension](https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor), then open any `.excalidraw` file.

### 3. Explore the examples
Start with `trainings/00-how-to-use-whispercanvas/canvas.excalidraw` for the onboarding guide, then open `trainings/01-plug-your-bottlenecks/canvas.excalidraw` to see a full training with AI-generated 3D infographics.

### 4. Create your own
Follow the [Generating Visuals](guides/generating-visuals.md) guide to create images with your free Gemini API key, then use the [Building Canvases](guides/building-canvases.md) guide to assemble them.

---

## How It Works

```
Topic Idea → Research Outline → AI Image Generation → Canvas Assembly → Export & Share
                                    (Gemini API)         (Excalidraw)      (PDF/HTML)
```

1. **Pick a topic** — Start with a concept you want to teach
2. **Generate visuals** — Use the style prompts with Google Gemini (free tier) to create 3D infographics
3. **Build the canvas** — Assemble images + text into an Excalidraw presentation (manual or automated)
4. **Export & share** — PDF, HTML, PNG — works on any device, no apps needed

---

## Visual Styles

WhisperCanvas supports multiple visual styles for AI image generation:

| Style | Description |
|-------|-------------|
| **Glass Morphism** | Frosted glass cards, white background, isometric 3D — clean and premium |
| **Dark Holographic** | Neon glow, dark background, sci-fi HUD aesthetic — futuristic and bold |
| **Medical Atlas** | Netter-style illustration, warm tones — clinical authority |

See [Style Prompts](templates/style-b-prompts.md) for ready-to-use prompt templates.

---

## Who Is This For?

WhisperCanvas was originally built for clinic owners (chiropractors, PTs, med spas, wellness practices) but works for **anyone who wants to create research-backed visual training content**:

- **Educators** — Course material with professional visuals
- **Coaches & consultants** — Authority-building content
- **Content creators** — Eye-catching infographics for social media
- **Teams** — Internal training presentations

---

## License

[CC BY-NC-SA 4.0](LICENSE) — You can share and adapt this work with attribution. Non-commercial use only. See the full license for details.

**Attribution:** WhisperCanvas by Dr. Emeka Ajufo

**Fingerprinting:** All images contain invisible steganographic fingerprints for ownership verification.

---

## Credits

Built with [Excalidraw](https://excalidraw.com) and [Google Gemini](https://ai.google.dev).

Research sources cited in each training script. Key references include Powers (2010), Hewett (2005), Cook (2010), and Hormozi (2021).
