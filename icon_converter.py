<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>SquareCropper Web</title>
<style>
  body { margin:0; font-family: Meiryo, sans-serif; background:#111; color:#eee; }
  #container { display:flex; height:100vh; }
  #canvas { background:#000; flex:1; }
  #right { width:300px; background:#222; padding:20px; overflow-y:auto; }
  button, input { margin:5px 0; padding:12px; width:100%; font-size:16px; }
  input[type="file"] { padding:10px; }
  .btn { background:#00cc00; color:white; border:none; cursor:pointer; font-weight:bold; }
  .btn:hover { background:#00ff00; }
  .save { background:#0088ff; }
  .ico { background:#ff6600; }
  .size-btn { background:#444; color:white; padding:10px; margin:5px 0; }
  .size-btn.active { background:#00aa00; }
  #hint { margin-top:30px; font-size:14px; color:#aaa; }
</style>
</head>
<body>

<div id="container">
  <canvas id="canvas"></canvas>
  <div id="right">
    <h2>SquareCropper Web</h2>
    <input type="file" id="fileInput" accept="image/*">
    <button class="btn" onclick="document.getElementById('fileInput').click()">
      画像を選択
    </button>

    <div style="margin:20px 0;">
      <strong>切り取りサイズ</strong><br>
      <div class="size-btn active" data-size="256">256×256</div>
      <div class="size-btn" data-size="512">512×512</div>
      <div class="size-btn" data-size="1024">1024×1024</div>
      <div class="size-btn" data-size="2048">2048×2048</div>
    </div>

    <button class="btn save" onclick="save('png')">PNGで保存</button>
    <button class="btn ico" onclick="save('ico')">ICOで保存（256+512）</button>

    <div id="hint">
      操作方法：<br>
      ・ドラッグ → 枠を移動<br>
      ・Shift + ドラッグ → 画像を移動<br>
      ・ホイール → ズーム<br>
      ・小さい画像は自動で枠にフィット！
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let img = null;
let zoom = 1, panX = 0, panY = 0;
let cropSize = 512;
let cropX = 0, cropY = 0;
let dragging = false, panning = false;
let startX, startY;

canvas.width = window.innerWidth - 320;
canvas.height = window.innerHeight;

window.addEventListener('resize', () => {
  canvas.width = window.innerWidth - 320;
  canvas.height = window.innerHeight;
  draw();
});

document.getElementById('fileInput').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    img = new Image();
    img.onload = () => {
      // 自動で枠にフィット
      if (img.width < cropSize || img.height < cropSize) {
        zoom = cropSize / Math.min(img.width, img.height) * 1.1;
      } else {
        zoom = 1;
      }
      cropX = (img.width - cropSize / zoom) / 2;
      cropY = (img.height - cropSize / zoom) / 2;
      panX = panY = 0;
      draw();
    };
    img.src = ev.target.result;
  };
  reader.readAsDataURL(file);
});

// サイズ選択
document.querySelectorAll('.size-btn').forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    cropSize = parseInt(btn.dataset.size);
    if (img) {
      if (img.width < cropSize || img.height < cropSize) {
        zoom = cropSize / Math.min(img.width, img.height) * 1.1;
      } else {
        zoom = 1;
      }
      cropX = (img.width - cropSize / zoom) / 2;
      cropY = (img.height - cropSize / zoom) / 2;
      draw();
    }
  };
});

// マウス操作
canvas.addEventListener('mousedown', e => {
  startX = e.offsetX;
  startY = e.offsetY;
  if (e.shiftKey) {
    panning = true;
  } else {
    dragging = true;
  }
});

canvas.addEventListener('mousemove', e => {
  if (!img) return;
  const dx = (e.offsetX - startX) / zoom;
  const dy = (e.offsetY - startY) / zoom;
  
  if (dragging) {
    cropX = Math.max(0, Math.min(cropX + dx, img.width - cropSize / zoom));
    cropY = Math.max(0, Math.min(cropY + dy, img.height - cropSize / zoom));
  } else if (panning) {
    panX += e.offsetX - startX;
    panY += e.offsetY - startY;
  }
  startX = e.offsetX;
  startY = e.offsetY;
  draw();
});

canvas.addEventListener('mouseup', () => {
  dragging = panning = false;
});

canvas.addEventListener('wheel', e => {
  e.preventDefault();
  zoom *= e.deltaY > 0 ? 0.9 : 1.1;
  zoom = Math.max(0.1, Math.min(zoom, 30));
  draw();
});

function draw() {
  if (!img) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  const dw = img.width * zoom;
  const dh = img.height * zoom;
  
  ctx.drawImage(img, 
    canvas.width/2 + panX - dw/2, 
    canvas.height/2 + panY - dh/2, 
    dw, dh
  );
  
  // 枠描画
  const s = dw / img.width;
  const x = canvas.width/2 + panX - dw/2 + cropX * s;
  const y = canvas.height/2 + panY - dh/2 + cropY * s;
  
  ctx.strokeStyle = '#00ff00';
  ctx.lineWidth = 6;
  ctx.globalAlpha = 0.3;
  ctx.fillStyle = '#00ff00';
  ctx.fillRect(x, y, cropSize, cropSize);
  ctx.globalAlpha = 1;
  ctx.strokeRect(x, y, cropSize, cropSize);
}

function save(type) {
  if (!img) return alert("画像を読み込んでください");
  
  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = cropSize;
  tempCanvas.height = cropSize;
  const tctx = tempCanvas.getContext('2d');
  
  const effectiveW = cropSize / zoom;
  const effectiveH = cropSize / zoom;
  
  tctx.drawImage(img,
    cropX, cropY, effectiveW, effectiveH,
    0, 0, cropSize, cropSize
  );
  
  tempCanvas.toBlob(blob => {
    const a = document.createElement('a');
    a.download = `cropped_${cropSize}x${cropSize}.${type === 'ico' ? 'ico' : 'png'}`;
    if (type === 'ico') {
      alert("ICOはブラウザでは直接保存できません。\nPNGで保存して、後で変換してください！");
      a.download = a.download.replace('ico', 'png');
      a.href = URL.createObjectURL(blob);
    } else {
      a.href = URL.createObjectURL(blob);
    }
    a.click();
  }, type === 'ico' ? 'image/png' : 'image/png');
}
</script>
</body>
</html>
