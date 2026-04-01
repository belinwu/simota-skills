# Figma Token Sync

Purpose: Use this reference when syncing Figma variables or Token Studio with code, generating DTCG tokens, or automating token diffs in CI.

## Contents

- Sync workflow
- Figma variables structure
- Style Dictionary configuration
- Token Studio workflow
- CI/CD automation
- Manual sync
- Token diff report

## Token Sync Workflow

1. Define or update variables in Figma.
2. Export in DTCG-compatible form.
3. Transform tokens into code artifacts.
4. Verify diffs and dark-mode behavior.
5. Run visual regression when token changes affect UI surfaces.

## Figma Variables Structure

```json
{
  "colors": {
    "primitive": {
      "gray-100": { "value": "#f3f4f6", "type": "color" }
    },
    "semantic": {
      "bg-primary": { "value": "{colors.primitive.gray-100}", "type": "color" }
    }
  },
  "spacing": {
    "6": { "value": "24px", "type": "dimension" }
  }
}
```

Rules:

- Preserve primitive vs semantic separation.
- Prefer a single source of truth per team or repo.
- Keep dark-mode tokens explicit instead of embedding theme ambiguity.
- For Token Studio, keep sets clearly separated, such as `global`, `light`, and `dark`.

## Style Dictionary Configuration

### Style Dictionary v4

```js
export default {
  source: ["tokens/**/*.json"],
  preprocessors: ["tokens-studio"],
  platforms: {
    css: {
      transformGroup: "css",
      buildPath: "dist/css/",
      files: [{ destination: "tokens.css", format: "css/variables", options: { outputReferences: true } }]
    }
  }
};
```

Use v4 for native DTCG support where possible.

## Token Studio For Figma

### Plugin Setup

- Organize token sets by primitive, semantic, and component scope.
- Keep theme variants explicit.
- Sync via Git when the team expects code-first review.

### Token Studio JSON

```json
{
  "global": {
    "color": {
      "bg-primary": {
        "value": "{color.gray.100}",
        "type": "color"
      }
    }
  }
}
```

### Git Sync

- Commit token source files, not only generated assets.
- Review token diffs like code.
- Tag breaking token changes with the lifecycle and semver context.

## CI/CD Automation

### GitHub Actions Example

```yaml
name: sync-tokens
on:
  workflow_dispatch:
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run tokens:build
      - run: npm run test:visual
```

Rules:

- Build generated assets deterministically.
- Review token diffs before publishing.
- Pair token sync with visual regression when UI output changes.

## Manual Sync

1. Export from Figma Variables or Token Studio.
2. Transform into CSS or framework artifacts.
3. Verify changed tokens and affected components.
4. Run visual regression or snapshot checks.

Common commands:

```sh
npx style-dictionary build
git diff src/styles/tokens.css
npm run test:visual
```

## Token Diff Report

```md
### Token Sync Report
- Source:
- Breaking Changes:
- New Tokens:
- Modified Tokens:
- Deprecated Tokens:
- Dark mode impact:
- Visual regression status:
- Action Required:
```

## Style Dictionary v4

| Change | v3 | v4 |
|--------|----|----|
| Module format | CommonJS | ES Modules |
| Instantiation | object | `new StyleDictionary()` |
| Core methods | synchronous | async/await |
| Token identification | CTI structure | `$type` property |
| Hook naming | `transformer`/`formatter` | `transform`/`format` |

DTCG-aware configuration:
```js
import StyleDictionary from 'style-dictionary';

const sd = new StyleDictionary({
  source: ['tokens/**/*.tokens.json'],
  preprocessors: ['tokens-studio'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [{
        destination: 'tokens.css',
        format: 'css/variables',
        options: { outputReferences: true }
      }]
    }
  }
});

await sd.hasInitialized;
await sd.buildAllPlatforms();
```

Auto-migration from v3:
```bash
npx codemod styledictionary/4/migration-recipe
```

Note: v4 has partial DTCG support. Full support is planned for v5.

## Figma Extended Collections (Enterprise, November 2025+)

Create brand/theme variants derived from existing collections:
```json
{
  "parentVariableCollectionId": "VariableCollectionId:1:1",
  "isExtension": true,
  "variableOverrides": {
    "VariableId:1:5": { "value": "#FF6B6B" }
  }
}
```

- `rootVariableCollectionId` (January 2026): returns the top-level ancestor collection node ID.
- Set `null` in an extended collection to fall back to the parent value.
- Variables REST API requires Enterprise org with Full seat access.
