# Scope Creep & Execution Anti-Patterns

> スコープクリープの防止、実行フェーズの失敗パターン、持続可能なペースの維持

## 1. スコープクリープ 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **SC-01** | **Maverick Addition（独断追加）** | チーム合意なしにSprint Backlogにアイテム追加 | 予定外の作業が出現、チームのコントロール感喪失、見積もり崩壊 | Sprint Backlog の変更はチーム合意のみ、POも勝手に追加不可 |
| **SC-02** | **Scope Creep via "Quick Fix"（Quick Fix経由のスコープ拡大）** | 「ちょっとした修正」が積み重なりスコープが膨張 | 「ついでに」「すぐ終わる」が1日に3回以上、計画作業の遅延 | 2分ルール: 2分超はParking Lot行き、現在のステップを優先完了 |
| **SC-03** | **Stakeholder Bypass（ステークホルダーバイパス）** | ステークホルダーが直接開発者に作業を依頼 | POを迂回した要望、優先順位の混乱、隠れ作業の発生 | 全リクエストはPO（またはバックログ）経由、開発者は直接受けない |
| **SC-04** | **Gold-Plating（金メッキ）** | 受入基準を超えた機能追加をチームが自発的に実施 | 「ついでにもっと良くしよう」、Definition of Doneを超えた改善、時間超過 | 受入基準の厳守、追加改善はバックログに記録して別途対応 |
| **SC-05** | **Emergency Inflation（緊急インフレ）** | 通常の要望が「緊急バグ」としてSprintに割り込み | 週2-3件以上の「緊急」、エクスプレスレーンの乱用 | バグ分類基準の明確化（本番障害/セキュリティ/その他）、緊急レーンの厳格管理 |
| **SC-06** | **Acceptance Criteria Drift（受入基準のドリフト）** | PO がSprint中に受入基準を変更・拡大 | Sprint中のスコープ変更、「やっぱりこれも必要」、再見積もり不在 | Sprint開始後の受入基準変更はPO-チーム合意が必要、変更時は工数再評価 |
| **SC-07** | **Perfectionism Trap（完璧主義の罠）** | 「もう少し良くできる」でいつまでも完了しない | タスクが永遠に「進行中」、エッジケースの無限追加、デプロイの先送り | Definition of Done の厳守、「十分に良い」の基準を明確化、 MVP思考 |

---

## 2. 実行フェーズのアンチパターン

```
ワークフロー実行の罠:

  ❌ Board Out-of-Date（ボード未更新）:
    → スプリントボードが実際のステータスを反映していない
    → ステークホルダーの信頼喪失、可視性ゼロ
    → 対策: Daily Scrumでボード更新を習慣化

  ❌ No Flow to Done（完了フローの欠如）:
    → 全タスクがSprint末までオープンのまま
    → 早期フィードバックなし、末尾に統合リスク集中
    → 対策: 1PBIずつ完了させる（バッチサイズ最小化）

  ❌ Absent PO（不在のPO）:
    → Sprint中にPOが質問に応答できない
    → 開発者が独断で判断、認識齟齬の蓄積
    → 対策: POの可用性確保、判断基準の事前合意

  ❌ Delayed Feedback（フィードバック遅延）:
    → 完成した作業のレビュー/承認がSprint末まで放置
    → サイクルタイム増大、手戻りコスト増大
    → 対策: 完了即レビュー、POは完成アイテムを即検査

  ❌ Lack of Support（サポート不足）:
    → タスクが予想以上に時間がかかっているのに誰も気づかない
    → サイレントな失敗、30分以上の停滞
    → 対策: Sherpa のStalled Detection（30分/3回/ブロック時にアラート）

  ❌ Reassigning Team Members（チームメンバーの入替え）:
    → マネジメントがSprint中にメンバーを別チームに移動
    → チーム連続性の破壊、信頼関係の毀損
    → 対策: Sprintのタイムボックス中はチーム構成を維持
```

---

## 3. 持続可能なペースの維持

