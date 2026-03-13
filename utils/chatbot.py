"""
AstroGuy AI — ML-Powered Chatbot (FIXED)
=========================================
Uses trained scikit-learn model (TF-IDF + Naive Bayes)
for intent classification, falls back to rule-based
if model not found.

Run  python train_model.py  once to create the model.
"""

import os
import re
import pickle
import random
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# ── Model path ─────────────────────────────────────────────────────────────
_DIR        = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_DIR, 'chatbot_model.pkl')

_model_data   = None
_model_loaded = False


# ── Preprocessing (must match train_model.py) ──────────────────────────────
def _preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return ' '.join(t for t in text.split() if len(t) > 1)


# ── Load model once ────────────────────────────────────────────────────────
def _load():
    global _model_data, _model_loaded
    if _model_loaded:
        return _model_data is not None
    try:
        if not os.path.exists(_MODEL_PATH):
            logger.warning("chatbot_model.pkl not found — run train_model.py")
            _model_loaded = True
            return False
        with open(_MODEL_PATH, 'rb') as f:
            _model_data = pickle.load(f)
        _model_loaded = True
        acc  = _model_data.get('accuracy', 0) * 100
        tags = len(_model_data.get('intent_tags', []))
        logger.info(f"ML model loaded — {tags} intents, {acc:.1f}% accuracy")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        _model_loaded = True
        return False


# ── Fallback rule-based responses (clean UTF-8) ────────────────────────────
_FALLBACK = {
    "en": [
        "I can help with your Rasi, Nakshatra, birth chart, career, love, health, finance, compatibility, planets, doshas, and remedies. What would you like to know?",
        "Try asking about your horoscope, compatibility matching, planetary guidance, or Vedic remedies!"
    ],
    "ta": [
        "உங்கள் ராசி, நட்சத்திரம், ஜாதகம், தொழில், காதல், ஆரோக்கியம், நிதி, பொருத்தம் பற்றி கேட்கலாம்!",
        "ஜோதிட வழிகாட்டுதலுக்கு நான் இங்கே இருக்கிறேன். என்ன அறிய விரும்புகிறீர்கள்?"
    ]
}

_GREETINGS = {
    "en": [
        "🙏 Vanakkam! I'm AstroGuy AI, your Vedic astrology assistant. Ask me about your Rasi, Nakshatra, compatibility, career, love, or remedies!",
        "🌟 Hello! Welcome to AstroGuy. How can I guide you through the cosmos today?"
    ],
    "ta": [
        "🙏 வணக்கம்! நான் ஆஸ்ட்ரோகை AI. உங்கள் ராசி, நட்சத்திரம், திருமண பொருத்தம் பற்றி கேட்கலாம்!",
        "🌟 வரவேற்கிறோம்! இன்று உங்களுக்கு எப்படி உதவலாம்?"
    ]
}

_GOODBYE = {
    "en": [
        "🙏 Vanakkam! May the stars guide your path. Come back anytime! ⭐",
        "🌟 Thank you for consulting AstroGuy AI. May all planets be favorable! 🪐"
    ],
    "ta": [
        "🙏 நன்றி! நட்சத்திரங்கள் உங்கள் பாதையை வழிநடத்தட்டும். மீண்டும் வாருங்கள்! ⭐",
        "🌟 AstroGuy AI-ஐ ஆலோசித்ததற்கு நன்றி. அனைத்து கிரகங்களும் சாதகமாக இருக்கட்டும்! 🪐"
    ]
}


