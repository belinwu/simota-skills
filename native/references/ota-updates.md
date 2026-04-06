# OTA Update Strategy

**Purpose:** CodePush / EAS Update / Shorebird による OTA アップデート戦略。
**Read when:** OTA 配信、段階的ロールアウト、ロールバック計画が必要な時。

---

## OTA Update Comparison

| Feature | EAS Update (Expo) | CodePush (MS) | Shorebird (Flutter) |
|---------|-------------------|---------------|---------------------|
| Framework | React Native (Expo) | React Native | Flutter |
| Update scope | JS bundle + assets | JS bundle + assets | Dart code + assets |
| Native code changes | ❌ Full build required | ❌ Full build required | ❌ Full build required |
| Rollback | Channel-based | Automatic + manual | Patch-based |
| Staged rollout | ✅ Via channels | ✅ Percentage-based | ✅ Percentage-based |
| Pricing | Expo plan included | App Center (EOL注意) | Free tier + paid |

---

## EAS Update (Recommended for Expo)

### Setup

```bash
# Install
npx expo install expo-updates

# Configure
eas update:configure

# Create update
eas update --branch production --message "Fix cart calculation bug"
```

### Channel Strategy

```
production ← 全ユーザー向け安定版
preview    ← QA/ステークホルダー向け検証版
staging    ← 開発チーム向け最新版
```

### Rollback Pattern

```bash
# 問題のある更新をロールバック
# 前回の安定版を再公開
eas update --branch production --message "Rollback: revert cart fix"

# または特定の更新をチャンネルに紐付け
eas channel:rollout production --percent 0  # 段階的に停止
```

### Implementation

```typescript
import * as Updates from 'expo-updates';

export async function checkForUpdates() {
  if (__DEV__) return; // Skip in development

  try {
    const update = await Updates.checkForUpdateAsync();
    if (update.isAvailable) {
      await Updates.fetchUpdateAsync();

      // Strategy: prompt user or auto-restart
      Alert.alert(
        'アップデート',
        '新しいバージョンが利用可能です。再起動しますか？',
        [
          { text: '後で', style: 'cancel' },
          { text: '再起動', onPress: () => Updates.reloadAsync() },
        ]
      );
    }
  } catch (error) {
    // Silently fail - don't block user
    console.error('Update check failed:', error);
  }
}
```

---

## Shorebird (Flutter)

### Setup

```bash
# Install Shorebird CLI
curl --proto '=https' --tlsv1.2 https://raw.githubusercontent.com/shorebirdtech/install/main/install.sh -sSf | bash

# Initialize
shorebird init

# Create release
shorebird release android
shorebird release ios

# Push patch
shorebird patch android --release-version 1.0.0
shorebird patch ios --release-version 1.0.0
```

---

## OTA Update Best Practices

### What Can Be Updated OTA

| Updatable (OTA) | Requires Full Build |
|-----------------|---------------------|
| UI layout changes | New native modules |
| Business logic fixes | Permission additions |
| Asset updates (images, fonts) | SDK version changes |
| Navigation changes | Native library updates |
| API endpoint changes | Minimum OS version change |

### Staged Rollout Strategy

```
Step 1: Internal (1%)   → 開発チームで検証
Step 2: Canary (5%)     → 小規模ユーザーで監視
Step 3: Gradual (25%)   → エラーレート監視
Step 4: Wide (50%)      → パフォーマンス指標確認
Step 5: Full (100%)     → 全ユーザーに展開
```

### Monitoring Checklist

| Metric | Threshold | Action |
|--------|-----------|--------|
| Crash rate | > 1% increase | Auto-rollback |
| ANR rate (Android) | > 0.5% | Pause rollout |
| Error rate | > 2x baseline | Investigate |
| Update adoption | < 50% after 24h | Check update logic |

### Rollback Decision Tree

```
Update deployed
      ↓
Monitor 1h → Crash spike? → YES → Immediate rollback
                              ↓ NO
Monitor 24h → Error increase? → YES → Pause + investigate
                                 ↓ NO
Continue rollout → Full deployment
```
