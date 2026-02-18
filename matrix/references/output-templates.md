# Output Templates

Matrix が生成する実行計画・カバレッジレポートの完全テンプレート。

---

## Template 1: 標準実行計画（Matrix Plan）

全ドメイン共通の標準出力フォーマット。

```markdown
## Matrix Plan: [ドメイン] — [名前]

### 組み合わせ空間サマリー

| 項目 | 値 |
|------|---|
| 軸数 | 3 |
| 軸の構成 | browser(3) × os(2) × auth(2) |
| 全組み合わせ数 | 12 |
| 最適化手法 | Pairwise (All-pairs) |
| 最適化後の件数 | **4** |
| 削減率 | **67%** |
| 2-wayカバレッジ保証 | ✅ 全ペア網羅（12/12ペア） |

---

### 実行セット（優先度順）

| # | browser | os      | auth      | Priority | カバーするペア |
|---|---------|---------|-----------|----------|--------------|
| 1 | Chrome  | Windows | logged_in | 🔴 HIGH  | (Chr,Win)(Chr,log)(Win,log) |
| 2 | Firefox | macOS   | anonymous | 🔴 HIGH  | (FF,mac)(FF,anon)(mac,anon) |
| 3 | Safari  | Windows | anonymous | 🟡 MED   | (Saf,Win)(Saf,anon) |
| 4 | Chrome  | macOS   | logged_in | 🟡 MED   | (Chr,mac)(mac,log) |

> ⚠️ 除外制約: Safari × Windows は通常除外するが、指定がないため含めています。
> 必要であれば除外設定を追加してください。

---

### カバレッジ保証

```
2-way ペア総数: 12
カバー済み:    12 (100%) ✅
未カバー:       0

カバレッジマトリクス:
          Chrome  Firefox  Safari
Windows     ✅       -      ✅
macOS       ✅       ✅      -

          Windows  macOS
logged_in    ✅      ✅
anonymous    ✅      ✅
```

---

### 後続エージェントへの引き渡し

**推奨エージェント:** Voyager（E2Eテスト実装）

```yaml
handoff_to: Voyager
matrix_plan:
  domain: test
  combinations:
    - id: 1
      browser: Chrome
      os: Windows
      auth: logged_in
      priority: HIGH
    - id: 2
      browser: Firefox
      os: macOS
      auth: anonymous
      priority: HIGH
    - id: 3
      browser: Safari
      os: Windows
      auth: anonymous
      priority: MEDIUM
    - id: 4
      browser: Chrome
      os: macOS
      auth: logged_in
      priority: MEDIUM
  coverage:
    method: pairwise
    guarantee: "2-way 100%"
    total_original: 12
    total_optimized: 4
    reduction_rate: "67%"
```
```

---

## Template 2: リスクマトリクス

リスク評価ドメイン向けの出力フォーマット。

```markdown
## Risk Matrix: [名前]

### 組み合わせ空間
- 軸: threat(5) × surface(4) × auth_level(3) = 60組み合わせ
- 最適化後: 15件（削減率 75%）

### 優先度別リスク評価表

| # | 脅威 | 攻撃対象 | 認証レベル | リスクスコア | 対応優先度 |
|---|------|---------|-----------|-----------|---------|
| 1 | SQLi | API | anonymous | 🔴 Critical (9.8) | P0 即時対応 |
| 2 | XSS  | Web | anonymous | 🔴 High (8.5) | P0 即時対応 |
| 3 | CSRF | Web | authenticated | 🟡 High (7.2) | P1 今週中 |
| 4 | SSRF | API | authenticated | 🟡 Medium (6.0) | P2 今月中 |
...

### リスクスコア計算式
```
リスクスコア = 脅威スコア × 攻撃対象の露出度 × 認証バイパス難易度
```

### 引き渡し
**推奨エージェント:** Triage（影響範囲特定）→ Sentinel（脆弱性修正）
```

---

## Template 3: デプロイマトリクス

デプロイ戦略ドメイン向けの出力フォーマット。

