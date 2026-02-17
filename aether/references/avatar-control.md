# Avatar Control

Live2D Cubism SDK / VRM アバター制御、パラメータマッピング、アイドルモーション設計。

---

## Framework Comparison

| Feature | Live2D Cubism SDK for Web | VRM (@pixiv/three-vrm) |
|---------|---------------------------|------------------------|
| **Model format** | .moc3 + .model3.json | .vrm (glTF extension) |
| **Rendering** | WebGL (Cubism Core) | Three.js + WebGL |
| **2D / 3D** | 2D (layered mesh deformation) | 3D (skeletal animation) |
| **Expression system** | Parameter-based (0.0–1.0) | BlendShape preset + custom |
| **Lip sync** | Mouth open parameter | Viseme BlendShapes (aa/ih/ou/ee/oh) |
| **Physics** | Built-in physics (hair, clothes) | Spring bone (VRM extension) |
| **Idle motion** | Motion files (.motion3.json) | VRM Animation / custom |
| **Community** | VTuber standard (JP) | Open standard (cross-platform) |
| **License** | Cubism SDK License (free for indie) | MIT (three-vrm) |
| **Model availability** | nizima, BOOTH | VRoid Hub, BOOTH |
| **Recommended for** | 2D VTuber (traditional style) | 3D VTuber (full body) |

---

## Live2D Cubism SDK for Web

### Parameter Control

Live2D models are controlled by named parameters with float values.

| Parameter ID | Range | Description |
|-------------|-------|-------------|
| `ParamAngleX` | -30 to 30 | Head rotation left/right |
| `ParamAngleY` | -30 to 30 | Head rotation up/down |
| `ParamAngleZ` | -30 to 30 | Head tilt |
| `ParamBodyAngleX` | -10 to 10 | Body rotation |
| `ParamEyeLOpen` | 0 to 1 | Left eye open |
| `ParamEyeROpen` | 0 to 1 | Right eye open |
| `ParamEyeBallX` | -1 to 1 | Eye gaze horizontal |
| `ParamEyeBallY` | -1 to 1 | Eye gaze vertical |
| `ParamBrowLY` | -1 to 1 | Left eyebrow position |
| `ParamBrowRY` | -1 to 1 | Right eyebrow position |
| `ParamMouthOpenY` | 0 to 1 | Mouth open amount |
| `ParamMouthForm` | -1 to 1 | Mouth shape (-1=frown, 1=smile) |

### Setup (Cubism SDK for Web)

```typescript
import { CubismFramework } from '@cubism-sdk/framework';

// Initialize
CubismFramework.startUp();
CubismFramework.initialize();

// Load model
const model = await loadModel('model.model3.json');

// Set parameter
model.setParameterValueById('ParamMouthOpenY', 0.8);
model.setParameterValueById('ParamMouthForm', 0.5);

// Update and render (per frame)
function animate() {
  model.update();
  renderer.draw(model);
  requestAnimationFrame(animate);
}
```

### Motion System

```typescript
// Play motion file
const motion = await loadMotion('idle.motion3.json');
model.startMotion(motion, {
  group: 'idle',
  priority: 2,  // 1=idle, 2=normal, 3=force
  onFinish: () => { /* return to idle */ },
});

// Motion priority levels
// 1 (Idle) — continuous background motion
// 2 (Normal) — triggered by events, blends with idle
// 3 (Force) — overrides everything (reactions, emotions)
```

---

## VRM (@pixiv/three-vrm)

### BlendShape Control

VRM models use BlendShape presets for facial expressions.

| Preset | Description | Typical Usage |
|--------|-------------|---------------|
| `happy` | 笑顔 | Joy emotion |
| `angry` | 怒り | Anger emotion |
| `sad` | 悲しみ | Sad emotion |
| `relaxed` | リラックス | Neutral/calm |
| `surprised` | 驚き | Surprise emotion |
| `aa` | 口形状「あ」 | Lip sync vowel A |
| `ih` | 口形状「い」 | Lip sync vowel I |
| `ou` | 口形状「う」 | Lip sync vowel U |
| `ee` | 口形状「え」 | Lip sync vowel E |
| `oh` | 口形状「お」 | Lip sync vowel O |
| `blink` | 瞬き | Auto-blink |
| `blinkLeft` | 左ウィンク | Expression |
| `blinkRight` | 右ウィンク | Expression |
| `lookUp/Down/Left/Right` | 視線 | Gaze direction |

### Setup (three-vrm)

