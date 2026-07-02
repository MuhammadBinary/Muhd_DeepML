import os, time, threading
import numpy as np
import librosa
import sounddevice as sd
import serial
import serial.tools.list_ports
import requests
from colorama import init, Fore, Style
init(autoreset=True)

SR                = 22050
EMOTIONS          = ['anger', 'fear', 'happy', 'neutral', 'sad']
TARGET            = {'anger': 'A', 'happy': 'H'}
SERVER            = 'http://localhost:5000/predict'
STATE_URL         = 'http://localhost:5000/state'
LATEST_URL        = 'http://localhost:5000/latest'
SILENCE_THRESHOLD = 0.012
CONFIDENCE_MIN    = 0.60
STREAK_NEEDED     = 2

_ser      = None
_ser_lock = threading.Lock()

def load_model():
    if os.path.exists('inference_model.onnx'):
        import onnxruntime as ort
        sess = ort.InferenceSession('inference_model.onnx')
        name = sess.get_inputs()[0].name
        print(Fore.GREEN + "  Model loaded (ONNX)")
        return lambda f: sess.run(None, {name: f})[0][0]
    print(Fore.RED + "  No model file. Put inference_model.onnx here.")
    exit(1)

def find_arduino():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        desc = (p.description or '').lower()
        if any(k in desc for k in ['arduino', 'ch340', 'ch341', 'cp210', 'usb serial']):
            return p.device
    if len(ports) == 1:
        return ports[0].device
    return None

def extract(audio):
    zcr  = librosa.feature.zero_crossing_rate(audio)
    rms  = librosa.feature.rms(y=audio)
    mfcc = librosa.feature.mfcc(y=audio, sr=SR, n_mfcc=40)
    feat = np.vstack([zcr, rms, mfcc])
    feat = feat[:, :130] if feat.shape[1] >= 130 \
           else np.pad(feat, ((0,0),(0, 130 - feat.shape[1])))
    feat = (feat - feat.mean()) / (feat.std() + 1e-8)
    return feat[np.newaxis, ...].astype(np.float32)

def send_to_server(emotion, confidence):
    try:
        requests.post(SERVER,
                      json={'emotion': emotion, 'confidence': float(confidence)},
                      timeout=0.5)
    except:
        pass

def is_paused():
    try:
        r = requests.get(STATE_URL, timeout=0.3)
        return not r.json().get('recording', True)
    except:
        return False

def send_serial(code):
    # Thread-safe serial write
    with _ser_lock:
        if _ser:
            try:
                _ser.write(code.encode())
            except:
                pass

# ── BACKGROUND THREAD ─────────────────────────────────────────────

def arduino_sync_thread():
    last_sent = None
    while True:
        try:
            r    = requests.get(LATEST_URL, timeout=0.8)
            data = r.json()
            emo  = data.get('emotion', 'neutral')
            conf = data.get('confidence', 0.0)

            code = TARGET[emo] if (emo in TARGET and conf >= 0.5) else 'N'

            # Only send if emotion changed — avoid flooding serial
            if code != last_sent:
                send_serial(code)
                last_sent = code
                print(Fore.CYAN + Style.DIM +
                      f'  [arduino sync] → {emo} ({conf:.0%}) → sent {code}')
        except:
            pass

        time.sleep(2)

def main():
    global _ser

    os.system('cls')
    print(Fore.CYAN + Style.BRIGHT + '\n  HEARD — Emotion Detection\n')

    run = load_model()

    # Connect Arduino
    port = find_arduino()
    if port:
        try:
            _ser = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)
            print(Fore.GREEN + f"  Arduino on {port}")
        except:
            print(Fore.YELLOW + "  Arduino found but could not connect")
            _ser = None
    else:
        print(Fore.YELLOW + "  No Arduino found — predictions still log to dashboard")
        _ser = None

    sync = threading.Thread(target=arduino_sync_thread, daemon=True)
    sync.start()
    print(Fore.GREEN + "  Arduino sync thread running")

    print(Fore.WHITE + Style.DIM + '\n  Listening. Ctrl+C to stop.')
    print(Fore.WHITE + Style.DIM + '  Go to dashboard and click Resume if paused.\n')
    print(f"  {'STATUS':<14} {'EMOTION':<12} {'CONF':>5}  NOTE")
    print('  ' + '─' * 52)

    streak   = 0
    last_emo = None

    try:
        while True:
            if is_paused():
                print(Fore.WHITE + Style.DIM +
                      '  [mic paused — go to dashboard and click Resume]')
                time.sleep(2)
                continue

            # Record 2-second window from mic
            audio = sd.rec(int(2 * SR), samplerate=SR, channels=1, dtype='float32')
            sd.wait()
            audio = audio.flatten()

            # Skip silence
            rms_energy = float(np.sqrt(np.mean(audio ** 2)))
            if rms_energy < SILENCE_THRESHOLD:
                print(Fore.WHITE + Style.DIM +
                      f'  {"silence":<14} {"—":<12} {"—":>5}  rms={rms_energy:.4f}')
                continue

            # Predict
            probs = run(extract(audio))
            idx   = int(np.argmax(probs))
            emo   = EMOTIONS[idx]
            conf  = float(probs[idx])

            # Debounce streak
            if emo == last_emo:
                streak += 1
            else:
                last_emo = emo
                streak   = 1

            if emo in TARGET and conf >= CONFIDENCE_MIN and streak >= STREAK_NEEDED:
                color = Fore.YELLOW if emo == 'happy' else Fore.RED
                note  = f'streak={streak} ✓'
            else:
                color = Fore.WHITE + Style.DIM
                note  = 'waiting' if streak < STREAK_NEEDED else 'low conf'

            # Send to server
            send_to_server(emo, conf)

            print(f'  {color + Style.BRIGHT}{"voice":<14}{emo:<12}'
                  f'{conf:.0%}  {note}  rms={rms_energy:.3f}')

    except KeyboardInterrupt:
        send_serial('N')
        if _ser:
            _ser.close()
        print(Fore.WHITE + Style.DIM + '\n  Stopped.\n')

if __name__ == '__main__':
    main()