```markdown
## Deploy Matrix: [名前]

### デプロイ計画（ロールアウト順）

| 順序 | 環境 | リージョン | バージョン | トラフィック | 検証項目 |
|------|------|----------|----------|-----------|---------|
| 1 | staging | ap-northeast-1 | v1.5.1 | 100% | ヘルスチェック・スモークテスト |
| 2 | production | ap-northeast-1 | v1.5.1 | 10% | エラー率監視・p99レイテンシ |
| 3 | production | us-east-1 | v1.5.1 | 10% | 同上 |
| 4 | production | ap-northeast-1 | v1.5.1 | 50% | トラフィック安定確認 |
| 5 | production | all | v1.5.1 | 100% | フルロールアウト |

### ロールバック条件
- エラー率 > 0.1% → 即時ロールバック
- p99レイテンシ > 2秒 → 次ステップ停止

### 引き渡し
**推奨エージェント:** Scaffold（IaC実行）→ Gear（監視設定）→ Beacon（SLO確認）
```

---

## Template 4: UX検証マトリクス

UX/ペルソナ検証ドメイン向けの出力フォーマット。

```markdown
## UX Matrix: [名前]

### 検証セット（Echo/Researcherへの依頼フォーマット）

| # | ペルソナ | デバイス | シナリオ | 検証ポイント |
|---|---------|---------|---------|-----------|
| 1 | 初心者ユーザー | スマートフォン | 初回登録 | オンボーディング完了率、離脱ポイント |
| 2 | シニアユーザー | タブレット | 購入フロー | 操作エラー頻度、ヘルプ参照率 |
| 3 | ヘビーユーザー | デスクトップ | 高度な設定 | タスク完了時間、ショートカット利用率 |
...

### ペルソナ定義（Castへの連携用）
各ペルソナの詳細は Cast に依頼して生成してください。

### 引き渡し
**推奨エージェント:** Cast（ペルソナ詳細化）→ Echo（UX検証実行）
```

---

## Template 5: 実験パラメータマトリクス

A/B実験ドメイン向けの出力フォーマット。

```markdown
## Experiment Matrix: [名前]

### 実験設計（Experimentエージェントへの引き渡し）

| # | 変数A | 変数B | ユーザーセグメント | 期間 | 測定指標 |
|---|-------|-------|----------------|------|---------|
| 1 | ボタン色=青 | CTA文言=「今すぐ」 | 新規ユーザー | 2週間 | CTR, CVR |
| 2 | ボタン色=緑 | CTA文言=「無料で試す」 | 既存ユーザー | 2週間 | 再購入率 |
...

### サンプルサイズ計算依頼
各実験グループの必要サンプルサイズは Experiment に計算を依頼してください。

### 引き渡し
**推奨エージェント:** Experiment（仮説文書・サンプルサイズ計算）→ Pulse（KPIトラッキング設計）
```

---

## Template 6: カバレッジ結果レポート（実行後）

実行完了後に結果を受け取ってカバレッジを更新するフォーマット。

```markdown
## Coverage Report: [名前] — 実行後

### 実行結果サマリー

| 項目 | 計画値 | 実績値 |
|------|-------|-------|
| 総件数 | 9 | 9 |
| 成功 | - | 7 ✅ |
| 失敗 | - | 2 ❌ |
| スキップ | - | 0 |

### 失敗ケースの分析

| # | 失敗した組み合わせ | 発見されたバグ | 影響するペア |
|---|-----------------|------------|-----------|
| 3 | Safari × macOS × auth_sso | SSO トークン有効期限バグ | (Safari,SSO)(macOS,SSO) |
| 7 | Chrome × iOS × offline | Service Worker 登録失敗 | (Chrome,iOS)(iOS,offline) |

### 未カバレッジの警告
```
⚠️ 以下のペアが未検証です（失敗により）:
- (Safari, SSO): 失敗 #3 により未確認
- (macOS, SSO): 失敗 #3 により未確認

追加実施推奨: Firefox × Windows × auth_sso
```

### 引き渡し
**推奨エージェント:** Scout（失敗の根本原因分析）→ Builder（修正実装）
```