# ── Personalized responses when user chart exists ─────────────────────────
def _personalized(intent: str, lang: str, chart: Dict) -> Optional[str]:
    """Return a chart-specific response for key intents."""
    # Support both key formats (english_name from calculator, or englishName)
    rasi_en = (chart.get('rasi') or {}).get('english_name') or \
              (chart.get('rasi') or {}).get('englishName', '')
    rasi_ta = (chart.get('rasi') or {}).get('tamil_name') or \
              (chart.get('rasi') or {}).get('tamilName', '')
    nak_en  = (chart.get('nakshatra') or {}).get('name', '')
    nak_ta  = (chart.get('nakshatra') or {}).get('tamil_name') or \
              (chart.get('nakshatra') or {}).get('tamilName', '')
    pada    = (chart.get('nakshatra') or {}).get('pada', '')
    lord    = (chart.get('nakshatra') or {}).get('lord', '')
    lagna   = (chart.get('lagna') or {}).get('name', '')

    rasi = rasi_ta if lang == 'ta' else rasi_en
    nak  = nak_ta  if lang == 'ta' else nak_en

    if intent == 'birth_chart':
        if lang == 'ta':
            return (f"📊 உங்கள் ஜாதக விவரங்கள்:\n"
                    f"🌙 ராசி: {rasi_ta} | ⭐ நட்சத்திரம்: {nak_ta} (பாதம் {pada})\n"
                    f"🪐 நட்சத்திர அதிபதி: {lord} | லக்னம்: {lagna}\n"
                    f"Birth Chart பக்கத்தில் முழு விவரங்கள் காணலாம்!")
        return (f"📊 Your Birth Chart:\n"
                f"🌙 Rasi: {rasi_en} | ⭐ Nakshatra: {nak_en} Pada {pada}\n"
                f"🪐 Nakshatra Lord: {lord} | Lagna: {lagna}\n"
                f"Visit the Birth Chart page for your full detailed chart!")

    if intent == 'rasi_info':
        if lang == 'ta':
            return f"🌙 உங்கள் ராசி **{rasi_ta}**! Horoscope பக்கத்தில் விரிவான பலன்களைக் காணலாம்."
        return f"🌙 Your Rasi is **{rasi_en}**! Visit the Horoscope page for detailed predictions."

    if intent == 'nakshatra_info':
        if lang == 'ta':
            return f"⭐ உங்கள் நட்சத்திரம் **{nak_ta}** (பாதம் {pada}), அதிபதி {lord}."
        return f"⭐ Your Nakshatra is **{nak_en}** (Pada {pada}), ruled by {lord}."

    if intent == 'career_advice':
        if lang == 'ta':
            return f"💼 {rasi_ta} ராசியினர் தொழில்: நட்சத்திர அதிபதி {lord} உங்கள் தொழில் திசையை வழிநடத்துகிறார். Predictions பக்கத்தில் விரிவான பலன்கள் காணலாம்!"
        return f"💼 Career for {rasi_en}: Your Nakshatra lord {lord} guides your professional path. See Predictions page for detailed career forecasts!"

    return None   # no personalization for this intent


# ── Main response function ─────────────────────────────────────────────────
def get_chatbot_response(message: str,
                         user_chart: Optional[Dict] = None,
                         language: str = "en") -> str:
    """
    Returns a chatbot response string.
    Called by Flask /api/chat route in app.py.
    """
    if not message or not message.strip():
        return random.choice(_FALLBACK[language])

    msg = message.strip()

    # ── Try ML model first ─────────────────────────────────────────────
    if _load() and _model_data:
        try:
            pipeline  = _model_data['pipeline']
            responses = _model_data['responses']

            processed  = _preprocess(msg)
            intent     = pipeline.predict([processed])[0]
            probs      = pipeline.predict_proba([processed])[0]
            confidence = float(max(probs))

            print(f"[CHATBOT] Message: '{msg}' | Intent: {intent} | Confidence: {confidence:.1%}")

            # Low confidence → fallback
            if confidence < 0.08:
                print(f"[CHATBOT] Low confidence, using fallback")
                return random.choice(_FALLBACK[language])

            # Special intents first
            if intent == 'greeting':
                return random.choice(_GREETINGS[language])
            if intent == 'goodbye':
                return random.choice(_GOODBYE[language])
            
            # Personalize if chart available
            if user_chart:
                personal = _personalized(intent, language, user_chart)
                if personal:
                    print(f"[CHATBOT] Using personalized response")
                    return personal

            # Return dataset response
            if intent in responses:
                response = random.choice(responses[intent])
                print(f"[CHATBOT] Using dataset response for intent '{intent}'")
                return response
            else:
                print(f"[CHATBOT] Intent '{intent}' not found in responses")
                return random.choice(_FALLBACK[language])

        except Exception as e:
            print(f"[CHATBOT] ML error: {e}")
            logger.error(f"ML prediction error: {e}")
            # Fall through to rule-based

    # ── Rule-based fallback ────────────────────────────────────────────
    print(f"[CHATBOT] Using rule-based fallback")
    return _rule_based(msg, user_chart, language)


