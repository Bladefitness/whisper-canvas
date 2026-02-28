# Building Canvases

How to combine AI-generated images and text into polished Excalidraw training canvases.

---

## Canvas Layout Pattern

Every canvas in this toolkit follows a consistent layout:

```
+--------------------------------------------------+
|              TITLE BAR (dark background)          |
|              Training Title + Subtitle            |
+--------------------------------------------------+

+--- Frame 1 ---+-------+    +--- Frame 2 ---+-------+
|               |       |    |               |       |
|    IMAGE      | TEXT   |    |    IMAGE      | TEXT   |
|   (620x465)   | BOX   |    |   (620x465)   | BOX   |
|               | (460w)|    |               | (460w)|
+---------------+-------+    +---------------+-------+

+--- Frame 3 ---+-------+    +--- Frame 4 ---+-------+
|               |       |    |               |       |
|    IMAGE      | TEXT   |    |    IMAGE      | TEXT   |
|               | BOX   |    |               | BOX   |
|               |       |    |               |       |
+---------------+-------+    +---------------+-------+
```

**Specs:**
- Canvas width: ~2400px
- 2 columns, each ~1150px wide with 50px gap
- Each frame: 1150px wide x 920px tall
- Image: 620x465px (left side)
- Text box: 460px wide (right side)
- Title bar: 2400x120px with dark background (#1e1e2e)

---

## Method 1: Manual (Drag and Drop)

### Step 1: Create the Title Bar

1. Draw a large rectangle at the top (2400x120px)
2. Set background color to `#1e1e2e` (dark)
3. Add text inside with white color (#ffffff), font size 32

### Step 2: Create Frame Borders

1. Draw a rectangle for each frame (1150x920px)
2. Set stroke color to `#4A7BF7` (blue), stroke width 3
3. Set background to `#f0f4ff` (light blue)
4. Position in a 2-column grid

### Step 3: Add Images

1. Drag your PNG image into the frame
2. Resize to approximately 620x465px
3. Position in the left side of the frame

### Step 4: Add Text Boxes

1. Press `T` to create a text element
2. Type your key takeaways (bullet points work well)
3. Set font size to 16px
4. Position to the right of the image

### Step 5: Add Frame Titles

1. Add a text element at the top of each frame
2. Font size 22px, color matching the frame border
3. All caps or title case

---

## Method 2: Automated (Python Script)

For faster results, use this Python script to generate complete canvases programmatically:

```python
import json, base64, os, random

def build_excalidraw(frames_dir, frames_data, title, subtitle, output_path):
    """
    Build an Excalidraw file with embedded images and text boxes.

    frames_data: list of tuples (filename, frame_title, description, is_clinical)
    is_clinical: True = dashed red border, False = solid blue border
    """
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

    # Title bar
    elements.append({
        "type": "rectangle", "id": next_id(),
        "x": 0, "y": 0, "width": 2400, "height": 120,
        "backgroundColor": "#1e1e2e", "strokeColor": "#1e1e2e",
        "roundness": {"type": 3}, **default_props()
    })
    elements.append({
        "type": "text", "id": next_id(),
        "x": 50, "y": 20, "width": 2300, "height": 40,
        "text": title, "fontSize": 32, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "top",
        "containerId": None, "originalText": title,
        "autoResize": True, "lineHeight": 1.25,
        "strokeColor": "#ffffff", **default_props()
    })
    elements.append({
        "type": "text", "id": next_id(),
        "x": 50, "y": 65, "width": 2300, "height": 30,
        "text": subtitle, "fontSize": 20, "fontFamily": 1,
        "textAlign": "center", "verticalAlign": "top",
        "containerId": None, "originalText": subtitle,
        "autoResize": True, "lineHeight": 1.25,
        "strokeColor": "#a0a0b0", **default_props()
    })

    # Layout settings
    col_width, start_y, row_height, padding = 1150, 160, 920, 50

    for i, (filename, frame_title, description, is_clinical) in enumerate(frames_data):
        col = i % 2
        row = i // 2
        x = col * (col_width + padding)
        y = start_y + row * (row_height + padding)

        # Frame styling
        border_color = "#E63946" if is_clinical else "#4A7BF7"
        bg_color = "#fff5f5" if is_clinical else "#f0f4ff"
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
        prefix = "🩺 " if is_clinical else ""
        elements.append({
            "type": "text", "id": next_id(),
            "x": x + 20, "y": y + 15, "width": col_width - 40, "height": 30,
            "text": f"{prefix}{frame_title}", "fontSize": 22, "fontFamily": 1,
            "textAlign": "left", "verticalAlign": "top",
            "containerId": None, "originalText": f"{prefix}{frame_title}",
            "autoResize": True, "lineHeight": 1.25,
            "strokeColor": border_color, **default_props()
        })

        # Embed image
        img_path = os.path.join(frames_dir, filename)
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

        # Text box
        elements.append({
            "type": "text", "id": next_id(),
            "x": x + 660, "y": y + 55, "width": 460, "height": 460,
            "text": description, "fontSize": 16, "fontFamily": 1,
            "textAlign": "left", "verticalAlign": "top",
            "containerId": None, "originalText": description,
            "autoResize": True, "lineHeight": 1.25,
            "strokeColor": "#333333", **default_props()
        })

    # Write file
    doc = {
        "type": "excalidraw", "version": 2, "source": "claude-code",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": files
    }
    with open(output_path, "w") as f:
        json.dump(doc, f)

    print(f"Created: {output_path} ({len(elements)} elements, {len(files)} images)")
```

### Usage

```python
build_excalidraw(
    frames_dir="frames",
    frames_data=[
        ("01-topic.png", "FRAME TITLE", "Key takeaway text...", False),
        ("02-topic.png", "ANOTHER FRAME", "More takeaways...", False),
        ("03-clinical.png", "CLINICAL SIDEBAR", "Medical analogy...", True),
    ],
    title="YOUR TRAINING TITLE",
    subtitle="Subtitle goes here",
    output_path="canvas.excalidraw"
)
```

---

## Clinical Sidebar Frames

Clinical sidebar frames use a different visual style to stand out:

| Property | Regular Frame | Clinical Frame |
|----------|--------------|----------------|
| Border color | `#4A7BF7` (blue) | `#E63946` (red) |
| Background | `#f0f4ff` (light blue) | `#fff5f5` (light red) |
| Border style | Solid | Dashed |
| Title prefix | None | 🩺 |

Set `is_clinical=True` in the frames data to use this style automatically.

---

## Next Steps

- [Customizing for Your Clinic](customizing-for-your-clinic.md) — Adapt the content for your practice
- [Templates](../templates/) — Start from pre-built canvas and prompt templates
