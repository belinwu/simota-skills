# API Integration Reference

Gemini API 画像生成の統合パターン詳細リファレンス。

> **動作確認環境**: google-genai SDK v1.38.0 + Google AI API（API キー認証）
> **確認済みモデル**: `gemini-2.5-flash-image`

---

## SDK Compatibility Note

| SDK Version | Config | Notes |
|-------------|--------|-------|
| **v1.38+** | `GenerateContentConfig(response_modalities=["IMAGE"])` | シンプルな config のみ。アスペクト比等はプロンプトで指示 |
| **v1.50+** | `GenerateContentConfig(image_generation_config=ImageGenerationConfig(...))` | aspect_ratio, person_generation 等を API パラメータで指定可能 |

本ドキュメントは **v1.38+ 互換**（シンプルな config）で記述。

---

## Authentication & Setup

### Python SDK (google-genai)

```python
import os
from google import genai
from google.genai import types

# API key from environment variable — NEVER hardcode
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
```

### Environment Setup

```bash
# Install SDK
pip install google-genai

# Set API key (add to .env, NOT committed to git)
export GEMINI_API_KEY="your-api-key-here"
```

### .env / .gitignore Pattern

```bash
# .env (DO NOT commit)
GEMINI_API_KEY=your-api-key-here

# .gitignore (MUST include)
.env
*.env
.env.*
```

---

## Model Specifications

| Model | ID | Speed | Cost | Best For |
|-------|-----|-------|------|----------|
| **Flash** | `gemini-2.5-flash-image` | Fast | Low | Default — Web, SNS, prototyping, iteration |

> **Note**: `imagen-3.0-*` モデルは Vertex AI 専用（Google AI API では 404）。
> Google AI API（API キー認証）では `gemini-2.5-flash-image` を使用すること。

---

## Request Patterns

### Pattern 1: Text-to-Image (Basic)

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=(
        "A modern minimalist workspace with a laptop and coffee, "
        "soft natural lighting, widescreen 16:9 composition"
    ),
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)

# Save generated image
for i, part in enumerate(response.candidates[0].content.parts):
    if part.inline_data:
        with open(f"output_{i}.png", "wb") as f:
            f.write(part.inline_data.data)
        print(f"Image saved: output_{i}.png")
```

### Pattern 2: Text-to-Image with Text Response

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="Generate an image of a sunset over mountains. Describe the scene briefly.",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    ),
)

for part in response.candidates[0].content.parts:
    if part.text:
        print(f"Description: {part.text}")
    elif part.inline_data:
        with open("sunset.png", "wb") as f:
            f.write(part.inline_data.data)
```

### Pattern 3: Image Editing (Reference-Based)

```python
from pathlib import Path

# Load reference image
ref_image_path = Path("input_image.png")
ref_image_data = ref_image_path.read_bytes()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        types.Part.from_bytes(data=ref_image_data, mime_type="image/png"),
        "Change the background to a tropical beach scene while keeping the foreground subject intact.",
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)
```

### Pattern 4: Multi-Turn Editing (Iterative)

```python
from google.genai import types

# Start chat session for iterative editing
chat = client.chats.create(
    model="gemini-2.5-flash-image",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    ),
)

# Turn 1: Initial generation
response1 = chat.send_message("Generate a cozy reading nook with warm lighting")
# Save image from response1...

# Turn 2: Edit the generated image
response2 = chat.send_message("Add a cat sleeping on the chair")
# Save updated image from response2...

# Turn 3: Further refinement
response3 = chat.send_message("Change the lighting to golden hour sunset tones")
# Save final image from response3...
```

### Pattern 5: Style Transfer (Multiple References)

```python
from pathlib import Path

# Load style reference and content image
style_image = Path("style_reference.png").read_bytes()
content_image = Path("content_photo.png").read_bytes()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        types.Part.from_bytes(data=style_image, mime_type="image/png"),
        types.Part.from_bytes(data=content_image, mime_type="image/png"),
        "Apply the artistic style of the first image to the content of the second image.",
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)
```

---

## Parameter Reference

### response_modalities

| Value | Behavior | Use Case |
|-------|----------|----------|
| `["IMAGE"]` | Image only output | Clean image generation, no text needed |
| `["TEXT", "IMAGE"]` | Text + Image output | When description/explanation is desired |

### Prompt-Based Controls

