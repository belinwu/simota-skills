# Input Schema

Matrix が受け付ける入力フォーマットの仕様。自然言語・YAML・JSON の3種類をサポート。

---

## 1. 自然言語入力

最も簡便な入力方法。Matrix が自動的に軸・値・制約・ドメインを解析する。

### パターン認識

| 表現 | 解析結果 |
|------|---------|
| `A/B/C × X/Y` | 軸1=[A,B,C], 軸2=[X,Y] |
| `AとBとCを、XとYで` | 軸1=[A,B,C], 軸2=[X,Y] |
| `AまたはB、XまたはY` | 軸1=[A,B], 軸2=[X,Y] |
| `AはXと組み合わせない` | constraint: exclude {A, X} |
| `テストしたい` | domain: test |
| `デプロイしたい` | domain: deploy |
| `リスク評価したい` | domain: risk |

### 自然言語入力例

```
「Chrome/Firefox/Safari を Windows/macOS/Linux で、
  ログイン済み/未ログインの状態でテストしたい。
  ただし Safari は Windows と組み合わせない。」
```

**解析結果:**
```yaml
domain: test
axes:
  - name: browser
    values: [Chrome, Firefox, Safari]
  - name: os
    values: [Windows, macOS, Linux]
  - name: auth
    values: [logged_in, anonymous]
constraints:
  exclude:
    - {browser: Safari, os: Windows}
optimization: pairwise
```

---

## 2. YAML 入力（推奨）

明示的で再利用しやすい標準フォーマット。

### 完全スキーマ

```yaml
matrix:
  # 必須: ドメイン識別子
  domain: test | load | deploy | ux | risk | experiment | compat | custom

  # 必須: 軸の定義
  axes:
    - name: <軸名>              # 必須: 英数字・アンダースコア
      values: [<値1>, <値2>, ...] # 必須: 2値以上
      priority: high | medium | low  # 任意: 優先度（デフォルト: medium）
      weight: <数値>             # 任意: 重み付けスコア（1-10）

  # 任意: 制約定義
  constraints:
    exclude:                    # 除外する組み合わせ
      - {<軸名>: <値>, <軸名>: <値>}
    conditional:                # 条件付き制約
      - if: {<軸名>: <値>}
        then: {<軸名>: <値>}
    require:                    # 必ず含める組み合わせ
      - {<軸名>: <値>, <軸名>: <値>}

  # 任意: 最適化設定
  optimization: pairwise | orthogonal | cit | full | custom
  t_way: 2 | 3 | 4             # CIT使用時のt値（デフォルト: 2）
  max_combinations: <数値>     # 最大実行数の上限

  # 任意: メタデータ
  name: <マトリクス名>
  description: <説明文>
  author: <作成者>
  tags: [<タグ1>, <タグ2>]
```

### YAML 入力例集

#### テストマトリクス
```yaml
matrix:
  domain: test
  name: login-flow-matrix
  axes:
    - name: browser
      values: [Chrome, Firefox, Safari, Edge]
      priority: high
    - name: os
      values: [Windows, macOS, iOS, Android]
    - name: auth_method
      values: [password, oauth_google, oauth_github, sso]
    - name: network
      values: [wifi, cellular, offline]
  constraints:
    exclude:
      - {browser: Safari, os: Windows}
      - {browser: Edge, os: iOS}
      - {auth_method: sso, network: offline}
  optimization: pairwise
  max_combinations: 20
```

#### デプロイマトリクス
```yaml
matrix:
  domain: deploy
  axes:
    - name: environment
      values: [staging, production]
      priority: high
    - name: region
      values: [us-east-1, ap-northeast-1, eu-west-1]
    - name: version
      values: [v1.5.0, v1.5.1]
    - name: traffic_split
      values: ["0%", "10%", "50%", "100%"]
  constraints:
    conditional:
      - if: {environment: staging}
        then: {traffic_split: "100%"}
  optimization: full
```

#### リスクマトリクス
```yaml
matrix:
  domain: risk
  axes:
    - name: threat
      values: [XSS, SQLi, CSRF, SSRF, XXE]
      priority: high
    - name: attack_surface
      values: [Web, API, Mobile, CLI]
    - name: auth_level
      values: [anonymous, authenticated, admin]
    - name: data_sensitivity
      values: [public, internal, confidential, restricted]
  optimization: pairwise
```

---

## 3. JSON 入力（プログラム連携向け）

API・スクリプト・他エージェントからの自動連携に使用。

### JSONスキーマ

```json
{
  "$schema": "matrix-v1",
  "matrix": {
    "domain": "string",
    "name": "string",
    "axes": [
      {
        "name": "string",
        "values": ["string"],
        "priority": "high|medium|low",
        "weight": "number"
      }
    ],
    "constraints": {
      "exclude": [{"key": "value"}],
      "conditional": [
        {"if": {"key": "value"}, "then": {"key": "value"}}
      ],
      "require": [{"key": "value"}]
    },
    "optimization": "pairwise|orthogonal|cit|full",
    "max_combinations": "number"
  }
}
```

### JSON 入力例

```json
{
  "matrix": {
    "domain": "ux",
    "name": "onboarding-ux-matrix",
    "axes": [
      {
        "name": "persona",
        "values": ["beginner", "intermediate", "expert"],
        "priority": "high"
      },
      {
        "name": "device",
        "values": ["desktop", "tablet", "mobile"]
      },
      {
        "name": "scenario",
        "values": ["first_visit", "return_visit", "referred"]
      },
      {
        "name": "locale",
        "values": ["ja", "en", "zh"]
      }
    ],
    "optimization": "pairwise"
  }
}
```

---

## 4. テーブル入力（既存資料の変換）

Markdown テーブルや既存のスプレッドシートからの入力も受け付ける。

```markdown
| Axis     | Values                        |
|----------|-------------------------------|
| browser  | Chrome, Firefox, Safari       |
| os       | Windows, macOS                |
| language | Japanese, English, Chinese    |
```

Matrix がこれを YAML スキーマに変換して処理する。

---

## 5. 入力バリデーション

Matrix は入力受信後、以下のバリデーションを実行する。

| チェック項目 | エラー時の対応 |
|------------|-------------|
| 軸が1個以下 | エラー: 最低2軸が必要 |
| 軸に値が1個以下 | エラー: 各軸に最低2値が必要 |
| 軸名が重複 | エラー: 軸名は一意である必要がある |
| 制約が矛盾（全組み合わせを除外） | 警告 + ON_CONSTRAINT_UNKNOWN trigger |
| 軸数が6以上 | 警告 + ON_AXIS_OVERFLOW trigger |
| max_combinations が全組み合わせより大 | 警告: 最適化の意味がない |

---

## 6. 軸の優先度（priority）

最適化時に優先度の高い軸を最初に配置し、カバレッジを最大化する。

| priority | 意味 | 使いどころ |
|----------|------|----------|
| `high` | 必ず全値をカバー | ビジネスクリティカルな軸 |
| `medium` | Pairwiseで網羅（デフォルト） | 通常の軸 |
| `low` | 最小限のカバレッジで可 | 補助的な軸 |

```yaml
# 例: ブラウザは必ず全種類テスト、言語は最低限でよい
axes:
  - name: browser
    values: [Chrome, Firefox, Safari, Edge]
    priority: high
  - name: language
    values: [ja, en, zh, ko, de, fr]
    priority: low
```
