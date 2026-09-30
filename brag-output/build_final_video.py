#!/usr/bin/env python3
"""
Build Snapcode 3D brag video end-to-end.
Generates frame-by-frame animation, compiles to MP4, creates poster.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION = 18
TOTAL_FRAMES = DURATION * FPS

def log(msg):
    print(f"  {msg}")

def step(title):
    print(f"\n🎬 {title}")

def build_video():
    script_dir = Path(__file__).parent
    frames_dir = script_dir / "frames"
    output_video = script_dir / "brag.mp4"
    output_poster = script_dir / "brag.jpg"

    # Clean up old frames
    if frames_dir.exists():
        import shutil
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(exist_ok=True)

    step("Generating animation frames")

    # Scene timing (in frame numbers at 30fps)
    scenes = {
        "hook": (0, 60, "Snapcode 3D", "3D → Code"),
        "drop": (60, 120, "Drop a 3D capture", ""),
        "processing": (120, 210, "Processing...", ""),
        "preview": (210, 390, "Three.js Preview", ""),
        "code": (390, 480, "Code Ready", ""),
        "cta": (480, 540, "Snapcode 3D", "Try Now")
    }

    log(f"Target: {TOTAL_FRAMES} frames ({DURATION}s @ {FPS}fps)")

    # Color palette (oklch values converted to RGB)
    colors = {
        "navy": (29, 21, 40),
        "cobalt": (133, 84, 255),
        "gold": (222, 170, 60),
        "white": (245, 245, 245),
        "gray": (100, 100, 120),
    }

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        log("Installing Pillow...")
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "-q"],
                      capture_output=True)
        from PIL import Image, ImageDraw, ImageFont

    # Generate frames
    for frame_num in range(TOTAL_FRAMES):
        img = Image.new('RGB', (WIDTH, HEIGHT), colors["navy"])
        draw = ImageDraw.Draw(img)

        # Find current scene
        scene_name = None
        scene_progress = 0
        for name, (start, end, title, subtitle) in scenes.items():
            if start <= frame_num < end:
                scene_name = name
                scene_progress = (frame_num - start) / (end - start)
                break

        # Render scene based on progress
        if scene_name == "hook":
            # Title + underline animation
            alpha = min(scene_progress * 3, 1.0)
            draw.text((WIDTH//2, HEIGHT//2 - 100), "Snapcode 3D",
                     fill=colors["white"], anchor="mm")
            draw.text((WIDTH//2, HEIGHT//2 + 50), "3D → Code",
                     fill=colors["cobalt"], anchor="mm")
            # Animated underline
            line_w = int(250 * min(scene_progress + 0.3, 1.0))
            draw.rectangle([WIDTH//2 - line_w//2, HEIGHT//2 + 120,
                           WIDTH//2 + line_w//2, HEIGHT//2 + 125],
                          fill=colors["cobalt"])

        elif scene_name == "drop":
            # Drop zone with scaling
            scale = 0.7 + scene_progress * 0.3
            box_size = int(200 * scale)
            draw.text((WIDTH//2, HEIGHT//2 - 250), "Drop a 3D capture",
                     fill=colors["white"], anchor="mm")
            draw.rectangle([WIDTH//2 - box_size, HEIGHT//2 - box_size,
                           WIDTH//2 + box_size, HEIGHT//2 + box_size],
                          outline=colors["cobalt"], width=2)
            # Ring inside
            r = int(100 * scale)
            draw.ellipse([WIDTH//2 - r, HEIGHT//2 - r,
                         WIDTH//2 + r, HEIGHT//2 + r],
                        outline=colors["gold"], width=6)

        elif scene_name == "processing":
            draw.text((WIDTH//2, HEIGHT//2 + 200), "Processing...",
                     fill=colors["white"], anchor="mm")
            # Rotating spinner
            angle = (scene_progress * 360) % 360
            r = 50
            x0, y0 = WIDTH//2 - r, HEIGHT//2 - r
            x1, y1 = WIDTH//2 + r, HEIGHT//2 + r
            draw.ellipse([x0, y0, x1, y1], outline=colors["cobalt"], width=4)
            # Spinner arc
            draw.arc([x0, y0, x1, y1], 0, int(scene_progress * 360),
                    fill=colors["gold"], width=6)

        elif scene_name == "preview":
            draw.text((WIDTH//2, HEIGHT//2 + 250), "Three.js Preview",
                     fill=colors["white"], anchor="mm")
            # Animated ring
            size = int(150 * (0.5 + scene_progress * 0.5))
            rotation_deg = (scene_progress * 360) % 360
            # Draw 3D-ish ring
            r1 = size
            r2 = int(size * 0.8)
            x, y = WIDTH//2, HEIGHT//2
            draw.ellipse([x - r1, y - r1, x + r1, y + r1],
                        outline=colors["gold"], width=12)
            draw.ellipse([x - r2, y - r2, x + r2, y + r2],
                        outline=colors["cobalt"], width=4)
            # Glow
            glow_size = int(r1 * 1.3)
            draw.ellipse([x - glow_size, y - glow_size,
                         x + glow_size, y + glow_size],
                        outline=colors["cobalt"], width=1)

        elif scene_name == "code":
            draw.text((WIDTH//2, HEIGHT//2 - 200), "Code Ready",
                     fill=colors["white"], anchor="mm")
            # Code panel
            panel_alpha = min(scene_progress * 2, 1.0)
            draw.rectangle([WIDTH//2 - 300, HEIGHT//2 - 50,
                           WIDTH//2 + 300, HEIGHT//2 + 50],
                          outline=colors["gold"], width=2)
            # Sample code
            code_text = "const mesh = new THREE.Mesh(...)"
            draw.text((WIDTH//2, HEIGHT//2), code_text,
                     fill=colors["gold"], anchor="mm")
            # Glowing border
            glow_w = int(4 * panel_alpha)
            draw.rectangle([WIDTH//2 - 305, HEIGHT//2 - 55,
                           WIDTH//2 + 305, HEIGHT//2 + 55],
                          outline=colors["cobalt"], width=glow_w)

        elif scene_name == "cta":
            # Final screen
            draw.text((WIDTH//2, HEIGHT//2 - 150), "Snapcode 3D",
                     fill=colors["white"], anchor="mm")
            draw.text((WIDTH//2, HEIGHT//2 - 50),
                     "Instant Three.js from 3D captures",
                     fill=colors["cobalt"], anchor="mm")
            # Button
            btn_alpha = min(scene_progress * 2, 1.0)
            draw.rectangle([WIDTH//2 - 120, HEIGHT//2 + 80,
                           WIDTH//2 + 120, HEIGHT//2 + 140],
                          fill=colors["cobalt"])
            draw.text((WIDTH//2, HEIGHT//2 + 110), "Try Now",
                     fill=colors["white"], anchor="mm", font=None)

        # Save frame
        frame_path = frames_dir / f"frame-{frame_num:06d}.png"
        img.save(frame_path)

        if (frame_num + 1) % 90 == 0:
            pct = (frame_num + 1) / TOTAL_FRAMES * 100
            log(f"Rendered {frame_num + 1}/{TOTAL_FRAMES} frames ({pct:.0f}%)")

    log(f"✓ All {TOTAL_FRAMES} frames generated")

    # Build MP4 with ffmpeg
    step("Encoding to MP4")
    input_pattern = str(frames_dir / "frame-%06d.png")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "23",
        "-preset", "fast",
        str(output_video)
    ]

    try:
        log(f"Running ffmpeg...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            log(f"FFmpeg stderr: {result.stderr[-500:]}")
            raise RuntimeError("FFmpeg encoding failed")
        log(f"✓ Video encoded: {output_video}")
        log(f"  Size: {output_video.stat().st_size / 1024 / 1024:.1f} MB")
    except FileNotFoundError:
        log("Installing ffmpeg...")
        subprocess.run(["apt-get", "update"], capture_output=True)
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"],
                      capture_output=True)
        return build_video()  # Retry

    # Create poster
    step("Creating poster thumbnail")
    poster_frame = frames_dir / "frame-000120.png"  # Good moment in drop scene
    if poster_frame.exists():
        import shutil
        shutil.copy(poster_frame, output_poster)
        log(f"✓ Poster: {output_poster}")

    return output_video, output_poster

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)

    try:
        video, poster = build_video()

        step("Complete!")
        print(f"\n✅ Snapcode 3D brag video ready:")
        print(f"   📹 {video.name}")
        print(f"   📸 {poster.name if poster else 'N/A'}")
        print(f"\n   Share copy in: share-copy.txt")
        print(f"   Plan in: brag-plan.md")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
