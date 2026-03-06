# Event Streaming Anti-Patterns

> Kafka / イベント駆動アーキテクチャの失敗パターン、イベントモデリングの罠、運用課題

## 1. イベントストリーミング 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **ES-01** | **God Topic（神トピック）** | 全イベントを1つのトピックに投入 | コンシューマーが大量のフィルタリング、パーティション戦略崩壊、スケーリング不能 | ドメイン別トピック分割（`{domain}.{entity}.{event}`）、関心の分離 |
| **ES-02** | **Schema Anarchy（スキーマ無法地帯）** | イベントスキーマのバージョン管理なし | デシリアライゼーション障害、コンシューマー破損、後方互換性なし | Schema Registry（Avro/Protobuf）、後方互換のみ許可、スキーマ進化ルール |
| **ES-03** | **Consumer Coupling（コンシューマー結合）** | プロデューサーがコンシューマーの要求に合わせてイベントを設計 | コンシューマー追加のたびにイベント変更、N:M の結合爆発 | ドメインイベント中心設計、コンシューマーは自分で投影（CQRS パターン） |
| **ES-04** | **Fire and Forget（撃ちっぱなし）** | イベント発行後の配信保証なし | acks=0 設定、メッセージ喪失、データ不整合 | acks=all + min.insync.replicas=2、プロデューサーべき等性有効化 |
| **ES-05** | **Offset Mismanagement（オフセット誤管理）** | auto.commit + 処理前コミット | 障害時のメッセージ喪失 or 重複処理、exactly-once 崩壊 | 手動コミット（処理完了後）、トランザクション利用、べき等コンシューマー |
| **ES-06** | **Partition Key Blindness（パーティションキー盲目）** | パーティションキーの設計を考慮しない | データ偏り（hot partition）、順序保証崩壊、並列処理効率低下 | ビジネスキーによるパーティショニング、カーディナリティ分析 |
| **ES-07** | **Event Soup（イベントスープ）** | コマンドとイベントの区別なし | `CreateOrder` と `OrderCreated` の混在、責務の曖昧さ、リプレイ不能 | コマンド（依頼）vs イベント（事実）の厳密分離、過去形命名（`OrderCreated`） |

---

## 2. イベントモデリングの罠

```
イベント設計のアンチパターン:

  ❌ Fat Event（太ったイベント）:
    → イベントに関連エンティティ全データを含める
    → 問題: イベントサイズ肥大、結合度増大、変更伝播
    → 対策: イベントは「何が起きたか」の最小情報 + 参照ID

  ❌ Thin Event（痩せたイベント）:
    → イベントに ID のみで詳細なし
    → 問題: コンシューマーが毎回 API コール、遅延増大
    → 対策: コンシューマーが自己完結できる最小限のデータを含める

  ❌ CRUD Event（CRUD イベント）:
    → Created/Updated/Deleted の汎用イベント
    → 問題: ビジネス意図が不明、何が変わったか不明
    → 対策: ドメインイベント（OrderPlaced, PaymentCompleted, ItemShipped）

  ❌ Temporal Coupling（時間的結合）:
    → イベントの順序に依存した処理
    → 問題: 順序保証はパーティション内のみ、分散環境で破綻
    → 対策: イベントの独立性設計、eventually consistent の許容

  ❌ Database as Event Bus（DB をイベントバスに）:
    → テーブルのポーリングでイベント検出
    → 問題: レイテンシ、DB 負荷、スケーラビリティ制限
    → 対策: Outbox Pattern + CDC（Debezium）、または直接イベント発行

  適切なイベント設計:
    → 名前: 過去形のドメイン用語（OrderPlaced, not CreateOrder）
    → データ: コンシューマーが自己完結できる最小限
    → メタデータ: event_id, timestamp, source, correlation_id, version
    → スキーマ: 後方互換（フィールド追加OK、削除/型変更NG）
    → サイズ目安: 1KB〜10KB（超える場合は参照パターン）
```

---

## 3. Kafka 運用のアンチパターン