SDK v1.38 では `ImageGenerationConfig` が存在しないため、以下の制御はプロンプトで行う：

| Control | Prompt Instruction | Example |
|---------|-------------------|---------|
| **Aspect Ratio** | 構図指示をプロンプトに含める | `"widescreen 16:9 composition"` |
| **Style** | スタイルキーワードを追加 | `"photorealistic, DSLR quality"` |
| **Quality** | 品質キーワードを追加 | `"8K detail, professional photography"` |
| **No People** | 人物除外をプロンプトに明記 | `"no people, empty scene"` |
| **Orientation** | 向きを指示 | `"vertical portrait orientation"` |

### Aspect Ratio Guide (Prompt-Based)

| Ratio | Prompt Instruction | Use Case |
|-------|-------------------|----------|
| 1:1 | `"square format, 1:1 aspect ratio"` | Social media, icons, avatars |
| 3:2 | `"landscape 3:2 photography format"` | Photography standard |
| 2:3 | `"portrait 2:3 vertical format"` | Portrait, mobile |
| 16:9 | `"widescreen 16:9 composition"` | Web heroes, video thumbnails |
| 9:16 | `"vertical 9:16 portrait orientation"` | Stories, mobile vertical |
| 21:9 | `"ultra-wide 21:9 panoramic"` | Ultra-wide banners |

### Reference Image Limits

- Maximum **14 reference images** per request
- Supported formats: PNG, JPEG, WebP, GIF (first frame)
- Recommended: keep reference images under 4MB each

---

## Response Processing

### Standard Image Extraction

```python
import json
from datetime import datetime
from pathlib import Path


def save_generated_images(response, output_dir="./generated", prefix="image"):
    """Extract and save images from Gemini API response."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_files = []
    text_responses = []

    for i, part in enumerate(response.candidates[0].content.parts):
        if part.inline_data:
            ext = "png" if "png" in part.inline_data.mime_type else "jpg"
            filename = f"{timestamp}_{prefix}_{i}.{ext}"
            filepath = output_path / filename
            filepath.write_bytes(part.inline_data.data)
            saved_files.append(str(filepath))
            print(f"Saved: {filepath}")
        elif part.text:
            text_responses.append(part.text)

    return saved_files, text_responses
```

### Metadata Generation

```python
def save_metadata(saved_files, prompt, output_dir="./generated"):
    """Save generation metadata alongside images."""
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "prompt": prompt,
        "model": "gemini-2.5-flash-image",
        "files": saved_files,
        "synthid": True,  # All Gemini images have SynthID watermark
    }

    metadata_path = Path(output_dir) / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    print(f"Metadata saved: {metadata_path}")
    return metadata
```

---

## Error Handling

### Comprehensive Error Handler

```python
import time

from google.api_core import exceptions as api_exceptions


def generate_image_safe(client, prompt, model="gemini-2.5-flash-image", max_retries=3):
    """Generate image with comprehensive error handling."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                ),
            )

            # Check for empty response (content policy block)
            if not response.candidates or not response.candidates[0].content.parts:
                print("Warning: Empty response — prompt may have been blocked by content policy.")
                print("Try adjusting the prompt to comply with content guidelines.")
                return None

            return response

        except api_exceptions.ResourceExhausted:
            wait_time = 2 ** attempt * 10  # Exponential backoff
            print(f"Rate limit exceeded. Waiting {wait_time}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)

        except api_exceptions.InvalidArgument as e:
            print(f"Invalid request: {e}")
            print("Check prompt content and parameter values.")
            return None

        except api_exceptions.PermissionDenied:
            print("API key invalid or insufficient permissions.")
            print("Verify GEMINI_API_KEY environment variable.")
            return None

        except api_exceptions.NotFound:
            print("Model not found. Verify the model ID is correct for your API type.")
            print("Google AI API (API key): use 'gemini-2.5-flash-image'")
            print("Vertex AI (service account): imagen models may be available")
            return None

        except api_exceptions.ServiceUnavailable:
            wait_time = 2 ** attempt * 5
            print(f"Service temporarily unavailable. Retrying in {wait_time}s...")
            time.sleep(wait_time)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    print(f"Failed after {max_retries} attempts.")
    return None
```

### Error Type Reference

