# Design-to-Development Handoff & Collaboration

> デザイン-開発ハンドオフのベストプラクティス、Figma トークン同期、コラボレーション戦略

## 1. ハンドオフ 6 大アンチパターン

| # | アンチパターン | 問題 | 影響 | 対策 |
|---|-------------|------|------|------|
| **HO-01** | **Wall-over-the-wall** | 完成後に一方的に投げる | 実装不可能な設計、手戻り | 初期ワイヤフレームから開発者を巻き込む |
| **HO-02** | **トークン名不一致** | Figma と コードで異なるトークン名 | 実装時の混乱、値のズレ | Figma Variables ↔ Code の自動同期パイプライン |
| **HO-03** | **曖昧なスペック** | 「いい感じに」「デザイナーに聞いて」 | 開発者の解釈ブレ、品質低下 | 具体的な値・状態・バリアント・エッジケースを明記 |
| **HO-04** | **ハッピーパスのみ** | 正常系のみデザイン | エラー・空・ローディング状態が未設計 | 全状態のデザイン必須（Empty/Error/Loading/Skeleton） |
| **HO-05** | **レスポンシブ未定義** | デスクトップのみデザイン | モバイルで破綻 | 全ブレークポイントの挙動を明示 |
| **HO-06** | **インタラクション未指定** | ホバー・フォーカス・アクティブ状態なし | 開発者が独自判断 | 全インタラクション状態を Figma でプロトタイプ化 |

---

## 2. Figma トークン同期（2025-2026）

```
Figma Variables の進化:
  - Design Tokens & Themes が CSS/JS/ネイティブトークンに直接マッピング
  - API でトークンのプログラマティック読み書きが可能
  - 単一ソースオブトゥルース（デザイン ↔ コード）

同期パイプライン:
  Figma Variables → Tokens Studio / Style Dictionary → CI/CD → Code

  ステップ:
    1. Figma Variables でトークン定義（デザイナー）
    2. Tokens Studio でエクスポート（JSON/YAML）
    3. Style Dictionary でプラットフォーム別変換
       - Web: CSS Custom Properties
       - iOS: Swift UIColor/Font
       - Android: XML resources
    4. CI/CD で自動デプロイ + Visual Regression テスト

Figma 2026 アップデート:
  - ネイティブ Git 連携（GitHub/GitLab 直接ブランチ/コミット/マージ）
  - Visual Diff が PR に表示
  - AI 生成デザイントークンのプロダクションリポジトリ直接書き出し
  - Figma MCP で Web Components への自動変換
```

---

## 3. ハンドオフベストプラクティス

```
"Ready for Dev" チェックリスト:

  デザイン準備:
    □ 全コンポーネントに一貫したトークンが使用されている
    □ インタラクション状態がすべてデザイン済み
      - Default / Hover / Focus / Active / Disabled / Error / Loading
    □ レスポンシブ挙動が全ブレークポイントで定義済み
    □ エッジケースがデザイン済み
      - Empty state / Error state / Loading / Skeleton
      - 長いテキスト / 短いテキスト / 多言語
    □ アクセシビリティ要件が明記
      - コントラスト比 / フォーカス順序 / aria ラベル
    □ アニメーション仕様が定義済み
      - duration / easing / trigger / prefers-reduced-motion 対応

  Figma 準備:
    □ フレームに "Ready for Dev" マークが付与
    □ 関連チケット/ドキュメントへのリンク
    □ Auto Layout が正しく設定（固定値ではなく）
    □ Variables（トークン）がコードと同一名称
    □ コンポーネントがプロパティベースで設定可能

  コミュニケーション:
    □ デザイン意図の「Why」が文書化
    □ 開発者向けの技術メモ（制約・優先順位）
    □ 不明点の確認先が明確
```

---

## 4. デザイン-開発コラボレーションモデル

```
効果的なコラボレーションパターン:

  パターン 1: Early Involvement（早期巻き込み）
    「開発者を巻き込むのに早すぎることはない」
    - ワイヤフレーム段階で技術的実現可能性チェック
    - コンポーネント設計段階で既存パターンとの整合確認
    - デザイン決定の背景共有

  パターン 2: Shared Language（共通言語）
    - デザイントークン名 = CSS 変数名 = Figma Variable 名
    - コンポーネント名の統一（デザイン ↔ コード）
    - 状態名の統一（default/hover/focus/active/disabled）

  パターン 3: Continuous Sync（継続的同期）
    - 週次デザイン-開発同期ミーティング
    - Figma コメントでの非同期フィードバック
    - PR での Visual Diff レビュー

  パターン 4: Living Documentation（生きたドキュメント）
    - Storybook = デザインシステムの単一ソースオブトゥルース
    - Figma → Code の自動リンク（Code Connect）
    - デザイン変更 → 自動テスト → 自動デプロイ

アンチパターン:
  ❌ デザイン完了後に開発に「投げる」（HO-01）
  ❌ Slack で口頭指示（記録なし、文脈喪失）
  ❌ デザインシステム外の一回限りのスタイル
  ❌ 「ピクセルパーフェクト」の過度な要求
  ❌ デザイナーと開発者の別々のスプリント
```

---

## 5. Vision との連携

```
Vision での活用:
  1. DELEGATE フェーズでハンドオフチェックリスト適用
  2. NEW_PRODUCT モードで Figma トークン同期パイプライン設計
  3. Forge/Muse/Artisan 委譲時に "Ready for Dev" 基準適用
  4. REVIEW モードで HO-01〜06 のスクリーニング

品質ゲート:
  - Muse 委譲時にトークン名一致確認（HO-02 防止）
  - Forge 委譲時に全状態デザイン済み確認（HO-04 防止）
  - レスポンシブ定義なし → 全ブレークポイント指定を要求（HO-05 防止）
  - インタラクション状態未指定 → 状態リスト完成を要求（HO-06 防止）
  - "Ready for Dev" チェックリスト未完了 → 委譲ブロック
```

**Source:** [Figma: Designer's Handbook for Developer Handoff](https://www.figma.com/blog/the-designers-handbook-for-developer-handoff/) · [Figma: Guide to Developer Handoff](https://www.figma.com/best-practices/guide-to-developer-handoff/) · [Figma Config 2025: What Developers Need to Know](https://f1studioz.com/blog/figma-config-2025-what-developers-really-need-to-know/) · [Figma MCP to Web Components](https://jangwook.net/en/blog/en/figma-mcp-web-components-sync/)