```
設定・運用の罠:

  パーティション設計:
    ❌ パーティション数 = 1（スケーリング不能）
    ❌ パーティション数 = 1000（管理不能、リバランスコスト大）
    ✅ 想定ピークスループット × 10（最小3、実用上限100）
    ✅ 後から増やせるが減らせない → 控えめに開始

  リテンション:
    ❌ 無制限リテンション（ストレージ爆発）
    ❌ 1日リテンション（リプレイ不能）
    ✅ 本番: 7日（リプレイ要件に応じて延長）
    ✅ コンパクショントピック: 無期限（ステートトピック用）

  コンシューマー設計:
    ❌ 1コンシューマーで全トピック購読
    ❌ コンシューマー数 > パーティション数（アイドルコンシューマー）
    ✅ 目的別コンシューマーグループ分離
    ✅ コンシューマー数 ≤ パーティション数

  エラーハンドリング:
    ❌ エラー時に無限リトライ（poison pill 問題）
    ❌ エラーレコード破棄（データ損失）
    ✅ リトライ可能エラー: exponential backoff（上限付き）
    ✅ リトライ不可エラー: Dead Letter Topic へ退避
    ✅ Poison pill 対策: 個別レコードスキップ + アラート

  モニタリング必須メトリクス:
    □ Consumer lag（コンシューマー遅延）
    □ Throughput（プロデューサー/コンシューマー）
    □ Error rate（エラー率）
    □ Rebalance frequency（リバランス頻度）
    □ Disk usage（ブローカーディスク使用量）
    □ Under-replicated partitions（レプリケーション遅延）
```

---

## 4. Exactly-Once の現実

```
配信保証レベル:

  At-Most-Once（最大1回）:
    → acks=0, auto.commit=true
    → メッセージ喪失あり、重複なし
    → 用途: ログ、メトリクス（損失許容）

  At-Least-Once（最低1回）:
    → acks=all, 手動コミット（処理後）
    → メッセージ喪失なし、重複あり
    → 用途: 大半のユースケース（+ べき等コンシューマー）

  Exactly-Once（正確に1回）:
    → Kafka Transactions + べき等プロデューサー
    → 重複なし、喪失なし
    → 制約: Kafka→Kafka のみ完全保証、外部システム連携は At-Least-Once + べき等

  現実的なアプローチ:
    → 「Effectively Once」= At-Least-Once + べき等処理
    → コンシューマー側で重複排除（event_id ベース）
    → シンク側で UPSERT（べき等書き込み）
    → Exactly-Once を目指すより、べき等設計に投資
```

---

## 5. Outbox Pattern

```
問題: DB 更新とイベント発行のアトミック性

  ❌ 危険なパターン:
    1. DB に書き込み
    2. Kafka にイベント発行
    → 2 が失敗すると DB とイベントが不整合

  ✅ Outbox Pattern:
    1. DB に書き込み + outbox テーブルに書き込み（同一トランザクション）
    2. CDC（Debezium）が outbox テーブルを監視
    3. 変更を Kafka トピックに自動発行

  outbox テーブル設計:
    CREATE TABLE outbox (
      id UUID PRIMARY KEY,
      aggregate_type VARCHAR(255),
      aggregate_id VARCHAR(255),
      event_type VARCHAR(255),
      payload JSONB,
      created_at TIMESTAMP DEFAULT NOW()
    );

  利点:
    → DB 更新とイベント発行のアトミック性保証
    → プロデューサーが Kafka に直接依存しない
    → CDC による信頼性の高い配信
```

---

## 6. Stream との連携

```
Stream での活用:
  1. Streaming Design で ES-01〜07 のスクリーニング
  2. イベントモデリング時に命名・構造ガイド適用
  3. Kafka 設定レビュー時に運用アンチパターン検出
  4. Beacon への可観測性ハンドオフ時にメトリクス定義提供

品質ゲート:
  - 1トピックに複数ドメイン → トピック分割提案（ES-01 防止）
  - Schema Registry 未使用 → 導入提案（ES-02 防止）
  - acks=0 設定 → 配信保証レベル確認（ES-04 防止）
  - auto.commit=true → 手動コミット移行（ES-05 防止）
  - パーティションキー未指定 → キー設計提案（ES-06 防止）
  - コマンド形式のイベント名 → ドメインイベント名提案（ES-07 防止）
  - DLT 未設定 → Dead Letter Topic 追加（運用安全性確保）
```

**Source:** [Event-Driven.io: Anti-Patterns](https://event-driven.io/en/anti-patterns/) · [Estuary: Kafka Event-Driven Architecture](https://estuary.dev/blog/kafka-event-driven-architecture/) · [IBM: Event-Driven Architecture Usage Patterns for Kafka](https://developer.ibm.com/articles/awb-event-driven-architecture-usage-patterns-kafka/) · [ArXiv: Kafka Event-Streaming Systems Analysis](https://arxiv.org/html/2512.16146)