| Error | Cause | Recovery |
|-------|-------|----------|
| `ResourceExhausted` | Rate limit / quota exceeded | Exponential backoff, check quota |
| `InvalidArgument` | Bad prompt or parameters | Fix prompt/params, check API docs |
| `PermissionDenied` | Invalid API key | Verify `GEMINI_API_KEY` env var |
| `NotFound` | Model doesn't exist for API type | Use `gemini-2.5-flash-image` for Google AI API |
| `ServiceUnavailable` | Server-side issue | Retry with backoff |
| Empty response | Content policy violation | Adjust prompt, remove sensitive content |
| `DeadlineExceeded` | Request timeout | Retry, consider simpler prompt |

### Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `ImageGenerationConfig` not found | `AttributeError` | SDK <v1.50 — use simple config without `image_generation_config` |
| `imagen-3.0-*` model 404 | `NotFound` | Vertex AI only — use `gemini-2.5-flash-image` for Google AI API |
| Wrong Gemini model name | `NotFound` | Use `-image` suffix: `gemini-2.5-flash-image` |

---

## Rate Limits & Cost Control

### Rate Limit Guidelines

| Model | RPM (est.) | Notes |
|-------|-----------|-------|
| Flash | 15-60 | Higher limits for paid plans |

### Cost Optimization Strategies

1. **Use Flash by default**: Most cost-effective for most use cases
2. **Start with 1 image**: Generate single image first, iterate
3. **Batch wisely**: Generate variants only after confirming direction
4. **Cache prompts**: Reuse successful prompts with minor tweaks
5. **Preview before bulk**: Always preview 1-3 images before batch

### Batch Generation Pattern

```python
import time


def batch_generate(client, prompts, model="gemini-2.5-flash-image",
                   output_dir="./generated", delay_seconds=2):
    """Generate multiple images with rate limit awareness."""
    results = []

    for i, prompt in enumerate(prompts):
        print(f"Generating {i + 1}/{len(prompts)}: {prompt[:50]}...")
        response = generate_image_safe(client, prompt, model)

        if response:
            files, _ = save_generated_images(
                response, output_dir=output_dir, prefix=f"batch_{i:03d}",
            )
            results.extend(files)
        else:
            print(f"  Skipped: generation failed for prompt {i + 1}")

        # Rate limit buffer
        if i < len(prompts) - 1:
            time.sleep(delay_seconds)

    print(f"\nBatch complete: {len(results)} images generated")
    return results
```

---

## SynthID Information

すべての Gemini API で生成された画像には **SynthID** 透かしが自動的に埋め込まれる。

| Property | Detail |
|----------|--------|
| **Type** | Invisible digital watermark |
| **Purpose** | AI-generated image identification |
| **Removal** | Cannot be removed without significant image degradation |
| **Detection** | Google provides detection tools |
| **Disclosure** | Generated images should be disclosed as AI-generated when appropriate |

### Documentation Template

生成画像を使用する際のメタデータに含めるべき情報：

```
This image was generated using Google Gemini API.
It contains an invisible SynthID watermark for AI-generated content identification.
Model: gemini-2.5-flash-image
Generated: [timestamp]
```

---

## Complete Script Template

実行可能な完全なスクリプトテンプレート（SDK v1.38+ 互換）：

```python
#!/usr/bin/env python3
"""Image generation script using Gemini API.

Usage:
    export GEMINI_API_KEY="your-api-key"
    python generate.py

Requirements:
    pip install google-genai
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types


def main():
    # Verify API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Set it with: export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # Configuration
    prompt = "YOUR PROMPT HERE"
    model = "gemini-2.5-flash-image"
    output_dir = Path("./generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate
    print(f"Generating image with {model}...")
    print(f"Prompt: {prompt}")

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Check response
    if not response.candidates or not response.candidates[0].content.parts:
        print("Error: No image generated. Prompt may violate content policy.")
        sys.exit(1)

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved = []

    for i, part in enumerate(response.candidates[0].content.parts):
        if part.inline_data:
            filename = f"{timestamp}_generated_{i}.png"
            filepath = output_dir / filename
            filepath.write_bytes(part.inline_data.data)
            saved.append(str(filepath))
            print(f"Saved: {filepath}")

    # Metadata
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "prompt": prompt,
        "model": model,
        "files": saved,
        "synthid": True,
    }
    meta_path = output_dir / f"{timestamp}_metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
    print(f"Metadata: {meta_path}")
    print("Done!")


if __name__ == "__main__":
    main()
```
