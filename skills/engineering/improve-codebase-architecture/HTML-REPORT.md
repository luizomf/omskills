# HTML Report Format

The architectural review is one HTML artifact in the OS temp directory. It is not offline or self-contained: styling and diagrams require network access to the two exact CDN-loaded resources in the scaffold, and the generated report must disclose both resources visibly.

## Repository-derived value safety

Treat every repository-derived value as untrusted, including repository and module names, paths, excerpts, candidate labels, ADR text, and worker findings. Apply the encoder for the output context every time the value is rendered; never copy repository text into markup or Mermaid grammar.

- **HTML text:** encode `&`, `<`, `>`, `"`, and `'` as `&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&#x27;`. In Python, `html.escape(value, quote=True)` is the reference behavior.
- **HTML attributes:** use only quoted attributes and apply the same five substitutions. Generate structural values such as `candidate-1` and `#candidate-1` independently; never derive an `id`, anchor target, class name, URL, script, style, or event handler from a repository label.
- **Mermaid-visible text:** encode every Unicode scalar as the Mermaid decimal entity `#<decimal Unicode scalar>;`, concatenate those entities, and place the result inside a quoted label. For example, `A<B` becomes `#65;#60;#66;`. Build node identifiers independently in observed order (`n1`, `n2`, ...) and use repository values only in encoded labels. Never interpolate them as identifiers, edge syntax, directives, classes, or links.
- **Nested Mermaid in HTML:** assemble Mermaid from fixed grammar, generated identifiers, and encoded labels, then HTML-text encode the complete Mermaid source before placing it in `<pre class="mermaid">`. Encoding for one parser does not replace encoding for the other.

Use the conceptual placeholders `{{html_text(value)}}`, `{{html_attr(value)}}`, and `{{mermaid_text(value)}}` below only after applying those rules. Before opening the report, exercise its rendering with hostile values containing markup delimiters, quotes, Mermaid arrows, brackets, directives, and repeated labels. Confirm that they remain text and that repeated labels still receive distinct generated identifiers.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{html_text(repo_name)}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "strict" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>
        <h1>Architecture review — {{html_text(repo_name)}}</h1>
        <p>{{html_text(report_date)}}</p>
        <div aria-label="Legend">...</div>
        <aside id="network-dependencies" class="rounded-lg border border-amber-200 bg-amber-50 p-4">
          <h2>Network dependencies</h2>
          <p>This report is one HTML artifact. Styling and diagrams require network access to load these two CDN resources:</p>
          <ul>
            <li>Tailwind CSS runtime — <code>https://cdn.tailwindcss.com</code></li>
            <li>Mermaid 11 ESM — <code>https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs</code></li>
          </ul>
        </aside>
      </header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name, date, and a compact legend: solid box = module, dashed line = seam, red arrow = leakage, thick dark box = deep module. No introduction paragraph — straight into the candidates.

## Candidate card

The diagrams carry the weight. Prose is sparse, plain, and uses the glossary terms (from the `codebase-design` skill) without ceremony.

Each candidate is one `<article>`:

- **Title** — short, names the deepening (e.g. "Collapse the Order intake pipeline").
- **Badge row** — recommendation strength (`Strong` = emerald, `Worth exploring` = amber, `Speculative` = slate), plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **Files** — monospaced list, `font-mono text-sm`.
- **Before / After diagram** — the centrepiece. Two columns, side by side. See patterns below.
- **Problem** — one sentence. What hurts.
- **Solution** — one sentence. What changes.
- **Wins** — bullets, ≤6 words each. e.g. "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR callout** (if applicable) — one line in an amber-tinted box.

If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same — variety is part of the point.

### Mermaid graph (the workhorse for dependencies / call flow)

Use a Mermaid `flowchart` or `graph` when the point is "X calls Y calls Z, and look at the mess." Wrap it in a Tailwind-styled card so it doesn't feel parachuted in. Style with classDef to colour leakage edges red and the deep module dark. Sequence diagrams work well for "before: 6 round-trips; after: 1."

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      n1["{{mermaid_text(module_1_label)}}"] --&gt; n2["{{mermaid_text(module_2_label)}}"]
      n2 --&gt; n3["{{mermaid_text(module_3_label)}}"]
      n3 -.leak.-&gt; n4["{{mermaid_text(module_4_label)}}"]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class n3,n4 leak
  </pre>
</div>
```

The `n1`–`n4` identifiers are generated, not transformed labels. The `&gt;` spellings show the outer HTML-text encoding; the browser restores Mermaid's fixed arrows without exposing repository text to HTML parsing.

### Hand-built boxes-and-arrows (when Mermaid's layout fights you)

Modules as `<div>`s with borders and labels. Arrows as inline SVG `<line>` or `<path>` elements positioned absolutely over a relative container. Reach for this when you want the "after" diagram to feel like one thick-bordered deep module with greyed-out internals — Mermaid won't render that with the right weight.

### Cross-section (good for layered shallowness)

Stack horizontal bands (`h-12 border-l-4`) to show layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band labelled with the consolidated responsibility.

### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module — one for interface surface area, one for implementation. Before: interface rectangle is nearly as tall as the implementation rectangle (shallow). After: interface rectangle is short, implementation rectangle is tall (deep).

### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one box, with the now-internal calls shown faded inside it.

## Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace. Serif optional for headings (`font-serif` works well with stone/slate).
- Colour sparingly: one accent (emerald or indigo) plus red for leakage and amber for warnings.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Use `text-xs uppercase tracking-wider` for module labels inside diagrams — they should read as schematic, not as UI.
- The only remote loads are the Tailwind CDN script and the Mermaid ESM import shown in the scaffold. Keep their exact URLs in the visible network-dependency disclosure. The report is otherwise static — no app code, no interactivity beyond Mermaid's own rendering.

## Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

## Tone

Plain English, concise — but the architectural nouns and verbs come straight from the `codebase-design` skill.

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

**Never substitute:** component, service, unit (for module) · API, signature (for interface) · boundary (for seam) · layer, wrapper (for module, when you mean module).

**Phrasings that fit the style:**

- "Order intake module is shallow — interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** name the gain in glossary terms: *"locality: bugs concentrate in one module"*, *"leverage: one interface, N call sites"*, *"interface shrinks; implementation absorbs the wrappers"*. Don't write *"easier to maintain"* or *"cleaner code"* — those terms aren't in the glossary and don't earn their place.

No hedging, no throat-clearing, no "it's worth noting that…". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it. If a term isn't in the `codebase-design` glossary, reach for one that is before inventing a new one.
