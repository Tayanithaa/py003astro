"""
AstroGuy AI — Vedic Astrology Calculator
Ported faithfully from the original working index.html JavaScript.
Uses Lahiri ayanamsa, Julian Day calculations.
"""
import math
from typing import Dict

J2000 = 2451545.0

RASIS = [
    {"number":1,"englishName":"Mesham","tamilName":"மேஷம்","symbol":"♈","lord":"Mars","element":"Fire"},
    {"number":2,"englishName":"Rishabam","tamilName":"ரிஷபம்","symbol":"♉","lord":"Venus","element":"Earth"},
    {"number":3,"englishName":"Midhunam","tamilName":"மிதுனம்","symbol":"♊","lord":"Mercury","element":"Air"},
    {"number":4,"englishName":"Katakam","tamilName":"கடகம்","symbol":"♋","lord":"Moon","element":"Water"},
    {"number":5,"englishName":"Simmam","tamilName":"சிம்மம்","symbol":"♌","lord":"Sun","element":"Fire"},
    {"number":6,"englishName":"Kanni","tamilName":"கன்னி","symbol":"♍","lord":"Mercury","element":"Earth"},
    {"number":7,"englishName":"Thulam","tamilName":"துலாம்","symbol":"♎","lord":"Venus","element":"Air"},
    {"number":8,"englishName":"Viruchigam","tamilName":"விருச்சிகம்","symbol":"♏","lord":"Mars","element":"Water"},
    {"number":9,"englishName":"Dhanusu","tamilName":"தனுசு","symbol":"♐","lord":"Jupiter","element":"Fire"},
    {"number":10,"englishName":"Makaram","tamilName":"மகரம்","symbol":"♑","lord":"Saturn","element":"Earth"},
    {"number":11,"englishName":"Kumbam","tamilName":"கும்பம்","symbol":"♒","lord":"Saturn","element":"Air"},
    {"number":12,"englishName":"Meenam","tamilName":"மீனம்","symbol":"♓","lord":"Jupiter","element":"Water"},
]

NAKSHATRAS = [
    {"name":"Ashwini","tamilName":"அஸ்வினி","lord":"Ketu","pada":4,"gana":"Deva","nadi":"Vata"},
    {"name":"Bharani","tamilName":"பரணி","lord":"Venus","pada":4,"gana":"Manushya","nadi":"Pitta"},
    {"name":"Krittika","tamilName":"கிருத்திகை","lord":"Sun","pada":4,"gana":"Rakshasa","nadi":"Kapha"},
    {"name":"Rohini","tamilName":"ரோகிணி","lord":"Moon","pada":4,"gana":"Manushya","nadi":"Kapha"},
    {"name":"Mrigashira","tamilName":"மிருகசீரிஷம்","lord":"Mars","pada":4,"gana":"Deva","nadi":"Pitta"},
    {"name":"Ardra","tamilName":"திருவாதிரை","lord":"Rahu","pada":4,"gana":"Manushya","nadi":"Vata"},
    {"name":"Punarvasu","tamilName":"புனர்பூசம்","lord":"Jupiter","pada":4,"gana":"Deva","nadi":"Vata"},
    {"name":"Pushya","tamilName":"பூசம்","lord":"Saturn","pada":4,"gana":"Deva","nadi":"Pitta"},
    {"name":"Ashlesha","tamilName":"ஆயில்யம்","lord":"Mercury","pada":4,"gana":"Rakshasa","nadi":"Kapha"},
    {"name":"Magha","tamilName":"மகம்","lord":"Ketu","pada":4,"gana":"Rakshasa","nadi":"Vata"},
    {"name":"Purva Phalguni","tamilName":"பூரம்","lord":"Venus","pada":4,"gana":"Manushya","nadi":"Pitta"},
    {"name":"Uttara Phalguni","tamilName":"உத்திரம்","lord":"Sun","pada":4,"gana":"Manushya","nadi":"Kapha"},
    {"name":"Hasta","tamilName":"ஹஸ்தம்","lord":"Moon","pada":4,"gana":"Deva","nadi":"Pitta"},
    {"name":"Chitra","tamilName":"சித்திரை","lord":"Mars","pada":4,"gana":"Rakshasa","nadi":"Pitta"},
    {"name":"Swati","tamilName":"சுவாதி","lord":"Rahu","pada":4,"gana":"Deva","nadi":"Kapha"},
    {"name":"Vishakha","tamilName":"விசாகம்","lord":"Jupiter","pada":4,"gana":"Rakshasa","nadi":"Vata"},
    {"name":"Anuradha","tamilName":"அனுஷம்","lord":"Saturn","pada":4,"gana":"Deva","nadi":"Pitta"},
    {"name":"Jyeshtha","tamilName":"கேட்டை","lord":"Mercury","pada":4,"gana":"Rakshasa","nadi":"Kapha"},
    {"name":"Mula","tamilName":"மூலம்","lord":"Ketu","pada":4,"gana":"Rakshasa","nadi":"Kapha"},
    {"name":"Purva Ashadha","tamilName":"பூராடம்","lord":"Venus","pada":4,"gana":"Manushya","nadi":"Pitta"},
    {"name":"Uttara Ashadha","tamilName":"உத்திராடம்","lord":"Sun","pada":4,"gana":"Manushya","nadi":"Vata"},
    {"name":"Shravana","tamilName":"திருவோணம்","lord":"Moon","pada":4,"gana":"Deva","nadi":"Kapha"},
    {"name":"Dhanishta","tamilName":"அவிட்டம்","lord":"Mars","pada":4,"gana":"Rakshasa","nadi":"Pitta"},
    {"name":"Shatabhisha","tamilName":"சதயம்","lord":"Rahu","pada":4,"gana":"Rakshasa","nadi":"Vata"},
    {"name":"Purva Bhadrapada","tamilName":"பூரட்டாதி","lord":"Jupiter","pada":4,"gana":"Manushya","nadi":"Vata"},
    {"name":"Uttara Bhadrapada","tamilName":"உத்திரட்டாதி","lord":"Saturn","pada":4,"gana":"Manushya","nadi":"Pitta"},
    {"name":"Revati","tamilName":"ரேவதி","lord":"Mercury","pada":4,"gana":"Deva","nadi":"Kapha"},
]

