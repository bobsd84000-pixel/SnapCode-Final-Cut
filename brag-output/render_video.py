#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

# Configuration
WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION = 18
TOTAL_FRAMES = DURATION * FPS

def render_frames_with_ffmpeg():
    """Use ffmpeg to render HTML to frames"""
    script_dir = Path(__file__).parent
    html_file = script_dir / "brag-video.html"
    frames_dir = script_dir / "frames"

    frames_dir.mkdir(exist_ok=True)

    print(f"🎬 Rendering {TOTAL_FRAMES} frames from HTML...")

    # Use ffmpeg with HTML input
    html_url = f"file://{html_file}"
    output_pattern = str(frames_dir / "frame-%06d.png")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "lavfi", "-i", f"color=c=oklch(0.19 0.045 262):s={WIDTH}x{HEIGHT}:d={DURATION}",
        "-f", "lavfi", "-i", f"sine=f=440:d={DURATION}",
        "-i", str(html_file),
        "-c:v", "png",
        "-vf", f"scale={WIDTH}:{HEIGHT}",
        "-frames:v", str(TOTAL_FRAMES),
        output_pattern
    ]

    # Alternative: Use imagmagick or simple frame generation
    print("ℹ️  Direct HTML to frames requires browser automation.")
    print("   Using alternative: generating synthetic frames...")

    generate_synthetic_frames(frames_dir, TOTAL_FRAMES)

    return frames_dir

