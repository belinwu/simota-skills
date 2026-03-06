# OWASP Top 10 (2025) Checklist & Audit Templates

OWASP Top 10:2025 に基づくセキュリティ監査チェックリストとレポートテンプレート。

## 1. OWASP Top 10 2025 Complete List

| Rank | Category | 2021 からの変更 |
|------|----------|----------------|
| **A01** | Broken Access Control | 維持（SSRF を統合） |
| **A02** | Security Misconfiguration | #5→#2 に上昇 |
| **A03** | Software Supply Chain Failures | **新規**（旧 A06 拡張） |
| **A04** | Cryptographic Failures | #2→#4 に下降 |
| **A05** | Injection | #3→#5（Prompt Injection 追加） |
| **A06** | Insecure Design | #4→#6 に下降 |
| **A07** | Authentication Failures | 維持 |
| **A08** | Software or Data Integrity Failures | 維持 |
| **A09** | Logging & Alerting Failures | 維持（名称変更） |
| **A10** | Mishandling of Exceptional Conditions | **新規** |

## 2. Category Checklists (A01-A10)

### A01: Broken Access Control (SSRF 統合)

SSRF は 2025 でこのカテゴリに統合。アクセス制御を統一的に扱う。

```
□ 全エンドポイントで認可チェック（deny-by-default）
□ API レート制限・CORS の適切な設定
□ ディレクトリリスティングの無効化
□ JWT/セッション検証（署名、有効期限、発行者）
□ IDOR の検出・権限昇格パスの検証
□ SSRF: URL バリデーション + ホワイトリスト
□ SSRF: 内部 IP（169.254.x.x, 10.x.x.x）へのリクエスト防止
```

### A02: Security Misconfiguration

クラウド設定ミス増加により #2 に昇格。719,000+ CWE マッピング。

```
□ セキュリティヘッダー（CSP, HSTS, X-Frame-Options, X-Content-Type-Options）
□ エラーメッセージ・スタックトレースで内部情報を漏洩しない
□ 不要な機能・HTTP メソッドの無効化
□ デフォルト認証情報の変更・デバッグモードの本番無効化
□ クラウド設定強化（S3 バケットポリシー、IAM、セキュリティグループ）
```

### A03: Software Supply Chain Failures (新規)

旧 A06 をサプライチェーン全体に拡張。詳細は `supply-chain-security.md` 参照。

```
□ SBOM の生成と管理（SPDX / CycloneDX）
□ 推移的依存関係の CVE チェック・未使用パッケージの検出
□ ライセンスコンプライアンス
□ CI/CD パイプラインのセキュリティ
□ アーティファクト署名の検証・ロックファイルの整合性チェック
```

### A04: Cryptographic Failures

```
□ 機密データの保存時暗号化・TLS 1.2+ による転送時暗号化
□ パスワードハッシュに強力なアルゴリズム（bcrypt, argon2）
□ 非推奨アルゴリズムの排除（MD5, SHA1）
□ シークレットがソースコードに含まれていない・適切な鍵管理
```

### A05: Injection

Prompt Injection が対象範囲に追加。LLM 統合システムも考慮。

```
□ SQL のパラメータ化クエリ・全ユーザー入力のバリデーション
□ XSS 防止の出力エンコーディング
□ コマンド / LDAP / NoSQL インジェクション防止
□ LLM Prompt Injection の考慮（AI 統合がある場合）
```

### A06: Insecure Design

```
□ 脅威モデリングの実施・セキュリティ要件の定義
□ セキュアデザインパターンの使用
□ ビジネスロジック悪用の防止・リソース集約型操作のレート制限
```

### A07: Authentication Failures

```
□ 多要素認証（MFA）の提供・弱いパスワードの防止
□ ブルートフォース保護・セキュアなパスワードリカバリー
□ セッション管理の安全性
```

### A08: Software or Data Integrity Failures

```
□ CI/CD パイプラインの保護・コード署名の実装
□ 依存関係の整合性検証・デシリアライゼーション入力のバリデーション
```

### A09: Logging & Alerting Failures

