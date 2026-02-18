# Domain Patterns

Matrix の7つの組み込みドメインパターン。各ドメインの典型的な軸定義・制約例・ユースケースを定義。

---

## 1. test — テスト検証

**目的:** ソフトウェアの動作をあらゆる環境・条件の組み合わせで検証する

### 典型的な軸

| 軸 | 代表的な値 | priority |
|----|----------|----------|
| browser | Chrome, Firefox, Safari, Edge | high |
| os | Windows, macOS, Linux, iOS, Android | high |
| viewport | desktop, tablet, mobile | medium |
| auth_state | logged_in, anonymous, expired_session | high |
| data_state | empty, populated, edge_case | medium |
| network | wifi, cellular, slow_3g, offline | low |
| locale | ja, en, zh-TW, ko | low |

### 典型的な制約

```yaml
constraints:
  exclude:
    - {browser: Safari, os: Windows}
    - {browser: IE, os: macOS}
    - {browser: Chrome, os: iOS}  # iOS上ではChrome=WebKit
  conditional:
    - if: {network: offline}
      then: {auth_state: logged_in}  # オフライン時は事前ログイン必須
```

### 後続エージェント
- **Voyager** — E2E テスト実装
- **Radar** — ユニット/統合テスト追加
- **Siege** — 負荷条件を含む場合

### ユースケース例
```
「ログイン画面を Chrome/Firefox/Safari × Windows/macOS ×
  日本語/英語でテストしたい」
→ 3×2×2=12 組み合わせ → Pairwise後: 4件
```

---

## 2. load — 負荷テスト

**目的:** システムがどの負荷条件の組み合わせで限界に達するかを特定する

### 典型的な軸

| 軸 | 代表的な値 | priority |
|----|----------|----------|
| concurrent_users | 10, 100, 500, 1000, 5000 | high |
| data_volume | small(1KB), medium(100KB), large(10MB) | high |
| endpoint | /api/users, /api/search, /api/checkout | high |
| duration | 1min, 5min, 30min, 1hour | medium |
| ramp_pattern | constant, gradual, spike, wave | medium |
| region | ap-northeast-1, us-east-1, eu-west-1 | low |

### 典型的な制約

```yaml
constraints:
  conditional:
    - if: {concurrent_users: 5000}
      then: {duration: "1min"}  # 最大負荷は短時間のみ
  exclude:
    - {data_volume: large, concurrent_users: 5000}  # OOM リスク回避
```

### 後続エージェント
- **Siege** — 負荷テスト実行
- **Beacon** — SLO/SLI との照合
- **Bolt** — ボトルネック修正

---

## 3. deploy — デプロイ戦略

**目的:** 複数の環境・リージョン・バージョンへの安全なデプロイ順序を設計する

### 典型的な軸

| 軸 | 代表的な値 | priority |
|----|----------|----------|
| environment | dev, staging, production | high |
| region | ap-northeast-1, us-east-1, eu-west-1 | high |
| version | v1.5.0, v1.5.1, v2.0.0-rc | high |
| traffic_split | 0%, 1%, 10%, 50%, 100% | medium |
| rollout_strategy | blue-green, canary, rolling | medium |
| feature_flags | enabled, disabled | low |

### 典型的な制約

```yaml
constraints:
  conditional:
    - if: {environment: dev}
      then: {traffic_split: "100%"}
    - if: {rollout_strategy: blue-green}
      then: {traffic_split: "0% or 100%"}  # B/G は中間値なし
  require:
    - {environment: staging}  # staging は必ず含める
```

### 推奨順序（デプロイ順）
1. dev → staging → production（環境）
2. ap-northeast-1 → us-east-1 → eu-west-1（地理的に身近な順）
3. 1% → 10% → 50% → 100%（カナリアリリース）

### 後続エージェント
- **Scaffold** — IaC 実行
- **Gear** — CI/CD パイプライン更新
- **Beacon** — デプロイ後の観測設定

---

## 4. ux — UX検証

**目的:** 多様なペルソナ・デバイス・シナリオの組み合わせでUX問題を発見する

### 典型的な軸

