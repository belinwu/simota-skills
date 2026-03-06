# Vue 3 & Svelte 5 Patterns

Production-quality patterns for Vue 3 Composition API and Svelte 5 Runes.

---

## Vue 3 Composition API

### Component with Props, Emits, and Reactivity

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';

// Props with TypeScript
interface Props {
  userId: string;
  initialName?: string;
}

const props = withDefaults(defineProps<Props>(), {
  initialName: '',
});

// Emits with TypeScript
const emit = defineEmits<{
  (e: 'update', value: string): void;
  (e: 'submit'): void;
}>();

// Reactive state
const name = ref(props.initialName);
const isLoading = ref(false);

// Computed
const isValid = computed(() => name.value.length >= 3);

// Watch
watch(name, (newValue) => {
  emit('update', newValue);
});

// Lifecycle
onMounted(async () => {
  isLoading.value = true;
  // fetch data...
  isLoading.value = false;
});

// Methods
const handleSubmit = () => {
  if (isValid.value) {
    emit('submit');
  }
};
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="name" :disabled="isLoading" />
    <button type="submit" :disabled="!isValid">Submit</button>
  </form>
</template>
```

---

## Vue Composables (Custom Hooks)

```typescript
// composables/useAsync.ts
import { ref, type Ref } from 'vue';

interface AsyncState<T> {
  data: Ref<T | null>;
  error: Ref<Error | null>;
  isLoading: Ref<boolean>;
  execute: () => Promise<void>;
}

export function useAsync<T>(asyncFn: () => Promise<T>): AsyncState<T> {
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const isLoading = ref(false);

  const execute = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      data.value = await asyncFn();
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e));
    } finally {
      isLoading.value = false;
    }
  };

  return { data, error, isLoading, execute };
}
```

---

## Pinia Store (State Management)

```typescript
// stores/auth.ts
import { defineStore } from 'pinia';

interface User {
  id: string;
  name: string;
  email: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
  }),

  getters: {
    userName: (state) => state.user?.name ?? 'Guest',
  },

  actions: {
    async login(email: string, password: string) {
      const user = await authApi.login(email, password);
      this.user = user;
      this.isAuthenticated = true;
    },

    logout() {
      this.user = null;
      this.isAuthenticated = false;
    },
  },
});
```

---

## Svelte 5 Runes

### Component with $state, $derived, $effect

```svelte
<script lang="ts">
  // Props with Runes
  interface Props {
    userId: string;
    initialCount?: number;
  }

  let { userId, initialCount = 0 }: Props = $props();

  // Reactive state with $state
  let count = $state(initialCount);
  let name = $state('');

  // Derived values with $derived
  let doubled = $derived(count * 2);
  let isValid = $derived(name.length >= 3);

  // Effects with $effect
  $effect(() => {
    console.log(`Count changed to ${count}`);
    return () => {
      console.log('Cleanup');
    };
  });

  // Event handlers
  function increment() {
    count++;
  }

  function handleSubmit() {
    if (isValid) {
      // submit logic
    }
  }
</script>

<div>
  <p>Count: {count} (doubled: {doubled})</p>
  <button onclick={increment}>Increment</button>

  <form onsubmit={handleSubmit}>
    <input bind:value={name} />
    <button type="submit" disabled={!isValid}>Submit</button>
  </form>
</div>
```

---

## Svelte 5 Snippet Components

```svelte
<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    title: string;
    children: Snippet;
    footer?: Snippet;
  }

  let { title, children, footer }: Props = $props();
</script>

<div class="card">
  <header class="card-header">
    <h2>{title}</h2>
  </header>
  <div class="card-body">
    {@render children()}
  </div>
  {#if footer}
    <footer class="card-footer">
      {@render footer()}
    </footer>
  {/if}
</div>

<!-- Usage -->
<Card title="My Card">
  <p>Card content here</p>
  {#snippet footer()}
    <button>Action</button>
  {/snippet}
</Card>
```

---

## Svelte Stores (State Management)

```typescript
// stores/auth.svelte.ts
import { writable, derived } from 'svelte/store';

interface User {
  id: string;
  name: string;
}

function createAuthStore() {
  const { subscribe, set, update } = writable<{
    user: User | null;
    isAuthenticated: boolean;
  }>({
    user: null,
    isAuthenticated: false,
  });

  return {
    subscribe,
    login: async (email: string, password: string) => {
      const user = await authApi.login(email, password);
      set({ user, isAuthenticated: true });
    },
    logout: () => {
      set({ user: null, isAuthenticated: false });
    },
  };
}

export const authStore = createAuthStore();

// Derived store
export const userName = derived(
  authStore,
  ($auth) => $auth.user?.name ?? 'Guest'
);
```

---

## Vue Performance Hints

### v-memo

リストアイテムの不要な再レンダリングを防止。指定した依存値が変わらない限り、VNode の再生成をスキップする。

```vue
<template>
  <!-- selected が変わった行のみ再レンダリング -->
  <div v-for="item in items" :key="item.id" v-memo="[item.id === selectedId]">
    <ItemComponent :item="item" :selected="item.id === selectedId" />
  </div>
</template>
```

| 使い所 | 効果 |
|--------|------|
| 大規模リスト (100+ 行) | 不要な VNode diff をスキップ |
| 選択状態の切り替え | 変更行のみ更新 |
| テーブルの行ハイライト | 全行の再レンダリングを防止 |

**注意:** `v-memo="[]"` は `v-once` と同等（一度だけレンダリング）。

### markRaw

リアクティビティ不要なオブジェクトをマークし、Proxy 化を回避する。

```ts
import { markRaw, ref } from 'vue';

// Bad: 大きなライブラリオブジェクトをリアクティブにする（パフォーマンスコスト大）
const map = ref(new MapLibreGL.Map({ /* ... */ }));

// Good: markRaw でリアクティビティを回避
const map = ref(markRaw(new MapLibreGL.Map({ /* ... */ })));

// サードパーティクラスインスタンスに有効
const chart = markRaw(new Chart(canvas, config));
const editor = markRaw(new Monaco.Editor(container));
```

| 対象 | 理由 |
|------|------|
| 地図ライブラリ (Mapbox, Leaflet) | 内部状態が膨大で Proxy 化不要 |
| チャートライブラリ (Chart.js, D3) | 独自の更新メカニズムを持つ |
| エディタインスタンス (Monaco, CodeMirror) | リアクティビティが干渉する |
| 不変の設定オブジェクト | 変更されないため Proxy 不要 |
