"""
AstroGuy AI — Flask Backend (v2, clean rebuild)
================================================
Run: python app.py
"""
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime
import os, json, traceback
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdf_canvas
from io import BytesIO
from flask import send_file
from utils.astrology   import calculate_birth_chart, calculate_compatibility, HOROSCOPE, RASIS
from utils.astrology   import get_current_transits
from utils.panchangam  import get_panchangam
from utils.chatbot     import get_chatbot_response
from utils.birth_chart_svg import generate_birth_chart_svg

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'astroguy-v2-secret')

# ── Database & Auth ──────────────────────────────────────────────────────
try:
    from models import db, bcrypt as bcrypt_ext, User, BirthChart, CompatibilityReport, Feedback
    from flask_login import LoginManager, login_required, current_user
    from flask_migrate import Migrate
    from auth import auth_bp

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///astroguy.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt_ext.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    _AUTH_ENABLED = True
except Exception as _auth_err:
    import sys
    print(f"[WARN] Auth/DB init failed: {_auth_err}", file=sys.stderr)
    _AUTH_ENABLED = False
    # Provide dummy current_user for templates
    class _FakeUser:
        is_authenticated = False
        dark_mode = False
        name = ''
    def _get_fake_user():
        return _FakeUser()
    # Inject into template globals below after app init

TRANSLATIONS = {
    "en":{"heroTitle":"AstroGuy AI","heroSubtitle":"Authentic Vedic Astrology • Ancient Wisdom • Modern Intelligence",
          "formTitle":"Begin Your Cosmic Journey","labelName":"Full Name","labelDob":"Date of Birth",
          "labelTime":"Birth Time","labelPlace":"Birth Place","labelGender":"Gender",
          "btnText":"Generate My Chart","langText":"தமிழ்","loadingText":"Aligning Cosmic Energies..."},
    "ta":{"heroTitle":"ஆஸ்ட்ரோகை AI","heroSubtitle":"நேர்மையான வேத ஜோதிடம் • பழங்கால ஞானம் • நவீன அறிவுநுட்பம்",
          "formTitle":"உங்கள் விண்வெளி பயணத்தைத் தொடங்குங்கள்","labelName":"முழு பெயர்",
          "labelDob":"பிறந்த தேதி","labelTime":"பிறந்த நேரம்","labelPlace":"பிறந்த இடம்",
          "labelGender":"பாலினம்","btnText":"என் ஜாதகத்தை உருவாக்கு",
          "langText":"English","loadingText":"விண்வெளி சக்திகளை சீரமைக்கிறது..."}
}

def lang(): return session.get("language","en")
def t():    return TRANSLATIONS[lang()]
def chart():return session.get("user_chart")
def prof(): return session.get("user_profile")

# Inject current_user + auth_enabled + translations into all templates
@app.context_processor
def inject_globals():
    _lang = session.get("language", "en")
    _trans = TRANSLATIONS[_lang]
    if _AUTH_ENABLED:
        from flask_login import current_user as cu
        return dict(current_user=cu, auth_enabled=True,
                    translations=_trans, language=_lang)
    return dict(current_user=_FakeUser(), auth_enabled=False,
                translations=_trans, language=_lang)

# ── Pages ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", translations=t(), language=lang(),
                           rasis=RASIS)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", translations=t(), language=lang(),
                           user_chart=chart(), profile=prof())

@app.route("/horoscope")
def horoscope():
    uc = chart()
    horoscope_data = None
    if uc:
        horoscope_data = HOROSCOPE.get(uc["rasi"]["englishName"], {})
    return render_template("horoscope.html", translations=t(), language=lang(),
                           user_chart=uc, horoscope_data=horoscope_data,
                           all_horoscope=HOROSCOPE)

@app.route("/compatibility")
def compatibility():
    return render_template("compatibility.html", translations=t(), language=lang())

@app.route("/birthchart")
def birthchart():
    uc  = chart()
    svg = generate_birth_chart_svg(uc) if uc else None
    return render_template("birthchart.html", translations=t(), language=lang(),
                           user_chart=uc, svg_chart=svg)

