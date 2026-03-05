# Persona Anti-Patterns

> ペルソナ作成・維持・組織導入における 10 大アンチパターン、Anti-Persona 概念、Persona Fatigue 対策

## 1. ペルソナ 10 大アンチパターン

### 作成フェーズのアンチパターン

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **PA-01** | **Demographics Fixation** | 年齢・性別・居住地で構成、行動データなし | 行動パターン・ゴール・ペインポイント中心に再構成 |
| **PA-02** | **Single Monolithic Persona** | 全ユーザーを 1 つのペルソナで代表 | セグメント分析で 3-7 ペルソナに分割 |
| **PA-03** | **Happy Path Persona** | 理想的ユーザーのみモデル化、離脱者・不満層を無視 | Anti-Persona + 離脱パターンを含める |
| **PA-04** | **Proto-Persona Ossification** | 仮説ベースの Proto-Persona を検証なしに本番運用 | Proto → Research-Based への段階的昇格プロセス |
| **PA-05** | **User-Buyer Conflation** | 購買者と利用者を同一ペルソナに混合（特に B2B） | 購買ペルソナと利用ペルソナを分離 |

### 維持フェーズのアンチパターン

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **PA-06** | **One-Shot Creation** | 作成後に一度も更新しない → 陳腐化 | 月次レビュー + ドリフト検出の自動化 |
| **PA-07** | **Over-Designed Artifact** | 美麗な PDF/ポスターで編集困難 → 更新されない | 編集可能な形式（Markdown/Wiki/Slides）で管理 |
| **PA-08** | **Specificity Imbalance** | 過度に具体的（1% のユーザーのみ代表）or 過度に汎用（誰も代表しない） | 20% ルール: 各ペルソナがユーザーベースの約 20% を代表 |

### 組織導入のアンチパターン

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **PA-09** | **Silo Creation** | UX チームが単独で作成 → 他チームが無関心 | 作成プロセスにステークホルダーを巻き込む |
| **PA-10** | **Gallery Display** | ペルソナを壁に飾るだけで意思決定に使わない | ブレスト/レビュー/優先順位付けでの活用を義務化 |

---

## 2. Persona Fatigue（ペルソナ疲労）

### 概要

```
Persona Fatigue:
  ペルソナへの関心が組織内で低下し、ツールとしての有効性を疑問視する現象

原因:
  - ペルソナが実際の意思決定に使われない
  - 作成後の更新が行われない → 現実との乖離
  - 「もうユーザーのことは知っている」という思い込み
  - 過去の失敗体験からの一般化（1 回の失敗で全否定）

NN/G 調査データ:
  - 46% の組織が 1-4 年ごとに更新
  - 28% が四半期以上の頻度で更新
  - 26% が 5 年以上更新なし or 一度も更新しない
```

### 対策フレームワーク

| 対策 | 実施方法 | 効果 |
|------|---------|------|
| **Living Document 化** | 編集可能な形式 + 定期レビュー | 陳腐化防止 |
| **意思決定統合** | 機能レビュー/優先順位付けでペルソナ参照を必須化 | 組織浸透 |
| **データ駆動更新** | 行動データ → ドリフト検出 → 自動アラート | 更新頻度向上 |
| **軽量フォーマット** | 過度なデザインを避け、情報密度を優先 | 編集障壁低下 |
| **リーダーシップ関与** | 「研究成果物」ではなく「整合ツール」として位置づけ | 経営層の支持 |

---

## 3. Anti-Persona（アンチペルソナ）

### 概要

```
Anti-Persona:
  製品・サービスが対象としない（すべきでない）ユーザーのプロファイル
  → 早期離脱者、低価値ユーザー、ミスマッチユーザーを定義

目的:
  1. リソースの集中（対象外ユーザーへの投資を回避）
  2. メッセージングの精度向上（誤った期待を生まない）
  3. プロダクト方針の明確化（何を「しない」かの定義）
```

### Anti-Persona 構築 5 ステップ

| Step | Action | 詳細 |
|------|--------|------|
| 1 | **高速離脱者の特定** | リテンション下位 20% のユーザーを抽出 |
| 2 | **離脱理由の調査** | 離脱後 24 時間以内のインタビュー |
| 3 | **理由のセグメント化** | 「関連性あり」（製品課題）vs「関連性なし」（スコープ外）に分類 |
| 4 | **誤った期待の追跡** | 専門家評価 + ユーザビリティテストで混乱ポイント特定 |
| 5 | **プロファイル文書化** | 名前・写真・引用・期待ギャップを記録 |

### Cast との連携

```
Cast の CONJURE/EVOLVE モードでの活用:
  1. Anti-Persona を registry に anti-persona カテゴリで登録
  2. AUDIT モードで Anti-Persona パターンへの該当をチェック
  3. Echo ハンドオフ時に Anti-Persona を除外リストとして提供
  4. Retain ハンドオフ時に Anti-Persona を離脱予防の参考として提供
```

---

## 4. NN/G ペルソナ失敗 5 因子

| # | 失敗因子 | 説明 | 対策 |
|---|---------|------|------|
| 1 | **Created but not used** | 作成後に棚上げ | 意思決定プロセスへの統合 |
| 2 | **No leadership buy-in** | 「すでにユーザーを知っている」 | 整合ツールとしての位置づけ |
| 3 | **Silo creation** | UX チーム単独 → 他チーム無関心 | ワークショップ形式の共同作成 |
| 4 | **Communication failure** | 使い方が伝わらない | 活用事例集 + 定期ワークショップ |
| 5 | **Structural misalignment** | 目的と形式のミスマッチ | 目的定義 → 適切なペルソナ形式選択 |

---

## 5. ペルソナ代替・補完アプローチ

| アプローチ | 特徴 | ペルソナとの関係 |
|-----------|------|----------------|
| **JTBD (Jobs-to-Be-Done)** | ユーザーの「達成したいジョブ」に焦点 | 補完（ペルソナの Goals セクションに統合） |
| **Cognitive Friction Mapping** | タスク中の認知負荷・意思決定疲労を追跡 | 補完（Echo Testing Focus に統合） |
| **Journey Mapping** | 実際のユーザーフローと行動パターン | 補完（Digital Behavior + Echo Testing Focus） |
| **Behavioral Archetypes** | デモグラフィックス不要の行動パターン分類 | 代替候補（Cast の echo_base_mapping が類似） |
| **Anti-Persona** | 対象外ユーザーの定義 | 補完（ペルソナの対極） |

**Source:** [NN/G: Why Personas Fail](https://www.nngroup.com/articles/why-personas-fail/) · [NN/G: Personas Are Living Documents](https://www.nngroup.com/articles/personas-are-living-documents/) · [NN/G: Revising Personas](https://www.nngroup.com/articles/revising-personas/) · [LogRocket: User Personas Common Mistakes](https://blog.logrocket.com/ux-design/user-personas-common-mistakes/) · [LogRocket: Anti-Personas](https://blog.logrocket.com/ux-design/using-anti-personas/) · [Medium: Persona Fatigue](https://medium.com/@marketingtd64/persona-fatigue-do-we-still-need-them-in-2025-f49b411c7309)
