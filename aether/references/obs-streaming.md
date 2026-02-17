# OBS & Streaming

obs-websocket-js v5 制御、シーン管理、RTMP/SRT 比較、配信自動化。

---

## obs-websocket-js v5

### Connection

```typescript
import OBSWebSocket from 'obs-websocket-js';

const obs = new OBSWebSocket();

// Connect (OBS WebSocket server default port: 4455)
await obs.connect('ws://localhost:4455', 'password');

// Disconnect
await obs.disconnect();

// Auto-reconnect pattern
class OBSConnection {
  private obs = new OBSWebSocket();
  private reconnecting = false;

  async connect(): Promise<void> {
    try {
      await this.obs.connect('ws://localhost:4455', process.env.OBS_WS_PASSWORD);
      this.obs.on('ConnectionClosed', () => this.handleDisconnect());
    } catch (err) {
      await this.handleDisconnect();
    }
  }

  private async handleDisconnect(): Promise<void> {
    if (this.reconnecting) return;
    this.reconnecting = true;
    let delay = 1000;
    while (true) {
      try {
        await new Promise(r => setTimeout(r, delay));
        await this.obs.connect('ws://localhost:4455', process.env.OBS_WS_PASSWORD);
        this.reconnecting = false;
        return;
      } catch {
        delay = Math.min(delay * 2, 30000);
      }
    }
  }
}
```

---

## Scene Management

### Scene Definitions

| Scene | Purpose | Sources | Transition |
|-------|---------|---------|------------|
| **Starting** | Pre-stream countdown | Countdown image, BGM audio | Fade (1s) |
| **Main** | Active streaming | Avatar (browser), Chat overlay, Game capture, BGM | Cut |
| **BRB** | Break | BRB animation, BGM, Chat overlay (optional) | Fade (1s) |
| **Ending** | Stream end | Credits, Follow CTA, BGM | Fade (2s) |
| **Emergency** | Technical issues | Static image, "Technical Difficulties" text | Cut (instant) |

### Scene Switching

```typescript
// Switch to scene
await obs.call('SetCurrentProgramScene', { sceneName: 'Main' });

// Get current scene
const { currentProgramSceneName } = await obs.call('GetCurrentProgramScene');

// List all scenes
const { scenes } = await obs.call('GetSceneList');
```

### Source Control

```typescript
// Toggle source visibility
await obs.call('SetSceneItemEnabled', {
  sceneName: 'Main',
  sceneItemId: chatOverlayId,
  sceneItemEnabled: true,
});

// Get source ID by name
const { sceneItemId } = await obs.call('GetSceneItemId', {
  sceneName: 'Main',
  sourceName: 'ChatOverlay',
});

// Set source volume (TTS audio, BGM)
await obs.call('SetInputVolume', {
  inputName: 'TTS_Audio',
  inputVolumeDb: -3.0,  // dB
});

// Mute/unmute
await obs.call('SetInputMute', {
  inputName: 'BGM',
  inputMuted: true,
});
```

---

## Audio Routing

### Audio Source Setup

| Source | Type | Purpose | Default Volume |
|--------|------|---------|----------------|
| **TTS_Audio** | Media source / Audio pipe | TTS output | 0 dB |
| **BGM** | Media source | Background music | -15 dB |
| **SFX** | Media source | Sound effects (alerts, transitions) | -10 dB |
| **Mic** | Audio input capture | Fallback / manual override | -∞ (muted) |

### TTS Audio Integration

```
Option 1: Virtual Audio Cable
  TTS process → Virtual Audio Device → OBS Audio Input Capture
  Pros: Simple, low latency
  Cons: Platform-specific setup (VB-CABLE on Windows, BlackHole on macOS)

Option 2: Media Source with file
  TTS process → Write WAV file → OBS Media Source (file monitoring)
  Pros: Cross-platform, reliable
  Cons: Small delay for file I/O

Option 3: Browser Source with Web Audio API
  TTS process → WebSocket → Browser Source → Web Audio API playback
  Pros: Flexible, integrated with avatar
  Cons: Additional WebSocket overhead

Recommendation: Option 3 for integrated avatar+audio in browser source
```

### BGM Management

```typescript
// Auto-lower BGM during TTS playback (ducking)
class AudioDucker {
  private normalBGMVolume = -15;  // dB
  private duckedBGMVolume = -25;  // dB
  private transitionTime = 300;   // ms

  async onTTSStart(): Promise<void> {
    await obs.call('SetInputVolume', {
      inputName: 'BGM',
      inputVolumeDb: this.duckedBGMVolume,
    });
  }

  async onTTSEnd(): Promise<void> {
    // Slight delay before restoring volume
    await new Promise(r => setTimeout(r, 200));
    await obs.call('SetInputVolume', {
      inputName: 'BGM',
      inputVolumeDb: this.normalBGMVolume,
    });
  }
}
```