@app.route("/predictions")
def predictions():
    from datetime import timedelta
    uc = chart(); preds = []
    if uc:
        l = lang()
        MOON_EMOJIS = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘"]
        NAKS_7 = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu"]
        DAY = [
            {"ce":"Peak energy — ideal for important meetings and decisions.","le":"Express your feelings openly. Romance is strong.","he":"Vitality is high. Great day for exercise.","fe":"Good for financial planning and reviewing investments.","ct":"உச்ச ஆற்றல் — முக்கிய சந்திப்புகளுக்கு சிறந்தது.","lt":"காதல் ஆற்றல் வலுவாக உள்ளது.","ht":"உயிர்ப்பு அதிகம். உடற்பயிற்சிக்கு சிறந்த நாள்.","ft":"நிதி திட்டமிடலுக்கு நல்ல நாள்."},
            {"ce":"Focus on completing pending tasks. Avoid new projects.","le":"Listen more than you speak. Understanding deepens bonds.","he":"Rest and recharge. Hydration is key today.","fe":"Hold off on major spending. Review your budget.","ct":"நிலுவையில் உள்ள பணிகளை முடிக்கவும்.","lt":"அதிகமாக கேளுங்கள். புரிதல் பிணைப்பை ஆழப்படுத்துகிறது.","ht":"ஓய்வெடுங்கள். நீரேற்றம் முக்கியம்.","ft":"பெரிய செலவுகளை தவிர்க்கவும்."},
            {"ce":"Excellent for networking and collaboration. New opportunities emerge.","le":"Social energy is high. Great day for dates and outings.","he":"Mental clarity is sharp. Good for yoga and meditation.","fe":"Good day for investments. Consult an advisor.","ct":"நெட்வொர்க்கிங்கிற்கு சிறந்தது. புதிய வாய்ப்புகள் வருகின்றன.","lt":"சமூக ஆற்றல் அதிகம். சந்திப்புகளுக்கு சிறந்த நாள்.","ht":"மன தெளிவு கூர்மையானது. யோகாவிற்கு நல்ல நாள்.","ft":"முதலீடுகளுக்கு நல்ல நாள்."},
            {"ce":"Creative work flourishes. Trust your instincts over analysis.","le":"Deep emotional conversations strengthen your relationship.","he":"Watch for fatigue. Take short breaks throughout the day.","fe":"Avoid speculative investments. Conservative choices safer.","ct":"படைப்பாற்றல் பணி சிறக்கும்.","lt":"ஆழமான உணர்வு உரையாடல்கள் உறவை வலுப்படுத்துகின்றன.","ht":"சோர்வை கவனியுங்கள். சிறிய இடைவெளிகள் எடுங்கள்.","ft":"ஊக முதலீடுகளை தவிர்க்கவும்."},
            {"ce":"Leadership shines. Take initiative on projects you believe in.","le":"Passion and romance are heightened. Plan something special.","he":"Physical energy is excellent. Push yourself a little.","fe":"Strong day for salary negotiations and financial talks.","ct":"தலைமைத்துவம் மிளிர்கிறது.","lt":"ஆர்வமும் காதலும் அதிகரித்திருக்கின்றன.","ht":"உடல் ஆற்றல் சிறந்தது.","ft":"சம்பள பேச்சுவார்த்தைகளுக்கு வலுவான நாள்."},
            {"ce":"Day of reflection. Review progress and set new intentions.","le":"Quiet togetherness is more valuable than grand gestures.","he":"Rest is productive. Sleep early, avoid screens.","fe":"Good day to track expenses and improve savings.","ct":"சிந்தனையின் நாள். முன்னேற்றத்தை மதிப்பீடு செய்யுங்கள்.","lt":"அமைதியான ஒன்றிணைவு இன்று மிகவும் மதிப்புமிக்கது.","ht":"ஓய்வு உற்பத்திகரமானது.","ft":"செலவுகளை கண்காணிக்கவும்."},
            {"ce":"Week ends high. Celebrate small wins and plan ahead.","le":"Joyful energy. Laughter and fun bring you closer.","he":"Excellent wellbeing. Treat yourself to something good.","fe":"Review the week's finances and plan the month ahead.","ct":"வாரம் உயர்வில் முடிகிறது. சிறிய வெற்றிகளை கொண்டாடுங்கள்.","lt":"மகிழ்ச்சியான ஆற்றல். சிரிப்பு உங்களை நெருக்கமாக்குகிறது.","ht":"சிறந்த நலன். ஏதாவது புத்துணர்ச்சிகரமானதை அனுபவியுங்கள்.","ft":"வாரத்தின் நிதியை மதிப்பாய்வு செய்யுங்கள்."},
        ]
        for i in range(7):
            try: dt = datetime.now() + timedelta(days=i)
            except: dt = datetime.now()
            e = DAY[i]
            if l == "ta":
                areas = [("தொழில்","💼",e["ct"]),("காதல்","❤️",e["lt"]),("ஆரோக்கியம்","🏥",e["ht"]),("நிதி","💰",e["ft"])]
            else:
                areas = [("Career","💼",e["ce"]),("Love","❤️",e["le"]),("Health","🏥",e["he"]),("Finance","💰",e["fe"])]
            preds.append({"date":dt.strftime("%A, %d %b"),"moon_emoji":MOON_EMOJIS[i%8],"nakshatra":NAKS_7[i],"areas":areas})
    return render_template("predictions.html", translations=t(), language=lang(),
                           user_chart=uc, predictions=preds)

