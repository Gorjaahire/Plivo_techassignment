# InspireWorks IVR Demo — Plivo Voice API

A Flask-based multi-level IVR system with OTP authentication built on Plivo's Voice API.

---

## 📞 Call Flow

```
Outbound Call (from +91 22 6423 2030)
    ↓
OTP Prompt (4-digit DDMM birthdate)
    ├─ Wrong OTP → Re-prompt
    └─ Correct OTP
            ↓
Level 1: Language Selection
    ├─ Press 1 → English
    └─ Press 2 → Spanish
            ↓
Level 2: Action Menu
    ├─ Press 1 → Play audio message
    └─ Press 2 → Transfer to live associate (+91 2264236412)
```

---

## Prerequisites

- **Python 3.8+**
- **ngrok** (for exposing local server to public internet)
- Plivo Account with:
  - **Auth ID**: `YOUR_PLIVO_AUTH_ID`
  - **Auth Token**: `YOUR_PLIVO_AUTH_TOKEN`
  - **Plivo Number**: `+91 22 6423 2030`
  - **Associate Number**: `02264236412`

---

## 🚀 Quick Start

### 1. Clone / Extract the Project

```bash
cd c:\Users\Gorja\.vscode\working\ thingies\plivo-ivr
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install flask>=2.3.0 plivo>=4.45.0 requests>=2.31.0
```

### 3. Set Your OTP (Birthdate in DDMM)

Open `app.py` and update line 20:

```python
OTP_SECRET = "1503"   # ← replace with YOUR birthdate in DDMM format
```

### 4. Expose your local server with ngrok

```bash
ngrok http 5000
```

Copy the `https://xxxx.ngrok.io` URL — you'll need it as `BASE_URL`.

### 5. Set environment variables (optional — defaults are pre-filled)

```bash
export PLIVO_AUTH_ID="YOUR_PLIVO_AUTH_ID"
export PLIVO_AUTH_TOKEN="YOUR_PLIVO_AUTH_TOKEN"
export PLIVO_NUMBER="+912264232030"
export ASSOCIATE_NUMBER="02264236412"
export BASE_URL="https://xxxx.ngrok.io"   # ← your ngrok URL
export TO_NUMBER="+91XXXXXXXXXX"          # optional default destination
```

Or edit the constants directly in `app.py`.

### 6. Run the server

```bash
python app.py
```

---

## Making a Call

### Via Web UI

Open `http://localhost:5000` in your browser, enter a phone number, and click **Make Call**.

### Via curl

```bash
curl "http://localhost:5000/make_call?to=+91XXXXXXXXXX"
```

### Via Python (standalone trigger)

```python
import plivo
client = plivo.RestClient("YOUR_PLIVO_AUTH_ID", "YOUR_PLIVO_AUTH_TOKEN")
client.calls.create(
    from_="+912264232030",
    to_="+91XXXXXXXXXX",
    answer_url="https://xxxx.ngrok.io/ivr/otp",
    answer_method="GET",
)
```

---

## API Endpoints

| Route | Purpose |
|---|---|
| `GET /` | Simple web UI to trigger a call |
| `GET/POST /make_call?to=<number>` | Initiates outbound call via Plivo |
| `GET/POST /ivr/otp` | Plivo webhook — OTP prompt |
| `GET/POST /ivr/otp_verify` | Validates DTMF input against OTP |
| `GET/POST /ivr/language` | Level 1 — language selection menu |
| `GET/POST /ivr/language_select` | Routes based on language digit |
| `GET/POST /ivr/menu?lang=en\|es` | Level 2 — action menu (language-aware) |
| `GET/POST /ivr/menu_select?lang=en\|es` | Handles audio play or call transfer |

---

## Plivo Credentials

| Key | Value |
|---|---|
| Auth ID | `YOUR_PLIVO_AUTH_ID` |
| Auth Token | `YOUR_PLIVO_AUTH_TOKEN` |
| Plivo Number | `+912264232030` |
| Live Associate | `02264236412` |

> **Security note:** Move credentials to environment variables or a `.env` file before committing to a public repository.

---

## Testing Checklist

- [ ] Wrong OTP entered → bot re-prompts
- [ ] Correct OTP entered → reaches language menu
- [ ] Press 1 (English) → English Level 2 menu
- [ ] Press 2 (Spanish) → Spanish Level 2 menu
- [ ] Press 1 in Level 2 → audio plays then hangs up
- [ ] Press 2 in Level 2 → call forwarded to associate number
- [ ] Invalid input at any level → current menu repeats

---

## Project Structure

