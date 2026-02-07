"""
Photo Curator (OpenAI GPT-4o Edition) - AI-powered photo organizer
Groups photos by event, names them via GPT-4o Vision, picks the best shot.
"""

import os
import sys
import shutil
import json
import re
import base64
from pathlib import Path
from datetime import datetime, timedelta
from io import BytesIO

from dotenv import load_dotenv
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from openai import OpenAI

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("ERROR: No OPENAI_API_KEY found in .env file.")
    print("Create a .env file with: OPENAI_API_KEY=your_key_here")
    sys.exit(1)

client = OpenAI(api_key=API_KEY)

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output_openai"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heif", ".heic"}
EVENT_GAP_MINUTES = 30  # Photos within this window = same event
THUMBNAIL_MAX_PX = 1024

# Register HEIF support so Pillow can open iPhone photos
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    print("HEIF/HEIC support loaded (iPhone photos will work)")
except ImportError:
    print("WARNING: pillow-heif not installed. HEIF/HEIC photos will be skipped.")
    print("  Fix: pip install pillow-heif")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_supported_photos(folder):
    """Return a sorted list of photo paths from the input folder."""
    photos = []
    for f in folder.iterdir():
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
            photos.append(f)
    photos.sort(key=lambda p: p.name.lower())
    return photos


