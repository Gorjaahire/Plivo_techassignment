# Plivo IVR — Testing & Deployment Guide

## 🧪 Testing Scenarios

### Scenario 1: Wrong OTP → Correct OTP

**Duration**: ~1 min

```
1. Web UI: Enter +91XXXXXXXXXX, click "Make Call"
2. Answer phone when it rings
3. Bot: "Welcome... enter 4 digit OTP"
4. YOU: Press 1-2-3-4 (wrong OTP)
5. Bot: "Incorrect OTP. Please try again."
6. Bot: "Welcome... enter 4 digit OTP"
7. YOU: Press your birthdate (e.g., 1-5-0-3 for March 15)
8. Bot: "OTP verified. Welcome!"
9. RESULT: ✅ Re-prompting works
```

### Scenario 2: English → Audio Playback

**Duration**: ~1.5 min

```
1. Start from Scenario 1, after OTP verification
2. Bot: "Select language: 1=English, 2=Spanish"
3. YOU: Press 1
4. Bot: "Select option: 1=audio, 2=associate"
5. YOU: Press 1
6. Bot: "Here is your audio message."
7. Bot: [Audio plays for ~30 seconds]
8. Bot: "Thank you for calling. Goodbye."
9. Call ends
10. RESULT: ✅ Audio playback works
```

### Scenario 3: Spanish → Call Transfer

**Duration**: ~2 min

```
1. Start from Scenario 1, after OTP verification
2. Bot: "Seleccione idioma: 1=Inglés, 2=Español"
3. YOU: Press 2
4. Bot: "Seleccione opción: 1=audio, 2=asociado"
5. YOU: Press 2
6. Bot: "Conectándole con un asociado. Por favor espere."
7. Call transfers to 02264236412
   [If line is available, you hear ringing/connected]
   [If not available, call ends after timeout]
8. RESULT: ✅ Call transfer works
```

### Scenario 4: Invalid Input Handling

**Duration**: ~1 min

```
1. OTP Prompt: Press 5-6-7-8 (more than 4 digits)
   → Call hangs up after 1 retry
2. Language Menu: Press 3
   → Bot: "Invalid option. Please try again."
   → Repeats language menu
3. Action Menu: Press 9
   → Bot: "Invalid selection. Please try again."
   → Repeats action menu
4. RESULT: ✅ Error handling works
```

### Scenario 5: Timeout Handling

**Duration**: ~15 sec

```
1. OTP Prompt: Don't press anything for 11 seconds
2. Call hangs up: "We did not receive any input. Goodbye."
3. RESULT: ✅ Timeout handling works
```

---

## 🔧 API Testing with curl

### Test 1: Check Flask is Running

```bash
curl http://localhost:5000
```

Expected response: HTML page with form

### Test 2: Trigger Outbound Call

```bash
curl "http://localhost:5000/make_call?to=%2B91XXXXXXXXXX"
```

Expected response:
```json
{
  "status": "call initiated",
  "request_uuid": "6a3dee9c-abcd-1234-5678-f3b7e2a1b1c1"
}
```

### Test 3: Test OTP Endpoint (Webhook)

```bash
curl "http://localhost:5000/ivr/otp"
```

Expected response: XML with `<GetDigits>` for OTP prompt

### Test 4: Test OTP Verification

```bash
# Wrong OTP
curl "http://localhost:5000/ivr/otp_verify?Digits=1234"

# Correct OTP (using "1503" as example)
curl "http://localhost:5000/ivr/otp_verify?Digits=1503"
```

Expected responses: XML redirects

### Test 5: Test Language Selection

```bash
curl "http://localhost:5000/ivr/language"
```

### Test 6: Test Language Handler

```bash
# English (1)
curl "http://localhost:5000/ivr/language_select?Digits=1"

# Spanish (2)
curl "http://localhost:5000/ivr/language_select?Digits=2"

# Invalid (3)
curl "http://localhost:5000/ivr/language_select?Digits=3"
```

