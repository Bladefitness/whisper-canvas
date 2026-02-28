# Excalidraw 101

A quick guide to working with Excalidraw — the hand-drawn style diagramming tool used throughout this toolkit.

---

## What Is Excalidraw?

Excalidraw is a free, open-source virtual whiteboard. It creates diagrams with a hand-drawn, sketchy aesthetic that looks natural and approachable. It's used by companies like Meta, Google, and thousands of developers for everything from architecture diagrams to mind maps.

**Key features:**
- Hand-drawn visual style (looks great in presentations)
- Infinite canvas — zoom and pan anywhere
- Real-time collaboration
- Export to PNG, SVG, or PDF
- Works in the browser or as an editor extension

---

## The Basics

### Adding Shapes

Use the toolbar at the top or keyboard shortcuts:

| Tool | Shortcut | Description |
|------|----------|-------------|
| Rectangle | `R` | Boxes, cards, containers |
| Ellipse | `O` | Circles, ovals |
| Diamond | `D` | Decision points |
| Arrow | `A` | Connecting lines with arrows |
| Line | `L` | Connecting lines without arrows |
| Text | `T` | Type text anywhere |
| Selection | `V` or `1` | Select and move elements |
| Hand | `H` | Pan the canvas |

### Editing Elements

- **Move:** Click and drag
- **Resize:** Drag corner handles
- **Rotate:** Grab the rotation handle above the element
- **Delete:** Select and press `Delete` or `Backspace`
- **Duplicate:** Select and press `Cmd+D` / `Ctrl+D`
- **Copy style:** Select source, `Cmd+Shift+C`, select target, `Cmd+Shift+V`

### Styling

With an element selected, use the left panel to change:

- **Stroke color** — the outline color
- **Background color** — the fill color
- **Fill style** — solid, hachure (lines), cross-hatch, dots
- **Stroke width** — thin, bold, extra bold
- **Stroke style** — solid, dashed, dotted
- **Roughness** — architect (clean), artist (sketchy), cartoonist (very sketchy)
- **Opacity** — 0% (invisible) to 100% (solid)

### Adding Images

1. Drag and drop an image file onto the canvas
2. Or use the menu: `Insert > Image`
3. Images are embedded in the `.excalidraw` file (no external links to break)

### Adding Text

1. Press `T` or double-click anywhere on the canvas
2. Type your text
3. Use the left panel to change font size, alignment, and font family

---

## Working with Groups

Group elements to move them together:

1. Select multiple elements (click + drag a selection box, or Shift+click each one)
2. Press `Cmd+G` / `Ctrl+G` to group
3. Press `Cmd+Shift+G` / `Ctrl+Shift+G` to ungroup

---

## Layers (Z-Order)

Elements stack on top of each other. To reorder:

- **Bring to front:** `Cmd+Shift+]` / `Ctrl+Shift+]`
- **Send to back:** `Cmd+Shift+[` / `Ctrl+Shift+[`
- **Bring forward one:** `Cmd+]` / `Ctrl+]`
- **Send backward one:** `Cmd+[` / `Ctrl+[`

---

## Exporting

### As Image (PNG)

1. Select the elements you want to export (or select none for everything)
2. `File > Export Image` or `Cmd+Shift+E`
3. Options:
   - **Background:** Include or exclude the canvas background
   - **Dark mode:** Export with dark background
   - **Scale:** 1x, 2x, 3x (use 2x for presentations)
   - **Padding:** Add extra space around edges

### As SVG

Same process as PNG, but choose SVG format. SVGs are:
- Infinitely scalable (no pixelation)
- Editable in design tools (Figma, Illustrator)
- Perfect for websites and print

### As File

The `.excalidraw` file itself IS the portable format:
- Share it with anyone
- They can open it at [excalidraw.com](https://excalidraw.com)
- Or in their own VS Code/Cursor with the extension

---

## Tips for Great-Looking Diagrams

1. **Use consistent colors** — Pick 3-4 colors and stick with them
2. **Leave space** — Don't cram elements together. White space makes things readable
3. **Align elements** — Use the alignment tools (select multiple → right-click → Align)
4. **Use font size hierarchy** — Titles: 28-32px, labels: 18-22px, notes: 14-16px
5. **Keep text short** — Bullet points > paragraphs on a canvas

---

## Color Palette Used in This Toolkit

| Color | Hex | Used For |
|-------|-----|----------|
| Light Blue | `#a5d8ff` | Primary sections, inputs |
| Light Green | `#b2f2bb` | Success, output, tips |
| Light Orange | `#ffd8a8` | Warnings, pending items |
| Light Purple | `#d0bfff` | Processing, special sections |
| Light Red | `#ffc9c9` | Critical items, errors |
| Light Yellow | `#fff3bf` | Notes, decisions |
| Light Teal | `#c3fae8` | Data, metrics |

---

## Next Steps

- [Generating Visuals](generating-visuals.md) — Create AI-generated infographics
- [Building Canvases](building-canvases.md) — Combine images + text into training canvases
