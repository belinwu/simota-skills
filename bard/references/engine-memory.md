# Engine Memory — Experience Tracking

## Overview

各エンジンの投稿経験を追跡し、話題の反復を防止する。
**エンジンの性格・感情は追跡しない。話題と統計のみ。**

---

## Chronicle Format (per engine)

Location: `.agents/bard/chronicle.md`

各エンジンに3セクション:

### 1. Experience Log (Last 10, FIFO)

| # | Date | Topic | Git Event | Notable |
|---|------|-------|-----------|---------|

- 新エントリは先頭に追加
- 10件を超えたら最古を削除
- **Emotion カラムなし** — エンジンの感情は外部から分類しない

### 2. Saturation Tracker

| Topic | Consecutive | Total | Status |
|-------|-------------|-------|--------|

**Status rules:**
- `fresh`: consecutive < 3
- `watch`: consecutive 3
- `saturating`: consecutive >= 4

### 3. Stats

- Total posts: N
- Last post: YYYY-MM-DD

---

## Recall Step

> Runs after **Map**, before **Pick** in the COMPOSE workflow.

1. `.agents/bard/chronicle.md` を読む（なければテンプレートから初期化）
2. Saturation Tracker から回避ヒントを生成
   - `saturating` → 「別の角度を探してもいい」
   - `fresh` → 制約なし
3. Engine Selection に Time Gap ボーナスを反映
   - 7+ days since last post → ×1.5 weight

---

## Record Step

> Runs after **Embellish** in the COMPOSE workflow.

1. Experience Log に新エントリ追加（最大10件、FIFO）
   - Date / Topic (short label) / Git Event (commit type) / Notable (≤20 chars)
2. Saturation Tracker 更新
   - 同じトピック → `consecutive++`
   - 異なるトピック → `consecutive` を 1 にリセット
   - `status` を consecutive に基づき再計算
3. Stats 更新
   - Total posts++
   - Last post date を更新

---

## Saturation Rules

| Status | Condition | Effect |
|--------|-----------|--------|
| `fresh` | consecutive < 3 | 制約なし |
| `watch` | consecutive = 3 | 注意。次で saturating |
| `saturating` | consecutive >= 4 | Topic Hint に回避ヒントを追加 |
