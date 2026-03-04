# OWASP Top 10 2025: Updates & Migration Guide

> 2021→2025 の変更点、新カテゴリ、削除/統合カテゴリ、移行ガイド

## 1. OWASP Top 10 2025 完全リスト

| Rank | Category | 2021 比較 |
|------|----------|----------|
| **A01** | Broken Access Control | 維持（SSRF 統合） |
| **A02** | Security Misconfiguration | #5→#2 に上昇 |
| **A03** | Software Supply Chain Failures | **新規**（旧 A06 拡張） |
| **A04** | Cryptographic Failures | #2→#4 に下降 |
| **A05** | Injection | #3→#5 に下降 |
| **A06** | Insecure Design | #4→#6 に下降 |
| **A07** | Authentication Failures | 維持 |
| **A08** | Software or Data Integrity Failures | 維持 |
| **A09** | Logging & Alerting Failures | 維持（名称変更） |
| **A10** | Mishandling of Exceptional Conditions | **新規** |

---

## 2. 主要変更点

### 統合: SSRF → Broken Access Control (A01)

```
2021: A10 SSRF（独立カテゴリ）
2025: A01 Broken Access Control に統合
理由: マイクロサービス化でサービスレベルとユーザーレベルの
      アクセス境界が曖昧化 → 統一的なアクセス制御として扱う
```

### 昇格: Security Misconfiguration (A02)

```
2021: #5 → 2025: #2
要因: 719,000+ の CWE マッピング
  - クラウド設定ミス（S3 公開、セキュリティグループ開放）
  - デフォルト設定の放置
  - 冗長なエラーメッセージ
  - 不要な機能の有効化
```

### 新規: Software Supply Chain Failures (A03)

```
旧 A06「Vulnerable and Outdated Components」を大幅拡張
コミュニティ投票 #1（50% の回答者）、平均発生率 5.19%

対象範囲:
  - 廃止/未メンテナンスのコンポーネント
  - 推移的依存関係の未管理
  - 安全でない CI/CD パイプライン
  - 変更追跡の不備
  - SBOM の欠如

実例: SolarWinds, Bybit, GlassWorm
```

### 新規: Mishandling of Exceptional Conditions (A10)

```
24 の CWE を包含する新カテゴリ

対象:
  - 不適切なエラーハンドリング（CWE-209: 機密情報漏洩）
  - 不完全なエラー回復
  - Failing Open シナリオ（CWE-636）
  - 一貫性のない例外処理

結果: クラッシュ、ロジック欠陥、データ破損、DoS
```

---

## 3. Sentinel スキャンマッピング（2021→2025）

| 2021 スキャン項目 | 2025 更新 |
|-----------------|----------|
| シークレット検出 | 変更なし（A07 Authentication Failures） |
| SQLi/XSS 検出 | A05 Injection（LLM Injection は別途追跡） |
| 入力バリデーション | A05 + A10 の両方でカバー |
| セキュリティヘッダー | A02 Security Misconfiguration に含む |
| 依存関係 CVE | **A03 Supply Chain Failures に拡張** |
| CSP 設定 | A02 Security Misconfiguration |
| **新規追加すべき** | **サプライチェーン全体、エラーハンドリング** |

---

## 4. カテゴリ別スキャンチェックリスト

### A01: Broken Access Control (SSRF 統合)

```
□ サーバーサイドのアクセス制御（deny-by-default）
□ CORS の適切な設定
□ IDOR（Insecure Direct Object Reference）の検出
□ 権限昇格パスの検証
□ SSRF: URL バリデーション + ホワイトリスト
□ SSRF: 内部 IP（169.254.x.x, 10.x.x.x）へのリクエスト防止
□ JWT トークンの検証（署名、有効期限、発行者）
```

### A02: Security Misconfiguration

```
□ デフォルト認証情報の使用検出
□ 不要な HTTP メソッドの有効化
□ ディレクトリリスティングの無効化
□ スタックトレースの本番公開
□ HSTS、X-Frame-Options、X-Content-Type-Options
□ クラウド設定（S3 バケットポリシー、IAM）
□ デバッグモードの本番無効化
```

### A03: Supply Chain Failures

```
□ SBOM の生成と管理（SPDX / CycloneDX）
□ 推移的依存関係の CVE チェック
□ 未使用パッケージの検出
□ ライセンスコンプライアンス
□ CI/CD パイプラインのセキュリティ
□ アーティファクト署名の検証
□ ロックファイルの整合性チェック
```

### A10: Mishandling of Exceptional Conditions

```
□ 空の catch ブロック検出
□ エラーメッセージでの機密情報漏洩
□ Failing Open パターンの検出
□ 未処理の Promise rejection
□ 不完全なエラーリカバリーフロー
□ null/undefined の安全でないアクセス
□ リソースリーク（ファイルハンドル、DB接続）
```

---

## 5. 哲学的シフト

```
2021: 症状ベース（例: Sensitive Data Exposure）
2025: 根本原因ベース（例: Cryptographic Failures）

2021: コンポーネントの脆弱性に焦点
2025: サプライチェーン全体のセキュリティに拡張

2021: SSRF を独立カテゴリとして扱う
2025: アクセス制御の一部として統合的に扱う

2021: エラーハンドリングは暗黙的
2025: 例外処理を独立カテゴリとして明示的に扱う
```

**Source:** [OWASP Top 10:2025](https://owasp.org/Top10/2025/) · [Orca Security: OWASP Top 10 2025 Key Changes](https://orca.security/resources/blog/owasp-top-10-2025-key-changes/) · [Semgrep: OWASP Top 10 2025 What's New](https://semgrep.dev/blog/2026/owasp-top-10-2025-whats-new/) · [GitLab: OWASP Top 10 2025](https://about.gitlab.com/blog/2025-owasp-top-10-whats-changed-and-why-it-matters/)
