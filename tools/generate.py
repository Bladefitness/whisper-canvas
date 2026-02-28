#!/usr/bin/env python3
"""WhisperCanvas — Unified training generation pipeline.

Takes a JSON config and runs the full pipeline:
  1. Generate images via Gemini API
  2. Fingerprint all PNGs (LSB steganography)
  3. Build Excalidraw canvas (2-column layout, embedded images)
  4. Export to self-contained HTML

Usage:
  python3 tools/generate.py config.json

Config format:
  {
    "title": "MY TRAINING TITLE",
    "subtitle": "A subtitle for the presentation",
    "style": "glass",           # glass | dark | medical
    "output_dir": "trainings/03-my-training",
    "frames": [
      {
        "name": "01-intro",
        "title": "INTRODUCTION",
        "description": "Text shown beside the image in the canvas...",
        "prompt": "Create a 3D infographic showing...",
        "is_clinical": false
      }
    ]
  }
"""

import json, base64, os, sys, struct, time, random, urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image


# ── Configuration ──────────────────────────────────────────────────

GEMINI_MODEL = "gemini-3.1-flash-image-preview"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
FINGERPRINT = "WhisperCanvas by Dr. Emeka Ajufo | github.com/Bladefitness/whisper-canvas"

STYLES = {
    "glass": {
        "name": "Glass Morphism",
        "image_prompt": """Style requirements:
- ISOMETRIC 3D perspective with depth and layering
- Frosted glass / glass morphism cards with soft blur edges
- Soft gradients, subtle drop shadows, floating card layers
- Color palette: blue #4A7BF7, purple #7C5CFC, gold #D4A843, red #E63946
- PURE WHITE background (#FFFFFF)
- Clean sans-serif typography, minimum 16pt font
- 4:3 landscape format
- Professional, premium feel""",
        "canvas": {
            "title_bg": "#1e1e2e", "title_color": "#ffffff",
            "subtitle_color": "#a0a0b0", "bg_color": "#ffffff",
            "frame_border": "#4A7BF7", "frame_bg": "#f0f4ff",
            "clinical_border": "#E63946", "clinical_bg": "#fff5f5",
            "text_color": "#333333",
        },
        "html": {
            "bg": "#ffffff", "title_bg": "#1e1e2e",
            "title_color": "#ffffff", "text_color": "#333333",
            "border_color": "#4A7BF7", "clinical_border": "#E63946",
        },
    },
    "dark": {
        "name": "Dark Holographic",
        "image_prompt": """Style requirements:
- Dark mode with deep navy/black background (#0a0e1a to #1a1e3a gradient)
- NEON GLOW bioluminescent effect on all elements
- Holographic scan aesthetic — glowing wireframes, luminous highlights
- Cyan #00f0ff, magenta #ff00ff, electric blue #4a9eff, neon green #00ff88
- Floating data panels with thin glowing borders
- Sci-fi HUD aesthetic
- Clean sans-serif typography in white/cyan, minimum 16pt
- 4:3 landscape format
- Futuristic, high-tech feel""",
        "canvas": {
            "title_bg": "#0a0e1a", "title_color": "#00f0ff",
            "subtitle_color": "#4a9eff", "bg_color": "#0d1117",
            "frame_border": "#00f0ff", "frame_bg": "#111827",
            "clinical_border": "#ff00ff", "clinical_bg": "#1a0a1a",
            "text_color": "#e0e0e0",
        },
        "html": {
            "bg": "#0d1117", "title_bg": "#0a0e1a",
            "title_color": "#00f0ff", "text_color": "#e0e0e0",
            "border_color": "#00f0ff", "clinical_border": "#ff00ff",
        },
    },
    "medical": {
        "name": "Medical Atlas",
        "image_prompt": """Style requirements:
- Premium medical atlas illustration style (inspired by Netter's anatomy)
- Rich warm color palette: deep reds, ivory, warm amber highlights
- Subtle cream/warm white background with slight parchment texture
- Professional medical illustration labels with clean leader lines
- Color accents: red #C41E3A, blue #1B4F72, ivory #F5E6CC, brown #8B2500
- Classical medical typography (serif for titles, sans for labels), minimum 16pt
- 4:3 landscape format
- Authoritative, textbook-quality feel""",
        "canvas": {
            "title_bg": "#2C1810", "title_color": "#F5E6CC",
            "subtitle_color": "#C4A882", "bg_color": "#FFF8F0",
            "frame_border": "#1B4F72", "frame_bg": "#FFF5EB",
            "clinical_border": "#C41E3A", "clinical_bg": "#FFF0F0",
            "text_color": "#2C1810",
        },
        "html": {
            "bg": "#FFF8F0", "title_bg": "#2C1810",
            "title_color": "#F5E6CC", "text_color": "#2C1810",
            "border_color": "#1B4F72", "clinical_border": "#C41E3A",
        },
    },
}