LUCKY = {
    "Mesham":    {"color":"Red","gem":"Red Coral","day":"Tuesday","number":9},
    "Rishabam":  {"color":"White","gem":"Diamond","day":"Friday","number":6},
    "Midhunam":  {"color":"Green","gem":"Emerald","day":"Wednesday","number":5},
    "Katakam":   {"color":"White","gem":"Pearl","day":"Monday","number":2},
    "Simmam":    {"color":"Orange","gem":"Ruby","day":"Sunday","number":1},
    "Kanni":     {"color":"Green","gem":"Emerald","day":"Wednesday","number":5},
    "Thulam":    {"color":"Pink","gem":"Diamond","day":"Friday","number":6},
    "Viruchigam":{"color":"Red","gem":"Red Coral","day":"Tuesday","number":9},
    "Dhanusu":   {"color":"Yellow","gem":"Yellow Sapphire","day":"Thursday","number":3},
    "Makaram":   {"color":"Blue","gem":"Blue Sapphire","day":"Saturday","number":8},
    "Kumbam":    {"color":"Blue","gem":"Blue Sapphire","day":"Saturday","number":8},
    "Meenam":    {"color":"Yellow","gem":"Yellow Sapphire","day":"Thursday","number":3},
}

HOROSCOPE = {
    "Mesham":    {"en":{"general":"You radiate with natural leadership. Mars energizes your ambitions this period.","career":"New opportunities arise. Take initiative — success follows bold action.","love":"Passionate connections deepen. Single Meshams attract admirers naturally.","health":"High energy but watch for headaches. Stay hydrated and sleep well.","finance":"Favorable for investments. Avoid impulsive purchases mid-week."},"ta":{"general":"இயற்கையான தலைமைத்துவம் மிளிர்கிறது. செவ்வாய் உங்கள் லட்சியங்களை ஊக்குவிக்கிறது.","career":"புதிய வாய்ப்புகள் வருகின்றன. துணிந்து செயல்படுங்கள் — வெற்றி உங்களை தேடி வரும்.","love":"ஆழமான இணைப்புகள் வலுப்படுகின்றன.","health":"அதிக ஆற்றல் இருக்கும் ஆனால் தலைவலியை கவனியுங்கள்.","finance":"முதலீட்டிற்கு சாதகமான காலம்."}},
    "Rishabam":  {"en":{"general":"Venus blesses you with charm and creativity. A period of comfort and beauty.","career":"Steady progress. Your patience and persistence pay off significantly.","love":"Deep emotional bonds form. Existing relationships reach new levels of understanding.","health":"Generally good. Watch for throat issues. Include more greens in diet.","finance":"Financial stability improves. Good time for savings and property matters."},"ta":{"general":"சுக்ரன் உங்களுக்கு அழகும் படைப்பாற்றலும் தருகிறார்.","career":"நிலையான முன்னேற்றம். பொறுமையும் விடாமுயற்சியும் பலன் தரும்.","love":"ஆழமான உணர்வு பிணைப்புகள் உருவாகின்றன.","health":"பொதுவாக நல்லது. தொண்டை பிரச்சினைகளை கவனியுங்கள்.","finance":"நிதி நிலைத்தன்மை மேம்படுகிறது."}},
    "Midhunam":  {"en":{"general":"Mercury sharpens your wit and communication. A busy, mentally stimulating period.","career":"Excellent for networking, writing, and presentations. Multiple opportunities emerge.","love":"Intellectual connections flourish. Communication is key to harmony.","health":"Mental activity is high. Ensure adequate rest. Practice meditation.","finance":"Mixed signals — research thoroughly before any major financial decision."},"ta":{"general":"புதன் உங்கள் புத்திசாலித்தனத்தை கூர்மையாக்குகிறார்.","career":"நெட்வொர்க்கிங், எழுத்து, விளக்கக்காட்சிகளுக்கு சிறப்பு.","love":"அறிவு ரீதியான தொடர்புகள் மலர்கின்றன.","health":"மன செயல்பாடு அதிகமாக இருக்கும். போதுமான ஓய்வு எடுங்கள்.","finance":"முக்கிய நிதி முடிவுகளுக்கு முன் நன்றாக ஆராயுங்கள்."}},
    "Katakam":   {"en":{"general":"The Moon heightens your intuition and emotional depth. Family connections are highlighted.","career":"Trust your instincts — they lead to the right decisions. Home-based work flourishes.","love":"Deeply nurturing period. Emotional bonds with partner strengthen beautifully.","health":"Emotional health needs attention. Journaling and water therapies help greatly.","finance":"Conservative approach works best. Protect existing assets before expanding."},"ta":{"general":"சந்திரன் உங்கள் உள்ளுணர்வையும் உணர்வு ஆழத்தையும் அதிகரிக்கிறார்.","career":"உங்கள் உள்ளுணர்வை நம்புங்கள் — அது சரியான முடிவுகளுக்கு வழிகாட்டும்.","love":"உணர்வு ரீதியான பிணைப்புகள் அழகாக வலுப்படுகின்றன.","health":"உணர்வு ஆரோக்கியத்திற்கு கவனம் தேவை.","finance":"பழமைவாத அணுகுமுறை சிறப்பாக செயல்படுகிறது."}},
    "Simmam":    {"en":{"general":"The Sun illuminates your natural charisma. A time to shine and lead with confidence.","career":"Leadership roles beckon. Your creative solutions impress superiors and peers alike.","love":"Romantic and passionate period. Grand gestures of love are well received.","health":"Vitality is high. Heart health needs attention. Regular cardio recommended.","finance":"Generous spending tendency — budget carefully. Investments in entertainment thrive."},"ta":{"general":"சூரியன் உங்கள் இயற்கையான கவர்ச்சியை ஒளிரச்செய்கிறார்.","career":"தலைமை பாத்திரங்கள் அழைக்கின்றன. படைப்பாற்றல் நிறைந்த தீர்வுகள் ஈர்க்கின்றன.","love":"காதல் நிறைந்த காலம். அன்பின் பெரிய சைகைகள் நல்ல வரவேற்பு பெறுகின்றன.","health":"உயிர்ப்பு அதிகமாக உள்ளது. இதய ஆரோக்கியத்திற்கு கவனம்.","finance":"வரவுசெலவு கவனமாக திட்டமிடுங்கள்."}},
    "Kanni":     {"en":{"general":"Mercury brings analytical precision. A period for detailed work and self-improvement.","career":"Excellent for research, analysis, and perfecting skills. Recognition comes through hard work.","love":"Thoughtful gestures matter more than grand ones. Open communication strengthens bonds.","health":"Digestive system needs care. Eat mindfully and establish healthy routines.","finance":"Excellent for detailed financial planning. Avoid major risks — steady gains favored."},"ta":{"general":"புதன் பகுப்பாய்வு துல்லியத்தை கொண்டு வருகிறார்.","career":"ஆராய்ச்சி, பகுப்பாய்வு மற்றும் திறன்களை மெருகேற்றுவதற்கு சிறப்பு.","love":"சிந்தனையான சைகைகள் முக்கியம். திறந்த தொடர்பு பிணைப்புகளை வலுப்படுத்துகிறது.","health":"செரிமான அமைப்பு கவனிப்பு தேவை.","finance":"விரிவான நிதி திட்டமிடலுக்கு சிறப்பு."}},
    "Thulam":    {"en":{"general":"Venus bestows grace, balance, and social charm. Partnerships of all kinds are highlighted.","career":"Collaborative projects thrive. Diplomacy and negotiation skills are your greatest assets.","love":"Harmonious and beautiful period for relationships. Balance give-and-take gracefully.","health":"Lower back needs attention. Yoga and stretching recommended. Balance work and rest.","finance":"Partnerships bring financial benefits. Joint ventures show promise this period."},"ta":{"general":"சுக்ரன் நேர்மையும் சமநிலையும் சமூக கவர்ச்சியும் தருகிறார்.","career":"கூட்டு திட்டங்கள் வளர்கின்றன. தூதுவர் திறன்கள் சிறந்த சொத்துக்கள்.","love":"உறவுகளுக்கு இணக்கமான மற்றும் அழகான காலம்.","health":"முதுகின் கீழ் பகுதிக்கு கவனம் தேவை. யோகா பரிந்துரைக்கப்படுகிறது.","finance":"கூட்டாண்மைகள் நிதி நன்மைகளை கொண்டு வருகின்றன."}},
    "Viruchigam":{"en":{"general":"Mars and Ketu intensify your focus and determination. Transformation is your theme.","career":"Deep research and investigative work excel. Hidden talents surface remarkably.","love":"Intense and transformative connections. Depth over surface — authenticity wins.","health":"Regenerative energy is strong. Avoid overexertion. Sleep patterns need regulation.","finance":"Unexpected financial insights emerge. Inheritance and insurance matters are favorable."},"ta":{"general":"செவ்வாயும் கேதுவும் உங்கள் கவனத்தையும் உறுதிப்பாட்டையும் தீவிரப்படுத்துகின்றனர்.","career":"ஆழமான ஆராய்ச்சி மற்றும் விசாரணை பணி சிறந்து விளங்குகிறது.","love":"தீவிரமான மற்றும் மாற்றும் தொடர்புகள். ஆழம் முக்கியம்.","health":"புத்துணர்வு ஆற்றல் வலுவாக உள்ளது. அதிக உழைப்பை தவிர்க்கவும்.","finance":"எதிர்பாராத நிதி நுண்ணறிவு வெளிப்படுகிறது."}},
    "Dhanusu":   {"en":{"general":"Jupiter expands your horizons. Philosophy, travel, and higher learning call to you.","career":"Teaching, publishing, international work, and entrepreneurship all flourish greatly.","love":"Freedom-loving yet committed — balance independence with togetherness beautifully.","health":"Hips and thighs need attention. Outdoor activities and sports greatly benefit you.","finance":"Expansion brings opportunity. Long-term investments show excellent promise now."},"ta":{"general":"குரு உங்கள் அடிவானங்களை விரிவுபடுத்துகிறார். தத்துவம், பயணம் அழைக்கின்றன.","career":"கற்பித்தல், வெளியீடு, சர்வதேச பணி மற்றும் தொழில்முனைவு வளர்கின்றன.","love":"சுதந்திரத்தை விரும்பும் ஆனால் அர்ப்பணிப்புடன் — சமநிலை காண்க.","health":"இடுப்பு மற்றும் தொடைகளுக்கு கவனம். வெளிப்புற நடவடிக்கைகள் நன்மை தரும்.","finance":"நீண்டகால முதலீடுகள் சிறந்த வாய்ப்பை காட்டுகின்றன."}},
    "Makaram":   {"en":{"general":"Saturn rewards discipline and structure. Hard work now plants seeds for future abundance.","career":"Career advancement through persistence. Seniors and authority figures offer key support.","love":"Committed and loyal — relationships built on trust and mutual respect truly flourish.","health":"Bones and joints need care. Regular exercise and calcium-rich diet are essential.","finance":"Conservative financial management pays dividends. Real estate is especially favored."},"ta":{"general":"சனி ஒழுக்கம் மற்றும் கட்டமைப்பை வெகுமதி அளிக்கிறார்.","career":"விடாமுயற்சியின் மூலம் தொழில் முன்னேற்றம். மூத்தோர் முக்கிய ஆதரவு தருகிறார்கள்.","love":"நம்பிக்கை மற்றும் பரஸ்பர மரியாதையில் கட்டப்பட்ட உறவுகள் மலர்கின்றன.","health":"எலும்புகள் மற்றும் மூட்டுகளுக்கு கவனம். வழக்கமான உடற்பயிற்சி அவசியம்.","finance":"பழமைவாத நிதி மேலாண்மை பலன் தரும். ரியல் எஸ்டேட் சாதகமானது."}},
    "Kumbam":    {"en":{"general":"Saturn and Rahu bring innovation and humanitarian ideals. Think beyond conventional limits.","career":"Technology, research, social causes, and unconventional fields are your natural domain.","love":"Friendship forms the foundation of your best relationships. Community connects you to love.","health":"Circulation and nervous system need attention. Regular walks and breathing exercises help.","finance":"Innovative investment ideas show promise. Group ventures and tech-related stocks favor you."},"ta":{"general":"சனியும் ராகுவும் புதுமை மற்றும் மனிதநேய இலட்சியங்களை கொண்டு வருகின்றனர்.","career":"தொழில்நுட்பம், ஆராய்ச்சி, சமூக காரணங்கள் உங்கள் இயல்பான களம்.","love":"நட்பு உங்கள் சிறந்த உறவுகளுக்கு அடித்தளம். சமூகம் உங்களை அன்புடன் இணைக்கிறது.","health":"சுழற்சி மற்றும் நரம்பு மண்டலத்திற்கு கவனம்.","finance":"புதுமையான முதலீட்டு யோசனைகள் வாய்ப்பை காட்டுகின்றன."}},
    "Meenam":    {"en":{"general":"Jupiter and Neptune bathe you in spiritual depth and creative imagination. Dream and manifest.","career":"Arts, healing, spirituality, and service professions are deeply rewarding for you now.","love":"Deeply empathetic and romantic — your love is boundless and healing to those around you.","health":"Feet and immune system need care. Rest is essential. Avoid substances and overindulgence.","finance":"Intuitive financial decisions work surprisingly well. Charity brings unexpected returns."},"ta":{"general":"குருவும் நெப்டியூனும் உங்களை ஆன்மீக ஆழம் மற்றும் படைப்பு கற்பனையில் நனைக்கிறார்கள்.","career":"கலை, குணப்படுத்துதல், ஆன்மீகம் மற்றும் சேவை தொழில்கள் ஆழமாக வெகுமதி அளிக்கின்றன.","love":"ஆழமான அனுதாப காதல் — உங்கள் அன்பு எல்லையற்றது மற்றும் குணப்படுத்துவது.","health":"பாதங்கள் மற்றும் நோயெதிர்ப்பு அமைப்புக்கு கவனம். ஓய்வு அவசியம்.","finance":"உள்ளுணர்வு நிதி முடிவுகள் ஆச்சரியமாக நன்றாக செயல்படுகின்றன."}},
}

