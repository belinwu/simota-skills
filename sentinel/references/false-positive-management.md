# False Positive Management

> FP 率目標、信頼度スコアリング、差分スキャン、LLM フィルタリング、SARIF 出力

## 1. FP Rate Targets & Impact

### FP 率が開発チームに与える影響

静的解析ツールの生アラートの約 53% は偽陽性（False Positive）であり、対策なしでは開発者のアラート疲れを引き起こす。

| FP 率 | 評価 | 開発者の信頼度 | Finding 解決率 |
|--------|------|---------------|----------------|
| > 40% | 有害 — "more harm than good" | 極低: アラート全体を無視 | < 20% |
| 20-40% | 要改善 | 低: 重要な finding も見落とし | 30-50% |
| 10-20% | 目標水準 | 中〜高: 大半を確認 | 60-80% |
| < 10% | 優秀 | 高: ほぼ全件を確認・対応 | > 85% |

### 核心的問題

```
Alert fatigue の悪循環:
  FP 多発 → 開発者がアラートを無視 → 真の脆弱性も見逃し
  → セキュリティインシデント発生 → ツールへの信頼崩壊
  → SAST 導入が「形骸化」する
```

---

## 2. Framework-Specific Custom Rules

### 組み込みルールが FP を生む理由

標準的な SAST ルールはプロジェクト固有のセキュリティ機構を認識しない:

- カスタム認可ミドルウェア（`requireAuth()`, `checkPermission()` 等）
- アプリケーション固有のサニタイザー関数
- フレームワークの自動 CSRF 保護
- API ゲートウェイでのスロットリング

### プロジェクト固有の抑制ルール

```yaml
rules:
  - id: ignore-sanitized-input
    patterns:
      - pattern: $FUNC($INPUT)
      - pattern-not-inside: |
          if (sanitize($INPUT)) { ... }
    message: "Unsanitized input detected"
    severity: WARNING
```

### Organization-Specific "Memories"

プロジェクト内部のセキュリティポリシーを「記憶」として保存し、スキャン時に参照する:

```
Memories 例:
  - sanitizer_functions: [sanitizeHtml, escapeSQL, purifyInput]
  - auth_middleware: [requireAuth, requireRole, requireApiKey]
  - csrf_protection: "Next.js 組み込みの CSRF 保護を使用"
  - rate_limiting: "API Gateway レイヤーで実施済み"
```

これにより、既知の安全パターンを認識し、無意味なアラートを抑制できる。

---

## 3. Delta/Diff-Based Scanning

### コンセプト

新規・変更コードのみをスキャンし、レガシーコードの既知 FP を排除する。

```
Strategy:
  PR-level: git diff でchanged filesのみスキャン → ノイズ激減
  Periodic: 週次フルスキャンで包括的カバレッジ
  Baseline: 既存findings をsuppressed としてマーク → 新規のみ報告
```

### メリット

- PR レビュー時のノイズを大幅削減し、Sentinel を PR レベルチェックに実用化
- 反復的開発における開発者体験の向上
- 新規導入された脆弱性のみにフォーカス可能

### Sentinel Process との統合

差分スキャンは Process テーブルの **PRIORITIZE** と **SECURE** の間に **FILTER** フェーズとして機能する:

```
SCAN → PRIORITIZE → [FILTER: delta/diff] → SECURE → VERIFY → PRESENT
```

---

## 4. Confidence Scoring Model

### スコアリング要素

| Factor | Weight | Example |
|--------|--------|---------|
| Multi-engine consensus | +30% | 3/3 engines flagged |
| Known vulnerability pattern match | +20% | Exact regex match for AWS key |
| Data flow reachability | +25% | User input reaches sink |
| Framework context mismatch | -20% | Framework auto-sanitizes |
| Test/mock code location | -30% | File in `__tests__/` |

### Multi-Engine Consensus Boost

複数エンジンが同一 finding を検出した場合、信頼度を大幅に引き上げる。Sentinel の Multi-Engine Mode（`references/multi-engine-mode.md`）と直接連携し、Union マージ時にスコアを計算する。

### Confidence Tiers

| Tier | Range | Action |
|------|-------|--------|
| **HIGH** | ≥ 80% | 即時報告 — PRESENT フェーズに含める |
| **MEDIUM** | 50-79% | レビュー用に報告 — 確認を推奨 |
| **LOW** | < 50% | デフォルト抑制 — オプションで表示可能 |

---

## 5. LLM-Based FP Filtering

### ルールベースでは判定できない領域

LLM は以下を評価でき、従来のルールエンジンでは不可能な文脈的判断を行う:

- **Cross-function data flow analysis**: 関数をまたぐデータフローの追跡
- **Upstream input validation**: 上流コードでの入力検証の有無
- **Exploit feasibility**: 攻撃条件が実際に成立するかの評価
- **Framework security guarantees**: フレームワーク固有のセキュリティ保証の理解

### 精度比較

| Approach | Accuracy |
|----------|----------|
| Rules only (SAST) | 35.7% |
| LLM only | 65.5% |
| **LLM + SAST (Hybrid)** | **89.5%** |

ハイブリッドアプローチにより、精度が大幅に向上する。

### トレードオフ

TP（True Positive）検出率を最大化すると FP 誤分類が増加し、逆に FP 抑制を強化すると TP の見逃しリスクが高まる。運用では TP 検出率を優先しつつ、Confidence Scoring で FP をフィルタリングするバランスが重要。

### Sentinel Multi-Engine Mode との統合

LLM エンジンが SAST finding のフィルタ/バリデータとして機能する。Multi-Engine Mode の各エンジン出力に対し、LLM が文脈的妥当性を評価し、Confidence Score を付与する。

---

## 6. SARIF Output Format

### SARIF とは

SARIF（Static Analysis Results Interchange Format）は、静的解析結果の標準化フォーマット。ツール間の互換性を確保し、統一的な結果管理を実現する。

### Sentinel SARIF 出力例

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [{
    "tool": { "driver": { "name": "Sentinel", "version": "1.0" } },
    "results": [{
      "ruleId": "SECRET-001",
      "level": "error",
      "message": { "text": "Hardcoded API key detected" },
      "locations": [{
        "physicalLocation": {
          "artifactLocation": { "uri": "src/config.ts" },
          "region": { "startLine": 42 }
        }
      }],
      "properties": {
        "confidence": 0.92,
        "engines": ["codex", "gemini", "claude"]
      }
    }]
  }]
}
```

### 統合先

- **GitHub Code Scanning**: SARIF アップロードで Security タブに自動表示
- **VS Code SARIF Viewer**: IDE 内でインライン表示
- **CI/CD パイプライン**: 品質ゲートとして SARIF 結果を評価

---

**Source:** [InfoWorld: How Pairing SAST with AI Dramatically Reduces False Positives](https://www.infoworld.com/article/4093079/how-pairing-sast-with-ai-dramatically-reduces-false-positives-in-code-security.html) · [Datadog: Using LLMs to Filter Out False Positives](https://www.datadoghq.com/blog/using-llms-to-filter-out-false-positives/) · [Semgrep: Why SAST Tools Need to Be Customizable](https://semgrep.dev/blog/2024/why-sast-tools-need-to-be-customizable-to-be-useful/) · [Check Point: Avoiding False Positive The Silent SAST Killer](https://blog.checkpoint.com/security/avoiding-false-positive-the-silent-sast-killer/)