# ── Stage 1: Image Generation ─────────────────────────────────────

def load_api_key():
    """Load Gemini API key from env var or .env file."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERROR: No GEMINI_API_KEY found. Set it in .env or as an environment variable.")
    sys.exit(1)


def generate_image(prompt, output_path, api_key, retries=2):
    """Generate one image via Gemini API."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                GEMINI_URL,
                data=json.dumps(payload).encode(),
                headers={"x-goog-api-key": api_key, "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode())

            parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    img_bytes = base64.b64decode(part["inlineData"]["data"])
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    return True

            finish = data.get("candidates", [{}])[0].get("finishReason", "UNKNOWN")
            print(f"    No image returned (finish: {finish}), attempt {attempt+1}/{retries+1}")
            if attempt < retries:
                time.sleep(3)
        except Exception as e:
            print(f"    Error: {e}, attempt {attempt+1}/{retries+1}")
            if attempt < retries:
                time.sleep(5)
    return False


def stage_generate(config, style, api_key):
    """Generate all frame images."""
    frames_dir = os.path.join(config["output_dir"], "frames")
    os.makedirs(frames_dir, exist_ok=True)

    total = len(config["frames"])
    success = 0

    for i, frame in enumerate(config["frames"]):
        output_path = os.path.join(frames_dir, f"{frame['name']}.png")

        if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            print(f"  [{i+1}/{total}] {frame['name']} — skipped (exists)")
            success += 1
            continue

        full_prompt = f"{frame['prompt']}\n\n{style['image_prompt']}"
        print(f"  [{i+1}/{total}] {frame['name']} — generating...")

        if generate_image(full_prompt, output_path, api_key):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"    done ({size_kb:.0f} KB)")
            success += 1
        else:
            print(f"    FAILED")

        if i < total - 1:
            time.sleep(2)

    return success, total


# ── Stage 2: Fingerprinting ───────────────────────────────────────

def _msg_to_bits(msg):
    enc = msg.encode("utf-8")
    data = struct.pack(">I", len(enc)) + enc
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def fingerprint_image(path, msg=FINGERPRINT):
    """Embed fingerprint into a PNG's red channel LSB."""
    bits = _msg_to_bits(msg)
    img = Image.open(path).convert("RGBA")
    pixels = list(img.getdata())
    if len(pixels) < len(bits):
        return False
    new_pixels = []
    for idx, px in enumerate(pixels):
        if idx < len(bits):
            r, g, b, a = px
            r = (r & 0xFE) | bits[idx]
            new_pixels.append((r, g, b, a))
        else:
            new_pixels.append(px)
    img.putdata(new_pixels)
    img.save(path, format="PNG")
    return True


def stage_fingerprint(config):
    """Fingerprint all generated PNGs."""
    frames_dir = os.path.join(config["output_dir"], "frames")
    pngs = sorted(Path(frames_dir).glob("*.png"))
    count = 0
    for png in pngs:
        if fingerprint_image(str(png)):
            count += 1
    return count


# ── Stage 3: Build Excalidraw Canvas ──────────────────────────────

