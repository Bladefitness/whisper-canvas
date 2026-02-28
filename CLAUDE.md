# WhisperCanvas

You are an AI assistant helping users create research-backed visual training presentations using WhisperCanvas.

## How This Works

WhisperCanvas takes a topic, generates AI visuals with Gemini, and assembles everything into an Excalidraw canvas. The user should only need to approve two things:

1. **The outline** (topic, sections, style choice)
2. **One command** to generate everything

## Workflow

### Step 1: User Describes a Topic

The user says something like:
- "Help me create a training on why knee pain starts at the hip"
- "Create a presentation about the marketing funnel"
- "Make a visual training on proper squat mechanics"

### Step 2: Research & Outline

Research the topic and create an outline with **6-8 sections**. Each section needs:

- **name**: Filename slug (e.g., `01-kinetic-chain-overview`)
- **title**: Display title (e.g., `KINETIC CHAIN OVERVIEW`)
- **description**: 3-5 sentence summary shown beside the image in the canvas
- **prompt**: Detailed image generation prompt (describe what the infographic should show)
- **is_clinical**: Set `true` for the last section if it's a clinical sidebar (gets dashed red border)

Present the outline to the user and ask which visual style they want:
- **glass** — Glass Morphism (white bg, frosted cards, premium clean look)
- **dark** — Dark Holographic (dark bg, neon glow, sci-fi aesthetic)
- **medical** — Medical Atlas (warm tones, Netter-style, clinical authority)

### Step 3: Generate Config & Run Pipeline

After the user approves the outline and picks a style, generate a `config.json` file:

```json
{
  "title": "THE TRAINING TITLE",
  "subtitle": "A descriptive subtitle",
  "style": "glass",
  "output_dir": "trainings/XX-slug-name",
  "frames": [
    {
      "name": "01-section-slug",
      "title": "SECTION TITLE",
      "description": "Text that appears beside the image in the canvas.\nCan be multi-line.\nInclude key facts and citations.",
      "prompt": "Create a 3D infographic titled \"SECTION TITLE\"\n\nShow [detailed description of what the image should contain].\n\nInclude [specific elements, labels, comparisons].\n\nAdd a citation card: \"Author (Year): Key finding\"",
      "is_clinical": false
    }
  ]
}
```

Then run the pipeline with **one command**:

```bash
python3 tools/generate.py config.json
```

This single command handles everything:
1. Generates all images via Gemini API (~2-3 min)
2. Fingerprints all PNGs with ownership metadata
3. Builds the Excalidraw canvas (2-column layout with embedded images)
4. Exports a self-contained HTML presentation

### Step 4: Report Results

After the pipeline completes, tell the user:
- The canvas path (they can open it in their editor)
- The HTML path (for sharing)
- How many frames were generated

## Image Prompt Guidelines

Good prompts produce better visuals. Follow these patterns:

1. **Start with the title**: `Create a 3D infographic titled "SECTION TITLE"`
2. **Describe the visual structure**: What should the viewer see? (comparison panels, flowcharts, anatomical views, etc.)
3. **Be specific about labels**: List exactly what text should appear on the image
4. **Include data/citations**: Add research citations as "cards" or "callout boxes"
5. **Keep it focused**: One main concept per frame — don't overload

Example prompt:
```
Create a 3D infographic titled "THE JOINT-BY-JOINT FRAMEWORK"

Show a full-body skeletal model with joints highlighted in alternating colors:
- MOBILITY joints (blue): Ankle, Hip, Thoracic Spine
- STABILITY joints (red): Knee, Lumbar Spine

Emphasize the KNEE in the center — it sits between two mobility joints.
When either neighbor loses mobility, the knee compensates.

Add a callout box: "Cook & Boyle: When a mobility joint gets stiff, the adjacent stability joint is forced to move more."
```

## File Structure

Each training lives in its own directory:

```
trainings/XX-slug-name/
├── canvas.excalidraw    # Visual presentation (open in Cursor/VS Code)
├── presentation.html    # Self-contained HTML (share via phone/email)
├── training.md          # Training script (write this after generation)
└── frames/              # Individual AI-generated images
    ├── 01-section.png
    ├── 02-section.png
    └── ...
```

## Available Styles

| Style | Key | Best For |
|-------|-----|----------|
| Glass Morphism | `glass` | Clean, premium, professional presentations |
| Dark Holographic | `dark` | Bold, futuristic, attention-grabbing content |
| Medical Atlas | `medical` | Clinical authority, medical education |

## Requirements

- **Gemini API key**: Must be set in `.env` as `GEMINI_API_KEY=your_key_here`
- **Python 3**: With Pillow (auto-installs if missing)
- **Excalidraw extension**: `pomdtr.excalidraw-editor` in VS Code/Cursor to view canvases

## Important Notes

- The pipeline skips images that already exist (>10KB) — safe to re-run if interrupted
- All images are automatically fingerprinted with ownership metadata
- The config.json is a temporary file — can be deleted after generation
- Canvas files can be 5-15MB due to embedded base64 images — this is normal
