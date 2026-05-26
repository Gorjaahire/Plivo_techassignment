# InspireWorks IVR Demo — Complete Setup & Testing Guide

## ✅ Current Status

The Plivo IVR application is **fully implemented** and **currently running** on `http://localhost:5000`. 

All core features are ready:
- ✅ OTP authentication with re-prompting
- ✅ Multi-level IVR (Language → Action)
- ✅ Bilingual support (English & Spanish)
- ✅ Audio playback
- ✅ Call transfer to live associate
- ✅ Web UI for triggering calls

---

## 🎯 Quick Start (5 Minutes)

### Step 1: Update Your OTP (Birthdate)

**File**: `app.py` — **Line 20**

```python
OTP_SECRET = "1503"   # ← Replace with YOUR birthdate in DDMM format
```

Examples:
- Birthday: March 15 → `"1503"`
- Birthday: December 25 → `"2512"`
- Birthday: January 1 → `"0101"`

### Step 2: Expose Your Server with ngrok

**Why?** Plivo webhooks need a public URL to reach your local Flask app.

```bash
# In a new terminal window:
ngrok http 5000
```

You'll see output like:
```
ngrok                                                       (Ctrl+C to quit)

Session Status                online
Account                       <your-account>
Version                        3.3.4
Region                         us
Forwarding                     https://abc123.ngrok.io -> http://localhost:5000
```

**Copy this URL**: `https://abc123.ngrok.io` (yours will be different)

### Step 3: Update BASE_URL in app.py

**File**: `app.py` — **Line 26**

```python
BASE_URL = os.getenv("BASE_URL", "https://abc123.ngrok.io")  # ← Paste YOUR ngrok URL
```

### Step 4: Restart Flask Server

In the terminal running Flask, press **Ctrl+C** and run again:

```bash
python app.py
```

Watch for:
```
Running on http://127.0.0.1:5000
Debugger PIN: xxxxxx
```

### Step 5: Make a Test Call

**Via Web UI** (recommended):
1. Open `http://localhost:5000` in your browser
2. Enter your phone number: `+91XXXXXXXXXX`
3. Click **Make Call**
4. Check Plivo dashboard for call status

**Via curl**:
```bash
curl "http://localhost:5000/make_call?to=%2B91XXXXXXXXXX"
```

---

## 🎬 Testing the Full IVR Flow

### Scenario: Complete Walkthrough

**Estimated time**: 3–5 minutes

#### 1️⃣ **Outbound Call**
- Browser shows: `{"status": "call initiated", "request_uuid": "..."}`
- **Your phone rings** in ~2–3 seconds
- Origin: `+91 xxxxxxxxxx` (Plivo number)

#### 2️⃣ **OTP Authentication**
- Bot says: *"Welcome to InspireWorks. Please enter your 4 digit O T P to continue."*
- **Test Case A**: Enter WRONG OTP (e.g., press `1234`)
  - Bot says: *"Incorrect O T P. Please try again."*
  - Bot repeats: *"Welcome to InspireWorks. Please enter your 4 digit O T P to continue."*
- **Test Case B**: Enter CORRECT OTP (your birthdate, e.g., press `1503`)
  - Bot says: *"O T P verified. Welcome!"*

#### 3️⃣ **Language Selection (Level 1)**
- Bot says: *"Please select your language. Press 1 for English. Press 2 for Spanish."*
- **Option A**: Press `1`
  - Language set to **English**
  - Proceed to Level 2 (English menu)
- **Option B**: Press `2`
  - Language set to **Spanish**
  - Proceed to Level 2 (Spanish menu)

#### 4️⃣ **Action Menu (Level 2) — English**
- Bot says: *"Please select an option. Press 1 to hear an audio message. Press 2 to connect to a live associate."*
- **Option A**: Press `1` (Audio)
  - Bot says: *"Here is your audio message."*
  - **Audio plays** (SoundHelix example MP3)
  - Bot says: *"Thank you for calling InspireWorks. Goodbye."*
  - **Call ends**
- **Option B**: Press `2` (Transfer)
  - Bot says: *"Connecting you to a live associate. Please hold."*
  - **Call transferred to**: live associate placeholder
  - If no one picks up, call ends

#### 5️⃣ **Action Menu (Level 2) — Spanish**
- Bot says: *"Seleccione una opción. Presione 1 para escuchar un mensaje de audio. Presione 2 para hablar con un asociado."*
- **Option A**: Press `1` (Audio)
  - Bot says: *"Aquí está su mensaje de audio."*
  - **Audio plays**
  - Bot says: *"Gracias por llamar. Hasta luego."*
  - **Call ends**
- **Option B**: Press `2` (Transfer)
  - Bot says: *"Conectándole con un asociado. Por favor espere."*
  - **Call transferred to**: `02264236412`

---

## 🔍 Verification Checklist

- [ ] **Outbound call** initiated from Plivo number
- [ ] **OTP wrong**: Re-prompts for correct OTP
- [ ] **OTP correct**: Proceeds to language menu
- [ ] **Language 1 (English)**: English prompts play
- [ ] **Language 2 (Spanish)**: Spanish prompts play
- [ ] **Action 1 (Audio)**: Audio file plays and call ends
- [ ] **Action 2 (Transfer)**: Call forwarded to associate number
- [ ] **Invalid input**: Menu repeats without breaking
- [ ] **Web UI works**: Can trigger calls from `http://localhost:5000`
- [ ] **ngrok active**: Plivo webhooks reach your Flask app

---

## 📊 Monitoring & Debugging

### 1. Check Flask Logs

