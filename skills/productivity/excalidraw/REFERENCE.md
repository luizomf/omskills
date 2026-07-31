# Excalidraw scene reference

Use this reference when creating new elements. When editing, preserve valid fields already present in the target rather than normalizing unrelated elements.

## Scene

A standard scene contains `type: "excalidraw"`, `version: 2`, `elements`, `appState`, and `files`. Keep the scene JSON as the editable source of truth.

## Common element fields

Every new element needs:

```json
{"id":"unique-id","type":"rectangle","x":100,"y":100,"width":200,"height":80,"angle":0,"strokeColor":"#ffffff","backgroundColor":"#151b6f","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","roughness":1,"opacity":100,"groupIds":[],"frameId":null,"roundness":{"type":3},"seed":123456,"version":1,"versionNonce":654321,"isDeleted":false,"boundElements":[],"updated":1700000000000,"link":null,"locked":false}
```

Generate distinct nonzero `seed` and `versionNonce` integers. Keep `version` at `1` for new elements and use a current millisecond timestamp for `updated`. Preserve fractional coordinates only when they improve alignment.

## Text

A shape label is a separate text element. Start from the common fields, set `type: "text"`, `backgroundColor: "transparent"`, `roundness: null`, and add:

```json
{"text":"Step A","rawText":"Step A","fontSize":20,"fontFamily":5,"textAlign":"center","verticalAlign":"middle","containerId":"shape-a","originalText":"Step A","autoResize":true,"lineHeight":1.25}
```

The container must include `{"id":"text-a","type":"text"}` in `boundElements`. Keep `text`, `rawText`, and `originalText` equal. Estimate text bounds generously; the editor may recalculate them.

## Arrows

Start from the common fields, set `type: "arrow"`, `roundness: {"type":2}`, and add:

```json
{"points":[[0,0],[200,0]],"startBinding":{"elementId":"shape-a","mode":"orbit","fixedPoint":[1,0.5]},"endBinding":{"elementId":"shape-b","mode":"orbit","fixedPoint":[0,0.5]},"startArrowhead":null,"endArrowhead":"arrow","elbowed":false,"moveMidPointsWithElement":false}
```

Set arrow `width` and `height` to the bounding size of `points`. Add `{"id":"arrow-a-b","type":"arrow"}` to both endpoint shapes. An arrow label uses the text rules with the arrow ID as `containerId`, and the arrow reciprocally lists that text ID.

## Visual profile

The bundled base uses a near-black canvas (`#0f0f14`), white strokes and text, solid rounded shapes, 20px font family `5`, and round arrows. Reuse these observed fill colors by role without assigning a universal meaning: `#9c36b5`, `#1971c2`, `#167461`, `#3d138b`, `#aa6f1d`, and `#151b6f`. Maintain strong contrast and use one color consistently for the same concept within a diagram.

## Exhaustive check

For every output element, verify the common fields, type-specific fields, unique ID, non-deleted state, and valid bounds. For every binding, verify both participants reference each other and exist in the output scene.