def stage_build_canvas(config, style):
    """Build Excalidraw canvas with embedded images."""
    s = style["canvas"]
    elements = []
    files = {}
    eid = 0

    def next_id():
        nonlocal eid
        eid += 1
        return f"elem_{eid}"

    def default_props():
        return {
            "versionNonce": random.randint(1, 999999999),
            "isDeleted": False, "fillStyle": "solid",
            "strokeWidth": 2, "strokeStyle": "solid",
            "roughness": 0, "opacity": 100, "angle": 0,
            "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
            "seed": random.randint(1, 999999999),
            "groupIds": [], "frameId": None,
            "boundElements": None, "updated": 1,
            "link": None, "locked": False
        }

    title = config["title"]
    subtitle = config.get("subtitle", "")

    # Title bar
    elements.append({
        "type": "rectangle", "id": next_id(),
        "x": 0, "y": 0, "width": 2400, "height": 120,
        "backgroundColor": s["title_bg"], "strokeColor": s["title_bg"],
        "roundness": {"type": 3}, **default_props()
    })
    elements.append({
        "type": "text", "id": next_id(),
        "x": 50, "y": 20, "width": 2300, "height": 40,
        "text": title, "fontSize": 32, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "top",
        "containerId": None, "originalText": title,
        "autoResize": True, "lineHeight": 1.25,
        "strokeColor": s["title_color"], **default_props()
    })
    if subtitle:
        elements.append({
            "type": "text", "id": next_id(),
            "x": 50, "y": 65, "width": 2300, "height": 30,
            "text": subtitle, "fontSize": 18, "fontFamily": 1,
            "textAlign": "center", "verticalAlign": "top",
            "containerId": None, "originalText": subtitle,
            "autoResize": True, "lineHeight": 1.25,
            "strokeColor": s["subtitle_color"], **default_props()
        })

    col_width, start_y, row_height, padding = 1150, 160, 920, 50
    frames_dir = os.path.join(config["output_dir"], "frames")

    for i, frame in enumerate(config["frames"]):
        col = i % 2
        row = i // 2
        x = col * (col_width + padding)
        y = start_y + row * (row_height + padding)

        is_clinical = frame.get("is_clinical", False)
        border_color = s["clinical_border"] if is_clinical else s["frame_border"]
        bg_color = s["clinical_bg"] if is_clinical else s["frame_bg"]
        stroke_style = "dashed" if is_clinical else "solid"

        # Frame border
        elements.append({
            "type": "rectangle", "id": next_id(),
            "x": x, "y": y, "width": col_width, "height": row_height,
            "backgroundColor": bg_color, "strokeColor": border_color,
            "strokeWidth": 3, "roundness": {"type": 3},
            **{**default_props(), "strokeStyle": stroke_style}
        })

        # Frame title
        prefix = "\U0001fa7a " if is_clinical else ""
        frame_title = f"{prefix}{frame['title']}"
        elements.append({
            "type": "text", "id": next_id(),
            "x": x + 20, "y": y + 15, "width": col_width - 40, "height": 30,
            "text": frame_title, "fontSize": 22, "fontFamily": 1,
            "textAlign": "left", "verticalAlign": "top",
            "containerId": None, "originalText": frame_title,
            "autoResize": True, "lineHeight": 1.25,
            "strokeColor": border_color, **default_props()
        })

        # Embed image
        img_path = os.path.join(frames_dir, f"{frame['name']}.png")
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode()

            file_id = f"file_{i+1}"
            files[file_id] = {
                "mimeType": "image/png", "id": file_id,
                "dataURL": f"data:image/png;base64,{img_data}",
                "created": 1, "lastRetrieved": 1
            }
            elements.append({
                "type": "image", "id": next_id(),
                "x": x + 20, "y": y + 55, "width": 620, "height": 465,
                "fileId": file_id, "status": "saved", **default_props()
            })

        # Text description
        description = frame.get("description", "")
        if description:
            elements.append({
                "type": "text", "id": next_id(),
                "x": x + 660, "y": y + 55, "width": 460, "height": 460,
                "text": description, "fontSize": 16, "fontFamily": 1,
                "textAlign": "left", "verticalAlign": "top",
                "containerId": None, "originalText": description,
                "autoResize": True, "lineHeight": 1.25,
                "strokeColor": s["text_color"], **default_props()
            })

    doc = {
        "type": "excalidraw", "version": 2,
        "source": "WhisperCanvas by Dr. Emeka Ajufo",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": s["bg_color"]},
        "files": files,
        "metadata": {
            "creator": "Dr. Emeka Ajufo",
            "tool": "WhisperCanvas",
            "license": "CC BY-NC-SA 4.0",
            "repository": "github.com/Bladefitness/whisper-canvas"
        }
    }

    output_path = os.path.join(config["output_dir"], "canvas.excalidraw")
    with open(output_path, "w") as f:
        json.dump(doc, f)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    return output_path, len(elements), len(files), size_mb


# ── Stage 4: HTML Export ──────────────────────────────────────────

