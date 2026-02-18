# Optimization Algorithms

Matrix が使用する最適化アルゴリズムの詳細実装ガイド。

---

## アルゴリズム選択フロー

```
入力受信
  │
  ├─ max_combinations 指定あり → コスト制約付き最適化
  │
  ├─ invalid pairs が全体の30%超 → 制約付きPairwise
  │
  ├─ 全軸の値数が均一（例: 全て3値） → 直交配列
  │
  ├─ 安全クリティカル要件あり → CIT (3-way以上)
  │
  ├─ 軸数が2以下 → 全組み合わせ（最適化不要）
  │
  └─ その他 → Pairwise (2-way)
```

---

## Pairwise アルゴリズム（IPOG法）

### IPOG (In-Parameter-Order Generation) 手順

```
入力: パラメータリスト P = {p1, p2, ..., pk}、各値リスト V(pi)
出力: テストケースセット T

手順:
1. T ← p1 の全値を1行ずつ追加（縦列を1列で初期化）
2. i = 2 から k まで繰り返す:
   a. U ← (p1...pi-1) × V(pi) の全2-wayペアセット
   b. 既存行を横方向に拡張（pi の値を貪欲に割り当て）
      - 各行に pi の値を割り当てる際、最も多くの未カバーペアをカバーする値を選ぶ
   c. U に残った未カバーペアがあれば新しい行を追加
3. return T
```

### Pythonによる概念実装

```python
from itertools import product

def pairwise(parameters: dict) -> list[dict]:
    """
    parameters: {"browser": ["Chrome","Firefox","Safari"], "os": ["Win","Mac"]}
    returns: 最小カバレッジセット
    """
    param_names = list(parameters.keys())
    param_values = list(parameters.values())

    # 全ペアの生成
    uncovered_pairs = set()
    for i in range(len(param_names)):
        for j in range(i+1, len(param_names)):
            for vi in param_values[i]:
                for vj in param_values[j]:
                    uncovered_pairs.add((param_names[i], vi, param_names[j], vj))

    test_cases = []

    while uncovered_pairs:
        # 最も多くの未カバーペアをカバーする組み合わせを選択
        best_case = None
        best_count = -1

        for combo in product(*param_values):
            case = dict(zip(param_names, combo))
            covered = sum(
                1 for (n1, v1, n2, v2) in uncovered_pairs
                if case[n1] == v1 and case[n2] == v2
            )
            if covered > best_count:
                best_count = covered
                best_case = case

        test_cases.append(best_case)
        uncovered_pairs -= {
            (n1, v1, n2, v2)
            for (n1, v1, n2, v2) in uncovered_pairs
            if best_case[n1] == v1 and best_case[n2] == v2
        }

    return test_cases
```

### 計算量
- 全組み合わせ列挙: O(∏|Vi|)
- IPOG: O(k² × N) — k=軸数、N=生成行数
- 実用上: 軸数20、各軸値数10程度まで現実的な時間で完了

---

## 直交配列の構築

### L9(3^4) の構築手順

3値×4軸の場合、9行の直交配列を使用:

```python
# L9(3^4) — 3水準4因子、9行
L9 = [
    [0, 0, 0, 0],
    [0, 1, 1, 1],
    [0, 2, 2, 2],
    [1, 0, 1, 2],
    [1, 1, 2, 0],
    [1, 2, 0, 1],
    [2, 0, 2, 1],
    [2, 1, 0, 2],
    [2, 2, 1, 0],
]

def apply_orthogonal_array(oa: list, parameters: dict) -> list[dict]:
    param_names = list(parameters.keys())
    param_values = list(parameters.values())

    result = []
    for row in oa:
        case = {}
        for col, name in enumerate(param_names):
            idx = row[col] % len(param_values[col])
            case[name] = param_values[col][idx]
        result.append(case)
    return result
```

### 既製直交配列の参照表

| 軸数(k) | 値数(v) | 推奨配列 | 行数(N) |
|---------|---------|---------|---------|
| 2-3 | 2 | L4 | 4 |
| 4-7 | 2 | L8 | 8 |
| 2-4 | 3 | L9 | 9 |
| 8-15 | 2 | L16 | 16 |
| 5-13 | 3 | L27 | 27 |
| 4-5 | 4 | L16 | 16 |

---

## 制約付き最適化

### invalid pair 処理

