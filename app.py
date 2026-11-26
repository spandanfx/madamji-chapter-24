import streamlit as st
import streamlit.components.v1 as components
import random
import time
import base64
import os
import config

def resolve_image_url(url_or_path):
    """Resolves local file paths or URLs to base64 Data URIs with multi-directory fallback."""
    if not url_or_path:
        return getattr(config, "MADAMJI_PHOTO_B64", "")
    
    # If it's already a Data URI or remote web URL, return directly
    if str(url_or_path).startswith("data:") or str(url_or_path).startswith("http://") or str(url_or_path).startswith("https://"):
        return url_or_path

    # Script directory (absolute location of app.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.basename(str(url_or_path))

    # Comprehensive list of candidate paths to check
    candidates = [
        os.path.join(script_dir, str(url_or_path)),
        os.path.join(script_dir, "assets", filename),
        os.path.join(script_dir, filename),
        str(url_or_path),
        os.path.join(os.getcwd(), str(url_or_path)),
        os.path.join(os.getcwd(), "assets", filename),
        os.path.join(os.getcwd(), filename),
    ]

    for cand in candidates:
        if cand and os.path.isfile(cand):
            try:
                with open(cand, "rb") as f:
                    ext = cand.split(".")[-1].lower()
                    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
                    return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
            except Exception:
                pass

    # If missing from disk, return embedded Madamji base64 asset as bulletproof fallback
    embedded = getattr(config, "MADAMJI_PHOTO_B64", "")
    if embedded and any(k in str(url_or_path).lower() for k in ["madamji", "mahima", "assets"]):
        return embedded

    return url_or_path

# Set page configuration - Fullscreen Mobile Friendly
st.set_page_config(
    page_title=f"Netflix | Stranger Things: Happy Birthday {config.FRIEND_NAME}!",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global Custom CSS optimized specifically for Mobile (Pixel 9a viewport ~412px) and Desktop
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Bebas+Neue&family=Lora:ital,wght@0,400;0,500;1,400&family=VT323&family=Inter:wght@400;600;800&display=swap');

/* COMPLETELY HIDE STREAMLIT SIDEBAR & COLLAPSED CONTROLS */
[data-testid="stSidebar"], 
[data-testid="collapsedControl"],
section[data-testid="stSidebar"],
div[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* Base Body Styling */
.stApp {
    background-color: #0b090c;
    color: #e5e5e5;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}

/* Container Spacing Optimized for Pixel 9a & Mobile */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
    max-width: 950px !important;
    margin: 0 auto !important;
}

/* Netflix Branding */
.netflix-logo {
    font-family: 'Bebas Neue', sans-serif;
    color: #E50914;
    font-size: 2.6rem;
    letter-spacing: 2px;
    text-shadow: 0 0 15px rgba(229, 9, 20, 0.5);
    margin: 0;
    line-height: 1;
}

.netflix-badge {
    background: #E50914;
    color: white;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.95rem;
    padding: 3px 8px;
    border-radius: 2px;
    letter-spacing: 1px;
}

/* Section Chapter Titles */
.chapter-divider {
    border-top: 2px solid #3d1419;
    margin: 35px 0 20px 0;
    position: relative;
    text-align: center;
}

.chapter-badge {
    display: inline-block;
    background: #18090d;
    border: 1px solid #E50914;
    color: #ff4d4d;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.25rem;
    padding: 4px 18px;
    border-radius: 20px;
    letter-spacing: 1.5px;
    box-shadow: 0 0 15px rgba(229, 9, 20, 0.3);
    margin-top: -16px;
}

.chapter-heading {
    font-family: 'Cinzel', serif;
    font-size: 1.6rem;
    color: #fff;
    margin: 15px 0 5px 0;
    text-align: center;
    letter-spacing: 1.5px;
}

.chapter-caption {
    font-family: 'VT323', monospace;
    font-size: 1.2rem;
    color: #aaa;
    text-align: center;
    margin-bottom: 18px;
    letter-spacing: 1px;
}

/* Hero Section */
.hero-card {
    position: relative;
    background: linear-gradient(180deg, rgba(14,10,14,0.6) 0%, rgba(11,9,12,0.95) 100%),
                radial-gradient(circle at 80% 25%, rgba(160, 0, 0, 0.45) 0%, rgba(10,5,10,0.9) 75%);
    border: 1px solid #44151a;
    border-radius: 8px;
    padding: 24px 18px;
    margin: 20px 0;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 30px rgba(229, 9, 20, 0.2);
}

.stranger-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(2rem, 5.5vw, 3.4rem);
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #0a0608;
    -webkit-text-stroke: 1.8px #ff1a1a;
    text-shadow: 
        0 0 10px #ff0000,
        0 0 22px #ff0000,
        0 0 40px #b30000;
    margin: 8px 0;
    line-height: 1.15;
}

.netflix-meta {
    display: flex;
    gap: 8px 12px;
    align-items: center;
    flex-wrap: wrap;
    font-size: 0.88rem;
    margin: 12px 0;
}

.meta-match {
    color: #46d369;
    font-weight: 800;
}

.meta-badge {
    border: 1px solid #666;
    padding: 1px 6px;
    border-radius: 3px;
    color: #ccc;
    font-size: 0.75rem;
}

/* Responsive Profiles 2x2 Grid for Mobile (Pixel 9a) & 4 Columns on Desktop */
.profile-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 15px 0 25px 0;
}