---

## RTMP vs SRT Comparison

| Feature | RTMP | SRT |
|---------|------|-----|
| **Protocol** | TCP-based | UDP-based |
| **Latency** | 2-5 seconds | 0.5-2 seconds |
| **Packet loss handling** | TCP retransmit (slow) | ARQ + FEC (fast) |
| **Encryption** | RTMPS (TLS) | AES-128/256 built-in |
| **Firewall** | Port 1935 | Configurable port |
| **Platform support** | YouTube ✅, Twitch ✅ | YouTube ✅, Twitch ❌ (ingest only partial) |
| **OBS support** | ✅ Native | ✅ Native |
| **Bandwidth adaptation** | Limited | ✅ Built-in |
| **Recommended for** | Standard streaming, maximum compatibility | Low-latency streaming, unstable networks |

### OBS Stream Settings

```
RTMP:
  Server: rtmp://a.rtmp.youtube.com/live2
  Stream Key: {youtube_stream_key}

SRT:
  Server: srt://a.srt.youtube.com:9710
  Stream Key: (embedded in SRT URL as streamid)

  Full SRT URL format:
  srt://a.srt.youtube.com:9710?streamid={stream_key}&latency=2000000
```

---

## Streaming Automation

### Stream Lifecycle

```typescript
class StreamLifecycle {
  async startStream(): Promise<void> {
    // 1. Switch to Starting scene
    await obs.call('SetCurrentProgramScene', { sceneName: 'Starting' });

    // 2. Start streaming
    await obs.call('StartStream');

    // 3. Start recording (for archive)
    await obs.call('StartRecord');

    // 4. Wait for countdown (configurable)
    await new Promise(r => setTimeout(r, 60_000)); // 1 min countdown

    // 5. Switch to Main scene
    await obs.call('SetCurrentProgramScene', { sceneName: 'Main' });
  }

  async endStream(): Promise<void> {
    // 1. Switch to Ending scene
    await obs.call('SetCurrentProgramScene', { sceneName: 'Ending' });

    // 2. Wait for ending screen
    await new Promise(r => setTimeout(r, 30_000)); // 30s ending

    // 3. Stop streaming
    await obs.call('StopStream');

    // 4. Stop recording
    await obs.call('StopRecord');
  }

  async emergencyStop(): Promise<void> {
    // Immediate switch to Emergency scene
    await obs.call('SetCurrentProgramScene', { sceneName: 'Emergency' });
    // Do NOT stop stream — allow recovery
  }
}
```

### Health Monitoring

```typescript
// OBS stats monitoring
const stats = await obs.call('GetStats');
// stats.cpuUsage, stats.memoryUsage, stats.activeFps,
// stats.renderSkippedFrames, stats.outputSkippedFrames

// Stream status
const streamStatus = await obs.call('GetStreamStatus');
// streamStatus.outputActive, streamStatus.outputDuration,
// streamStatus.outputBytes, streamStatus.outputSkippedFrames

// Alert on dropped frames
obs.on('StreamStateChanged', (data) => {
  if (data.outputState === 'OBS_WEBSOCKET_OUTPUT_RECONNECTING') {
    // Connection unstable — alert
  }
});
```

---

## OBS Recommended Settings

### Video Settings

| Setting | Recommended | Notes |
|---------|-------------|-------|
| Base resolution | 1920×1080 | Match monitor |
| Output resolution | 1920×1080 | Scale down to 1280×720 if GPU limited |
| FPS | 30 | 60fps only if GPU can handle avatar + encoding |
| Downscale filter | Lanczos | Best quality for downscaling |

### Output Settings (Streaming)

| Setting | RTMP | SRT |
|---------|------|-----|
| Encoder | NVENC H.264 (GPU) or x264 (CPU) | NVENC H.264 |
| Rate control | CBR | CBR |
| Bitrate | 4500-6000 kbps | 4500-6000 kbps |
| Keyframe interval | 2s | 2s |
| Profile | High | High |
| Tune | — | zerolatency |

### Browser Source Settings (Avatar)

| Setting | Value | Notes |
|---------|-------|-------|
| Width | 1920 | Match base resolution |
| Height | 1080 | Match base resolution |
| FPS | 30 | Match OBS FPS |
| Custom CSS | `body { background: transparent; }` | Transparent background for overlay |
| Shutdown when invisible | ❌ Disabled | Keep avatar running |
| Refresh when active | ❌ Disabled | Prevent reloads during stream |