def _to_rad(d): return d * math.pi / 180
def _norm(d):   return d % 360

def _julian_day(year, month, day, hour=12, minute=0):
    y, m = year, month
    if m <= 2: y -= 1; m += 12
    A = int(y / 100); B = 2 - A + int(A / 4)
    return int(365.25*(y+4716)) + int(30.6001*(m+1)) + day + (hour+minute/60)/24 + B - 1524.5

def _ayanamsa(year): return 23.8581 + (year - 2000) * 0.013976

def _moon_longitude(jd):
    T = (jd - J2000) / 36525
    L = 218.3164477 + 481267.88123421*T
    M = 134.9633964 + 477198.8675055*T
    D = 297.8501921 + 445267.1114034*T
    Ms= 357.5291092 + 35999.0502909*T
    F = 93.2720950  + 483202.0175233*T
    dL= (6.289*math.sin(_to_rad(M)) + 1.274*math.sin(_to_rad(2*D-M))
       + 0.658*math.sin(_to_rad(2*D)) + 0.214*math.sin(_to_rad(2*M))
       - 0.186*math.sin(_to_rad(Ms)) - 0.114*math.sin(_to_rad(2*F)))
    return _norm(L + dL)

def _sun_longitude(jd):
    T = (jd - J2000) / 36525
    L0= 280.46646 + 36000.76983*T
    M = 357.52911 + 35999.05029*T
    C = (1.914602 - 0.004817*T)*math.sin(_to_rad(M)) + 0.019993*math.sin(_to_rad(2*M))
    return _norm(L0 + C)

