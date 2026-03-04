# Isometric Office Design

> アイソメトリック表示、エージェント行動パターン、Depth Sorting の設計ガイド

## 1. Top-Down vs Isometric

| 基準 | Top-Down | Isometric | 判定 |
|------|----------|-----------|------|
| 実装難易度 | 低 | 中〜高 | Top-Down |
| 視覚的魅力 | 普通 | 高い | **Isometric** |
| 奥行き表現 | なし | あり | **Isometric** |
| オフィス感 | 弱い | 強い（Sim/Tycoon感） | **Isometric** |
| Phaser対応 | 完全 | Tilemap標準対応 | 同等 |

**推奨: 段階的移行**
1. Phase 1: Top-Down強化（パーティクル、アニメーション追加）
2. Phase 2: `--iso` フラグでIsometric提供
3. Phase 3: デフォルト切替

**Source:** [Isometric video game graphics](https://en.wikipedia.org/wiki/Isometric_video_game_graphics) · [Fundamentals of Isometric Pixel Art](https://pixelparmesan.com/blog/fundamentals-of-isometric-pixel-art)

---

## 2. Isometric 座標変換

```javascript
const TILE_WIDTH = 64, TILE_HEIGHT = 32; // 2:1 比率

function worldToScreen(x, y) {
  return {
    screenX: (x - y) * TILE_WIDTH / 2,
    screenY: (x + y) * TILE_HEIGHT / 2
  };
}

// Phaser 3 ネイティブ対応
const map = this.make.tilemap({
  tileWidth: 64, tileHeight: 32, width: 20, height: 20,
  orientation: 'isometric'
});
```

---

## 3. 部門配置ルール

| ルール | 説明 |
|--------|------|
| 隣接性 | 協力頻度が高い部門を隣接配置 |
| 階層性 | Meta/Orchestration を上位に配置 |
| アクセス性 | Command Center を中央に固定 |
| 視認性 | 重要部門を前面に配置（depth sorting） |

---

## 4. エージェント行動パターン

```javascript
const AGENT_BEHAVIORS = {
  idle:        { animation: 'work',      probability: 0.6,  duration: [5000, 15000] },
  wander:      { animation: 'walk',      probability: 0.2,  duration: [3000, 8000] },
  collaborate: { animation: 'talk',      probability: 0.15, duration: [2000, 5000],
                 condition: (a) => a.activeQuest?.party?.length > 1 },
  celebrate:   { animation: 'celebrate', probability: 0.05, duration: [1000, 3000],
                 condition: (a) => a.recentEvent != null }
};
```

**Source:** [Office Management 101 — Woes of Isometry](https://www.indiedb.com/games/office-management-101/features/woes-of-isometry)

---

## 5. Depth Sorting

```javascript
// Phaser 3 自動ソート
this.children.sortChildrenFlag = true;

// カスタムソート: レイヤー優先 → Y座標
scene.children.sort((a, b) => {
  if (a.layer !== b.layer) return a.layer - b.layer;
  return a.y - b.y; // 手前を上に描画
});
```

---

## 6. ピクセルアートスプライト仕様

| 項目 | 仕様 |
|------|------|
| 基本サイズ | 16×16px（通常）、20-28px（高ランク） |
| カラーパレット | クラス別8色 |
| アニメフレーム | 4方向 × 4-6フレーム |
| CSS | `image-rendering: pixelated` / `crisp-edges` |

**Source:** [Crisp pixel art look - MDN](https://developer.mozilla.org/en-US/docs/Games/Techniques/Crisp_pixel_art_look)

---

## 改善優先度サマリー

| 優先度 | 改善項目 | 工数 | 効果 |
|--------|----------|------|------|
| P1 | Depth Sorting導入 | 小 | Top-Downでも効果 |
| P1 | エージェント行動パターン | 中 | 生き生きとした可視化 |
| P2 | Isometric `--iso` フラグ | 大 | 視覚的魅力大幅向上 |
| P2 | プロシージャルスプライト生成 | 中 | ランク/クラス差別化 |
| P3 | 協力ベース部門配置 | 中 | レイアウト最適化 |
