# Motion Accessibility Anti-Patterns

> WCAG モーション要件、前庭障害への配慮、prefers-reduced-motion 実装、プログレッシブエンハンスメント

## 1. モーションアクセシビリティ 7 大アンチパターン

| # | アンチパターン | 問題 | ユーザーへの影響 | 対策 |
|---|-------------|------|---------------|------|
| **MA-01** | **reduced-motion 未対応** | `prefers-reduced-motion` を無視 | 前庭障害ユーザーにめまい・吐き気 | 全アニメーションに `prefers-reduced-motion` 対応 |
| **MA-02** | **自動再生アニメーション** | ユーザー操作なしにアニメーション開始 | 制御不能な視覚刺激、集中力阻害 | 5秒以上は一時停止/停止/非表示メカニズム必須 |
| **MA-03** | **フラッシュ/点滅** | 3回/秒以上の明滅 | てんかん発作の誘発リスク | 3回/秒未満を厳守、または閾値以下の面積に制限 |
| **MA-04** | **モーションのみの情報伝達** | アニメーションでしか伝わらない状態変化 | アニメーション無効時に情報欠落 | 色・テキスト・アイコンで冗長に情報提供 |
| **MA-05** | **全消去アプローチ** | reduced-motion 時に全アニメーションを削除 | 機能的フィードバックも消失、UX 低下 | 代替アニメーション提供（フェード、即時遷移） |
| **MA-06** | **OS 設定のみ依存** | OS レベルの設定しか尊重しない | 状況に応じた制御ができない | ページ内トグルも提供（OS 設定 + アプリ内設定） |
| **MA-07** | **パララックス強制** | スクロール連動の大きな視差効果 | 前庭障害ユーザーに乗り物酔い様症状 | reduced-motion 時はパララックス無効化 |

---

## 2. WCAG モーション関連基準

```
WCAG 2.2 モーション関連:

  2.2.2 一時停止、停止、非表示（レベル A）:
    - 自動開始 + 5秒以上続くアニメーション → 一時停止/停止/非表示の手段必須
    - 自動更新情報 → 一時停止/停止/頻度制御の手段必須
    - 例外: アニメーションが本質的に必要な場合（ローディング表示等）

  2.3.1 3回の閃光、又は閾値以下（レベル A）:
    - 1秒間に3回以上の閃光を含まない
    - または閃光が一般閃光閾値・赤色閃光閾値以下

  2.3.3 インタラクションによるアニメーション（レベル AAA）:
    - インタラクション起因のアニメーションを無効化可能
    - 例外: 機能または伝達情報に必須のアニメーション

影響を受けるユーザー:
  - 前庭障害: 成人の約 35%（40歳以上）が何らかの前庭機能障害
  - てんかん: 光過敏性てんかんは全てんかんの約 3%
  - 注意障害: ADHD 等でアニメーションが集中阻害要因に
  - 乗り物酔い感受性: パララックス、ズーム効果で症状誘発
```

---

## 3. prefers-reduced-motion 実装パターン

```
CSS 実装（推奨: プログレッシブエンハンスメント）:

  ✅ 推奨: reduced-motion をデフォルトとする
    /* ベース: アニメーションなし */
    .element {
      transition: none;
    }

    /* モーション許可時のみアニメーション追加 */
    @media (prefers-reduced-motion: no-preference) {
      .element {
        transition: transform 0.3s var(--ease-out);
      }
    }

  ⚠️ 従来型: reduced-motion でアニメーション除去
    .element {
      transition: transform 0.3s var(--ease-out);
    }

    @media (prefers-reduced-motion: reduce) {
      .element {
        transition: none;
      }
    }

  ✅ 推奨: 代替アニメーション提供（全消去ではなく）
    @media (prefers-reduced-motion: reduce) {
      .element {
        /* スライドの代わりにフェード */
        transition: opacity 0.15s ease;
        animation: none;
      }
    }

JS 実装:

  // メディアクエリの監視
  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

  function handleMotionPreference(e) {
    if (e.matches) {
      // アニメーション縮小/無効化
      document.documentElement.dataset.motion = 'reduce';
    } else {
      document.documentElement.dataset.motion = 'full';
    }
  }

  motionQuery.addEventListener('change', handleMotionPreference);
  handleMotionPreference(motionQuery);
```