def _rule_based(msg: str, chart: Optional[Dict], lang: str) -> str:
    """Simple keyword fallback if ML model unavailable."""
    m = msg.lower()

    greeting_words = ['hi','hello','hey','vanakkam','namaste','வணக்கம்']
    if any(w in m for w in greeting_words):
        return random.choice(_GREETINGS[lang])

    bye_words = ['bye','goodbye','thanks','thank you','நன்றி','போகிறேன்']
    if any(w in m for w in bye_words):
        return random.choice(_GOODBYE[lang])

    planet_map = {
        'sun':'Sun','surya':'Sun','moon':'Moon','chandra':'Moon',
        'mars':'Mars','sevvai':'Mars','mercury':'Mercury','budhan':'Mercury',
        'jupiter':'Jupiter','guru':'Jupiter','venus':'Venus','sukran':'Venus',
        'saturn':'Saturn','sani':'Saturn','rahu':'Rahu','ketu':'Ketu'
    }
    planet_info = {
        'Sun':     {'en':"☀️ The Sun represents soul, ego, authority, and vitality. A strong Sun gives leadership and recognition.",'ta':"☀️ சூரியன் ஆன்மா, அகந்தை, அதிகாரம் மற்றும் உயிர்ப்பைக் குறிக்கிறது."},
        'Moon':    {'en':"🌙 The Moon represents mind, emotions, mother, and intuition. A strong Moon gives emotional stability.",'ta':"🌙 சந்திரன் மனம், உணர்வுகள், தாய் மற்றும் உள்ளுணர்வைக் குறிக்கிறது."},
        'Mars':    {'en':"🔴 Mars represents energy, courage, siblings, and property. A strong Mars gives determination.",'ta':"🔴 செவ்வாய் சக்தி, துணிச்சல், சகோதரர்கள் மற்றும் சொத்தைக் குறிக்கிறது."},
        'Mercury': {'en':"💚 Mercury represents intelligence, communication, and business. A strong Mercury gives sharp intellect.",'ta':"💚 புதன் அறிவு, தகவல்தொடர்பு மற்றும் வணிகத்தைக் குறிக்கிறது."},
        'Jupiter': {'en':"🟡 Jupiter represents wisdom, wealth, children, and spirituality. A strong Jupiter brings prosperity.",'ta':"🟡 குரு ஞானம், செல்வம், குழந்தைகள் மற்றும் ஆன்மீகத்தைக் குறிக்கிறது."},
        'Venus':   {'en':"💗 Venus represents love, beauty, luxury, and arts. A strong Venus brings charm and comfort.",'ta':"💗 சுக்ரன் காதல், அழகு, ஆடம்பரம் மற்றும் கலைகளைக் குறிக்கிறது."},
        'Saturn':  {'en':"🔵 Saturn represents karma, discipline, and longevity. A strong Saturn builds long-term success.",'ta':"🔵 சனி கர்மா, கட்டுப்பாடு மற்றும் ஆயுளைக் குறிக்கிறது."},
        'Rahu':    {'en':"🟣 Rahu represents obsession, foreign matters, and sudden events. It brings both sudden gains and losses.",'ta':"🟣 ராகு பற்றார்வம், வெளிநாட்டு விஷயங்கள் மற்றும் திடீர் நிகழ்வுகளைக் குறிக்கிறது."},
        'Ketu':    {'en':"⚫ Ketu represents spirituality, detachment, and past-life karma. It brings spiritual growth.",'ta':"⚫ கேது ஆன்மீகம், பற்றறுத்தல் மற்றும் முன்பிறவி கர்மாவைக் குறிக்கிறது."},
    }
    for kw, planet in planet_map.items():
        if kw in m:
            return planet_info[planet][lang]

    if any(w in m for w in ['dasha','mahadasha','dashai','தசை','மகாதசை']):
        return _dasha_response(chart, lang)

    if any(w in m for w in ['transit','gochar','கோசாரம்','current planet']):
        return _transit_response(lang)

    if any(w in m for w in ['career','job','work','தொழில்','வேலை']):
        if lang == 'ta':
            return "💼 தொழில் வெற்றிக்கு: உங்கள் 10வது வீட்டு அதிபதியை வழிபடுங்கள். வியாழக்கிழமைகளில் குருவை வழிபடுங்கள்." + _suggest_followup('career', lang)
        return "💼 For career success: Worship your 10th house lord. Thursday worship of Jupiter is highly beneficial." + _suggest_followup('career', lang)

    if any(w in m for w in ['love','marriage','relationship','காதல்','திருமணம்']):
        if lang == 'ta':
            return "💑 திருமண பொருத்தம் பார்க்க Compatibility பக்கத்தில் இரு பேரின் விவரங்களை உள்ளிடவும்." + _suggest_followup('love', lang)
        return "💑 Use the Compatibility page to check your Ashtakoota matching score! Enter both birth details for a full analysis." + _suggest_followup('love', lang)

    if any(w in m for w in ['remedy','pariharam','பரிகாரம்','gemstone','gem','ratna']):
        if chart:
            return _remedy_response(chart, lang)
        if lang == 'ta':
            return "🕉️ பரிகாரங்கள்: ரத்தினக் கற்கள், மந்திரம், விரதம், தானம். Remedies பக்கத்தில் முழு விவரங்கள்!"
        return "🕉️ Vedic remedies: gemstones, mantras, fasting, and charity. Visit the Remedies page for complete details!"

    if any(w in m for w in ['compatibility','match','பொருத்தம்','porutham']):
        if lang == 'ta':
            return "💑 அஷ்டகூட பொருத்தம் 8 அம்சங்களை அடிப்படையாகக் கொண்டது. Compatibility பக்கத்தில் செல்லுங்கள்."
        return "💑 Ashtakoota matching checks 8 aspects out of 36 points. Go to the Compatibility page and enter both birth details!"

    if any(w in m for w in ['nakshatra','star','நட்சத்திரம்','natchathiram']):
        if chart:
            return _personalized('nakshatra_info', lang, chart) or random.choice(_FALLBACK[lang])
        if lang == 'ta':
            return "⭐ உங்கள் நட்சத்திரத்தை அறிய, முகப்பில் பிறந்த தேதி உள்ளிடவும்."
        return "⭐ Enter your birth date and time on the home page to discover your Nakshatra!"

    if any(w in m for w in ['rasi','zodiac','ராசி','moon sign']):
        if chart:
            return _personalized('rasi_info', lang, chart) or random.choice(_FALLBACK[lang])
        if lang == 'ta':
            return "🌙 உங்கள் ராசியை அறிய, முகப்பில் பிறந்த தேதி உள்ளிடவும்."
        return "🌙 Enter your birth date and time on the home page to find your Rasi!"

    if any(w in m for w in ['health','wellness','ஆரோக்கியம்','உடல்நலம்']):
        if lang == 'ta':
            return "🏥 ஆரோக்கிய குறிப்புகள்: 6வது வீட்டு அதிபதியை பலப்படுத்துங்கள். Wellness பக்கத்தில் தினசரி ஆரோக்கிய குறிப்புகள் காணலாம்."
        return "🏥 Health tips: Strengthen your 6th house lord and maintain daily routines. Visit the Wellness page for personalized health guidance!"

    if any(w in m for w in ['finance','money','wealth','நிதி','பணம்','செல்வம்']):
        if lang == 'ta':
            return "💰 நிதி வழிகாட்டுதல்: அதிர்ஷ்ட கல் அணிவது, 11வது வீட்டு அதிபதியை வழிபடுவது உதவும். Finance பக்கத்தில் விரிவான ஜோதிட நிதி ஆலோசனை."
        return "💰 Financial guidance: Wearing your lucky gemstone and worshipping the 11th house lord helps. Visit the Finance page for detailed Vedic advice!"

    return random.choice(_FALLBACK[lang])