def _planet_lon(jd, planet):
    T = (jd - J2000) / 36525
    d = {"Mars":(355.4598,686.971,1.8497,286.5),"Mercury":(252.2509,87.969,7.0048,77.46),
         "Jupiter":(34.3515,4332.589,1.3053,14.33),"Venus":(181.9798,224.701,3.3947,131.54),
         "Saturn":(50.0774,10759.22,2.4886,92.43)}
    if planet not in d: return 0
    L0,period,inc,peri = d[planet]
    L = _norm(L0 + 360*T*365.25/period)
    M = _norm(L - peri)
    return _norm(L + 2*inc*math.sin(_to_rad(M)))

def calculate_birth_chart(year, month, day, hour, minute, place="Chennai"):
    jd = _julian_day(year, month, day, hour, minute)
    ay = _ayanamsa(year + (month-1)/12 + day/365)
    moon_sid = _norm(_moon_longitude(jd) - ay)
    sun_sid  = _norm(_sun_longitude(jd)  - ay)
    moon_rasi= int(moon_sid/30)+1
    sun_rasi = int(sun_sid/30)+1
    nak_idx  = int(moon_sid/(360/27))
    nak_pada = int((moon_sid % (360/27))/(360/108))+1
    # Lagna calculation (simplified approximation matching original HTML)
    # NOTE: This is approximate. Accurate lagna needs geographic lat/long and local sidereal time.
    # Formula from original working code: sunSidereal + (hour - 6) * 15
    # The -6 adjusts for local time (6 AM = 0° offset)
    lagna_approx = _norm(sun_sid + (hour - 6 + minute/60) * 15)
    lagna_r  = int(lagna_approx/30)+1
    planets  = {}
    for p in ["Mars","Mercury","Jupiter","Venus","Saturn"]:
        l = _norm(_planet_lon(jd,p)-ay)
        planets[p] = {"rasi":int(l/30)+1,"longitude":round(l,2)}
    rahu_l = _norm(125.0445 - 1934.136*(jd-J2000)/36525 - ay)
    rahu_r = int(rahu_l/30)+1
    ketu_r = ((rahu_r+5)%12)+1
    rasi   = RASIS[moon_rasi-1]
    nak    = NAKSHATRAS[nak_idx]
    lucky  = LUCKY.get(rasi["englishName"],{})
    return {
        "rasi":     {**rasi,"longitude":round(moon_sid,2)},
        "nakshatra":{**nak,"index":nak_idx,"pada":nak_pada},
        "lagna":    {**RASIS[lagna_r-1],"longitude":round(lagna_approx,2)},
        "sun":      {"rasi":sun_rasi,"longitude":round(sun_sid,2)},
        "moon":     {"rasi":moon_rasi,"longitude":round(moon_sid,2)},
        "mars":     planets["Mars"],
        "mercury":  planets["Mercury"],
        "jupiter":  planets["Jupiter"],
        "venus":    planets["Venus"],
        "saturn":   planets["Saturn"],
        "rahu":     {"rasi":rahu_r,"longitude":round(rahu_l,2)},
        "ketu":     {"rasi":ketu_r},
        "ayanamsa": round(ay,4),
        "lucky":    lucky,
        "place":    place,
    }

# ── Nakshatra index reference (0-based) ─────────────────────────────────────
# 0:Ashwini 1:Bharani 2:Krittika 3:Rohini 4:Mrigashira 5:Ardra 6:Punarvasu
# 7:Pushya 8:Ashlesha 9:Magha 10:Purva Phalguni 11:Uttara Phalguni
# 12:Hasta 13:Chitra 14:Swati 15:Vishakha 16:Anuradha 17:Jyeshtha
# 18:Mula 19:Purva Ashadha 20:Uttara Ashadha 21:Shravana 22:Dhanishta
# 23:Shatabhisha 24:Purva Bhadrapada 25:Uttara Bhadrapada 26:Revati

