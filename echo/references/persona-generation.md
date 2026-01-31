# Echo Persona Generation Workflow

コード/ドキュメントからサービス特化ペルソナを自動生成するワークフロー。

---

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ANALYZE                                   │
│  コード/ドキュメントからユーザー情報を収集                    │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                    EXTRACT                                   │
│  ペルソナ要素（役割、ゴール、ペインポイント）を抽出           │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                    GENERATE                                  │
│  テンプレートに沿ってペルソナを生成                          │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                    SAVE                                      │
│  .agents/personas/{service}/ に保存                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Trigger Methods

### 1. Explicit Command

```
/Echo generate personas
/Echo generate personas for [service-name]
/Echo generate personas from [file-path]
```

### 2. Auto-Suggestion

ペルソナ未定義でレビュー開始時に自動提案:

```yaml
questions:
  - question: "サービス特化ペルソナが見つかりません。生成しますか？"
    header: "Persona"
    options:
      - label: "Yes, generate personas (Recommended)"
        description: "コード/ドキュメントから自動生成"
      - label: "Use Echo base personas"
        description: "標準ペルソナでレビューを続行"
      - label: "I'll provide personas"
        description: "手動でペルソナを定義"
    multiSelect: false
```

---

## Phase 1: ANALYZE

### Analysis Targets

| ファイルタイプ | 抽出対象 | 優先度 |
|---------------|---------|-------|
| `README.md` | ターゲットユーザー、使用シナリオ | High |
| `docs/**/*.md` | ユーザーガイド、チュートリアル | High |
| `src/**/auth*` | 認証フロー、ユーザータイプ | Medium |
| `src/**/user*` | ユーザーモデル、役割定義 | Medium |
| `src/**/checkout*` | 購入フロー、顧客タイプ | Medium |
| `tests/**/*` | テストシナリオ、ユースケース | Medium |
| `*.config.*` | 設定オプション、機能フラグ | Low |
| `package.json` | プロジェクト説明 | Low |

### Analysis Patterns

#### Pattern A: README/Documentation Analysis

```markdown
## 抽出キーワード

### ユーザータイプ
- "for developers", "for teams", "for enterprises"
- "初心者", "上級者", "管理者"
- "customer", "admin", "guest", "member"

### 利用シナリオ
- "when you need to...", "use case:"
- "例えば...", "このような場合に..."

### 技術レベル
- "no coding required" → 低
- "API integration" → 中-高
- "advanced configuration" → 高
```

#### Pattern B: Code Structure Analysis

```markdown
## コード分析

### ユーザーモデル
- `user.role`, `user.type`, `user.tier`
- Enum values for user types
- Permission levels

### フロー分析
- Route definitions → user journeys
- Form components → required inputs
- Error handlers → friction points

### 機能フラグ
- Feature toggles → user segments
- A/B test configs → user variations
```

#### Pattern C: Test Scenario Analysis

```markdown
## テスト分析

### E2E Tests
- Test descriptions → user stories
- Test steps → expected flows
- Assertions → success criteria

### User Stories in Tests
- "as a [role], I want to [action]"
- describe blocks with user context
```

---

## Phase 2: EXTRACT

### Extraction Matrix

| 要素 | ソース | 抽出方法 |
|-----|--------|---------|
| **User Types** | README, user models | ロール/タイプの列挙 |
| **Goals** | Documentation, test descriptions | "want to", "need to" パターン |
| **Context** | Usage examples, tutorials | シナリオ記述 |
| **Pain Points** | Error handling, FAQ | エラーメッセージ、よくある質問 |
| **Tech Level** | Setup complexity, API docs | 必要な前提知識 |
| **Devices** | Responsive code, mobile tests | デバイス対応状況 |

### Extraction Output Format

```yaml
extracted:
  user_types:
    - name: "First-Time Buyer"
      evidence: "README.md line 42: 'perfect for first-time shoppers'"
    - name: "Enterprise Admin"
      evidence: "src/models/user.ts: role enum includes 'admin'"

  goals:
    - goal: "Purchase products quickly"
      type: functional
      evidence: "docs/quick-start.md: 'complete purchase in 3 steps'"

  pain_points:
    - pain: "Complex registration process"
      evidence: "src/auth/register.tsx: 15 required fields"

  context:
    - scenario: "Mobile shopping during commute"
      evidence: "tests/e2e/mobile-checkout.spec.ts"
```

---

## Phase 3: GENERATE

### Generation Rules

1. **最小3ペルソナ**: Primary, Secondary, Edge Case
2. **Echo基本ペルソナとのマッピング**: 必ず対応付け
3. **Emotion Triggers**: サービス固有のトリガーを定義
4. **Testing Focus**: 検証すべきフローを明示

### Persona Priority

