# Supply Chain Security & SCA (Software Composition Analysis)

> サプライチェーンセキュリティ、SBOM、SCA ツール、依存関係管理、CI/CD パイプラインハードニング

## 1. サプライチェーン攻撃の現状（2025-2026）

### 脅威ランドスケープ

```
- 70-90% のアプリケーションがOSSコンポーネントで構成
- サプライチェーン攻撃は自動化・高度化が進行
- パッケージマネージャ経由の悪意あるパッケージ注入が増加
- OWASP Top 10 2025 で A03（新規カテゴリ）に昇格
```

### 攻撃ベクトル

| ベクトル | 手法 | 実例 |
|---------|------|------|
| **Typosquatting** | 類似名パッケージの公開 | `lodash` → `lodahs` |
| **Dependency Confusion** | 内部パッケージ名でパブリック公開 | 2021 Alex Birsan |
| **Slopsquatting** | AI が推奨する存在しないパッケージ名を悪用 | 5-21% の AI 推奨パッケージが実在しない |
| **Compromised Maintainer** | メンテナアカウントの乗っ取り | event-stream (2018) |
| **Build System Attack** | CI/CD パイプラインへの注入 | SolarWinds (2020) |
| **Malicious Update** | 正規パッケージの悪意あるアップデート | ua-parser-js (2021) |

---

## 2. Software Composition Analysis (SCA)

### SCA の役割

```
SCA = オープンソースコンポーネントの特定 + 脆弱性検出 + ライセンスコンプライアンス

従来の SAST が自社コードを分析するのに対し、
SCA はサードパーティコンポーネントのリスクを管理する
```

### 主要 SCA ツール（2026）

| ツール | 特徴 | 無料/有料 |
|--------|------|----------|
| **Snyk** | 開発者フレンドリー、自動修正 PR | Freemium |
| **Dependabot** | GitHub ネイティブ、自動 PR | 無料 |
| **Socket** | サプライチェーン攻撃検出特化 | Freemium |
| **Mend (WhiteSource)** | エンタープライズ向け、ライセンス管理 | 有料 |
| **Endor Labs** | リーチャビリティ分析、ノイズ削減 | 有料 |
| **OWASP Dependency-Check** | 言語非依存、NVD ベース | 無料 |
| **Trivy** | コンテナ + FS + IaC スキャン | 無料 |

### リーチャビリティ分析

```
従来: 脆弱性がある依存関係 → すべてアラート（ノイズ大）
最新: リーチャビリティ分析 → 実際に実行パスにある脆弱性のみ報告

評価要素:
  1. CVSS/EPSS スコア
  2. 実際のコードパスでの到達可能性
  3. エクスプロイト成熟度
  4. コンテキスト要因（ネットワーク露出、特権レベル）
```

---

## 3. SBOM（Software Bill of Materials）

### SBOM の重要性

```
SBOM = ソフトウェアの「成分表」
  - 全依存関係（直接 + 推移的）のリスト
  - バージョン、ライセンス、供給元の記録
  - インシデント発生時の影響範囲特定に必須
  - 規制要件（米国大統領令 14028、EU CRA）で義務化の動き
```

### 標準フォーマット

| フォーマット | 管理団体 | 特徴 |
|------------|---------|------|
| **SPDX** | Linux Foundation | ISO 5962 標準、ライセンス重視 |
| **CycloneDX** | OWASP | セキュリティ重視、VEX 対応 |

### 生成ツール

```bash
# CycloneDX (npm)
npx @cyclonedx/cyclonedx-npm --output-format json > sbom.json

# Syft (汎用)
syft dir:. -o cyclonedx-json > sbom.json

# Trivy
trivy fs . --format cyclonedx --output sbom.json
```

---

## 4. CI/CD パイプラインハードニング

### セキュリティゲート設計

```yaml
# GitHub Actions: 依存関係セキュリティスキャン
name: Supply Chain Security
on: [push, pull_request]

jobs:
  sca-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # 依存関係の脆弱性スキャン
      - name: Run npm audit
        run: npm audit --audit-level=high

      # SBOM 生成
      - name: Generate SBOM
        run: npx @cyclonedx/cyclonedx-npm --output-format json > sbom.json

      # ロックファイル整合性チェック
      - name: Verify lockfile integrity
        run: npm ci --ignore-scripts

      # ライセンスコンプライアンス
      - name: License check
        run: npx license-checker --failOn "GPL-3.0;AGPL-3.0"
```

### パイプラインセキュリティ原則

```
1. 最小権限の原則（CI/CD トークンのスコープ制限）
2. 分離の原則（ビルド環境の隔離）
3. 不変性の原則（ビルドアーティファクトの署名）
4. 検証の原則（サードパーティアクションのハッシュ固定）
5. 監査の原則（パイプライン実行ログの保存）
```

### GitHub Actions セキュリティ

```yaml
# ❌ Anti-pattern: タグ指定（改ざん可能）
- uses: actions/checkout@v4

# ✅ Pattern: SHA ハッシュ固定
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
```

---

## 5. 依存関係管理ベストプラクティス

### ロックファイル管理

```
必須:
  - package-lock.json / yarn.lock / pnpm-lock.yaml をコミット
  - CI で npm ci（ロックファイルに厳密に従う）を使用
  - ロックファイルの差分をレビュー対象にする

禁止:
  - ロックファイルの .gitignore 追加
  - npm install での CI ビルド（非決定的）
```

### 脆弱性管理フロー

```
1. 定期スキャン: 毎日の自動 CVE チェック
2. 優先度付け: CVSS + EPSS + リーチャビリティ
3. 修正: 自動 PR 生成（Dependabot/Snyk）
4. 検証: テストスイートでのリグレッション確認
5. 追跡: 修正の完了と未対応の可視化
```

### Sentinel での実装

```
Sentinel スキャン項目（サプライチェーン）:
  □ npm audit / yarn audit の実行
  □ 既知の CVE を持つパッケージの検出
  □ 未使用パッケージの特定
  □ ロックファイルの存在と整合性確認
  □ プライベートパッケージ名の公開レジストリ重複チェック
  □ postinstall スクリプトの安全性確認
  □ ライセンスコンプライアンスチェック
```

**Source:** [Sonatype: Future-Proofing Software Supply Chain with SCA](https://www.sonatype.com/blog/future-proofing-your-software-supply-chain-with-sca-best-practices) · [Cycode: Top 21 Enterprise SCA Tools 2026](https://cycode.com/blog/top-enterprise-sca-tools/) · [Mend: What Is SCA 2025](https://www.mend.io/blog/software-composition-analysis/) · [Aikido: Top 10 SCA Tools 2026](https://www.aikido.dev/blog/top-10-software-composition-analysis-sca-tools-in-2025) · [Anchore: SCA Overview](https://anchore.com/software-supply-chain-security/software-composition-analysis/)
