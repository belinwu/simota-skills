# AI-Powered Reverse Engineering

> LLM によるコード→図の自動生成、Claude Code パターン、静的解析ツール、限界と対策

## 1. LLM ベースの図生成 (2025 主流)

### アプローチ

コードファイル取得 → LLM にプロンプト → Mermaid/PlantUML/draw.io 形式で出力。

### 主要ツール

| ツール | 特徴 |
|--------|------|
| **Swark** | VS Code 拡張、GitHub Copilot 連携、言語非依存でアーキテクチャ図自動生成 |
| **GenAI-DrawIO-Creator** | draw.io XML を LLM で生成するフレームワーク |
| **Claude Code** | O'Reilly 発表のリバースエンジニアリングパターン |

---

## 2. Claude Code パターン (O'Reilly)

水平スイムレーンフローチャート (`flowchart LR`) を使用した実践パターン:

### 原則

1. 各システムを個別のコンテナとして表現
2. ステップタイプを限定:
   - HTTP エンドポイント
   - ドメインメソッド
   - DB 操作
   - イベント
   - ワークフロー
3. 反復的にルールを蓄積し、要件ドキュメントを成長させる

### プロンプト設計

```
1. コンテキスト提供: ドメイン概念、リポジトリ関係、OpenAPI 仕様
2. 出力形式指定: Mermaid flowchart LR
3. 制約指定: 最大コンポーネント数、抽象度レベル
4. 反復改善: 初回生成 → レビュー → 修正プロンプト
```

---

## 3. デュアルモデルパイプライン

学術的に提案されたパターン:

```
軽量 LLM → 技術仕様生成
  ↓
高性能推論モデル → PlantUML コード変換
  ↓
マルチモーダルバリデーション → 仕様と図の整合性スコアリング
```

3つのビジョン-言語モデルで検証。

---

## 4. 静的解析ツール

| ツール | 対応言語 | 特徴 |
|--------|---------|------|
| pyan | Python | 関数間の呼び出し依存グラフ生成 |
| PyCG | Python | 数千行を1秒未満で処理 |
| code2flow | Python, JS | Graphviz 利用のコールグラフ |
| callGraph | 20+ 言語 | AWK, Bash, Go, JS, Kotlin, Rust 等 |
| PhpDependencyAnalysis | PHP | 名前空間ベースの依存関係グラフ |

---

## 5. ベストプラクティス

### コンテキスト基盤の構築

LLM に渡す前に以下を準備:

| コンテキスト | 用途 |
|-------------|------|
| ドメイン概念辞書 | ビジネス用語の一貫性 |
| リポジトリ関係マップ | モノレポ内のサービス境界 |
| OpenAPI 仕様 | API エンドポイントの正確な把握 |
| DB スキーマ | データモデルの全体像 |

### 出力形式の標準化

**Mermaid が推奨**: Git 連携、GitHub ネイティブレンダリング、LLM の学習データに豊富。

### 定期的な再生成

- **四半期ごとに再生成**
- 専用の検証エージェントで正確性を担保
- コード変更イベントをトリガーに自動更新検討

---

## 6. 限界と対策

| 限界 | 対策 |
|------|------|
| **20 コンポーネント超で精度低下** | システムを分割して個別に生成 |
| **空間関係の誤認識** | レイアウト調整は手動で補正 |
| **ランタイム動作の欠落** | 静的解析 + 動的プロファイリングで補完 |
| **ドメイン知識の不足** | 初期コンテキストでドメイン辞書を提供 |
| **幻覚 (存在しない接続の生成)** | コードベースとのクロスチェック |

### リスク軽減策

- 図のエラーはレンダリング時に即座に発見される (本番コードより低リスク)
- 内容エラーは視覚的検査で明白
- 生成速度は手動の **4-5 倍** → 初期ドラフトに有効
- 最終確認は人間が行う

---

## 7. Canvas エージェントでの活用

### 既存 reverse-engineering.md との棲み分け

| 既存パターン | AI 拡張パターン |
|-------------|----------------|
| 静的 AST/コード解析 | LLM + 静的解析のハイブリッド |
| パターン固定 (8種類) | 自然言語で柔軟に指定 |
| React/Next.js 中心 | 言語非依存 |

### 推奨ワークフロー

```
1. 静的解析でコード構造を抽出
2. LLM にコンテキスト + コード構造を提供
3. Mermaid 図を生成
4. レンダリングで構文検証
5. 人間レビューで内容検証
6. diagram-library に保存
```

**Source:** [O'Reilly - Reverse Engineering with Claude Code](https://www.oreilly.com/radar/reverse-engineering-your-software-architecture-with-claude-code-to-help-claude-code/) · [Swark GitHub](https://github.com/swark-io/swark) · [GenAI-DrawIO-Creator (arXiv)](https://arxiv.org/html/2601.05162v1) · [Software Diagrams with ChatGPT/Claude (The New Stack)](https://thenewstack.io/how-to-create-software-diagrams-with-chatgpt-and-claude/)
