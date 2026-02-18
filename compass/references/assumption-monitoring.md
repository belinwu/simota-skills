# Assumption Monitoring Reference — Compass

前提条件の監視ロジック、Assumption-to-Metric マッピング、状態遷移ルール。

---

## Assumption-to-Metric Mapping

各前提仮定を測定可能な指標に紐付ける構造。

```yaml
assumption_mapping:
  assumption_id: "A-001"
  assumption_text: "<前提仮定の記述>"
  category: "MARKET | CUSTOMER | FINANCIAL | TECHNOLOGY | REGULATORY"
  source: "Helm scenario / User input / Compete intel"
  linked_metric:
    metric_name: "<KPI名>"
    data_source: "Pulse | Compete | 直接入力"
    measurement_frequency: "DAILY | WEEKLY | MONTHLY | QUARTERLY"
  thresholds:
    green: "<条件: 正常範囲>"
    yellow: "<条件: 注意範囲>"
    red: "<条件: 危険範囲>"
    black: "<条件: 致命的>"
  current_status: "VALID | WATCH | BREACH"
  last_checked: "YYYY-MM-DD"
  breach_history: []
```

---

## Assumption Categories

| Category | 典型的な前提 | 典型的なメトリクス | 監視頻度 |
|----------|------------|----------------|---------|
| **MARKET** | 市場成長率X%維持、TAM拡大 | 市場規模データ、業界レポート | QUARTERLY |
| **CUSTOMER** | チャーン率X%以下、NPS XX以上 | チャーン率、NPS、CSAT | MONTHLY |
| **FINANCIAL** | 粗利率X%維持、CAC ¥X以下 | 粗利率、CAC、LTV | MONTHLY |
| **TECHNOLOGY** | プラットフォーム安定性、スケーラビリティ | SLA達成率、レスポンスタイム | WEEKLY |
| **REGULATORY** | 規制変更なし、コンプライアンス維持 | 規制動向、監査結果 | QUARTERLY |

---

## Status Transition Rules

### 遷移ロジック: VALID → WATCH → BREACH

```
VALID ──→ WATCH: メトリクスがYellow閾値に到達
WATCH ──→ VALID: メトリクスがGreen範囲に回復（2連続期間）
WATCH ──→ BREACH: メトリクスがRed閾値に到達 or WATCH状態が3期間継続
BREACH ──→ WATCH: 是正措置により改善が確認された場合
BREACH ──→ VALID: 3連続期間Green維持（完全回復）
```

### 遷移条件の詳細

| 遷移 | 条件 | アクション |
|------|------|----------|
| VALID → WATCH | メトリクスが閾値の±10-25%に接近 or 2期連続で悪化トレンド | 監視頻度を1段階引き上げ |
| WATCH → BREACH | メトリクスが閾値超過 or WATCH 3期間継続 | Alert発行、ルーティング先へ通知 |
| BREACH → WATCH | 是正措置後にメトリクス改善 | 監視継続、回復トレンド確認 |
| WATCH → VALID | 2連続期間でGreen範囲 | 監視頻度を通常に戻す |
| BREACH → VALID | 3連続期間でGreen維持 | 完全回復として記録 |

---

## Category-specific Defaults

各カテゴリの典型的なID接頭辞・閾値パターン・検証方法。実際のテンプレートは上記の汎用マッピング構造に当てはめて使用する。

| Category | ID Prefix | Typical Metric | Green | Yellow | Red | Black | Validation |
|----------|-----------|---------------|-------|--------|-----|-------|------------|
| **MARKET** | A-MKT | 市場成長率 | >= X% | X-5% 〜 X% | < X-5% | マイナス成長 | 業界レポート + Compete |
| **CUSTOMER** | A-CUS | MRRチャーン率 | <= X% | X% 〜 X+2% | > X+2% | > X+5% or 3ヶ月連続悪化 | Pulse KPIデータ |
| **FINANCIAL** | A-FIN | 粗利率 | >= X% | X-5% 〜 X% | < X-5% | < X-10% or マイナス利益 | 財務データ |
| **TECHNOLOGY** | A-TEC | SLA達成率 | >= 99.9% | 99.5% 〜 99.9% | < 99.5% | < 99.0% or 重大障害 | インフラモニタリング |
| **REGULATORY** | A-REG | 規制変更影響度 | 変更なし/軽微 | 中程度（対応可能） | 重大（事業影響） | 禁止/規制強化 | 法務レビュー + 業界動向 |

---

## Multi-Assumption Breach Protocol

3件以上の前提が同時にBREACHした場合のトリアージ手順。

### Triage Priority Matrix

| 優先度 | 条件 | アクション |
|--------|------|----------|
| **P0 — 即時対応** | FINANCIAL + CUSTOMER 同時BREACH | → Magi（ピボット判断）即座にエスカレーション |
| **P1 — 緊急** | いずれか2カテゴリ同時BREACH | → Helm（戦略修正）+ Sherpa（実行調整） |
| **P2 — 重要** | 同一カテゴリ内3件BREACH | → Helm（当該領域の戦略見直し） |
| **P3 — 注意** | 異なるカテゴリで3件WATCH | 監視頻度引き上げ、次サイクルで再評価 |

### Correlation Check

同時BREACHの場合、相関関係を確認する:
- **根本原因が共通か？** → 共通なら1つの是正措置で複数回復の可能性
- **連鎖崩壊か？** → 1つのBREACHが他を引き起こしている場合、上流を優先
- **独立事象か？** → 各前提ごとに個別対応が必要

---

## Assumption Health Dashboard (Summary Format)

```markdown
### Assumption Health — [期間]

| Category | Total | VALID | WATCH | BREACH | Health |
|----------|-------|-------|-------|--------|--------|
| MARKET | X | X | X | X | G/Y/R/B |
| CUSTOMER | X | X | X | X | G/Y/R/B |
| FINANCIAL | X | X | X | X | G/Y/R/B |
| TECHNOLOGY | X | X | X | X | G/Y/R/B |
| REGULATORY | X | X | X | X | G/Y/R/B |
| **Total** | **X** | **X** | **X** | **X** | **G/Y/R/B** |
```
