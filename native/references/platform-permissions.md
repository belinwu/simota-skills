# Platform Permissions Guide

**Purpose:** iOS / Android のパーミッション管理パターンとベストプラクティス。
**Read when:** カメラ、位置情報、通知等のパーミッションリクエストを実装する時。

---

## iOS Permissions

### Info.plist Usage Description Keys

| Permission | Key | Example Description |
|------------|-----|---------------------|
| Camera | NSCameraUsageDescription | 商品写真の撮影に使用します |
| Photo Library | NSPhotoLibraryUsageDescription | プロフィール画像の選択に使用します |
| Location (使用中) | NSLocationWhenInUseUsageDescription | 近くの店舗を検索するために使用します |
| Location (常時) | NSLocationAlwaysUsageDescription | 配達状況の追跡に使用します |
| Notifications | (runtime request) | expo-notifications で動的にリクエスト |
| Contacts | NSContactsUsageDescription | 友達招待機能に使用します |
| Microphone | NSMicrophoneUsageDescription | ボイスメッセージの録音に使用します |
| Face ID | NSFaceIDUsageDescription | セキュアログインに使用します |
| Tracking | NSUserTrackingUsageDescription | 広告のパーソナライズに使用します |

### iOS Permission Flow (React Native)

```typescript
import { check, request, PERMISSIONS, RESULTS } from 'react-native-permissions';

type PermissionResult = 'granted' | 'denied' | 'blocked' | 'unavailable';

async function requestCameraPermission(): Promise<PermissionResult> {
  // Step 1: Check current status
  const status = await check(PERMISSIONS.IOS.CAMERA);

  switch (status) {
    case RESULTS.GRANTED:
      return 'granted';

    case RESULTS.DENIED:
      // Step 2: Show pre-prompt (custom UI)
      const userAccepted = await showPrePrompt({
        title: 'カメラへのアクセス',
        message: '商品の写真を撮影するためにカメラを使用します。',
        icon: 'camera',
      });

      if (!userAccepted) return 'denied';

      // Step 3: Request system permission
      const result = await request(PERMISSIONS.IOS.CAMERA);
      return result === RESULTS.GRANTED ? 'granted' : 'denied';

    case RESULTS.BLOCKED:
      // Step 4: Guide to Settings
      showSettingsPrompt({
        title: 'カメラが無効です',
        message: '設定アプリからカメラへのアクセスを許可してください。',
      });
      return 'blocked';

    case RESULTS.UNAVAILABLE:
      return 'unavailable';

    default:
      return 'denied';
  }
}
```

---

## Android Permissions

### AndroidManifest.xml Declarations

```xml
<!-- Normal permissions (auto-granted) -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.VIBRATE" />

<!-- Dangerous permissions (runtime request required) -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.READ_CONTACTS" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- Android 13+ notification permission -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<!-- Android 14+ photo/video picker -->
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
<uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
```

### Android Runtime Permission (Jetpack Compose)

```kotlin
@Composable
fun CameraFeature() {
    val cameraPermissionState = rememberPermissionState(Manifest.permission.CAMERA)

    when {
        cameraPermissionState.status.isGranted -> {
            CameraPreview()
        }
        cameraPermissionState.status.shouldShowRationale -> {
            // Pre-prompt with rationale
            RationaleDialog(
                title = "カメラへのアクセス",
                message = "商品の写真を撮影するためにカメラを使用します。",
                onConfirm = { cameraPermissionState.launchPermissionRequest() },
                onDismiss = { /* Show degraded UI */ }
            )
        }
        else -> {
            // First request or permanently denied
            PermissionRequestButton(
                text = "カメラを有効にする",
                onClick = { cameraPermissionState.launchPermissionRequest() }
            )
        }
    }
}
```

---

## Pre-Prompt Best Practices

### Do

- 機能を使う直前にリクエスト（アプリ起動時にまとめてリクエストしない）
- なぜ必要かを具体的に説明（「写真を撮影するため」等）
- 拒否した場合の代替手段を提供
- 設定画面への導線を用意（blocked 状態の場合）

### Don't

- アプリ起動直後に全パーミッションを一括リクエスト
- 曖昧な理由（「アプリの機能向上のため」）
- 拒否後に繰り返しリクエスト
- パーミッションなしで機能が使えないことを伝えずにエラー

### Pre-Prompt UI Pattern

```
┌────────────────────────────────┐
│  📷 カメラへのアクセス          │
│                                │
│  商品の写真を撮影するために     │
│  カメラを使用します。           │
│                                │
│  [許可しない]  [許可する]       │
└────────────────────────────────┘
        ↓ 「許可する」タップ
┌────────────────────────────────┐
│  "MyApp"がカメラへのアクセスを   │
│  求めています                   │
│                                │
│  [許可しない]  [OK]             │  ← システムダイアログ
└────────────────────────────────┘
```

---

## Permission Audit Checklist

| Check | iOS | Android |
|-------|-----|---------|
| 必要なパーミッションのみ宣言 | Info.plist review | Manifest review |
| Usage Description が具体的 | ✅ Required | N/A (rationale in code) |
| Pre-prompt UI 実装 | ✅ Recommended | ✅ shouldShowRationale |
| Denied 時の graceful degradation | ✅ Required | ✅ Required |
| Settings 誘導 | ✅ Blocked 時 | ✅ Permanently denied 時 |
| Android 13+ 通知権限対応 | N/A | POST_NOTIFICATIONS |
