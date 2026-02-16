# Prompt Patterns Reference

Sketch エージェントのプロンプトエンジニアリング詳細リファレンス。

---

## Prompt Architecture

すべてのプロンプトは4層構造で構築する：

```
[Subject] + [Style] + [Composition] + [Technical]
```

### Layer Details

| Layer | Role | Weight | Examples |
|-------|------|--------|----------|
| **Subject** | 何を描くか（主題・被写体） | 40% | "A minimalist home office desk", "A mountain landscape at sunset" |
| **Style** | どんな雰囲気・表現か | 30% | "photorealistic, cinematic lighting", "watercolor, soft pastels" |
| **Composition** | 構図・視点・配置 | 20% | "centered, rule of thirds", "bird's eye view, symmetrical" |
| **Technical** | 品質・技術的指示 | 10% | "8K detail, sharp focus", "studio lighting, color graded" |

### Construction Order

1. **Subject first**: 最も重要な要素を先頭に配置
2. **Style modifiers**: 主題の直後にスタイル指定
3. **Composition details**: 構図・カメラアングル
4. **Technical quality**: 品質向上キーワード（末尾に配置）

---

## Style Preset Library

### Photorealistic

```
photorealistic, natural lighting, detailed textures, DSLR quality,
sharp focus, high dynamic range, color accurate
```

**Variations:**
- **Studio**: professional studio lighting, white background, product photography
- **Natural**: golden hour lighting, environmental portrait, natural colors
- **Editorial**: magazine quality, color graded, dramatic lighting
- **Documentary**: candid, authentic, natural moment, available light

### Digital Illustration

```
digital illustration, clean lines, vibrant colors, flat design,
modern graphic style, vector-like quality
```

**Variations:**
- **Flat Design**: minimal shadows, bold colors, geometric shapes, clean edges
- **Semi-realistic**: painterly style, visible brush strokes, rich details
- **Line Art**: detailed line work, minimal color, pen and ink style
- **Pixel Art**: pixel art, retro style, 16-bit, limited palette

### 3D Render

```
3D render, isometric view, clean geometry, soft shadows,
ambient occlusion, physically based rendering
```

**Variations:**
- **Isometric**: isometric perspective, clean edges, flat lighting
- **Clay Render**: clay material, matte surface, neutral colors, soft shadows
- **Low Poly**: low polygon, geometric, stylized, colorful facets
- **Realistic 3D**: photorealistic 3D render, ray tracing, caustics, PBR materials

### Watercolor

```
watercolor painting, soft edges, translucent layers, paper texture,
bleeding colors, organic flow, hand-painted quality
```

### Abstract / Conceptual

```
abstract composition, geometric shapes, bold color palette,
minimalist design, conceptual art, visual metaphor
```

### Additional Styles

| Style | Core Keywords |
|-------|--------------|
| **Oil Painting** | oil painting, canvas texture, impasto, rich colors, classical lighting |
| **Anime/Manga** | anime style, cel shading, large expressive eyes, vibrant |
| **Vintage/Retro** | vintage, film grain, faded colors, 1970s aesthetic, warm tones |
| **Cyberpunk** | neon lighting, dark atmosphere, futuristic, rain-slicked streets, holographic |
| **Art Nouveau** | ornamental, flowing lines, organic forms, decorative borders |
| **Minimalist** | minimalist, negative space, simple shapes, monochromatic, clean |

---

## Domain-Specific Templates

### Marketing / Hero Images

```
[Product/Scene], professional commercial photography,
hero image composition, clean background, brand-appropriate lighting,
advertising quality, high-end retouching, [aspect: 16:9 or 21:9]
```

**Use cases**: Landing page heroes, banner ads, social media covers

### Product Photography

```
[Product] on [surface/background], studio product photography,
soft box lighting, slight reflection, clean minimal composition,
e-commerce quality, white/neutral background, [aspect: 1:1 or 4:3]
```

**Use cases**: E-commerce listings, catalog images, product showcases

### UI/UX Assets

```
[UI element/icon/illustration], flat design, UI-ready,
consistent line weight, [brand color] palette, scalable,
clean edges, transparent-ready, [aspect: 1:1]
```

**Use cases**: App icons, feature illustrations, onboarding graphics

### Documentation / Technical

```
[Concept visualization], clean infographic style,
explanatory illustration, clear visual hierarchy,
professional documentation quality, [aspect: 16:9 or 4:3]
```

**Use cases**: Technical docs, blog headers, presentation slides

### Social Media

```
[Subject], eye-catching social media post,
vibrant colors, bold composition, scroll-stopping visual,
[platform-specific aspect ratio]
```

