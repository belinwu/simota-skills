# Parameter Space

**Purpose:** Tunable-parameter taxonomy, bounds, constraints, and hot-path indicators for the DESIGN phase.
**Read when:** Deciding which parameters to tune and across what range.

## Contents
- Domain Catalog
- JVM Runtime
- Node.js Runtime
- Go Runtime
- Python Runtime
- Connection Pools
- Thread / Worker Pools
- Cache Sizing
- Batch / Micro-batch
- Autoscaler Targets
- LLM Serving
- Kernel / OS
- Parameter Space Specification Schema
- Co-Tuning Decomposition Rules

---

## Domain Catalog

| Domain | Owner | Typical campaign size | Risk of co-effect |
|--------|-------|------------------------|---------------------|
| JVM runtime | App | 3–6 params | High (GC × heap × thread) |
| Node.js runtime | App | 2–4 params | Medium |
| Go runtime | App | 2–3 params | Low |
| Python runtime | App | 1–3 params | Medium (GIL × workers) |
| TypeScript toolchain | Build / CI / DX | 2–4 params | Medium (worker × isolate × cache) |
| Build & monorepo toolchain | Build / CI | 2–5 params | Medium (workers × cache × shards) |
| Test tooling | CI / Dev | 2–4 params | Medium (parallelism × isolation × flake) |
| Developer tooling (lint / format / package mgr / container) | Dev / CI | 1–3 params | Low |
| Connection pools | App ↔ DB | 2–4 params | High (with Tuner) |
| Thread / worker pools | App | 2–3 params | High (saturation × queue) |
| Cache sizing | App | 1–3 params | Medium |
| Batch / micro-batch | App | 1–2 params | Low |
| Autoscaler targets | Platform | 2–3 params | Medium |
| LLM serving | App ↔ Oracle | 3–6 params | High |
| Kernel / OS | Platform | 1–3 params | Low (large effect) |

**Rule**: Default search dimension is `≤ 5`. Beyond 5 parameters, decompose into sequential sub-campaigns. Co-tuning ≥ 3 parameters at once degrades attribution and rollback.

---

## JVM Runtime

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `-Xmx` (heap max) | `[1g, available_ram × 0.75]` | leave headroom for native + threads | RSS climbing or OOM |
| `-Xms` initial heap | `= -Xmx` for steady workloads | avoids resize churn | Startup throughput |
| GC algorithm | `{G1, ZGC, Shenandoah, Parallel}` | discrete | Pause vs throughput need |
| `-XX:MaxGCPauseMillis` | `[50, 500]` ms (G1) | soft target | p99 GC pause > SLO/4 |
| `-XX:ParallelGCThreads` | `[1, vCPU]` | for parallel collectors | GC CPU share |
| `-XX:ConcGCThreads` | `[1, vCPU/4]` | for G1/ZGC | Concurrent mark cost |
| `-XX:G1HeapRegionSize` | `{1m, 2m, 4m, 8m, 16m, 32m}` | discrete; auto-sized by default | Large humongous alloc |
| `-XX:InitiatingHeapOccupancyPercent` | `[25, 70]` | when to start concurrent cycle | Mixed GC efficiency |
| JIT compile thresholds | `[100, 10000]` invocations | per tier | Warmup time vs steady |
| `-XX:+UseStringDeduplication` | boolean | G1 only | String-heavy heap |

**Sensitive constraints**:
- Heap > available RAM × 0.75 risks OS swap; never exceed.
- Don't co-tune GC algorithm with heap size in one campaign — fix algorithm first, then heap, then pause target.
- Container memory limit must be ≥ `-Xmx + native overhead (~25%)`.

---

## Node.js Runtime

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `--max-old-space-size` (MB) | `[512, container_mem × 0.75]` | matches container limit | RSS climbing, OOM kills |
| `--max-semi-space-size` (MB) | `[16, 1024]` | young-gen scavenge cost | Scavenge GC frequent |
| `UV_THREADPOOL_SIZE` | `[4, 128]` | libuv fs / dns / crypto | fs/dns/crypto waiting |
| Cluster workers | `[1, vCPU × 2]` | classic cluster mode | CPU under-utilized |
| Worker threads | `[0, vCPU]` | CPU-bound offload | CPU-bound main thread |
| `--max-http-header-size` | `[8k, 80k]` bytes | denial-of-service risk if large | Header-heavy traffic |

**Sensitive constraints**:
- `UV_THREADPOOL_SIZE` change requires restart; environment-set only.
- Worker count interacts with HPA — pin one before tuning the other.

---

## Go Runtime

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `GOGC` | `[25, 800]` | percent heap growth before GC | GC CPU > 10% |
| `GOMEMLIMIT` | `[mem × 0.5, mem × 0.9]` | Go 1.19+ soft memory limit | RSS spikes, OOM |
| `GOMAXPROCS` | `[1, vCPU]` | usually `= container vCPU` | Scheduler latency / waste |

**Sensitive constraints**:
- `GOMEMLIMIT` and `GOGC` interact — high `GOGC` with low `GOMEMLIMIT` triggers aggressive emergency GC. Set both, observe both.
- In Kubernetes, `GOMAXPROCS` should match the CPU request, not the node — use `automaxprocs`.

---

