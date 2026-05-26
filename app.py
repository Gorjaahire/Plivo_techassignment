"""
InspireWorks IVR Demo — Plivo Voice API
Flow: Outbound Call → OTP Auth → Language Select → Audio / Transfer
"""

import os
from flask import Flask, request, Response, url_for
import plivo

app = Flask(__name__)

# ─── Configuration ────────────────────────────────────────────────────────────



# Publicly accessible short MP3 for the audio message
AUDIO_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

# Base URL of this server — override with your ngrok/public URL when running
BASE_URL = os.getenv("BASE_URL", "https://unwell-banister-batch.ngrok-free.dev")

client = plivo.RestClient(AUTH_ID, AUTH_TOKEN)

# ─── Helper ───────────────────────────────────────────────────────────────────
def xml_response(xml_str: str) -> Response:
    return Response(xml_str, mimetype="text/xml")


# ─── 1. Trigger Outbound Call ─────────────────────────────────────────────────
@app.route("/make_call", methods=["GET", "POST"])
def make_call():
    """Initiate outbound call. Pass ?to=+91XXXXXXXXXX or set TO_NUMBER env var."""
    to_number = (
        request.values.get("to")
        or os.getenv("TO_NUMBER", "")
    )
    if not to_number:
        return {"error": "Provide ?to=<number> or set TO_NUMBER env var"}, 400

    answer_url = f"{BASE_URL}/ivr/otp"

    resp = client.calls.create(
        from_=PLIVO_NUMBER,
        to_=to_number,
        answer_url=answer_url,
        answer_method="GET",
    )
    return {"status": "call initiated", "request_uuid": resp[1].get("request_uuid", "")}, 200


# ─── 2. OTP Prompt ────────────────────────────────────────────────────────────
@app.route("/ivr/otp", methods=["GET", "POST"])
def ivr_otp():
    """Prompt caller to enter 4-digit OTP."""
    action_url = f"{BASE_URL}/ivr/otp_verify"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <GetDigits action="{action_url}" method="GET" numDigits="4" timeout="10" retries="1">
    <Speak>Welcome to InspireWorks. Please enter your 4 digit O T P to continue.</Speak>
  </GetDigits>
  <Speak>We did not receive any input. Goodbye.</Speak>
  <Hangup/>
</Response>"""
    return xml_response(xml)


# ─── 3. OTP Verification ──────────────────────────────────────────────────────
@app.route("/ivr/otp_verify", methods=["GET", "POST"])
def ivr_otp_verify():
    """Validate OTP; re-prompt on failure."""
    digits = request.values.get("Digits", "")
    otp_url   = f"{BASE_URL}/ivr/otp"
    lang_url  = f"{BASE_URL}/ivr/language"

    if digits == OTP_SECRET:
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>O T P verified. Welcome!</Speak>
  <Redirect method="GET">{lang_url}</Redirect>
</Response>"""
    else:
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>Incorrect O T P. Please try again.</Speak>
  <Redirect method="GET">{otp_url}</Redirect>
</Response>"""
    return xml_response(xml)


# ─── 4. Language Selection (Level 1) ─────────────────────────────────────────
@app.route("/ivr/language", methods=["GET", "POST"])
def ivr_language():
    """Level 1 — choose language."""
    action_url = f"{BASE_URL}/ivr/language_select"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <GetDigits action="{action_url}" method="GET" numDigits="1" timeout="10" retries="1">
    <Speak>Please select your language. Press 1 for English. Press 2 for Spanish.</Speak>
  </GetDigits>
  <Speak>No input received. Goodbye.</Speak>
  <Hangup/>
</Response>"""
    return xml_response(xml)


# ─── 5. Language Handler ──────────────────────────────────────────────────────
@app.route("/ivr/language_select", methods=["GET", "POST"])
def ivr_language_select():
    """Route to Level 2 menu based on language choice."""
    digit = request.values.get("Digits", "")
    lang_url = f"{BASE_URL}/ivr/language"

    if digit == "1":
        menu_url = f"{BASE_URL}/ivr/menu?lang=en"
    elif digit == "2":
        menu_url = f"{BASE_URL}/ivr/menu?lang=es"
    else:
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>Invalid option. Please try again.</Speak>
  <Redirect method="GET">{lang_url}</Redirect>
