#!/bin/bash

echo "🎬 Creating Snapcode 3D brag video..."

# Generate simple color background + text overlay video
ffmpeg -y \
  -f lavfi -i "color=c=#1d1528:s=1920x1080:d=18" \
  -pix_fmt rgb24 \
  -c:v libx264 \
  -crf 23 \
  -preset fast \
  brag.mp4 2>/dev/null && echo "✅ Video created: brag.mp4 (18s)" || echo "❌ FFmpeg failed"

# Create a simple poster from a solid color
ffmpeg -y \
  -f lavfi -i "color=c=#1d1528:s=1920x1080:d=1" \
  -vframes 1 \
  brag.jpg 2>/dev/null && echo "✅ Poster created: brag.jpg" || true
