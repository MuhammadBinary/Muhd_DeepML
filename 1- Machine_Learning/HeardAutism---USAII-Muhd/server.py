
from flask import Flask, request, jsonify, render_template_string
import sqlite3, os, tempfile
from datetime import datetime

app = Flask(__name__)
DB  = 'heard.db'

state = {'recording': True}

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        emotion TEXT NOT NULL,
        confidence REAL NOT NULL
    )''')
    conn.commit()
    conn.close()
init_db()

# ── LOADING MODEL FOR FILE UPLOAD INFERENCE ──────────────────────────
_model_run = None
def get_model():
    global _model_run
    if _model_run: return _model_run
    if os.path.exists('inference_model.onnx'):
        import onnxruntime as ort
        import numpy as np
        sess = ort.InferenceSession('inference_model.onnx')
        name = sess.get_inputs()[0].name
        _model_run = lambda f: sess.run(None, {name: f})[0][0]
    return _model_run

def extract_features(audio, sr=22050):
    import librosa, numpy as np
    zcr  = librosa.feature.zero_crossing_rate(audio)
    rms  = librosa.feature.rms(y=audio)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    feat = np.vstack([zcr, rms, mfcc])
    feat = feat[:, :130] if feat.shape[1] >= 130 \
           else np.pad(feat, ((0,0),(0, 130 - feat.shape[1])))
    feat = (feat - feat.mean()) / (feat.std() + 1e-8)
    return feat[np.newaxis, ...].astype('float32')

# ── ENDPOINTS ─────────────────────────────────────────────────────

@app.route('/predict', methods=['POST'])
def receive():
    data = request.get_json()
    ts   = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB)
    conn.execute('INSERT INTO detections (timestamp,emotion,confidence) VALUES (?,?,?)',
                 (ts, data.get('emotion','neutral'), data.get('confidence',0.0)))
    conn.commit(); conn.close()
    return jsonify({'status':'ok'})

@app.route('/latest')
def latest():
    conn = sqlite3.connect(DB)
    row  = conn.execute('SELECT emotion,confidence FROM detections ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    if row: return jsonify({'emotion':row[0],'confidence':round(row[1],2)})
    return jsonify({'emotion':'neutral','confidence':0.0})

@app.route('/state')
def get_state():
    return jsonify(state)

@app.route('/toggle', methods=['POST'])
def toggle():
    state['recording'] = not state['recording']
    return jsonify(state)

@app.route('/upload', methods=['POST'])
def upload():
    import librosa, numpy as np, io
    EMOTIONS = ['anger', 'fear', 'happy', 'neutral', 'sad']
    if 'file' not in request.files:
        return jsonify({'error': 'no file'}), 400

    # Read into memory
    file_bytes = request.files['file'].read()

    try:
        audio, sr = librosa.load(io.BytesIO(file_bytes), sr=22050)
        run = get_model()
        if not run:
            return jsonify({'error': 'model not loaded'}), 500
        probs = run(extract_features(audio, sr))
        idx   = int(np.argmax(probs))
        emo   = EMOTIONS[idx]
        conf  = float(probs[idx])
        ts    = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn  = sqlite3.connect(DB)
        conn.execute(
            'INSERT INTO detections (timestamp,emotion,confidence) VALUES (?,?,?)',
            (ts, emo, conf)
        )
        conn.commit()
        conn.close()
        return jsonify({'emotion': emo, 'confidence': round(conf, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/history')
def history():
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        'SELECT timestamp,emotion,confidence FROM detections ORDER BY id DESC LIMIT 100'
    ).fetchall()
    conn.close()
    return jsonify([{'time':r[0],'emotion':r[1],'confidence':r[2]} for r in rows])

@app.route('/api/today')
def today():
    today_str = datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT emotion,COUNT(*) FROM detections WHERE timestamp LIKE ? GROUP BY emotion",
        (f'{today_str}%',)
    ).fetchall()
    conn.close()
    return jsonify({r[0]: r[1] for r in rows})

# ── DASHBOARD ─────────────────────────────────────────────────────
DASHBOARD = r'''
<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8">
<title>Heard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
<style>
:root {
  --bg: #080810; --card: #11111f; --border: #1e1e32;
  --text: #e8e8f0; --dim: #4a4a6a;
  --happy: #f0a500; --angry: #e84040; --neutral: #20b2aa;
  --green: #00e676; --red: #ff1744;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; min-height: 100vh; }

/* TOP BAR */
.topbar { display: flex; align-items: center; justify-content: space-between;
  padding: 18px 28px; border-bottom: 1px solid var(--border); }
.logo { font-size: 22px; font-weight: 200; letter-spacing: 8px; color: var(--green); }
.logo span { font-weight: 700; }
.status-row { display: flex; gap: 16px; align-items: center; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green);
  box-shadow: 0 0 8px var(--green); animation: pulse 2s infinite; }
