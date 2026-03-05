# Verification & Validation Frameworks

> V&V プロセスのベストプラクティス、4 つの検証手法、リスクベースアプローチ、AI 活用

## 1. V&V の基本フレームワーク

### Verification vs Validation

| 観点 | Verification（検証） | Validation（妥当性確認） |
|------|--------------------|-----------------------|
| 問い | "正しく作っているか？" | "正しいものを作っているか？" |
| 対象 | 仕様への適合性 | ユーザーニーズへの適合性 |
| タイミング | 開発中（各フェーズ終了時） | 開発後（受入テスト時） |
| 実行者 | 開発チーム | ステークホルダー |

```
Attest の位置づけ:
  - 主に Verification（仕様適合検証）を担当
  - Validation は Warden（V.A.I.R.E.）/ Echo（ペルソナ検証）に委譲
  - ただし EXTRACT モードでは仕様品質の Validation も実施
```

---

## 2. 4 つの検証手法（TDIA）

### 概要

| 手法 | 説明 | Attest での適用 |
|------|------|---------------|
| **Test** | 実行して結果を確認 | NOT_TESTED → Radar/Voyager に委譲 |
| **Demonstration** | プロトタイプ/デモで確認 | Echo/Forge 連携で視覚的確認 |
| **Inspection** | 専門家レビューで確認 | Attest の主要手法（静的検証） |
| **Analysis** | 数学的/論理的分析で確認 | ロジックトレース、状態遷移分析 |

### 手法選択マトリクス

| 基準タイプ | 推奨手法 | 理由 |
|-----------|---------|------|
| 機能要件（入力→出力） | Test + Inspection | 実行結果 + コード確認 |
| パフォーマンス要件 | Test | 実測が必要 |
| セキュリティ要件 | Inspection + Analysis | コードパターン + 脅威分析 |
| ユーザビリティ要件 | Demonstration | 主観的評価が必要 |
| データ整合性要件 | Analysis + Test | 論理検証 + 実行確認 |
| API 契約 | Inspection + Test | スキーマ検証 + 統合テスト |
| 状態遷移要件 | Analysis | 状態機械の網羅性検証 |
| 設定/構成要件 | Inspection | 設定値の確認 |

### Attest の検証手法マッピング

```
verification-methods.md の 5 手法との対応:

  Code Search    → Inspection（コード存在確認）
  Logic Trace    → Analysis（データフロー追跡）
  State Check    → Analysis（状態遷移検証）
  Error Path     → Inspection + Analysis（エラー処理確認）
  Absence Check  → Inspection（実装不在の検出）
```

---

## 3. リスクベース検証

### リスク分類

| リスクレベル | 基準 | 検証深度 |
|------------|------|---------|
| **CRITICAL** | データ損失、セキュリティ侵害、システム障害 | 全手法適用 + 敵対的プローブ必須 |
| **HIGH** | ユーザー向け機能の障害、主要ワークフローの破壊 | Inspection + Analysis + 敵対的プローブ |
| **MEDIUM** | エッジケースでの予期しない動作 | Inspection + 基本プローブ |
| **LOW** | マイナーな動作差異 | Inspection のみ |

### リソース配分ガイドライン

```
検証時間の配分（推奨）:
  CRITICAL 基準: 40% の検証リソース
  HIGH 基準:     30%
  MEDIUM 基準:   20%
  LOW 基準:      10%

スコープ制限時の優先順位:
  1. 全 CRITICAL 基準の完全検証
  2. 全 HIGH 基準の Inspection
  3. MEDIUM 基準のサンプリング検証
  4. LOW 基準は AUDIT モードでのみ
```

---

## 4. 仕様品質の 6 原則

### Validation Quality Principles

| 原則 | 説明 | Attest での実践 |
|------|------|---------------|
| **正しいステークホルダーの参加** | 検証に適切な専門家を含める | Three Amigos 推奨、AMBIGUOUS_FLAG で議論を促進 |
| **エラー識別と修正の分離** | 発見と修正を別工程で行う | Attest = 発見、Builder = 修正 |
| **多角的視点での検証** | 異なる角度から要件を検証 | 6 カテゴリ敵対的プローブ |
| **適切なドキュメント変更** | 検証結果に基づく仕様更新 | Scribe ハンドオフで仕様改善 |
| **開発成果物の構築** | 検証プロセスで有用な成果物を生成 | BDD シナリオ、トレーサビリティマトリクス |
| **検証の反復実施** | 一度ではなく繰り返し検証 | AUDIT モードの定期実行 |