## Python Runtime

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Gunicorn `workers` | `[1, vCPU × 2 + 1]` | per process | CPU under-utilized |
| Gunicorn `threads` | `[1, 50]` | per worker (sync workers only) | I/O-bound |
| Gunicorn `worker_class` | `{sync, gevent, uvicorn.workers.UvicornWorker}` | choose async if mostly I/O | Concurrency saturation |
| Uvicorn `--workers` | `[1, vCPU × 2]` | ASGI | Throughput cap |
| `PYTHONMALLOC` | `{default, malloc}` | mostly diagnostic | RSS bloat |
| `--gc-threshold` (CPython) | tuple `(700, 10, 10)` default | gc collection cadence | gc cycle CPU |

---

## TypeScript Toolchain

TypeScript projects expose tunable knobs in three places: **compile/build time** (tsc, swc, esbuild, Vite, Next.js), **test time** (Jest, Vitest), and **dev / editor time** (tsserver, tsx, ts-node). Production runtime knobs live under **Node.js Runtime**. Bolt owns one-shot speedups; Dial owns continuous tuning campaigns when build/test latency or memory is a recurring cost.

### tsc / build (and the tsgo transition)

As of 2026-Q2 the TypeScript compiler landscape is split: production teams still ship on `tsc` (Node, TS ≤ 5.x), while TypeScript 7.0 beta ships a Go-native port (`tsgo`, project Corsa) that reports ~10× cold compile speedups on the VS Code codebase (78s → 7.5s). Treat the `tsc` → `tsgo` swap as a **Horizon migration**, not a Dial knob; Dial tunes *within* whichever compiler is in place. [Source: Microsoft DevBlogs - A 10x Faster TypeScript](https://devblogs.microsoft.com/typescript/typescript-native-port/) [Source: InfoWorld - Microsoft steers native port to early 2026](https://www.infoworld.com/article/4100582/microsoft-steers-native-port-of-typescript-to-early-2026-release.html)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `compilerOptions.incremental` | `{true, false}` | requires `.tsbuildinfo` writable | full-build time vs incremental ratio |
| `compilerOptions.composite` + `references` | per-package boolean | enables project-level caching | typecheck wall time on multi-package repo |
| `compilerOptions.skipLibCheck` | `{true, false}` | type-correctness vs build speed | `node_modules/**/*.d.ts` parse share in profile |
| `compilerOptions.isolatedModules` | `{true, false}` | enables single-file emit for SWC/esbuild | transpile parallelism unlocked |
| `compilerOptions.isolatedDeclarations` | `{true, false}` | enables parallel `.d.ts` emission | declaration-build wall time on multi-package repo |
| `compilerOptions.assumeChangesOnlyAffectDirectDependencies` | `{true, false}` | trade-off: faster rebuild vs missed downstream type errors | `--build` rebuild time |
| `compilerOptions.moduleResolution` | `{node, bundler, node16, nodenext}` | must match runtime + bundler | resolution cost in cold build |
| Parallel typecheck workers (`fork-ts-checker` / Nx `--parallel` / Turbo `--concurrency`) | `[1, vCPU]` | CI agent vCPU | typecheck wall time |
| `tsgo` opt-in (`@typescript/native-preview` / TS 7 beta) | `{tsc, tsgo}` | feature parity caveats; not yet 1:1 with tsc | cold typecheck wall time |
| SWC `jsc.parser.syntax` | `{typescript, ecmascript}` | choose `typescript` for `.ts` | per-file parse time |
| esbuild `target` / `treeShaking` / `splitting` | discrete | runtime support floor | bundle size, parse cost |
| Build cache (Turborepo / Nx / `tsbuildinfo`) | enabled / disabled / remote | network for remote cache | cache hit rate |

**Sensitive constraints**:
- `skipLibCheck: true` is the highest-leverage single change for cold tsc time but defers `.d.ts` regressions; pair with a nightly full-check job.
- `isolatedModules: true` unlocks SWC / esbuild transpile but rejects const-enum re-export and certain ambient patterns — measure migration cost before campaigning.
- `isolatedDeclarations: true` is the prerequisite for parallel declaration emission and is the highest-leverage knob for multi-package monorepo `tsc -b` wall time.
- `tsgo` (TS 7 beta) ships through `@typescript/native-preview@beta` and Microsoft labels it production-ready for many day-to-day flows, but feature parity is incomplete — gate adoption behind a Horizon migration plan, then let Dial tune within whichever compiler ships.
- Worker count rarely scales past `vCPU` — over-subscription wastes cache locality.

### Test runners

Vitest 3 (released early 2026) introduced **browser-test `instances`** (replacing the workspace pattern for multi-browser matrices) and **line-number test selection** (`vitest file.ts:10`); both reduce the search space for CI campaigns by making the evaluator's invocation cheaper. [Source: Vitest 3.0 release blog](https://vitest.dev/blog/vitest-3)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Vitest `pool` | `{threads, forks, vmThreads, vmForks}` | threads = fastest, forks = strongest isolation, vm* = experimental | suite wall time, leak rate |
| Vitest `poolOptions.threads.maxThreads` / `minThreads` | `[1, vCPU]` | per-process workers | CPU under-use vs OOM |
| Vitest `poolOptions.threads.singleThread` | `{true, false}` | disables parallelism | I/O-bound suite serialization |
| Vitest `isolate` | `{true, false}` | shared module graph between tests when `false` | suite wall time vs flake risk |
| Vitest `maxConcurrency` | `[1, 50]` | concurrent tests per file | I/O-bound parallelism |
| Vitest `sequence.shuffle` | `{true, false}` | flake detection vs cache locality | flaky-test surfacing |
| Vitest 3 browser-test `instances` (per-browser) | discrete list | one Vite server shared across instances; cheaper than workspace | per-browser wall-time vs cache cost |
| Jest `maxWorkers` | `[1, vCPU - 1]` or `"50%"` | CI vCPU minus reservation | suite wall time |
| Jest `workerIdleMemoryLimit` | `[256MB, 2GB]` | recycle worker before OOM | worker RSS growth |
| `ts-jest` `isolatedModules` vs `@swc/jest` | discrete | type-safety vs speed | per-file transform time |
| Bun `bun test` parallelism (`--concurrency`) | `[1, vCPU]` | Jest-compatible API; native TS, no transpile step | suite wall time |
| Bun `bun test` watch + filter | discrete | per-package cache | dev-loop latency |

**Sensitive constraints**:
- Vitest `pool: 'threads'` shares the V8 isolate across workers — fastest, but tests that mutate global state must isolate. Switch to `forks` only if leaks proven.
- Vitest 3 `instances` for browser tests share a single Vite server — *prefer over `workspace`* for multi-browser CI campaigns; the workspace pattern is being retired.
- Jest `maxWorkers` set too high causes context-switch thrash; CI agents with 4 vCPU often optimize at `2–3`, not `4`.
- Bun's test runner has no transpile step (TS executes directly) so `repeats_per_eval` can be lower than in Jest/Vitest — but Bun is *not* a drop-in for every Jest API; gate the runner choice through Horizon and let Dial tune only after the runner is fixed.

### dev / editor

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| tsserver `--max-old-space-size` (via `TS_SERVER_MAX_OLD_SPACE_SIZE` or VSCode `typescript.tsserver.maxTsServerMemory`) | `[2048, 16384]` MB | within machine RAM | tsserver OOM, autocomplete lag |
| tsserver `disableSourceOfProjectReferenceRedirect` | `{true, false}` | reduces ref graph cost | IDE response on large monorepo |
| `tsx watch` debounce / `ts-node-dev` `--respawn-delay` | `[100, 2000]` ms | restart cost vs responsiveness | restart frequency |
| Vite `optimizeDeps.include` / `exclude` | per-dep | dev cold-start | dev cold-start time |
| Vite `server.warmup.clientFiles` | `[0, 50]` paths | initial-route HMR | first-render delay |

### Next.js / Turbopack

As of Next.js 16 (Oct 2025), **Turbopack is the default bundler for both `next dev` and `next build`**; Next.js 16.1 added stable File System Caching and 16.2 added SRI, postcss.config.ts, dynamic-import tree-shaking, and Server Fast Refresh. Real-world reports show 2–5× faster production builds vs webpack. The "Turbopack vs webpack" knob is therefore vestigial on new Next.js projects — treat staying on webpack as the *non-default* choice that must be justified. [Source: Next.js 16.2 Turbopack release notes](https://nextjs.org/blog/next-16-2-turbopack) [Source: Progosling - Next.js 16 makes Turbopack stable and the default](https://progosling.com/en/dev-digest/2026-02/nextjs-16-turbopack-default)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `experimental.parallelServerCompiles` | `{true, false}` | RSC + route handler parallel | server compile wall time |
| Turbopack File System Caching (`turbopack.cacheConfig`) | enabled / disabled / persistent | disk space, cache-invalidation correctness | repeated-build hit rate |
| Webpack-fallback opt-out (`next build --webpack` on Next.js 16) | `{turbopack, webpack}` | webpack is now the *exception*; only when a Turbopack incompatibility is documented | build wall-time delta |
| Webpack `parallelism` (when fallback is in use) | `[1, vCPU]` | module build parallelism | build wall time |

**Co-tuning notes**:
- TypeScript-toolchain campaigns are typically run **in CI** with the build/test pipeline as the evaluator. Wall-clock time and CI cost ($/build) are the natural objective.
- Wall-clock time is **noisier in shared CI runners** than in production — increase `repeats_per_eval` to `5+` and prefer dedicated runners for the campaign.
- For frontend bundles, hand off bundle-size objective to **Bolt** (`bundle` recipe); Dial only co-tunes when bundle size enters the objective alongside build time.

---

## Build & Monorepo Toolchain

Language- and framework-agnostic build, bundler, monorepo, CI shard, and container parameters. Evaluator is the CI pipeline; objective is wall-clock and `$/build`.

### Java / Kotlin (Gradle, Maven)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Gradle `org.gradle.parallel` | `{true, false}` | tasks must be parallel-safe | configuration + execution time |
| Gradle `org.gradle.workers.max` | `[1, vCPU]` | cap worker daemons | worker over-subscription |
| Gradle `org.gradle.caching` | `{true, false}` | remote-cache infra | repeated-build hit rate |
| Gradle `org.gradle.configuration-cache` | `{true, false}` | plugin compatibility | configuration phase time |
| Gradle `org.gradle.jvmargs -Xmx` | `[2g, mem × 0.75]` | OOM on big modules | daemon OOM, GC pause |
| Gradle daemon `idle-timeout` | `[1m, 3h]` | CI worker recycling | cold-start cost |
| Maven `-T <N>` / `-T 1C` | `[1, vCPU]` (or per-core) | thread-safe plugins | build wall-time |
| Maven `--offline` / `--no-snapshot-updates` | boolean | dependency freshness | network spend |

### Rust (Cargo, sccache)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `CARGO_BUILD_JOBS` / `--jobs` | `[1, vCPU]` | linker-bottleneck workload | wall-time, RAM peak |
| `CARGO_INCREMENTAL` | `{0, 1}` | cache size on CI | rebuild time |
| `[profile.dev]` `codegen-units` | `[1, 256]` | LTO compatibility | parallel codegen |
| `[profile.release]` `lto` | `{off, thin, fat}` | runtime perf vs build cost | release-build wall-time |
| `sccache` enable / remote backend | on / off / S3 / GCS | network + token | compile-cache hit rate |
| Linker (`mold`, `lld`, `ld64`) | discrete | OS compatibility | link phase time |

### Go

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `GOFLAGS=-p=<N>` (parallel compile) | `[1, vCPU]` | CPU cap | compile wall-time |
| `GOCACHE` path / size | path; size implicit | disk space | cache hit rate |
| `GOMODCACHE` location | shared volume in CI | network | dep-fetch time |
| `-trimpath`, `-buildvcs=false` | boolean | reproducibility vs debug | minor wall-time |

### Bundlers (Webpack / Rollup / esbuild / Rolldown / Rspack / Parcel)

As of 2026-Q2 the JS bundler market has split into a **Rust-native tier** (Rolldown, Rspack, Turbopack, esbuild 0.24+) and a **legacy JS tier** (Webpack, Rollup). Vite 8 ships **Rolldown as its single bundler** (replacing both esbuild dev-server and Rollup production build); Rolldown reached 1.0-RC in January 2026 and the Vite team reports 10–30× build speedups vs Rollup. Rspack 1.x is the drop-in webpack-config-compatible alternative (cold dev ~1.4s, prod build < 4s on large apps). Treat the bundler swap as a Horizon migration; Dial tunes inside the chosen bundler. [Source: Vite 8 + Rolldown announcement](https://www.theregister.com/2026/03/16/vite_8_rolldown/) [Source: Rolldown integration guide](https://v7.vite.dev/guide/rolldown)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Webpack `parallelism` | `[1, vCPU]` | module-build parallelism | build wall-time |
| Webpack `cache.type` (`filesystem`) + `cache.buildDependencies` | discrete | invalidation correctness | rebuild speed |
| `terser-webpack-plugin` / `swcMinifyPlugin` `parallel` | `[1, vCPU]` | minify cost | build wall-time |
| esbuild `workers` / `--bundle` `--splitting` | `[1, vCPU]` / bool | runtime support | build wall-time, chunk count |
| Rollup `output.experimentalMinChunkSize` | `[0, 100_000]` bytes | chunking heuristic | chunk count |
| Rolldown `minify` (alpha) / `treeshake` / `optimization.inlineConst` | discrete | minifier is alpha — gate behind Horizon | build wall-time, bundle size |
| Rspack `experiments.cache.type` + `parallelism` | discrete / `[1, vCPU]` | webpack-config compatible | rebuild speed |
| Vite `optimizeDeps.holdUntilCrawlEnd` (v6+) | `{true, false}` | dev cold-start latency vs HMR correctness | dev cold-start |
| Parcel `--cache-dir` / `--workers` | path / `[1, vCPU]` | cache invalidation | wall-time |

### Monorepo Orchestration

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Turborepo `--concurrency` | `[1, vCPU × 2]` | I/O-bound tasks | wall-time |
| Turborepo `remoteCache` (Vercel / self-hosted) | on / off | network + auth | cache hit rate |
| Turborepo `daemon` | on / off | local-only acceleration | repeated invocation |
| Nx `--parallel` / `nx.json` `parallel` | `[1, vCPU]` | task graph independence | wall-time |
| Nx Cloud / `nx-remote-cache` | on / off | network | cache hit rate |
| Bazel `--jobs` | `[1, vCPU × 2]` | remote workers available | wall-time |
| Bazel `--remote_executor` / `--remote_cache` | on / off | network bandwidth | local CPU underuse |
| Bazel `--disk_cache` path | path | disk space | repeat-build speed |
| Buck2 `--threads` | `[1, vCPU]` | per-process cap | wall-time |
| Pants `--process-execution-parallelism` | `[1, vCPU]` | per-stage cap | wall-time |

### CI Sharding

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| GHA `strategy.matrix` shard count | `[1, 32]` | per-job startup overhead vs parallelism | total wall-time, `$/build` |
| CircleCI `parallelism` | `[1, 32]` | per-job overhead | wall-time |
| Buildkite agent count | `[1, fleet_cap]` | agent cost | queue wait + run time |
| GitLab `parallel: N` | `[1, 100]` | runner pool | wall-time |

### Container Build

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Docker BuildKit `--jobs` (buildx) | `[1, vCPU]` | per-stage parallelism | image build time |
| Build cache mount `--mount=type=cache,id=...` | per language (`/root/.npm`, `/root/.cache/go-build`, `~/.cargo`, `~/.gradle`) | cache-id stability | cache hit rate |
| Registry-based cache `--cache-from`/`--cache-to type=registry,mode=max` | on / off | registry bandwidth | image build time |
| Multi-stage parallelism (`--target`) | discrete | DAG dependencies | wall-time |
| `--platform linux/amd64,linux/arm64` (multi-arch) | discrete | QEMU vs native | per-arch wall-time |

**Sensitive constraints**:
- CI shards beyond `vCPU / per-shard-cost-floor` saturate the queue — each new shard adds ~20–40s startup overhead.
- Remote cache for Bazel / Turborepo / Gradle is high-leverage but requires network + auth + cold-cache fallback testing.
- Container `--mount=type=cache` is the highest-leverage container-build optimization; pair with a stable `id` per language and a cleanup policy.

---

## Test Tooling

Language- and framework-specific test runners. Wall-clock time + flake rate is the natural objective. (TypeScript Vitest / Jest are in the **TypeScript Toolchain** section above.)

### Python (pytest, unittest)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `pytest -n <N>` (`pytest-xdist`) | `[1, vCPU × 2]` | shared-state flakes | suite wall-time |
| `pytest-xdist --dist {load, loadscope, loadfile, worksteal}` | discrete | per-class fixture cost | per-worker imbalance |
| `pytest --maxfail=<N>` | `[1, ∞]` | fail-fast vs coverage | feedback latency on red |
| `pytest --reruns <N>` (`pytest-rerunfailures`) | `[0, 3]` | masks real flakes | reported flake rate |
| `pytest --collect-only` profiling | run once | identifies slow collection | collection phase share |
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` | boolean | plugin compat | startup time |

### Ruby (RSpec, Minitest)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `parallel_tests` `PARALLEL_TEST_PROCESSORS` | `[1, vCPU]` | per-DB schema isolation | suite wall-time |
| RSpec `--profile <N>` (slowest N spec report) | `[5, 50]` | analysis only | slow-spec identification |
| RSpec `--order rand:<seed>` | seed | flake detection | flake surfacing |
| `--fail-fast` | boolean | CI cost vs feedback | feedback on red |

### Java / Kotlin (JUnit, Gradle Test, Maven Surefire)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Gradle Test `maxParallelForks` | `[1, vCPU]` | shared resource (DB, port) | suite wall-time |
| Gradle Test `forkEvery` | `[0, 100]` | JVM startup cost vs leak isolation | per-fork JVM startup share |
| Gradle Test `jvmArgs -Xmx` per fork | mem | total = `forks × Xmx ≤ container mem` | OOM kill in fork |
| Surefire `forkCount` / `reuseForks` | `[1, vCPU]` / bool | classpath sharing | wall-time |
| JUnit Platform `junit.jupiter.execution.parallel.enabled` | boolean | test-class thread safety | wall-time |
| JUnit Platform `parallel.mode.default` / `mode.classes.default` | `{same_thread, concurrent}` | shared state | wall-time |

### Go

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `go test -p <N>` (pkg parallelism) | `[1, vCPU]` | per-pkg fixtures | wall-time |
| `-parallel <N>` (within pkg) | `[1, 100]` | `t.Parallel()` ratio | per-pkg under-use |
| `-race` | boolean | 5–10× slowdown | CI cost vs safety |
| `-shuffle on,<seed>` | seed | order-dependence | flake surfacing |
| `-timeout` | `[30s, 30m]` | CI wall-time cap | timeout hits |
| `-count <N>` | `[1, 10]` | flake confirmation | re-run cost |

### Rust

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `cargo test --jobs` | `[1, vCPU]` | compile-only stage | compile share |
| `cargo nextest --test-threads` | `[1, vCPU × 2]` | binary linking | test exec wall-time |
| `cargo nextest --retries` | `[0, 3]` | masks flakes | reported flake rate |
| `cargo nextest --partition count:<i>/<n>` | shard | CI distribution | total wall-time |

### Browser E2E (Playwright, Cypress)

Playwright 1.59 (April 2026) added `browser.bind()` for one shared browser across CLI/MCP/tests and `playwright-cli show` for a live multi-worker dashboard — these change the *evaluator*, not the parameter space, but they tighten the worker-tuning feedback loop in CI. [Source: Playwright 1.59 Release Breakdown](https://scrolltest.com/playwright-1-59-release-breakdown/)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Playwright `workers` | `[1, vCPU × 2]` | RAM per browser context | wall-time vs OOM |
| Playwright `fullyParallel` | boolean | shared-state tests | wall-time |
| Playwright `retries` | `[0, 3]` | masks flakes — guardrail, not knob | reported flake rate |
| Playwright `expect.timeout` | `[1s, 30s]` | flake vs latency tolerance | timeout hits |
| Playwright `use.video` / `trace` | discrete | artifact size | CI storage |
| Playwright `browser.bind()` reuse mode (1.59+) | `{per-test, shared}` | per-test isolation vs reuse cost | per-spec setup wall-time |
| Playwright shard count (CI `--shard=N/M`) | `[1, 32]` | balanced via prior-run timing, not file count | total wall-time |
| Cypress `--parallel` (Cloud) + machines | `[1, 32]` | Cloud cost | wall-time |
| Cypress `numTestsKeptInMemory` | `[0, 50]` | RAM per browser | OOM |

### Mocha

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `parallel` + `jobs` | bool / `[1, vCPU]` | shared global state | wall-time |
| `timeout` | `[2s, 60s]` | flake vs latency | timeout hits |

**Sensitive constraints**:
- Test parallelism `> vCPU` rarely helps and often hurts due to context-switch thrash and shared-resource contention.
- Retries (`--reruns`, `--retries`) inflate green builds but *mask* real flakes — set a separate **flake-rate guardrail** so the optimizer cannot trade correctness for wall-time.
- E2E shards benefit from **load-balancing by previous run duration**, not file count. Pair shard tuning with that strategy or shard count is wasted.

---

## Developer Tooling

Lint, format, package manager, and container-tool parameters. Evaluator is dev-loop wall-clock or CI wall-clock; objective is time + cache hit rate.

### Lint / Format

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| ESLint `--cache` + `--cache-strategy {metadata, content}` | bool / discrete | filesystem stat reliability | repeated-run wall-time |
| ESLint `--max-warnings` | `[0, ∞]` | strict vs warn | CI failure rate |
| ESLint parallel workers (`eslint_d`, `lint-runner`) | `[1, vCPU]` | rule shared state | wall-time |
| Prettier `--cache` + `--cache-strategy` | bool / discrete | cache size | wall-time |
| Ruff `--cache-dir`, `--target-version`, `--line-length` | path / discrete | none | lint wall-time (typically `< 1s` already) |
| RuboCop `--parallel` + `--cache` | bool / bool | cache invalidation | wall-time |
| golangci-lint `--concurrency` + `--timeout` + enabled linters | `[1, vCPU]` / `[1m, 30m]` / discrete | each linter has its own cost surface | per-linter cost share |
| Biome `--max-diagnostics` / `vcs.enabled` | discrete | VCS sync | wall-time |

### Package Managers

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| npm `--prefer-offline` / `--no-audit` / `--no-fund` | boolean | freshness vs speed | install wall-time |
| pnpm `network-concurrency` | `[1, 64]` | registry rate-limit | install wall-time |
| pnpm `--prefer-offline` / `--lockfile-only` | boolean | freshness vs speed | install wall-time |
| pnpm `package-import-method` (`hardlink`, `clone`, `copy`) | discrete | filesystem support | linking time |
| yarn `--network-concurrency` / `--mutex network` | `[1, 64]` / discrete | parallel runs | install wall-time |
| Bun `bun install --concurrent-scripts` / `--ignore-scripts` | `[1, 256]` / bool | postinstall safety | install wall-time |
| Bun `bun.lockb` (binary) vs `bun.lock` (text, 1.2+) | discrete | reviewability vs parse speed | CI checkout + install wall-time |
| pip `--no-cache-dir` / `--prefer-binary` | boolean | wheel availability | install wall-time |
| uv `--cache-dir` / `--no-build-isolation` | path / boolean | reproducibility | install wall-time |
| Gradle dependency-cache lock + `--refresh-dependencies` | boolean | freshness | install wall-time |
| Maven `~/.m2/repository` cache mount in CI | path | CI volume | install wall-time |

**Sensitive constraints**:
- ESLint `--cache-strategy content` is more correct under filesystem-stat unreliability (Docker, network FS) but slightly slower than `metadata`.
- Package-manager `network-concurrency` is bounded by registry rate-limits and a private registry's NAT/CDN edge, not just local CPU.
- pnpm `package-import-method=hardlink` is the fastest on supported filesystems but breaks under tmpfs or cross-device mounts.

**Co-tuning notes**:
- Build, test, and dev-tooling campaigns share an evaluator (CI pipeline). Run them as **sequential sub-campaigns** rather than co-tuning across domains — attribution requires it.
- For lint/format, the absolute time is often `< 1s` per run on Ruff/Biome; Dial is justified only when the aggregate over a large monorepo or PR-bot cycle is the cost driver.

---

## Connection Pools

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| HikariCP `maximumPoolSize` | `[5, db_max_connections × 0.8 / app_replicas]` | total across replicas ≤ DB cap | Queue wait > 10ms |
| HikariCP `idleTimeout` | `[30s, 30m]` | connection lifecycle | Idle conn count high |
| HikariCP `maxLifetime` | `[10m, 30m]` | < DB-side timeout | Forced disconnects |
| pgbouncer `pool_size` | `[5, 100]` per DB | transaction-pool mode preferred | Server conn pressure |
| pgbouncer `default_pool_size` | sum ≤ `max_client_conn` | global cap | Conn errors |
| Redis pool size | `[10, 200]` | per-replica | BLPOP / pipeline saturation |
| gRPC channel count | `[1, 16]` per upstream | HTTP/2 multiplexing | Head-of-line blocking |

**Sensitive constraints**:
- `maximumPoolSize × replicas ≤ DB max_connections × 0.8` — leaving 20% headroom for migrations and admin.
- Hand off DB-internal trade-offs (max_connections, work_mem) to **Tuner**.

---

## Thread / Worker Pools

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Tomcat `maxThreads` | `[50, 2000]` | per connector | Queue depth growing |
| Tomcat `acceptCount` | `[10, 1000]` | OS accept backlog | Connection refused |
| Puma `workers` | `[1, vCPU × 2]` | process | CPU under-used |
| Puma `threads` (`min:max`) | `[1:5, 5:32]` | per worker | GIL contention (CRuby) |
| Nginx `worker_processes` | `auto` or `[1, vCPU]` | one per core | CPU under-used |
| Nginx `worker_connections` | `[1024, 65536]` | per worker | `worker_connections not enough` |
| Adaptive concurrency limit | dynamic | Netflix concurrency-limits | use MAB / Vegas / Gradient |

**Sensitive constraints**:
- Adaptive concurrency (Vegas / Gradient algorithm) replaces fixed pool size and adapts to backend latency. Strong default for pools facing variable backends.

---

## Cache Sizing

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Caffeine `maximumSize` | `[1000, JVM heap × 0.4 / avg_entry_bytes]` | within heap | hit ratio < 0.85 |
| Caffeine `expireAfterWrite` | `[30s, 24h]` | TTL | staleness vs miss cost |
| Redis `maxmemory` | `[0.5g, instance × 0.75]` | leave OS headroom | evict events |
| Redis `maxmemory-policy` | `{allkeys-lru, volatile-lru, allkeys-lfu, volatile-lfu, noeviction}` | discrete | working set fit |
| In-process LRU size | `[100, 1_000_000]` entries | within process heap | hit ratio < 0.8 |
| HTTP `s-maxage` | `[30s, 24h]` | CDN freshness | origin RPS > target |

**Sensitive constraints**:
- Optimize on hit-ratio surface, not on raw cache size. Beyond a knee point, size has diminishing returns.
- Always pair cache-size tuning with **TTL** and **stampede protection** (see Bolt).

---

## Batch / Micro-batch

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Kafka producer `linger.ms` | `[0, 200]` ms | latency vs batch size trade | small batches |
| Kafka producer `batch.size` | `[16k, 1m]` bytes | memory per partition | tput cap |
| DataLoader batch window | `[1, 50]` ms | request-coalescing window | per-call overhead high |
| DB statement batch size | `[100, 10000]` rows | depends on row size | per-call overhead |
| BFF / gateway batch window | `[1, 50]` ms | request coalescing | small-payload spam |

---

## Autoscaler Targets

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| HPA target CPU | `[40, 80]` % | leave headroom for spike | scale oscillation |
| HPA target memory | `[60, 85]` % | OOM risk above 90 | OOM kills |
| KEDA queue-depth target | `[1, 100]` msgs/replica | per scaler | queue lag |
| HPA scale-up stabilization | `[0, 300]` s | prevent thrash | rapid scale flapping |
| HPA scale-down stabilization | `[60, 1800]` s | longer than up | premature downscale |
| Min replicas | `[1, baseline_rps / per_replica_capacity × 1.2]` | cold start cost | first-request latency |

---

## LLM Serving

Co-design with **Oracle** for AI workload. Multiple serving stacks expose different knob sets — Dial picks the stack-appropriate parameter space.

### vLLM (v1 / Model Runner V2)

vLLM V1's Model Runner V2 (introduced in v0.17.0+) reports ~56% throughput gains over the legacy runner on GB200 and unlocked async-scheduled speculative decoding with zero-bubble overlap. Treat MRV2 vs legacy as a *categorical*, not a knob — fix the runner first, then tune. [Source: vLLM Benchmarks 2026](https://www.morphllm.com/vllm-benchmarks)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| vLLM `--max-num-seqs` | `[8, 256]` | KV-cache memory cap | queue wait |
| vLLM `--gpu-memory-utilization` | `[0.7, 0.95]` | OOM if too high | tok/s ceiling |
| vLLM `--max-num-batched-tokens` | `[1024, 16384]` | throughput vs first-token latency | TTFT vs TPS |
| KV-cache block size | `{16, 32, 64}` tokens | discrete | memory fragmentation |
| Prefix-cache (Automatic Prefix Caching) enable + reuse window | bool + TTL `[60s, 1h]` | hit ratio vs staleness | prefix hit ratio < 0.5 |
| CPU KV-cache offload (V1) | on / off | host RAM, PCIe bandwidth | GPU KV pressure, preemptions |
| FlashAttention backend | `{FA2, FA3, FA4}` | hardware + model support | attention CPU/HBM share |
| Speculative decoding method | `{none, ngram, eagle, mtp, medusa}` | model + draft availability | acceptance rate, TPS sub-linearity |
| Speculative decoding draft length `k` | `[2, 8]` tokens | acceptance rate × verify cost | TPS / accept-rate curve |
| Async-scheduled spec decode (V1) | on / off | requires MRV2 | scheduler bubble share |
| Tensor parallelism degree | `{1, 2, 4, 8}` | per GPU count | inter-GPU bandwidth |
| Pipeline parallelism stages | `{1, 2, 4}` | latency vs throughput | bubbles |

**Sensitive constraints**:
- `max_num_seqs × max_seq_len × bytes_per_token ≤ KV-cache budget` — violating this OOMs.
- Speculative decoding method is *not* a numeric knob — it depends on draft-model availability and target-model family. Treat as categorical; tune `k` and acceptance-threshold afterward. NGram is the cheapest baseline and now runs on GPU in vLLM V1. [Source: Red Hat Developer - vLLM gpt-oss spec decode](https://developers.redhat.com/articles/2026/04/16/performance-improvements-speculative-decoding-vllm-gpt-oss)
- FlashAttention 4 lands in V1 with hardware floors — verify GPU compatibility before adding it as a tunable.

### SGLang (RadixAttention-led workloads)

SGLang's RadixAttention gives ~29% throughput edge over vLLM on H100 for prefix-heavy workloads (e.g., chat with system prompt reuse). Choose SGLang as the stack first; then tune. [Source: Spheron - vLLM vs TensorRT-LLM vs SGLang H100 Benchmarks 2026](https://www.spheron.network/blog/vllm-vs-tensorrt-llm-vs-sglang-benchmarks/)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `--mem-fraction-static` | `[0.7, 0.92]` | total GPU mem budget | OOM, KV thrash |
| `--max-running-requests` | `[8, 256]` | concurrency cap | queue wait |
| `--max-total-tokens` | per model | KV budget | preemption rate |
| `--chunked-prefill-size` | `[1024, 16384]` | TTFT vs TPS | first-token vs streaming TPS |
| RadixAttention prefix-cache enable | on / off | shared prefixes | prefix-hit ratio |
| `--schedule-policy` | `{fcfs, lpm, dfs-weight}` | request mix | tail latency |

### TGI (HuggingFace text-generation-inference)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `--max-concurrent-requests` | `[8, 512]` | KV budget | queue wait |
| `--max-batch-prefill-tokens` | `[1024, 16384]` | TTFT | first-token latency |
| `--max-batch-total-tokens` | per model | KV budget | preemption / OOM |
| `--max-waiting-tokens` | `[5, 50]` | batching window | TTFT vs throughput |

### TensorRT-LLM

TensorRT-LLM leads on per-engine latency once compiled, but the engine itself is a configuration artifact — many "knobs" are baked at build time, not at serve time. Treat **engine-build params** (precision, plugins, max_batch_size, kv_cache_type) as a separate offline sub-campaign before runtime tuning. [Source: Spheron - 2026 Benchmarks](https://www.spheron.network/blog/vllm-vs-tensorrt-llm-vs-sglang-benchmarks/)

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| Engine `max_batch_size` (build) | `[8, 256]` | engine recompile required | throughput ceiling |
| Engine `max_input_len` / `max_output_len` (build) | per model | engine recompile | request rejection rate |
| In-flight batching scheduler `max_num_tokens` | `[1024, 16384]` | runtime | TTFT vs TPS |
| Paged-KV-cache block size | `{16, 32, 64}` | discrete | KV fragmentation |
| KV-cache quantization | `{fp16, fp8, int8}` | accuracy degradation | KV memory footprint |

**Sensitive constraints**:
- TensorRT-LLM compile step is 20–30 min; campaign budget must account for engine rebuild cost. Prefer Grid or Random on small categorical sets; Bayesian only when the same engine artifact is reused across evals.
- Choosing the serving stack itself (vLLM vs SGLang vs TensorRT-LLM vs TGI) is **Oracle's call**, not a Dial knob. Dial owns runtime tuning *inside* the chosen stack. Hand off stack selection to Oracle when ambiguous.

---

## Kernel / OS

| Parameter | Bounds | Constraint | Hot-path indicator |
|-----------|--------|------------|---------------------|
| `net.core.somaxconn` | `[1024, 65535]` | accept queue depth | accept-queue overflow |
| `net.ipv4.tcp_max_syn_backlog` | `[1024, 65535]` | SYN flood resilience | SYN drops |
| `net.ipv4.ip_local_port_range` | `"1024 65535"` | ephemeral port count | port exhaustion |
| `net.ipv4.tcp_tw_reuse` | `0` or `1` | TIME_WAIT reuse | TIME_WAIT > 30k |
| `fs.file-max` (system) / `ulimit -n` (proc) | `[65536, 1048576]` | fd budget | EMFILE errors |
| `vm.swappiness` | `[0, 10]` for low-latency | OOM risk if 0 | swap-in during load |
| `vm.overcommit_memory` | `{0, 1, 2}` | discrete | OOM-killer behavior |

**Sensitive constraints**:
- Kernel parameters often have large, discrete effects — Grid is preferred over Bayesian.
- Coordinate with platform/SRE — kernel tuning typically requires node-level deployment.

---

## Parameter Space Specification Schema

Codified for the campaign artifact (see `optimization-algorithms.md`).

```yaml
parameter_space:
  - name: "jvm.heap.max_mb"
    type: integer
    bounds: [1024, 12288]
    step: 256
    prior: 4096           # current value
    log_scale: false
    constraint: "<= container_mem_mb * 0.75"

  - name: "jvm.gc.algorithm"
    type: categorical
    choices: ["G1", "ZGC", "Shenandoah"]
    prior: "G1"

  - name: "jvm.gc.max_pause_ms"
    type: integer
    bounds: [50, 500]
    step: 25
    prior: 200
    only_if: "jvm.gc.algorithm == G1"

  - name: "hikari.max_pool"
    type: integer
    bounds: [10, 50]
    prior: 20
    constraint: "sum_across_replicas <= db_max_connections * 0.8"
```

---

## Co-Tuning Decomposition Rules

When more than 5 parameters look relevant, decompose:

1. **Rank by hot-path share** (CPU / lock / alloc / wait).
2. **Group strongly interacting parameters** as sub-campaigns:
   - JVM: `(GC algorithm) → (heap size) → (pause target) → (parallel/conc threads)` — sequential, in this order.
   - Connection pool: `(pool size) → (timeouts)` — sequential.
   - Caffeine: `(maximumSize) → (TTL)` — sequential.
   - LLM serving: `(gpu-memory-util) → (max-num-seqs) → (max-num-batched-tokens)` — sequential.
3. **Fix the prior parameter** before tuning the next.
4. **Re-baseline noise floor** after each sub-campaign — earlier wins can shift σ.
5. **Re-confirm objective stability**: if the objective surface looks non-stationary across sub-campaigns, you are chasing workload drift — go back to SCAN.

The decomposition reduces a 7-parameter search (intractable, attribution-poor) into three 2-parameter sub-campaigns (tractable, attributable, individually revertable).
