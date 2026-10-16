import streamlit as st
import streamlit.components.v1 as components
import json
import os
import base64
from datetime import datetime

# ==============================================================================
# 1. PAGE CONFIG & PREMIUM ANIMATED CSS
# ==============================================================================
st.set_page_config(
    page_title="Dyanjyoti Classes",
    page_icon="🪔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Noto+Sans+Devanagari:wght@600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Baloo 2', 'Noto Sans Devanagari', sans-serif !important;
}

/* Hide Streamlit default menu & footer so parents never see code */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

.stApp {
    background: linear-gradient(160deg, #0f172a 0%, #1e1b4b 55%, #311042 100%);
    color: #f8fafc;
}

/* Royal Animated Banner */
.dj-header {
    background: linear-gradient(135deg, #ea580c, #db2777, #4f46e5);
    padding: 16px 18px;
    border-radius: 22px;
    text-align: center;
    color: white;
    box-shadow: 0 10px 28px rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.25);
    margin-bottom: 14px;
    animation: fadeInDown 0.5s ease;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-15px); }
    to { opacity: 1; transform: translateY(0); }
}

.dj-title {
    font-size: 26px;
    font-weight: 900;
    margin: 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.35);
}

.dj-sub {
    font-size: 13px;
    font-weight: 700;
    background: rgba(0,0,0,0.28);
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    margin-top: 4px;
}

/* 3D White Cards */
.dj-card {
    background: rgba(255, 255, 255, 0.96);
    color: #0f172a;
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 6px 0 #cbd5e1, 0 12px 24px rgba(0,0,0,0.25);
    border: 2px solid #e2e8f0;
}

