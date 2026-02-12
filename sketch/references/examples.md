# Usage Examples

Sketch エージェントの使用例とワークフローパターン。

---

## Basic Examples

### Example 1: Simple Text-to-Image

**Request**: 「ランディングページ用のヒーロー画像を生成して」

**Generated Script**:

```python
#!/usr/bin/env python3
"""Landing page hero image generation."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not set")
    sys.exit(1)

client = genai.Client(api_key=api_key)
output_dir = Path("./generated/hero")
output_dir.mkdir(parents=True, exist_ok=True)

prompt = (
    "A modern SaaS dashboard interface floating in abstract 3D space, "
    "soft gradient background in blue and purple tones, "
    "clean minimalist design, glass morphism effect, "
    "professional technology aesthetic, hero image composition, "
    "cinematic lighting, 8K quality"
)

print(f"Generating hero image...")
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
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

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
for i, part in enumerate(response.candidates[0].content.parts):
    if part.inline_data:
        filepath = output_dir / f"{timestamp}_hero.png"
        filepath.write_bytes(part.inline_data.data)
        print(f"Saved: {filepath}")

# Metadata
metadata = {
    "prompt": prompt,
    "model": "gemini-2.5-flash-image",
    "aspect_ratio": "16:9",
    "use_case": "Landing page hero image",
    "synthid": True,
    "generated_at": datetime.now().isoformat(),
}
(output_dir / f"{timestamp}_metadata.json").write_text(
    json.dumps(metadata, indent=2, ensure_ascii=False)
)
print("Done!")
```

---

### Example 2: Style-Specified Generation

**Request**: 「水彩風のイラストで、東京の街並みを描いて。9:16のストーリーサイズで」

**Generated Script**:

```python
#!/usr/bin/env python3
"""Watercolor-style Tokyo cityscape for Stories."""

import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or sys.exit("Error: GEMINI_API_KEY not set"))
output_dir = Path("./generated/tokyo")
output_dir.mkdir(parents=True, exist_ok=True)

prompt = (
    "Tokyo cityscape at twilight, watercolor painting style, "
    "soft edges, translucent color layers, paper texture visible, "
    "bleeding colors between sky and buildings, "
    "neon lights reflecting in rain puddles, organic brush strokes, "
    "traditional Japanese watercolor technique, wabi-sabi aesthetic, "
    "vertical composition optimized for mobile"
)

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_generation_config=types.ImageGenerationConfig(
            number_of_images=1,
            output_image_format="png",
            aspect_ratio="9:16",
            person_generation="DONT_ALLOW",
        ),
    ),
)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
for part in response.candidates[0].content.parts:
    if part.inline_data:
        filepath = output_dir / f"{timestamp}_tokyo_watercolor.png"
        filepath.write_bytes(part.inline_data.data)
        print(f"Saved: {filepath}")
```

---

## Iterative Editing Example

### Example 3: Multi-Turn Refinement

**Request**: 「カフェの画像を生成して、段階的に調整したい」

**Generated Script**:

```python
#!/usr/bin/env python3
"""Iterative image editing with multi-turn chat."""

import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or sys.exit("Error: GEMINI_API_KEY not set"))
output_dir = Path("./generated/cafe_iterations")
output_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


def save_response(response, label):
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            filepath = output_dir / f"{timestamp}_{label}.png"
            filepath.write_bytes(part.inline_data.data)
            print(f"Saved: {filepath}")
        elif part.text:
            print(f"AI: {part.text}")


# Create chat session for iterative editing
chat = client.chats.create(
    model="gemini-2.5-flash-image",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_generation_config=types.ImageGenerationConfig(
            output_image_format="png",
            aspect_ratio="4:3",
            person_generation="DONT_ALLOW",
        ),
    ),
)

# --- Turn 1: Initial generation ---
print("=== Turn 1: Initial cafe scene ===")
r1 = chat.send_message(
    "Generate a cozy Japanese-style cafe interior with wooden furniture, "
    "warm lighting, plants on shelves, morning sunlight through windows"
)
save_response(r1, "01_initial")

# --- Turn 2: Add details ---
print("\n=== Turn 2: Adding details ===")
r2 = chat.send_message(
    "Add a latte art coffee cup on the nearest table, "
    "and a small bookshelf in the background"
)
save_response(r2, "02_details_added")

# --- Turn 3: Adjust mood ---
print("\n=== Turn 3: Adjusting mood ===")
r3 = chat.send_message(
    "Change the lighting to late afternoon golden hour, "
    "make the atmosphere warmer and more nostalgic"
)
save_response(r3, "03_mood_adjusted")

print(f"\nAll iterations saved to: {output_dir}")
```

