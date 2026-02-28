# Interaction Triggers

Levyが判断を求めるべきタイミングとYAMLテンプレート。

---

## トリガー一覧

| Trigger | Condition | Default Action |
|---------|-----------|---------------|
| FISCAL_YEAR_UNKNOWN | 対象年度が不明 | 直近の申告年度を適用 |
| INCOME_TYPE_AMBIGUOUS | 事業所得と雑所得の判定が困難 | 事業所得の要件チェックリストを提示 |
| SPECIAL_INCOME | 暗号資産・海外所得・ストックオプション等の特殊所得 | 税理士相談を推奨 |
| CONSUMPTION_TAX | 年間売上1,000万円超 or インボイス関連 | 課税事業者判定フローを提示 |
| AMENDMENT_REQUEST | 修正申告・更正の請求 | 対応レベルL3として税理士相談を推奨 |
| BLUE_FILING_ELIGIBILITY | 青色申告承認申請の提出状況が不明 | 申請状況を確認 |

---

## YAML テンプレート

### FISCAL_YEAR_UNKNOWN

```yaml
INTERACTION_TRIGGER:
  type: FISCAL_YEAR_UNKNOWN
  condition: "対象年度が明示されていない"
  question: "どの年度の確定申告についてお聞きですか？"
  options:
    - "令和6年分（2024年）— 2025年3月申告期限(Recommended)"
    - "令和7年分（2025年）— 2026年3月申告期限"
    - "令和5年分（2023年）以前 — 期限後申告・還付申告"
    - "Other（詳細を教えてください）"
  context:
    current_date: "[現在日付]"
    filing_deadline: "対象年度の翌年3月15日"
  default: "令和6年分（2024年）"
```

### INCOME_TYPE_AMBIGUOUS

```yaml
INTERACTION_TRIGGER:
  type: INCOME_TYPE_AMBIGUOUS
  condition: "副業収入の所得区分（事業所得 vs 雑所得）が判定困難"
  question: "副業の所得区分を判定するため、以下のどれに該当しますか？"
  options:
    - "開業届提出済み・反復継続的な収入・独立した事業として運営 → 事業所得"
    - "会社員の副業・年間収入300万円以下・開業届未提出 → 雑所得(Recommended)"
    - "判断が難しい — 詳細ヒアリングを希望"
    - "Other（詳細を教えてください）"
  context:
    revenue_amount: "[年間収入額]"
    has_opening_notification: "[開業届の有無]"
    business_continuity: "[反復継続性]"
  default: "雑所得"
  reference: "所得税基本通達35-2、国税庁「雑所得の範囲の明確化」"
```

### SPECIAL_INCOME

```yaml
INTERACTION_TRIGGER:
  type: SPECIAL_INCOME
  condition: "暗号資産・海外所得・ストックオプション・不動産売却等の特殊所得を検出"
  question: "特殊な所得が含まれています。どのように対応しますか？"
  options:
    - "一般的な解説と計算の大枠を提示（免責事項付き）(Recommended)"
    - "税理士への相談を推奨（紹介基準を提示）"
    - "該当所得を除外し、他の所得のみ計算"
    - "Other（詳細を教えてください）"
  context:
    special_income_type: "[検出した特殊所得の種類]"
    estimated_amount: "[概算金額]"
  default: "一般的な解説と計算の大枠を提示（免責事項付き）"
  guardrail: "references/disclaimer-templates.md L3テンプレートを適用"
```

### CONSUMPTION_TAX

```yaml
INTERACTION_TRIGGER:
  type: CONSUMPTION_TAX
  condition: "年間売上が1,000万円超、またはインボイス登録に関する質問"
  question: "消費税に関する判断が必要です。現在の状況を教えてください。"
  options:
    - "免税事業者（年間売上1,000万円以下）— インボイス登録を検討中"
    - "課税事業者 — 簡易課税を選択済み(Recommended)"
    - "課税事業者 — 本則課税"
    - "Other（詳細を教えてください）"
  context:
    annual_revenue: "[年間売上]"
    invoice_registration: "[インボイス登録状況]"
    tax_method: "[課税方式]"
  default: "課税事業者 — 簡易課税を選択済み"
  reference: "消費税法第9条、インボイス制度（適格請求書等保存方式）"
```

### AMENDMENT_REQUEST

```yaml
INTERACTION_TRIGGER:
  type: AMENDMENT_REQUEST
  condition: "修正申告・更正の請求・期限後申告に関する質問"
  question: "修正申告・更正の請求は専門的な判断が必要です。どう進めますか？"
  options:
    - "税理士への相談を推奨（一般的な手続きフローのみ案内）(Recommended)"
    - "一般的な制度解説のみ提示（免責事項付き）"
    - "修正内容が単純なため手続きガイドを希望"
    - "Other（詳細を教えてください）"
  context:
    amendment_type: "[修正申告 / 更正の請求 / 期限後申告]"
    original_filing_date: "[当初申告日]"
    reason: "[修正理由]"
  default: "税理士への相談を推奨"
  guardrail: "references/disclaimer-templates.md L3テンプレートを適用"
```

### BLUE_FILING_ELIGIBILITY

```yaml
INTERACTION_TRIGGER:
  type: BLUE_FILING_ELIGIBILITY
  condition: "青色申告の適用可否が不明"
  question: "青色申告承認申請書は提出済みですか？"
  options:
    - "提出済み — 65万円控除を適用(Recommended)"
    - "未提出 — 今年度から申請したい（期限・手続きを案内）"
    - "不明 — 確認方法を知りたい"
    - "Other（詳細を教えてください）"
  context:
    business_start_date: "[事業開始日]"
    filing_history: "[過去の申告実績]"
  default: "提出済み — 65万円控除を適用"
  reference: "所得税法第143条〜第151条"
```

---

## トリガー検出のヒューリスティクス

| 検出キーワード | 推定トリガー |
|-------------|------------|
| 「何年」「いつの」「年度」が不明な入力 | FISCAL_YEAR_UNKNOWN |
| 「副業」「事業か雑か」「開業届」「300万円」 | INCOME_TYPE_AMBIGUOUS |
| 「暗号資産」「仮想通貨」「海外」「ストックオプション」「不動産売却」 | SPECIAL_INCOME |
| 「消費税」「インボイス」「1000万円」「課税事業者」「簡易課税」 | CONSUMPTION_TAX |
| 「修正申告」「更正」「間違えた」「やり直し」「期限後」 | AMENDMENT_REQUEST |
| 「青色申告」「65万円控除」「承認申請」 | BLUE_FILING_ELIGIBILITY |
