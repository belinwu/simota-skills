# Advanced Reproduction & Triage

> タイムトラベルデバッグ、決定論的リプレイ、フレイキーテスト、RICE/ICE スコアリング、バグトリアージ自動化

## 1. タイムトラベルデバッグ

### 概要

プログラム実行を記録し、逆方向にステップ実行できるデバッガ。「結果から原因をたどる」プロセスを実現。

### ツール比較

| ツール | 対象 | オーバーヘッド | 特徴 |
|--------|------|------------|------|
| **rr** | Linux (C/C++/Rust) | ~1.2倍 | 軽量記録、逆方向実行、ウォッチポイント |
| **Replay.io** | ブラウザ (JS/TS) | ~3% | 決定論的ブラウザ、DevTools で検査 |
| **Pernosco** | Linux (rr 拡張) | — | クラウド型、協調分析 |

### rr の使用フロー

```bash
# 1. 実行を記録
rr record ./program

# 2. 記録をリプレイ（逆方向ステップ可能）
rr replay

# 3. GDB コマンドが使用可能
(rr) reverse-continue   # 逆方向に実行
(rr) reverse-step       # 逆方向にステップ
(rr) watch -l var       # ハードウェアウォッチポイント
```

### Replay.io のフロー

```
1. テスト実行を記録（Replay ブラウザ使用）
2. 記録をアップロード
3. チーム全員が DevTools で検査可能（ローカル再現不要）
4. 任意の時点にジャンプして状態を確認
```

### Scout での活用

- REPRODUCE フェーズで再現困難なバグに対して rr/Replay.io を推奨
- Race Condition の確定的な再現
- 「Heisenbug」（観測すると消えるバグ）の捕捉

---

## 2. フレイキーテスト対策

### 実態（2025年データ）

- 開発者の **59%** が定期的に遭遇
- 開発時間の **8%以上** が対応に費やされる
- 推定コスト: **5.12億ドル/年**（業界全体）

### 主要な原因と対策

| 原因 | 対策 |
|------|------|
| テスト間の状態共有 | 各テストを自己完結型に（セットアップ/ティアダウン） |
| 固定 `sleep` 間隔 | 条件ベースの明示的待機（ポーリング or イベント待ち） |
| ランダムデータ依存 | シード固定 or 決定論的テストデータ |
| 現在時刻依存 | 時刻のモック/固定 |
| 外部依存 | モック/スタブ/コンテナ化 |
| Race Condition | rr + Debug AI パイプラインで自動検出 |

### フレイキーテスト管理戦略

```
Detection → Quarantine → Root Cause → Fix → Monitor
```

1. **検出**: CI で再実行して不安定なテストを特定
2. **隔離**: フレイキーテストを quarantine スイートに移動
3. **根本原因**: rr 記録 or ストレステストで原因特定
4. **修正**: 非決定論的要素を排除
5. **監視**: 修正後のフレイク率を追跡

---

## 3. バグ重要度の精密分類

### Severity vs Priority

| 概念 | 定義 | 判断基準 |
|------|------|---------|
| **Severity** | 技術的な深刻度（「どれだけ悪いか」） | データ損失、機能停止、ワークアラウンド有無 |
| **Priority** | 修正の緊急度（「いつ修正すべきか」） | ビジネス影響、影響ユーザー数、SLA |

**重要**: 高 Severity ≠ 必ず高 Priority。低 Severity でも多数ユーザーに影響 → 高 Priority。

### 拡張 Severity 分類

| レベル | 定義 | SLA 目安 |
|--------|------|---------|
| **Blocker** | ソフトウェア使用/テスト続行不可 | 即時対応 |
| **Critical** | 主要機能が完全に動作しない | 4時間以内 |
| **Major** | 重要機能に影響、ワークアラウンドあり | 24時間以内 |
| **Minor** | ユーザー体験への影響は限定的 | 次スプリント |
| **Trivial** | 機能に影響なし（誤字脱字等） | バックログ |

---

## 4. RICE / ICE スコアリング

### RICE スコア（Intercom 考案）

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

| 要素 | 説明 | スケール |
|------|------|---------|
| **Reach** | 影響を受けるユーザー/トランザクション数 | 実数 |
| **Impact** | 個々のユーザーへの影響度 | 3=大, 2=高, 1=中, 0.5=低, 0.25=最小 |
| **Confidence** | 見積りの確信度 | 100%=高, 80%=中, 50%=低 |
| **Effort** | 修正に必要な人月 | 実数 |

### ICE スコア（Sean Ellis 考案）

```
ICE Score = Impact × Confidence × Ease
```

| 要素 | 説明 | スケール |
|------|------|---------|
| **Impact** | 修正による影響度 | 1-10 |
| **Confidence** | 見積りの確信度 | 1-10 |
| **Ease** | 修正の容易さ（Effort の逆） | 1-10 |

### RICE vs ICE の使い分け

| 場面 | 推奨 |
|------|------|
| データが豊富で精密な優先順位が必要 | RICE |
| 迅速な判断が必要 | ICE |
| 影響ユーザー数が重要な判断基準 | RICE（Reach あり） |
| 修正コストの比較が重要 | RICE（Effort あり） |

---

## 5. バグトリアージのアンチパターン

| # | アンチパターン | 対策 |
|---|-------------|------|
| 1 | Severity と Priority の混同 | 2軸で独立に評価 |
| 2 | 「声の大きい人」のバグを優先 | 定量フレームワーク（RICE/ICE）を使用 |
| 3 | すべてを Critical に分類 | 分類のインフレを防ぐ明確な基準 |
| 4 | ビジネスコンテキスト無視 | 収益影響、ユーザー影響数を考慮 |
| 5 | 修正コスト（Effort）の未考慮 | RICE スコアで Effort を明示的に評価 |
| 6 | トリアージプロセスの欠如 | 定期的なバグトリアージ会議を設定 |

---

## 6. LLM によるトリアージ自動化（2025年）

### CASEY アプローチ

LLM ベースのセキュリティ脆弱性トリアージ自動化:

| 指標 | 精度 |
|------|------|
| CWE 自動特定 | 68% |
| 重要度特定 | 73.6% |
| 合計精度 | 51.2% |

**Scout への示唆**: TRIAGE フェーズで LLM による初期分類を活用し、人間が検証・修正。

---

## 7. Scout の ASSESS フェーズ強化

### 推奨評価項目

```markdown
## Impact Assessment

### Severity: [Blocker|Critical|Major|Minor|Trivial]
### Priority: [P0|P1|P2|P3]

### Quantitative Impact
- 影響ユーザー数: ___
- 影響トランザクション/日: ___
- 収益影響（推定）: ___
- SLA 違反リスク: [Yes/No]

### RICE Score
- Reach: ___
- Impact: ___
- Confidence: ___
- Effort (推定): ___
- **Score: ___**

### Workaround
- 有無: [Yes/No]
- 説明: ___
```

**Source:** [Bug Severity Levels - QATestLab](https://blog.qatestlab.com/2015/03/10/software-bugs-severity-levels/) · [RICE Scoring - ProductPlan](https://www.productplan.com/glossary/rice-scoring-model/) · [ICE Scoring - SaaS Funnel Lab](https://www.saasfunnellab.com/essay/ice-score-prioritization-method/) · [rr Project](https://rr-project.org/) · [Replay.io](https://www.replay.io/) · [Flaky Tests - Reproto](https://reproto.com/how-to-fix-flaky-tests-in-2025-a-complete-guide-to-detection-prevention-and-management/) · [LLM Triage - arXiv](https://arxiv.org/pdf/2501.18908)
