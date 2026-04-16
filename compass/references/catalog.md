# Skill Agent Catalog

**Purpose:** Complete catalog of all skill agents with descriptions and triggers.
**Read when:** You need to look up agents by category, find agents for a specific task, or provide a full listing.

---

## How to Use This Catalog

- カテゴリ別にエージェントを探す場合はカテゴリセクションを参照
- タスクからエージェントを探す場合は `references/patterns.md` を参照
- 最新の正確なエージェント数やカテゴリは、リポジトリのディレクトリ構造から確認すること

---

## Orchestration (5)

タスクの分解・調整・並列実行を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Nexus** | チームオーケストレータ | 複数エージェント連携が必要な複雑タスク | No |
| **Sherpa** | タスク分解ガイド | 15分以内のアトミックステップに分解 | No |
| **Titan** | プロダクトデリバリー | 最速でコード納品、計画より実装優先 | No |
| **Rally** | 並列オーケストレータ | 複数セッション並列実行 | No |
| **Aether** | AITuberオーケストレータ | AI VTuberシステム構築 | No |

## Investigation (9)

調査・分析・根本原因特定を担当。コードは書かない。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Scout** | バグ調査・RCA | バグの原因調査、再現手順作成 | No |
| **Lens** | コード理解 | コード構造マッピング、機能発見、データフロー追跡 | No |
| **Rewind** | Git履歴調査 | リグレッション分析、コミット考古学 | No |
| **Fossil** | レガシーコード解析 | 暗黙のビジネスルール抽出、移行リスク評価 | No |
| **Ripple** | 影響範囲分析 | 変更前のリスク評価、blast radius 算出 | No |
| **Specter** | 並行性問題検出 | Race condition、メモリリーク、デッドロック | No |
| **Sweep** | 不要コード検出 | 未使用ファイル・デッドコード・孤立ファイル特定 | No |
| **Spark** | 新機能提案 | 既存データ/ロジックを活かした機能アイデア | No |
| **Void** | YAGNI検証 | スコープカット、複雑性削減提案 | No |

## Implementation (6)

コード実装を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Builder** | ビジネスロジック実装 | 堅牢なAPI統合、データモデル | Yes |
| **Artisan** | フロントエンド実装 | React/Vue/Svelte本格実装 | Yes |
| **Forge** | プロトタイプ | フロント/バック両方の高速プロトタイプ | Yes |
| **Anvil** | CLI/TUI構築 | ターミナルUI、CLIツール | Yes |
| **Native** | モバイル開発 | React Native/Flutter/SwiftUI/Compose | Yes |
| **Pixel** | モックアップ→コード | 画像からピクセル精度のHTML/CSS生成 | Yes |

## Testing (3)

テスト作成・検証を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Radar** | ユニットテスト | エッジケース追加、flakyテスト修正、カバレッジ向上 | Yes |
| **Voyager** | E2Eテスト | Playwright/Cypress設定、Page Object設計 | Yes |
| **Siege** | 負荷・耐障害テスト | 負荷テスト、契約テスト、カオスエンジニアリング | Yes |

## Security (4)

セキュリティ分析・テストを担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Sentinel** | 静的セキュリティ分析 | ハードコード秘密検出、SQLi防止、依存脆弱性 | Mixed |
| **Breach** | レッドチーム | 攻撃シナリオ設計、MITRE ATT&CK | No |
| **Probe** | 動的セキュリティテスト | OWASP ZAP/Burp Suite、ペネトレーションテスト | Mixed |
| **Crypt** | 暗号アーキテクチャ | アルゴリズム選定、鍵管理、E2EE、TLS設定 | Mixed |

## Review (7)

コードレビュー・品質チェックを担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Judge** | 自動コードレビュー | PRレビュー自動化、バグ検出 | Mixed |
| **Zen** | リファクタリング | 変数名改善、関数抽出、デッドコード除去 | Mixed |
| **Canon** | 規格準拠チェック | OWASP/WCAG/OpenAPI準拠評価 | No |
| **Gauge** | SKILL.md監査 | 16項目チェックリスト準拠確認 | No |
| **Attest** | 仕様準拠検証 | 受入基準抽出、BDDシナリオ生成 | No |
| **Warden** | UX品質ゲート | V.A.I.R.E.評価、スコアカード | No |
| **Cloak** | プライバシーエンジニアリング | PII検出、GDPR/CCPA準拠 | Mixed |

## Performance (2)

パフォーマンス最適化を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Bolt** | フロント/バック最適化 | 再レンダリング削減、N+1修正、キャッシュ | Yes |
| **Tuner** | DB最適化 | EXPLAIN ANALYZE、インデックス推奨、スロークエリ | Yes |

