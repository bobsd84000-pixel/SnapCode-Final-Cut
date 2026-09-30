#!/bin/bash

# Build Snapcode 3D brag video with pure ffmpeg
# No external dependencies — just ffmpeg filters

OUTPUT="brag.mp4"
POSTER="brag.jpg"
DURATION=18
WIDTH=1920
HEIGHT=1080
FPS=30

echo "🎬 Building Snapcode 3D brag video with ffmpeg..."

# Create video using ffmpeg drawtext filter
# This creates animated text overlays on a colored background

ffmpeg -y \
  -f lavfi \
  -i "color=c=#1d1528:s=${WIDTH}x${HEIGHT}:d=${DURATION}" \
  -vf "
    drawtext=text='Snapcode 3D':fontsize=120:fontcolor=#f5f5f5:x=(w-text_w)/2:y=h/2-150:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf:enable='between(t,0,2)':alpha='if(lt(t,0.5),t*2,1)';
    drawtext=text='3D → Code':fontsize=80:fontcolor=#8554ff:x=(w-text_w)/2:y=h/2+50:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:enable='between(t,0,2)':alpha='if(lt(t,1),t,1)';
    drawtext=text='Drop a 3D capture':fontsize=100:fontcolor=#f5f5f5:x=(w-text_w)/2:y=h/2-250:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf:enable='between(t,2,4)';
    drawtext=text='Processing...':fontsize=100:fontcolor=#f5f5f5:x=(w-text_w)/2:y=h/2+200:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf:enable='between(t,4,7)';
    drawtext=text='Three.js Preview':fontsize=100:fontcolor=#f5f5f5:x=(w-text_w)/2:y=h/2+250:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf:enable='between(t,7,13)';
    drawtext=text='Code Ready':fontsize=100:fontcolor=#f5f5f5:x=(w-text_w)/2:y=h/2-200:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf:enable='between(t,13,16)';
    drawtext=text='Snapcode 3D':fontsize=120:fontcolor=#f5f5f5:x=(w-text_w)/2:y=h/2-150:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf:enable='between(t,16,18)';
    drawtext=text='Try Now':fontsize=80:fontcolor=#f5f5f5:x=(w-text_w)/2:y=h/2+110:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:enable='between(t,16,18)'
  " \
  -c:v libx264 \
  -pix_fmt yuv420p \
  -crf 23 \
  "${OUTPUT}" 2>&1 | grep -E "(frame=|Duration|bitrate)" || echo "✅ Video encoding complete"

if [ -f "${OUTPUT}" ]; then
  SIZE=$(du -h "${OUTPUT}" | cut -f1)
  echo "✅ Video created: ${OUTPUT} (${SIZE})"

  # Create poster
  ffmpeg -y -i "${OUTPUT}" -ss 00:00:02 -vframes 1 "${POSTER}" 2>/dev/null
  echo "✅ Poster created: ${POSTER}"
else
  echo "❌ Video encoding failed"
  exit 1
fi
