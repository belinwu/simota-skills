# Mobile Design Patterns

**Purpose:** モバイル開発のデザインパターンと実装テンプレート集。
**Read when:** Navigation、状態管理、オフライン、プラットフォーム固有パターンの実装時。

---

## Navigation Patterns

### React Native (React Navigation v7)

```typescript
// Stack Navigator with typed routes
import { createNativeStackNavigator } from '@react-navigation/native-stack';

type RootStackParamList = {
  Home: undefined;
  Profile: { userId: string };
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

function RootNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Profile" component={ProfileScreen} />
      <Stack.Screen name="Settings" component={SettingsScreen} />
    </Stack.Navigator>
  );
}
```

### Flutter (GoRouter)

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'profile/:userId',
          builder: (context, state) {
            final userId = state.pathParameters['userId']!;
            return ProfileScreen(userId: userId);
          },
        ),
      ],
    ),
  ],
);
```

### SwiftUI (NavigationStack)

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            HomeView()
                .navigationDestination(for: UserID.self) { userId in
                    ProfileView(userId: userId)
                }
        }
    }
}
```

### Jetpack Compose (Navigation)

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "home") {
        composable("home") { HomeScreen(navController) }
        composable("profile/{userId}") { backStackEntry ->
            val userId = backStackEntry.arguments?.getString("userId")
            ProfileScreen(userId = userId)
        }
    }
}
```

---

## Deep Link Configuration

### React Native (Expo)

```json
// app.json
{
  "expo": {
    "scheme": "myapp",
    "ios": {
      "associatedDomains": ["applinks:example.com"]
    },
    "android": {
      "intentFilters": [
        {
          "action": "VIEW",
          "autoVerify": true,
          "data": [{ "scheme": "https", "host": "example.com", "pathPrefix": "/app" }],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    }
  }
}
```

### Linking Configuration

```typescript
const linking = {
  prefixes: ['myapp://', 'https://example.com'],
  config: {
    screens: {
      Home: '',
      Profile: 'profile/:userId',
      Settings: 'settings',
    },
  },
};
```

---

## State Management Patterns

### React Native (Zustand + MMKV)

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

const zustandStorage = createJSONStorage(() => ({
  getItem: (name: string) => storage.getString(name) ?? null,
  setItem: (name: string, value: string) => storage.set(name, value),
  removeItem: (name: string) => storage.delete(name),
}));

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
}

export const useCartStore = create<CartStore>()(
  persist(
    (set) => ({
      items: [],
      addItem: (item) => set((state) => ({ items: [...state.items, item] })),
      removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.id !== id) })),
    }),
    { name: 'cart-storage', storage: zustandStorage }
  )
);
```

### Flutter (Riverpod)

```dart
@riverpod
class CartNotifier extends _$CartNotifier {
  @override
  List<CartItem> build() => [];

  void addItem(CartItem item) {
    state = [...state, item];
  }

  void removeItem(String id) {
    state = state.where((item) => item.id != id).toList();
  }
}
```

---

## Offline-First Patterns

### Write Queue Pattern (React Native)

```typescript
interface QueuedWrite {
  id: string;
  endpoint: string;
  method: 'POST' | 'PUT' | 'DELETE';
  body: unknown;
  createdAt: number;
  retryCount: number;
}

class OfflineWriteQueue {
  private queue: QueuedWrite[] = [];

  async enqueue(write: Omit<QueuedWrite, 'id' | 'createdAt' | 'retryCount'>) {
    const entry: QueuedWrite = {
      ...write,
      id: uuid(),
      createdAt: Date.now(),
      retryCount: 0,
    };
    this.queue.push(entry);
    await this.persistQueue();
  }

  async flush() {
    const pending = [...this.queue];
    for (const write of pending) {
      try {
        await fetch(write.endpoint, { method: write.method, body: JSON.stringify(write.body) });
        this.queue = this.queue.filter(w => w.id !== write.id);
      } catch {
        write.retryCount++;
        if (write.retryCount > 5) {
          // Move to dead letter queue
          this.queue = this.queue.filter(w => w.id !== write.id);
        }
      }
    }
    await this.persistQueue();
  }
}
```

### Network Status Hook

```typescript
import NetInfo from '@react-native-community/netinfo';
import { useEffect, useState } from 'react';

export function useNetworkStatus() {
  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsConnected(state.isConnected ?? false);
    });
    return unsubscribe;
  }, []);

  return { isConnected };
}
```

---

## Platform Adaptation Pattern

```typescript
import { Platform } from 'react-native';

// Component-level branching (preferred)
const SearchBar = Platform.select({
  ios: () => <IOSSearchBar />,
  android: () => <AndroidSearchBar />,
  default: () => <DefaultSearchBar />,
})!;

// Style-level branching
const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
    },
    android: {
      elevation: 4,
    },
  }),
});
```
