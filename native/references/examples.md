# Usage Examples

**Purpose:** Native エージェントの代表的なユースケースと出力例。
**Read when:** タスクの進め方や出力フォーマットの参考が必要な時。

---

## Example 1: React Native Expo プロジェクト初期セットアップ

### Input
```
React Native (Expo) で EC アプリを作りたい。Tab ナビゲーションで Home / Cart / Profile の3タブ構成。
```

### Output Summary
- Expo Router によるファイルベースルーティング設定
- 3タブレイアウト（Home / Cart / Profile）
- TypeScript strict mode 設定
- 基本的な状態管理（Zustand + MMKV）
- オフラインキャッシュ基盤（TanStack Query + NetInfo）

### Key Files Generated
```
app/
├── (tabs)/
│   ├── _layout.tsx      # Tab navigator configuration
│   ├── index.tsx         # Home tab
│   ├── cart.tsx          # Cart tab
│   └── profile.tsx       # Profile tab
├── _layout.tsx           # Root layout with providers
└── +not-found.tsx        # 404 screen
src/
├── stores/
│   └── cart-store.ts     # Zustand + MMKV persistence
├── hooks/
│   └── use-network.ts   # Network status hook
└── lib/
    └── query-client.ts   # TanStack Query configuration
```

---

## Example 2: プッシュ通知統合

### Input
```
既存の Expo アプリにプッシュ通知を追加。バックエンドは Firebase。
```

### Output Summary
- expo-notifications 設定
- FCM トークン取得・登録フロー
- 通知権限リクエスト（pre-prompt 付き）
- フォアグラウンド・バックグラウンドハンドリング
- ディープリンク連携

### Permission Pre-prompt Pattern
```typescript
async function requestNotificationPermission(): Promise<boolean> {
  const { status: existing } = await Notifications.getPermissionsAsync();
  if (existing === 'granted') return true;

  // Pre-prompt: show custom UI before system dialog
  const userConsent = await showPrePromptDialog({
    title: '通知を受け取りますか？',
    message: '注文状況やセール情報をお知らせします。設定からいつでも変更できます。',
    acceptLabel: '通知を許可',
    declineLabel: '後で',
  });

  if (!userConsent) return false;

  const { status } = await Notifications.requestPermissionsAsync();
  return status === 'granted';
}
```

---

## Example 3: Flutter オフラインファーストアプリ

### Input
```
Flutter でフィールドワーク記録アプリ。電波の届かない場所でも使える必要がある。
```

### Output Summary
- Drift (SQLite) によるローカルデータベース
- Write queue + 自動同期
- 画像のローカルキャッシュ
- 同期状態インジケーター UI
- コンフリクト解決戦略（Last-Write-Wins + ユーザー確認）

---

## Example 4: SwiftUI アプリ内課金

### Input
```
SwiftUI アプリに月額サブスクリプションを追加。StoreKit 2 で実装。
```

### Output Summary
- StoreKit 2 Product / Transaction API
- サブスクリプションライフサイクル管理
- トライアル期間ハンドリング
- 課金状態の永続化と復元
- App Store Server Notifications v2 連携ポイント

---

## Example 5: ストア審査対応レビュー

### Input
```
App Store に提出する前にガイドライン準拠をチェックしてほしい。
```

### Output Summary（チェックリスト形式）
```markdown
## App Store Review Checklist

### Privacy (Section 5.1)
- [ ] NSPrivacyAccessedAPITypes in PrivacyInfo.xcprivacy
- [ ] Purpose strings for all permission requests
- [ ] App Tracking Transparency if IDFA used
- [ ] Privacy nutrition labels match actual data collection

### In-App Purchase (Section 3.1)
- [ ] All digital content uses Apple IAP (no external payment links)
- [ ] Restore purchases button accessible
- [ ] Subscription terms displayed before purchase

### Performance (Section 2.1)
- [ ] App launches within reasonable time
- [ ] No crashes on supported OS versions
- [ ] Memory usage within limits

### Design (Section 4.0)
- [ ] SF Symbols used for system icons
- [ ] Dynamic Type supported
- [ ] Safe area respected on all device sizes
```