---

## 4. プログレッシブエンハンスメント戦略

```
3 段階のモーション戦略:

  Level 0: ベースライン（reduced-motion）
    - アニメーションなし
    - 即時の状態変化（opacity の瞬時切替は可）
    - 全ユーザーに機能的に完全な体験

  Level 1: 最小モーション
    - フェードのみ（opacity 0.15s）
    - 短い duration（100ms 以下）
    - 移動・スケール・回転なし

  Level 2: フルモーション（no-preference）
    - スライド、スケール、回転
    - パララックス、スクロールアニメーション
    - 複合アニメーション、ジェスチャーフィードバック

実装例:
  :root {
    --motion-duration: 0ms;
    --motion-transform: none;
  }

  @media (prefers-reduced-motion: no-preference) {
    :root {
      --motion-duration: 200ms;
      --motion-transform: translateY(-4px);
    }
  }

  .card:hover {
    transform: var(--motion-transform);
    transition: transform var(--motion-duration) var(--ease-out);
  }
```

---

## 5. ページ内モーション制御

```
OS 設定に加えてアプリ内トグルを提供:

  理由:
    - OS 設定を知らないユーザーが多い
    - サイトごとに異なるモーション許容度がある
    - 一時的にモーションを減らしたい場合がある

  実装:
    <button id="motion-toggle" aria-pressed="false">
      モーションを減らす
    </button>

    const toggle = document.getElementById('motion-toggle');
    toggle.addEventListener('click', () => {
      const reduced = document.documentElement.classList.toggle('reduce-motion');
      toggle.setAttribute('aria-pressed', reduced);
      localStorage.setItem('motion-preference', reduced ? 'reduce' : 'full');
    });

    // ページ読み込み時に復元
    const saved = localStorage.getItem('motion-preference');
    if (saved === 'reduce') {
      document.documentElement.classList.add('reduce-motion');
    }

  CSS:
    .reduce-motion *,
    .reduce-motion *::before,
    .reduce-motion *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
    }
```

---

## 6. アニメーション種別ごとの対応方針

| アニメーション種別 | reduced-motion 時の対応 | 理由 |
|----------------|---------------------|------|
| ページ遷移（スライド） | フェードまたは即時切替 | 機能は維持、動きを抑制 |
| ホバーエフェクト | 色変化のみ、移動なし | フィードバックは維持 |
| ローディングスピナー | 静的プログレスバーまたはテキスト | 機能的に必須なら維持可 |
| スクロールアニメーション | 即時表示 | 装飾的、非必須 |
| パララックス | 完全無効化 | 前庭障害リスク高 |
| モーダル遷移 | フェードまたは即時表示 | 出現は知らせるが動きは抑制 |
| ドラッグフィードバック | 維持（機能的） | 操作に必須のフィードバック |
| 成功/エラーフィードバック | 色 + アイコン + テキスト | アニメーションなしで情報伝達 |

---

## 7. Flow との連携

```
Flow での活用:
  1. 全アニメーション実装時に prefers-reduced-motion 対応を必須化
  2. プログレッシブエンハンスメント（Level 0 → 2）で設計
  3. 代替アニメーション提供（全消去ではなく段階的縮小）
  4. パララックス実装時は必ず無効化オプション

品質ゲート:
  - prefers-reduced-motion 未対応 → 対応追加（MA-01 防止）
  - 5秒以上の自動アニメーション → 停止メカニズム追加（MA-02 防止）
  - 3回/秒以上の明滅 → 即時修正（MA-03 防止）
  - reduced-motion で全アニメーション削除 → 代替提供（MA-05 防止）
  - パララックス効果 → reduced-motion 時の無効化確認（MA-07 防止）
  - アニメーションのみで状態変化伝達 → 冗長な情報提供追加（MA-04 防止）
```

**Source:** [Smashing Magazine: Respecting Motion Preferences](https://www.smashingmagazine.com/2024/10/respecting-users-motion-preferences/) · [WCAG 2.2: Understanding 2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) · [web.dev: prefers-reduced-motion](https://web.dev/articles/prefers-reduced-motion)
