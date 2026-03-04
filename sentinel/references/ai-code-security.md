# AI-Generated Code Security & Modern SAST

> AI 生成コードの脆弱性パターン、セキュリティアンチパターン、SAST ツールランドスケープ、Agentic SAST

## 1. AI 生成コードのセキュリティ現状（2025-2026）

### 統計データ

| 指標 | 値 | 出典 |
|------|-----|------|
| AI コードの脆弱性含有率 | 45-62% | Veracode / CSA |
| XSS 失敗率 | 86% | sec-context |
| Java AI コードの脆弱性率 | 72% | sec-context |
| AI コード vs 人間コードの XSS 率 | 2.74x | sec-context |
| 本番にデプロイされた脆弱な AI コード | 81% の組織 | sec-context |
| AI コード起因のブリーチ | 5件に1件 | Veracode |
| 高リスク脆弱性の増加 | 8.3% → 11.3% | Veracode |
| 本番コードにおける AI 生成比率 | 24%（米国 29%） | Veracode |

### AI がセキュアコードを書けない理由

```
1. リスクモデルの欠如: アプリケーション固有の脅威を理解しない
2. コンテキスト不足: 内部標準、セキュリティポリシーを知らない
3. トレーニングデータの汚染: 脆弱なコードで学習している
4. 構造的盲点: 論理的欠陥、認証フロー、権限モデルの不備
5. モデル改善 ≠ セキュリティ改善: 構文的正確性とセキュリティは無相関
```

---

## 2. AI コードセキュリティ・アンチパターン Top 10

| Rank | パターン | スコア | 検出方法 |
|------|---------|--------|---------|
| 1 | **Slopsquatting**（存在しないパッケージ推奨） | 24 | パッケージ名レジストリ照合 |
| 2 | **XSS 脆弱性** | 23 | 出力エスケープ漏れの検出 |
| 3 | **ハードコードシークレット** | 23 | 正規表現パターンマッチ |
| 4 | **SQL インジェクション** | 22 | パラメタライズドクエリ未使用の検出 |
| 5 | **認証の失敗** | 22 | 認証フローの不備検出 |
| 6 | **入力バリデーション欠如** | 21 | バウンダリバリデーション未実装 |
| 7 | **コマンドインジェクション** | 21 | シェルコマンド実行のサニタイズ検証 |
| 8 | **レート制限の欠如** | 20 | API エンドポイントの制限確認 |
| 9 | **過剰なデータ露出** | 20 | API レスポンスのフィールド制限 |
| 10 | **無制限ファイルアップロード** | 20 | ファイルタイプ/サイズ検証 |

### 言語別脆弱性傾向

```
Java:   最高失敗率（72%）、特にXSS（86%）、ログインジェクション（88%）
Python: シェルコマンドインジェクション、pickle デシリアライゼーション
JS/TS:  XSS、prototype pollution、eval() 使用
Go:     エラーハンドリング不備、レースコンディション
```

---

## 3. AI 生成コードのセキュリティレビュー

### 必須チェックリスト

```markdown
## AI-Generated Code Security Review

### Critical（即座に修正）
- [ ] ハードコードされた秘密情報がないか?
- [ ] SQL/NoSQL クエリがパラメタライズされているか?
- [ ] ユーザー入力が出力時にエスケープされているか?
- [ ] コマンド実行にユーザー入力が直接使われていないか?
- [ ] 認証/認可チェックが適切に実装されているか?

### High（24時間以内）
- [ ] 入力バリデーションがバウンダリで実施されているか?
- [ ] エラーメッセージに機密情報が含まれていないか?
- [ ] ファイルアップロードにタイプ/サイズ制限があるか?
- [ ] API レスポンスが必要最小限のフィールドか?
- [ ] レート制限が設定されているか?

### Medium（1週間以内）
- [ ] 推奨パッケージが実在し、メンテされているか?
- [ ] ライセンスが互換性あるか?
- [ ] 非推奨 API/メソッドを使用していないか?
- [ ] ログに機密データが含まれていないか?
```

### Sentinel スキャン拡張ポイント

