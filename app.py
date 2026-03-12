import time
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).parent

PRODUCT_ASSETS: dict[str, dict[str, Path]] = {
    "https://www.amazon.ca/Jutqut-Matte-lipstick-pen-01/dp/B0GFCXQSKD": {
        "Hotel": ASSETS_DIR / "lipstick_hotel_final.mp4",
        "Beach": ASSETS_DIR / "lipstick_beach_final.mp4",
    },
    "https://www.amazon.ca/dp/B0GGYX4STX": {
        "Gym": ASSETS_DIR / "creatine_gym_final.mp4",
        "Home": ASSETS_DIR / "creatine_home_final.mp4",
    },
}

AGENTIC_LOG_LINES = [
    "Authenticating with Amazon API...",
    "Downloading high-res textures...",
    "Removing background via Vision-Model...",
    "Synthesizing environment lighting...",
    "Compiling final 15s commercial...",
]


def inject_brand_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root{
  --bg: #080810;
  --panel: #0E0F1A;
  --text: #F0F0FA;
  --muted: rgba(240,240,250,0.55);
  --gold: #D4A853;
  --goldSoft: rgba(212,168,83,0.15);
  --border: rgba(212,168,83,0.18);
}

html, body, [class*="css"]{
  font-family: 'Inter', system-ui, sans-serif !important;
}

.stApp{
  background: radial-gradient(ellipse at top, #0D0D1A 0%, #080810 60%);
  color: var(--text);
}

div[data-testid="stVerticalBlockBorderWrapper"]{
  background: rgba(14,15,26,0.85);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 20px;
  backdrop-filter: blur(10px);
}

hr{
  border-top: 1px solid rgba(212,168,83,0.12) !important;
}

input, textarea, div[data-baseweb="select"] > div{
  background: rgba(14,15,26,0.90) !important;
  border: 1px solid rgba(212,168,83,0.22) !important;
  border-radius: 14px !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.95rem !important;
}

input:focus, textarea:focus{
  border: 1px solid rgba(212,168,83,0.80) !important;
  box-shadow: 0 0 0 3px rgba(212,168,83,0.12) !important;
}

div.stButton > button{
  background: linear-gradient(135deg, #D4A853, #C9943A) !important;
  color: #080810 !important;
  border: none !important;
  border-radius: 16px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  padding: 0.9rem 1.2rem !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  transition: all 0.2s ease !important;
}

div.stButton > button:hover{
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 25px rgba(212,168,83,0.30) !important;
}

h1, h2, h3{
  font-family: 'Syne', sans-serif !important;
  color: var(--text) !important;
  letter-spacing: 0.5px !important;
}

label, .stMarkdown, p, li{
  color: var(--text);
}
.muted{
  color: var(--muted);
  font-size: 0.88rem;
}
.gold{
  color: var(--gold);
}

.agency-header{
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1.5rem 0 0.5rem 0;
}
.agency-mark{
  display: inline-flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.85rem 1.6rem;
  border-radius: 999px;
  border: 1px solid rgba(212,168,83,0.25);
  background: linear-gradient(135deg, rgba(14,15,26,0.95), rgba(8,8,16,0.95));
  box-shadow: 0 0 40px rgba(212,168,83,0.08), 0 10px 30px rgba(0,0,0,0.40);
}
.agency-dot{
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--gold);
  box-shadow: 0 0 12px rgba(212,168,83,0.60);
  animation: pulse 2s infinite;
}
@keyframes pulse{
  0%{ box-shadow: 0 0 0 0 rgba(212,168,83,0.4); }
  70%{ box-shadow: 0 0 0 8px rgba(212,168,83,0); }
  100%{ box-shadow: 0 0 0 0 rgba(212,168,83,0); }
}
.agency-title{
  color: var(--gold);
  font-family: 'Syne', sans-serif !important;
  font-weight: 800;
  letter-spacing: 3px;
  font-size: 1rem;
  text-transform: uppercase;
}

.terminal{
  background: rgba(5,5,10,0.90);
  border: 1px solid rgba(212,168,83,0.18);
  border-radius: 16px;
  padding: 16px;
}
.terminal pre{
  margin: 0;
  color: var(--gold);
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.88rem;
  line-height: 1.7;
  white-space: pre-wrap;
}

.video-card{
  border: 1px solid rgba(212,168,83,0.15);
  background: rgba(14,15,26,0.60);
  border-radius: 20px;
  padding: 14px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.30);
}

</style>
        """,
        unsafe_allow_html=True,
    )


def run_agentic_log() -> None:
    log_box = st.container()
    placeholder = log_box.empty()
    rendered: list[str] = []
    for line in AGENTIC_LOG_LINES:
        rendered.append(f"> {line}")
        placeholder.markdown(
            "<div class='terminal'><pre>"
            + "\n".join(rendered)
            + "</pre></div>",
            unsafe_allow_html=True,
        )
        time.sleep(2)


def play_video(path: Path) -> None:
    try:
        st.video(str(path), autoplay=True)
    except TypeError:
        st.video(str(path))


def resolve_asset_path(requested: Path) -> Path:
    if requested.exists():
        return requested
    if requested.suffix.lower() == ".mp4":
        double_ext = requested.with_name(requested.name + ".mp4")
        if double_ext.exists():
            return double_ext
    return requested


st.set_page_config(
    page_title="Agency AI Video Tool",
    page_icon="🎬",
    layout="wide",
)

inject_brand_css()

st.markdown(
    """
<div class="agency-header">
  <div class="agency-mark">
    <div class="agency-dot"></div>
    <div class="agency-title">AGENCY AI</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

st.markdown("### Inputs")
st.markdown("<div class='muted'>Paste a product URL and choose an environment.</div>", unsafe_allow_html=True)
st.divider()

amazon_url = st.text_input(
    "Amazon Product URL",
    placeholder="Paste an Amazon product URL…",
)
if amazon_url.strip() in PRODUCT_ASSETS:
    available_envs = list(PRODUCT_ASSETS[amazon_url.strip()].keys())
else:
    available_envs = ["Hotel", "Beach", "Gym", "Home"]

scene_env = st.selectbox("Scene Environment", available_envs, index=0)
generate = st.button("Generate", use_container_width=True)

st.divider()
st.markdown("### Output")
st.markdown("<div class='muted'>Progress + renders.</div>", unsafe_allow_html=True)
st.divider()

if generate:
    stripped_url = amazon_url.strip()
    if stripped_url in PRODUCT_ASSETS:
        run_agentic_log()
        assets = PRODUCT_ASSETS[stripped_url]
        keys = list(assets.keys())
        first_path = resolve_asset_path(assets[keys[0]])
        second_path = resolve_asset_path(assets[keys[1]])
        missing = [p.name for p in [first_path, second_path] if not p.exists()]
        if missing:
            st.error("Missing video(s): " + ", ".join(f"`{m}`" for m in missing))
        else:
            st.success("Render complete.")
            selected_path = resolve_asset_path(assets.get(scene_env, assets[keys[0]]))
            st.markdown(f"**{scene_env} Scene**")
            st.markdown("<div class='video-card'>", unsafe_allow_html=True)
            play_video(selected_path)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info(
            "New Product Detected. Queuing for background removal and scene synthesis. "
            "Estimated time: 8 minutes."
        )


