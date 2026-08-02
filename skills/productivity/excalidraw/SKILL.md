---
name: excalidraw
description:
  Creates and edits clear, editable Excalidraw diagrams from text, a visual
  base, or an existing scene.
disable-model-invocation: true
---

# Excalidraw

Create or edit an Excalidraw scene while preserving editability and the
requested visual style.

## Input

Identify:

- the diagram content and destination path;
- an existing **target diagram**, when the request edits one;
- a **base scene** used only when creating a new diagram;
- any required layout, labels, colors, or output format.

When no target or base is supplied, use
[`assets/diagram-base.excalidraw`](assets/diagram-base.excalidraw). A supplied
target always wins over the base. Never merge the base into an existing target
or overwrite the bundled base. Input is complete when the scene source and
requested transformation are unambiguous.

## Workflow

1. **Read the scene.** Parse the full Excalidraw JSON. For wrapped formats,
   locate the scene without treating wrapper text as drawing content. Preserve
   unknown top-level data, `appState`, `files`, and elements outside the
   requested edit. The source is ready when all retained scene data is accounted
   for.

2. **Plan the diagram.** Convert the request into a small set of nodes,
   relationships, groups, and reading order. Reuse the target's spacing and
   element styles; otherwise derive new-element defaults from the base scene's
   `appState.currentItem*` values. Prefer fewer, larger elements and direct
   labels. The plan is ready when every requested concept and relationship has
   one visual representation.

3. **Build or edit elements.** Read [`REFERENCE.md`](REFERENCE.md) before
   creating elements. Use unique stable IDs and preserve existing IDs for
   elements that retain their identity. Keep labels as text elements, not custom
   `label` properties. Bind every shape label to its shape and every arrow label
   to its arrow: set the text's `containerId` and add the text ID to the
   container's `boundElements`. Do not place an arrow's label as independent
   text near the arrow. For connected arrows, set `startBinding` and
   `endBinding` and add the arrow ID to both endpoint shapes. Every new element
   must satisfy the reference schema, and every binding must be reciprocal and
   reference an existing, non-deleted element.

4. **Lay out the scene.** Prevent overlaps, leave clear gaps, keep labels inside
   their containers, and route arrows so direction is obvious. Order elements
   back-to-front: regions, shapes, bound text, connectors, connector labels,
   then annotations. The layout is complete when every element is legible and
   every relationship can be followed without ambiguity.

5. **Write the requested destination.** Preserve the target format when editing;
   for a new scene, use the requested Excalidraw-compatible format. Keep the
   result editable rather than rasterizing it. Writing is complete when the
   destination contains the transformed scene and the bundled base is unchanged.

6. **Verify.** Parse the produced scene and check every element ID for
   uniqueness, every reference for a live target, every reciprocal binding in
   both directions, every arrow label for a live arrow `containerId` and the
   reciprocal text entry in that arrow's `boundElements`, and every requested
   concept for coverage. Render and inspect visually when that capability is
   available. Otherwise state that verification was structural only. Completion
   requires all structural checks to pass and the inspection level to be
   reported.

## Example

Request:
`Create a new left-to-right diagram showing Script -> Recording -> Edit, using the bundled visual base.`

Result: a new editable scene with three labeled shapes, two bound arrows, the
base canvas settings, unique IDs, valid reciprocal bindings, and no changes to
the bundled base.
