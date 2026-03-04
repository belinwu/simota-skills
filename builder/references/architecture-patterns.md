# Architecture & Design Patterns

> Clean/Hexagonal Architecture、SOLID 2025解釈、CUPID、API設計選定、エラーハンドリング戦略、DI原則、アンチパターン

## 1. Clean / Hexagonal Architecture

### 依存性ルール (最重要)

> "ソースコードの依存関係は内側にのみ向けることができる"

```
[Frameworks] → [Adapters] → [Use Cases] → [Domain/Entities]
     外側            ↓            ↓           内側 (最安定)
```

| 層 | 責務 | 依存先 |
|----|------|--------|
| Domain | エンティティ、Value Object、ドメインサービス | なし |
| Application | ユースケース (1ユーザーアクション = 1ユースケース) | Domain のみ |
| Infrastructure | リポジトリ実装、アダプター、DB接続 | Application, Domain |
| Frameworks | Webフレームワーク、DB ドライバ | すべての内側 |

### Hexagonal (Ports & Adapters)

- **Port**: 外部とのやり取りを抽象化するインターフェース
- **Adapter**: ポートの具体的実装

> "ビジネスロジックは REST/GraphQL の選択にも、DB/CSV の選択にも依存すべきではない"

### 選択ガイド

| アーキテクチャ | 適用場面 |
|--------------|---------|
| Hexagonal | API開発、プラグ可能なアダプター |
| Clean | 大規模アプリ、明確な層分離 |
| 両方の組み合わせ | エンタープライズシステム |

**注意**: フォルダ構造ではなく分離の原則。プロジェクトごとにカスタマイズが必要。

---

## 2. SOLID 2025 解釈

| 原則 | 古典的解釈 | 2025年の適用 |
|------|-----------|-------------|
| **S**RP | 1クラス1責任 | ビジネスロジックとインフラの分離 |
| **O**CP | 拡張に開、修正に閉 | プラグインアーキテクチャ |
| **L**SP | サブタイプ置換可能 | 多態的APIの統合障害防止 |
| **I**SP | クライアント不要メソッド非依存 | コンテキスト固有の小さい契約 |
| **D**IP | 抽象に依存 | DI でビジネスロジックをインフラからデカップリング |

**2025年の認識**: SOLID は OOP に限定されず、関数型・システムレベルにも適用可能な普遍的原則。

### CUPID (補完的フレームワーク)

| プロパティ | 意味 |
|-----------|------|
| **C**omposable | 容易に組み合わせ可能、最小限の依存 |
| **U**nix philosophy | 1つのことをうまくやる |
| **P**redictable | 期待通りに動作する |
| **I**diomatic | 他の開発者が理解可能 |
| **D**omain-based | 問題領域をモデル化する |

SOLID = 開発プロセス中の原則、CUPID = 完成コードのプロパティ。

---

## 3. API 設計選定

| プロトコル | 最適なケース | 特徴 |
|-----------|-------------|------|
| **REST** | CRUD、パブリックAPI | 標準HTTP、広く採用、学習コスト低 |
| **GraphQL** | SPA/モバイル、複雑なデータ | クライアント駆動、over-fetching 解消 |
| **gRPC** | マイクロサービス間通信 | バイナリ、5-7x 低レイテンシ、双方向ストリーミング |

### 2025年トレンド

内部 = gRPC、外部 = REST、高度なクライアント向け = GraphQL ゲートウェイの共存構成。

### 共通原則

- ページネーション + フィルタリング (大規模データ)
- レート制限 (ロールベース)
- セマンティックバージョニング (非推奨化通知)
- OAuth 2.0 / JWT / APIキー
- 入力バリデーション徹底
- HTTPS 強制

---

## 4. エラーハンドリング戦略

| パターン | 言語 | 特徴 |
|---------|------|------|
| エラーコード返却 | Go | シンプル、忘れやすい |
| 例外 (try/catch) | Java, Python, TS | ハッピーパス分離、シグネチャに非明示 |
| **Result/Either** | Rust, TS, Kotlin | **明示的+型安全 (推奨)** |

### Result パターン (2025年推奨)

- コンパイラが全結果の処理を保証
- Railway-Oriented Programming で関数合成
- TS: neverthrow、Python: Result型、Go: error インターフェース

### 補完パターン

| パターン | 用途 |
|---------|------|
| Circuit Breaker | 外部サービス障害の閾値超過で遮断 |
| Retry with Backoff | 漸増遅延で再試行 |
| Bulkhead | 障害隔離、波及防止 |

---

## 5. 依存性注入 原則

### コンストラクタインジェクション (最推奨)

生成時に全依存関係で完全初期化。

### Composition Root

アプリ内の唯一の場所で依存関係を設定しオブジェクトグラフをインスタンス化。

### ベストプラクティス

1. **インターフェースに対してプログラム** (具象ではなく抽象)
2. **Service Locator を避ける** (依存関係を隠蔽)
3. **サービスを小さく保つ** (注入が多い = SRP 違反の兆候)
4. **状態を持つ静的クラスを避ける** (シングルトンサービスを使用)
5. **依存関係を直接 new しない** (コンストラクタで受け取る)

---

## 6. コード品質メトリクス (2025)

| メトリクス | 説明 |
|-----------|------|
| Defect Density | KLOC あたりのバグ数 |
| Code Churn | モジュール変更率 (高 = 不安定) |
| Cyclomatic Complexity | 分岐の複雑さ |
| Architectural Alignment | 設計パターンへの適合度 |

**AI時代の課題**: 開発者の70%以上がAIコーディングツールを毎週使用、48%がAI生成コードで品質維持が困難と回答。アーキテクチャ適合性レビューの重要性が増大。

---

## 7. 設計アンチパターン

| # | パターン | 問題 | 修正 |
|---|---------|------|------|
| 1 | God Object | 過度の責任集中 | SOLID 適用、専門クラスに分解 |
| 2 | Spaghetti Code | 絡み合った非構造的コード | モジュール化、関心の分離 |
| 3 | Golden Hammer | 1つのツールを全問題に適用 | 問題ごとに適切なツール選択 |
| 4 | Boat Anchor | 未使用コードの放置 | YAGNI、定期的な削除 |
| 5 | Copy-Paste Programming | 理解なしのコード複製 | 再利用可能な関数にリファクタ |
| 6 | Premature Optimization | 影響の小さい部分を最適化 | 計測→プロファイリング→最適化 |
| 7 | Service Locator | 依存関係の隠蔽 | コンストラクタインジェクション |

**Source:** [Clean vs Hexagonal Architecture](https://dev.to/dyarleniber/hexagonal-architecture-and-clean-architecture-with-examples-48oi) · [SOLID 2025 (Ethisys)](https://ethisys.co.uk/2025/06/05/building-resilient-software-why-solid-principles-still-matter-in-2025/) · [CUPID (Dan North)](https://dannorth.net/blog/cupid-for-joyful-coding/) · [API Design 2025](https://dev.to/cryptosandy/api-design-best-practices-in-2025-rest-graphql-and-grpc-2666)