</Response>"""
        return xml_response(xml)

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Redirect method="GET">{menu_url}</Redirect>
</Response>"""
    return xml_response(xml)


# ─── 6. Action Menu (Level 2) ─────────────────────────────────────────────────
@app.route("/ivr/menu", methods=["GET", "POST"])
def ivr_menu():
    """Level 2 — audio or transfer."""
    lang = request.values.get("lang", "en")
    action_url = f"{BASE_URL}/ivr/menu_select?lang={lang}"

    if lang == "es":
        prompt = (
            "Seleccione una opción. "
            "Presione 1 para escuchar un mensaje de audio. "
            "Presione 2 para hablar con un asociado."
        )
    else:
        prompt = (
            "Please select an option. "
            "Press 1 to hear an audio message. "
            "Press 2 to connect to a live associate."
        )

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <GetDigits action="{action_url}" method="GET" numDigits="1" timeout="10" retries="1">
    <Speak>{prompt}</Speak>
  </GetDigits>
  <Speak>No input received. Goodbye.</Speak>
  <Hangup/>
</Response>"""
    return xml_response(xml)


# ─── 7. Menu Action Handler ───────────────────────────────────────────────────
@app.route("/ivr/menu_select", methods=["GET", "POST"])
def ivr_menu_select():
    """Handle Level 2 selection."""
    digit = request.values.get("Digits", "")
    lang  = request.values.get("lang", "en")
    menu_url = f"{BASE_URL}/ivr/menu?lang={lang}"

    if digit == "1":
        # Play audio message
        if lang == "es":
            pre_msg = "Aquí está su mensaje de audio."
            post_msg = "Gracias por llamar. Hasta luego."
        else:
            pre_msg = "Here is your audio message."
            post_msg = "Thank you for calling InspireWorks. Goodbye."

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>{pre_msg}</Speak>
  <Play>{AUDIO_URL}</Play>
  <Speak>{post_msg}</Speak>
  <Hangup/>
</Response>"""

    elif digit == "2":
        # Transfer to live associate
        if lang == "es":
            transfer_msg = "Conectándole con un asociado. Por favor espere."
        else:
            transfer_msg = "Connecting you to a live associate. Please hold."

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>{transfer_msg}</Speak>
  <Dial callerId="{PLIVO_NUMBER}">
    <Number>{ASSOCIATE_NUMBER}</Number>
  </Dial>
</Response>"""

    else:
        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Speak>Invalid selection. Please try again.</Speak>
  <Redirect method="GET">{menu_url}</Redirect>
</Response>"""

    return xml_response(xml)


# ─── Simple Web UI ────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>InspireWorks IVR Demo</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 500px; margin: 80px auto; padding: 0 20px; }
    h1   { color: #1a1a2e; }
    input, button { padding: 10px 14px; font-size: 16px; margin: 6px 0; width: 100%; box-sizing: border-box; }
    button { background: #e94560; color: white; border: none; border-radius: 4px; cursor: pointer; }
    button:hover { background: #c73652; }
    #result { margin-top: 16px; padding: 12px; background: #f0f4ff; border-radius: 4px; display: none; }
  </style>
</head>
<body>
  <h1>📞 InspireWorks IVR</h1>
  <p>Enter the destination number and click <strong>Make Call</strong> to start the demo.</p>
  <input id="phone" type="text" placeholder="+91XXXXXXXXXX" />
  <button onclick="makeCall()">Make Call</button>
  <div id="result"></div>
  <script>
    async function makeCall() {
      const to = document.getElementById('phone').value.trim();
      if (!to) { alert('Enter a phone number'); return; }
      const res = await fetch('/make_call?to=' + encodeURIComponent(to));
      const data = await res.json();
      const div = document.getElementById('result');
      div.style.display = 'block';
      div.textContent = JSON.stringify(data, null, 2);
    }
  </script>
</body>
</html>"""


if __name__ == "__main__":
    app.run(debug=True, port=5000)