```python
def pairwise_with_constraints(parameters: dict, exclude: list[dict]) -> list[dict]:
    """
    exclude: [{"browser": "Safari", "os": "Windows"}, ...]
    """
    # 1. 除外ルールを適用した有効組み合わせ空間を生成
    all_combos = list(product(*parameters.values()))
    param_names = list(parameters.keys())

    def is_excluded(combo):
        case = dict(zip(param_names, combo))
        for rule in exclude:
            if all(case.get(k) == v for k, v in rule.items()):
                return True
        return False

    valid_combos = [c for c in all_combos if not is_excluded(c)]

    # 2. 有効な組み合わせ空間に対してPairwiseを適用
    # （以降はpairwise()と同様）
    ...
```

### max_combinations 制約

```python
def pairwise_with_budget(parameters: dict, max_n: int) -> list[dict]:
    """
    max_combinations が指定された場合の優先度付き選択
    """
    all_cases = pairwise(parameters)  # 通常のPairwiseで最小セットを生成

    if len(all_cases) <= max_n:
        return all_cases  # 予算内に収まる場合はそのまま

    # 予算オーバーの場合: カバレッジの高い順に max_n 件を選択
    scored = []
    uncovered = compute_all_pairs(parameters)
    for case in all_cases:
        coverage = count_covered_pairs(case, uncovered)
        scored.append((coverage, case))

    scored.sort(reverse=True)
    selected = [case for _, case in scored[:max_n]]

    # カバレッジレポート: 何%のペアをカバーできているか
    achieved_coverage = compute_coverage_rate(selected, parameters)
    return selected, achieved_coverage
```

---

## 優先度スコアリング

実行セットを生成後、優先度を付けるスコアリング。

```python
def prioritize(
    test_cases: list[dict],
    priority_axes: dict[str, int],  # {"browser": 3, "os": 2, "auth": 1}
    risk_values: dict[str, int]      # {"Chrome": 2, "Safari": 3}
) -> list[dict]:
    """
    priority_axes: 軸の重要度スコア（大きいほど重要）
    risk_values: 特定の値のリスクスコア
    """
    scored = []
    for case in test_cases:
        score = 0
        for axis, value in case.items():
            axis_weight = priority_axes.get(axis, 1)
            value_risk = risk_values.get(value, 1)
            score += axis_weight * value_risk
        scored.append((score, case))

    scored.sort(reverse=True)
    result = []
    for score, case in scored:
        priority = "HIGH" if score >= 6 else "MEDIUM" if score >= 3 else "LOW"
        result.append({**case, "_priority": priority, "_score": score})

    return result
```

---

## カバレッジ検証

最適化後のカバレッジを確認するアルゴリズム。

```python
def verify_coverage(
    test_cases: list[dict],
    parameters: dict,
    t_way: int = 2
) -> dict:
    """
    t_way=2: 2-wayカバレッジ検証（Pairwise保証）
    t_way=3: 3-wayカバレッジ検証
    """
    from itertools import combinations as combs

    param_names = list(parameters.keys())
    total_pairs = 0
    covered_pairs = 0
    missing_pairs = []

    for axes in combs(range(len(param_names)), t_way):
        axis_names = [param_names[i] for i in axes]
        axis_values = [parameters[n] for n in axis_names]

        for combo in product(*axis_values):
            pair = dict(zip(axis_names, combo))
            total_pairs += 1

            is_covered = any(
                all(case.get(k) == v for k, v in pair.items())
                for case in test_cases
            )

            if is_covered:
                covered_pairs += 1
            else:
                missing_pairs.append(pair)

    return {
        "total": total_pairs,
        "covered": covered_pairs,
        "rate": covered_pairs / total_pairs,
        "missing": missing_pairs
    }
```

---

## パフォーマンスガイドライン

| 軸数 | 各軸の値数 | 推奨手法 | 処理時間目安 |
|------|---------|---------|-----------|
| 2-5 | 2-5 | Pairwise | <1秒 |
| 6-10 | 2-5 | Pairwise | 1-10秒 |
| 10-15 | 2-10 | Pairwise or OA | 10-60秒 |
| 15以上 | 2-5 | 直交配列推奨 | 状況依存 |
| 制約が複雑 | any | SAT solver | 状況依存 |

**10軸以上・制約複雑な場合:** ACTS, pict, CAen等の専用ツールを推奨。MatrixはそれらのInput仕様を生成する役割を担う。
