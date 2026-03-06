# draw.io Specs Reference

Purpose: Read this when the output must be editable in draw.io or diagrams.net.

## Contents

- Minimal XML structure
- ID rules
- Shape and edge defaults
- Layout rules
- Quality checklist

## Minimal XML Skeleton

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## ID Rules

- Prefix nodes by type, for example: `proc-1`, `db-1`, `actor-1`.
- Keep IDs stable inside one file.
- Do not reuse IDs for different semantic entities.

## Shape Defaults

| Use | Shape |
|-----|-------|
| Process | Rounded rectangle |
| Decision | Diamond |
| Actor | Rectangle or icon-backed node |
| Database | Cylinder |
| Group | Container / swimlane |

## Edge Defaults

- Prefer orthogonal edges for business and architecture flow.
- Use solid edges for primary flow.
- Use dashed edges for optional, async, or inferred relationships.

## Layout Rules

- Keep the main reading direction consistent.
- Avoid crossing edges when the semantic model allows rearrangement.
- Journey cards commonly need around `180px` width to stay readable.

## Quality Checklist

- Node count stays `<=20`
- Labels are short
- Group boundaries are clear
- Edge direction is readable
- File opens cleanly in draw.io
