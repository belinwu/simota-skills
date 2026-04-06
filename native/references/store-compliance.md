# Store Compliance Guide

**Purpose:** App Store / Google Play のガイドライン準拠チェックリストと対応パターン。
**Read when:** ストア提出準備、IAP 実装、プライバシー対応が必要な時。

---

## App Store Guidelines (Apple)

### Privacy (Section 5.1)

| Requirement | Implementation |
|-------------|----------------|
| PrivacyInfo.xcprivacy | Required API reason declarations |
| Purpose strings | NSCameraUsageDescription, NSLocationWhenInUseUsageDescription 等 |
| App Tracking Transparency | IDFA 使用時は ATTrackingManager 必須 |
| Privacy nutrition labels | App Store Connect で正確に申告 |
| Data minimization | 必要最小限のデータのみ収集 |

### In-App Purchase (Section 3.1)

| Rule | Detail |
|------|--------|
| Digital goods via Apple IAP only | 外部決済リンク禁止（Reader App 例外あり） |
| Restore purchases | 復元ボタンを設定画面等に配置 |
| Subscription terms | 購入前に期間・価格・自動更新を明示 |
| Free trial | トライアル終了後の課金を事前に明示 |
| Price display | ローカル通貨で表示（ProductResponse から取得） |

### StoreKit 2 Implementation Pattern

```swift
import StoreKit

@Observable
class SubscriptionManager {
    private(set) var products: [Product] = []
    private(set) var purchasedSubscriptions: [Product] = []

    func loadProducts() async {
        do {
            products = try await Product.products(for: ["com.app.monthly", "com.app.yearly"])
        } catch {
            // Handle error
        }
    }

    func purchase(_ product: Product) async throws -> Transaction? {
        let result = try await product.purchase()
        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)
            await transaction.finish()
            await updatePurchasedSubscriptions()
            return transaction
        case .userCancelled, .pending:
            return nil
        @unknown default:
            return nil
        }
    }

    func checkVerified<T>(_ result: VerificationResult<T>) throws -> T {
        switch result {
        case .unverified:
            throw StoreError.failedVerification
        case .verified(let safe):
            return safe
        }
    }
}
```

### Common Rejection Reasons

| Reason | Prevention |
|--------|------------|
| 2.1 Performance - crashes | テスト全デバイスサイズで実行 |
| 2.3 Accurate metadata | スクリーンショットが実際の UI と一致 |
| 3.1.1 IAP required | デジタルコンテンツは Apple IAP 経由 |
| 4.0 Design - HIG violation | SF Symbols 使用、Dynamic Type 対応 |
| 5.1.1 Data collection | PrivacyInfo.xcprivacy 正確に記述 |
| 5.1.2 Data use | 目的外利用なし |

---

## Google Play Policy

### Data Safety

| Requirement | Implementation |
|-------------|----------------|
| Data safety form | Play Console で正確に申告 |
| Encryption in transit | HTTPS 必須 |
| Data deletion option | アカウント削除機能の提供 |
| Families policy | 子供向けアプリは追加制限あり |

### Google Play Billing

| Rule | Detail |
|------|--------|
| Digital goods via Play Billing | デジタルコンテンツは Google Play Billing 経由 |
| Subscription transparency | 価格・期間・自動更新を購入前に表示 |
| Grace period | 支払い失敗時の猶予期間を設定推奨 |
| Account hold | 一時停止状態のハンドリング |

### Billing Implementation Pattern (Kotlin)

```kotlin
class BillingManager(private val activity: Activity) {
    private val billingClient = BillingClient.newBuilder(activity)
        .setListener(purchasesUpdatedListener)
        .enablePendingPurchases()
        .build()

    fun startConnection() {
        billingClient.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(billingResult: BillingResult) {
                if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                    queryProducts()
                }
            }
            override fun onBillingServiceDisconnected() {
                // Retry connection
            }
        })
    }

    private fun queryProducts() {
        val productList = listOf(
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId("monthly_subscription")
                .setProductType(BillingClient.ProductType.SUBS)
                .build()
        )
        val params = QueryProductDetailsParams.newBuilder()
            .setProductList(productList)
            .build()

        billingClient.queryProductDetailsAsync(params) { billingResult, productDetailsList ->
            // Handle product details
        }
    }
}
```

---

## Cross-Platform Compliance Checklist

| Item | iOS | Android |
|------|-----|---------|
| Privacy declaration | PrivacyInfo.xcprivacy + Nutrition Labels | Data Safety Form |
| Permission rationale | NSUsageDescription strings | shouldShowRequestPermissionRationale |
| IAP implementation | StoreKit 2 | Google Play Billing Library |
| Age rating | App Store rating questionnaire | Content rating questionnaire |
| Accessibility | VoiceOver + Dynamic Type | TalkBack + Font scaling |
| Data deletion | Account deletion feature | Account deletion feature |
| Encryption export | ITSAppUsesNonExemptEncryption | N/A (Google handles) |