```
バーンアウト予防:

  危険サイン:
    □ 毎Sprint Goal未達 → キャパシティ見直し
    □ エラー率の増加 → 休憩/ステップサイズ縮小
    □ ドリフト頻度の増加 → 集中力低下の兆候
    □ 作業時間の延長が常態化 → 持続不可能なペース
    □ チームの発言が減少 → 心理的安全性の問題

  対策:
    □ 80-85%キャパシティでコミット（15-20%のバッファ）
    □ 改善アクション1件をSprintに含める
    □ 休憩の強制（Sherpa Weather: Fatigue Detection）
    □ Sprint Retrospectiveで持続可能性を定期チェック
    □ 「No」と言う権限をチームに付与

  Sherpa Weather との統合:
    → Energy指標が「Fatigued」→ ステップサイズ縮小
    → 3h超のセッション → 休憩提案
    → 連続2Sprint未達 → キャパシティ再計算提案
    → ドリフト頻度 3+/30分 → 集中力チェック
```

---

## 4. スコープ管理のベストプラクティス

```
Sprint 境界の防衛:

  Sprint開始時:
    □ Sprint Goalが明確に定義されている
    □ 受入基準が全PBIに記載されている
    □ Definition of Done が合意されている
    □ キャパシティが正直に計算されている
    □ スコープ外が明示されている

  Sprint中:
    □ 新規要望 → バックログ行き（Parking Lot）
    □ 「Quick Fix」→ 2分ルール適用
    □ 緊急割り込み → バグ分類基準で判定
    □ 受入基準変更 → チーム合意 + 工数再評価
    □ スコープ変化 → Weather Reportに反映

  Sprint終了時:
    □ 完了 vs 未完了の明確な判定
    □ 未完了アイテムは次Sprintのバックログに戻す
    □ スコープ変更の振り返り（何が変わったか、なぜか）
    □ 学習事項をRetrospectiveに記録

変更管理プロセス:
  1. 変更要求の受理（誰が、何を、なぜ）
  2. 影響分析（工数、リスク、依存関係）
  3. トレードオフ提示（追加する場合、何を削るか）
  4. チーム合意（PO + 開発チーム）
  5. ボードへの反映 + Weather Report更新
```

---

## 5. 外部割り込みの分類と対応

```
割り込みの緊急度分類:

  P0 — 本番障害（即座対応）:
    → 顧客影響あり、データ損失リスク
    → 対応: 即座にSprint作業を中断、Triage起動
    → Sherpa: Red Alert → ASSESS → Triage ハンドオフ

  P1 — 重大バグ（当日対応）:
    → 重大な機能障害、回避策あり
    → 対応: 現在のステップ完了後に対応
    → Sherpa: Yellow Alert → スコープ調整 → 対応

  P2 — 改善要望（バックログ行き）:
    → 機能強化、UX改善、技術的負債
    → 対応: Parking Lot → 次Sprint計画で検討
    → Sherpa: LOCATE → Parking Lot → 続行

  P3 — 情報共有（非同期処理）:
    → FYI、質問、ディスカッション
    → 対応: バッチ処理時間（30分ごと等）に確認
    → Sherpa: 影響なし、フロー維持
```

---

## 6. Sherpa との連携

```
Sherpa での活用:
  1. LOCATE フェーズで SC-01〜07 のリアルタイム検出
  2. Anti-Drift フレームワークと連携したスコープ防衛
  3. Weather System にスコープ変化を反映
  4. Emergency Protocols と割り込み分類の統合

品質ゲート:
  - Sprint Backlogへの無断追加 → Maverick検出（SC-01 防止）
  - 「ちょっとした修正」の連発 → 2分ルール適用（SC-02 防止）
  - 直接の開発者依頼 → PO/バックログ経由を強制（SC-03 防止）
  - 受入基準超えの作業 → DoD遵守リマインド（SC-04 防止）
  - 偽の緊急 → バグ分類基準適用（SC-05 防止）
  - Sprint中の基準変更 → 合意プロセス+工数再評価（SC-06 防止）
  - 完了しないタスク → MVP思考+DoD確認（SC-07 防止）
  - Sprint毎の未達 → キャパシティ再計算（バーンアウト防止）
```

**Source:** [Age-of-Product: Sprint Anti-Patterns](https://age-of-product.com/sprint-anti-patterns-2/) · [Agilemania: Sprint Planning Anti-Patterns](https://agilemania.com/anti-patterns-of-sprint-planning-task-creation) · [minware: Scope Creep](https://www.minware.com/guide/anti-patterns/scope-creep) · [GitScrum: Preventing Scope Creep](https://docs.gitscrum.com/en/best-practices/preventing-scope-creep-in-agile-projects)