def _dasha_response(chart: Optional[Dict], lang: str) -> str:
    """Return personalized dasha information."""
    if not chart:
        if lang == 'ta':
            return "🪐 தசை கணக்கீட்டை பார்க்க, முகப்பில் பிறந்த விவரங்களை உள்ளிடவும்."
        return "🪐 Enter your birth details on the home page to see your Vimshottari Dasha periods!"

    dasha = chart.get("dasha", {})
    if not dasha:
        if lang == 'ta':
            return "🪐 தசை விவரங்கள் கிடைக்கவில்லை. ஜாதகம் மீண்டும் கணக்கிடவும்."
        return "🪐 Dasha details not available. Please recalculate your chart."

    current = dasha.get("current", {})
    planet  = current.get("planet", "")
    end     = current.get("end", "")

    DASHA_EFFECTS = {
        "Sun":     {"en": "Authority, leadership, government connections, father's health", "ta": "அதிகாரம், தலைமைத்துவம், அரசு தொடர்பு"},
        "Moon":    {"en": "Emotional changes, travel, mother's wellbeing, intuition heightens", "ta": "உணர்வு மாற்றங்கள், பயணம், தாயின் நலன்"},
        "Mars":    {"en": "Energy, property matters, siblings, sudden actions and courage", "ta": "ஆற்றல், சொத்து விஷயங்கள், திடீர் செயல்கள்"},
        "Mercury": {"en": "Business, education, communication, short journeys thrive", "ta": "வணிகம், கல்வி, தகவல்தொடர்பு சிறக்கும்"},
        "Jupiter": {"en": "Wisdom, expansion, children, spiritual growth, prosperity", "ta": "ஞானம், வளர்ச்சி, குழந்தைகள், செழிப்பு"},
        "Venus":   {"en": "Love, luxury, arts, comfort, marriage prospects brighten", "ta": "காதல், ஆடம்பரம், கலை, திருமண வாய்ப்பு"},
        "Saturn":  {"en": "Hard work, karmic lessons, discipline, slow but steady gains", "ta": "கடின உழைப்பு, கர்ம பாடங்கள், நிலையான முன்னேற்றம்"},
        "Rahu":    {"en": "Foreign opportunities, technology, sudden changes, material gains", "ta": "வெளிநாட்டு வாய்ப்பு, தொழில்நுட்பம், திடீர் மாற்றங்கள்"},
        "Ketu":    {"en": "Spirituality, detachment, research, past-life fruition", "ta": "ஆன்மீகம், பற்றறுத்தல், ஆராய்ச்சி, முன்பிறவி பலன்"},
    }

    effect = DASHA_EFFECTS.get(planet, {})
    if lang == 'ta':
        effect_text = effect.get("ta", "")
        return (f"🪐 உங்கள் தற்போதைய மகாதசை: **{planet}**\n"
                f"📅 முடிவு தேதி: {end}\n"
                f"🌟 பலன்கள்: {effect_text}\n"
                f"Birth Chart பக்கத்தில் அனைத்து தசைகளும் காணலாம்!")
    else:
        effect_text = effect.get("en", "")
        return (f"🪐 Your current Mahadasha: **{planet}**\n"
                f"📅 Ends: {end}\n"
                f"🌟 Effects: {effect_text}\n"
                f"Visit your Birth Chart page to see all upcoming Dasha periods!")