```
plivo-ivr/
├── app.py            # Main Flask application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## 🔧 Troubleshooting

### 1. **`ModuleNotFoundError: No module named 'flask'`**
   - Install dependencies: `pip install -r requirements.txt`

### 2. **`Connection refused` when making a call**
   - Make sure Flask server is running: `python app.py`
   - Verify ngrok is running in another terminal: `ngrok http 5000`
   - Check that `BASE_URL` in `app.py` matches your ngrok URL

### 3. **Plivo call fails with 401 Unauthorized**
   - Verify Auth ID and Auth Token are correct
   - Check that credentials are properly set in environment or `app.py`

### 4. **DTMF input not being recognized**
   - Ensure the call was answered before pressing digits
   - Wait for the voice prompt before entering the OTP
   - Some VoIP providers may require tone generation settings

### 5. **Audio file not playing**
   - Verify the `AUDIO_URL` is publicly accessible
   - Test the URL directly in a browser
   - Ensure the file format is supported (MP3, WAV, etc.)

---

## 📝 Demo Script

### Scenario: Successful Full Flow

1. **Start Server:**
   ```bash
   python app.py
   ```
   Note the ngrok URL (e.g., `https://abc123.ngrok.io`)

2. **Make Outbound Call:**
   - Visit `http://localhost:5000`
   - Enter your phone number
   - Click **Make Call**

3. **Answer the Call:**
   - Your phone rings from Plivo number `+91 22 6423 2030`
   - Answer the call

4. **OTP Authentication:**
   - Bot says: "Welcome to InspireWorks. Please enter your 4 digit O T P to continue."
   - Enter **wrong OTP** (e.g., 1234)
   - Bot says: "Incorrect O T P. Please try again."
   - Enter **correct OTP** (your birthdate in DDMM, e.g., 1503)
   - Bot says: "O T P verified. Welcome!"

5. **Language Selection (Level 1):**
   - Bot says: "Please select your language. Press 1 for English. Press 2 for Spanish."
   - Press **1** for English (or **2** for Spanish)

6. **Action Menu (Level 2):**
   - English: "Please select an option. Press 1 to hear an audio message. Press 2 to connect to a live associate."
   - Spanish: "Seleccione una opción. Presione 1 para escuchar un mensaje de audio. Presione 2 para hablar con un asociado."
   - Press **1** to hear audio
   - Bot plays a message, then audio, then hangs up
   - OR Press **2** to transfer to live associate (`02264236412`)

---

## 🚀 Deployment

### For Production

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set secure environment variables:**
   ```bash
   export PLIVO_AUTH_ID="your_auth_id"
   export PLIVO_AUTH_TOKEN="your_auth_token"
   export BASE_URL="https://your-domain.com"
   ```

3. **Use a reverse proxy (e.g., Nginx)** to handle SSL/TLS

4. **Monitor Plivo logs** in your Plivo dashboard for call metrics

---

## 📞 Plivo API Reference

- **Make Call**: [plivo.com/docs/voice/api/call/](https://www.plivo.com/docs/voice/api/call/)
- **XML Reference**: [plivo.com/docs/voice/xml/](https://www.plivo.com/docs/voice/xml/)
- **DTMF (Digits)**: [plivo.com/docs/voice/xml/getdigits/](https://www.plivo.com/docs/voice/xml/getdigits/)
- **Speak**: [plivo.com/docs/voice/xml/speak/](https://www.plivo.com/docs/voice/xml/speak/)
- **Play**: [plivo.com/docs/voice/xml/play/](https://www.plivo.com/docs/voice/xml/play/)
- **Dial/Transfer**: [plivo.com/docs/voice/xml/dial/](https://www.plivo.com/docs/voice/xml/dial/)

---

## 📚 Features Implemented

✅ **Outbound Call Initiation** — Flask endpoint to trigger calls via Plivo  
✅ **OTP Authentication** — 4-digit DDMM birthdate verification with re-prompting  
✅ **Multi-level IVR** — Language selection (Level 1) → Action menu (Level 2)  
✅ **Bilingual Support** — English and Spanish prompts  
✅ **Audio Playback** — Play publicly accessible MP3 files  
✅ **Call Transfer** — Forward to live associate number  
✅ **DTMF Input Handling** — Robust digit input with retries  
✅ **Web UI** — Simple interface to trigger calls  
✅ **Error Handling** — Invalid inputs, timeouts, hangups  

---

## 📄 License

This project is provided as-is for evaluation and demo purposes.

---

## ❓ Support

For issues with:
- **Flask/Python**: Check Python version (3.8+) and dependencies
- **Plivo API**: Consult [Plivo documentation](https://www.plivo.com/docs/)
- **ngrok**: Visit [ngrok docs](https://ngrok.com/docs)

