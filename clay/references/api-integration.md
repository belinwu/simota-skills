# API Integration Reference

Provider integration patterns for AI 3D model generation APIs.

## Provider Comparison

| Provider | Strength | Topology Quality | Input | Pricing Model | Format Output |
|----------|----------|-----------------|-------|---------------|---------------|
| **Meshy** | General purpose, reliable | Medium | Text, Image | Credit-based (free tier available) | FBX, OBJ, glTF, USDZ, STL |
| **Tripo** | Fast generation, good topology | Medium-High | Text, Image, Multi-view | Credit-based | FBX, OBJ, glTF, STL |
| **Hunyuan3D** | Open-source, self-hostable | Medium | Text, Image | Free (self-hosted) / API pricing | OBJ, glTF |
| **Rodin** | High detail, production quality | High | Text, Image, Multi-view | Credit-based | FBX, OBJ, glTF, USDZ |
| **Sloyd** | Game-ready topology, parametric | High (pre-retopologized) | Text, Parameters | Subscription + usage | FBX, OBJ, glTF |
| **Stability (TripoSR)** | Fast single-image reconstruction | Medium | Image | API credit-based | OBJ, glTF |

## Authentication Pattern

All providers use API key authentication via environment variables.

```python
import os
import httpx

# Standard auth pattern - NEVER hardcode keys
API_KEY = os.environ["MESHY_API_KEY"]  # or TRIPO_API_KEY, RODIN_API_KEY, etc.

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
```

Environment variable naming convention:

| Provider | Environment Variable |
|----------|---------------------|
| Meshy | `MESHY_API_KEY` |
| Tripo | `TRIPO_API_KEY` |
| Hunyuan3D | `HUNYUAN3D_API_KEY` (if using hosted API) |
| Rodin | `RODIN_API_KEY` |
| Sloyd | `SLOYD_API_KEY` |
| Stability | `STABILITY_API_KEY` |

## Text-to-3D Request Pattern

### Meshy

```python
import os
import time
import httpx

API_KEY = os.environ["MESHY_API_KEY"]
BASE_URL = "https://api.meshy.ai/openapi/v2"

def create_text_to_3d(prompt: str, art_style: str = "realistic",
                      topology: str = "quad", target_polycount: int = 30000) -> str:
    """Create a text-to-3D task. Returns task ID for polling."""
    resp = httpx.post(
        f"{BASE_URL}/text-to-3d",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "mode": "refine",  # "preview" for draft, "refine" for quality
            "prompt": prompt,
            "art_style": art_style,
            "topology": topology,
            "target_polycount": target_polycount,
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["result"]


def poll_task(task_id: str, interval: int = 10, max_wait: int = 600) -> dict:
    """Poll until task completes. Returns task result with model URLs."""
    elapsed = 0
    while elapsed < max_wait:
        resp = httpx.get(
            f"{BASE_URL}/text-to-3d/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")
        if status == "SUCCEEDED":
            return data
        if status == "FAILED":
            raise RuntimeError(f"Task failed: {data.get('task_error', {})}")
        print(f"Status: {status} (progress: {data.get('progress', 0)}%)")
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"Task {task_id} did not complete within {max_wait}s")
```

### Tripo

```python
import os
import httpx

API_KEY = os.environ["TRIPO_API_KEY"]
BASE_URL = "https://api.tripo3d.ai/v2/openapi"

def create_text_to_model(prompt: str, model_version: str = "v2.0-20240919") -> str:
    """Create a text-to-3D task. Returns task ID."""
    resp = httpx.post(
        f"{BASE_URL}/task",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "type": "text_to_model",
            "prompt": prompt,
            "model_version": model_version,
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    data = resp.json()
    if data["code"] != 0:
        raise RuntimeError(f"API error: {data['message']}")
    return data["data"]["task_id"]
```

### Rodin

```python
import os
import httpx

API_KEY = os.environ["RODIN_API_KEY"]
BASE_URL = "https://hyperhuman.deemos.com/api/v2"

def create_rodin_task(prompt: str, condition_image_url: str = None) -> str:
    """Create a Rodin generation task."""
    payload = {"prompt": prompt}
    if condition_image_url:
        payload["images"] = [condition_image_url]
    resp = httpx.post(
        f"{BASE_URL}/rodin",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=payload,
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["uuid"]
```

## Image-to-3D Request Pattern

Image-to-3D endpoints differ from text-to-3D in that they require an image URL or base64-encoded image.