def extract_exif_datetime(path):
    """
    Try to pull a timestamp from the photo's EXIF data.
    Falls back to the file's modification time if EXIF is missing.
    """
    try:
        img = Image.open(path)
        exif_data = img._getexif()
        if exif_data:
            # Tag 36867 = DateTimeOriginal, 306 = DateTime
            for tag_id in (36867, 306):
                raw = exif_data.get(tag_id)
                if raw:
                    return datetime.strptime(raw, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass

    # Fallback: file modification time
    mod_time = os.path.getmtime(path)
    return datetime.fromtimestamp(mod_time)


def extract_gps(path):
    """Try to pull GPS coordinates from EXIF. Returns (lat, lon) or None."""
    try:
        img = Image.open(path)
        exif_data = img._getexif()
        if not exif_data:
            return None

        gps_info = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == "GPSInfo":
                for gps_tag_id, gps_value in value.items():
                    gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_info[gps_tag_name] = gps_value

        if not gps_info:
            return None

        def to_degrees(values):
            d, m, s = [float(v) for v in values]
            return d + m / 60.0 + s / 3600.0

        lat = to_degrees(gps_info["GPSLatitude"])
        if gps_info.get("GPSLatitudeRef", "N") == "S":
            lat = -lat

        lon = to_degrees(gps_info["GPSLongitude"])
        if gps_info.get("GPSLongitudeRef", "E") == "W":
            lon = -lon

        return (round(lat, 6), round(lon, 6))
    except Exception:
        return None


def make_thumbnail(path):
    """Open a photo, shrink to max 1024px on longest side, return as PIL Image."""
    img = Image.open(path)
    # Handle EXIF orientation so thumbnails aren't rotated
    try:
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    img.thumbnail((THUMBNAIL_MAX_PX, THUMBNAIL_MAX_PX), Image.LANCZOS)
    # Convert to RGB if needed (e.g. RGBA PNGs, palette images)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    return img


def pil_to_bytes(img, fmt="JPEG"):
    """Convert a PIL Image to bytes."""
    buf = BytesIO()
    img.save(buf, format=fmt, quality=85)
    return buf.getvalue()


def group_photos_by_time(photo_records, gap_minutes=EVENT_GAP_MINUTES):
    """
    Given a list of dicts with 'timestamp', group them into events.
    A new group starts when the gap between consecutive photos > gap_minutes.
    """
    if not photo_records:
        return []

    # Sort by timestamp
    sorted_records = sorted(photo_records, key=lambda r: r["timestamp"])
    groups = [[sorted_records[0]]]

    for record in sorted_records[1:]:
        prev_time = groups[-1][-1]["timestamp"]
        if record["timestamp"] - prev_time > timedelta(minutes=gap_minutes):
            groups.append([record])
        else:
            groups[-1].append(record)

    return groups


def sanitize_folder_name(name):
    """Turn an event name into a safe folder name."""
    # Keep letters, numbers, spaces, hyphens, underscores
    clean = re.sub(r"[^\w\s\-]", "", name)
    # Replace spaces with underscores, collapse multiples
    clean = re.sub(r"\s+", "_", clean.strip())
    # Truncate
    return clean[:60] if clean else "Unknown_Event"


def analyze_group_with_openai(group):
    """
    Send thumbnails of a photo group to GPT-4o and get back:
    - event_name: short descriptive name
    - scores: list of quality scores (0-100) in the same order as the group
    - best_index: index of the best photo
    """
    print(f"  Sending {len(group)} photo(s) to GPT-4o for analysis...")

    # Build the prompt text (identical scoring criteria as Gemini version)
    prompt = (
        "You are a PARENT picking your favorite photos to frame on the wall — "
        "NOT a photography contest judge. You care about the FEELING of the photo, "
        "not whether it's technically perfect.\n\n"
        "I'm giving you a set of photos taken around the same time (same event).\n\n"
        "For each photo (numbered starting at 1), score based on these priorities "
        "(in order of importance):\n"
        "1. EXPRESSION & PERSONALITY (highest weight) — cheeky smiles, genuine laughs, "
        "playful looks, mischievous expressions, candid moments that show who someone really is\n"
        "2. EMOTIONAL STORYTELLING — does this photo capture a feeling you'd want to remember? "
        "A moment that tells a story? The kind of photo that makes you smile years later?\n"
        "3. CUTENESS & CHARM — especially for babies, kids, and pets. The 'aww' factor. "
        "Messy faces, curious eyes, silly poses are GOOD things.\n"
        "4. TECHNICAL QUALITY (lowest weight, tiebreaker only) — sharpness, lighting, "
        "composition. Only matters if two photos are equally charming.\n\n"
        "IMPORTANT: A slightly blurry photo of a genuinely funny expression beats a "
        "perfectly sharp photo of a neutral face. Personality > perfection.\n\n"
        "Respond in STRICT JSON (no markdown, no code fences) with exactly this format:\n"
        "{\n"
        '  "event_name": "Short Descriptive Name (2-4 words)",\n'
        '  "scores": [85, 72, 91],\n'
        '  "best_index": 3,\n'
        '  "reason": "One sentence explaining the EMOTIONAL quality that makes the best photo special"\n'
        "}\n\n"
        "Rules:\n"
        "- event_name should describe WHAT is happening (e.g. 'Beach Sunset', 'Family Dinner')\n"
        "- scores is a list of integers 0-100, one per photo, in order\n"
        "- best_index is 1-based (first photo = 1)\n"
        "- If there's only 1 photo, still score it and pick it as best\n"
        "- In your reason, describe the FEELING, not the technical quality\n"
        f"\nThere are {len(group)} photo(s) total."
    )

    # Build the content array for OpenAI chat completions with vision
    content = [{"type": "text", "text": prompt}]

    for i, record in enumerate(group):
        thumb = make_thumbnail(record["path"])
        img_bytes = pil_to_bytes(thumb)
        b64_string = base64.b64encode(img_bytes).decode("utf-8")
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64_string}"},
        })
        content.append({
            "type": "text",
            "text": f"(Photo {i + 1}: {record['path'].name})",
        })

    # Call GPT-4o
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=2000,
            messages=[{"role": "user", "content": content}],
        )
        raw_text = response.choices[0].message.content.strip()

        # Strip markdown code fences if GPT-4o wraps the JSON
        if raw_text.startswith("```"):
            raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
            raw_text = re.sub(r"\s*```$", "", raw_text)

        result = json.loads(raw_text)

        # Validate
        event_name = result.get("event_name", "Unknown Event")
        scores = result.get("scores", [50] * len(group))
        best_index = result.get("best_index", 1)
        reason = result.get("reason", "")

        # Clamp best_index to valid range (convert to 0-based)
        best_index_0 = max(0, min(best_index - 1, len(group) - 1))

        # Ensure we have the right number of scores
        if len(scores) != len(group):
            scores = scores[:len(group)] + [50] * (len(group) - len(scores))

        return {
            "event_name": event_name,
            "scores": scores,
            "best_index": best_index_0,
            "reason": reason,
        }

    except json.JSONDecodeError as e:
        print(f"  WARNING: GPT-4o returned invalid JSON. Using defaults.")
        print(f"  Raw response: {raw_text[:200]}")
        return {
            "event_name": "Unknown Event",
            "scores": [50] * len(group),
            "best_index": 0,
            "reason": "Could not parse AI response",
        }
    except Exception as e:
        print(f"  ERROR calling GPT-4o: {e}")
        return {
            "event_name": "Unknown Event",
            "scores": [50] * len(group),
            "best_index": 0,
            "reason": f"API error: {e}",
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  PHOTO CURATOR (GPT-4o Edition)")
    print("  AI-powered photo organizer")
    print("=" * 60)

    # 1. Find photos
    print(f"\nScanning {INPUT_DIR} for photos...")
    photos = get_supported_photos(INPUT_DIR)
    if not photos:
        print("No photos found in input/ folder.")
        print(f"  Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
        print("  Drop some photos in there and run again.")
        sys.exit(0)
    print(f"Found {len(photos)} photo(s)")

    # 2. Extract metadata
    print("\nExtracting metadata...")
    records = []
    for p in photos:
        ts = extract_exif_datetime(p)
        gps = extract_gps(p)
        records.append({"path": p, "timestamp": ts, "gps": gps})
        gps_str = f" | GPS: {gps}" if gps else ""
        print(f"  {p.name}  ->  {ts.strftime('%Y-%m-%d %H:%M')}{gps_str}")

    # 3. Group by time
    print(f"\nGrouping photos (gap threshold: {EVENT_GAP_MINUTES} min)...")
    groups = group_photos_by_time(records)
    print(f"Identified {len(groups)} event group(s)")
    for i, g in enumerate(groups):
        first_ts = g[0]["timestamp"].strftime("%Y-%m-%d %H:%M")
        last_ts = g[-1]["timestamp"].strftime("%H:%M")
        print(f"  Group {i + 1}: {len(g)} photo(s), {first_ts} - {last_ts}")

    # 4. Analyze each group with GPT-4o
    print("\nAnalyzing photos with GPT-4o...")
    event_results = []

    for i, group in enumerate(groups):
        print(f"\n--- Event group {i + 1}/{len(groups)} ({len(group)} photos) ---")
        analysis = analyze_group_with_openai(group)
        event_results.append({"group": group, "analysis": analysis})

        event_name = analysis["event_name"]
        best_idx = analysis["best_index"]
        best_name = group[best_idx]["path"].name
        best_score = analysis["scores"][best_idx]
        print(f"  Event: {event_name}")
        print(f"  Best photo: {best_name} (score: {best_score}/100)")
        print(f"  Reason: {analysis['reason']}")

    # 5. Organize output (do NOT clear/delete existing output folders)
    print("\nOrganizing output folders...")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_lines = []
    summary_lines.append("# Photo Curator Summary (GPT-4o)\n")
    summary_lines.append(f"**Run date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    summary_lines.append(f"**Total photos:** {len(records)}\n")
    summary_lines.append(f"**Events identified:** {len(event_results)}\n")
    summary_lines.append("---\n")

    total_copied = 0

    for i, result in enumerate(event_results):
        group = result["group"]
        analysis = result["analysis"]
        event_name = analysis["event_name"]
        scores = analysis["scores"]
        best_idx = analysis["best_index"]

        # Build folder name: YYYY-MM-DD_Event_Name
        date_str = group[0]["timestamp"].strftime("%Y-%m-%d")
        safe_name = sanitize_folder_name(event_name)
        folder_name = f"{date_str}_{safe_name}"
        event_folder = OUTPUT_DIR / folder_name
        event_folder.mkdir(parents=True, exist_ok=True)

        summary_lines.append(f"## {event_name}\n")
        summary_lines.append(f"**Date:** {date_str}\n")
        summary_lines.append(f"**Photos:** {len(group)}\n")
        summary_lines.append(f"**Best:** {group[best_idx]['path'].name} (score: {scores[best_idx]})\n")
        summary_lines.append(f"**Why:** {analysis['reason']}\n")
        summary_lines.append("| Rank | Photo | Score |")
        summary_lines.append("|------|-------|-------|")

        # Build a list of (original_index, score) and sort by score descending
        indexed_scores = [(j, scores[j] if j < len(scores) else 50) for j in range(len(group))]
        indexed_scores.sort(key=lambda x: x[1], reverse=True)

        for rank, (j, score) in enumerate(indexed_scores, start=1):
            src = group[j]["path"]
            stem = src.stem
            suffix = src.suffix
            dest_name = f"No.{rank}_{stem}_score{score}{suffix}"

            shutil.copy2(src, event_folder / dest_name)
            total_copied += 1

            marker = " **BEST**" if j == best_idx else ""
            summary_lines.append(f"| {rank} | {src.name} | {score}{marker} |")

            print(f"  Copied {src.name} -> {folder_name}/{dest_name}")

        summary_lines.append("")

    # Write summary
    summary_lines.append("---\n")
    summary_lines.append(f"*Generated by Photo Curator using GPT-4o*\n")
    summary_path = OUTPUT_DIR / "summary.md"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    # Done
    print("\n" + "=" * 60)
    print("  DONE! (GPT-4o Edition)")
    print(f"  {total_copied} photos organized into {len(event_results)} event(s)")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Summary: {summary_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