.profile-box {
    background: #141115;
    border: 2px solid #281d28;
    border-radius: 8px;
    padding: 12px 8px;
    text-align: center;
    transition: all 0.3s ease;
    min-height: 185px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.profile-box:hover {
    border-color: #E50914;
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(229, 9, 20, 0.4);
}
.profile-avatar {
    width: 72px;
    height: 72px;
    border-radius: 6px;
    object-fit: cover;
    margin: 0 auto 8px auto;
    border: 2px solid transparent;
}
.profile-box:hover .profile-avatar {
    border-color: #fff;
}

/* Hopper Letter Parchment - Crisp, Elegant & Readable Typography */
.hopper-letter {
    background: #141012;
    border-left: 4px solid #d4a373;
    border-radius: 6px;
    padding: 26px 22px;
    font-family: 'Lora', Georgia, serif;
    font-weight: 400;
    color: #f3eae0;
    font-size: 1.08rem;
    line-height: 1.85;
    letter-spacing: 0.25px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6), inset 0 0 25px rgba(212, 163, 115, 0.08);
    margin-bottom: 30px;
}

/* Dossier Layout */
.dossier-card {
    background: #151014;
    border: 2px solid #5a1414;
    border-radius: 6px;
    padding: 20px;
    position: relative;
    margin-bottom: 20px;
}

/* Custom Buttons - Touch Target friendly (min 44px) */
div.stButton > button {
    background: linear-gradient(180deg, #E50914 0%, #990000 100%);
    color: #ffffff;
    font-family: 'Cinzel', serif;
    font-weight: 700;
    border: 1px solid #ff4d4d;
    border-radius: 4px;
    box-shadow: 0 0 15px rgba(229, 9, 20, 0.4);
    min-height: 48px;
    font-size: 1.05rem;
    width: 100%;
    transition: all 0.25s ease;
}
div.stButton > button:hover {
    background: linear-gradient(180deg, #ff1a1a 0%, #b30000 100%);
    box-shadow: 0 0 22px rgba(255, 30, 30, 0.8);
    transform: translateY(-2px);
}

/* Responsive Breakpoints for Pixel 9a & Mobile (< 700px) */
@media (max-width: 700px) {
    .block-container {
        padding-left: 0.65rem !important;
        padding-right: 0.65rem !important;
        padding-top: 0.8rem !important;
    }
    .profile-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
    }
    .profile-box {
        min-height: 170px !important;
        padding: 10px 6px !important;
    }
    .profile-avatar {
        width: 66px !important;
        height: 66px !important;
    }
    .hero-card {
        padding: 18px 14px !important;
    }
    .hopper-letter {
        padding: 22px 16px !important;
        font-size: 1.02rem !important;
        line-height: 1.8 !important;
        font-weight: 400 !important;
    }
    .stranger-title {
        font-size: 1.85rem !important;
    }
}

/* CRT Scanlines Overlay */
.crt-overlay {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
    background-size: 100% 4px;
    z-index: 999;
    pointer-events: none;
    opacity: 0.22;
}
</style>
<div class="crt-overlay"></div>
""", unsafe_allow_html=True)

# ----------------- TOP NAVBAR -----------------
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 5px;">
    <span class="netflix-logo">NETFLIX</span>
    <span class="netflix-badge">ORIGINAL SPECIAL</span>
</div>
""", unsafe_allow_html=True)