```typescript
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { VRMLoaderPlugin, VRM } from '@pixiv/three-vrm';

const loader = new GLTFLoader();
loader.register((parser) => new VRMLoaderPlugin(parser));

const gltf = await loader.loadAsync('model.vrm');
const vrm: VRM = gltf.userData.vrm;
scene.add(vrm.scene);

// Set expression
vrm.expressionManager?.setValue('happy', 0.8);
vrm.expressionManager?.setValue('aa', 1.0);  // Lip sync

// Update (per frame)
function animate() {
  vrm.update(clock.getDelta());
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

---

## Emotion → Expression Mapping

チャットメッセージの感情分析結果をアバター表情パラメータに変換するマッピングテーブル。

### Live2D Expression Map

| Emotion | ParamEyeLOpen | ParamEyeROpen | ParamBrowLY | ParamBrowRY | ParamMouthForm | ParamMouthOpenY |
|---------|-------------|-------------|-----------|-----------|--------------|---------------|
| **Neutral** | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **Joy** | 0.8 | 0.8 | 0.3 | 0.3 | 0.8 | 0.3 |
| **Sad** | 0.6 | 0.6 | -0.5 | -0.5 | -0.5 | 0.0 |
| **Angry** | 0.9 | 0.9 | -0.7 | -0.7 | -0.3 | 0.2 |
| **Surprised** | 1.0 | 1.0 | 0.8 | 0.8 | 0.0 | 0.7 |
| **Thinking** | 0.7 | 0.9 | 0.2 | -0.2 | 0.0 | 0.0 |

### VRM Expression Map

| Emotion | happy | angry | sad | surprised | relaxed | Custom blendshapes |
|---------|-------|-------|-----|-----------|---------|-------------------|
| **Neutral** | 0.0 | 0.0 | 0.0 | 0.0 | 0.3 | — |
| **Joy** | 0.8 | 0.0 | 0.0 | 0.0 | 0.2 | — |
| **Sad** | 0.0 | 0.0 | 0.7 | 0.0 | 0.0 | — |
| **Angry** | 0.0 | 0.8 | 0.0 | 0.0 | 0.0 | — |
| **Surprised** | 0.0 | 0.0 | 0.0 | 0.9 | 0.0 | — |
| **Thinking** | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | lookUp: 0.3 |

### Expression Transition

表情は瞬時に切り替えず、スムーズに遷移させる。

```typescript
class ExpressionTransitioner {
  private current: Record<string, number> = {};
  private target: Record<string, number> = {};
  private transitionSpeed = 0.1; // 0-1, higher = faster

  setTarget(expression: Record<string, number>): void {
    this.target = { ...expression };
  }

  update(deltaTime: number): Record<string, number> {
    for (const [key, targetValue] of Object.entries(this.target)) {
      const current = this.current[key] ?? 0;
      const diff = targetValue - current;
      this.current[key] = current + diff * Math.min(this.transitionSpeed * deltaTime * 60, 1);
    }
    return { ...this.current };
  }
}
```

---

## Idle Motion Design

配信中、メッセージ処理していない時のアバター自然な動き。

### Idle Behaviors

| Behavior | Frequency | Duration | Parameters |
|----------|-----------|----------|------------|
| **Auto-blink** | 3-5s interval | 150ms | EyeLOpen/ROpen: 1→0→1 |
| **Breathing** | Continuous | 4s cycle | BodyAngleX: ±1, scale ±0.02 |
| **Head sway** | Continuous | 6-8s cycle | AngleX: ±3, AngleY: ±2 |
| **Eye wander** | 5-10s interval | 1-2s | EyeBallX/Y: random ±0.3 |
| **Micro expression** | 15-30s interval | 2-3s | MouthForm: 0→0.2→0 (slight smile) |

### Implementation Pattern

```typescript
class IdleAnimator {
  private time = 0;

  update(deltaTime: number): Record<string, number> {
    this.time += deltaTime;

    return {
      // Breathing (sine wave, 4s period)
      bodyScale: 1 + Math.sin(this.time * Math.PI * 0.5) * 0.02,

      // Head sway (slow sine, 7s period)
      headAngleX: Math.sin(this.time * Math.PI * 2 / 7) * 3,
      headAngleY: Math.sin(this.time * Math.PI * 2 / 9) * 2,

      // Auto-blink (periodic, ~4s interval)
      eyeOpen: this.calculateBlink(this.time),
    };
  }

  private calculateBlink(time: number): number {
    const blinkInterval = 4;
    const blinkDuration = 0.15;
    const t = time % blinkInterval;
    if (t < blinkDuration) {
      // Close and open
      return t < blinkDuration / 2
        ? 1 - (t / (blinkDuration / 2))
        : (t - blinkDuration / 2) / (blinkDuration / 2);
    }
    return 1;
  }
}
```
