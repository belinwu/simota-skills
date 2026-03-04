# Celebration & Visual Effects

> canvas-confetti（HTML Map）、Phaser Particles（Game Mode）、CSSアニメーションの実装ガイド

## 1. ライブラリ選定

| ライブラリ | サイズ | 用途 |
|-----------|--------|------|
| **canvas-confetti** | 6KB | HTML map（CDN、依存なし、位置指定バースト） |
| **Phaser Particles** | 内蔵 | Game mode（GameObjectとして管理） |

**Source:** [canvas-confetti](https://github.com/catdad/canvas-confetti) · [tsParticles](https://confetti.js.org/)

---

## 2. canvas-confetti（HTML Map用）

```html
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
```

### イベント別エフェクト

| イベント | パーティクル数 | 色 |
|---------|--------------|-----|
| Rank Up F→E | 30 | 白 |
| Rank Up E→D | 60 | 緑 |
| Rank Up D→C | 100 | 青 |
| Rank Up C→B | 150 | 紫 |
| Rank Up B→A | 200 | ゴールド |
| Rank Up A→S | 400 | ゴールド+レッド |
| Rank Up S→SS | 1000（10秒連続） | レインボー |
| Badge (Rare+) | 80 | バッジ色+金 |
| Quest Complete | 100（下→上噴水） | レアリティ色 |

### 実装

```javascript
const RealmCelebration = {
  rankUp(rank, element) {
    const rect = element?.getBoundingClientRect();
    const origin = rect
      ? { x: (rect.left + rect.width/2) / innerWidth, y: (rect.top + rect.height/2) / innerHeight }
      : { x: 0.5, y: 0.6 };
    const configs = {
      E: { particleCount: 30, spread: 40, colors: ['#FFFFFF'] },
      D: { particleCount: 60, spread: 50, colors: ['#4CAF50'] },
      C: { particleCount: 100, spread: 60, colors: ['#2196F3'] },
      B: { particleCount: 150, spread: 70, colors: ['#9C27B0'] },
      A: { particleCount: 200, spread: 80, colors: ['#FFD700'] },
      S: { particleCount: 400, spread: 100, colors: ['#FFD700', '#FF5722'] },
      SS: null
    };
    if (rank === 'SS') return this._legendaryFireworks();
    confetti({ ...configs[rank], origin, zIndex: 9999 });
  },

  _legendaryFireworks() {
    const end = Date.now() + 10000;
    const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'];
    (function frame() {
      confetti({ particleCount: 5, angle: 60, spread: 55, origin: { x: 0 }, colors });
      confetti({ particleCount: 5, angle: 120, spread: 55, origin: { x: 1 }, colors });
      if (Date.now() < end) requestAnimationFrame(frame);
    })();
  },

  questComplete(rarity) {
    const colors = { Common: ['#FFF'], Uncommon: ['#4CAF50'], Rare: ['#2196F3'], Epic: ['#9C27B0'], Legendary: ['#FFD700', '#FF5722'] };
    confetti({ particleCount: 100, spread: 70, origin: { y: 1 }, gravity: 1.5, colors: colors[rarity], zIndex: 9999 });
  }
};
```

---

## 3. Phaser 3 パーティクル（Game Mode用）

```javascript
class CelebrationManager {
  constructor(scene) {
    this.scene = scene;
    // テクスチャ事前生成
    const gfx = scene.make.graphics({ add: false });
    gfx.fillStyle(0xffffff).fillCircle(4, 4, 4);
    gfx.generateTexture('particle_dot', 8, 8);
    gfx.destroy();
  }

  rankUp(x, y, rank) {
    const colors = { E: [0xCCCCCC], D: [0x4CAF50], C: [0x2196F3], B: [0x9C27B0], A: [0xFFD700], S: [0xFFD700, 0xFF5722], SS: [0xFFD700, 0xFF6B6B, 0x4ECDC4] };
    const ri = ['F','E','D','C','B','A','S','SS'].indexOf(rank);
    const emitter = this.scene.add.particles(x, y, 'particle_dot', {
      speed: { min: 50, max: 200 + ri * 50 }, scale: { start: 0.6, end: 0 },
      lifespan: { min: 1000, max: 2000 }, tint: colors[rank], emitting: false
    });
    emitter.explode(20 + ri * 20);

    const text = this.scene.add.text(x, y - 40, `RANK ${rank}!`, {
      fontFamily: '"Press Start 2P"', fontSize: '16px', color: '#FFD700', stroke: '#000', strokeThickness: 4
    }).setOrigin(0.5);
    this.scene.tweens.add({ targets: text, y: y - 100, alpha: 0, scale: 1.5, duration: 2000, ease: 'Power2', onComplete: () => text.destroy() });
    this.scene.time.delayedCall(3000, () => emitter.destroy());
  }

  createAura(sprite, rank) {
    const ri = ['F','E','D','C','B','A','S','SS'].indexOf(rank);
    if (ri < 4) return null; // B未満はオーラなし
    const colors = { B: 0x9C27B0, A: 0xFFD700, S: 0xFF5722, SS: 0x4ECDC4 };
    return this.scene.add.particles(0, 0, 'particle_dot', {
      speed: { min: 5, max: 15 }, scale: { start: 0.3, end: 0 }, lifespan: 800,
      frequency: rank === 'SS' ? 50 : 100, tint: colors[rank], follow: sprite, blendMode: 'ADD'
    });
  }
}
```

---

## 4. CSS アニメーション（HTML Map用）

```css
/* ランクアップトースト */
@keyframes slide-in-bounce {
  0% { transform: translateX(100%); opacity: 0; }
  60% { transform: translateX(-10px); opacity: 1; }
  100% { transform: translateX(0); }
}
@keyframes rankup-glow {
  0%, 100% { box-shadow: 0 0 5px var(--rank-color); }
  50% { box-shadow: 0 0 30px var(--rank-color); transform: scale(1.05); }
}
.toast-rankup { animation: slide-in-bounce 0.6s ease-out, rankup-glow 2s ease-in-out 0.6s 3; }

/* XPゲインポップアップ */
@keyframes xp-float {
  0% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-60px) scale(1.3); }
}
.xp-gain {
  position: absolute; font-family: 'Press Start 2P', monospace; font-size: 12px;
  color: #FFD700; text-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
  animation: xp-float 1.5s ease-out forwards; pointer-events: none;
}

/* アクティブクエスト中のエージェントカード */
.agent-card.active-quest { animation: 2s ease-in-out infinite alternate; border-left: 3px solid var(--quest-rarity-color); }
```

---

## 改善優先度サマリー

| 優先度 | 改善項目 | 工数 | 対象 |
|--------|----------|------|------|
| P0 | canvas-confetti統合 | 極小 | HTML Map |
| P0 | CSSトースト通知 | 小 | HTML Map |
| P1 | Phaser Particle統合 | 小 | Game Mode |
| P1 | XPゲインポップアップ | 極小 | 両方 |
| P2 | 常時オーラエフェクト | 中 | Game Mode |