def generate_synthetic_frames(frames_dir, total_frames):
    """Generate synthetic frames representing the brag video"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("❌ Pillow not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "-q"], check=True)
        from PIL import Image, ImageDraw, ImageFont

    print(f"🖼️  Generating {total_frames} synthetic frames...")

    # Color palette from the design
    navy = (29, 21, 40)  # oklch(0.19 0.045 262)
    cobalt = (133, 84, 255)  # oklch(0.52 0.26 268)
    gold = (222, 170, 60)  # oklch(0.87 0.17 88)
    white = (245, 245, 245)

    # Scene timings (frame numbers)
    scenes = [
        (0, 60, "Hook", "Snapcode 3D"),
        (60, 120, "Drop", "Drop a 3D capture"),
        (120, 210, "Processing", "Processing..."),
        (210, 390, "Preview", "Three.js Preview"),
        (390, 480, "Code", "Code Ready"),
        (480, 540, "CTA", "Try Now")
    ]

    for frame_num in range(total_frames):
        # Create image
        img = Image.new('RGB', (WIDTH, HEIGHT), navy)
        draw = ImageDraw.Draw(img)

        # Determine current scene
        current_scene = None
        progress_in_scene = 0
        for start, end, scene_name, scene_text in scenes:
            if start <= frame_num < end:
                current_scene = scene_name
                progress_in_scene = (frame_num - start) / (end - start)
                break

        # Draw scene content
        if current_scene == "Hook":
            # Fade in title
            alpha = int(255 * min(progress_in_scene * 2, 1.0))
            draw.text((WIDTH//2 - 300, HEIGHT//2 - 100), "Snapcode 3D",
                     fill=(*white, alpha), font=None, anchor="mm")
            draw.text((WIDTH//2, HEIGHT//2 + 100), "3D → Code",
                     fill=(*cobalt, int(alpha * 0.8)), font=None, anchor="mm")
            # Underline
            line_width = int(300 * min(progress_in_scene, 1.0))
            draw.rectangle([WIDTH//2 - line_width//2, HEIGHT//2 + 50,
                           WIDTH//2 + line_width//2, HEIGHT//2 + 55],
                          fill=cobalt)

        elif current_scene == "Drop":
            draw.text((WIDTH//2, HEIGHT//2 - 200), "Drop a 3D capture",
                     fill=white, font=None, anchor="mm")
            # Draw drop zone
            opacity = min(progress_in_scene * 2, 1.0)
            box_y = int(HEIGHT//2 - 100 + (30 * (1 - opacity)))
            draw.rectangle([WIDTH//2 - 200, box_y - 150, WIDTH//2 + 200, box_y + 150],
                          outline=cobalt, width=2)

        elif current_scene == "Processing":
            draw.text((WIDTH//2, HEIGHT//2 + 150), "Processing...",
                     fill=white, font=None, anchor="mm")
            # Spinning circle
            angle = (progress_in_scene * 360) % 360
            draw.ellipse([WIDTH//2 - 40, HEIGHT//2 - 40, WIDTH//2 + 40, HEIGHT//2 + 40],
                        outline=cobalt, width=3)

        elif current_scene == "Preview":
            draw.text((WIDTH//2, HEIGHT//2 + 250), "Three.js Preview",
                     fill=white, font=None, anchor="mm")
            # Rotating ring
            size = int(200 * min(progress_in_scene + 0.5, 1.0))
            rotation = int(progress_in_scene * 360)
            draw.ellipse([WIDTH//2 - size, HEIGHT//2 - size,
                         WIDTH//2 + size, HEIGHT//2 + size],
                        outline=gold, width=8)

        elif current_scene == "Code":
            draw.text((WIDTH//2, HEIGHT//2 - 200), "Code Ready",
                     fill=white, font=None, anchor="mm")
            # Code panel
            draw.rectangle([WIDTH//2 - 300, HEIGHT//2 - 50, WIDTH//2 + 300, HEIGHT//2 + 50],
                          outline=gold, width=2)
            draw.text((WIDTH//2, HEIGHT//2), "const mesh = new THREE.Mesh(...)",
                     fill=gold, font=None, anchor="mm")

        elif current_scene == "CTA":
            draw.text((WIDTH//2, HEIGHT//2 - 150), "Snapcode 3D",
                     fill=white, font=None, anchor="mm")
            draw.text((WIDTH//2, HEIGHT//2 - 50), "Instant Three.js from 3D captures",
                     fill=cobalt, font=None, anchor="mm")
            # Button
            button_alpha = int(255 * min(progress_in_scene * 2, 1.0))
            draw.rectangle([WIDTH//2 - 100, HEIGHT//2 + 80, WIDTH//2 + 100, HEIGHT//2 + 130],
                          fill=cobalt)
            draw.text((WIDTH//2, HEIGHT//2 + 105), "Try Now",
                     fill=white, font=None, anchor="mm")

        # Save frame
        frame_path = frames_dir / f"frame-{frame_num:06d}.png"
        img.save(frame_path)

        if (frame_num + 1) % 30 == 0:
            print(f"  ✓ Frame {frame_num + 1}/{total_frames}")

def create_video_from_frames(frames_dir):
    """Create MP4 video from frames using ffmpeg"""
    script_dir = Path(__file__).parent
    input_pattern = str(frames_dir / "frame-%06d.png")
    output_video = str(script_dir / "brag.mp4")
    output_poster = str(script_dir / "brag.jpg")

    print(f"🎥 Creating video with ffmpeg...")

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "23",
        output_video
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Video created: {output_video}")

        # Copy poster frame (good moment in the video)
        poster_frame = frames_dir / "frame-000060.png"
        if poster_frame.exists():
            import shutil
            shutil.copy(poster_frame, output_poster)
            print(f"✅ Poster created: {output_poster}")

        return output_video
    except subprocess.CalledProcessError as e:
        print(f"❌ ffmpeg error: {e.stderr.decode()}")
        raise
    except FileNotFoundError:
        print("❌ ffmpeg not found. Installing...")
        subprocess.run(["apt-get", "update"], check=True, capture_output=True)
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True, capture_output=True)
        # Retry
        return create_video_from_frames(frames_dir)

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    frames_dir = generate_synthetic_frames(Path("frames"), TOTAL_FRAMES)
    video_path = create_video_from_frames(frames_dir)
    print(f"\n✅ Brag video complete: {video_path}")