---

## Batch Generation Example

### Example 4: Multiple Variations

**Request**: 「プロダクトのアイコン候補を5パターン生成して」

**Generated Script**:

```python
#!/usr/bin/env python3
"""Batch generation of product icon variations."""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types
from google.api_core import exceptions as api_exceptions

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or sys.exit("Error: GEMINI_API_KEY not set"))
output_dir = Path("./generated/icons")
output_dir.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Define variations
variations = [
    {
        "name": "gradient",
        "prompt": (
            "App icon, modern gradient design, smooth blue-to-purple transition, "
            "abstract geometric shape, rounded square format, clean minimal, "
            "iOS app icon style, glossy finish"
        ),
    },
    {
        "name": "flat",
        "prompt": (
            "App icon, flat design, bold single color, simple geometric symbol, "
            "no shadows, no gradients, material design inspired, "
            "clean silhouette on solid background"
        ),
    },
    {
        "name": "3d",
        "prompt": (
            "App icon, 3D rendered, soft clay material, pastel colors, "
            "rounded friendly shape, subtle shadow, playful aesthetic, "
            "modern 3D icon trend"
        ),
    },
    {
        "name": "glass",
        "prompt": (
            "App icon, glassmorphism style, frosted glass effect, "
            "translucent layers, subtle border glow, depth effect, "
            "modern UI trend, light background"
        ),
    },
    {
        "name": "neon",
        "prompt": (
            "App icon, neon glow effect, dark background, "
            "vibrant electric blue outline, futuristic tech aesthetic, "
            "clean geometric shape, cyberpunk minimal"
        ),
    },
]

config = types.GenerateContentConfig(
    response_modalities=["IMAGE"],
    image_generation_config=types.ImageGenerationConfig(
        number_of_images=1,
        output_image_format="png",
        aspect_ratio="1:1",
        person_generation="DONT_ALLOW",
    ),
)

results = []
for i, var in enumerate(variations):
    print(f"[{i + 1}/{len(variations)}] Generating: {var['name']}...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=var["prompt"],
            config=config,
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data:
                filename = f"{timestamp}_icon_{var['name']}.png"
                filepath = output_dir / filename
                filepath.write_bytes(part.inline_data.data)
                results.append({"name": var["name"], "file": str(filepath), "prompt": var["prompt"]})
                print(f"  Saved: {filepath}")

    except api_exceptions.ResourceExhausted:
        print(f"  Rate limited. Waiting 30s...")
        time.sleep(30)
    except Exception as e:
        print(f"  Error: {e}")

    if i < len(variations) - 1:
        time.sleep(3)  # Rate limit buffer

# Summary
summary = {
    "generated_at": datetime.now().isoformat(),
    "total": len(results),
    "variations": results,
    "synthid": True,
}
(output_dir / f"{timestamp}_batch_summary.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=False)
)
print(f"\nBatch complete: {len(results)}/{len(variations)} icons generated")
print(f"Output directory: {output_dir}")
```

---

## Reference-Based Example

### Example 5: Image Editing with Reference

**Request**: 「この写真の背景を変更して」

**Generated Script**:

```python
#!/usr/bin/env python3
"""Edit image background using reference image."""

import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or sys.exit("Error: GEMINI_API_KEY not set"))
output_dir = Path("./generated/edited")
output_dir.mkdir(parents=True, exist_ok=True)

# Load source image
source_path = Path("./input/product_photo.png")  # ← 編集する画像のパス
if not source_path.exists():
    print(f"Error: Source image not found: {source_path}")
    sys.exit(1)

source_data = source_path.read_bytes()

# Edit instruction
edit_prompt = (
    "Replace the background with a clean, modern office environment. "
    "Keep the foreground product exactly as is. "
    "Match the lighting direction and color temperature."
)

print(f"Editing: {source_path}")
print(f"Edit: {edit_prompt}")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        types.Part.from_bytes(data=source_data, mime_type="image/png"),
        edit_prompt,
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_generation_config=types.ImageGenerationConfig(
            number_of_images=1,
            output_image_format="png",
        ),
    ),
)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

if response.candidates and response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            filepath = output_dir / f"{timestamp}_bg_replaced.png"
            filepath.write_bytes(part.inline_data.data)
            print(f"Saved: {filepath}")
else:
    print("Error: No image generated. The edit request may have been blocked.")
```

---

## Agent Collaboration Examples

### Example 6: Vision → Sketch Pipeline

**Scenario**: Vision がクリエイティブディレクションを提供し、Sketch が画像生成コードを作成

**Vision からのハンドオフ**:

```yaml
VISION_TO_SKETCH:
  creative_direction: "Warm, organic, approachable brand aesthetic"
  target_use: "Marketing landing page hero + 3 feature section backgrounds"
  requirements:
    aspect_ratio: "16:9 for hero, 4:3 for features"
    style: "Photorealistic with subtle warm color grading"
    constraints:
      - "No people — use objects and environments"
      - "Brand colors: warm amber (#F5A623), deep forest (#2D5016)"
      - "Must feel premium but approachable"
  reference_images: []
```

**Sketch の出力**: 4つの画像生成スクリプト（hero + 3 features）

### Example 7: Sketch → Muse Pipeline

**Scenario**: 生成画像をデザインシステムに統合

**Sketch からのハンドオフ**:

```yaml
SKETCH_TO_MUSE:
  generated_images:
    - "./generated/hero/20250615_143022_hero.png"
    - "./generated/features/20250615_143105_feature_01.png"
    - "./generated/features/20250615_143148_feature_02.png"
    - "./generated/features/20250615_143231_feature_03.png"
  metadata: "./generated/metadata.json"
  prompt_used: "Modern SaaS workspace, warm amber and forest green tones..."
  integration_notes: |
    - Hero image: Use as full-width background with overlay gradient
    - Feature images: Crop to 4:3, apply 8px border-radius
    - All images contain SynthID watermark (AI-generated disclosure may be needed)
    - Color palette extracted: #F5A623 (primary), #2D5016 (accent), #FFF8F0 (bg)
```

---

## Production Patterns

### Pattern A: CLI Tool Wrapper