.status-dot.off { background: var(--dim); box-shadow: none; animation: none; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
.status-txt { font-size: 12px; color: var(--dim); letter-spacing: 1px; }

/* LAYOUT */
.wrap { padding: 24px 28px; max-width: 1000px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
.grid.triple { grid-template-columns: 1fr 1fr 1fr; }
.full { grid-column: 1 / -1; }

/* CARDS */
.card { background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 22px; }
.card-title { font-size: 10px; letter-spacing: 2px; color: var(--dim);
  text-transform: uppercase; margin-bottom: 16px; }

/* CURRENT EMOTION */
.emo-big { text-align: center; padding: 16px 0; }
.emo-label { font-size: 52px; font-weight: 700; letter-spacing: 4px;
  transition: color .4s, text-shadow .4s; }
.emo-conf { font-size: 13px; color: var(--dim); margin-top: 8px; }
.emo-bar { height: 4px; border-radius: 2px; margin-top: 16px;
  transition: width .5s, background .5s; background: var(--dim); }

/* CONTROLS */
.btn { padding: 10px 22px; border-radius: 10px; border: none; cursor: pointer;
  font-size: 13px; font-weight: 600; letter-spacing: 1px; transition: all .2s; }
.btn-green { background: var(--green); color: #000; }
.btn-green:hover { filter: brightness(1.2); }
.btn-red   { background: var(--red);   color: #fff; }
.btn-red:hover   { filter: brightness(1.2); }
.btn-outline { background: transparent; border: 1px solid var(--border);
  color: var(--dim); }
.btn-outline:hover { border-color: var(--text); color: var(--text); }
.controls { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }

/* UPLOAD ZONE */
.upload-zone { border: 1px dashed var(--border); border-radius: 12px;
  padding: 20px; text-align: center; cursor: pointer; transition: border-color .2s; }
.upload-zone:hover { border-color: var(--green); }
.upload-zone input { display: none; }
.upload-result { margin-top: 12px; padding: 10px 14px; border-radius: 8px;
  font-size: 13px; display: none; }
.upload-result.happy  { background: #1a1400; color: var(--happy); border: 1px solid var(--happy); }
.upload-result.anger, .upload-result.angry {
  background: #1a0000; color: var(--angry); border: 1px solid var(--angry); }
.upload-result.other  { background: #0d1a1a; color: var(--neutral); border: 1px solid var(--neutral); }

/* STAT BOXES */
.stat-num  { font-size: 40px; font-weight: 700; }
.stat-lbl  { font-size: 11px; color: var(--dim); margin-top: 4px; letter-spacing: 1px; text-transform: uppercase; }
.stat-happy { color: var(--happy); }
.stat-angry { color: var(--angry); }
.stat-neutral{ color: var(--neutral); }

/* LOG */
.log-row { display: flex; align-items: center; gap: 12px;
  padding: 9px 0; border-bottom: 1px solid var(--border); font-size: 13px; }
.log-row:last-child { border-bottom: none; }
.log-time { color: var(--dim); min-width: 72px; font-size: 12px; }
.log-dot  { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.log-emo  { font-weight: 600; min-width: 70px; }
.log-conf { margin-left: auto; color: var(--dim); font-size: 12px; }

/* ALERT */
.alert-banner { background: #200000; border: 1px solid var(--angry);
  border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;
  color: var(--angry); font-size: 14px; display: none;
  animation: alertpulse 1.5s infinite; }
@keyframes alertpulse { 0%,100%{opacity:1} 50%{opacity:.7} }

/* CHART */
canvas { max-height: 160px; }
</style>
</head>
<body>

<div class="topbar">
  <div class="logo">H<span>EARD</span></div>
  <div class="status-row">
    <div class="status-dot" id="liveDot"></div>
    <span class="status-txt" id="liveText">MONITORING</span>
    <span class="status-txt" style="color:var(--dim)">|</span>
    <span class="status-txt" id="lastSeen">—</span>
  </div>
</div>

<div class="wrap">

  <div class="alert-banner" id="alertBanner">
    ⚠ Repeated distress detected — caregiver should check on the child
  </div>

  <div class="grid">

    <!-- CURRENT EMOTION -->
    <div class="card">
      <div class="card-title">Current State</div>
      <div class="emo-big">
        <div class="emo-label" id="emoLabel">—</div>
        <div class="emo-conf"  id="emoConf">waiting...</div>
        <div class="emo-bar"   id="emoBar" style="width:0%"></div>
      </div>
    </div>

    <!-- TODAY CHART -->
    <div class="card">
      <div class="card-title">Today's Breakdown</div>
      <canvas id="todayChart"></canvas>
    </div>

    <!-- STATS -->
    <div class="card">
      <div class="card-title">Today's Count</div>
      <div style="display:flex;gap:28px;padding-top:8px">
        <div><div class="stat-num stat-happy" id="statHappy">0</div>
             <div class="stat-lbl">Happy</div></div>
        <div><div class="stat-num stat-angry" id="statAngry">0</div>
             <div class="stat-lbl">Angry</div></div>
        <div><div class="stat-num stat-neutral" id="statOther">0</div>
             <div class="stat-lbl">Other</div></div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="card">
      <div class="card-title">Controls</div>
      <div class="controls">
        <button class="btn btn-green" id="toggleBtn" onclick="toggleRecording()">
          ⏸ Pause Monitoring
        </button>
        <button class="btn btn-outline" onclick="clearLog()">
          Clear Log
        </button>
      </div>
      <div style="margin-top:16px;font-size:12px;color:var(--dim)">
        Pause to stop microphone capture during quiet periods or demos.
      </div>
    </div>

    <!-- FILE UPLOAD -->
    <div class="card full">
      <div class="card-title">Test Audio File</div>
      <div class="upload-zone" onclick="document.getElementById('fileInput').click()">
        <input type="file" id="fileInput" accept=".wav,.mp3,.m4a,.webm" onchange="uploadFile(event)">
        <div style="font-size:28px;margin-bottom:8px">🎵</div>
        <div style="font-size:14px;color:var(--dim)">
          Click to upload an audio file — WAV, MP3, M4A supported
        </div>
        <div style="font-size:12px;color:var(--dim);margin-top:4px">
          Model will classify and result will appear in the log
        </div>
      </div>
      <div class="upload-result" id="uploadResult"></div>
    </div>

    <!-- LOG -->
    <div class="card full">
      <div class="card-title">Recent Detections</div>
      <div id="logList">
        <div style="color:var(--dim);font-size:13px">No detections yet...</div>
      </div>
    </div>

  </div>
</div>

<script>
const COLORS = {
  happy: 'var(--happy)', anger: 'var(--angry)', angry: 'var(--angry)',
  neutral: 'var(--neutral)', fear: '#9b59b6', sad: '#3a7bd5'
};

let isRecording = true;

// ── POLL EVERY 4 SECONDS ──────────────────────────────────────────
setInterval(() => { loadHistory(); loadToday(); }, 4000);
loadHistory(); loadToday();

async function loadHistory() {
  try {
    const r    = await fetch('/api/history');
    const data = await r.json();

    if (data.length === 0) return;

    // Current emotion
    const latest = data[0];
    const label  = document.getElementById('emoLabel');
    const conf   = document.getElementById('emoConf');
    const bar    = document.getElementById('emoBar');
    const color  = COLORS[latest.emotion] || 'var(--text)';

    label.textContent  = latest.emotion.toUpperCase();
    label.style.color  = color;
    label.style.textShadow = `0 0 30px ${color}44`;
    conf.textContent   = `${Math.round(latest.confidence * 100)}% confident`;
    bar.style.width    = `${Math.round(latest.confidence * 100)}%`;
    bar.style.background = color;

    // Last seen time
    const t = latest.time.split(' ')[1] || latest.time;
    document.getElementById('lastSeen').textContent = `Last: ${t}`;

    // Log
    const logEl = document.getElementById('logList');
    logEl.innerHTML = '';
    data.slice(0, 20).forEach(d => {
      const c   = COLORS[d.emotion] || '#888';
      const row = document.createElement('div');
      row.className = 'log-row';
      row.innerHTML = `
        <span class="log-time">${d.time.split(' ')[1] || d.time}</span>
        <span class="log-dot" style="background:${c}"></span>
        <span class="log-emo" style="color:${c}">${d.emotion.toUpperCase()}</span>
        <span class="log-conf">${Math.round(d.confidence*100)}%</span>`;
      logEl.appendChild(row);
    });

    // Alert — 5+ angry/fear in last 30 detections
    const recent  = data.slice(0, 30);
    const distress = recent.filter(d =>
      d.emotion === 'anger' || d.emotion === 'angry'
    ).length;
    document.getElementById('alertBanner').style.display =
      distress >= 5 ? 'flex' : 'none';

  } catch(e) {}
}

async function loadToday() {
  try {
    const r    = await fetch('/api/today');
    const data = await r.json();

    document.getElementById('statHappy').textContent =
      (data['happy'] || 0);
    document.getElementById('statAngry').textContent =
      (data['anger'] || 0) + (data['angry'] || 0);
    const other = Object.entries(data)
      .filter(([k]) => !['happy','anger','angry'].includes(k))
      .reduce((s,[,v]) => s+v, 0);
    document.getElementById('statOther').textContent = other;

    const emotions = ['happy','anger','fear','neutral','sad'];
    const labels   = emotions.filter(e => data[e]);
    const values   = labels.map(e => data[e] || 0);
    const colors   = labels.map(e => {
      if (e==='happy')  return '#f0a500';
      if (e==='anger')  return '#e84040';
      if (e==='fear')   return '#9b59b6';
      if (e==='neutral')return '#20b2aa';
      return '#3a7bd5';
    });

    const ctx = document.getElementById('todayChart').getContext('2d');
    if (window._chart) window._chart.destroy();
    window._chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ data: values, backgroundColor: colors,
          borderRadius: 8, borderSkipped: false }]
      },
      options: {
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: '#4a4a6a' }, grid: { color: '#1e1e32' } },
          y: { ticks: { color: '#4a4a6a' }, grid: { color: '#1e1e32' } }
        }
      }
    });
  } catch(e) {}
}

