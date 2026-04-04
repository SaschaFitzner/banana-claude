#!/usr/bin/env python3
"""Banana Claude -- Image Editing

Edit images via Gemini REST API.
Uses only Python stdlib (no pip dependencies).

Usage:
    edit.py --image path/to/image.png --prompt "remove the background"
            [--reference ref1.png --reference ref2.png]
            [--model MODEL] [--api-key KEY]
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
OUTPUT_DIR_NAME = "nanobanana_generated"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def encode_image(path):
    """Read an image file and return (base64_data, mime_type)."""
    path = Path(path).resolve()
    if not path.exists():
        print(json.dumps({"error": True, "message": f"Image not found: {path}"}))
        sys.exit(1)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    suffix = path.suffix.lower()
    mime_types = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                  ".webp": "image/webp", ".gif": "image/gif"}
    return b64, mime_types.get(suffix, "image/png")


def edit_image(image_path, prompt, model, api_key, output_dir=None, reference_images=None):
    """Call Gemini API to edit an image, optionally with reference images."""
    image_path = Path(image_path).resolve()

    # Build request parts: primary image first (highest weight), then references, then prompt
    request_parts = []

    img_b64, img_mime = encode_image(image_path)
    request_parts.append({"inlineData": {"mimeType": img_mime, "data": img_b64}})

    ref_paths = []
    for ref in (reference_images or []):
        ref_b64, ref_mime = encode_image(ref)
        request_parts.append({"inlineData": {"mimeType": ref_mime, "data": ref_b64}})
        ref_paths.append(str(Path(ref).resolve()))

    request_parts.append({"text": prompt})

    url = f"{API_BASE}/{model}:generateContent?key={api_key}"

    body = {
        "contents": [{"parts": request_parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    max_retries = 3
    result = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            break  # Success
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            if e.code == 429 and attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(json.dumps({"retry": True, "attempt": attempt + 1, "wait_seconds": wait, "reason": "rate_limited"}), file=sys.stderr)
                time.sleep(wait)
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
                continue
            if e.code == 400 and "FAILED_PRECONDITION" in error_body:
                print(json.dumps({"error": True, "status": 400, "message": "Billing not enabled. Enable billing at https://aistudio.google.com/apikey"}))
                sys.exit(1)
            print(json.dumps({"error": True, "status": e.code, "message": error_body}))
            sys.exit(1)
        except urllib.error.URLError as e:
            print(json.dumps({"error": True, "message": str(e.reason)}))
            sys.exit(1)

    if result is None:
        print(json.dumps({"error": True, "message": "Max retries exceeded"}))
        sys.exit(1)

    # Extract image from response
    candidates = result.get("candidates", [])
    if not candidates:
        finish_reason = result.get("promptFeedback", {}).get("blockReason", "UNKNOWN")
        print(json.dumps({"error": True, "message": f"No candidates returned. Reason: {finish_reason}"}))
        sys.exit(1)

    parts = candidates[0].get("content", {}).get("parts", [])
    image_data = None
    text_response = ""

    for part in parts:
        if "inlineData" in part:
            image_data = part["inlineData"]["data"]
        elif "text" in part:
            text_response = part["text"]

    if not image_data:
        finish_reason = candidates[0].get("finishReason", "UNKNOWN")
        print(json.dumps({"error": True, "message": f"No image in response. finishReason: {finish_reason}"}))
        sys.exit(1)

    # Save image
    save_dir = Path(output_dir) if output_dir else Path.cwd() / OUTPUT_DIR_NAME
    save_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"banana_edit_{timestamp}.png"
    output_path = (save_dir / filename).resolve()

    with open(output_path, "wb") as f:
        f.write(base64.b64decode(image_data))

    result = {
        "path": str(output_path),
        "model": model,
        "source": str(image_path),
        "text": text_response,
    }
    if ref_paths:
        result["references"] = ref_paths
    return result


def main():
    parser = argparse.ArgumentParser(description="Edit images via Gemini REST API")
    parser.add_argument("--image", required=True, help="Path to input image (primary, highest weight)")
    parser.add_argument("--reference", action="append", default=[], help="Reference image(s) for style/context (repeatable, max 13)")
    parser.add_argument("--prompt", required=True, help="Edit instruction")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--api-key", default=None, help="Google AI API key (or set GOOGLE_AI_API_KEY env)")
    parser.add_argument("--output-dir", default=None, help="Output directory for edited images (default: ./<nanobanana_generated> in CWD)")

    args = parser.parse_args()

    if len(args.reference) > 13:
        print(json.dumps({"error": True, "message": "Max 13 reference images (14 total including primary). Got: " + str(len(args.reference))}))
        sys.exit(1)

    api_key = args.api_key or os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        try:
            result = subprocess.run(
                ["fio-vault", "get", "google-api-key", "--global"],
                capture_output=True, text=True, check=True,
            )
            api_key = result.stdout.strip()
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
    if not api_key:
        print(json.dumps({"error": True, "message": "No API key. Set GOOGLE_AI_API_KEY env, pass --api-key, or store in fio-vault: fio-vault set google-api-key GOOGLE_AI_API_KEY --global"}))
        sys.exit(1)

    result = edit_image(
        image_path=args.image,
        prompt=args.prompt,
        model=args.model,
        api_key=api_key,
        output_dir=args.output_dir,
        reference_images=args.reference,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