def _transit_response(lang: str) -> str:
    """Return current planetary transit summary."""
    try:
        from utils.astrology import get_current_transits
        transits = get_current_transits()
        planets  = transits.get("planets", {})
        lines = []
        for name, data in list(planets.items())[:5]:
            lines.append(f"{name}: {data['rasi_name']} ({data['degree']}°)")
        joined = " | ".join(lines)
        if lang == 'ta':
            return f"🌍 தற்போதைய கோசாரம் ({transits.get('date','')}):\n{joined}"
        return f"🌍 Current Planetary Transits ({transits.get('date','')}):\n{joined}"
    except Exception:
        if lang == 'ta':
            return "🌍 கோசார விவரங்கள் இப்போது கிடைக்கவில்லை."
        return "🌍 Real-time transit details are being calculated. Please try again shortly."


def _remedy_response(chart: Optional[Dict], lang: str) -> str:
    """Return gemstone and remedy suggestions based on Lagna/Moon sign."""
    if not chart:
        return random.choice(_FALLBACK[lang])

    rasi_en  = (chart.get('rasi') or {}).get('englishName', '')
    lord_map = {
        "Mesham": ("Mars", "Red Coral", "செவ்வாய்", "பவளம்"),
        "Rishabam": ("Venus", "Diamond", "சுக்ரன்", "வைரம்"),
        "Midhunam": ("Mercury", "Emerald", "புதன்", "மரகதம்"),
        "Katakam": ("Moon", "Pearl", "சந்திரன்", "முத்து"),
        "Simmam": ("Sun", "Ruby", "சூரியன்", "மாணிக்கம்"),
        "Kanni": ("Mercury", "Emerald", "புதன்", "மரகதம்"),
        "Thulam": ("Venus", "Diamond", "சுக்ரன்", "வைரம்"),
        "Viruchigam": ("Mars", "Red Coral", "செவ்வாய்", "பவளம்"),
        "Dhanusu": ("Jupiter", "Yellow Sapphire", "குரு", "புஷ்பராகம்"),
        "Makaram": ("Saturn", "Blue Sapphire", "சனி", "நீல்கல்"),
        "Kumbam": ("Saturn", "Blue Sapphire", "சனி", "நீல்கல்"),
        "Meenam": ("Jupiter", "Yellow Sapphire", "குரு", "புஷ்பராகம்"),
    }
    info = lord_map.get(rasi_en, ("Jupiter", "Yellow Sapphire", "குரு", "புஷ்பராகம்"))

    if lang == 'ta':
        return (f"💎 உங்கள் ராசி {rasi_en} — ஆதிக்க கிரகம்: {info[2]}\n"
                f"🪨 பரிந்துரைக்கப்பட்ட ரத்தினம்: {info[3]}\n"
                f"🕉️ {info[2]} மந்திரம் தினமும் 108 முறை ஜெபிக்கவும்.\n"
                f"📿 Remedies பக்கத்தில் முழுமையான பரிகாரங்கள் காணலாம்!")
    return (f"💎 Your Rasi {rasi_en} — Ruling planet: {info[0]}\n"
            f"🪨 Recommended gemstone: {info[1]}\n"
            f"🕉️ Chant the {info[0]} mantra 108 times daily.\n"
            f"📿 Visit the Remedies page for complete divine remedies!")


def _suggest_followup(topic: str, lang: str) -> str:
    """Return follow-up question suggestions."""
    suggestions = {
        'career': {
            'en': "\n\n💬 You can also ask: What is my current Dasha? | What gemstone should I wear? | Show me my birth chart",
            'ta': "\n\n💬 இவற்றையும் கேட்கலாம்: என் தசை என்ன? | என் அதிர்ஷ்ட கல் என்ன? | என் ஜாதகம் காட்டு"
        },
        'love': {
            'en': "\n\n💬 You can also ask: Check our compatibility | What is my Venus placement? | Remedies for love",
            'ta': "\n\n💬 இவற்றையும் கேட்கலாம்: எங்கள் பொருத்தம் என்ன? | காதல் பரிகாரம் என்ன?"
        }
    }
    s = suggestions.get(topic, {})
    return s.get(lang, s.get('en', ''))