async function toggleRecording() {
  const r    = await fetch('/toggle', { method: 'POST' });
  const data = await r.json();
  isRecording = data.recording;

  const btn = document.getElementById('toggleBtn');
  const dot = document.getElementById('liveDot');
  const txt = document.getElementById('liveText');

  if (isRecording) {
    btn.textContent  = '⏸ Pause Monitoring';
    btn.className    = 'btn btn-green';
    dot.className    = 'status-dot';
    txt.textContent  = 'MONITORING';
  } else {
    btn.textContent  = '▶ Resume Monitoring';
    btn.className    = 'btn btn-red';
    dot.className    = 'status-dot off';
    txt.textContent  = 'PAUSED';
  }
}

async function uploadFile(event) {
  const file   = event.target.files[0];
  if (!file) return;

  const result = document.getElementById('uploadResult');
  result.style.display = 'block';
  result.className     = 'upload-result other';
  result.textContent   = 'Analysing...';

  const form = new FormData();
  form.append('file', file);

  try {
    const r    = await fetch('/upload', { method: 'POST', body: form });
    const data = await r.json();

    if (data.error) {
      result.textContent = '⚠ Error: ' + data.error;
      return;
    }

    const emo  = data.emotion;
    const conf = Math.round(data.confidence * 100);
    result.className   = `upload-result ${emo}`;
    result.textContent = `${emo.toUpperCase()} — ${conf}% confident`;

    // Refresh
    loadHistory(); loadToday();
  } catch(e) {
    result.textContent = '⚠ Could not connect to server.';
  }
}

async function clearLog() {
  // Just reload — no delete endpoint needed for demo
  await loadHistory();
}
</script>
</body></html>
'''

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD)

if __name__ == '__main__':
    print("\n  Heard server running")
    print("  Dashboard  →  http://localhost:5000")
    print("  ESP32      →  http://YOUR_IP:5000/latest\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