@app.route("/finance")
def finance():
    uc = chart()
    return render_template("finance.html", translations=t(), language=lang(), user_chart=uc)

@app.route("/remedies")
def remedies():
    return render_template("remedies.html", translations=t(), language=lang(), user_chart=chart())

@app.route("/videos")
def videos():
    vlist = [
        {"id":"iw0yxLP0J5E","title":"Understanding Your Birth Chart" if lang()=="en" else "உங்கள் பிறப்பு சக்கரத்தைப் புரிந்துகொள்ளுதல்","meta":"Basics of Vedic Astrology"},
        {"id":"5Rj9EoX_QJk","title":"Planetary Remedies" if lang()=="en" else "கிரக பரிகாரங்கள்","meta":"Authentic Pariharams"},
        {"id":"Hzv4RVRk4Tg","title":"Marriage Compatibility" if lang()=="en" else "திருமண பொருத்தம்","meta":"10 Porutham Explained"},
    ]
    return render_template("videos.html", translations=t(), language=lang(), videos=vlist)

@app.route("/chat")
def chat():
    return render_template("chat.html", translations=t(), language=lang())

@app.route("/panchangam")
def panchangam():
    pdata = get_panchangam()
    return render_template("panchangam.html", translations=t(), language=lang(), panchangam=pdata)

@app.route("/cosmic-card")
def cosmic_card():
    return render_template("cosmic_card.html", translations=t(), language=lang(),
                           user_chart=chart(), profile=prof())

@app.route("/quiz")
def quiz():
    return render_template("quiz.html", translations=t(), language=lang())

@app.route("/wellness")
def wellness():
    pdata = get_panchangam()
    return render_template("wellness.html", translations=t(), language=lang(),
                           user_chart=chart(), panchangam=pdata)

# ── Help / FAQ ─────────────────────────────────────────────────────────────
@app.route("/help")
@app.route("/faq")
def help_page():
    return render_template("help.html", translations=t(), language=lang())

# ── API ────────────────────────────────────────────────────────────────────
@app.route("/api/calculate-chart", methods=["POST"])
def api_chart():
    try:
        d = request.get_json()
        if not d: return jsonify({"success":False,"error":"No data"}),400
        dob  = d.get("dob",""); time = d.get("time","")
        if not dob or not time: return jsonify({"success":False,"error":"Date/time required"}),400
        y,mo,day = map(int,dob.split("-"))
        h,mi     = map(int,time.split(":"))
        c = calculate_birth_chart(y,mo,day,h,mi,d.get("place","Chennai"))
        session["user_chart"]   = c
        session["user_profile"] = {"name":d.get("name",""),"dob":dob,"time":time,
                                   "place":d.get("place",""),"gender":d.get("gender","")}
        # Save to DB for logged-in users
        if _AUTH_ENABLED:
            from flask_login import current_user as cu
            if cu.is_authenticated:
                try:
                    bc = BirthChart(
                        user_id    = cu.id,
                        full_name  = d.get("name",""),
                        dob        = dob,
                        birth_time = time,
                        birth_place= d.get("place",""),
                        gender     = d.get("gender",""),
                        latitude   = c.get("latitude"),
                        longitude  = c.get("longitude"),
                        timezone   = c.get("timezone",""),
                        chart_json = json.dumps(c)
                    )
                    db.session.add(bc)
                    db.session.commit()
                except Exception:
                    db.session.rollback()
        return jsonify({"success":True,"chart":c})
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"success":False,"error":str(e)}),500