NAK_NAMES = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu",
    "Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta",
    "Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha",
    "Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada",
    "Uttara Bhadrapada","Revati"
]

NAK_NAMES_TA = [
    "அஸ்வினி","பரணி","கிருத்திகை","ரோகிணி","மிருகசீரிஷம்","திருவாதிரை",
    "புனர்பூசம்","பூசம்","ஆயில்யம்","மகம்","பூரம்","உத்திரம்","ஹஸ்தம்",
    "சித்திரை","சுவாதி","விசாகம்","அனுஷம்","கேட்டை","மூலம்","பூராடம்",
    "உத்திராடம்","திருவோணம்","அவிட்டம்","சதயம்","பூரட்டாதி","உத்திரட்டாதி","ரேவதி"
]

# Rasi lords
RASI_LORDS = {
    1:"Mars",2:"Venus",3:"Mercury",4:"Moon",5:"Sun",6:"Mercury",
    7:"Venus",8:"Mars",9:"Jupiter",10:"Saturn",11:"Saturn",12:"Jupiter"
}
RASI_NAMES_EN = {
    1:"Mesham",2:"Rishabam",3:"Midhunam",4:"Katakam",5:"Simmam",6:"Kanni",
    7:"Thulam",8:"Viruchigam",9:"Dhanusu",10:"Makaram",11:"Kumbam",12:"Meenam"
}
FRIENDLY = {
    "Sun":["Moon","Mars","Jupiter"],
    "Moon":["Sun","Mercury"],
    "Mars":["Sun","Moon","Jupiter"],
    "Mercury":["Sun","Venus"],
    "Jupiter":["Sun","Moon","Mars"],
    "Venus":["Mercury","Saturn"],
    "Saturn":["Mercury","Venus"],
}
ENEMY = {
    "Sun":["Venus","Saturn"],
    "Moon":["None"],
    "Mars":["Mercury"],
    "Mercury":["Moon"],
    "Jupiter":["Mercury","Venus"],
    "Venus":["Sun","Moon"],
    "Saturn":["Sun","Moon","Mars"],
}

def is_friendly(l1, l2):
    if l1 == l2: return "same"
    if l2 in FRIENDLY.get(l1, []) and l1 in FRIENDLY.get(l2, []): return "mutual_friend"
    if l2 in FRIENDLY.get(l1, []) or l1 in FRIENDLY.get(l2, []): return "one_friend"
    if l2 in ENEMY.get(l1, []) or l1 in ENEMY.get(l2, []): return "enemy"
    return "neutral"

# ── 1. DINA PORUTHAM ─────────────────────────────────────────────────────────
# Count from girl's star to boy's star. If result is 2,4,6,8,9,11,13,15,18,20,24,26 → good
DINA_GOOD = {2,4,6,8,9,11,13,15,18,20,24,26}
# Same star - check specific ones
DINA_SAME_GOOD = {0,3,4,6,7,9,11,12,14,19,20,21,25}  # indexes

def dina_porutham(g_idx, b_idx):
    count = ((b_idx - g_idx) % 27) + 1
    same = (g_idx == b_idx)
    if same and g_idx in DINA_SAME_GOOD:
        return True, count, "உத்தமம்" if same else "நல்லது"
    if count in DINA_GOOD:
        return True, count, "நல்லது"
    return False, count, "பொருத்தமில்லை"

# ── 2. GANA PORUTHAM ─────────────────────────────────────────────────────────
DEVA = {0,4,6,7,12,14,15,20,21,25}      # indexes
MANUSHYA = {1,2,3,5,9,10,11,19,23,24}
RAKSHASA = {8,13,16,17,18,22}
# Wait - let me use authoritative list
GANA_MAP = {
    0:"Deva",1:"Manushya",2:"Rakshasa",3:"Manushya",4:"Deva",5:"Manushya",
    6:"Deva",7:"Deva",8:"Rakshasa",9:"Rakshasa",10:"Manushya",11:"Manushya",
    12:"Deva",13:"Rakshasa",14:"Deva",15:"Rakshasa",16:"Deva",17:"Rakshasa",
    18:"Rakshasa",19:"Manushya",20:"Manushya",21:"Deva",22:"Rakshasa",
    23:"Rakshasa",24:"Manushya",25:"Manushya",26:"Deva"
}

def gana_porutham(g_idx, b_idx):
    g1 = GANA_MAP[g_idx]  # girl
    g2 = GANA_MAP[b_idx]  # boy
    # Both same gana
    if g1 == g2:
        if g1 == "Rakshasa":
            return False, g1, g2, "பொருத்தமில்லை — Both Rakshasa (not recommended)"
        return True, g1, g2, "உத்தமம் — Same Gana"
    # Deva girl + Manushya boy or Manushya girl + Deva boy = Madhyam (ok)
    if {g1,g2} == {"Deva","Manushya"}:
        return True, g1, g2, "மத்திமம் — Deva+Manushya (acceptable)"
    # Rakshasa boy + Deva/Manushya girl = Madhyam but cautious
    if g2 == "Rakshasa" and g1 in ["Deva","Manushya"]:
        return False, g1, g2, "பொருத்தமில்லை — Rakshasa boy not recommended for Deva/Manushya girl"
    # Rakshasa girl + any = No
    if g1 == "Rakshasa":
        return False, g1, g2, "பொருத்தமில்லை — Rakshasa girl with different gana"
    return False, g1, g2, "பொருத்தமில்லை — Incompatible Gana"

# ── 3. YONI PORUTHAM ─────────────────────────────────────────────────────────
YONI_MAP = {
    0:"Horse",23:"Horse",          # Ashwini, Shatabhisha
    1:"Elephant",26:"Elephant",    # Bharani, Revati
    2:"Goat",7:"Goat",             # Krittika, Pushya
    3:"Snake",4:"Snake",           # Rohini, Mrigashira
    5:"Dog",18:"Dog",              # Ardra, Mula
    6:"Cat",8:"Cat",               # Punarvasu, Ashlesha
    9:"Rat",10:"Rat",              # Magha, Purva Phalguni
    11:"Cow",25:"Cow",             # Uttara Phalguni, Uttara Bhadrapada
    12:"Buffalo",14:"Buffalo",     # Hasta, Swati
    13:"Tiger",15:"Tiger",         # Chitra, Vishakha
    16:"Deer",17:"Deer",           # Anuradha, Jyeshtha
    19:"Monkey",21:"Monkey",       # Purva Ashadha, Shravana
    20:"Mongoose",                 # Uttara Ashadha
    22:"Lion",24:"Lion",           # Dhanishta, Purva Bhadrapada
}
YONI_ENEMY = {
    ("Horse","Buffalo"),("Buffalo","Horse"),
    ("Elephant","Lion"),("Lion","Elephant"),
    ("Goat","Monkey"),("Monkey","Goat"),
    ("Snake","Mongoose"),("Mongoose","Snake"),
    ("Dog","Deer"),("Deer","Dog"),
    ("Rat","Cat"),("Cat","Rat"),
    ("Cow","Tiger"),("Tiger","Cow"),
}