def stage_export_html(config, style):
    """Generate a self-contained HTML file with embedded images."""
    h = style["html"]
    frames_dir = os.path.join(config["output_dir"], "frames")

    frames_html = ""
    for i, frame in enumerate(config["frames"]):
        img_path = os.path.join(frames_dir, f"{frame['name']}.png")
        if not os.path.exists(img_path):
            continue

        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()

        is_clinical = frame.get("is_clinical", False)
        border = h["clinical_border"] if is_clinical else h["border_color"]
        border_style = "dashed" if is_clinical else "solid"
        prefix = "\U0001fa7a " if is_clinical else ""
        description = frame.get("description", "")

        frames_html += f"""
    <div class="frame" style="border: 3px {border_style} {border};">
      <h2 style="color: {border};">{prefix}{frame['title']}</h2>
      <div class="frame-content">
        <img src="data:image/png;base64,{img_b64}" alt="{frame['title']}">
        <p class="description">{description}</p>
      </div>
    </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{config['title']}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: {h['bg']};
    color: {h['text_color']};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    padding: 0;
  }}
  .title-bar {{
    background: {h['title_bg']};
    padding: 28px 20px;
    text-align: center;
  }}
  .title-bar h1 {{
    color: {h['title_color']};
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 1px;
  }}
  .title-bar p {{
    color: {h['title_color']}88;
    font-size: 15px;
    margin-top: 6px;
  }}
  .container {{
    max-width: 900px;
    margin: 0 auto;
    padding: 24px 16px;
  }}
  .frame {{
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
    background: {h['bg']};
  }}
  .frame h2 {{
    font-size: 18px;
    margin-bottom: 14px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}
  .frame-content {{
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .frame img {{
    width: 100%;
    border-radius: 8px;
  }}
  .description {{
    font-size: 15px;
    line-height: 1.6;
    opacity: 0.85;
    white-space: pre-line;
  }}
  .footer {{
    text-align: center;
    padding: 30px 16px;
    font-size: 13px;
    opacity: 0.5;
  }}
  @media (min-width: 768px) {{
    .frame-content {{
      flex-direction: row;
      align-items: flex-start;
    }}
    .frame img {{
      width: 60%;
      flex-shrink: 0;
    }}
    .description {{
      width: 40%;
    }}
  }}
</style>
</head>
<body>

<div class="title-bar">
  <h1>{config['title']}</h1>
  <p>{config.get('subtitle', '')}</p>
</div>

<div class="container">
{frames_html}
</div>

<div class="footer">
  WhisperCanvas by Dr. Emeka Ajufo — CC BY-NC-SA 4.0
</div>

</body>
</html>"""

    output_path = os.path.join(config["output_dir"], "presentation.html")
    with open(output_path, "w") as f:
        f.write(html)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    return output_path, size_mb


# ── Main Pipeline ─────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/generate.py config.json")
        print("\nConfig format: see tools/generate.py header or CLAUDE.md")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path) as f:
        config = json.load(f)

    style_key = config.get("style", "glass")
    if style_key not in STYLES:
        print(f"ERROR: Unknown style '{style_key}'. Choose: glass, dark, medical")
        sys.exit(1)

    style = STYLES[style_key]
    os.makedirs(config["output_dir"], exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  WhisperCanvas Pipeline")
    print(f"  Title: {config['title']}")
    print(f"  Style: {style['name']}")
    print(f"  Frames: {len(config['frames'])}")
    print(f"  Output: {config['output_dir']}")
    print(f"{'='*60}\n")

    # Stage 1: Generate images
    print("[1/4] Generating images via Gemini API...")
    api_key = load_api_key()
    generated, total = stage_generate(config, style, api_key)
    print(f"  Result: {generated}/{total} images generated\n")

    if generated == 0:
        print("ERROR: No images generated. Check your API key and network.")
        sys.exit(1)

    # Stage 2: Fingerprint
    print("[2/4] Fingerprinting images...")
    fingerprinted = stage_fingerprint(config)
    print(f"  Result: {fingerprinted} images fingerprinted\n")

    # Stage 3: Build canvas
    print("[3/4] Building Excalidraw canvas...")
    canvas_path, elem_count, file_count, canvas_mb = stage_build_canvas(config, style)
    print(f"  Result: {elem_count} elements, {file_count} images, {canvas_mb:.1f} MB")
    print(f"  Output: {canvas_path}\n")

    # Stage 4: Export HTML
    print("[4/4] Exporting HTML presentation...")
    html_path, html_mb = stage_export_html(config, style)
    print(f"  Result: {html_mb:.1f} MB")
    print(f"  Output: {html_path}\n")

    # Summary
    print(f"{'='*60}")
    print(f"  DONE!")
    print(f"  Canvas:  {canvas_path}")
    print(f"  HTML:    {html_path}")
    print(f"  Frames:  {config['output_dir']}/frames/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