@app.route("/api/transits")
def api_transits():
    try:
        transits = get_current_transits()
        return jsonify({"success": True, "transits": transits, "date": datetime.now().strftime("%d %B %Y")})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    try:
        rating   = int(request.form.get("rating", 5))
        category = request.form.get("category", "general")[:50]
        message  = request.form.get("message", "").strip()[:1000]
        if not message:
            flash("Please enter a message.", "error")
            return redirect(url_for("help_page") + "#feedback")
        if _AUTH_ENABLED:
            from flask_login import current_user as cu
            user_id = cu.id if cu.is_authenticated else None
            try:
                fb = Feedback(rating=rating, category=category, message=message, user_id=user_id)
                db.session.add(fb)
                db.session.commit()
            except Exception:
                db.session.rollback()
        flash("Thank you for your feedback! 🙏", "success")
        return redirect(url_for("help_page"))
    except Exception as e:
        flash(f"Error saving feedback: {str(e)}", "error")
        return redirect(url_for("help_page"))
        
@app.route("/api/download-chart-pdf")
def download_chart_pdf():
    """Generate detailed birth chart PDF with remedies, Dasha table, and planet positions."""
    try:
        uc   = chart()
        pr   = session.get("user_profile")
        if not uc or not pr:
            return jsonify({"success": False, "error": "No chart data. Generate your chart first."}), 400

        buffer = BytesIO()
        c      = pdf_canvas.Canvas(buffer, pagesize=A4)
        W, H   = A4   # 595 x 842 pts

        GOLD  = colors.HexColor("#FFD700")
        WHITE = colors.HexColor("#FFFFFF")
        LIGHT = colors.HexColor("#CCCCCC")
        DARK  = colors.HexColor("#1A1A2E")
        PURPLE= colors.HexColor("#6B46C1")
        GREEN = colors.HexColor("#22C55E")
        RED   = colors.HexColor("#EF4444")

        def hr(y_pos, col=GOLD, w=2):
            c.setStrokeColor(col); c.setLineWidth(w)
            c.line(50, y_pos, W - 50, y_pos)

        def section_title(text, y_pos):
            c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 13)
            c.drawString(50, y_pos, text)
            hr(y_pos - 8, col=colors.HexColor("#333366"), w=1)
            return y_pos - 28

        def row(label, value, y_pos, label_x=50, val_x=200):
            c.setFillColor(LIGHT); c.setFont("Helvetica-Bold", 9)
            c.drawString(label_x, y_pos, label)
            c.setFillColor(WHITE); c.setFont("Helvetica", 9)
            c.drawString(val_x, y_pos, str(value)[:60])
            return y_pos - 18

        # ── Page 1: Cover + Overview ─────────────────────────────────────
        # Background
        c.setFillColor(DARK); c.rect(0, 0, W, H, fill=1, stroke=0)

        # Header bar
        c.setFillColor(PURPLE); c.rect(0, H - 90, W, 90, fill=1, stroke=0)
        c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(W/2, H - 48, "AstroGuy AI")
        c.setFillColor(WHITE); c.setFont("Helvetica", 13)
        c.drawCentredString(W/2, H - 70, "Vedic Birth Chart Report — Authentic Jyotish Analysis")

        hr(H - 100)

        # Personal information
        y = H - 130
        y = section_title("Personal Information", y)
        y = row("Full Name:", pr.get("name", "-"), y)
        y = row("Date of Birth:", pr.get("dob", "-"), y)
        y = row("Birth Time:", pr.get("time", "-"), y)
        y = row("Birth Place:", pr.get("place", "-"), y)
        y = row("Gender:", pr.get("gender", "-"), y)
        y = row("Latitude/Longitude:", f"{uc.get('latitude','')}, {uc.get('longitude','')}", y)
        y = row("Calculation:", uc.get("precision", "approximate"), y)

        y -= 10; hr(y, col=LIGHT, w=0.5); y -= 20

        # Core chart
        y = section_title("Core Vedic Chart", y)
        rasi_en  = uc.get("rasi", {}).get("englishName", "-")
        rasi_ta  = uc.get("rasi", {}).get("tamilName", "-")
        nak_name = uc.get("nakshatra", {}).get("name", "-")
        nak_ta   = uc.get("nakshatra", {}).get("tamilName", "-")
        pada     = uc.get("nakshatra", {}).get("pada", "-")
        nak_lord = uc.get("nakshatra", {}).get("lord", "-")
        lagna_en = uc.get("lagna", {}).get("englishName", "-")
        y = row("Rasi (Moon Sign):", f"{rasi_en} ({rasi_ta})", y)
        y = row("Nakshatra:", f"{nak_name} ({nak_ta}) — Pada {pada}", y)
        y = row("Nakshatra Lord:", nak_lord, y)
        y = row("Lagna (Ascendant):", lagna_en, y)
        y = row("Ayanamsa (Lahiri):", str(uc.get("ayanamsa", "-")), y)

        y -= 10; hr(y, col=LIGHT, w=0.5); y -= 20

        # Planetary positions table
        y = section_title("Planetary Positions", y)
        headers = [("Planet", 50), ("Rasi", 160), ("Longitude", 290), ("Rasi No.", 380)]
        c.setFillColor(PURPLE); c.rect(45, y - 4, W - 90, 18, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 8)
        for h_text, h_x in headers:
            c.drawString(h_x, y + 2, h_text)
        y -= 20

        PLANET_KEYS = [
            ("Sun",     uc.get("sun",     {})),
            ("Moon",    uc.get("moon",    {})),
            ("Mars",    uc.get("mars",    {})),
            ("Mercury", uc.get("mercury", {})),
            ("Jupiter", uc.get("jupiter", {})),
            ("Venus",   uc.get("venus",   {})),
            ("Saturn",  uc.get("saturn",  {})),
            ("Rahu",    uc.get("rahu",    {})),
            ("Ketu",    uc.get("ketu",    {})),
        ]
        RASI_NAMES = {1:"Mesham",2:"Rishabam",3:"Midhunam",4:"Katakam",5:"Simmam",
                      6:"Kanni",7:"Thulam",8:"Viruchigam",9:"Dhanusu",10:"Makaram",
                      11:"Kumbam",12:"Meenam"}
        for i, (pname, pdata) in enumerate(PLANET_KEYS):
            if i % 2 == 0:
                c.setFillColor(colors.HexColor("#0D0D1A"))
            else:
                c.setFillColor(colors.HexColor("#111128"))
            c.rect(45, y - 4, W - 90, 16, fill=1, stroke=0)
            rnum = pdata.get("rasi", 0)
            rname= RASI_NAMES.get(rnum, str(rnum))
            lon  = pdata.get("longitude", "-")
            c.setFillColor(LIGHT); c.setFont("Helvetica-Bold", 8); c.drawString(50,  y, pname)
            c.setFillColor(WHITE); c.setFont("Helvetica",      8); c.drawString(160, y, rname)
            c.drawString(290, y, str(lon))
            c.drawString(380, y, str(rnum))
            y -= 18

        y -= 10; hr(y, col=LIGHT, w=0.5); y -= 20

        # Lucky details
        lucky = uc.get("lucky", {})
        if lucky and y > 120:
            y = section_title("Lucky Elements", y)
            y = row("Lucky Color:", lucky.get("color", "-"), y)
            y = row("Lucky Gemstone:", lucky.get("gem", "-"), y)
            y = row("Lucky Day:", lucky.get("day", "-"), y)
            y = row("Lucky Number:", str(lucky.get("number", "-")), y)

        # Footer page 1
        c.setFillColor(colors.HexColor("#555555")); c.setFont("Helvetica", 7)
        c.drawCentredString(W/2, 30, f"Generated by AstroGuy AI  •  {datetime.now().strftime('%d %B %Y')}  •  Authentic Vedic Astrology")
        c.drawString(W - 80, 30, "Page 1 of 2")
        c.showPage()

        # ── Page 2: Dasha + Remedies ─────────────────────────────────────
        c.setFillColor(DARK); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(PURPLE); c.rect(0, H - 90, W, 90, fill=1, stroke=0)
        c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(W/2, H - 48, "Vimshottari Dasha Periods & Remedies")
        c.setFillColor(WHITE); c.setFont("Helvetica", 11)
        c.drawCentredString(W/2, H - 70, f"{pr.get('name','')}  —  {rasi_en} Rasi, {nak_name} Nakshatra")
        hr(H - 100)

        y = H - 130
        dasha = uc.get("dasha", {})
        if dasha:
            current_d = dasha.get("current", {})
            y = section_title("Vimshottari Dasha Schedule", y)

            # Current dasha highlight
            c.setFillColor(GREEN); c.rect(45, y - 4, W - 90, 20, fill=1, stroke=0)
            c.setFillColor(DARK);  c.setFont("Helvetica-Bold", 9)
            c.drawString(50, y + 2, f"► CURRENT DASHA: {current_d.get('planet','')}  ({current_d.get('start','')} — {current_d.get('end','')})")
            y -= 28

            # Dasha table header
            c.setFillColor(PURPLE); c.rect(45, y - 4, W - 90, 18, fill=1, stroke=0)
            c.setFillColor(WHITE);  c.setFont("Helvetica-Bold", 8)
            c.drawString(50,  y + 2, "Planet")
            c.drawString(160, y + 2, "Start Date")
            c.drawString(270, y + 2, "End Date")
            c.drawString(380, y + 2, "Years")
            c.drawString(440, y + 2, "Status")
            y -= 20

            for i, d_item in enumerate(dasha.get("sequence", [])[:12]):
                bg = colors.HexColor("#162016") if d_item.get("current") else (colors.HexColor("#0D0D1A") if i % 2 == 0 else colors.HexColor("#111128"))
                c.setFillColor(bg); c.rect(45, y - 4, W - 90, 16, fill=1, stroke=0)
                status = "◄ Active Now" if d_item.get("current") else ""
                col    = GREEN if d_item.get("current") else LIGHT
                c.setFillColor(col); c.setFont("Helvetica-Bold" if d_item.get("current") else "Helvetica", 8)
                c.drawString(50,  y, d_item.get("planet", ""))
                c.drawString(160, y, d_item.get("start", ""))
                c.drawString(270, y, d_item.get("end", ""))
                c.drawString(380, y, str(d_item.get("years", "")))
                if status:
                    c.setFillColor(GREEN); c.drawString(440, y, status)
                y -= 18
                if y < 100: break

        y -= 10; hr(y, col=LIGHT, w=0.5); y -= 20

        # Remedies section
        if y > 120:
            y = section_title("Vedic Remedies & Recommendations", y)
            rasi_lord_gem = {
                "Mesham": "Red Coral for Mars — Wear on right ring finger on Tuesday.",
                "Rishabam": "Diamond for Venus — Wear on right ring finger on Friday.",
                "Midhunam": "Emerald for Mercury — Wear on right little finger on Wednesday.",
                "Katakam": "Pearl for Moon — Wear on right ring finger on Monday.",
                "Simmam": "Ruby for Sun — Wear on right ring finger on Sunday.",
                "Kanni": "Emerald for Mercury — Wear on right little finger on Wednesday.",
                "Thulam": "Diamond for Venus — Wear on right ring finger on Friday.",
                "Viruchigam": "Red Coral for Mars — Wear on right ring finger on Tuesday.",
                "Dhanusu": "Yellow Sapphire for Jupiter — Wear on right index finger on Thursday.",
                "Makaram": "Blue Sapphire for Saturn — Wear on right middle finger on Saturday.",
                "Kumbam": "Blue Sapphire for Saturn — Wear on right middle finger on Saturday.",
                "Meenam": "Yellow Sapphire for Jupiter — Wear on right index finger on Thursday.",
            }
            remedy = rasi_lord_gem.get(rasi_en, "Consult your astrologer for personalized remedy.")
            c.setFillColor(LIGHT); c.setFont("Helvetica-Bold", 9); c.drawString(50, y, "💎 Gemstone:")
            c.setFillColor(WHITE); c.setFont("Helvetica", 9); c.drawString(140, y, remedy)
            y -= 20
            c.setFillColor(LIGHT); c.setFont("Helvetica-Bold", 9); c.drawString(50, y, "🕉️ Mantra:")
            c.setFillColor(WHITE); c.setFont("Helvetica", 9)
            c.drawString(140, y, f"Chant the {nak_lord} beeja mantra 108 times daily, especially on {lucky.get('day','Thursday')}.")
            y -= 20
            c.setFillColor(LIGHT); c.setFont("Helvetica-Bold", 9); c.drawString(50, y, "🌿 Color:")
            c.setFillColor(WHITE); c.setFont("Helvetica", 9)
            c.drawString(140, y, f"Wearing {lucky.get('color','Yellow')} strengthens your planetary energy.")
            y -= 20
            c.setFillColor(LIGHT); c.setFont("Helvetica-Bold", 9); c.drawString(50, y, "🔢 Lucky Number:")
            c.setFillColor(WHITE); c.setFont("Helvetica", 9)
            c.drawString(140, y, f"{lucky.get('number','')} — Use this number in important decisions.")

        # Disclaimer
        c.setFillColor(colors.HexColor("#666666")); c.setFont("Helvetica-Oblique", 7)
        c.drawCentredString(W/2, 60, "This report is for educational and spiritual guidance only. Consult a qualified Jyotishi for major life decisions.")
        c.setFillColor(colors.HexColor("#555555")); c.setFont("Helvetica", 7)
        c.drawCentredString(W/2, 45, f"Generated by AstroGuy AI  •  {datetime.now().strftime('%d %B %Y')}  •  astroguy.ai")
        c.drawString(W - 80, 45, "Page 2 of 2")

        c.save()
        buffer.seek(0)
        fname = f"astroguy-{pr.get('name','chart').lower().replace(' ','-')}-{datetime.now().strftime('%Y%m%d')}.pdf"
        return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name=fname)

    except Exception as e:
        app.logger.error(f"PDF error: {traceback.format_exc()}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/calculate-compatibility", methods=["POST"])