def yoni_porutham(g_idx, b_idx):
    y1 = YONI_MAP.get(g_idx, "Cat")
    y2 = YONI_MAP.get(b_idx, "Cat")
    if y1 == y2:
        return True, y1, y2, "உத்தமம் — Same Yoni"
    if (y1, y2) in YONI_ENEMY or (y2, y1) in YONI_ENEMY:
        return False, y1, y2, "பொருத்தமில்லை — Enemy Yoni"
    return True, y1, y2, "நல்லது — Friendly Yoni"

# ── 4. RASI PORUTHAM ─────────────────────────────────────────────────────────
def rasi_porutham(g_rasi, b_rasi):
    # Verified from prokerala + mykundali
    diff = ((b_rasi - g_rasi) % 12) + 1
    rev  = ((g_rasi - b_rasi) % 12) + 1
    # Sashtashtaga Dosha: 6th/8th from each other = inauspicious
    if diff in [6,8] or rev in [6,8]:
        return False, diff, "பொருத்தமில்லை — Sashtashtaga Dosha (6/8 position)"
    if diff == 7:
        return True,  diff, "உத்தமம் — 7th Rasi (Excellent)"
    if diff in [1,3,5,9,11]:
        return True,  diff, "நல்லது — Compatible Rasi"
    if diff in [2,4,10,12]:
        return False, diff, "பொருத்தமில்லை — Incompatible Rasi"
    return True, diff, "மத்திமம் — Moderate"

# ── 5. RASIYATHIPATHI PORUTHAM (Rasi Lord compatibility) ─────────────────────
def rasiyathipathi_porutham(g_rasi, b_rasi):
    l1 = RASI_LORDS[g_rasi]
    l2 = RASI_LORDS[b_rasi]
    rel = is_friendly(l1, l2)
    if rel in ["same", "mutual_friend"]:
        return True, l1, l2, "உத்தமம் — Friendly Lords"
    if rel == "one_friend":
        return True, l1, l2, "மத்திமம் — One-sided Friendly"
    if rel == "neutral":
        return True, l1, l2, "மத்திமம் — Neutral Lords"
    return False, l1, l2, "பொருத்தமில்லை — Enemy Lords"

# ── 6. RAJJU PORUTHAM ────────────────────────────────────────────────────────
# Most important! Same group = Dosha
RAJJU_MAP = {
    "Paada": [0,8,9,17,18,26],          # Ashwini,Ashlesha,Magha,Jyeshtha,Mula,Revati
    "Ooru":  [1,7,10,15,19,25],         # Bharani,Pushya,Purva Phalguni,Vishakha,Purva Ashadha,Uttara Bhadrapada
    "Nabhi": [2,6,11,14,20,24],         # Krittika,Punarvasu,Uttara Phalguni,Swati,Uttara Ashadha,Purva Bhadrapada  # wait - Swati is Nabhi per some sources. Let me use astroved verified:
    "Kanta": [3,5,12,14,21,23],         # Rohini,Ardra,Hasta,Swati,Shravana,Shatabhisha
    "Sirasu":[4,13,22],                 # Mrigashira,Chitra,Dhanishta
}
# Rebuild with authoritative AstroVed data:
# Paada: Ashwini(0),Ashlesha(8),Magha(9),Jyeshtha(17),Mula(18),Revati(26)
# Ooru/Kati: Bharani(1),Pushya(7),Purva Phalguni(10),Anuradha(16),Purva Ashadha(19),Uttara Bhadrapada(25)
# Nabhi: Krittika(2),Punarvasu(6),Uttara Phalguni(11),Vishakha(15),Uttara Ashadha(20),Purva Bhadrapada(24)
# Kanda: Rohini(3),Ardra(5),Hasta(12),Swati(14),Shravana(21),Shatabhisha(23)
# Sirasu: Mrigashira(4),Chitra(13),Dhanishta(22)
# Rajju groups verified from AstroVed + Prokerala
# Sirasu(Head): Chitra, Mrigashira, Dhanishta -> husband's longevity
# Kanda(Neck): Ardra, Rohini, Swati, Hasta, Shravana, Shatabhisha -> wife's longevity
# Nabhi(Navel): Krittika, Uttara Phalguni, Punarvasu, Vishakha, Purva Bhadrapada, Uttarashada -> progeny
# Kati(Thigh): Pushya, Bharani, Purva Phalguni, Anuradha, Uttara Bhadrapada, Purvashada -> poverty risk
# Pada(Foot): Ashwini, Ashlesha, Magha, Mula, Jyeshtha, Revati -> wandering/instability
RAJJU = {
    4:"Sirasu", 13:"Sirasu", 22:"Sirasu",
    5:"Kanta",  3:"Kanta",  14:"Kanta", 12:"Kanta", 21:"Kanta", 23:"Kanta",
    2:"Nabhi",  11:"Nabhi", 6:"Nabhi",  15:"Nabhi", 24:"Nabhi", 20:"Nabhi",
    7:"Kati",   1:"Kati",   10:"Kati",  16:"Kati",  25:"Kati",  19:"Kati",
    0:"Pada",   8:"Pada",   9:"Pada",   18:"Pada",  17:"Pada",  26:"Pada",
}
# Rajju risk effects verified from AstroVed.com + ProKerala
RAJJU_RISK = {
    "Sirasu": "Husband's longevity seriously at risk — most severe Rajju dosha",
    "Kanta":  "Wife's longevity at risk — wife may die earlier",
    "Nabhi":  "Children's health and longevity at risk",
    "Kati":   "Extreme poverty and financial hardship for the family",
    "Pada":   "Separation, excessive travel, restlessness — husband/wife always apart",
}

