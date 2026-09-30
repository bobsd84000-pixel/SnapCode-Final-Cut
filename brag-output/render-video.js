const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const WIDTH = 1920;
const HEIGHT = 1080;
const FPS = 30;
const DURATION = 18; // seconds
const TOTAL_FRAMES = DURATION * FPS;

async function renderVideo() {
  console.log('🎬 Rendering Snapcode 3D brag video...');

  const browser = await chromium.launch();
  const context = await browser.createContext({
    viewport: { width: WIDTH, height: HEIGHT }
  });
  const page = await context.newPage();

  // Load the HTML file
  const htmlPath = `file://${path.resolve(__dirname, 'brag-video.html')}`;
  await page.goto(htmlPath);

  // Wait for fonts to load
  await page.waitForTimeout(1000);

  // Create frames directory
  const framesDir = path.join(__dirname, 'frames');
  if (!fs.existsSync(framesDir)) {
    fs.mkdirSync(framesDir, { recursive: true });
  }

  // Capture frames
  console.log(`📸 Capturing ${TOTAL_FRAMES} frames...`);
  for (let i = 0; i < TOTAL_FRAMES; i++) {
    const progress = (i / TOTAL_FRAMES * 100).toFixed(1);
    if (i % 30 === 0) {
      console.log(`  Progress: ${progress}%`);
    }

    // Set timeline position
    const timeMs = (i / FPS) * 1000;
    await page.evaluate((ms) => {
      const startTime = window.startTime;
      window.startTime = Date.now() - ms;
      // Trigger update
      const event = new Event('update');
      window.dispatchEvent(event);
    }, timeMs);

    // Small delay for rendering
    await page.waitForTimeout(10);

    // Capture frame
    const frameNum = String(i).padStart(6, '0');
    const framePath = path.join(framesDir, `frame-${frameNum}.png`);
    await page.screenshot({ path: framePath });
  }

  console.log('✅ Frame capture complete');
  await browser.close();

  // Now use FFmpeg to create video
  console.log('🎥 Creating MP4 with ffmpeg...');
  const { execSync } = require('child_process');

  try {
    const inputPattern = path.join(framesDir, 'frame-%06d.png');
    const outputPath = path.join(__dirname, 'brag.mp4');

    const ffmpegCmd = `ffmpeg -y -framerate ${FPS} -i "${inputPattern}" -c:v libx264 -pix_fmt yuv420p -crf 23 "${outputPath}"`;
    execSync(ffmpegCmd, { stdio: 'inherit' });

    console.log(`✅ Video saved: ${outputPath}`);

    // Create poster frame (frame at 2 seconds - good moment in the hook)
    const posterFrame = path.join(framesDir, 'frame-000060.png'); // 60 frames at 30fps = 2 seconds
    const posterPath = path.join(__dirname, 'brag.jpg');
    if (fs.existsSync(posterFrame)) {
      fs.copyFileSync(posterFrame, posterPath);
      console.log(`✅ Poster saved: ${posterPath}`);
    }
  } catch (e) {
    console.error('FFmpeg error:', e.message);
    console.log('💡 Make sure ffmpeg is installed: apt-get install ffmpeg');
  }
}

renderVideo().catch(console.error);