---

## 5. AI 活用の検証

### LLM によるソフトウェア検証（2025年の動向）

| 活用領域 | 手法 | 成熟度 |
|---------|------|--------|
| **要件品質チェック** | LLM で曖昧性・矛盾を自動検出 | 中-高 |
| **テストケース生成** | 仕様から BDD シナリオを自動生成 | 高 |
| **コード-仕様照合** | LLM がコードの意図と仕様を比較 | 中 |
| **形式検証補助** | 自然言語→形式仕様への変換 | 低-中 |
| **説明生成** | 違反理由の自然言語説明 | 高 |

### Attest での AI 活用方針

```
信頼できる活用:
  ✅ 仕様テキストの曖昧性検出（パターンマッチ + AI 推論）
  ✅ BDD シナリオの生成（テンプレート + AI 拡張）
  ✅ 違反理由の説明文生成
  ✅ テスタビリティの評価

慎重な活用（人間レビュー必須）:
  ⚠️ コード-仕様の適合判定
  ⚠️ 暗黙の前提の推論
  ⚠️ 矛盾検出

避けるべき活用:
  ❌ AI 単独での CERTIFIED 判定
  ❌ ハルシネーションリスクのある推論での FAIL 判定
  ❌ 形式検証の代替としての使用
```

### LLM-AQuA-DiVeR フレームワーク（ICSE 2025）

```
2 つの LLM ロール:
  1. Explanation Assistant:
     - ステークホルダーが検証結果を理解できるよう支援
     - 技術的な違反を平易な言語で説明

  2. Refinement Assistant:
     - ステークホルダーのフィードバックを仕様に反映
     - 検証基準の改善提案

Attest への示唆:
  - レポートの「検出事項」セクションを平易な説明で補強
  - AMBIGUOUS_FLAG の suggested_clarification を AI で高品質化
  - ステークホルダー向けサマリーの自動生成
```

---

## 6. 検証プロセスのアンチパターン

| アンチパターン | 症状 | 対策 |
|--------------|------|------|
| **Big Bang Verification** | リリース直前に全検証を一括実施 | 段階的検証（EXTRACT → FULL → AUDIT） |
| **Checklist Verification** | 形式的なチェックリスト消化のみ | 敵対的プローブで深い検証 |
| **Single-Method Reliance** | Inspection のみで Test なし | TDIA の複数手法を組み合わせ |
| **Spec-Blind Development** | 仕様を読まずに実装→後付け検証 | Pre-Implementation Extraction チェーン |
| **Verdict Shopping** | 望む判定が出るまで再検証 | 判定基準の機械的適用（Verdict Rules） |
| **Gold Plating Tolerance** | 仕様外の機能追加を許容 | Backward トレースで仕様外実装を検出 |

---

## 7. 早期検出の経済的効果

```
IBM Systems Sciences Institute の調査:

  要件フェーズでの欠陥修正: $100
  設計フェーズ:              $500
  コーディングフェーズ:       $1,000
  テストフェーズ:             $2,000
  本番フェーズ:              $10,000+

→ Attest の EXTRACT モード（要件フェーズ）での品質チェックは
  本番障害と比較して 100 倍のコスト効率

要件起因の欠陥が全ソフトウェア欠陥の約 50%:
  → 仕様品質の改善は最もレバレッジの高い品質投資
```

**Source:** [Visure Solutions: Requirements V&V](https://visuresolutions.com/alm-guide/requirements-verification-and-validation/) · [ArgonDigital: Verification Best Practices](https://argondigital.com/blog/product-management/verification-and-validation/) · [ICSE 2025: LLM-AQuA-DiVeR](https://conf.researchr.org/details/icse-2025/raie-2025-papers/6/LLM-AQuA-DiVeR-LLM-Assisted-Quality-Assurance-Through-Dialogues-on-Verifiable-Specif) · [Martin Kleppmann: AI + Formal Verification](https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html) · [ACL 2025: Enhancing Software RE with LLMs](https://aclanthology.org/2025.acl-srw.31.pdf)