## Documentation (4)

ドキュメント作成を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Scribe** | 技術仕様書 | PRD/SRS/HLD/LLD作成 | No |
| **Quill** | コードドキュメント | JSDoc追加、README更新、any型修正 | Mixed |
| **Prose** | UXライティング | マイクロコピー、エラーメッセージ、トーン設計 | No |
| **Tome** | 学習教材 | diff→教材変換、設計判断記録 | No |

## Architecture (7)

システム設計・構造を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Atlas** | アーキテクチャ分析 | 依存関係分析、ADR/RFC作成 | Mixed |
| **Schema** | DB設計 | 正規化、インデックス戦略、ER図 | Mixed |
| **Gateway** | API設計 | OpenAPI生成、バージョニング | Mixed |
| **Stratum** | C4モデル | Structurizr DSL生成 | Mixed |
| **Grove** | リポジトリ構造 | ディレクトリ設計、docs/レイアウト | Mixed |
| **Nest** | LLM最適化フォルダ構造 | エージェント向けディレクトリ最適化 | Mixed |
| **Shard** | マルチテナント設計 | テナント分離、RLS、スケール設計 | Mixed |

## UX/Design (10)

UI/UX設計・改善を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Vision** | クリエイティブディレクション | UI/UXの方向性決定 | No |
| **Palette** | ユーザビリティ改善 | 認知負荷削減、a11y準拠 | Mixed |
| **Echo** | ペルソナ認知ウォークスルー | ユーザビリティ評価、混乱点発見 | No |
| **Flow** | アニメーション実装 | CSS/JSアニメーション、トランジション | Yes |
| **Muse** | デザイントークン | トークンアーキテクチャ、ダークモード | Mixed |
| **Showcase** | Storybook | ストーリー作成、Visual Regression | Mixed |
| **Researcher** | ユーザーリサーチ | インタビュー設計、ペルソナ作成 | No |
| **Trace** | セッションリプレイ分析 | 行動パターン抽出、UX問題発見 | No |
| **Cast** | ペルソナキャスティング | ペルソナ生成・管理・同期 | No |
| **Funnel** | LP構築 | ランディングページ設計・最適化 | Mixed |

## DevOps (7)

インフラ・CI/CD・運用を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Gear** | 依存管理・CI/CD | ビルドエラー、dev環境問題 | Yes |
| **Scaffold** | インフラ構築 | Terraform/Docker Compose設計 | Yes |
| **Pipe** | GitHub Actions | ワークフロー設計、セキュリティ強化 | Yes |
| **Beacon** | 監視・信頼性 | SLO/SLI設計、アラート戦略 | Mixed |
| **Launch** | リリース管理 | バージョニング、CHANGELOG、ロールバック | Mixed |
| **Comply** | コンプライアンス | SOC2/PCI-DSS/HIPAA準拠チェック | Mixed |
| **Ledger** | FinOps | クラウドコスト最適化、RI/SP推奨 | No |

## Modernization (2)

移行・近代化を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Shift** | 移行オーケストレータ | フレームワーク/ライブラリ/DB移行 | Mixed |
| **Horizon** | 技術更新 | 非推奨ライブラリ検出、ネイティブAPI置換 | Mixed |

## Growth (2)

成長施策を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Growth** | SEO/CRO/GEO | メタ/OGP/JSON-LD、CTA最適化 | Mixed |
| **Retain** | リテンション | 再エンゲージメント、チャーン防止 | Mixed |

## Analytics (3)

指標・実験・組み合わせ分析を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Pulse** | KPI設計 | North Star Metric、ファネル分析 | Mixed |
| **Experiment** | A/Bテスト設計 | 仮説文書化、サンプルサイズ計算 | Mixed |
| **Matrix** | 組み合わせ分析 | 組み合わせ爆発制御、最小カバレッジ | No |

## Git/PR (2)

バージョン管理ワークフローを担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Guardian** | PR管理 | 変更分類、粒度推奨、戦略提案 | No |
| **Harvest** | PR収集・レポート | 週次/月次レポート、リリースノート | No |

## Browser (2)

ブラウザ操作を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Navigator** | ブラウザ自動化 | Playwright/DevToolsでタスク完了 | Yes |
| **Spider** | クロール設計 | 分散クローラー、ポライトネス設計 | No |

## Data (2)

データパイプライン・変換を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Stream** | ETL/ELTパイプライン | Kafka/Airflow/dbt設計 | Mixed |
| **Morph** | ドキュメント変換 | Markdown/Word/Excel/PDF/HTML変換 | Mixed |

## Strategy (4)