| Priority | Type | Description |
|----------|------|-------------|
| P0 | Primary | 主要ターゲットユーザー（必須） |
| P1 | Secondary | 重要な二次ユーザー |
| P2 | Edge | 特殊ケース、アクセシビリティ |

### Generation Prompt Structure

```markdown
## Generate Persona

Based on extracted data:
- User type: [extracted user type]
- Goals: [extracted goals]
- Context: [extracted context]
- Pain points: [extracted pain points]

Generate a persona following `persona-template.md`:
1. Fill all required fields
2. Map to Echo base persona
3. Define 5 emotion triggers
4. List 3 testing focus areas
5. Include source analysis
```

---

## Phase 4: SAVE

### File Naming Convention

```
.agents/personas/{service}/{persona-name}.md

Examples:
.agents/personas/ec-platform/first-time-buyer.md
.agents/personas/ec-platform/power-shopper.md
.agents/personas/admin-dashboard/it-admin.md
```

### Directory Structure

```
.agents/
└── personas/
    ├── README.md              # Usage guide
    └── {service-name}/        # Per-service folder
        ├── primary-user.md
        ├── secondary-user.md
        └── edge-case-user.md
```

### Save Confirmation

```yaml
questions:
  - question: "生成されたペルソナを保存しますか？"
    header: "Save"
    options:
      - label: "Yes, save all (Recommended)"
        description: ".agents/personas/{service}/ に保存"
      - label: "Review and edit first"
        description: "内容を確認してから保存"
      - label: "Save selected only"
        description: "一部のペルソナのみ保存"
    multiSelect: false
```

---

## Service-Specific Review

保存されたペルソナを使用したUXレビューの実行方法。

### Load Personas

```
/Echo review with saved personas
/Echo review [flow] as [persona-name]
```

### Review Process

```
1. LOAD - .agents/personas/{service}/ からペルソナを読み込み
2. SELECT - レビュー対象フローとペルソナを選択
3. WALK - ペルソナ固有のEmotion Triggersを適用
4. SCORE - サービス特化の文脈でスコアリング
5. REPORT - ペルソナ固有の Testing Focus に基づくレポート
```

### Cross-Persona Analysis

複数の保存済みペルソナでフローを比較:

```markdown
### Cross-Persona Matrix: Checkout Flow

| Step | First-Time Buyer | Power Shopper | Enterprise Admin |
|------|-----------------|---------------|------------------|
| 1    | +1              | +2            | +1               |
| 2    | -2              | +1            | -1               |
| 3    | -3              | +2            | -2               |

**Universal Issues**: Step 3 (all personas struggle)
**Segment Issues**: Step 2 (affects First-Time Buyer)
```

---

## Integration with Echo Workflow

### SKILL.md Reference

この機能は `SKILL.md` の以下のセクションと連携:

- **PERSONA LIBRARY**: 基本ペルソナとのマッピング
- **EMOTION SCORING**: カスタムEmotion Triggers
- **ECHO'S DAILY PROCESS**: 拡張されたペルソナ選択

### Journal Integration

ペルソナ生成時の重要な発見は `.agents/echo.md` に記録:

```markdown
## YYYY-MM-DD - Persona Discovery: [Service Name]

**Generated Personas:**
- [Persona 1]: [Key insight]
- [Persona 2]: [Key insight]

**Unexpected Finding:**
[コード分析から発見した予想外のユーザータイプ等]
```

---

## Question Templates

### ON_PERSONA_GENERATION

```yaml
questions:
  - question: "どのソースからペルソナを生成しますか？"
    header: "Source"
    options:
      - label: "Auto-detect (Recommended)"
        description: "README、docs、srcを自動分析"
      - label: "Documentation only"
        description: "ドキュメントファイルのみ分析"
      - label: "Code only"
        description: "ソースコードのみ分析"
      - label: "Specify files"
        description: "分析対象ファイルを指定"
    multiSelect: false
```

### ON_PERSONA_COUNT

```yaml
questions:
  - question: "何体のペルソナを生成しますか？"
    header: "Count"
    options:
      - label: "3 (Recommended)"
        description: "Primary, Secondary, Edge Case"
      - label: "5"
        description: "より詳細なセグメント分け"
      - label: "Auto"
        description: "発見されたユーザータイプ数に応じて"
    multiSelect: false
```

### ON_PERSONA_REVIEW

```yaml
questions:
  - question: "保存済みペルソナでレビューしますか？"
    header: "Persona"
    options:
      - label: "Use saved personas (Recommended)"
        description: ".agents/personas/ から読み込み"
      - label: "Use Echo base personas"
        description: "標準ペルソナを使用"
      - label: "Generate new personas"
        description: "新たにペルソナを生成"
    multiSelect: false
```