「Monitoring」→「Alerting」に名称変更。受動的監視から能動的アラートへ。

```
□ ログイン/アクセス失敗のログ記録・セキュリティイベントの監視
□ ログの改ざん防止
□ 不審なアクティビティへのアラート設定
```

### A10: Mishandling of Exceptional Conditions (新規)

24 CWE を包含。不適切な例外処理がクラッシュ、データ破損、DoS を引き起こす。

```
□ 空の catch ブロック検出
□ エラーメッセージでの機密情報漏洩（CWE-209）
□ Failing Open パターンの検出（CWE-636）
□ 未処理の Promise rejection・不完全なエラーリカバリー
□ null/undefined の安全でないアクセス
□ リソースリーク（ファイルハンドル、DB 接続）
```

## 3. Security Audit Report Template

### Executive Summary

| Metric | Value |
|--------|-------|
| Scan Date | YYYY-MM-DD |
| Files Scanned | X |
| Critical / High / Medium / Low | X / X / X / X |
| OWASP 2025 Coverage | X/10 |

### Risk Matrix

| Severity | Count | Action |
|----------|-------|--------|
| CRITICAL | X | 即時対応 |
| HIGH | X | 24 時間以内に修正 |
| MEDIUM | X | 1 週間以内に修正 |
| LOW | X | 計画的に対応 |

### Finding Template

```markdown
#### [SEVERITY-NNN] Finding Title
- **File**: `src/path/file.js:42`
- **OWASP 2025**: A0X - Category Name
- **Risk**: 悪用された場合の影響
- **Evidence**: `code snippet showing the issue`
- **Remediation**: 修正手順
- **Status**: Open / In Progress / Fixed
```

### Recommendations

1. **Immediate**: Critical / High の全件修正
2. **Short-term**: 脆弱な依存関係の更新
3. **Long-term**: CI/CD へのセキュリティテスト統合

## 4. 2021 → 2025 Migration Summary

| 2021 | 2025 | 変更 |
|------|------|------|
| A01 Broken Access Control | A01 同名 | SSRF（旧 A10）統合 |
| A02 Cryptographic Failures | A04 に下降 | - |
| A03 Injection | A05 に下降 | Prompt Injection 追加 |
| A04 Insecure Design | A06 に下降 | - |
| A05 Security Misconfiguration | A02 に上昇 | クラウド設定ミス重視 |
| A06 Vulnerable Components | A03 Supply Chain | サプライチェーン全体に拡張 |
| A07-A08 | A07-A08 維持 | - |
| A09 Logging & Monitoring | A09 Logging & Alerting | 名称変更 |
| A10 SSRF | _(A01 に統合)_ | 独立カテゴリ廃止 |
| _(なし)_ | A10 Exceptional Conditions | 24 CWE 包含の新規 |

### 哲学的シフト

- **症状ベース → 根本原因ベース**: Sensitive Data Exposure → Cryptographic Failures
- **コンポーネント単体 → サプライチェーン全体**: CI/CD・SBOM・署名まで包含
- **SSRF 独立 → アクセス制御統合**: マイクロサービス化による境界の統一管理
- **エラー処理の暗黙化 → 明示化**: 例外処理を独立カテゴリとして扱う

## 5. Sentinel Scan Mapping

| スキャン項目 | OWASP 2025 | 備考 |
|------------|-----------|------|
| シークレット検出 | A07 Auth Failures | 変更なし |
| SQLi/XSS 検出 | A05 Injection | LLM Injection は別途 |
| 入力バリデーション | A05 + A10 | Injection + Exceptional Conditions |
| セキュリティヘッダー | A02 Misconfiguration | CSP 含む |
| 依存関係 CVE | A03 Supply Chain | サプライチェーン全体に拡張 |
| **追加推奨** | **A03 + A10** | **サプライチェーン監査、エラーハンドリング** |

---

**Source:** [OWASP Top 10:2025](https://owasp.org/Top10/2025/) | [GitLab OWASP 2025 Analysis](https://about.gitlab.com/blog/2025-owasp-top-10-whats-changed-and-why-it-matters/)