.hw-badge {
    background: #e0e7ff;
    color: #4338ca;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. DATABASE STORAGE IN PYTHON (Saves Homework, Attendance, Students & PIN)
# ==============================================================================
DB_FILE = "dyanjyoti_data.json"

DEFAULT_DB = {
    "teacher_pin": "1234",
    "bilingual": True,
    "voice_speed": 0.82,
    "students": [
        {"name": "आरव (Aarav)", "cls": "Nursery", "stars": 5},
        {"name": "सिया (Siya)", "cls": "LKG / UKG", "stars": 8},
        {"name": "विवान (Vivaan)", "cls": "1st Std SSC", "stars": 10}
    ],
    "attendance": {},
    "homework": [
        {
            "id": "hw_1",
            "date": datetime.now().strftime("%d %b %Y"),
            "cls": "1st Std SSC",
            "title": "मराठी बालभारती व पाढे सराव",
            "desc": "१) 'अ' ते 'ज्ञ' मुळाक्षरे २ वेळा सुंदर अक्षरात वहीत लिहा.\n२) २ आणि ३ चा पाढा अ‍ॅपमधून ऐकून पाठ करा.",
            "file_name": "",
            "file_data": "",
            "file_type": "",
            "link": ""
        }
    ]
}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_DB.copy()

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db = load_db()

if "teacher_unlocked" not in st.session_state:
    st.session_state.teacher_unlocked = False

# ==============================================================================
# 3. HEADER DISPLAY
# ==============================================================================
st.markdown("""
<div class="dj-header">
    <div class="dj-title">🪔 Dyanjyoti Classes 🎓</div>
    <div class="dj-sub">Nursery • LKG • UKG • 1st Std SSC (Maharashtra Board)</div>
</div>
""", unsafe_allow_html=True)

# Top Navigation Tabs
tab_learn, tab_slate, tab_att, tab_hw, tab_settings = st.tabs([
    "📚 सर्व विषय",
    "✏️ पाटी व Quiz",
    "📋 हजेरी (Attendance)",
    "📖 गृहपाठ (Homework)",
    "⚙️ सेटिंग्ज"
])

# ==============================================================================
# TAB 1: INTERACTIVE SUBJECTS + INDIAN ENGLISH & MARATHI VOICE ENGINE
# ==============================================================================
with tab_learn:
    bilingual_flag = "true" if db.get("bilingual", True) else "false"
    v_speed = db.get("voice_speed", 0.82)

    interactive_learning_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Noto+Sans+Devanagari:wght@700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; font-family: 'Baloo 2', 'Noto Sans Devanagari', sans-serif; user-select: none; }}
        body {{ margin: 0; padding: 4px; background: transparent; color: #0f172a; }}
        .ribbon {{ display: flex; gap: 6px; overflow-x: auto; padding-bottom: 8px; }}
        .pill {{
            flex: 0 0 auto; padding: 7px 14px; border-radius: 999px;
            background: rgba(255,255,255,0.16); color: #fff; border: 1px solid rgba(255,255,255,0.3);
            font-weight: 800; font-size: 13px; cursor: pointer;
        }}
        .pill.active {{
            background: linear-gradient(135deg, #fde047, #f59e0b); color: #0f172a;
            box-shadow: 0 4px 12px rgba(245,158,11,0.4);
        }}
        .hero {{
            background: linear-gradient(145deg, #ffffff, #f1f5f9);
            border-radius: 22px; padding: 14px; text-align: center;
            margin: 8px 0 12px; box-shadow: 0 10px 24px rgba(0,0,0,0.25);
            cursor: pointer; border: 2px solid #c7d2fe;
        }}
        .hero-big {{
            font-size: 46px; font-weight: 900; line-height: 1.1;
            background: linear-gradient(135deg, #4f46e5, #db2777);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .hero-title {{ font-size: 18px; font-weight: 800; color: #1e293b; }}
        .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 9px; }}
        .card {{
            background: #fff; border-radius: 18px; padding: 10px 6px; text-align: center;
            box-shadow: 0 5px 0 #cbd5e1, 0 8px 16px rgba(0,0,0,0.18);
            cursor: pointer; transition: transform 0.14s;
        }}
        .card:active {{ transform: translateY(4px) scale(0.95); }}
        .char {{ font-size: 24px; font-weight: 900; }}
        .emo {{ font-size: 28px; margin: 2px 0; }}
        .en {{ font-size: 12.5px; font-weight: 800; color: #1e293b; }}
        .mr {{ font-size: 11.5px; font-weight: 700; color: #4f46e5; }}
        .bk-strip {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 7px; margin-bottom: 10px; }}
        .bk-chip {{
            background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white;
            border-radius: 12px; padding: 7px; text-align: center; font-size: 19px; font-weight: 800; cursor: pointer;
        }}
    </style>
    </head>
    <body>
        <div class="ribbon">
            <button class="pill active" onclick="showTab('abc', this)">🇬🇧 English A-Z</button>
            <button class="pill" onclick="showTab('marathi', this)">🇮🇳 मराठी मुळाक्षरे</button>
            <button class="pill" onclick="showTab('barakhadi', this)">✨ बाराखडी</button>
            <button class="pill" onclick="showTab('maths', this)">🔢 १ ते १०० व पाढे</button>
            <button class="pill" onclick="showTab('evs', this)">🌍 EVS / परिसर</button>
            <button class="pill" onclick="showTab('rhymes', this)">🎵 गाणी (Rhymes)</button>
        </div>

        <div class="hero" onclick="replayHero()">
            <div class="hero-big" id="hBig">A a</div>
            <div class="hero-title" id="hTitle">🍎 Apple (सफरचंद)</div>
            <div style="font-size:11.5px; color:#64748b;">🔊 आवाज ऐकण्यासाठी कोणत्याही कार्डवर टॅप करा!</div>
        </div>

        <div id="contentBox"></div>

        <script>
        const BILINGUAL = {bilingual_flag};
        const RATE = {v_speed};
        let voices = [];
        let mrVoice = null, enVoice = null;

        function loadVoices() {{
            if (!('speechSynthesis' in window)) return;
            voices = window.speechSynthesis.getVoices();
            mrVoice = voices.find(v => v.lang.toLowerCase().includes('mr')) || voices.find(v => v.lang.toLowerCase().includes('hi')) || voices[0];
            enVoice = voices.find(v => v.lang.toLowerCase().includes('en-in')) || voices.find(v => v.lang.toLowerCase().startsWith('en')) || voices[0];
        }}
        if ('speechSynthesis' in window) {{ loadVoices(); window.speechSynthesis.onvoiceschanged = loadVoices; }}

        function speakList(items) {{
            if (!('speechSynthesis' in window)) return;
            if (!voices.length) loadVoices();
            window.speechSynthesis.cancel();
            items.forEach(it => {{
                const u = new SpeechSynthesisUtterance(it.text);
                u.rate = RATE; u.pitch = 1.0;
                u.lang = it.lang === 'mr' ? 'mr-IN' : 'en-IN';
                if (it.lang === 'mr' && mrVoice) u.voice = mrVoice;
                if (it.lang === 'en' && enVoice) u.voice = enVoice;
                window.speechSynthesis.speak(u);
            }});
        }}

        function speakBoth(en, mr) {{
            if (BILINGUAL && mr) speakList([{{text: en, lang: 'en'}}, {{text: mr, lang: 'mr'}}]);
            else speakList([{{text: en, lang: 'en'}}]);
        }}

        const ABC = [
            {{c:'A',w:'Apple',mr:'सफरचंद',e:'🍎'}},{{c:'B',w:'Ball',mr:'चेंडू',e:'⚽'}},{{c:'C',w:'Cat',mr:'मांजर',e:'🐱'}},
            {{c:'D',w:'Dog',mr:'कुत्रा',e:'🐶'}},{{c:'E',w:'Elephant',mr:'हत्ती',e:'🐘'}},{{c:'F',w:'Fish',mr:'मासा',e:'🐟'}},
            {{c:'G',w:'Grapes',mr:'द्राक्षे',e:'🍇'}},{{c:'H',w:'House',mr:'घर',e:'🏠'}},{{c:'I',w:'Ice Cream',mr:'आईस्क्रीम',e:'🍦'}},
            {{c:'J',w:'Joker',mr:'विदूषक',e:'🤡'}},{{c:'K',w:'Kite',mr:'पतंग',e:'🪁'}},{{c:'L',w:'Lion',mr:'सिंह',e:'🦁'}},
            {{c:'M',w:'Mango',mr:'आंबा',e:'🥭'}},{{c:'N',w:'Nest',mr:'घरटे',e:'🪺'}},{{c:'O',w:'Orange',mr:'संत्रे',e:'🍊'}},
            {{c:'P',w:'Parrot',mr:'पोपट',e:'🦜'}},{{c:'Q',w:'Queen',mr:'राणी',e:'👑'}},{{c:'R',w:'Rabbit',mr:'ससा',e:'🐰'}},
            {{c:'S',w:'Sun',mr:'सूर्य',e:'☀️'}},{{c:'T',w:'Tiger',mr:'वाघ',e:'🐯'}},{{c:'U',w:'Umbrella',mr:'छत्री',e:'☂️'}},
            {{c:'V',w:'Van',mr:'गाडी',e:'🚐'}},{{c:'W',w:'Watch',mr:'घड्याळ',e:'⌚'}},{{c:'X',w:'Xylophone',mr:'झायलोफोन',e:'🎹'}},
            {{c:'Y',w:'Yacht',mr:'होडी',e:'⛵'}},{{c:'Z',w:'Zebra',mr:'झेब्रा',e:'🦓'}}
        ];

        const MAR = [
            {{c:'अ',w:'अननस',e:'🍍',s:'अ अननसाचा'}},{{c:'आ',w:'आगगाडी',e:'🚂',s:'आ आगगाडीचा'}},
            {{c:'इ',w:'इमारत',e:'🏢',s:'इ इमारतीचा'}},{{c:'ई',w:'ईडलिंबू',e:'🍋',s:'ई ईडलिंबूचा'}},
            {{c:'उ',w:'उखळ',e:'🥣',s:'उ उखळीचा'}},{{c:'ऊ',w:'ऊस',e:'🎋',s:'ऊ उसाचा'}},
            {{c:'ए',w:'एडका',e:'🐏',s:'ए एडक्याचा'}},{{c:'ऐ',w:'ऐरण',e:'🔨',s:'ऐ ऐरणीचा'}},
            {{c:'ओ',w:'ओढा',e:'🏞️',s:'ओ ओढ्याचा'}},{{c:'औ',w:'औषध',e:'💊',s:'औ औषधाचा'}},
            {{c:'अं',w:'अंगठी',e:'💍',s:'अं अंगठीचा'}},{{c:'क',w:'कमळ',e:'🪷',s:'क कमळाचा'}},
            {{c:'ख',w:'खडू',e:'🖍️',s:'ख खडूचा'}},{{c:'ग',w:'गणपती',e:'🐘',s:'ग गणपतीचा'}},
            {{c:'घ',w:'घर',e:'🏡',s:'घ घराचा'}},{{c:'च',w:'चमचा',e:'🥄',s:'च चमच्याचा'}},
            {{c:'छ',w:'छत्री',e:'☂️',s:'छ छत्रीचा'}},{{c:'ज',w:'जहाज',e:'🚢',s:'ज जहाजाचा'}},
            {{c:'झ',w:'झबले',e:'👗',s:'झ झबल्याचा'}},{{c:'ट',w:'टपाल',e:'📮',s:'ट टपालाचा'}},
            {{c:'ठ',w:'ठसा',e:'💮',s:'ठ ठशाचा'}},{{c:'ड',w:'डबा',e:'📦',s:'ड डब्याचा'}},
            {{c:'ढ',w:'ढग',e:'☁️',s:'ढ ढगाचा'}},{{c:'ण',w:'बाण',e:'🏹',s:'ण बाणाचा'}},
            {{c:'त',w:'तलवार',e:'⚔️',s:'त तलवारीचा'}},{{c:'थ',w:'थवा',e:'🐦',s:'थ थव्याचा'}},
            {{c:'द',w:'दप्तर',e:'🎒',s:'द दप्तराचा'}},{{c:'ध',w:'धनुष्य',e:'🏹',s:'ध धनुष्याचा'}},
            {{c:'न',w:'नळ',e:'🚰',s:'न नळाचा'}},{{c:'प',w:'पतंग',e:'🪁',s:'प पतंगाचा'}},
            {{c:'फ',w:'फणस',e:'🍈',s:'फ फणसाचा'}},{{c:'ब',w:'बदक',e:'🦆',s:'ब बदकाचा'}},
            {{c:'भ',w:'भवरा',e:'🪀',s:'भ भवऱ्याचा'}},{{c:'म',w:'मका',e:'🌽',s:'म मक्याचा'}},
            {{c:'य',w:'यज्ञ',e:'🔥',s:'य यज्ञाचा'}},{{c:'र',w:'रथ',e:'🛞',s:'र रथाचा'}},
            {{c:'ल',w:'लसूण',e:'🧄',s:'ल लसणाचा'}},{{c:'व',w:'वजन',e:'🏋️',s:'व वजनाचा'}},
            {{c:'श',w:'शहामृग',e:'🦤',s:'श शहामृगाचा'}},{{c:'ष',w:'षटकोन',e:'🛑',s:'ष षटकोनाचा'}},
            {{c:'स',w:'ससा',e:'🐰',s:'स सशाचा'}},{{c:'ह',w:'हत्ती',e:'🐘',s:'ह हत्तीचा'}},
            {{c:'ळ',w:'बाळ',e:'👶',s:'ळ बाळाचा'}},{{c:'क्ष',w:'क्षत्रिय',e:'🛡️',s:'क्ष क्षत्रियाचा'}},
            {{c:'ज्ञ',w:'ज्ञानेश्वर',e:'🙏',s:'ज्ञ ज्ञानेश्वरांचा'}}
        ];

        const EVS = [
            {{e:'🍎',en:'Apple',mr:'सफरचंद'}},{{e:'🥭',en:'Mango',mr:'आंबा'}},{{e:'🍌',en:'Banana',mr:'केळी'}},
            {{e:'🥔',en:'Potato',mr:'बटाटा'}},{{e:'🍅',en:'Tomato',mr:'टोमॅटो'}},{{e:'🦁',en:'Lion',mr:'सिंह'}},
            {{e:'🐯',en:'Tiger',mr:'वाघ'}},{{e:'🦚',en:'Peacock',mr:'मोर'}},{{e:'👀',en:'Eyes',mr:'डोळे'}},
            {{e:'✋',en:'Hand',mr:'हात'}},{{e:'1️⃣',en:'Monday',mr:'सोमवार'}},{{e:'7️⃣',en:'Sunday',mr:'रविवार'}}
        ];

        const COLS = ['#4f46e5','#db2777','#059669','#d97706','#2563eb','#7c3aed'];
        let lastFn = () => speakBoth('A for Apple', 'Apple म्हणजे सफरचंद');
        function replayHero() {{ if(lastFn) lastFn(); }}

        function setHero(big, title, fn) {{
            document.getElementById('hBig').textContent = big;
            document.getElementById('hTitle').textContent = title;
            lastFn = fn; fn();
        }}

        function showTab(tab, btn) {{
            if(btn) {{
                btn.parentElement.querySelectorAll('.pill').forEach(p=>p.classList.remove('active'));
                btn.classList.add('active');
            }}
            const box = document.getElementById('contentBox');
            box.innerHTML = '';

            if(tab === 'abc') {{
                const g = document.createElement('div'); g.className = 'grid';
                ABC.forEach((it, i) => {{
                    const c = document.createElement('div'); c.className = 'card';
                    c.innerHTML = `<div class="char" style="color:${{COLS[i%6]}}">${{it.c}} ${{it.c.toLowerCase()}}</div><div class="emo">${{it.e}}</div><div class="en">${{it.w}}</div><div class="mr">${{it.mr}}</div>`;
                    c.onclick = () => setHero(`${{it.c}} ${{it.c.toLowerCase()}}`, `${{it.e}} ${{it.w}} (${{it.mr}})`, () => speakBoth(`${{it.c}}. ${{it.c}} for ${{it.w}}`, `${{it.w}} म्हणजे ${{it.mr}}`));
                    g.appendChild(c);
                }});
                box.appendChild(g);
            }} else if(tab === 'marathi') {{
                const g = document.createElement('div'); g.className = 'grid';
                MAR.forEach((it, i) => {{
                    const c = document.createElement('div'); c.className = 'card';
                    c.innerHTML = `<div class="char" style="color:${{COLS[i%6]}}">${{it.c}}</div><div class="emo">${{it.e}}</div><div class="en">${{it.w}}</div>`;
                    c.onclick = () => setHero(it.c, `${{it.e}} ${{it.w}}`, () => speakList([{{text: it.s, lang:'mr'}}]));
                    g.appendChild(c);
                }});
                box.appendChild(g);
            }} else if(tab === 'barakhadi') {{
                renderBarakhadi('क');
            }} else if(tab === 'maths') {{
                const g = document.createElement('div'); g.className = 'grid';
                for(let n=1; n<=30; n++) {{
                    const c = document.createElement('div'); c.className = 'card';
                    c.innerHTML = `<div class="char" style="color:${{COLS[n%6]}}">${{n}}</div><div class="mr">Table / अंक</div>`;
                    c.onclick = () => setHero(String(n), `Number ${{n}}`, () => speakBoth(String(n), String(n)));
                    g.appendChild(c);
                }}
                box.appendChild(g);
            }} else if(tab === 'evs') {{
                const g = document.createElement('div'); g.className = 'grid';
                EVS.forEach(it => {{
                    const c = document.createElement('div'); c.className = 'card';
                    c.innerHTML = `<div class="emo">${{it.e}}</div><div class="en">${{it.en}}</div><div class="mr">${{it.mr}}</div>`;
                    c.onclick = () => setHero(it.e, `${{it.en}} (${{it.mr}})`, () => speakBoth(it.en, `${{it.en}} म्हणजे ${{it.mr}}`));
                    g.appendChild(c);
                }});
                box.appendChild(g);
            }} else if(tab === 'rhymes') {{
                box.innerHTML = `
                    <div class="card" style="text-align:left; padding:14px; margin-bottom:10px;" onclick="speakList([{{text:'Twinkle twinkle little star, how I wonder what you are! Up above the world so high, like a diamond in the sky.', lang:'en'}}])">
                        <div class="en" style="font-size:16px; color:#be185d;">🌟 Twinkle Twinkle Little Star (🔊 ऐका)</div>
                        <div style="font-size:13.5px; margin-top:4px;">Twinkle, twinkle, little star, How I wonder what you are!</div>
                    </div>
                    <div class="card" style="text-align:left; padding:14px;" onclick="speakList([{{text:'ये रे ये रे पावसा, तुला देतो पैसा! पैसा झाला खोटा, पाऊस आला मोठा!', lang:'mr'}}])">
                        <div class="en" style="font-size:16px; color:#be185d;">🌧️ ये रे ये रे पावसा (🔊 ऐका)</div>
                        <div style="font-size:13.5px; margin-top:4px;">ये रे ये रे पावसा, तुला देतो पैसा! पैसा झाला खोटा, पाऊस आला मोठा!</div>
                    </div>
                `;
            }}
        }}

        function renderBarakhadi(ch) {{
            const matras = ['','ा','ि','ी','ु','ू','े','ै','ो','ौ','ं','ः'];
            const box = document.getElementById('contentBox');
            let html = '<div class="bk-strip">';
            matras.forEach(m => {{
                const comb = ch + m;
                html += `<div class="bk-chip" onclick="speakList([{{text:'${{comb}}',lang:'mr'}}])">${{comb}}</div>`;
            }});
            html += '</div><div class="grid" id="bkGrid"></div>';
            box.innerHTML = html;
            const g = document.getElementById('bkGrid');
            MAR.slice(11).forEach((it, i) => {{
                const c = document.createElement('div'); c.className = 'card';
                c.innerHTML = `<div class="char" style="color:${{COLS[i%6]}}">${{it.c}}</div><div class="mr">${{it.c}} बाराखडी</div>`;
                c.onclick = () => {{ renderBarakhadi(it.c); speakList([{{text: matras.map(m=>it.c+m).join(', '), lang:'mr'}}]); }};
                g.appendChild(c);
            }});
        }}

        showTab('abc');
        </script>
    </body>
    </html>
    """
    components.html(interactive_learning_html, height=620, scrolling=True)

# ==============================================================================
# TAB 2: MAGIC SLATE & INTERACTIVE QUIZ
# ==============================================================================
with tab_slate:
    slate_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body { margin: 0; font-family: sans-serif; color: white; text-align: center; }
        .bar { display: flex; justify-content: center; gap: 8px; margin-bottom: 8px; }
        button {
            background: #4f46e5; color: white; border: none; padding: 8px 14px;
            border-radius: 12px; font-weight: 800; cursor: pointer;
        }
        canvas {
            background: #090d16; border: 3px solid #6366f1; border-radius: 20px;
            touch-action: none; width: 100%; height: 280px;
        }
    </style>
    </head>
    <body>
        <div class="bar">
            <button onclick="step(-1)">◀ मागे</button>
            <button onclick="toggleMode()" id="mBtn">मोड: A-Z</button>
            <button onclick="clearSlate()" style="background:#ef4444;">🧽 पुसा</button>
            <button onclick="step(1)">पुढे ▶</button>
        </div>
        <canvas id="c"></canvas>
        <script>
            const charsABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
            const charsMAR = ["अ","आ","इ","ई","उ","ऊ","क","ख","ग","घ","च","छ","ज","झ","ट","त","प","म","य","र","ल","व","श","स","ह","ळ","क्ष","ज्ञ"];
            let mode = 'ABC', idx = 0, drawing = false, pts = [];
            const cv = document.getElementById('c'), ctx = cv.getContext('2d');
            function resize() { cv.width = cv.clientWidth; cv.height = cv.clientHeight; draw(); }
            window.onresize = resize;
            function curChar() { return mode === 'ABC' ? charsABC[idx % charsABC.length] : charsMAR[idx % charsMAR.length]; }
            function toggleMode() { mode = mode === 'ABC' ? 'MAR' : 'ABC'; idx = 0; document.getElementById('mBtn').textContent = 'मोड: ' + mode; clearSlate(); }
            function step(d) { idx = Math.max(0, idx + d); clearSlate(); }
            function clearSlate() { pts = []; draw(); }
            function draw() {
                ctx.clearRect(0,0,cv.width,cv.height);
                ctx.font = "900 170px sans-serif";
                ctx.textAlign = "center"; ctx.textBaseline = "middle";
                ctx.strokeStyle = "rgba(255,255,255,0.22)"; ctx.lineWidth = 4;
                ctx.setLineDash([8,8]); ctx.strokeText(curChar(), cv.width/2, cv.height/2);
                ctx.setLineDash([]); ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.lineWidth = 16;
                for(let i=1;i<pts.length;i++){
                    if(pts[i].s) continue;
                    ctx.strokeStyle = `hsl(${pts[i].h}, 95%, 60%)`;
                    ctx.beginPath(); ctx.moveTo(pts[i-1].x, pts[i-1].y); ctx.lineTo(pts[i].x, pts[i].y); ctx.stroke();
                }
            }
            cv.onpointerdown = e => { drawing = true; const r = cv.getBoundingClientRect(); pts.push({x:e.clientX-r.left, y:e.clientY-r.top, s:true, h:Math.random()*360}); };
            cv.onpointermove = e => { if(!drawing) return; const r = cv.getBoundingClientRect(); pts.push({x:e.clientX-r.left, y:e.clientY-r.top, s:false, h:(Date.now()*0.2)%360}); draw(); };
            window.onpointerup = () => drawing = false;
            setTimeout(resize, 80);
        </script>
    </body>
    </html>
    """
    components.html(slate_html, height=350)

# ==============================================================================
# TAB 3: LIVE ATTENDANCE REGISTER (Saved on Server!)
# ==============================================================================
with tab_att:
    st.markdown("<div class='dj-card'><h3 style='margin:0;'>📋 Dyanjyoti Classes — हजेरी पट (Attendance)</h3></div>", unsafe_allow_html=True)

    sel_date = st.date_input("📅 तारीख निवडा (Select Date):", datetime.now()).strftime("%Y-%m-%d")
    day_record = db["attendance"].get(sel_date, {})

    if st.session_state.teacher_unlocked:
        st.success("👩‍🏫 Teacher Mode Active: तुम्ही हजेरी सेव्ह करू शकता.")
        updated_record = {}
        for idx, stu in enumerate(db["students"]):
            sname = stu["name"]
            cur_status = day_record.get(sname, "उपस्थित (Present) ✅")
            choice = st.radio(
                f"👧 **{idx+1}. {sname}** ({stu.get('cls', 'All')})",
                ["उपस्थित (Present) ✅", "गैरहजर (Absent) ❌"],
                index=0 if "Present" in cur_status else 1,
                horizontal=True,
                key=f"att_{sel_date}_{idx}"
            )
            updated_record[sname] = choice

        if st.button("💾 आजची हजेरी सेव्ह करा (Save Attendance)", use_container_width=True):
            db["attendance"][sel_date] = updated_record
            save_db(db)
            st.toast("✅ हजेरी यशस्वीरित्या सेव्ह झाली!")
            st.rerun()
    else:
        st.info("🔒 पालक व विद्यार्थ्यांसाठी Read-Only यादी (हजेरी भरण्यासाठी ⚙️ सेटिंग्ज मधून Teacher Login करा).")
        for idx, stu in enumerate(db["students"]):
            sname = stu["name"]
            status = day_record.get(sname, "उपस्थित (Present) ✅")
            st.markdown(f"""
            <div class="dj-card" style="padding:10px 14px; display:flex; justify-content:space-between; align-items:center;">
                <strong>{idx+1}. {sname}</strong>
                <span>{status}</span>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: LIVE HOMEWORK & FILE / PHOTO ATTACHMENT PORTAL
# ==============================================================================
with tab_hw:
    st.markdown("<div class='dj-card'><h3 style='margin:0;'>📖 गृहपाठ व वर्कशीट (Homework Portal)</h3></div>", unsafe_allow_html=True)

    # Teacher Upload Box (Only visible when Teacher PIN is unlocked)
    if st.session_state.teacher_unlocked:
        with st.expander("➕ नवीन गृहपाठ किंवा फोटो/PDF फाईल जोडा (Teacher Only)", expanded=True):
            hw_cls = st.selectbox("वर्ग निवडा:", ["All Classes", "Nursery", "LKG / UKG", "1st Std SSC"])
            hw_title = st.text_input("विषय व शीर्षक (उदा. मराठी - क ते ज्ञ लिहा):")
            hw_desc = st.text_area("गृहपाठ माहिती (Homework Instructions):")
            hw_file = st.file_uploader("📎 वहीचा फोटो किंवा PDF वर्कशीट जोडा (Attach Photo / PDF):", type=["png", "jpg", "jpeg", "pdf"])
            hw_link = st.text_input("🔗 किंवा Google Drive / YouTube Link (Optional):")

            if st.button("✅ गृहपाठ पब्लिश करा (Publish Live)", use_container_width=True):
                if hw_title and hw_desc:
                    f_name, f_data, f_type = "", "", ""
                    if hw_file is not None:
                        f_name = hw_file.name
                        f_type = hw_file.type
                        f_data = base64.b64encode(hw_file.read()).decode("utf-8")

                    db["homework"].insert(0, {
                        "id": f"hw_{int(datetime.now().timestamp())}",
                        "date": datetime.now().strftime("%d %b %Y"),
                        "cls": hw_cls,
                        "title": hw_title,
                        "desc": hw_desc,
                        "file_name": f_name,
                        "file_data": f_data,
                        "file_type": f_type,
                        "link": hw_link
                    })
                    save_db(db)
                    st.success("🎉 गृहपाठ पब्लिश झाला! आता सर्व पालकांना हा अभ्यास दिसेल.")
                    st.rerun()
                else:
                    st.warning("कृपया विषय आणि माहिती भरा!")

    # Filter Homework by Class
    filter_cls = st.selectbox("🎓 तुमचा वर्ग निवडा (Filter Class):", ["All Classes", "Nursery", "LKG / UKG", "1st Std SSC"])

    for hw in db["homework"]:
        if filter_cls != "All Classes" and hw["cls"] not in ["All Classes", filter_cls]:
            continue

        st.markdown(f"""
        <div class="dj-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span class="hw-badge">🎓 {hw['cls']}</span>
                <span style="font-size:12px; color:#64748b; font-weight:800;">📅 {hw['date']}</span>
            </div>
            <h4 style="margin:4px 0; color:#0f172a;">{hw['title']}</h4>
            <p style="white-space:pre-line; background:#f8fafc; padding:10px; border-radius:12px; border:1px solid #e2e8f0; margin:6px 0;">{hw['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Show Attached Photo or Downloadable PDF
        if hw.get("file_data"):
            raw_bytes = base64.b64decode(hw["file_data"])
            if "image" in hw.get("file_type", ""):
                st.image(raw_bytes, caption=f"📎 {hw['file_name']}", use_container_width=True)
            st.download_button(
                label=f"📥 Download Attachment ({hw['file_name']})",
                data=raw_bytes,
                file_name=hw["file_name"],
                mime=hw.get("file_type", "application/octet-stream"),
                key=f"dl_{hw['id']}"
            )

        if hw.get("link"):
            st.markdown(f"🔗 **[फाईल / व्हिडिओ लिंक उघडा (Click Here)]({hw['link']})**")

        if st.session_state.teacher_unlocked:
            if st.button(f"🗑️ हा गृहपाठ डिलीट करा ({hw['title']})", key=f"del_{hw['id']}"):
                db["homework"] = [x for x in db["homework"] if x["id"] != hw["id"]]
                save_db(db)
                st.rerun()

# ==============================================================================
# TAB 5: SETTINGS & TEACHER PASSWORD MANAGEMENT (⚙️ सेटिंग्ज)
# ==============================================================================
with tab_settings:
    st.markdown("<div class='dj-card'><h3 style='margin:0;'>⚙️ अ‍ॅप व शिक्षक सेटिंग्ज (Settings)</h3></div>", unsafe_allow_html=True)

    # 1. Teacher Login & Password Rights
    st.subheader("🔐 शिक्षक लॉगिन (Teacher Admin Login)")
    if not st.session_state.teacher_unlocked:
        pin_inp = st.text_input("शिक्षक पिन टाका (Default PIN: 1234):", type="password")
        if st.button("🔓 Teacher Mode Unlock करा"):
            if pin_inp == db.get("teacher_pin", "1234"):
                st.session_state.teacher_unlocked = True
                st.success("✅ Teacher Mode सुरू झाला! आता तुम्ही गृहपाठ, हजेरी आणि पासवर्ड बदलू शकता.")
                st.rerun()
            else:
                st.error("❌ चुकीचा पासवर्ड!")
    else:
        st.success("✅ तुम्ही सध्या Teacher Mode मध्ये आहात.")
        if st.button("🔒 Teacher Mode लॉक करा (Return to Parent Read-Only View)"):
            st.session_state.teacher_unlocked = False
            st.rerun()

        st.markdown("---")
        st.subheader("🔑 तुमचा Teacher पासवर्ड बदला (Change PIN)")
        new_pin = st.text_input("नवीन पासवर्ड टाका (उदा. 5678):")
        if st.button("💾 नवीन पासवर्ड सेव्ह करा"):
            if len(new_pin.strip()) >= 4:
                db["teacher_pin"] = new_pin.strip()
                save_db(db)
                st.success("✅ तुमचा नवीन पासवर्ड सेव्ह झाला आहे!")
            else:
                st.warning("किमान ४ अंकी पासवर्ड टाका.")

        st.markdown("---")
        st.subheader("👧 नवीन विद्यार्थी जोडा किंवा काढा (Manage Students)")
        c1, c2 = st.columns(2)
        with c1:
            new_stu_name = st.text_input("विद्यार्थ्याचे नाव (उदा. सोहम):")
        with c2:
            new_stu_cls = st.selectbox("वर्ग:", ["Nursery", "LKG / UKG", "1st Std SSC"])

        if st.button("➕ विद्यार्थी यादीत जोडा"):
            if new_stu_name.strip():
                db["students"].append({"name": new_stu_name.strip(), "cls": new_stu_cls, "stars": 0})
                save_db(db)
                st.success(f"✅ {new_stu_name} चे नाव जोडले!")
                st.rerun()

        for i, s in enumerate(db["students"]):
            col_a, col_b = st.columns([4, 1])
            col_a.write(f"**{i+1}. {s['name']}** ({s.get('cls', '')})")
            if col_b.button("🗑️ काढा", key=f"rm_stu_{i}"):
                db["students"].pop(i)
                save_db(db)
                st.rerun()

    st.markdown("---")
    st.subheader("🔊 आवाज सेटिंग्ज (Voice Settings)")
    b_mode = st.toggle("Indian English + मराठी अर्थ एकत्र बोला (Bilingual Voice)", value=db.get("bilingual", True))
    v_spd = st.slider("आवाजाचा वेग (Voice Speed):", 0.60, 1.10, float(db.get("voice_speed", 0.82)), 0.05)
    if st.button("💾 आवाज सेटिंग सेव्ह करा"):
        db["bilingual"] = b_mode
        db["voice_speed"] = v_spd
        save_db(db)
        st.success("✅ आवाज सेटिंग सेव्ह झाली!")
        st.rerun()
