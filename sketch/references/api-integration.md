# API Integration Reference

Gemini API 画像生成の統合パターン詳細リファレンス。

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

| Model | ID | Resolution | Speed | Cost | Best For |
|-------|-----|-----------|-------|------|----------|
| **Flash** | `gemini-2.5-flash-image` | 1K-2K | Fast | Low | Default — Web, SNS, prototyping, iteration |
| **Pro** | `gemini-3-pro-image-preview` | 1K-4K | Slower | High | Print, commercial, premium quality |

### Model Selection Decision Tree

```
Is 4K resolution needed? → Yes → Pro
Is highest quality critical? → Yes → Pro
Is speed/cost important? → Yes → Flash
Is this iterative/exploratory? → Yes → Flash
Default → Flash
```

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
    contents="A modern minimalist workspace with a laptop and coffee, soft natural lighting",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_generation_config=types.ImageGenerationConfig(
            number_of_images=1,
            output_image_format="png",
            aspect_ratio="16:9",
            person_generation="DONT_ALLOW",
        ),
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
        image_generation_config=types.ImageGenerationConfig(
            number_of_images=1,
            output_image_format="png",
            aspect_ratio="16:9",
        ),
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
import base64

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
        image_generation_config=types.ImageGenerationConfig(
            number_of_images=1,
            output_image_format="png",
        ),
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
        image_generation_config=types.ImageGenerationConfig(
            output_image_format="png",
        ),
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
        image_generation_config=types.ImageGenerationConfig(
            number_of_images=1,
            output_image_format="png",
        ),
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

### image_generation_config

| Parameter | Type | Options | Default | Notes |
|-----------|------|---------|---------|-------|
| `number_of_images` | int | 1-4 | 1 | Flash: 1-4, Pro: 1-4 |
| `output_image_format` | str | `"png"`, `"jpeg"` | `"png"` | PNG for lossless, JPEG for smaller size |
| `aspect_ratio` | str | See below | `"1:1"` | Must match use case |
| `person_generation` | str | `"DONT_ALLOW"`, `"ALLOW_ADULT"` | `"DONT_ALLOW"` | Safety setting |
| `image_compression_quality` | int | 0-100 | 75 | JPEG only |

### Aspect Ratio Guide

| Ratio | Pixels (1K) | Use Case |
|-------|-------------|----------|
| `1:1` | 1024×1024 | Social media, icons, avatars |
| `3:2` | 1024×683 | Photography standard, landscape |
| `2:3` | 683×1024 | Portrait, mobile screenshots |
| `4:3` | 1024×768 | Presentations, documents |
| `3:4` | 768×1024 | Tablets, book covers |
| `16:9` | 1024×576 | Web heroes, video thumbnails |
| `9:16` | 576×1024 | Stories, mobile vertical |
| `21:9` | 1024×439 | Ultra-wide banners |
| `4:5` | 1024×1280 | Instagram portrait |
| `5:4` | 1024×819 | Large prints |

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
def save_metadata(saved_files, prompt, config, output_dir="./generated"):
    """Save generation metadata alongside images."""
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "prompt": prompt,
        "model": config.get("model", "gemini-2.5-flash-image"),
        "parameters": {
            "aspect_ratio": config.get("aspect_ratio", "1:1"),
            "person_generation": config.get("person_generation", "DONT_ALLOW"),
            "number_of_images": config.get("number_of_images", 1),
            "format": config.get("output_image_format", "png"),
        },
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
from google.api_core import exceptions as api_exceptions


def generate_image_safe(client, prompt, config, max_retries=3):
    """Generate image with comprehensive error handling."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=config.get("model", "gemini-2.5-flash-image"),
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_generation_config=types.ImageGenerationConfig(
                        number_of_images=config.get("number_of_images", 1),
                        output_image_format=config.get("format", "png"),
                        aspect_ratio=config.get("aspect_ratio", "1:1"),
                        person_generation=config.get("person_generation", "DONT_ALLOW"),
                    ),
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
            import time
            time.sleep(wait_time)

        except api_exceptions.InvalidArgument as e:
            print(f"Invalid request: {e}")
            print("Check prompt content and parameter values.")
            return None

        except api_exceptions.PermissionDenied:
            print("API key invalid or insufficient permissions.")
            print("Verify GEMINI_API_KEY environment variable.")
            return None

        except api_exceptions.ServiceUnavailable:
            wait_time = 2 ** attempt * 5
            print(f"Service temporarily unavailable. Retrying in {wait_time}s...")
            import time
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
| `ServiceUnavailable` | Server-side issue | Retry with backoff |
| Empty response | Content policy violation | Adjust prompt, remove sensitive content |
| `DeadlineExceeded` | Request timeout | Retry, consider simpler prompt |

---

## Rate Limits & Cost Control

### Rate Limit Guidelines

| Model | RPM (est.) | TPM (est.) | Notes |
|-------|-----------|-----------|-------|
| Flash | 15-60 | Varies | Higher limits for paid plans |
| Pro | 2-10 | Varies | Lower limits, higher quality |

### Cost Optimization Strategies

1. **Use Flash by default**: 5-10x cheaper than Pro
2. **Start with 1 image**: Generate single image first, iterate
3. **Use 1K resolution**: Upscale only when needed
4. **Batch wisely**: Generate variants only after confirming direction
5. **Cache prompts**: Reuse successful prompts with minor tweaks
6. **Preview before bulk**: Always preview 1-3 images before batch

### Batch Generation Pattern

```python
import time


def batch_generate(client, prompts, config, delay_seconds=2):
    """Generate multiple images with rate limit awareness."""
    results = []

    for i, prompt in enumerate(prompts):
        print(f"Generating {i + 1}/{len(prompts)}: {prompt[:50]}...")
        response = generate_image_safe(client, prompt, config)

        if response:
            files, _ = save_generated_images(
                response,
                output_dir=config.get("output_dir", "./generated"),
                prefix=f"batch_{i:03d}",
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
Model: [model name]
Generated: [timestamp]
```

---

## Complete Script Template

実行可能な完全なスクリプトテンプレート：

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
                image_generation_config=types.ImageGenerationConfig(
                    number_of_images=1,
                    output_image_format="png",
                    aspect_ratio="1:1",
                    person_generation="DONT_ALLOW",
                ),
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
        "aspect_ratio": "1:1",
        "person_generation": "DONT_ALLOW",
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