The terminal running Flask shows:
```
127.0.0.1 - - [26/May/2026 12:00:00] "GET /ivr/otp HTTP/1.1" 200 -
127.0.0.1 - - [26/May/2026 12:00:05] "GET /ivr/otp_verify?Digits=1234 HTTP/1.1" 200 -
...
```

**Tip**: Each endpoint call produces a log entry.

### 2. Monitor Plivo Dashboard

Visit [plivo.com/app](https://plivo.com/app):
- **Call Logs**: See all calls, duration, status
- **Debug**: Check if webhooks are being received
- **Test**: Make API calls directly

### 3. Test Endpoints Directly

```bash
# Test OTP prompt
curl "http://localhost:5000/ivr/otp"

# Test language menu
curl "http://localhost:5000/ivr/language"

# Test with digits
curl "http://localhost:5000/ivr/otp_verify?Digits=1503"
curl "http://localhost:5000/ivr/language_select?Digits=1"
curl "http://localhost:5000/ivr/menu_select?Digits=1&lang=en"
```

---

## 🎥 Recording a Demo Video (3–5 min)

### Script:

1. **Intro** (15 sec):
   - "This is the InspireWorks Plivo IVR demo."
   - Show browser with web UI at `http://localhost:5000`

2. **Outbound Call** (30 sec):
   - Enter phone number, click "Make Call"
   - Show call initiated message
   - Show incoming call on phone, answer

3. **OTP Authentication** (1 min):
   - Demonstrate WRONG OTP (enter `1234`)
   - Bot re-prompts
   - Then enter CORRECT OTP (e.g., `1503`)
   - Bot confirms verification

4. **Language Selection** (20 sec):
   - Press `1` for English
   - Show English prompts

5. **Audio Playback** (1 min):
   - Press `1` to hear audio
   - Audio plays (show on screen/phone)
   - Call ends with goodbye message

6. **Call Transfer** (1 min):
   - Make another call, authenticate, select English
   - Press `2` to transfer to associate
   - Show transfer message
   - (Can end here or let it dial the associate)

7. **Outro** (15 sec):
   - "The system demonstrates OTP auth, multi-level IVR, and call routing."

**Total: ~5 minutes**

**Tip**: Screen record with audio + phone audio for best demo

---

## ⚙️ Advanced Configuration

### Use Environment Variables (Recommended for Production)

Instead of hardcoding credentials, set environment variables:

**Windows PowerShell:**
```powershell
$env:PLIVO_AUTH_ID="YOUR_PLIVO_AUTH_ID"
$env:PLIVO_AUTH_TOKEN="YOUR_PLIVO_AUTH_TOKEN"
$env:PLIVO_NUMBER="+912264232030"
$env:ASSOCIATE_NUMBER="02264236412"
$env:BASE_URL="https://your-ngrok-url.ngrok.io"
```

**Windows CMD:**
```cmd
set PLIVO_AUTH_ID=YOUR_PLIVO_AUTH_ID
set PLIVO_AUTH_TOKEN=YOUR_PLIVO_AUTH_TOKEN
...
```

**Linux/macOS:**
```bash
export PLIVO_AUTH_ID="YOUR_PLIVO_AUTH_ID"
export PLIVO_AUTH_TOKEN="YOUR_PLIVO_AUTH_TOKEN"
...
```

Then run:
```bash
python app.py
```

### Use a .env File

Create `.env` in project root:
```
PLIVO_AUTH_ID=YOUR_PLIVO_AUTH_ID
PLIVO_AUTH_TOKEN=YOUR_PLIVO_AUTH_TOKEN
PLIVO_NUMBER=+912264232030
ASSOCIATE_NUMBER=02264236412
BASE_URL=https://abc123.ngrok.io
```

Then install `python-dotenv`:
```bash
pip install python-dotenv
```

Add to `app.py` (line 6, before Flask import):
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install -r requirements.txt
```

Or:
```bash
pip install flask plivo requests
```

### Issue: ngrok connection fails

**Check:**
1. Is Flask running? (Should see `Running on http://127.0.0.1:5000`)
2. Is ngrok running in a separate terminal?
3. Does ngrok URL in `app.py` match actual ngrok URL?

**Reset:**
```bash
# Stop both Flask and ngrok (Ctrl+C)
# Restart ngrok:
ngrok http 5000

# Update app.py with new URL
# Restart Flask
```

### Issue: Plivo call fails to connect

**Check Plivo Dashboard:**
1. Are credentials correct?
2. Are call logs showing attempts?
3. Is the phone number valid?

**Test credentials:**
```bash
python -c "
import plivo
client = plivo.RestClient('YOUR_PLIVO_AUTH_ID', 'YOUR_PLIVO_AUTH_TOKEN')
print('Auth OK!')
"
```

### Issue: DTMF (digits) not being recognized

**Check:**
1. Are you waiting for the voice prompt before pressing digits?
2. Are you using a real phone (not a computer mic)?
3. Does your VoIP provider support DTMF?

**Test in Plivo Console:**
- Make a manual call via Plivo dashboard
- Try entering digits

### Issue: Audio not playing

**Check:**
1. Is the audio URL accessible?
```bash
curl "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
```

2. Try a different audio URL:
   - WAV: `https://www.soundjay.com/button/beep-07.wav`
   - MP3: Any publicly accessible MP3 file

3. Update `AUDIO_URL` in `app.py`:
```python
AUDIO_URL = "https://your-public-audio-url.mp3"
```

---

## 📚 Resources

- **Plivo Docs**: https://www.plivo.com/docs/
- **Flask**: https://flask.palletsprojects.com/
- **ngrok**: https://ngrok.com/docs
- **Python 3.8+**: https://www.python.org/

---
