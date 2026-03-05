# Versioning Pitfalls & Breaking Change Management

> SemVer 違反の実態、破壊的変更の検出課題、バージョニング戦略の選択ミス

## 1. Semantic Versioning 7 大落とし穴

| # | 落とし穴 | 問題 | 対策 |
|---|---------|------|------|
| **VP-01** | **MINOR/PATCH での破壊的変更** | 研究: 約半数の破壊的変更が MINOR/PATCH で導入される | 破壊的変更の自動検出ツール導入 · API 差分チェック |
| **VP-02** | **破壊的変更の過小評価** | 「影響範囲が小さい」と判断 → PATCH で出す → 下流で障害 | 破壊的変更の定義を明文化 · 影響分析を必須化 |
| **VP-03** | **0.x.y の長期使用** | 「まだ安定版じゃない」で 0.x に留まり続ける → ユーザーに不安定さを常時伝達 | 実用に耐えるなら 1.0.0 をリリース · 0.x は本当の実験期間のみ |
| **VP-04** | **MAJOR バンプ恐怖症** | 破壊的変更を避けるためにワークアラウンド蓄積 → 技術的負債 | MAJOR は健全な進化の証 · 定期的な Breaking Change ウィンドウ |
| **VP-05** | **情報の過剰圧縮** | MAJOR.MINOR.PATCH に変更の性質・影響範囲・深刻度を詰め込む → 不十分 | CHANGELOG と組み合わせて詳細を補完 |
| **VP-06** | **CD 環境との摩擦** | 継続的デプロイで毎コミットのバージョン付けが煩雑 → 形骸化 | CalVer や自動バージョニング · CD では CHANGELOG が主役 |
| **VP-07** | **Pre-release ラベルの乱用** | alpha/beta/rc を長期間使い続ける → ユーザーが「永遠のベータ」と認識 | Pre-release に期限を設定 · rc は最長 2 週間 |

---

## 2. 破壊的変更の検出課題

### 研究に基づく知見

```
Maven リポジトリ研究 (IEEE):
  - 全リリースの約 1/3 が少なくとも 1 つの破壊的変更を含む
  - MINOR/MAJOR に関わらず同比率 → バージョン番号が安定性を示さない
  - ライブラリのユーザーは SemVer を信頼して依存管理 → 裏切られる

ACM ISSTA 2023:
  - Semantic Breaking Change: API シグネチャは同一だが意味が変わる
  - 静的解析で検出困難 → 内部メソッドの意味変更は追跡不能
  - テストが最も信頼性の高い検出手段
```

### 破壊的変更の 3 分類

| 分類 | 検出容易性 | 例 |
|------|----------|------|
| **Syntactic Breaking** | 高（静的解析可） | API 削除、引数変更、戻り値型変更 |
| **Behavioral Breaking** | 中（テスト必要） | 同じ API で挙動が変化、エラー条件変更 |
| **Semantic Breaking** | 低（人間の判断必要） | パフォーマンス特性変化、暗黙の契約違反 |

### 破壊的変更の定義チェックリスト

```
以下を「破壊的変更」として定義（チームで合意）:
  □ パブリック API の削除または名前変更
  □ 必須パラメータの追加
  □ 戻り値の型変更
  □ デフォルト値の変更
  □ エラー/例外の種類変更
  □ 既存の挙動の変更（同じ入力で異なる出力）
  □ 最低要件の変更（Node.js バージョン等）
  □ 設定ファイル形式の変更
  □ データベーススキーマの非互換変更
```

---

## 3. バージョニング戦略の選択ミス

### 戦略とプロジェクトタイプのミスマッチ

| プロジェクトタイプ | 推奨 | アンチパターン | 理由 |
|-----------------|------|-------------|------|
| **OSS ライブラリ** | SemVer | CalVer | ユーザーが互換性情報を必要とする |
| **SaaS（CD）** | CalVer or 自動採番 | SemVer 厳密適用 | 毎デプロイにバージョン付けが煩雑 |
| **モバイルアプリ** | SemVer + ビルド番号 | CalVer | ストア審査で MAJOR.MINOR 必要 |
| **内部ツール** | CalVer | SemVer | 互換性管理が不要 · 日付で十分 |
| **API** | URI バージョン + SemVer | SemVer のみ | API バージョンとリリースバージョンを分離 |

### CalVer フォーマット

```
YYYY.MM.DD      → 2024.01.15（日次リリース向け）
YYYY.MM.MICRO   → 2024.01.3（月次リリース向け）
YY.MM           → 24.01（四半期リリース向け）
YYMM.BUILD      → 2401.0009（CD 向け、月次ビルドカウンター）
```

---

## 4. 依存関係とバージョニング

### 依存管理の落とし穴

```
問題:
  1. ワイドレンジ指定（>=1.0.0）→ 将来の破壊的変更を自動取り込み
  2. 完全固定（=1.0.0）→ セキュリティパッチが適用されない
  3. Lock ファイル未コミット → 環境間でバージョン不一致
  4. 推移的依存の SemVer 違反 → 直接依存は安全でも間接依存で破壊

推奨:
  - キャレット指定（^1.2.3）を基本 → MINOR/PATCH の自動更新
  - Lock ファイルを必ずコミット
  - 定期的な依存更新（Renovate/Dependabot）
  - 破壊的変更のある依存は手動更新
```

---

## 5. Launch との連携

```
Launch での活用:
  1. バージョン決定時に VP-01〜07 のチェックを適用
  2. 破壊的変更チェックリストで MAJOR バンプ要否を判断
  3. プロジェクトタイプに応じたバージョニング戦略を推奨
  4. Pre-release ラベルの期限管理

品質ゲート:
  - MINOR/PATCH に破壊的変更を含む場合 → MAJOR バンプを提案（VP-01 防止）
  - 0.x.y が 6 ヶ月超 → 1.0.0 リリースを提案（VP-03 防止）
  - Pre-release (alpha/beta) が 1 ヶ月超 → 安定版リリースまたは中止を提案（VP-07 防止）
  - SemVer を CD プロジェクトに適用 → CalVer を代替案として提示（VP-06 防止）
```

**Source:** [IEEE: Semantic Versioning versus Breaking Changes (Maven Study)](https://ieeexplore.ieee.org/document/6975655/) · [ACM ISSTA 2023: Understanding Breaking Changes in the Wild](https://dl.acm.org/doi/10.1145/3597926.3598147) · [Surfing the Cloud: Semantic Versioning Anti-Pattern](https://surfingthe.cloud/semantic-versioning-anti-pattern/) · [SemVer 2.0.0 Specification](https://semver.org/) · [DEV.to: Rethinking API Versioning](https://dev.to/ralphsebastian/rethinking-api-versioning-why-full-semantic-versioning-might-be-an-anti-pattern-for-your-api-3h8b)
