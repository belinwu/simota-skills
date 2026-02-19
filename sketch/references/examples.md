# Usage Examples

Sketch エージェントの使用例とワークフローパターン。

> **動作確認環境**: google-genai SDK v1.38.0 + Google AI API（`gemini-2.5-flash-image`）

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
# ...
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

# ...
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
# ...
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
# ...
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

# ...
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
    python generate_cli.py --prompt "Your prompt"
    python generate_cli.py --prompt "Your prompt" --ratio 16:9
    python generate_cli.py --prompt "Your prompt" --output ./my_images
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
# ...
```

### Pattern B: API Wrapper Class

```python
"""Reusable Gemini image generation wrapper.

Usage:
    from image_generator import ImageGenerator

    gen = ImageGenerator()  # Uses GEMINI_API_KEY env var
    files = gen.generate("A sunset over mountains")
    files = gen.edit("input.png", "Change background to beach")
    files = gen.batch(["prompt1", "prompt2", "prompt3"])
"""

import json
import os
import time
from datetime import datetime
# ...
```