```python
import os
import base64
from pathlib import Path
import httpx

API_KEY = os.environ["MESHY_API_KEY"]
BASE_URL = "https://api.meshy.ai/openapi/v2"

def create_image_to_3d(image_path: str, topology: str = "quad",
                       target_polycount: int = 30000) -> str:
    """Create an image-to-3D task from a local image file."""
    image_data = Path(image_path).read_bytes()
    image_b64 = base64.b64encode(image_data).decode()
    mime = "image/png" if image_path.endswith(".png") else "image/jpeg"

    resp = httpx.post(
        f"{BASE_URL}/image-to-3d",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "image_url": f"data:{mime};base64,{image_b64}",
            "topology": topology,
            "target_polycount": target_polycount,
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()["result"]
```

### Multi-view Image Preparation

For best image-to-3D results:

- Provide 1-4 views (front, side, back, 3/4 angle).
- Use clean, solid-color backgrounds (white or transparent).
- Maintain consistent lighting across views.
- Ensure subject fills 70-80% of the frame.
- Remove background clutter and shadows on the ground plane.

## Async Polling Pattern

All providers use async task creation + polling. Standard pattern:

```python
import time
from typing import Callable

def poll_with_backoff(check_fn: Callable[[], dict], task_id: str,
                      initial_interval: int = 5, max_interval: int = 30,
                      max_wait: int = 600) -> dict:
    """Generic polling with exponential backoff."""
    elapsed = 0
    interval = initial_interval
    while elapsed < max_wait:
        result = check_fn(task_id)
        status = result.get("status", "").upper()
        if status in ("SUCCEEDED", "COMPLETED", "DONE"):
            return result
        if status in ("FAILED", "ERROR"):
            raise RuntimeError(f"Task {task_id} failed: {result}")
        progress = result.get("progress", "unknown")
        print(f"[{task_id}] status={status} progress={progress} elapsed={elapsed}s")
        time.sleep(interval)
        elapsed += interval
        interval = min(interval * 1.5, max_interval)
    raise TimeoutError(f"Task {task_id} timed out after {max_wait}s")
```

## Rate Limiting and Retry

```python
import httpx
import time

MAX_RETRIES = 3
RETRY_DELAYS = [1, 5, 15]  # seconds

def request_with_retry(method: str, url: str, **kwargs) -> httpx.Response:
    """HTTP request with retry on rate limit (429) and server errors (5xx)."""
    for attempt in range(MAX_RETRIES):
        resp = httpx.request(method, url, **kwargs)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", RETRY_DELAYS[attempt]))
            print(f"Rate limited. Retrying in {retry_after}s...")
            time.sleep(retry_after)
            continue
        if resp.status_code >= 500:
            print(f"Server error {resp.status_code}. Retrying in {RETRY_DELAYS[attempt]}s...")
            time.sleep(RETRY_DELAYS[attempt])
            continue
        resp.raise_for_status()
        return resp
    raise RuntimeError(f"Failed after {MAX_RETRIES} retries: {url}")
```

## Cost Estimation

Estimate before batch runs. Include this pattern in batch scripts:

```python
def estimate_cost(provider: str, count: int, mode: str = "standard") -> dict:
    """Estimate API cost for a batch of generations."""
    # Approximate per-model costs (check current pricing)
    costs = {
        "meshy": {"preview": 0.10, "refine": 0.50},
        "tripo": {"draft": 0.10, "standard": 0.30},
        "rodin": {"standard": 0.50, "high": 1.00},
        "sloyd": {"standard": 0.05, "detailed": 0.15},
        "stability": {"standard": 0.20},
    }
    per_unit = costs.get(provider, {}).get(mode, 0.50)
    total = per_unit * count
    return {
        "provider": provider,
        "count": count,
        "mode": mode,
        "per_unit_usd": per_unit,
        "total_usd": total,
        "note": "Estimates only. Check provider dashboard for current pricing.",
    }
```

## Download and Save Pattern

```python
import httpx
from pathlib import Path

def download_model(url: str, output_dir: str, filename: str) -> Path:
    """Download generated model file."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filepath = output_path / filename

    with httpx.stream("GET", url, timeout=120.0) as resp:
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in resp.iter_bytes(chunk_size=8192):
                f.write(chunk)

    print(f"Downloaded: {filepath} ({filepath.stat().st_size / 1024:.1f} KB)")
    return filepath
```

## Provider Selection Guide

| Use Case | Recommended Provider | Reason |
|----------|---------------------|--------|
| Quick prototyping | Meshy (preview mode) | Fast, cheap, good enough for concepting |
| Game-ready assets | Sloyd | Pre-retopologized output, parametric control |
| High-detail hero assets | Rodin | Best detail fidelity |
| Single-image reconstruction | Stability (TripoSR) or Tripo | Optimized for image input |
| Self-hosted / open-source | Hunyuan3D | Full control, no API costs |
| Batch generation | Tripo or Meshy | Good rate limits, predictable pricing |