### Test 7: Test Action Menu

```bash
curl "http://localhost:5000/ivr/menu?lang=en"
curl "http://localhost:5000/ivr/menu?lang=es"
```

### Test 8: Test Menu Actions

```bash
# Audio (1) English
curl "http://localhost:5000/ivr/menu_select?Digits=1&lang=en"

# Transfer (2) Spanish
curl "http://localhost:5000/ivr/menu_select?Digits=2&lang=es"

# Invalid (3)
curl "http://localhost:5000/ivr/menu_select?Digits=3&lang=en"
```

---

## 📊 Monitoring & Debugging

### 1. Flask Debug Logs

When testing, Flask logs appear in your terminal:

```
127.0.0.1 - - [26/May/2026 12:00:00] "GET /ivr/otp HTTP/1.1" 200 -
127.0.0.1 - - [26/May/2026 12:00:05] "GET /ivr/otp_verify?Digits=1234 HTTP/1.1" 200 -
127.0.0.1 - - [26/May/2026 12:00:10] "GET /ivr/language HTTP/1.1" 200 -
127.0.0.1 - - [26/May/2026 12:00:15] "GET /ivr/language_select?Digits=1 HTTP/1.1" 200 -
127.0.0.1 - - [26/May/2026 12:00:20] "GET /ivr/menu?lang=en HTTP/1.1" 200 -
127.0.0.1 - - [26/May/2026 12:00:25] "GET /ivr/menu_select?Digits=1&lang=en HTTP/1.1" 200 -
```

**What to check:**
- Are all endpoints being called in order?
- Are HTTP status codes all 200?
- Are there any errors or exceptions?

### 2. Plivo Dashboard

Navigate to https://www.plivo.com/app/:

1. **Active Calls** → Real-time calls in progress
2. **Call Logs** → History of all calls
3. **Detailed Logs** → Webhook requests/responses
4. **Audio/Media** → Check file playback status

### 3. ngrok Inspector

While ngrok is running, visit `http://localhost:4040/`:

- See all HTTP requests to your webhooks
- View request/response bodies
- Useful for debugging webhook issues

### 4. Test Plivo Credentials

```bash
python -c "
import plivo
try:
    client = plivo.RestClient('YOUR_PLIVO_AUTH_ID', 'YOUR_PLIVO_AUTH_TOKEN')
    print('✅ Plivo credentials are valid!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

## 🎯 Pre-Demo Checklist

- [ ] OTP updated in `app.py` with your birthdate
- [ ] ngrok running and URL copied
- [ ] BASE_URL updated in `app.py`
- [ ] Flask restarted
- [ ] Test call successfully received
- [ ] OTP authentication works (both wrong and correct)
- [ ] Language selection works (English and Spanish)
- [ ] Audio playback works
- [ ] Call transfer works (or at least initiates)
- [ ] Web UI accessible at `http://localhost:5000`
- [ ] Recording device ready (for demo video)



## 🚀 Production Deployment

### Using Gunicorn (WSGI Server)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t plivo-ivr .
docker run -e PLIVO_AUTH_ID=... -e PLIVO_AUTH_TOKEN=... -p 5000:5000 plivo-ivr
```

### Using Heroku

```bash
# Install Heroku CLI, then:
heroku create your-app-name
git push heroku main
heroku config:set PLIVO_AUTH_ID=...
heroku config:set PLIVO_AUTH_TOKEN=...
heroku config:set BASE_URL=https://your-app-name.herokuapp.com
```

### Using AWS Lambda + API Gateway

1. Package app as ZIP
2. Upload to Lambda
3. Create API Gateway endpoint
4. Set `BASE_URL` to API Gateway URL

---

---

**Submission Package:**
```
plivo-ivr/
├── app.py
├── requirements.txt
├── README.md
├── SETUP_GUIDE.md
├── QUICK_REFERENCE.md
├── TESTING_GUIDE.md (this file)
└── demo_video.mp4
```