# ----------------- "WHO'S WATCHING?" 2x2 MOBILE GRID / 4x1 DESKTOP -----------------
st.markdown("""
<div style="font-family: 'Bebas Neue'; font-size: 1.35rem; letter-spacing: 1.2px; color: #ddd; margin: 15px 0 10px 0;">
    👥 WHO IS CELEBRATING IN HAWKINS TODAY?
</div>
""", unsafe_allow_html=True)

# Generate responsive HTML grid for Pixel 9a
cards = []
for prof in config.NETFLIX_PROFILES:
    is_her = (prof["id"] == "birthday_girl")
    display_name = prof["name"].format(name=config.FRIEND_NAME)
    avatar_src = resolve_image_url(prof["avatar"])
    fallback_src = prof.get("fallback", "") or (getattr(config, "MADAMJI_PHOTO_B64", "") if is_her else "")
    onerror_attr = f'onerror="this.onerror=null; this.src=\'{fallback_src}\';"' if fallback_src else ""
    border_style = "border-color: #E50914; background: #220a0f;" if is_her else ""

    card_html = (
        f'<div class="profile-box" style="{border_style}">'
        f'<div>'
        f'<img class="profile-avatar" src="{avatar_src}" {onerror_attr} referrerpolicy="no-referrer">'
        f'<div style="font-weight: 700; font-size: 0.92rem; color: {"#ff4d4d" if is_her else "#eee"}; line-height: 1.2;">{display_name}</div>'
        f'<div style="font-size: 0.75rem; color: #888; margin-top: 3px;">{prof["role"]}</div>'
        f'</div>'
        f'<div style="margin-top: 8px; font-size: 0.75rem; color: #ffcc00; font-weight: bold;">{prof["badge"]}</div>'
        f'</div>'
    )
    cards.append(card_html)

profiles_html = f'<div class="profile-grid">{"".join(cards)}</div>'
st.markdown(profiles_html, unsafe_allow_html=True)

