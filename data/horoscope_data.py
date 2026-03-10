"""AstroGuy AI — Horoscope & Remedy Data"""

HOROSCOPE_DATA = {
    "Mesham": {
        "en": {
            "general": "Dynamic energy surrounds you. Leadership opportunities arise. Trust your instincts.",
            "career": "Excellent period for career growth. New projects and promotions are favored. Mars gives you drive.",
            "love": "Passionate connections deepen. Singles may meet someone through work or social events.",
            "health": "High energy but watch for headaches and stress. Regular exercise and rest are essential.",
            "finance": "Unexpected income possible. Avoid impulsive spending. Invest in long-term assets.",
            "lucky_color": "Red", "lucky_number": 9, "lucky_day": "Tuesday", "lucky_gem": "Red Coral"
        },
        "ta": {
            "general": "உங்களுக்கு சாதகமான காலம். தலைமைத்துவ வாய்ப்புகள் வருகின்றன.",
            "career": "தொழிலில் வளர்ச்சி காணப்படும். புதிய திட்டங்கள் வெற்றி பெறும்.",
            "love": "காதல் வாழ்க்கையில் மகிழ்ச்சி நிலவும். புதிய நட்பு ஏற்படலாம்.",
            "health": "ஆற்றல் அதிகமாக இருக்கும். தலைவலியில் கவனம் தேவை.",
            "finance": "எதிர்பாராத வருமானம் வரலாம். தேவையற்ற செலவுகளை தவிர்க்கவும்.",
            "lucky_color": "சிவப்பு", "lucky_number": 9, "lucky_day": "செவ்வாய்", "lucky_gem": "பவளம்"
        }
    },
    "Rishabam": {
        "en": {
            "general": "Stability and prosperity mark this period. Venus blesses relationships and finances.",
            "career": "Steady progress. Creative fields and finance roles are highlighted. Patience pays off.",
            "love": "Romantic and harmonious. Long-term relationships strengthen. Good for engagements.",
            "health": "Watch throat and neck. Yoga and meditation are beneficial. Maintain regular diet.",
            "finance": "Good for savings and investments. Property deals are favored. Avoid large loans.",
            "lucky_color": "Green", "lucky_number": 6, "lucky_day": "Friday", "lucky_gem": "Diamond"
        },
        "ta": {
            "general": "நிலைத்தன்மையும் வளமையும் நிலவும். வீனஸ் ஆசீர்வதிக்கிறார்.",
            "career": "படிப்படியான முன்னேற்றம். கலை மற்றும் நிதி துறைகளில் வெற்றி.",
            "love": "காதல் வாழ்க்கையில் நல்ல நேரம். திருமண முடிவுகளுக்கு ஏற்றது.",
            "health": "தொண்டை மற்றும் கழுத்தில் கவனம். யோகா பயிற்சி நல்லது.",
            "finance": "சேமிப்பு மற்றும் முதலீட்டிற்கு சாதகமான காலம். சொத்து வாங்குவது நல்லது.",
            "lucky_color": "பச்சை", "lucky_number": 6, "lucky_day": "வெள்ளி", "lucky_gem": "வைரம்"
        }
    },
    "Midhunam": {
        "en": {
            "general": "Communication and intellect shine. Mercury brings clarity and new opportunities.",
            "career": "Excellent for writing, teaching, business. Multiple income sources possible.",
            "love": "Intellectual connections form. Good communication strengthens bonds.",
            "health": "Mind over matter. Breathing exercises help. Watch for nervous tension.",
            "finance": "Business ventures show profit. Diversify investments. Short-term gains likely.",
            "lucky_color": "Yellow", "lucky_number": 5, "lucky_day": "Wednesday", "lucky_gem": "Emerald"
        },
        "ta": {
            "general": "தகவல்தொடர்பு மற்றும் அறிவு சிறப்பாக இருக்கும். புதன் தெளிவு தருகிறார்.",
            "career": "எழுத்து, கல்வி, வணிகத்தில் சிறப்பான காலம். பல வருமான வழிகள்.",
            "love": "அறிவுபூர்வமான தொடர்புகள் உருவாகும். நல்ல தகவல்தொடர்பு உறவை வலுப்படுத்தும்.",
            "health": "மன அமைதி முக்கியம். சுவாச பயிற்சிகள் உதவும். நரம்பு இறுக்கம் குறையும்.",
            "finance": "வணிக முயற்சிகளில் லாபம் வரும். குறுகிய கால ஆதாயங்கள் எதிர்பார்க்கலாம்.",
            "lucky_color": "மஞ்சள்", "lucky_number": 5, "lucky_day": "புதன்", "lucky_gem": "மரகதம்"
        }
    },
    "Katakam": {
        "en": {
            "general": "Emotional depth and intuition guide you. Family matters come to the forefront.",
            "career": "Nurturing professions flourish. Real estate and food industries are highlighted.",
            "love": "Deep emotional bonds. Family approvals likely. Good period for settling down.",
            "health": "Digestive health needs attention. Stay hydrated. Emotional balance is key.",
            "finance": "Home-related investments are favorable. Avoid lending money. Save diligently.",
            "lucky_color": "White", "lucky_number": 2, "lucky_day": "Monday", "lucky_gem": "Pearl"
        },
        "ta": {
            "general": "உணர்வு ஆழமும் உள்ளுணர்வும் வழிகாட்டும். குடும்ப விஷயங்கள் முக்கியமாகும்.",
            "career": "பராமரிப்பு தொழில்கள் சிறக்கும். ரியல் எஸ்டேட் மற்றும் உணவு தொழிலில் வெற்றி.",
            "love": "ஆழமான உணர்வு உறவுகள். குடும்ப அங்கீகாரம் கிடைக்கும். குடியமர்வதற்கு நல்ல காலம்.",
            "health": "செரிமான ஆரோக்கியம் கவனிக்க வேண்டும். நீர் அதிகம் குடிக்கவும்.",
            "finance": "வீட்டு முதலீடுகள் சாதகமாக இருக்கும். சேமிப்பில் கவனம் செலுத்தவும்.",
            "lucky_color": "வெள்ளை", "lucky_number": 2, "lucky_day": "திங்கள்", "lucky_gem": "முத்து"
        }
    },
    "Simmam": {
        "en": {
            "general": "Confidence and charisma are at their peak. Sun empowers you to lead and inspire.",
            "career": "Leadership roles beckon. Politics, management, and entertainment are favored.",
            "love": "Romantic and grand gestures define this period. Loyalty is paramount.",
            "health": "Heart and spine need attention. Stay active. Avoid overexertion.",
            "finance": "Generous but maintain budgets. Investments in gold and luxury goods pay off.",
            "lucky_color": "Gold", "lucky_number": 1, "lucky_day": "Sunday", "lucky_gem": "Ruby"
        },
        "ta": {
            "general": "நம்பிக்கையும் கவர்ச்சியும் உச்சத்தில் உள்ளன. சூரியன் வலிமை தருகிறார்.",
            "career": "தலைமை பாத்திரங்கள் கிடைக்கும். அரசியல், நிர்வாகம், பொழுதுபோக்கு துறைகளில் வெற்றி.",
            "love": "காதல் மற்றும் பெரிய சைகைகள் இந்த காலத்தை வரையறுக்கின்றன. விசுவாசம் முக்கியம்.",
            "health": "இதயம் மற்றும் முதுகுத்தண்டில் கவனம். சுறுசுறுப்பாக இருக்கவும்.",
            "finance": "தங்கம் மற்றும் ஆடம்பர பொருட்களில் முதலீடு பலன் தரும்.",
            "lucky_color": "தங்கம்", "lucky_number": 1, "lucky_day": "ஞாயிறு", "lucky_gem": "மாணிக்கம்"
        }
    },
    "Kanni": {
        "en": {
            "general": "Analytical mind is sharp. Details and precision bring success. Mercury guides you.",
            "career": "Medicine, research, accounting, and editing are highlighted. Perfectionism pays.",
            "love": "Practical approach to relationships. Show love through service and care.",
            "health": "Digestive and nervous system need care. Clean diet and routine are essential.",
            "finance": "Careful planning yields results. Avoid speculative investments. Budget strictly.",
            "lucky_color": "Navy Blue", "lucky_number": 5, "lucky_day": "Wednesday", "lucky_gem": "Emerald"
        },
        "ta": {
            "general": "பகுப்பாய்வு மனம் கூர்மையாக உள்ளது. விவரங்களும் துல்லியமும் வெற்றி தரும்.",
            "career": "மருத்துவம், ஆராய்ச்சி, கணக்கு, திருத்தம் - இவற்றில் சிறப்பான காலம்.",
            "love": "உறவுகளில் நடைமுறை அணுகுமுறை. சேவை மற்றும் அக்கறை மூலம் அன்பு காட்டுங்கள்.",
            "health": "செரிமான மற்றும் நரம்பு மண்டலத்தில் கவனம். சுத்தமான உணவு அவசியம்.",
            "finance": "கவனமான திட்டமிடல் பலன் தரும். ஊக முதலீடுகளை தவிர்க்கவும்.",
            "lucky_color": "நேவி நீலம்", "lucky_number": 5, "lucky_day": "புதன்", "lucky_gem": "மரகதம்"
        }
    },
    "Thulam": {
        "en": {
            "general": "Balance, beauty, and harmony define your path. Venus blesses partnerships.",
            "career": "Law, arts, diplomacy, and fashion are highlighted. Partnerships bring success.",
            "love": "Romantic bliss. Marriages and engagements are very favorable now.",
            "health": "Kidney and lower back need attention. Balance rest and activity.",
            "finance": "Joint ventures and partnerships bring profit. Luxury spending should be moderated.",
            "lucky_color": "Pink", "lucky_number": 6, "lucky_day": "Friday", "lucky_gem": "Diamond"
        },
        "ta": {
            "general": "சமநிலை, அழகு மற்றும் நல்லிணக்கம் உங்கள் பாதையை வரையறுக்கின்றன.",
            "career": "சட்டம், கலை, தூதுவரம் மற்றும் நகை தொழிலில் வெற்றி. கூட்டாண்மை பலன் தரும்.",
            "love": "காதல் மகிழ்ச்சி. திருமணங்கள் மற்றும் நிச்சயதார்த்தங்களுக்கு மிகவும் சாதகமான காலம்.",
            "health": "சிறுநீரகம் மற்றும் கீழ் முதுகில் கவனம். ஓய்வும் செயல்பாடும் சமநிலையில் இருக்கட்டும்.",
            "finance": "கூட்டு முயற்சிகளில் லாபம். ஆடம்பர செலவுகளை மிதப்படுத்தவும்.",
            "lucky_color": "இளஞ்சிவப்பு", "lucky_number": 6, "lucky_day": "வெள்ளி", "lucky_gem": "வைரம்"
        }
    },
    "Viruchigam": {
        "en": {
            "general": "Intense transformation and deep insights. Mars and Ketu make you fearless.",
            "career": "Research, occult, surgery, and investigation are highlighted. Hidden talents emerge.",
            "love": "Intense and transformative relationships. Deep loyalty and passion define bonds.",
            "health": "Reproductive health needs attention. Detox and cleanse regularly.",
            "finance": "Inheritance and joint assets bring gains. Insurance and long-term investments favored.",
            "lucky_color": "Dark Red", "lucky_number": 9, "lucky_day": "Tuesday", "lucky_gem": "Red Coral"
        },
        "ta": {
            "general": "ஆழமான மாற்றம் மற்றும் உள்நுட்பம். செவ்வாய் மற்றும் கேது தைரியம் தருகிறார்கள்.",
            "career": "ஆராய்ச்சி, மறைவான, அறுவை சிகிச்சை மற்றும் விசாரணையில் வெற்றி.",
            "love": "தீவிரமான மற்றும் மாற்றத்தக்க உறவுகள். ஆழமான விசுவாசம் மற்றும் ஆர்வம்.",
            "health": "இனப்பெருக்க ஆரோக்கியம் கவனிக்கவும். நச்சு நீக்கம் அவசியம்.",
            "finance": "மரபுரிமை மற்றும் கூட்டு சொத்துக்கள் ஆதாயம் தரும்.",
            "lucky_color": "அடர் சிவப்பு", "lucky_number": 9, "lucky_day": "செவ்வாய்", "lucky_gem": "பவளம்"
        }
    },
    "Dhanusu": {
        "en": {
            "general": "Expansion, wisdom, and adventure call you. Jupiter opens doors to higher learning.",
            "career": "Teaching, law, philosophy, and international business are highlighted.",
            "love": "Freedom-loving yet committed. Long-distance relationships may develop.",
            "health": "Hips and thighs need attention. Outdoor activities and sports are beneficial.",
            "finance": "Foreign investments and higher education expenses are favored. Expansion pays.",
            "lucky_color": "Purple", "lucky_number": 3, "lucky_day": "Thursday", "lucky_gem": "Yellow Sapphire"
        },
        "ta": {
            "general": "விரிவாக்கம், ஞானம் மற்றும் சாகசம் உங்களை அழைக்கின்றன. குரு கல்வியின் கதவுகளை திறக்கிறார்.",
            "career": "கல்வி, சட்டம், தத்துவம் மற்றும் சர்வதேச வணிகத்தில் சிறப்பான காலம்.",
            "love": "சுதந்திரத்தை நேசிக்கும் ஆனால் உறுதியான உறவுகள். தொலைதூர உறவுகள் உருவாகலாம்.",
            "health": "இடுப்பு மற்றும் தொடைகளில் கவனம். வெளிப்புற செயல்பாடுகள் நல்லது.",
            "finance": "வெளிநாட்டு முதலீடுகள் மற்றும் உயர்கல்வி செலவுகள் சாதகமாக இருக்கும்.",
            "lucky_color": "ஊதா", "lucky_number": 3, "lucky_day": "வியாழன்", "lucky_gem": "மஞ்சள் நீலம்"
        }
    },
    "Makaram": {
        "en": {
            "general": "Discipline, ambition, and hard work define your path. Saturn rewards patience.",
            "career": "Government, engineering, and corporate careers are highlighted. Seniority increases.",
            "love": "Practical and committed approach. Long-lasting bonds built on trust and respect.",
            "health": "Knees and bones need attention. Calcium-rich diet and regular checkups are advised.",
            "finance": "Long-term investments and real estate are very favorable. Avoid shortcuts.",
            "lucky_color": "Black", "lucky_number": 8, "lucky_day": "Saturday", "lucky_gem": "Blue Sapphire"
        },
        "ta": {
            "general": "ஒழுக்கம், லட்சியம் மற்றும் கடின உழைப்பு உங்கள் பாதையை வரையறுக்கின்றன. சனி பொறுமையை வெகுமதிக்கிறார்.",
            "career": "அரசு, பொறியியல் மற்றும் கார்ப்பரேட் வாழ்வில் வெற்றி. மூத்த நிலை அதிகரிக்கும்.",
            "love": "நடைமுறை மற்றும் உறுதியான அணுகுமுறை. நம்பிக்கை மற்றும் மரியாதையில் கட்டப்பட்ட நீடித்த உறவுகள்.",
            "health": "முழங்கால்கள் மற்றும் எலும்புகளில் கவனம். கால்சியம் நிறைந்த உணவு அவசியம்.",
            "finance": "நீண்டகால முதலீடுகள் மற்றும் ரியல் எஸ்டேட் மிகவும் சாதகமாக இருக்கும்.",
            "lucky_color": "கருப்பு", "lucky_number": 8, "lucky_day": "சனி", "lucky_gem": "நீல நீலம்"
        }
    },
    "Kumbam": {
        "en": {
            "general": "Innovation, technology, and humanitarian causes inspire you. Rahu brings sudden changes.",
            "career": "IT, science, social work, and aviation are highlighted. Unconventional paths succeed.",
            "love": "Friendship-based love. Intellectual compatibility is more important than passion.",
            "health": "Circulatory system and ankles need care. Stay warm and hydrated.",
            "finance": "Technology investments and startup ventures bring gains. Network for opportunities.",
            "lucky_color": "Electric Blue", "lucky_number": 8, "lucky_day": "Saturday", "lucky_gem": "Blue Sapphire"
        },
        "ta": {
            "general": "கண்டுபிடிப்பு, தொழில்நுட்பம் மற்றும் மனிதாபிமான காரணங்கள் உங்களை உத்வேகப்படுத்துகின்றன.",
            "career": "IT, அறிவியல், சமூக பணி மற்றும் விமானம் - இவற்றில் வெற்றி. மரபுக்கு மாறான பாதைகள் வெற்றி பெறும்.",
            "love": "நட்பு அடிப்படையிலான காதல். அறிவுப்பூர்வமான இணக்கம் மிக முக்கியம்.",
            "health": "ரத்த ஓட்ட மண்டலம் மற்றும் கணுக்கால்களில் கவனம்.",
            "finance": "தொழில்நுட்ப முதலீடுகள் மற்றும் தொடக்க முயற்சிகள் ஆதாயம் தரும்.",
            "lucky_color": "மின்சார நீலம்", "lucky_number": 8, "lucky_day": "சனி", "lucky_gem": "நீல நீலம்"
        }
    },
    "Meenam": {
        "en": {
            "general": "Spiritual depth, creativity, and compassion flow through you. Jupiter and Venus bless.",
            "career": "Arts, music, spirituality, healing, and marine fields are highlighted.",
            "love": "Dreamy and unconditional love. Spiritual and romantic connections deepen.",
            "health": "Feet and lymphatic system need care. Adequate sleep and meditation are essential.",
            "finance": "Charitable giving brings blessings. Avoid get-rich-quick schemes. Trust intuition.",
            "lucky_color": "Sea Green", "lucky_number": 3, "lucky_day": "Thursday", "lucky_gem": "Yellow Sapphire"
        },
        "ta": {
            "general": "ஆன்மீக ஆழம், படைப்பாற்றல் மற்றும் அனுகம்பம் உங்களில் ஓடுகின்றன.",
            "career": "கலை, இசை, ஆன்மீகம், குணமாக்கல் மற்றும் கடல் சார்ந்த துறைகளில் சிறப்பான காலம்.",
            "love": "கனவு நிறைந்த மற்றும் நிபந்தனையற்ற காதல். ஆன்மீக மற்றும் காதல் தொடர்புகள் ஆழமடையும்.",
            "health": "பாதங்கள் மற்றும் நிணநீர் மண்டலத்தில் கவனம். போதுமான தூக்கம் மற்றும் தியானம் அவசியம்.",
            "finance": "தர்மச்சாலை கொடுப்பனவுகள் ஆசீர்வாதம் தரும். விரைவான செல்வ திட்டங்களை தவிர்க்கவும்.",
            "lucky_color": "கடல் பச்சை", "lucky_number": 3, "lucky_day": "வியாழன்", "lucky_gem": "மஞ்சள் நீலம்"
        }
    }
}

