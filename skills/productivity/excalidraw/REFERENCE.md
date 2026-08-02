# Excalidraw scene reference

Use this reference when creating new elements. When editing, preserve valid fields already present in the target rather than normalizing unrelated elements.

## Scene

A standard scene contains `type: "excalidraw"`, `version: 2`, `elements`, `appState`, and `files`. Keep the scene JSON as the editable source of truth.

## Common element fields

Every new element needs:

```json
{"id":"unique-id","type":"rectangle","x":100,"y":100,"width":200,"height":80,"angle":0,"strokeColor":"#88aaf2","backgroundColor":"#495b81","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],"frameId":null,"roundness":{"type":3},"seed":123456,"version":1,"versionNonce":654321,"index":null,"isDeleted":false,"boundElements":[],"updated":1700000000000,"link":null,"locked":false}
```

Generate distinct nonzero `seed` and `versionNonce` integers. Keep `version` at `1` for new elements and use a current millisecond timestamp for `updated`. Preserve fractional coordinates only when they improve alignment.

## Text

A shape label is a separate text element. Start from the common fields, set `type: "text"`, `strokeColor: "#f0f0ff"`, `backgroundColor: "transparent"`, `roundness: null`, and add:

```json
{"text":"Step A","fontSize":20,"fontFamily":5,"textAlign":"center","verticalAlign":"middle","containerId":"shape-a","originalText":"Step A","autoResize":true,"lineHeight":1.25}
```

The container must include `{"id":"text-a","type":"text"}` in `boundElements`. Keep `text` and `originalText` equal. Estimate text bounds generously; the editor may recalculate them.

## Arrows

Start from the common fields, set `type: "arrow"`, `backgroundColor: "transparent"`, `roundness: {"type":2}`, and add:

```json
{"points":[[0,0],[200,0]],"startBinding":{"elementId":"shape-a","mode":"orbit","fixedPoint":[1,0.5]},"endBinding":{"elementId":"shape-b","mode":"orbit","fixedPoint":[0,0.5]},"startArrowhead":null,"endArrowhead":"arrow","elbowed":false}
```

Set arrow `width` and `height` to the bounding size of `points`. Add `{"id":"arrow-a-b","type":"arrow"}` to both endpoint shapes.

Bind every arrow label to its arrow instead of placing independent text nearby. Use the text rules with the arrow ID as `containerId`:

```json
{"id":"text-a-b","type":"text","text":"HTTP","originalText":"HTTP","containerId":"arrow-a-b","fontSize":20,"fontFamily":5,"textAlign":"center","verticalAlign":"middle","autoResize":true,"lineHeight":1.25}
```

The arrow must reciprocally include `{"id":"text-a-b","type":"text"}` in `boundElements`. This binding makes the label move and edit with the arrow.

## Visual profile

The bundled visual profile uses a near-black canvas (`#0f0f14`), light text (`#f0f0ff`), solid rounded shapes, 20px font family `5`, and round arrows. Prefer simple labeled rectangles and direct connectors.

Use the paired `omtheme` palette below. Apply the dark color as a shape's solid fill and its bright counterpart as the stroke, connector, or small accent. Keep text `#f0f0ff`; do not use the bright colors as fills behind light text.

| Role | Fill | Stroke or accent |
| --- | --- | --- |
| Red | `#8c4555` | `#ff7e9a` |
| Green | `#16684b` | `#37feb7` |
| Yellow | `#695a31` | `#ffda76` |
| Blue | `#495b81` | `#88aaf2` |
| Magenta | `#864763` | `#ff87bc` |
| Cyan | `#336078` | `#6bccff` |

Use one pair consistently for the same concept. Use `#3b4fa6` as a neutral or primary fill when no semantic color is needed.

## Exhaustive check

For every output element, verify the common fields, type-specific fields, unique ID, non-deleted state, and valid bounds. For every binding, verify both participants reference each other and exist in the output scene.
