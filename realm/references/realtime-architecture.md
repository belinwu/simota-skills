# Real-Time Update Architecture

> SSE推奨、差分更新プロトコル、レイヤードアーキテクチャの設計ガイド

## 1. プロトコル選定: SSE 推奨

| 基準 | WebSocket | SSE | 推奨 |
|------|-----------|-----|------|
| 通信方向 | 双方向 | サーバー→クライアント | **SSE** |
| 複雑度 | 高（プロトコル管理） | 低（HTTP標準） | **SSE** |
| 自動再接続 | 手動実装必要 | ブラウザ標準搭載 | **SSE** |
| HTTP/2互換 | 別接続 | 多重化対応 | **SSE** |
| スケーリング | 専用インフラ必要 | 既存HTTPインフラ | **SSE** |

**結論:** Realm live mode はサーバー→クライアントのデータ配信が主目的。SSE が最適。

**Source:** [SSE Beat WebSockets for 95% of Real-Time Apps](https://dev.to/polliog/server-sent-events-beat-websockets-for-95-of-real-time-apps-heres-why-a4l) · [SSE vs WebSockets 2026](https://www.nimbleway.com/blog/server-sent-events-vs-websockets-what-is-the-difference-2026-guide)

### SSE サーバー実装（Python）

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio, json

app = FastAPI()

async def realm_event_stream():
    while True:
        state = await collect_ecosystem_state()
        yield f"data: {json.dumps(state)}\n\n"
        await asyncio.sleep(3)

@app.get("/events")
async def sse_endpoint():
    return StreamingResponse(
        realm_event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
```

### SSE クライアント実装

```javascript
class RealmDataBridge {
  constructor(url) {
    this.source = new EventSource(url);
    this.source.onmessage = (e) => this.dispatch(JSON.parse(e.data));
    this.source.onerror = () => console.log('[Realm] Reconnecting...');
  }
  dispatch(data) {
    // agent_update / quest_complete / rank_up 等をハンドリング
  }
}
```

---

## 2. 差分更新プロトコル

### 3層バッファリング

```
Layer 1: データ収集 (1秒) — git log, PROJECT.md, ECOSYSTEM.md の差分検出
Layer 2: バッチ集約 (3秒) — 変更時のみSSE送信、差分のみ（フル状態は初回のみ）
Layer 3: クライアント描画 (rAF) — キューイング → フレーム単位反映 → 補間遷移
```

**Source:** [Real-Time Chart Updates with Live Dashboards](https://dev.to/byte-sized-news/real-time-chart-updates-using-websockets-to-build-live-dashboards-3hml)

### プロトコル定義

```json
// 初回接続: フル状態
{ "type": "full_state", "agents": [...], "quests": [...], "departments": [...] }

// 以降: 差分のみ
{ "type": "delta", "timestamp": 1709550000, "changes": [
    { "path": "agents.builder.xp", "value": 4250 },
    { "path": "quests.Q-42.status", "value": "completed" },
    { "path": "events", "append": { "type": "Victory", "summary": "..." } }
]}
```

---

## 3. レイヤードアーキテクチャ

```
┌──────────────────────────────┐
│  Client Layer (HTML/Phaser)  │  描画・インタラクション
├──────────────────────────────┤
│  Data Bridge Layer (SSE)     │  リアルタイム通信・差分適用
├──────────────────────────────┤
│  State Manager Layer         │  realm-state.md 管理・差分計算
├──────────────────────────────┤
│  Data Collector Layer        │  git/agents/*.md 収集・変更検出
└──────────────────────────────┘
```

**Source:** [Layered WebSocket Architecture](https://medium.com/@jamala.zawia/designing-a-layered-websocket-architecture-for-scalable-real-time-systems-1ba3591e3ffb)

---

## 4. ブラウザ側データ管理

> "Browsers don't love maintaining unlimited history."

- 直近100イベントのみ保持
- エージェント統計は最新値のみ（履歴はサーバー側）
- クエスト履歴は完了後50件のみ

**Source:** [Building Real-Time Dashboards with Node.js](https://blog.openreplay.com/real-time-dashboards-nodejs/)

---

## 改善優先度サマリー

| 優先度 | 改善項目 | 工数 | 効果 |
|--------|----------|------|------|
| P0 | WebSocket → SSE 移行 | 中 | 複雑度削減・信頼性向上 |
| P0 | 差分更新プロトコル | 中 | 帯域削減・応答性向上 |
| P1 | 3層バッファリング | 小 | 描画パフォーマンス向上 |
| P2 | レイヤードアーキテクチャ | 大 | 保守性向上 |