| 軸 | 代表的な値 | priority |
|----|----------|----------|
| persona | beginner, intermediate, expert, senior, accessibility_user | high |
| device | desktop, tablet, mobile | high |
| scenario | first_visit, return_visit, task_completion, error_recovery | high |
| locale | ja, en, zh, ko, ar (RTL) | medium |
| accessibility | none, screen_reader, keyboard_only, high_contrast | medium |
| connection | fast, slow, offline | low |

### 典型的な制約

```yaml
constraints:
  conditional:
    - if: {persona: accessibility_user}
      then: {accessibility: screen_reader or keyboard_only}
    - if: {locale: ar}
      then: {accessibility: none}  # RTL は別途テスト
```

### 後続エージェント
- **Cast** — ペルソナ詳細定義
- **Echo** — UX フロー検証実行
- **Researcher** — インタビュー設計との連携

---

## 5. risk — リスク評価

**目的:** 脅威×資産×影響度の組み合わせを優先順位付きで評価する

### 典型的な軸

| 軸 | 代表的な値 | priority |
|----|----------|----------|
| threat | XSS, SQLi, CSRF, SSRF, XXE, RCE, PathTraversal | high |
| attack_surface | Web_UI, REST_API, GraphQL, WebSocket, File_Upload | high |
| auth_level | anonymous, authenticated, privileged, admin | high |
| data_sensitivity | public, internal, confidential, restricted, PII | high |
| impact | low, medium, high, critical | medium |

### リスクスコア計算

```
リスクスコア = 脅威スコア(1-10) × 露出度(1-5) × 認証バイパス容易性(1-3)

分類:
  Critical: 7.0-10.0 → P0 即時対応
  High:     4.0-6.9  → P1 今週中
  Medium:   2.0-3.9  → P2 今月中
  Low:      0.0-1.9  → P3 次スプリント
```

### 後続エージェント
- **Triage** — 影響範囲の特定
- **Sentinel** — 静的解析で検証
- **Probe** — 動的テストで検証
- **Scout** — 根本原因調査

---

## 6. experiment — A/B実験

**目的:** 複数の実験変数×ユーザーセグメントの組み合わせを体系的に設計する

### 典型的な軸

| 軸 | 代表的な値 | priority |
|----|----------|----------|
| variable | button_color, cta_text, layout, price_display | high |
| user_segment | new_users, returning_users, premium, free | high |
| exposure_rate | 1%, 5%, 10%, 50% | medium |
| duration | 1week, 2weeks, 1month | medium |
| metric | CTR, CVR, retention, ARPU | high |

### 後続エージェント
- **Experiment** — 仮説文書・サンプルサイズ計算・フィーチャーフラグ実装
- **Pulse** — KPIトラッキング設計

---

## 7. compat — 互換性検証

**目的:** ライブラリ・バージョン・実行環境の組み合わせで互換性を検証する

### 典型的な軸

| 軸 | 代表的な値 | priority |
|----|----------|----------|
| runtime_version | Node.js 18, 20, 22 / Python 3.9, 3.10, 3.12 | high |
| dependency_version | react@17, react@18, react@19 | high |
| os | ubuntu-22.04, ubuntu-24.04, macos-13, macos-14 | medium |
| architecture | x86_64, arm64 | medium |
| feature | core, experimental, deprecated | medium |

### 典型的な制約

```yaml
constraints:
  exclude:
    - {runtime_version: "Node.js 18", dependency_version: "next@15"}  # 非対応
  require:
    - {runtime_version: "Node.js 20"}  # LTS は必ず含める
```

### 後続エージェント
- **Horizon** — 非推奨バージョンの特定・モダナイゼーション提案
- **Builder** — 互換性修正の実装

---

## カスタムドメイン（custom）

上記7パターン以外の場合。Matrix が軸から自動的にドメインを推測できない場合に使用。

```yaml
matrix:
  domain: custom
  description: "採用プロセスの組み合わせ評価"
  axes:
    - name: role
      values: [Engineer, Designer, PM]
    - name: interview_stage
      values: [screening, technical, culture_fit, offer]
    - name: interviewer_count
      values: [1, 2, 3]
```

ドメインが `custom` の場合、後続エージェントの推薦は行わない。ユーザーが手動で指定する。
