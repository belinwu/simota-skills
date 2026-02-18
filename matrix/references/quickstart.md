# Quickstart Templates

Matrix の即席テンプレート3種。コピー&ペーストして使用可能。

---

## Q1: テストマトリクス（browser × os × auth）

**ユースケース**: Webアプリのブラウザ互換性テスト計画

```yaml
matrix:
  domain: test
  axes:
    - name: browser
      values: [Chrome, Firefox, Safari]
    - name: os
      values: [Windows, macOS, Linux]
    - name: auth
      values: [logged_in, anonymous]
  constraints:
    - exclude: {browser: Safari, os: Windows}
    - exclude: {browser: Safari, os: Linux}
  optimization: pairwise
  priority_axis: browser
```

**結果例**:
- 全組み合わせ: 18 → Pairwise後: 6件（削減率 67%）
- カバレッジ: 全2軸ペア 100%

**後続エージェント**: `Voyager`（E2Eテスト実装）/ `Radar`（テストカバレッジ向上）

---

## Q2: デプロイマトリクス（environment × region × traffic）

**ユースケース**: カナリアリリースの段階的デプロイ計画

```yaml
matrix:
  domain: deploy
  axes:
    - name: environment
      values: [production, staging]
    - name: region
      values: [us-east, ap-northeast, eu-west]
    - name: traffic
      values: [100%, 50%, 10%]
  constraints:
    - if: {environment: staging}
      then_exclude: {traffic: "100%"}
  optimization: pairwise
  priority_axis: region
```

**結果例**:
- 全組み合わせ: 18 → Pairwise後: 6件（削減率 67%）
- カバレッジ: 全2軸ペア 100%

**後続エージェント**: `Scaffold`（インフラプロビジョニング）/ `Gear`（デプロイパイプライン）

---

## Q3: リスクマトリクス（threat × surface × auth_level）

**ユースケース**: セキュリティリスク評価の優先順位付け

```yaml
matrix:
  domain: risk
  axes:
    - name: threat
      values: [XSS, SQLi, CSRF, RCE]
    - name: surface
      values: [API, Web, Mobile]
    - name: auth_level
      values: [admin, user, anonymous]
  optimization: pairwise
  priority_axis: threat
```

**結果例**:
- 全組み合わせ: 36 → Pairwise後: 9件（削減率 75%）
- カバレッジ: 全2軸ペア 100%

**後続エージェント**: `Triage`（インシデント対応）/ `Sentinel`（静的セキュリティ分析）/ `Scout`（根本原因調査）

---

## 使い方

1. 上記YAMLをコピーしてMatrixに渡す
2. Matrixが最適化された実行計画を生成
3. 後続エージェントに渡して実行

より多くのドメインパターン: `references/domain-patterns.md`
完全なYAML仕様: `references/input-schema.md`