```
AI 生成コード固有のスキャン:
  1. 存在しないパッケージ名の検出（Slopsquatting）
  2. 一般的だが安全でないパターンの検出
     - eval(), exec(), Function() の使用
     - innerHTML / dangerouslySetInnerHTML
     - 文字列連結による SQL クエリ
  3. 認証フローの完全性チェック
  4. エラーハンドリングの一貫性検証
```

---

## 4. Modern SAST ツールランドスケープ（2026）

### トップ 10 SAST ツール

| ツール | 特徴 | AI 対応 |
|--------|------|---------|
| **Semgrep** | ルールベース、30+ 言語、高速 | AI フィルタリング |
| **CodeQL** | GitHub ネイティブ、セマンティッククエリ | カスタムクエリ |
| **Snyk Code** | リアルタイム IDE スキャン | AI 自動修正 |
| **Veracode** | エンタープライズ、ポートフォリオ管理 | AI コードレポート |
| **Checkmarx** | プラットフォーム統合 | AI 支援修復 |
| **SonarQube** | 品質ゲート、テイント分析 | 品質 + セキュリティ |
| **DryRun Security** | PR ネイティブ、自然言語ポリシー | MCP 統合 |
| **Endor Labs** | ノイズ削減、ポリシー駆動 | リーチャビリティ |
| **Aikido** | 開発者フレンドリー | 自動トリアージ |
| **Mend SAST** | AI エディタ統合 | MCP サーバー |

### LinkedIn の SAST パイプライン事例

```
LinkedIn アーキテクチャ:
  GitHub Actions → CodeQL + Semgrep（並列スキャン）
    → SARIF 標準で結果正規化
      → メタデータ付きの修復ガイダンス生成

ポイント:
  - 2つのエンジンの補完的カバレッジ
  - SARIF による統一的な結果フォーマット
  - 開発者への actionable なフィードバック
```

### Agentic SAST（2026 フロンティア）

```
Agentic SAST = AI コードエディタへの直接統合

フロー:
  1. AI ツール（Claude Code, Cursor 等）でコード生成/リファクタリング
  2. PR 作成時に自動セキュリティレビュー発火
  3. PR コメントで修復ガイダンス提供
  4. 開発者 or AI エージェントがフィードバック反映

MCP 統合:
  - DryRun Security: Code Insights MCP（自然言語セキュリティクエリ）
  - Mend SAST: Cursor/Claude Code/Copilot に直接統合
  - Semgrep: IDE プラグイン + CI/CD 統合
```

---

## 5. IDE セキュリティ脆弱性（IDEsaster）

```
2025年に 30+ の IDE セキュリティ脆弱性が公開:
  - プロンプトインジェクション + 正規機能の組み合わせ
  - データ流出（コードベースの外部送信）
  - リモートコード実行（RCE）

対策:
  - IDE 拡張機能の最小化
  - AI エージェントのサンドボックス化
  - コード実行前の人間レビュー
  - IDE セキュリティアップデートの即時適用
```

---

## 6. コードポリシー強制

### ポリシー定義のベストプラクティス

```
効果的なコードポリシー:
  1. 自然言語で定義（正規表現のみに頼らない）
  2. PR ステージで自動強制（マージ前）
  3. 修復例を開発者フィードバックに含める
  4. クロスファイルロジック検出（認可、IDOR）
  5. リポジトリ横断の集中管理と可視化
```

**Source:** [Veracode: AI-Generated Code Security Risks](https://www.veracode.com/blog/ai-generated-code-security-risks/) · [CSA: Security Risks in AI-Generated Code](https://cloudsecurityalliance.org/blog/2025/07/09/understanding-security-risks-in-ai-generated-code) · [Arcanum-Sec: sec-context Anti-Patterns](https://github.com/Arcanum-Sec/sec-context) · [DryRun Security: Top AI SAST Tools 2026](https://www.dryrun.security/blog/top-ai-sast-tools-2026) · [InfoQ: LinkedIn CodeQL + Semgrep](https://www.infoq.com/news/2026/02/linkedin-redesigns-sast-pipeline/) · [The Hacker News: IDE Security Flaws](https://thehackernews.com/2025/12/researchers-uncover-30-flaws-in-ai.html)