def api_compat():
    try:
        d = request.get_json()
        y1,mo1,d1 = map(int,d["dob1"].split("-")); h1,m1 = map(int,d["time1"].split(":"))
        y2,mo2,d2 = map(int,d["dob2"].split("-")); h2,m2 = map(int,d["time2"].split(":"))
        c1 = calculate_birth_chart(y1,mo1,d1,h1,m1,d.get("place1","Chennai"))
        c2 = calculate_birth_chart(y2,mo2,d2,h2,m2,d.get("place2","Chennai"))
        result = calculate_compatibility(c1,c2)
        return jsonify({"success":True,"result":result,"chart1":c1,"chart2":c2})
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({"success":False,"error":str(e)}),500

@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        d   = request.get_json()
        msg = d.get("message","").strip()
        if not msg: return jsonify({"success":False,"error":"Empty"}),400
        l   = d.get("lang") or lang()
        uc  = d.get("userChart") or chart()
        resp= get_chatbot_response(msg, uc, l)
        return jsonify({"success":True,"response":resp})
    except Exception as e:
        return jsonify({"success":False,"error":str(e)}),500

@app.route("/api/toggle-language", methods=["POST"])
def api_lang():
    session["language"] = "ta" if lang()=="en" else "en"
    return jsonify({"success":True,"language":session["language"]})

@app.route("/api/get-user-data")
def api_user():
    return jsonify({"chart":chart(),"profile":prof(),"language":lang()})

@app.route("/api/panchangam")
def api_panchangam():
    return jsonify({"success":True,"data":get_panchangam()})

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html",translations=t(),language=lang(),rasis=RASIS),404

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True,threaded=True)