# ----------------- NETFLIX HERO EPISODE BANNER -----------------
st.markdown(f"""
<div class="hero-card">
    <div style="font-family: 'Bebas Neue'; color: #ff4d4d; letter-spacing: 2px; font-size: 1.15rem;">
        ★ {config.NETFLIX_METRICS['badge']} ★
    </div>
    <div class="stranger-title">STRANGER BIRTHDAYS</div>
    <div style="font-family: 'Cinzel'; font-size: 1.2rem; color: #ffcccc; margin-bottom: 5px;">
        {config.NETFLIX_METRICS['episode_title']}
    </div>
    <div class="netflix-meta">
        <span class="meta-match">{config.NETFLIX_METRICS['match']}</span>
        <span class="meta-badge">{config.CHAPTER_NUMBER}</span>
        <span class="meta-badge">{config.NETFLIX_METRICS['maturity']}</span>
        <span style="color: #aaa;">{config.NETFLIX_METRICS['duration']}</span>
        <span class="meta-badge">{config.NETFLIX_METRICS['quality']}</span>
    </div>
    <p style="color: #ccc; font-size: 1rem; line-height: 1.6; margin-top: 8px;">
        {config.NETFLIX_METRICS['synopsis']}
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# CHAPTER 1: JOYCE'S CHRISTMAS LIGHT WALL (Optimized for Mobile Pixel 9a)
# ==============================================================================
st.markdown("""
<div class="chapter-divider">
    <span class="chapter-badge">CHAPTER 1</span>
</div>
<div class="chapter-heading">JOYCE'S COMMUNICATION WALL</div>
<div class="chapter-caption">When the bulbs flicker on the floral wallpaper, Hawkins is sending a message.</div>
""", unsafe_allow_html=True)

lights_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=VT323&display=swap');

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    padding: 12px 6px;
    background: #1b1614;
    background-image: 
        radial-gradient(circle, rgba(0,0,0,0.5) 0%, rgba(10,5,5,0.95) 100%),
        repeating-linear-gradient(45deg, #241d1a 0, #241d1a 20px, #1c1613 20px, #1c1613 40px);
    border: 3px solid #3d2c23;
    border-radius: 8px;
    box-shadow: inset 0 0 40px #000;
    font-family: 'Permanent Marker', cursive;
    color: #111;
    user-select: none;
}}

.row-container {{
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex-wrap: nowrap;
    margin-bottom: 20px;
    width: 100%;
}}

.char-block {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 2px 1px;
    flex: 1;
    max-width: 38px;
}}

.bulb {{
    width: 17px;
    height: 26px;
    border-radius: 50% 50% 45% 45%;
    margin-bottom: 4px;
    position: relative;
    opacity: 0.3;
    transition: all 0.15s ease-in-out;
    border: 1px solid rgba(0,0,0,0.6);
}}

.bulb::before {{
    content: '';
    position: absolute;
    top: -5px;
    left: 4px;
    width: 9px;
    height: 5px;
    background: #333;
    border-radius: 2px;
}}

.letter {{
    font-size: 1.6rem;
    color: #0d0a09;
    -webkit-text-stroke: 1px #000;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.1);
    transition: all 0.2s;
}}

/* Bulb Colors */
.bulb-red {{ background: #ff2222; }}
.bulb-green {{ background: #00e640; }}
.bulb-blue {{ background: #00bfff; }}
.bulb-yellow {{ background: #ffd700; }}
.bulb-purple {{ background: #da70d6; }}
.bulb-orange {{ background: #ff8c00; }}

.bulb.active {{
    opacity: 1 !important;
    transform: scale(1.35);
}}

.bulb-red.active {{ box-shadow: 0 0 18px 6px #ff2222, 0 0 35px 12px rgba(255,34,34,0.8); }}
.bulb-green.active {{ box-shadow: 0 0 18px 6px #00e640, 0 0 35px 12px rgba(0,230,64,0.8); }}
.bulb-blue.active {{ box-shadow: 0 0 18px 6px #00bfff, 0 0 35px 12px rgba(0,191,255,0.8); }}
.bulb-yellow.active {{ box-shadow: 0 0 18px 6px #ffd700, 0 0 35px 12px rgba(255,215,0,0.8); }}
.bulb-purple.active {{ box-shadow: 0 0 18px 6px #da70d6, 0 0 35px 12px rgba(218,112,214,0.8); }}
.bulb-orange.active {{ box-shadow: 0 0 18px 6px #ff8c00, 0 0 35px 12px rgba(255,140,0,0.8); }}

.char-block.lit .letter {{
    color: #fff !important;
    text-shadow: 0 0 15px #ffeedd, 0 0 25px #ff5533 !important;
    transform: scale(1.15);
}}

.controls {{
    display: flex;
    justify-content: center;
    margin-top: 15px;
}}

button.btn-light {{
    background: #E50914;
    color: white;
    border: 1px solid #ff4444;
    padding: 12px 24px;
    font-family: 'VT323', monospace;
    font-size: 1.45rem;
    cursor: pointer;
    border-radius: 4px;
    box-shadow: 0 0 15px rgba(229,9,20,0.5);
    transition: all 0.2s;
    letter-spacing: 1px;
    width: 100%;
    max-width: 340px;
    min-height: 48px;
}}
button.btn-light:hover {{
    background: #ff1a1a;
    box-shadow: 0 0 22px rgba(255,30,30,0.9);
    transform: scale(1.02);
}}

#status {{
    text-align: center;
    font-family: 'VT323', monospace;
    font-size: 1.3rem;
    color: #ff8888;
    min-height: 28px;
    margin-top: 8px;
    letter-spacing: 1.5px;
}}
</style>
</head>
<body>

<div id="wall">
    <div class="row-container" id="row1"></div>
    <div class="row-container" id="row2"></div>
    <div class="row-container" id="row3"></div>
</div>

<div id="status">TAP BUTTON BELOW TO COMMUNICATE</div>

<div class="controls">
    <button class="btn-light" onclick="spellMessage('{config.CHRISTMAS_WALL_MESSAGE}')">✨ CLICK ME TO SPELL BIRTHDAY MESSAGE</button>
</div>

<script>
const rows = [
    {{ id: 'row1', letters: ['A','B','C','D','E','F','G','H'] }},
    {{ id: 'row2', letters: ['I','J','K','L','M','N','O','P','Q'] }},
    {{ id: 'row3', letters: ['R','S','T','U','V','W','X','Y','Z'] }}
];

const colors = ['red', 'yellow', 'blue', 'green', 'purple', 'orange'];
const letterMap = {{}};

let audioCtxWall = null;
function playBeep(freq = 440, duration = 0.25) {{
    try {{
        if (!audioCtxWall) {{
            audioCtxWall = new (window.AudioContext || window.webkitAudioContext)();
        }}
        if (audioCtxWall.state === 'suspended') audioCtxWall.resume();
        const osc = audioCtxWall.createOscillator();
        const gain = audioCtxWall.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(freq, audioCtxWall.currentTime);
        gain.gain.setValueAtTime(0.08, audioCtxWall.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtxWall.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtxWall.destination);
        osc.start();
        osc.stop(audioCtxWall.currentTime + duration);
    }} catch(e) {{}}
}}

let colorIdx = 0;
rows.forEach(r => {{
    const rowEl = document.getElementById(r.id);
    r.letters.forEach(char => {{
        const block = document.createElement('div');
        block.className = 'char-block';
        block.id = 'char-' + char;

        const bulb = document.createElement('div');
        const color = colors[colorIdx % colors.length];
        colorIdx++;
        bulb.className = `bulb bulb-${{color}}`;
        bulb.id = 'bulb-' + char;

        const letter = document.createElement('div');
        letter.className = 'letter';
        letter.innerText = char;

        block.appendChild(bulb);
        block.appendChild(letter);
        rowEl.appendChild(block);

        letterMap[char] = {{ block, bulb, freq: 220 + (char.charCodeAt(0) - 65) * 20 }};
    }});
}});

let isPlayingWall = false;

function lightLetter(char, duration = 550) {{
    return new Promise(resolve => {{
        const upper = char.toUpperCase();
        if (letterMap[upper]) {{
            const {{ block, bulb, freq }} = letterMap[upper];
            bulb.classList.add('active');
            block.classList.add('lit');
            playBeep(freq, duration / 1000);

            setTimeout(() => {{
                bulb.classList.remove('active');
                block.classList.remove('lit');
                resolve();
            }}, duration);
        }} else {{
            setTimeout(resolve, duration);
        }}
    }});
}}

async function spellMessage(text) {{
    if (isPlayingWall) return;
    isPlayingWall = true;
    const status = document.getElementById('status');
    status.innerText = "TRANSMISSION INCOMING...";
    
    const clean = text.trim();
    for (let i = 0; i < clean.length; i++) {{
        const ch = clean[i];
        if (ch === ' ') {{
            await new Promise(r => setTimeout(r, 350));
        }} else {{
            status.innerText = "LIGHTING: " + ch.toUpperCase();
            await lightLetter(ch, 500);
            await new Promise(r => setTimeout(r, 140));
        }}
    }}

    status.innerText = "MESSAGE: " + clean.toUpperCase() + " 🧇❤️";
    isPlayingWall = false;
}}
</script>
</body>
</html>
"""
components.html(lights_html, height=480, scrolling=False)

# ==============================================================================
# CHAPTER 2: HAWKINS LAB CLASSIFIED DOSSIER
# ==============================================================================
st.markdown("""
<div class="chapter-divider">
    <span class="chapter-badge">CHAPTER 2</span>
</div>
<div class="chapter-heading">HAWKINS NATIONAL LAB: SUBJECT PROFILE</div>
<div class="chapter-caption">Recovered documents from Dr. Brenner's subterranean facility.</div>
""", unsafe_allow_html=True)

dossier_photo = resolve_image_url(getattr(config, "MADAMJI_PHOTO_B64", "assets/madamji.jpg"))
dossier_fallback = getattr(config, "MADAMJI_PHOTO_B64", "")
dossier_onerror = f'onerror="this.onerror=null; this.src=\'{dossier_fallback}\';"' if dossier_fallback else ""

# Responsive Dossier Layout
col_photo, col_info = st.columns([1, 1.4], vertical_alignment="center")

with col_photo:
    st.markdown(
        f'<div style="background: #181517; border: 2px dashed #E50914; padding: 12px; border-radius: 6px; text-align: center; margin-bottom: 15px;">'
        f'<img src="{dossier_photo}" {dossier_onerror} alt="{config.FULL_NAME}" style="width: 100%; max-height: 320px; object-fit: cover; border-radius: 4px; filter: contrast(1.05);">'
        f'<div style="font-family: \'VT323\', monospace; font-size: 1.35rem; color: #ff5555; margin-top: 8px;">SUBJECT IDENTIFIER: {config.LAB_DOSSIER["subject_id"]}</div>'
        f'<div style="font-family: \'Cinzel\', serif; font-size: 1.05rem; color: #ccc;">{config.FULL_NAME}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

with col_info:
    powers_html = "".join([f"<li style='margin-bottom: 4px;'>{p}</li>" for p in config.LAB_DOSSIER["powers"]])
    st.markdown(
        f'<div class="dossier-card">'
        f'<div style="font-family: \'VT323\'; color: #E50914; font-size: 1.25rem; margin-bottom: 6px;">★ TOP SECRET / HAWKINS ARCHIVES</div>'
        f'<h3 style="font-family: \'Cinzel\', serif; color: #E50914; margin: 0 0 8px 0; font-size: 1.35rem;">{config.LAB_DOSSIER["codename"]}</h3>'
        f'<p style="font-size: 0.95rem; margin-bottom: 8px;"><strong>Party Status:</strong> <span style="color: #46d369;">{config.LAB_DOSSIER["friendship_status"]}</span></p>'
        f'<p style="font-size: 0.95rem; margin-bottom: 6px;"><strong>Superpowers:</strong></p>'
        f'<ul style="font-size: 0.9rem; padding-left: 20px; color: #ccc;">{powers_html}</ul>'
        f'<p style="font-size: 0.95rem; margin-top: 8px;"><strong>Weakness:</strong> <span style="color: #ff9999;">{config.LAB_DOSSIER["weakness"]}</span></p>'
        f'<p style="font-size: 0.95rem;"><strong>Threat to Boredom:</strong> <span style="color: #ff3333; font-weight: bold;">{config.LAB_DOSSIER["threat_to_boredom"]}</span></p>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown("<div style='font-family: Bebas Neue; font-size: 1.25rem; color: #ddd; margin: 15px 0 8px 0;'>📊 FRIENDSHIP POWER INDEX</div>", unsafe_allow_html=True)
m_c1, m_c2, m_c3 = st.columns(3)
with m_c1:
    st.metric(label="Cuteness", value="101%", delta="Off the Charts")
with m_c2:
    st.metric(label="Humor & Wit", value="99.9%", delta="Lethal")
with m_c3:
    st.metric(label="Inside Joke Sync", value="∞", delta="Instant")

# ==============================================================================
# CHAPTER 3: HOPPER'S THREE-INCH LETTER
# ==============================================================================
st.markdown("""
<div class="chapter-divider">
    <span class="chapter-badge">CHAPTER 3</span>
</div>
<div class="chapter-heading">HOPPER'S THREE-INCH LETTER</div>
<div class="chapter-caption">A heart-to-heart from Chief Hopper. Because friends don't lie.</div>
""", unsafe_allow_html=True)

formatted_letter = config.HEARTFELT_LETTER.strip().replace("\n", "<br>")

st.markdown(f'<div class="hopper-letter">{formatted_letter}</div>', unsafe_allow_html=True)