ビジネス戦略・意思決定を担当。コードは書かない。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Helm** | ビジネス戦略 | SWOT/PESTLE/Porter分析 | No |
| **Compete** | 競合調査 | 機能マトリクス、ポジショニング | No |
| **Rank** | 優先順位付け | ICE/RICE/WSJF/MoSCoWスコアリング | No |
| **Levy** | 確定申告ガイド | 所得分類、控除最適化、申告手順 | No |

## Incident (2)

インシデント対応を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Triage** | インシデント初動 | 影響特定、復旧手順、ポストモーテム | No |
| **Mend** | 自動修復 | ランブック実行、段階検証、ロールバック | Mixed |

## Communication (2)

連携・コミュニケーションを担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Relay** | メッセージング統合 | ボット開発、Webhook、WebSocket | Mixed |
| **Accord** | 仕様整合 | Business/Dev/Design横断仕様 | No |

## Meta / Tooling (7)

エコシステム自体の管理・進化を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Architect** | スキル設計 | 新エージェント設計、ギャップ分析 | No |
| **Sigil** | プロジェクト固有スキル生成 | コードベース分析→最適スキル生成 | No |
| **Lore** | 知識キュレーション | パターン抽出、知識劣化検出 | No |
| **Darwin** | エコシステム進化 | ライフサイクル検出、適応度評価 | No |
| **Hone** | AI CLI設定最適化 | Claude Code/Gemini CLI設定監査 | No |
| **Realm** | エコシステム可視化 | ゲーミフィケーション、インタラクティブマップ | Yes |
| **Compass** | スキルナビゲーター | スキル案内、オンボーディング | No |

## Creative / Media (6)

メディア・クリエイティブ生成を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Dot** | ピクセルアート | SVG/Canvas/Phaser 3でピクセルアート | Yes |
| **Ink** | SVGアイコン | アイコンシステム、スプライト構築 | Yes |
| **Tone** | ゲーム音声 | SFX/BGM/Voice/Ambient | Yes |
| **Sketch** | AI画像生成 | Gemini APIでテキスト→画像 | Yes |
| **Clay** | AI 3D生成 | テキスト/画像→3Dモデル | Yes |
| **Lyric** | 作詞 | Suno AI向け歌詞・メタタグ作成 | No |

## AI / ML (3)

AI設計・思考支援を担当。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Oracle** | AI/ML設計 | プロンプト工学、RAG設計、評価 | No |
| **Flux** | 思考屈折 | 前提チャレンジ、視点転換 | No |
| **Prism** | NotebookLM最適化 | ステアリングプロンプト設計 | No |

## Other Specialists

上記カテゴリに収まりきらない専門スキル。

| Agent | Role | Trigger | Code |
|-------|------|---------|------|
| **Riff** | ブレインストーミング | 対話的アイデア深掘り | No |
| **Plea** | 合成ユーザー代弁 | 架空ユーザーとして機能要求生成 | No |
| **Polyglot** | i18n/l10n | 多言語対応、RTLサポート | Mixed |
| **Weave** | ワークフロー設計 | 状態遷移、Sagaパターン | Mixed |
| **Omen** | プレモーテム分析 | 失敗シナリオ列挙、RPN評価 | No |
| **Seek** | 検索エンジン設計 | 全文検索、ベクトル検索、RAG | Mixed |
| **Vigil** | 検出エンジニアリング | Sigma/YARAルール設計 | Mixed |
| **Magi** | 多視点審議 | アーキテクチャ仲裁、Go/No-Go | No |
| **Saga** | ナラティブデザイン | 顧客体験ストーリーテリング | No |
| **Cue** | 動画脚本 | プロダクト動画、ストーリーボード | No |
| **Director** | デモ動画制作 | Playwright E2Eからデモ生成 | Mixed |
| **Reel** | ターミナル録画 | CLI デモGIF/動画生成 | Mixed |
| **Stage** | スライド生成 | Marp/reveal.js/Slidev | Mixed |
| **Loom** | Figma Make準備 | Figma Make Guidelines.md生成 | No |
| **Frame** | Figma→コード橋渡し | デザインコンテキスト抽出 | No |
| **Clause** | 法務文書レビュー | 利用規約、プライバシーポリシー | No |
| **Quest** | ゲーム企画 | GDD、バランス設計、経済設計 | No |
| **Orbit** | 自律ループ設計 | nexus-autoloopのスクリプト生成 | Mixed |
| **Arena** | マルチAI比較 | Codex/Gemini CLIの競合/協調実行 | Mixed |
| **Hearth** | dotfile管理 | zsh/tmux/neovim/ghostty設定 | Mixed |
| **Mint** | テストデータ生成 | Factory、境界値、シード管理 | Mixed |
