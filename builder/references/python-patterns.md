# Python Best Practices

> Python 3.12+ 型ヒント、async/await、プロジェクト構成 (uv)、pytest、Pydantic、アンチパターン

## 1. Python 3.12+ 新機能

### PEP 695: 新ジェネリクス構文

```python
# Python 3.12+: TypeVar 不要
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()

# 型エイリアス
type Vector = list[float]
type Matrix = list[Vector]

# バウンド型
class Container[T: Mapping]: ...

# デコレータ ParamSpec
def decorator[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return func(*args, **kwargs)
    return wrapper
```

### Exception Groups (Python 3.11+)

```python
try:
    raise ExceptionGroup("errors", [
        FileNotFoundError("config.yaml"),
        ValueError("Invalid port"),
    ])
except* FileNotFoundError as eg:
    for err in eg.exceptions: print(f"File: {err}")
except* ValueError as eg:
    for err in eg.exceptions: print(f"Val: {err}")
```

### Python 3.13 実験的機能

- **Free-threaded (no-GIL)**: `python3.13t` で実行（実験的）
- **JIT コンパイラ**: `PYTHON_JIT=1` で有効化（最大30%高速化）

---

## 2. プロジェクト構成 & uv

### 推奨構成

```
my-app/
├── pyproject.toml
├── uv.lock              # バージョン管理に含める
├── .python-version
├── src/
│   └── my_app/
│       ├── __init__.py
│       ├── py.typed       # PEP 561 (ライブラリの場合)
│       └── main.py
└── tests/
    ├── conftest.py
    └── test_main.py
```

### pyproject.toml 推奨設定

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["httpx>=0.27", "pydantic>=2.0"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.24", "mypy>=1.10", "ruff>=0.5"]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "UP", "B", "I", "SIM", "RUF"]

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

### uv コマンド

| 操作 | コマンド |
|------|---------|
| 依存追加 | `uv add httpx` |
| 開発依存追加 | `uv add --dev pytest ruff mypy` |
| 実行 | `uv run python src/my_app/main.py` |
| 環境同期 | `uv sync` |

**重要**: `uv.lock` は必ず VCS に含める。`pip install` は使わない。

---

## 3. async/await パターン

### TaskGroup (gather より推奨)

```python
async def process_batch(items: list[str]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_item(item)) for item in items]
    return [t.result() for t in tasks]
```

TaskGroup の利点: 例外時の自動キャンセル、ExceptionGroup で全エラー集約、リソースリーク防止。

### Semaphore で並行数制限

```python
SEM = asyncio.Semaphore(10)

async def fetch_with_limit(client: httpx.AsyncClient, url: str) -> str:
    async with SEM:
        response = await client.get(url)
        return response.text
```

### ブロッキング関数の統合

```python
async def run_blocking(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)
```

---

## 4. テスト (pytest)

### パラメータ化テスト

```python
@pytest.mark.parametrize("input_val, expected", [
    ("hello", "HELLO"),
    ("", ""),
    pytest.param("mixed", "MIXED", id="mixed_case"),
])
def test_to_upper(input_val: str, expected: str):
    assert to_upper(input_val) == expected
```

### Fixture スコープ

| スコープ | 用途 |
|---------|------|
| `function` | テスト毎リセット (デフォルト) |
| `module` | ファイル単位共有 |
| `session` | 全体共有 (DB接続等) |

### 非同期テスト

```python
# asyncio_mode = "auto" なら @pytest.mark.asyncio 不要
async def test_fetch_user():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/users/1")
    assert resp.status_code == 200
```

### プロパティベーステスト (Hypothesis)

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_preserves(xs: list[int]):
    result = sorted(xs)
    assert Counter(result) == Counter(xs)
```

**モック**: `autospec=True` でシグネチャ不一致を検出。`AsyncMock` で非同期モック。

---

## 5. 型安全性

### mypy vs pyright

| 観点 | mypy | pyright |
|------|------|---------|
| 速度 | 中 | 高速 |
| IDE | プラグイン | VS Code ネイティブ |
| 推奨 | CI (`--strict`) | 開発時フィードバック |

### Pydantic バリデーション

```python
from pydantic import BaseModel, Field, model_validator

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    email: str

    @model_validator(mode="after")
    def validate_email(self) -> "UserCreate":
        if not self.email.endswith("@example.com"):
            raise ValueError("Invalid domain")
        return self
```

### 段階的型付け

```python
# Level 3: Protocol + ジェネリクス
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict[str, object]: ...

def save[T: Serializable](item: T) -> None:
    data = item.to_dict()
    db.insert(data)
```

---

## 6. アンチパターン

| # | パターン | 問題 | 修正 |
|---|---------|------|------|
| 1 | ミュータブルデフォルト引数 | `def f(x=[])` でリスト共有 | `None` をデフォルトにして内部で初期化 |
| 2 | `is` で値比較 | CPython インターンに依存 | 値比較は `==`、`is` は None のみ |
| 3 | with 文なしのファイル操作 | 例外時にリソースリーク | `with open(...) as f:` |
| 4 | 不統一な戻り値型 | `User` or `"not found"` 混在 | `Optional[User]` or 例外 |
| 5 | 内包表記の副作用利用 | `[print(x) for x in items]` | `for x in items: print(x)` |
| 6 | `from module import *` | 名前空間汚染 | 明示的インポート |
| 7 | await 忘れ | coroutine was never awaited | 必ず `await` する |
| 8 | イベントループ内ブロッキング | `time.sleep()` が全体をブロック | `await asyncio.sleep()` |

---

## 7. 推奨スタック (2025)

| 用途 | 推奨 |
|------|------|
| パッケージ管理 | **uv** |
| リンター/フォーマッター | **Ruff** |
| 型チェック | **mypy** (CI) + **pyright** (IDE) |
| テスト | **pytest** + hypothesis |
| バリデーション | **Pydantic v2** |
| Python バージョン | **3.12** (安定 + 新ジェネリクス) |

**Source:** [Python 3.12 What's New](https://docs.python.org/3/whatsnew/3.12.html) · [Real Python uv Guide](https://realpython.com/python-uv/) · [Ruff Configuration](https://docs.astral.sh/ruff/configuration/) · [DeepSource Python Anti-Patterns](https://deepsource.com/blog/8-new-python-antipatterns)
