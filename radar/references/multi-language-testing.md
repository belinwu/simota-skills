# Multi-Language Testing

Testing patterns and tools for Python, Go, Rust, and Java projects.

---

## Language Detection

| Indicator | Language | Test Framework | Coverage Tool |
|-----------|----------|----------------|---------------|
| `pytest.ini` / `pyproject.toml` [tool.pytest] | Python | pytest | coverage.py / pytest-cov |
| `go.mod` | Go | testing (stdlib) | go test -cover |
| `Cargo.toml` | Rust | cargo test (built-in) | cargo-tarpaulin / llvm-cov |
| `pom.xml` / `build.gradle` | Java | JUnit 5 | JaCoCo |
| `vitest.config.*` / `jest.config.*` | TypeScript/JS | Vitest / Jest | v8 / istanbul |

---

## Python (pytest)

### Basic Test

```python
# test_calculator.py
import pytest
from calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        assert self.calc.add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert self.calc.add(-1, -1) == -2

    def test_divide_by_zero_raises_error(self):
# ...
```

### Parametrize (Edge Cases)

```python
@pytest.mark.parametrize("input_val,expected", [
    ("", True),           # empty string
    ("  ", True),         # whitespace only
    (None, True),         # None
    ("hello", False),     # valid string
    ("  hello  ", False), # string with spaces
])
def test_is_blank(input_val, expected):
    assert is_blank(input_val) == expected
```

### Fixtures

```python
@pytest.fixture
def db_session():
    """Provide a clean database session for each test."""
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def sample_user(db_session):
    """Create a sample user in the test database."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user
# ...
```

### Async Tests

```python
import pytest
import httpx

@pytest.mark.asyncio
async def test_fetch_user():
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
```

### Mocking

```python
from unittest.mock import patch, MagicMock

def test_send_email_on_signup(mocker):
    # mocker is from pytest-mock
    mock_send = mocker.patch("services.email.send_welcome_email")

    create_user(name="Test", email="test@example.com")

    mock_send.assert_called_once_with("test@example.com")
```

### Coverage

```bash
# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80

# Per-file coverage
pytest --cov=src --cov-report=term-missing
```

### Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/migrations/*"]

# ...
```

---

## Go (testing)

### Basic Test

```go
// calculator_test.go
package calculator

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

// Table-driven tests (Go idiom)
func TestAdd_TableDriven(t *testing.T) {
    tests := []struct {
// ...
```

### With testify

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/suite"
)

func TestCalculator(t *testing.T) {
    assert.Equal(t, 5, Add(2, 3))
    assert.NotNil(t, result)
    assert.ErrorIs(t, err, ErrNotFound)
}

// require stops test on failure (useful for setup)
func TestUserService(t *testing.T) {
// ...
```

### Test Suite

```go
type UserServiceSuite struct {
    suite.Suite
    db      *sql.DB
    service *UserService
}

func (s *UserServiceSuite) SetupTest() {
    s.db = setupTestDB()
    s.service = NewUserService(s.db)
}

func (s *UserServiceSuite) TearDownTest() {
    s.db.Close()
}

// ...
```

### HTTP Handler Test

```go
func TestGetUser(t *testing.T) {
    req := httptest.NewRequest("GET", "/users/1", nil)
    w := httptest.NewRecorder()

    handler := NewUserHandler(mockService)
    handler.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    var user User
    err := json.Unmarshal(w.Body.Bytes(), &user)
    require.NoError(t, err)
    assert.Equal(t, "Test User", user.Name)
}
```

### Mocking (gomock / mockery)

```go
//go:generate mockgen -source=repository.go -destination=mock_repository.go -package=user

func TestGetUser_NotFound(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := NewMockRepository(ctrl)
    mockRepo.EXPECT().FindByID("999").Return(nil, ErrNotFound)

    service := NewService(mockRepo)
    _, err := service.GetUser("999")
    assert.ErrorIs(t, err, ErrNotFound)
}
```

### Coverage

```bash
# Run with coverage
go test ./... -cover

# Generate coverage profile
go test ./... -coverprofile=coverage.out

# View HTML report
go tool cover -html=coverage.out -o coverage.html

# Check coverage threshold
go test ./... -cover | grep -E "coverage: [0-7][0-9]\." && exit 1 || echo "OK"
```

---

## Rust (cargo test)

### Basic Test

```rust
// src/calculator.rs
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_positive() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
// ...
```

### Integration Tests

```rust
// tests/integration_test.rs (separate from src/)
use my_crate::Calculator;

#[test]
fn test_calculator_workflow() {
    let calc = Calculator::new();
    let result = calc.add(2, 3);
    assert_eq!(result, 5);
}
```

### Parameterized Tests (test-case crate)

```rust
use test_case::test_case;

#[test_case("", true ; "empty string")]
#[test_case("  ", true ; "whitespace only")]
#[test_case("hello", false ; "valid string")]
fn test_is_blank(input: &str, expected: bool) {
    assert_eq!(is_blank(input), expected);
}
```

### Async Tests (tokio)

```rust
#[tokio::test]
async fn test_fetch_user() {
    let client = TestClient::new(app());
    let response = client.get("/api/users/1").send().await;
    assert_eq!(response.status(), StatusCode::OK);
}
```

### Coverage

```bash
# Using cargo-tarpaulin
cargo install cargo-tarpaulin
cargo tarpaulin --out html --output-dir coverage/

# Using llvm-cov
cargo install cargo-llvm-cov
cargo llvm-cov --html --output-dir coverage/

# Check threshold
cargo tarpaulin --fail-under 80
```

---

## Java (JUnit 5)

### Basic Test

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    private Calculator calc;

    @BeforeEach
    void setUp() {
        calc = new Calculator();
    }

    @Test
    @DisplayName("adds positive numbers correctly")
    void testAddPositive() {
        assertEquals(5, calc.add(2, 3));
// ...
```

### Parameterized Tests

```java
@ParameterizedTest
@CsvSource({
    "'', true",
    "'  ', true",
    "'hello', false",
})
void testIsBlank(String input, boolean expected) {
    assertEquals(expected, StringUtils.isBlank(input));
}

@ParameterizedTest
@MethodSource("provideEdgeCases")
void testEdgeCases(int input, int expected) {
    assertEquals(expected, process(input));
}
// ...
```

### Mocking (Mockito)

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository repository;

    @InjectMocks
    private UserService service;

    @Test
    void testGetUser_NotFound() {
        when(repository.findById("999")).thenReturn(Optional.empty());

        assertThrows(UserNotFoundException.class,
            () -> service.getUser("999"));

// ...
```

### Coverage (JaCoCo)

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
        <execution>
            <goals><goal>check</goal></goals>
            <configuration>
                <rules>
                    <rule>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <minimum>0.80</minimum>
                            </limit>
<!-- ... -->
```
