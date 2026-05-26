# Plivo IVR — Quick Reference Card

## 📱 System Overview

```
Your Phone
    ↓
Plivo Receives Call → Routes to Flask Webhook
                        ↓
                   Flask App (http://localhost:5000)
                        ↓
                   Returns XML Response
                        ↓
                   Plivo Reads XML → Handles Call
                        ↓
                   IVR Flow Executes
```

---

## 🔧 Configuration Checklist

### Before First Test:

- [ ] **OTP Secret** — Update line 20 in `app.py` with your birthdate (DDMM)
  ```python
  OTP_SECRET = "MMDD"  # e.g., "1503" for March 15
  ```

- [ ] **ngrok Running** — In separate terminal:
  ```bash
  ngrok http 5000
  ```
  Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

- [ ] **BASE_URL Updated** — Line 26 in `app.py`:
  ```python
  BASE_URL = "https://your-ngrok-url.ngrok.io"
  ```

- [ ] **Flask Running** — Terminal shows:
  ```
  Running on http://127.0.0.1:5000
  ```

---

## 📞 Making a Call

### Method 1: Web UI (Easiest)
```
1. Open http://localhost:5000 in browser
2. Enter phone number: +91XXXXXXXXXX
3. Click "Make Call"
4. Answer your phone when it rings
```

### Method 2: curl
```bash
curl "http://localhost:5000/make_call?to=%2B91XXXXXXXXXX"
```

### Method 3: Python Script
```python
import requests
response = requests.get(
    "http://localhost:5000/make_call",
    params={"to": "+91XXXXXXXXXX"}
)
print(response.json())
```

---

## 🎯 IVR Flow — Quick Test

### Flow Diagram
```
CALL ANSWERED
    ↓
[OTP] Enter 4 digits
    ├─ Wrong → Re-prompt
    └─ Correct ↓
[LANGUAGE] Press 1 or 2
    ├─ 1: English → [MENU_EN]
    └─ 2: Spanish → [MENU_ES]
[MENU] Press 1 or 2
    ├─ 1: Play audio → Hang up
    └─ 2: Transfer → Route to the Live associate
```

### Test Script (Step-by-Step)

| Step | What You Hear | What You Do | Expected |
|------|--------------|-----------|----------|
| 1 | "Welcome... enter O T P" | Press wrong (e.g., 1234) | "Incorrect... try again" |
| 2 | "Welcome... enter O T P" | Press correct (e.g., 1503) | "O T P verified" |
| 3 | "Select language: 1=English, 2=Spanish" | Press 1 | English menu |
| 4 | "Select option: 1=audio, 2=associate" | Press 1 | Audio plays → Hang up |

---

## 🗂️ File Structure

```
plivo-ivr/
├── app.py                 ← Main application (EDIT LINES 20, 26)
├── requirements.txt       ← Python packages
├── README.md              ← Complete documentation
├── SETUP_GUIDE.md         ← Detailed setup instructions
└── QUICK_REFERENCE.md     ← This file

```
## 🌐 API Endpoints

| GET/POST | Purpose | Query Params |
|----------|---------|--------------|
| `/` | Web UI | — |
| `/make_call` | Initiate call | `to=+91XXXXXXXXXX` |
| `/ivr/otp` | OTP prompt | — |
| `/ivr/otp_verify` | OTP validation | `Digits=1234` |
| `/ivr/language` | Language menu | — |
| `/ivr/language_select` | Language handler | `Digits=1\|2` |
| `/ivr/menu` | Action menu | `lang=en\|es` |
| `/ivr/menu_select` | Action handler | `Digits=1\|2`, `lang=en\|es` |

```

## 🎤 Prompts (Exact Text)

### English
```
"Welcome to InspireWorks. Please enter your 4 digit O T P to continue."
"Incorrect O T P. Please try again."
"O T P verified. Welcome!"
"Please select your language. Press 1 for English. Press 2 for Spanish."
"Please select an option. Press 1 to hear an audio message. Press 2 to connect to a live associate."
"Here is your audio message."
"Thank you for calling InspireWorks. Goodbye."
"Connecting you to a live associate. Please hold."
```

### Spanish
```
"Seleccione una opción. Presione 1 para escuchar un mensaje de audio. Presione 2 para hablar con un asociado."
"Aquí está su mensaje de audio."
"Gracias por llamar. Hasta luego."
"Conectándole con un asociado. Por favor espere."
```

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: flask` | `pip install -r requirements.txt` |
| "Connection refused" | Start Flask: `python app.py` |
| Plivo call doesn't arrive | Check ngrok running + BASE_URL updated |
| DTMF not recognized | Wait for voice prompt, press digits slowly |
| Audio won't play | Verify audio URL is publicly accessible |
| "No input received" | You took too long (10 sec timeout) |

---
```
## ⏱️ Timeouts & Retries

- **DTMF Input Timeout**: 10 seconds (wait for your input)
- **Max Retries**: 1 (re-prompt once if wrong/no input)
- **Call Duration**: ~2-3 min for full flow test
```
---



- **Flask Issues**: https://flask.palletsprojects.com/
- **Plivo Issues**: https://www.plivo.com/docs/ (or check dashboard)
- **ngrok Issues**: https://ngrok.com/docs
- **Python**: https://docs.python.org/3/

Good luck! 📞✅
