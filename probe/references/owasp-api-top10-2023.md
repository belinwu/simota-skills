# OWASP API Security Top 10 2023 Testing Guide

> OWASP API Security Top 10 2023 の各リスクに対するテスト戦略、攻撃ベクトル、検出手法

## 1. OWASP API Security Top 10 2023 概要

| # | リスク | 2019 版との比較 | 深刻度 |
|---|-------|---------------|--------|
| **API1** | Broken Object Level Authorization (BOLA) | 変更なし（#1 維持） | CRITICAL |
| **API2** | Broken Authentication | 変更なし（#2 維持） | CRITICAL |
| **API3** | Broken Object Property Level Authorization (BOPLA) | 新規（API3:2019 + API6:2019 統合） | HIGH |
| **API4** | Unrestricted Resource Consumption | 改名（旧: Lack of Resources & Rate Limiting） | HIGH |
| **API5** | Broken Function Level Authorization (BFLA) | 変更なし（#5 維持） | HIGH |
| **API6** | Unrestricted Access to Sensitive Business Flows | 新規 | HIGH |
| **API7** | Server Side Request Forgery (SSRF) | 新規 | HIGH |
| **API8** | Security Misconfiguration | 順位変更（旧 #7） | MEDIUM-HIGH |
| **API9** | Improper Inventory Management | 順位変更（旧 #9） | MEDIUM |
| **API10** | Unsafe Consumption of APIs | 新規 | MEDIUM |

---

## 2. 各リスクのテスト戦略

### API1: Broken Object Level Authorization (BOLA)

```
攻撃ベクトル:
  - オブジェクト ID の操作（/api/users/123 → /api/users/124）
  - UUID の推測・列挙
  - 他ユーザーのリソースへのアクセス

テスト手法:
  □ 異なるユーザートークンで同一リソースにアクセス
  □ オブジェクト ID のインクリメンタル列挙
  □ GUID/UUID の推測可能性テスト
  □ 削除済みリソースへのアクセス試行
  □ バッチ操作での権限チェック

検出ツール: ZAP (手動) + カスタムスクリプト
統計: 全 API 攻撃の約 40% を占める最大の脅威

防御策:
  - 全データアクセス関数で認可チェック実装
  - 推測困難な ID（UUID v4）の使用
  - アクセスパターンのログ記録・監視
```

### API2: Broken Authentication

```
攻撃ベクトル:
  - クレデンシャルスタッフィング
  - ブルートフォース攻撃
  - 認証トークンの盗取・再利用
  - セッション固定攻撃

テスト手法:
  □ パスワードポリシーの検証（弱いパスワードの受け入れ）
  □ アカウントロックアウトメカニズムのテスト
  □ JWT 署名検証（alg: none 攻撃）
  □ トークン有効期限の検証
  □ MFA バイパスの試行
  □ パスワードリセットフローの検証

検出ツール: ZAP + Hydra + カスタムスクリプト

防御策:
  - 強力なパスワードポリシー + MFA
  - セッション管理の適切な実装
  - トークンの暗号化（通信時・保管時）
```

### API3: Broken Object Property Level Authorization (BOPLA)

```
攻撃ベクトル:
  - Mass Assignment: リクエストに追加プロパティを注入
  - Excessive Data Exposure: レスポンスに不要なデータ

テスト手法:
  □ PUT/PATCH リクエストに管理者プロパティを追加（role, isAdmin）
  □ レスポンスの余剰データチェック（パスワードハッシュ、内部 ID）
  □ フィルタリングのバイパス試行
  □ GraphQL の過剰なフィールド返却テスト

検出ツール: ZAP + Burp Suite + 手動テスト

防御策:
  - プロパティレベルのアクセス制御
  - 必要最小限のプロパティのみ露出
  - 許可リストによるリクエスト/レスポンスフィルタリング
```

### API4: Unrestricted Resource Consumption

```
攻撃ベクトル:
  - 大量リクエスト送信（DoS）
  - 巨大ペイロード送信
  - ファイルアップロードサイズ制限の欠如
  - 高コスト操作の反復呼び出し

テスト手法:
  □ レート制限の存在・有効性テスト
  □ ペイロードサイズ制限テスト
  □ ページネーション制限テスト（?limit=999999）
  □ 並行リクエストテスト
  □ リソース集中型エンドポイントの特定

検出ツール: Nuclei (rate-limit テンプレート) + カスタムスクリプト

防御策:
  - エンドポイントごとのレート制限
  - ペイロードサイズ制限
  - リソース使用量の監視・アラート
```

### API5: Broken Function Level Authorization (BFLA)

```
攻撃ベクトル:
  - 管理者エンドポイントへの非認可アクセス
  - HTTP メソッドの変更（GET → DELETE）
  - URL パスの操作（/api/users → /api/admin/users）

テスト手法:
  □ 一般ユーザートークンで管理者 API にアクセス
  □ HTTP メソッドの変更テスト
  □ エンドポイント列挙（/admin, /internal, /debug）
  □ ロールベースのアクセス制御の網羅的テスト
  □ 水平・垂直権限昇格テスト

検出ツール: ZAP + 手動テスト

防御策:
  - 全関数呼び出しに認可チェック
  - 最小権限の原則
  - ゼロトラストモデル
```

### API6: Unrestricted Access to Sensitive Business Flows

