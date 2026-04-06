# Modern Mobile Stack Reference

**Purpose:** 最新のモバイル技術スタックの概要と移行ガイダンス。
**Read when:** フレームワーク選定、新規プロジェクトセットアップ、既存プロジェクトの最新化判断時。

---

## React Native New Architecture

### Overview

React Native 0.76+ で New Architecture がデフォルトに。主要な変更点:

| Component | Old Architecture | New Architecture |
|-----------|-----------------|-----------------|
| Bridge | JSON serialization (async) | JSI (synchronous, shared memory) |
| UI Renderer | Paper | Fabric |
| Native Modules | Legacy NativeModules | TurboModules (lazy-loaded) |
| Type Safety | None (runtime) | Codegen from Flow/TS specs |

### Migration Considerations

```typescript
// TurboModule spec example (new pattern)
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  getConstants(): { version: string };
  multiply(a: number, b: number): Promise<number>;
}

export default TurboModuleRegistry.getEnforcing<Spec>('Calculator');
```

### Key Benefits
- 同期的な JS-Native 通信（JSI 経由）
- TurboModules の遅延ロードによる起動時間改善
- Fabric renderer による並行レンダリング
- Codegen による型安全な Native インターフェース

---

## Expo SDK 52+

### Key Features

| Feature | Description |
|---------|-------------|
| expo-router v4 | File-based routing with React Server Components support |
| EAS Workflows | CI/CD pipeline as YAML config |
| Fingerprint | Deterministic native runtime versioning |
| DOM Components | Web views embedded in native apps |
| React 19 support | Use hook, Server Components, improved Suspense |

### Expo Router v4

```typescript
// app/(tabs)/_layout.tsx - Typed Routes
import { Tabs } from 'expo-router';

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: 'Home' }} />
      <Tabs.Screen name="cart" options={{ title: 'Cart' }} />
      <Tabs.Screen name="profile" options={{ title: 'Profile' }} />
    </Tabs>
  );
}
```

### EAS Workflows

```yaml
# eas-workflows.yml
build-and-submit:
  name: Build and Submit
  on:
    push:
      branches: [main]
  jobs:
    build:
      steps:
        - uses: eas/build
          with:
            platform: all
            profile: production
        - uses: eas/submit
          with:
            platform: all
```

---

## Swift 6 Concurrency

### Strict Concurrency

Swift 6 はデフォルトでデータ競合安全性をコンパイル時に検証。

```swift
// Swift 6: Actor-based state isolation
@Observable
@MainActor
final class CartViewModel {
    private(set) var items: [CartItem] = []
    private(set) var isLoading = false

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await CartService.shared.fetchItems()
        } catch {
            // Handle error
        }
    }

    func addItem(_ item: CartItem) {
        items.append(item)
        Task {
            try await CartService.shared.syncItem(item)
        }
    }
}
```

### Key Patterns

| Pattern | Use Case |
|---------|----------|
| `@MainActor` | UI state management, ViewModel |
| `actor` | Thread-safe shared mutable state |
| `Sendable` | Cross-isolation boundary data |
| `async let` | Parallel async operations |
| `TaskGroup` | Dynamic concurrency |

### Migration from GCD

```swift
// Before (GCD)
DispatchQueue.global().async {
    let data = loadData()
    DispatchQueue.main.async {
        self.updateUI(data)
    }
}

// After (Swift 6 structured concurrency)
Task {
    let data = await loadData()
    await MainActor.run {
        updateUI(data)
    }
}
```

---

## Kotlin Multiplatform (KMP)

### Architecture

```
┌─────────────────────────────────┐
│         Shared Module (KMP)     │
│  ┌───────────────────────────┐  │
│  │  Business Logic           │  │
│  │  Data Models              │  │
│  │  Repository Layer         │  │
│  │  Network Client (Ktor)    │  │
│  │  Local DB (SQLDelight)    │  │
│  └───────────────────────────┘  │
├────────────┬────────────────────┤
│  iOS App   │   Android App      │
│  SwiftUI   │   Jetpack Compose  │
│  Native UI │   Native UI        │
└────────────┴────────────────────┘
```

### Shared Module Example

```kotlin
// shared/src/commonMain/kotlin/com/app/repository/ProductRepository.kt
class ProductRepository(
    private val api: ProductApi,
    private val db: ProductDatabase,
) {
    suspend fun getProducts(): List<Product> {
        return try {
            val remote = api.fetchProducts()
            db.saveProducts(remote)
            remote
        } catch (e: Exception) {
            db.getProducts() // Offline fallback
        }
    }
}
```

### When to Choose KMP

| Scenario | Recommendation |
|----------|---------------|
| New project, native UI required | KMP + SwiftUI/Compose |
| Existing separate iOS/Android apps | KMP for shared logic migration |
| Complex business logic, simple UI | KMP (high value) |
| UI-heavy, simple logic | Native or Flutter (low KMP value) |

---

## Compose Multiplatform

### Platform Support

| Platform | Status | Maturity |
|----------|--------|----------|
| Android | Stable | Production-ready |
| Desktop (JVM) | Stable | Production-ready |
| iOS | Beta | Suitable for new projects |
| Web (Wasm) | Alpha | Experimental |

### Shared UI Example

```kotlin
// shared/src/commonMain/kotlin/com/app/ui/ProductCard.kt
@Composable
fun ProductCard(
    product: Product,
    onAddToCart: (Product) -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(modifier = modifier) {
        AsyncImage(
            model = product.imageUrl,
            contentDescription = product.name,
        )
        Text(product.name, style = MaterialTheme.typography.titleMedium)
        Text(product.formattedPrice, style = MaterialTheme.typography.bodyLarge)
        Button(onClick = { onAddToCart(product) }) {
            Text("カートに追加")
        }
    }
}
```

---

## Framework Selection Guide (Updated)

| Criteria | React Native + Expo | Flutter | KMP + Native UI | Compose Multiplatform |
|----------|--------------------|---------|-----------------|-----------------------|
| Team skills | JS/TS | Dart | Kotlin + Swift | Kotlin |
| UI sharing | Full | Full | None (native per platform) | Full (Beta on iOS) |
| Logic sharing | Full | Full | Full | Full |
| Performance | Near-native (JSI) | Near-native (Impeller) | Native | Near-native |
| Ecosystem | npm (largest) | pub.dev | Maven/CocoaPods | Maven/CocoaPods |
| Hot reload | Yes | Yes | No (native builds) | Yes (desktop/Android) |
| iOS maturity | Stable | Stable | Stable | Beta |
