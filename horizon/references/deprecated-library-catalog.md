# Deprecated Library Catalog

## Date/Time Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `moment.js` | `Temporal API`, `date-fns`, `dayjs`, `luxon` | Legacy project in maintenance mode since 2020; team explicitly discourages new use. Temporal reached TC39 Stage 4 in March 2026 and ships in Chrome/Edge 144 + Firefox 139; use `@js-temporal/polyfill` until Safari ships. date-fns / dayjs remain the pragmatic interim (2KB vs 72KB). |
| `moment-timezone` | `Temporal.ZonedDateTime`, `Intl.DateTimeFormat`, `luxon` | Native `Intl` + Temporal handle timezone conversion without the 900KB IANA data bundle. |

```typescript
// Before: moment
import moment from 'moment';
const formatted = moment().format('YYYY-MM-DD');

// After: date-fns (tree-shakeable)
import { format } from 'date-fns';
const formatted = format(new Date(), 'yyyy-MM-dd');

// After: Native Intl (no dependency)
const formatted = new Intl.DateTimeFormat('sv-SE').format(new Date());
```

## HTTP Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `request` | native `fetch`, `undici`, `got` | Deprecated since 2020, no security patches. Native `fetch` is stable since Node 21; `undici` powers it and is the request-compatible replacement (v6 adds HTTP/3). For drop-in migration, use npm `overrides` to point `request` at `undici`. |
| `axios` (audit before use) | native `fetch` (simple) or `undici`/`got` (advanced) | **Axios maintainer account was compromised on 2026-03-31 (CISA alert 2026-04-20)** — versions `1.14.1` / `0.30.4` contained a RAT and were deprecated. Project itself remains active but treat as a supply-chain risk: verify provenance attestations and pin via lockfile + `trustPolicy: no-downgrade`. |
| `superagent` | native `fetch` | fetch with `AbortController` covers most cases. |
| `node-fetch` | native `fetch` | Native `fetch` shipped in Node 18 and is stable since 21 — `node-fetch` is no longer needed. |

```typescript
// Before: axios
import axios from 'axios';
const { data } = await axios.get('/api/users');

// After: Native fetch
const response = await fetch('/api/users');
const data = await response.json();
```

## Testing Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `enzyme` | `@testing-library/react` | Effectively dead — no adapter for React 18 or 19, no maintainer. React 19 also deprecated `react-test-renderer`, consolidating RTL as the standard. HubSpot/Slack/NYT documented 15K–76K test migrations as reference cases. |
| `sinon` (consider) | `node:test` mocks, `vitest.fn()`, `jest.fn()` | `node:test` ships built-in mock/spy APIs (stable in Node 22+). |
| `karma` | `vitest`, `playwright/test`, `node:test` | Karma was archived. Vitest covers JSDOM-style suites; Playwright handles real-browser tests. |
| `jest` (simple suites, consider) | `node:test` (`node --test`) | For lightweight unit tests, the built-in runner avoids the jest dependency tree entirely. Jest remains valid for snapshot-heavy or large monorepo setups. |
| `mocha` (consider) | `node:test`, `vitest` | Same rationale — keep mocha only where its plugin ecosystem is load-bearing. |

```typescript
// Before: Enzyme
import { shallow } from 'enzyme';
const wrapper = shallow(<MyComponent />);
expect(wrapper.find('.button').text()).toBe('Click');

// After: React Testing Library
import { render, screen } from '@testing-library/react';
render(<MyComponent />);
expect(screen.getByRole('button')).toHaveTextContent('Click');
```

## CSS/Styling Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `node-sass` | `sass` (dart-sass) | node-sass is deprecated. dart-sass is the primary implementation. |
| CSS-in-JS (runtime) | CSS Modules, Tailwind, vanilla-extract | Runtime CSS-in-JS has performance overhead. |
| `@emotion/core` | `@emotion/react` | Package renamed. |

## Utility Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `lodash` (full bundle) | native methods, `lodash-es` (tree-shake), `es-toolkit` | Most lodash use cases now native: `groupBy` → `Object.groupBy` (Baseline 2024), set ops → `Set.prototype.union/.intersection/.difference` (ES2025), chains → Iterator helpers (Baseline 2025-03), `cloneDeep` → `structuredClone`. Frequently flagged in 2026 npm vulnerability reports for prototype pollution. |
| `lodash.groupBy` | `Object.groupBy()` | Native since Chrome 117 / Firefox 119 / Safari 17.4 / Node 20.12. |
| `lodash.chain` / iteration | Iterator helpers | Native since Chrome 122 / Firefox 131 / Safari 18.4 / Node 22. |
| `underscore` | native ES6+ methods | Most utilities now built into JavaScript. |
| `uuid` | `crypto.randomUUID()` | Native in Node 19+ and all evergreen browsers (Secure Context required). |
| `classnames` | `clsx` or template literals | `clsx` is smaller (~250B) and faster; same API. |
| `dotenv` | `--env-file` flag | Native since Node 20. |
| `chalk` | `util.styleText()` | Stable since Node 22. |

```typescript
// Before: lodash
import _ from 'lodash';
const result = _.uniq(array);

// After: Native Set
const result = [...new Set(array)];

// Before: uuid
import { v4 as uuidv4 } from 'uuid';
const id = uuidv4();

// After: Native crypto
const id = crypto.randomUUID();
```

## Build Tools

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `webpack` (consider) | `vite`, `rspack`, `turbopack`, `esbuild` | Vite is the default recommendation in the React docs since CRA sunset. `rspack` (Rust-based, webpack-compatible) is the migration path when webpack config must be preserved. |
| `create-react-app` | `vite`, `next.js`, `remix`, `tanstack/start` | **Officially deprecated by the React team on 2025-02-14** ("Sunsetting Create React App"). No security patches, no dependency updates. React docs now point new users to a framework or to Vite/Parcel/RSBuild. |
| `babel` (consider) | `swc`, `esbuild`, native TS stripping (Node 24+) | SWC/esbuild are 10–100× faster. Babel still required for some custom transforms. |
| `tslint` | `eslint` + `@typescript-eslint` | TSLint was officially deprecated. |
| `ts-node` / `tsx` (erasable syntax) | Native TS stripping (`node file.ts`) | Built-in in Node 24+ for erasable TS syntax (no enums / `namespace` / param-properties / `const enum`). Use `swc`/`tsx` only when those features are required. |
| `node-sass` | `sass` (dart-sass) | node-sass was deprecated; dart-sass is the primary implementation. |

---

## Sources (verified 2026-05)

- React team: [Sunsetting Create React App](https://react.dev/blog/2025/02/14/sunsetting-create-react-app) (2025-02-14)
- TC39: [Temporal proposal](https://tc39.es/proposal-temporal/) reached Stage 4 (March 2026 plenary)
- CISA: [Supply Chain Compromise Impacts Axios npm Package](https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager) (2026-04-20)
- Node.js: [Modules: TypeScript](https://nodejs.org/api/typescript.html), [WebSocket](https://nodejs.org/learn/getting-started/websocket), [release schedule](https://nodejs.org/en/about/previous-releases)
- MDN: [Object.groupBy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy), [Set methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)
- web.dev: [Iterator helpers Baseline](https://web.dev/blog/baseline-iterator-helpers) (2025-03)
