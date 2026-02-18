# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

#### New Agents
- **Helm** - 財務・市場・競合データから短期/中期/長期の経営シミュレーションを実施する経営戦略特化エージェント（SWOT/PESTLE/Porter分析、シナリオプランニング）
- **Pipe** - GHAワークフロー専門エージェント（トリガー戦略、セキュリティ強化、PR自動化、Reusable Workflow設計）
- **Aether** - AITuber（AI VTuber）システムの企画から実装・運用までを一貫支援するフルスタック・オーケストレーター
- **Oracle** - AI/ML設計・評価専門エージェント（プロンプトエンジニアリング、RAG設計、LLMアプリパターン）
- **Beacon** - 可観測性・信頼性エンジニアリング専門エージェント（SLO/SLI設計、分散トレーシング）
- **Siege** - 負荷テスト・カオスエンジニアリング・レジリエンス検証専門エージェント
- **Prose** - ユーザー向けテキスト専門エージェント（マイクロコピー、エラーメッセージ、ボイス＆トーン設計）
- **Latch** - Claude Codeフック管理エージェント（PreToolUse/PostToolUse等のイベントシステム）
- **Relay** - メッセージング統合・Bot開発・リアルタイム通信の設計＋実装エージェント
- **Void** - 引き算設計エージェント。YAGNI検証、スコープカット、複雑性削減提案
- **Totem** - プロジェクトDNAプロファイラー。8次元の文化分析、逸脱検出、オンボーディングガイド

### Enhanced
- **Nexus** - 19種類のルーティングコマンドと42種類のチェーンテンプレートを追加（フルエコシステムカバレッジ）
- **Orbit** - Gemini TTSによるイテレーション通知（Pattern D）とスクリプト生成機能を追加
- **Sigil** - `.agents/skills/` サポート追加でポータブルなスキル配置が可能に
- **Bard** - エンジン・エゴアーキテクチャに刷新（Codex/Gemini/Claude各エンジンが固有の声で語る）
- **Cast** - SPEAKモード追加、Google Cloud TTSを第三のエンジンとして統合
- **Titan** - 統合プロトコル・自律検証・実行ブートストラップを追加し信頼性向上
- **Scaffold** - Terraformオペレーション、コンプライアンス、FinOps参照ドキュメントを追加
- **Hearth** - SKILL.mdと参照ドキュメントを拡充
- **Voyager, Navigator, Sketch** - 各SKILL.mdを包括的に改善（グレードA相当）

### Changed
- 全エージェントのSKILL.mdを最適化（コンテキスト削減、28〜81%圧縮）
- エコシステムへのPipe/Relay/Aether/Oracle/Beacon/Siege/Prose統合（Nexus, Architect, Gearのルーティング更新）

## [1.0.0] - 2025-01-15

### Added

#### New Agents
- **Artisan** - フロントエンド本番実装の職人（React/Vue/Svelte、Hooks、状態管理）
- **Showcase** - Storybookストーリー作成・カタログ管理・Visual Regression連携
- **Vision** - クリエイティブディレクション・Design System構築
- **Probe** - セキュリティ動的テスト（DAST）・ペネトレーションテスト
- **Tuner** - DBパフォーマンス最適化・EXPLAIN ANALYZE分析
- **Researcher** - ユーザーリサーチ設計・インタビューガイド作成
- **Voyager** - E2Eテスト専門（Playwright/Cypress）
- **Judge** - codex reviewによるコードレビュー・PRレビュー自動化・AI幻覚検出
- **Anvil** - Terminal UI構築・CLI開発支援

#### Features
- **AUTORUN_FULL mode** - ガードレール付き完全自動実行モード
- 40種類の専門エージェント体制
- 全エージェントの使用例を完備
- タスクタイプ別チェーンテンプレート（11カテゴリ、41テンプレート）

### Enhanced
- **Vision** - 2025-2026デザイントレンド、AI設計ツール統合（Figma AI、v0、Claude）
- **Artisan** - Vue 3 Composition API、Svelte 5 Runes、スタイリング戦略ガイド
- **Showcase** - Storybook 8対応、MDX 3ドキュメント、Figma連携
- **Builder** - TDD、Event Sourcing、CQRS、Forgeからの自動引き継ぎ

### Changed
- AUTORUN_FULLをデフォルトモードに設定
- プラットフォーム非依存に対応（Claude Code、Codex CLI、Gemini CLI等）
- エージェント境界定義の明確化（Bolt vs Tuner、Schema vs Tuner等）

### Removed
- **Roadmap** - PM向け機能のため削除
- **Insight** - Spark/Scoutに統合
- **Lens** - Canvas/Showcaseに統合
- **Fixture** - Builder/Radarに統合

## [0.9.0] - 2025-01-08

### Added
- Initial release with 35 agents
- Nexus orchestrator with AUTORUN/GUIDED modes
- Basic agent collaboration framework
- Hub & Spoke architecture

---

## Agent Categories

| Category | Count | Agents |
|----------|-------|--------|
| Orchestration | 2 | Nexus, Sherpa |
| Research & Planning | 5 | Scout, Spark, Compete, Voice, Researcher |
| Quality Assurance | 6 | Radar, Voyager, Sentinel, Probe, Judge, Zen |
| Implementation | 3 | Builder, Artisan, Forge |
| Performance | 2 | Bolt, Tuner |
| UI/UX | 6 | Vision, Palette, Muse, Flow, Echo, Showcase |
| Documentation | 1 | Quill |
| Visualization | 1 | Canvas |
| Architecture | 3 | Atlas, Horizon, Gateway |
| Data | 1 | Schema |
| DevOps | 3 | Anvil, Gear, Scaffold |
| i18n | 1 | Polyglot |
| Growth | 2 | Growth, Retain |
| Analytics | 2 | Pulse, Experiment |
| Operations | 1 | Triage |
| **Total** | **40** | |