| Platform | Aspect Ratio | Notes |
|----------|-------------|-------|
| Instagram Post | 1:1 | Square, high visual impact |
| Instagram Story | 9:16 | Vertical, full-screen |
| Twitter/X | 16:9 | Horizontal, preview-friendly |
| LinkedIn | 4:3 | Professional, clean |
| YouTube Thumbnail | 16:9 | Bold text-ready, high contrast |

### Backgrounds / Textures

```
[Type] seamless texture, tileable pattern, high resolution,
subtle variation, [color scheme], material quality,
[aspect: 1:1]
```

**Types**: marble, wood grain, fabric, concrete, gradient, bokeh, nature

---

## Quality Enhancement Techniques

### Lighting

| Technique | Keywords | Effect |
|-----------|----------|--------|
| **Golden Hour** | golden hour, warm sunset light | Warm, inviting atmosphere |
| **Blue Hour** | blue hour, twilight, cool tones | Moody, serene feeling |
| **Studio** | studio lighting, 3-point lighting, softbox | Professional, controlled |
| **Rim Light** | rim lighting, backlit, edge glow | Dramatic subject separation |
| **Diffused** | soft diffused light, overcast | Even, flattering illumination |
| **Dramatic** | chiaroscuro, strong shadows, spotlight | High contrast, theatrical |

### Camera / Perspective

| Technique | Keywords | Best For |
|-----------|----------|----------|
| **Close-up** | macro, extreme close-up, detail shot | Textures, products |
| **Wide Angle** | wide angle, expansive, panoramic | Landscapes, architecture |
| **Shallow DOF** | shallow depth of field, bokeh, f/1.4 | Portraits, product focus |
| **Tilt-Shift** | tilt-shift, miniature effect | Urban scenes, playful |
| **Aerial** | aerial view, drone shot, bird's eye | Maps, environments |
| **Eye Level** | eye level, straight-on, natural perspective | General purpose |

### Material / Texture

| Keywords | Effect |
|----------|--------|
| detailed textures, surface quality | More realistic surfaces |
| glossy, reflective, metallic | Shiny materials |
| matte, soft touch, organic | Natural materials |
| translucent, glass, crystal | See-through materials |
| weathered, aged, patina | Worn/vintage feel |

---

## Japanese → English Translation Patterns

日本語プロンプトを高品質な英語プロンプトに変換するパターン：

### Basic Translation Rules

1. **主語を明示**: 日本語の省略された主語を補完
2. **形容詞を具体化**: 「きれいな」→ "elegant, well-composed" (文脈依存)
3. **雰囲気を英語キーワードに**: 「やわらかい」→ "soft, gentle, diffused"
4. **技術用語は英語維持**: 「ボケ」→ "bokeh", 「ハイキー」→ "high-key"

### Common Mappings

| 日本語 | English Keywords |
|--------|-----------------|
| かわいい | cute, adorable, charming, kawaii-style |
| かっこいい | cool, stylish, sleek, dynamic |
| おしゃれ | fashionable, trendy, chic, sophisticated |
| あたたかい（雰囲気） | warm, cozy, inviting, golden tones |
| クール | cool tones, blue palette, modern, minimal |
| レトロ | vintage, retro, nostalgic, film-like |
| ナチュラル | natural, organic, earthy, authentic |
| シンプル | minimalist, clean, simple, uncluttered |
| ダイナミック | dynamic, energetic, motion blur, bold angles |
| 幻想的 | ethereal, dreamy, fantasy, soft glow |
| 荘厳 | majestic, grand, imposing, awe-inspiring |
| 繊細 | delicate, intricate, fine detail, subtle |

### Translation Example

**Input (日本語)**:
> やわらかい光のなかで、木のテーブルの上にコーヒーとノートパソコンがある、おしゃれなワークスペース

**Output (English prompt)**:
> A stylish modern workspace with a laptop and coffee cup on a wooden table, soft diffused natural lighting, cozy atmosphere, shallow depth of field, warm tones, lifestyle photography, 8K detail

---

## Content Policy Compliance Guide

### Safe Prompt Patterns

| Category | Safe Approach | Avoid |
|----------|--------------|-------|
| **People** | "silhouette of a person", "illustrated character" | Real individuals by name |
| **Workplace** | "professional office environment" | Specific company logos |
| **Nature** | "serene forest landscape" | Endangered species exploitation |
| **Food** | "gourmet dish, professional food photography" | — |
| **Architecture** | "modern building facade" | Copyrighted buildings (some) |

### Fallback Strategy