```python
#!/usr/bin/env python3
"""CLI tool for image generation.

Usage:
    python generate_cli.py --prompt "Your prompt" --ratio 16:9 --style photo
    python generate_cli.py --prompt "Your prompt" --model pro --resolution 4k
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types


def parse_args():
    parser = argparse.ArgumentParser(description="Generate images with Gemini API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--model", choices=["flash", "pro"], default="flash")
    parser.add_argument("--ratio", default="1:1", help="Aspect ratio (e.g., 16:9)")
    parser.add_argument("--count", type=int, default=1, help="Number of images (1-4)")
    parser.add_argument("--format", choices=["png", "jpeg"], default="png")
    parser.add_argument("--output", default="./generated", help="Output directory")
    parser.add_argument("--allow-persons", action="store_true", help="Allow person generation")
    return parser.parse_args()


def main():
    args = parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set")
        sys.exit(1)

    model_map = {
        "flash": "gemini-2.5-flash-image",
        "pro": "gemini-3-pro-image-preview",
    }

    client = genai.Client(api_key=api_key)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Model: {model_map[args.model]}")
    print(f"Prompt: {args.prompt}")
    print(f"Ratio: {args.ratio} | Count: {args.count} | Format: {args.format}")

    response = client.models.generate_content(
        model=model_map[args.model],
        contents=args.prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_generation_config=types.ImageGenerationConfig(
                number_of_images=args.count,
                output_image_format=args.format,
                aspect_ratio=args.ratio,
                person_generation="ALLOW_ADULT" if args.allow_persons else "DONT_ALLOW",
            ),
        ),
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved = []

    if response.candidates:
        for i, part in enumerate(response.candidates[0].content.parts):
            if part.inline_data:
                ext = args.format
                filepath = output_dir / f"{timestamp}_{i:02d}.{ext}"
                filepath.write_bytes(part.inline_data.data)
                saved.append(str(filepath))
                print(f"Saved: {filepath}")

    if saved:
        meta = {
            "prompt": args.prompt,
            "model": model_map[args.model],
            "ratio": args.ratio,
            "count": len(saved),
            "files": saved,
            "synthid": True,
            "generated_at": datetime.now().isoformat(),
        }
        meta_path = output_dir / f"{timestamp}_meta.json"
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        print(f"Metadata: {meta_path}")
    else:
        print("No images generated. Check prompt and content policy.")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### Pattern B: API Wrapper Class

```python
"""Reusable Gemini image generation wrapper.

Usage:
    from image_generator import ImageGenerator

    gen = ImageGenerator()  # Uses GEMINI_API_KEY env var
    files = gen.generate("A sunset over mountains", ratio="16:9")
    files = gen.edit("input.png", "Change background to beach")
    files = gen.batch(["prompt1", "prompt2", "prompt3"])
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types
from google.api_core import exceptions as api_exceptions


class ImageGenerator:
    """Wrapper for Gemini API image generation."""

    MODELS = {
        "flash": "gemini-2.5-flash-image",
        "pro": "gemini-3-pro-image-preview",
    }

    def __init__(self, api_key=None, output_dir="./generated", model="flash"):
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY not set")
        self.client = genai.Client(api_key=key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.model = self.MODELS.get(model, model)

    def generate(self, prompt, ratio="1:1", count=1, fmt="png",
                 allow_persons=False, max_retries=3):
        """Generate images from text prompt."""
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        image_generation_config=types.ImageGenerationConfig(
                            number_of_images=count,
                            output_image_format=fmt,
                            aspect_ratio=ratio,
                            person_generation="ALLOW_ADULT" if allow_persons else "DONT_ALLOW",
                        ),
                    ),
                )
                return self._save(response, prompt, ratio)

            except api_exceptions.ResourceExhausted:
                wait = 2 ** attempt * 10
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            except Exception as e:
                print(f"Error: {e}")
                return []
        return []

    def edit(self, image_path, instruction, fmt="png"):
        """Edit an existing image."""
        source = Path(image_path).read_bytes()
        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_bytes(data=source, mime_type="image/png"),
                instruction,
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_generation_config=types.ImageGenerationConfig(
                    number_of_images=1,
                    output_image_format=fmt,
                ),
            ),
        )
        return self._save(response, instruction, "edited")

    def batch(self, prompts, ratio="1:1", delay=3, **kwargs):
        """Generate multiple images with rate limiting."""
        all_files = []
        for i, prompt in enumerate(prompts):
            print(f"[{i + 1}/{len(prompts)}] {prompt[:60]}...")
            files = self.generate(prompt, ratio=ratio, **kwargs)
            all_files.extend(files)
            if i < len(prompts) - 1:
                time.sleep(delay)
        return all_files

    def _save(self, response, prompt, label):
        """Save response images and metadata."""
        if not response.candidates:
            return []

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved = []

        for i, part in enumerate(response.candidates[0].content.parts):
            if part.inline_data:
                ext = "png" if "png" in part.inline_data.mime_type else "jpg"
                path = self.output_dir / f"{ts}_{i}.{ext}"
                path.write_bytes(part.inline_data.data)
                saved.append(str(path))

        if saved:
            meta = {
                "prompt": prompt, "model": self.model,
                "files": saved, "synthid": True,
                "generated_at": datetime.now().isoformat(),
            }
            (self.output_dir / f"{ts}_meta.json").write_text(
                json.dumps(meta, indent=2, ensure_ascii=False)
            )

        return saved
```