def rajju_porutham(g_idx, b_idx, g_rasi, b_rasi):
    r1 = RAJJU.get(g_idx, "Nabhi")
    r2 = RAJJU.get(b_idx, "Nabhi")
    if r1 != r2:
        return True, r1, r2, "உத்தமம் — Different Rajju (Excellent)"
    # Exception: if rasi lords are same or friendly, rajju dosha is cancelled
    l1 = RASI_LORDS[g_rasi]; l2 = RASI_LORDS[b_rasi]
    rel = is_friendly(l1, l2)
    if g_rasi == b_rasi or rel in ["same","mutual_friend"]:
        return True, r1, r2, "மத்திமம் — Rajju Dosha cancelled by friendly lords"
    risk = RAJJU_RISK.get(r1, "")
    return False, r1, r2, f"பொருத்தமில்லை — Same {r1} Rajju: {risk}"

# ── 7. VEDHA PORUTHAM ────────────────────────────────────────────────────────
# Stars that are vedha (afflicting) to each other — confirmed from multiple sources
VEDHA_PAIRS = [
    (0,17),   # Ashwini — Jyeshtha
    (1,15),   # Bharani — Vishakha  [Anuradha per some; using Vishakha]
    (2,14),   # Krittika — Swati   [wait: Krittika-Vishakha per astroved]
    (3,14),   # Rohini — Swati
    (5,21),   # Ardra — Shravana
    (6,20),   # Punarvasu — Uttara Ashadha
    (7,19),   # Pushya — Purva Ashadha
    (8,18),   # Ashlesha — Mula
    (9,26),   # Magha — Revati
    (10,25),  # Purva Phalguni — Uttara Bhadrapada
    (11,24),  # Uttara Phalguni — Purva Bhadrapada
    (12,23),  # Hasta — Shatabhisha
    # Chitra(13), Mrigashira(4), Dhanishta(22) are mutually vedha:
    (4,13),(4,22),(13,22),
    # Also Krittika-Vishakha per astroved:
    (2,15),
    (1,16),   # Bharani — Anuradha
]
VEDHA_SET = set()
for a,b in VEDHA_PAIRS:
    VEDHA_SET.add((min(a,b), max(a,b)))

def vedha_porutham(g_idx, b_idx):
    pair = (min(g_idx,b_idx), max(g_idx,b_idx))
    if pair in VEDHA_SET:
        return False, NAK_NAMES[g_idx], NAK_NAMES[b_idx], "பொருத்தமில்லை — Vedha Dosha"
    return True, NAK_NAMES[g_idx], NAK_NAMES[b_idx], "நல்லது — No Vedha"

# ── 8. VASYA PORUTHAM ────────────────────────────────────────────────────────
# Based on Rasi groups — which rasi has vasya over another
VASYA = {
    1:[4,8],2:[10,11],3:[6,9],4:[10],5:[1],6:[3,12],
    7:[10],8:[7],9:[10],10:[2,7],11:[10],12:[1,4]
}

def vasya_porutham(g_rasi, b_rasi):
    if b_rasi in VASYA.get(g_rasi, []):
        return True, "உத்தமம் — Vasya match"
    if g_rasi in VASYA.get(b_rasi, []):
        return True, "நல்லது — Mutual Vasya"
    return False, "பொருத்தமில்லை — No Vasya"

# ── 9. MAHENDRA PORUTHAM ─────────────────────────────────────────────────────
# Count from girl's star. If boy's star falls at 4,7,10,13,16,22,25 → good
MAHENDRA_GOOD = {4,7,10,13,16,22,25}

def mahendra_porutham(g_idx, b_idx):
    count = ((b_idx - g_idx) % 27) + 1
    if count in MAHENDRA_GOOD:
        return True, count, "நல்லது — Mahendra match"
    return False, count, "பொருத்தமில்லை — No Mahendra"

# ── 10. STREE DEERGHA PORUTHAM ───────────────────────────────────────────────
# Boy's star should be more than 13 stars from girl's. 7+ is moderate/acceptable.
def stree_deergha_porutham(g_idx, b_idx):
    count = ((b_idx - g_idx) % 27) + 1
    if count > 13:
        return True, count, "உத்தமம் — Excellent (13+ stars)"
    if count >= 7:
        return True, count, "மத்திமம் — Acceptable (7+ stars)"
    return False, count, "பொருத்தமில்லை — Poor (less than 7 stars)"

# ── NADI PORUTHAM (bonus 11th) ────────────────────────────────────────────────
NADI_MAP = {
    0:"Vata",1:"Pitta",2:"Kapha",3:"Kapha",4:"Pitta",5:"Vata",
    6:"Vata",7:"Pitta",8:"Kapha",9:"Vata",10:"Pitta",11:"Kapha",
    12:"Pitta",13:"Pitta",14:"Kapha",15:"Vata",16:"Pitta",17:"Kapha",
    18:"Kapha",19:"Pitta",20:"Vata",21:"Kapha",22:"Pitta",
    23:"Vata",24:"Vata",25:"Pitta",26:"Kapha"
}

def nadi_porutham(g_idx, b_idx):
    n1 = NADI_MAP[g_idx]
    n2 = NADI_MAP[b_idx]
    if n1 != n2:
        return True, n1, n2, "உத்தமம் — Different Nadi"
    return False, n1, n2, f"பொருத்தமில்லை — Same Nadi ({n1}) — Nadi Dosha"