When a prompt is flagged:
1. Remove potentially sensitive keywords
2. Replace specific references with generic descriptions
3. Add positive framing keywords
4. Attempt with simplified prompt
5. If still blocked, suggest alternative concept

---

## Prompt Quality Checklist

Before finalizing any prompt:

- [ ] Subject is clearly defined and specific
- [ ] Style keywords are consistent (not conflicting styles)
- [ ] Aspect ratio matches the intended use case
- [ ] No copyrighted character/brand references (unless explicitly requested)
- [ ] Person generation policy is considered
- [ ] English language used for optimal generation quality
- [ ] Technical quality keywords included
- [ ] Prompt length is 50-200 words (optimal range for Gemini)

---

## Negative Prompt Patterns

よくある失敗パターンとその回避策。SKILL.md の要約版に対する詳細リファレンス。

### Style Conflicts（矛盾するスタイル）

| Bad Prompt | Problem | Fix |
|-----------|---------|-----|
| "photorealistic watercolor painting" | フォトリアルと水彩は矛盾 | スタイルを1つに統一: "watercolor painting, soft edges" |
| "minimalist detailed ornamental" | ミニマルと装飾的は矛盾 | 方向性を選択: "minimalist, clean, simple" |
| "bright dark moody cheerful" | 明暗・雰囲気が矛盾 | トーンを統一: "moody, dark, dramatic lighting" |

### Prompt Length Issues（長さの問題）

| Problem | Symptom | Guideline |
|---------|---------|-----------|
| < 20語 | 曖昧で汎用的な結果 | 最低50語を目指す |
| 50–200語 ★ | 最適な品質と制御 | このレンジを維持 |
| > 200語 | 主題がぼやける、品質低下 | 重要度順に削減、Technical 層を厳選 |
| > 500語 | API がキーワードを無視し始める | 大幅に削減が必要 |

### Ineffective Patterns（効果のないパターン）

| Pattern | Why It Fails | Better Approach |
|---------|-------------|-----------------|
| "NOT a photo of..." | ネガティブ指示は効きにくい | ポジティブに: "illustration of..." |
| "Don't include people" | 否定形は無視されがち | "empty scene, no figures, landscape only" |
| "ultra mega super high quality" | 修飾語の重複は効果なし | "8K detail, sharp focus" で十分 |
| "like the Mona Lisa" | 著作権リスク + 曖昧 | 具体的特徴を記述: "portrait, soft sfumato, warm tones" |
| "beautiful amazing stunning" | 主観的すぎて効果なし | 具体的技術指示に置換 |

### Quality Keyword Best Practices

**効果的な品質キーワード（3–5個を厳選）:**

```
# Good — 具体的で互いに補完
"8K detail, sharp focus, professional color grading, studio lighting"

# Bad — 冗長で効果が相殺
"ultra high quality, best quality, masterpiece, extremely detailed, very high resolution, incredibly sharp, amazingly beautiful, award-winning"
```

---

## SDK v1.50+ ImageGenerationConfig

SDK v1.50 以降で利用可能な `ImageGenerationConfig` パラメータの活用パターン。

### Basic Usage

```python
from google.genai import types

config = types.GenerateContentConfig(
    response_modalities=["IMAGE"],
    image_generation_config=types.ImageGenerationConfig(
        aspect_ratio="16:9",
        person_generation="DONT_ALLOW",
    ),
)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A modern workspace with natural lighting",
    config=config,
)
```

### Available Parameters

| Parameter | Type | Values | Default |
|-----------|------|--------|---------|
| `aspect_ratio` | string | `"1:1"`, `"3:2"`, `"2:3"`, `"16:9"`, `"9:16"`, `"21:9"` | Model default |
| `person_generation` | string | `"DONT_ALLOW"`, `"ALLOW_ADULT"` | `"DONT_ALLOW"` |

### v1.38 vs v1.50+ Comparison

```python
# SDK v1.38+ — アスペクト比はプロンプトで指示
config_v138 = types.GenerateContentConfig(
    response_modalities=["IMAGE"],
)
prompt_v138 = "A landscape photo, widescreen 16:9 composition, no people"

# SDK v1.50+ — パラメータで制御（より確実）
config_v150 = types.GenerateContentConfig(
    response_modalities=["IMAGE"],
    image_generation_config=types.ImageGenerationConfig(
        aspect_ratio="16:9",
        person_generation="DONT_ALLOW",
    ),
)
prompt_v150 = "A landscape photo"  # アスペクト比・人物制御はパラメータ側で
```

> **推奨**: SDK v1.50+ が利用可能な場合は `ImageGenerationConfig` でアスペクト比・人物生成を制御し、プロンプトは Subject + Style に集中させる。