```
攻撃ベクトル:
  - Bot による自動購入（買い占め）
  - 自動アカウント作成
  - API 経由の大量データスクレイピング
  - ビジネスフロー悪用（クーポン乱用、レビュー操作）

テスト手法:
  □ ビジネスクリティカルフローの特定
  □ 自動化による大量操作テスト
  □ CAPTCHA・Bot 検出メカニズムの検証
  □ レート制限のビジネスフロー単位での検証
  □ 異常パターン検出メカニズムのテスト

検出ツール: カスタムスクリプト + 手動テスト

防御策:
  - ビジネスフローごとのレート制限
  - Bot 検出メカニズム
  - 異常行動パターンの検出・ブロック
```

### API7: Server Side Request Forgery (SSRF)

```
攻撃ベクトル:
  - 内部サービスへのアクセス（http://localhost, http://169.254.169.254）
  - クラウドメタデータエンドポイントアクセス
  - 内部ネットワークスキャン
  - ファイアウォールバイパス

テスト手法:
  □ URL パラメータの内部アドレス注入
  □ クラウドメタデータ URL テスト（AWS/GCP/Azure）
  □ DNS リバインディング試行
  □ プロトコルスキーム変更（file://, gopher://）
  □ リダイレクトチェーンを利用したバイパス

検出ツール: ZAP + Nuclei + 手動テスト
検出容易性: SAST で検出可能 + DAST で高信頼度確認

防御策:
  - ユーザー入力の厳密な検証・サニタイズ
  - 許可リストによる URL 制限
  - ネットワークセグメンテーション
```

### API8: Security Misconfiguration

```
攻撃ベクトル:
  - デフォルト認証情報
  - 不要な機能の有効化
  - CORS の過剰な許可
  - 詳細なエラーメッセージ
  - 古いソフトウェアバージョン

テスト手法:
  □ セキュリティヘッダーの検証
  □ CORS 設定のテスト
  □ エラーレスポンスの情報漏洩チェック
  □ デフォルト認証情報テスト
  □ 不要なエンドポイントの特定
  □ TLS 設定の検証

検出ツール: Nuclei + ZAP (passive scan) + testssl.sh

防御策:
  - 設定管理プロセスの確立
  - 定期的なアップデート
  - 自動化された設定チェック
```

### API9: Improper Inventory Management

```
攻撃ベクトル:
  - 旧バージョン API への攻撃（/api/v1 vs /api/v2）
  - 未文書化エンドポイントの発見
  - 開発・ステージング環境の露出
  - シャドウ API の悪用

テスト手法:
  □ API バージョン列挙
  □ 未文書化エンドポイントの発見
  □ 非本番環境の露出チェック
  □ 古い API バージョンのセキュリティ検証
  □ OpenAPI 仕様と実装の差分チェック

検出ツール: Nuclei + 手動偵察

防御策:
  - API インベントリの自動発見・監視
  - 非推奨 API の計画的廃止
  - 全バージョンの文書化
```

### API10: Unsafe Consumption of APIs

```
攻撃ベクトル:
  - サードパーティ API レスポンスの改ざん
  - 中間者攻撃（暗号化なし通信）
  - サードパーティ API 経由のインジェクション
  - 信頼されたサードパーティの侵害

テスト手法:
  □ サードパーティ API レスポンスの検証有無チェック
  □ HTTPS 強制の確認
  □ API レスポンスのサニタイズ検証
  □ タイムアウト・エラーハンドリングの検証
  □ サードパーティ API 障害時のフォールバック動作

検出ツール: 手動レビュー + SAST

防御策:
  - サードパーティデータもユーザー入力と同等に検証
  - HTTPS 強制
  - レスポンスの適切な検証・サニタイズ
```

---

## 3. テスト優先順位マトリクス

| リスク | 自動検出 | 手動必須 | CI/CD 統合 | 優先度 |
|-------|---------|---------|-----------|-------|
| API1 (BOLA) | 困難 | 必須 | △ | 最高 |
| API2 (Auth) | 部分的 | 必須 | ○ | 最高 |
| API3 (BOPLA) | 部分的 | 必須 | △ | 高 |
| API4 (Resource) | 容易 | 推奨 | ○ | 高 |
| API5 (BFLA) | 困難 | 必須 | △ | 高 |
| API6 (Business) | 困難 | 必須 | × | 高 |
| API7 (SSRF) | 容易 | 推奨 | ○ | 高 |
| API8 (Misconfig) | 容易 | 推奨 | ○ | 中 |
| API9 (Inventory) | 部分的 | 必須 | △ | 中 |
| API10 (Unsafe) | 困難 | 必須 | × | 中 |

---

## 4. Probe との連携

```
Probe での活用:
  1. Plan フェーズで API1〜10 のテスト計画を策定
  2. Scan フェーズで自動検出可能なリスク（API4/7/8）を先行スキャン
  3. Validate フェーズで手動必須リスク（API1/5/6）を重点検証
  4. Report フェーズで OWASP API Top 10 カテゴリでの分類表示

品質ゲート:
  - BOLA テスト未実施 → 警告（API 攻撃の 40% をカバーする最重要項目）
  - 認証テスト未実施 → セキュリティゲートブロック
  - SSRF テスト未実施（URL パラメータあり）→ 警告
  - レート制限テスト未実施 → 警告
```

**Source:** [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [CyCognito: OWASP API Top 10 2023](https://www.cycognito.com/learn/api-security/owasp-api-security/) · [Veracode: Breaking Down OWASP Top 10 API Security 2023](https://www.veracode.com/blog/breaking-down-owasp-top-10-api-security-risks-2023-what-changed-2019/) · [Salt Security: OWASP API Top 10 Explained](https://salt.security/blog/owasp-api-security-top-10-explained) · [StackHawk: Understanding 2023 OWASP API Top 10](https://www.stackhawk.com/blog/understanding-the-2023-owasp-top-10-api-security-risks/)
