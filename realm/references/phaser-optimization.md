# Phaser 3 Optimization & Best Practices

> パフォーマンス最適化、Object Pooling、Tilemap、アニメーション、バージョン更新

## 1. パフォーマンス最適化 7原則

| # | 手法 | Realm適用 |
|---|------|-----------|
| 1 | FPSカウンター | Live modeでFPS表示 |
| 2 | Object Pooling | エージェントスプライト/パーティクル再利用 |
| 3 | 参照キャッシュ | 部門/エージェントデータのキャッシュ |
| 4 | ゲームループ最適化 | 可視エリアのみ更新（カリング） |
| 5 | アセット圧縮 | テクスチャアトラス化 |
| 6 | Lazy Loading | 画面外部門の遅延ロード |
| 7 | Canvas/WebGL切替 | 低スペック機で最大30%向上 |

**Source:** [How I optimized my Phaser 3 action game — in 2025](https://franzeus.medium.com/how-i-optimized-my-phaser-3-action-game-in-2025-5a648753f62b)

---

## 2. Object Pooling

Phaser 3のGroupをObject Poolとして活用。60+エージェント環境でメモリ効率を確保。

```javascript
class AgentPool {
  constructor(scene) {
    this.pool = scene.add.group({ classType: AgentSprite, maxSize: 100, runChildUpdate: true });
  }
  spawn(data) {
    const agent = this.pool.get(data.x, data.y);
    if (agent) { agent.setActive(true).setVisible(true); agent.configure(data); }
    return agent;
  }
  despawn(agent) { this.pool.killAndHide(agent); }
}
```

**Source:** [Object Pooling Sprites in Phaser](https://www.thepolyglotdeveloper.com/2020/09/object-pooling-sprites-phaser-game-performance-gains/) · [Phaser 3 Sprite Pool](https://phaser.io/examples/v3/view/game-objects/group/sprite-pool)

---

## 3. Tilemap プロシージャルレイアウト

現在のプログラマティック描画からTilemapベースへの移行オプション。

**Room-Based Generation:**
1. 中央ロビー（Command Center）から開始
2. 協力頻度の高い部門を隣接配置（重み付けグラフ）
3. 廊下で部門間を接続

**フォグ・オブ・ウォー:** 部門に入ると上層タイル透明化、退出時にフォグ。部門ヘルスが低い部門を暗く表現。

**Source:** [Modular Game Worlds — Procedural Dungeon](https://itnext.io/modular-game-worlds-in-phaser-3-tilemaps-3-procedural-dungeon-3bc19b841cd)

---

## 4. Animation State Machine

```javascript
const AGENT_STATES = {
  idle:      { frames: [0, 1], rate: 2 },
  walk:      { frames: [2, 3, 4, 5], rate: 8 },
  work:      { frames: [6, 7], rate: 4 },
  celebrate: { frames: [8, 9, 10, 11], rate: 12 },
  battle:    { frames: [12, 13, 14], rate: 10 }
};
```

### ランク別スプライトサイズ

| ランク | サイズ | エフェクト |
|--------|--------|-----------|
| F-E | 12×12px | なし |
| D-C | 16×16px | 歩行時に影 |
| B-A | 20×20px | 常時微光 |
| S | 24×24px | ゴールドオーラ |
| SS | 28×28px | レインボーパーティクル |

**Source:** [Pixel Art Tutorial 2025](https://generalistprogrammer.com/tutorials/pixel-art-complete-tutorial-beginner-to-pro) · [Crisp pixel art - MDN](https://developer.mozilla.org/en-US/docs/Games/Techniques/Crisp_pixel_art_look)

---

## 5. Phaser 3 バージョン

| Version | Release | Notable |
|---------|---------|---------|
| 3.80 | 2024-02 | Particle Emitter改善 |
| 3.85 | 2024-09 | ParticleEmitter GameObject対応 |
| 3.87 | 2025-02 | 最新安定版 |

**Action:** CDN読み込みを3.87に更新。

**Source:** [Phaser GitHub Releases](https://github.com/phaserjs/phaser/releases)

---

## 改善優先度サマリー

| 優先度 | 改善項目 | 工数 | 効果 |
|--------|----------|------|------|
| P0 | Object Pooling導入 | 小 | パフォーマンス大幅向上 |
| P0 | Phaser CDN 3.87更新 | 極小 | バグ修正・新機能 |
| P1 | Animation State Machine | 中 | 視覚的魅力向上 |
| P1 | Canvas/WebGLフォールバック | 小 | 互換性向上 |
| P2 | Tilemap化 | 大 | レイアウト柔軟性 |
| P2 | プロシージャルスプライト | 中 | ランク差別化 |