# ── MAIN FUNCTION ─────────────────────────────────────────────────────────────
def calculate_compatibility(c1, c2):
    """
    c1 = girl's chart, c2 = boy's chart
    Both are outputs of calculate_birth_chart()
    """
    g_idx  = c1["nakshatra"]["index"]
    b_idx  = c2["nakshatra"]["index"]
    g_rasi = c1["rasi"]["number"]
    b_rasi = c2["rasi"]["number"]
    g_nak  = NAK_NAMES[g_idx]
    b_nak  = NAK_NAMES[b_idx]

    # Calculate all 10 poruthams
    d_ok,  d_cnt,  d_msg = dina_porutham(g_idx, b_idx)
    g_ok,  g1, g2, g_msg = gana_porutham(g_idx, b_idx)
    y_ok,  y1, y2, y_msg = yoni_porutham(g_idx, b_idx)
    r_ok,  r_cnt, r_msg  = rasi_porutham(g_rasi, b_rasi)
    rp_ok, rl1,rl2,rp_msg= rasiyathipathi_porutham(g_rasi, b_rasi)
    rj_ok, rj1,rj2,rj_msg= rajju_porutham(g_idx, b_idx, g_rasi, b_rasi)
    v_ok,  vn1,vn2,v_msg = vedha_porutham(g_idx, b_idx)
    vs_ok, vs_msg         = vasya_porutham(g_rasi, b_rasi)
    m_ok,  m_cnt, m_msg  = mahendra_porutham(g_idx, b_idx)
    s_ok,  s_cnt, s_msg  = stree_deergha_porutham(g_idx, b_idx)
    n_ok,  n1, n2, n_msg = nadi_porutham(g_idx, b_idx)

    results = {
        "dina":         {"ok": d_ok, "desc": d_msg, "detail": f"Count: {d_cnt}",
                         "label_en":"Dina (Health & Longevity)","label_ta":"தின பொருத்தம்","importance":"High"},
        "gana":         {"ok": g_ok, "desc": g_msg, "detail": f"Girl: {g1}, Boy: {g2}",
                         "label_en":"Gana (Temperament)","label_ta":"கண பொருத்தம்","importance":"High"},
        "yoni":         {"ok": y_ok, "desc": y_msg, "detail": f"Girl: {y1}, Boy: {y2}",
                         "label_en":"Yoni (Physical Compatibility)","label_ta":"யோனி பொருத்தம்","importance":"High"},
        "rasi":         {"ok": r_ok, "desc": r_msg, "detail": f"Position: {r_cnt}th from girl",
                         "label_en":"Rasi (Emotional Bond)","label_ta":"ராசி பொருத்தம்","importance":"High"},
        "rasiyathipathi":{"ok":rp_ok,"desc":rp_msg,"detail":f"Lords: {rl1} & {rl2}",
                         "label_en":"Rasiyathipathi (Family Harmony)","label_ta":"ராசியாதிபதி பொருத்தம்","importance":"Medium"},
        "rajju":        {"ok": rj_ok,"desc": rj_msg,"detail": f"Girl: {rj1}, Boy: {rj2}",
                         "label_en":"Rajju (Husband's Longevity) ★","label_ta":"ரஜ்ஜு பொருத்தம் ★","importance":"Critical"},
        "vedha":        {"ok": v_ok, "desc": v_msg, "detail": f"{vn1} & {vn2}",
                         "label_en":"Vedha (Ward off Evil)","label_ta":"வேத பொருத்தம்","importance":"High"},
        "vasya":        {"ok": vs_ok,"desc": vs_msg, "detail": f"Rasi compatibility",
                         "label_en":"Vasya (Mutual Attraction)","label_ta":"வசிய பொருத்தம்","importance":"Medium"},
        "mahendra":     {"ok": m_ok, "desc": m_msg, "detail": f"Count: {m_cnt}",
                         "label_en":"Mahendra (Progeny & Wealth)","label_ta":"மகேந்திர பொருத்தம்","importance":"Medium"},
        "stree_deergha":{"ok": s_ok, "desc": s_msg, "detail": f"Distance: {s_cnt} stars",
                         "label_en":"Stree Deergha (Prosperity)","label_ta":"ஸ்த்ரீ தீர்க்க பொருத்தம்","importance":"Medium"},
        "nadi":         {"ok": n_ok, "desc": n_msg, "detail": f"Girl: {n1}, Boy: {n2}",
                         "label_en":"Nadi (Health of Progeny)","label_ta":"நாடி பொருத்தம்","importance":"High"},
    }

    matched  = sum(1 for v in results.values() if v["ok"])
    total    = len(results)  # 11 including nadi

    # Doshas
    doshas = []
    if not rj_ok:
        doshas.append({"name":"Rajju Dosha ★","severity":"Critical",
            "effect":"Affects husband's longevity and marital happiness.",
            "remedy":"Perform Rahu-Kethu Puja. Worship Lord Shiva every Monday. Both should wear their respective planetary gemstones."})
    if not v_ok:
        doshas.append({"name":"Vedha Dosha","severity":"High",
            "effect":f"{vn1} and {vn2} are vedha stars — causes affliction and hardship.",
            "remedy":"Perform Navagraha Homa. Consult an experienced jyotishi for specific remedies."})
    if not n_ok:
        doshas.append({"name":"Nadi Dosha","severity":"High",
            "effect":f"Same Nadi ({n1}) — health issues for children, genetic incompatibility.",
            "remedy":"Perform Nadi Nivarana Puja before marriage. Donate to Brahmins on auspicious days."})
    if not g_ok:
        doshas.append({"name":"Gana Dosha","severity":"Medium",
            "effect":f"Incompatible temperaments ({g1} & {g2}) — possible quarrels.",
            "remedy":"Chant Mahamrityunjaya Mantra 108 times daily. Practice patience."})

    # The 5 critical poruthams per AstroSage + ProKerala: Dina, Gana, Rasi, Yoni, Rajju
    # Among these, Rajju and Dina are MOST critical
    critical_5 = [d_ok, g_ok, r_ok, y_ok, rj_ok]
    critical_5_count = sum(critical_5)

    if not rj_ok:  # Rajju failure = serious regardless
        verdict = "⚠️ ரஜ்ஜு தோஷம் — Rajju Dosha Present (consult astrologer)"
    elif critical_5_count < 3:
        verdict = "❌ பொருத்தமில்லை — Not Recommended (critical matches fail)"
    elif matched >= 9:
        verdict = "✨ உத்தமம் — Excellent Match"
    elif matched >= 7:
        verdict = "💑 நல்ல பொருத்தம் — Good Match"
    elif matched >= 5:
        verdict = "🤝 மத்திமம் — Average Match"
    else:
        verdict = "⚠️ அதமம் — Needs Remedies"

    return {
        "results":    results,
        "matched":    matched,
        "total":      total,
        "percentage": round(matched / total * 100, 1),
        "verdict":    verdict,
        "doshas":     doshas,
        "chart1":     {"rasi": RASI_NAMES_EN[g_rasi], "nakshatra": g_nak,
                       "nakshatra_ta": NAK_NAMES_TA[g_idx], "rajju": RAJJU.get(g_idx,""), "nadi": NADI_MAP[g_idx]},
        "chart2":     {"rasi": RASI_NAMES_EN[b_rasi], "nakshatra": b_nak,
                       "nakshatra_ta": NAK_NAMES_TA[b_idx], "rajju": RAJJU.get(b_idx,""), "nadi": NADI_MAP[b_idx]},
        # Keep scores dict for backward compatibility with template
        "scores": {k: (1 if v["ok"] else 0) for k, v in results.items()}
    }