REMEDIES_DATA = {
    "Sun": {
        "mantra": "Om Hraam Hreem Hraum Sah Suryaya Namah",
        "gemstone": "Ruby (Manikya)",
        "day": "Sunday",
        "charity": "Donate wheat, jaggery, or copper on Sundays",
        "puja": "Worship Lord Shiva, chant Gayatri Mantra 108 times at sunrise",
        "color": "#FF8C00",
        "ta": {"mantra":"ஓம் ஹ்ராம் ஹ்ரீம் ஹ்ரௌம் ஸ: சூர்யாய நம:","gemstone":"மாணிக்கம்","day":"ஞாயிறு","charity":"ஞாயிற்றுக்கிழமைகளில் கோதுமை மற்றும் வெல்லம் தானம் செய்யவும்","puja":"சூரிய உதயத்தில் காயத்ரி மந்திரம் 108 முறை சொல்லவும்"}
    },
    "Moon": {
        "mantra": "Om Shraam Shreem Shraum Sah Chandraya Namah",
        "gemstone": "Pearl (Moti)",
        "day": "Monday",
        "charity": "Donate white rice, milk, or silver on Mondays",
        "puja": "Worship Goddess Parvati, offer white flowers",
        "color": "#C0C0FF",
        "ta": {"mantra":"ஓம் ஶ்ராம் ஶ்ரீம் ஶ்ரௌம் ஸ: சந்த்ராய நம:","gemstone":"முத்து","day":"திங்கள்","charity":"திங்கட்கிழமைகளில் வெண்ணெய், பால் அல்லது வெள்ளி தானம் செய்யவும்","puja":"பார்வதி தேவியை வழிபட்டு வெண்மை மலர்கள் படைக்கவும்"}
    },
    "Mars": {
        "mantra": "Om Kraam Kreem Kraum Sah Bhaumaya Namah",
        "gemstone": "Red Coral (Moonga)",
        "day": "Tuesday",
        "charity": "Donate red lentils, copper, or red items on Tuesdays",
        "puja": "Worship Lord Hanuman, chant Hanuman Chalisa",
        "color": "#FF4444",
        "ta": {"mantra":"ஓம் க்ராம் க்ரீம் க்ரௌம் ஸ: பௌமாய நம:","gemstone":"பவளம்","day":"செவ்வாய்","charity":"செவ்வாய்க்கிழமைகளில் சிவப்பு பருப்பு அல்லது தாமிரம் தானம் செய்யவும்","puja":"ஆஞ்சநேயரை வழிபட்டு ஹனுமான் சாலிசா பாடவும்"}
    },
    "Mercury": {
        "mantra": "Om Braam Breem Braum Sah Budhaya Namah",
        "gemstone": "Emerald (Panna)",
        "day": "Wednesday",
        "charity": "Donate green items, moong dal, or books on Wednesdays",
        "puja": "Worship Lord Vishnu, read Vishnu Sahasranama",
        "color": "#44BB44",
        "ta": {"mantra":"ஓம் ப்ராம் ப்ரீம் ப்ரௌம் ஸ: புதாய நம:","gemstone":"மரகதம்","day":"புதன்","charity":"புதன்கிழமைகளில் பசுமை பொருட்கள் அல்லது புத்தகங்கள் தானம் செய்யவும்","puja":"விஷ்ணுவை வழிபட்டு விஷ்ணு சஹஸ்ரநாமம் படிக்கவும்"}
    },
    "Jupiter": {
        "mantra": "Om Graam Greem Graum Sah Gurave Namah",
        "gemstone": "Yellow Sapphire (Pukhraj)",
        "day": "Thursday",
        "charity": "Donate yellow items, turmeric, or gold on Thursdays",
        "puja": "Worship Lord Brihaspati, chant Guru mantra",
        "color": "#FFD700",
        "ta": {"mantra":"ஓம் க்ராம் க்ரீம் க்ரௌம் ஸ: குரவே நம:","gemstone":"மஞ்சள் நீலம்","day":"வியாழன்","charity":"வியாழக்கிழமைகளில் மஞ்சள் பொருட்கள் அல்லது தங்கம் தானம் செய்யவும்","puja":"பிருஹஸ்பதியை வழிபட்டு குரு மந்திரம் சொல்லவும்"}
    },
    "Venus": {
        "mantra": "Om Draam Dreem Draum Sah Shukraya Namah",
        "gemstone": "Diamond (Heera)",
        "day": "Friday",
        "charity": "Donate white items, rice, or silver on Fridays",
        "puja": "Worship Goddess Lakshmi, offer lotus flowers",
        "color": "#FF69B4",
        "ta": {"mantra":"ஓம் த்ராம் த்ரீம் த்ரௌம் ஸ: சுக்ராய நம:","gemstone":"வைரம்","day":"வெள்ளி","charity":"வெள்ளிக்கிழமைகளில் வெண்மை பொருட்கள் அல்லது வெள்ளி தானம் செய்யவும்","puja":"லக்ஷ்மி தேவியை வழிபட்டு தாமரை மலர்கள் படைக்கவும்"}
    },
    "Saturn": {
        "mantra": "Om Praam Preem Praum Sah Shanaischaraya Namah",
        "gemstone": "Blue Sapphire (Neelam)",
        "day": "Saturday",
        "charity": "Donate black sesame, iron, or oil on Saturdays",
        "puja": "Worship Lord Shani, light sesame oil lamp",
        "color": "#8888FF",
        "ta": {"mantra":"ஓம் ப்ராம் ப்ரீம் ப்ரௌம் ஸ: சனைஸ்சராய நம:","gemstone":"நீல நீலம்","day":"சனி","charity":"சனிக்கிழமைகளில் கருப்பு எள், இரும்பு அல்லது எண்ணெய் தானம் செய்யவும்","puja":"சனி பகவானை வழிபட்டு எள் எண்ணெய் விளக்கு ஏற்றவும்"}
    },
    "Rahu": {
        "mantra": "Om Raam Rahave Namah",
        "gemstone": "Hessonite (Gomed)",
        "day": "Saturday",
        "charity": "Donate blue items, coconut, or black til on Saturdays",
        "puja": "Worship Lord Bhairava, visit Rahu temples",
        "color": "#AA44AA",
        "ta": {"mantra":"ஓம் ராம் ராஹவே நம:","gemstone":"கோமேதகம்","day":"சனி","charity":"சனிக்கிழமைகளில் நீல பொருட்கள் அல்லது தேங்காய் தானம் செய்யவும்","puja":"பைரவரை வழிபட்டு ராஹு கோயில்களில் பிரார்த்தனை செய்யவும்"}
    },
    "Ketu": {
        "mantra": "Om Keem Ketave Namah",
        "gemstone": "Cat's Eye (Lehsunia)",
        "day": "Tuesday",
        "charity": "Donate multi-colored blankets, sesame, or iron on Tuesdays",
        "puja": "Worship Lord Ganesha, chant Ganesha mantras",
        "color": "#AA8844",
        "ta": {"mantra":"ஓம் கீம் கேதவே நம:","gemstone":"வைடூரியம்","day":"செவ்வாய்","charity":"செவ்வாய்க்கிழமைகளில் பல நிற போர்வைகள் அல்லது எள் தானம் செய்யவும்","puja":"விநாயகரை வழிபட்டு விநாயக மந்திரங்கள் ஜெபிக்கவும்"}
    }
}
