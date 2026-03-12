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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root{
  --bg: #0A0A0F;
  --panel: #0E0F16;
  --panel2: #0B0C12;
  --text: #EAEAF2;
  --muted: rgba(234,234,242,0.68);
  --gold: #C9A84C;
  --goldSoft: rgba(201,168,76,0.28);
  --border: rgba(201,168,76,0.22);
}

html, body, [class*="css"]{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif !important;
}

.stApp{
  background: var(--bg);
  color: var(--text);
}

div[data-testid="stVerticalBlockBorderWrapper"]{
  background: linear-gradient(180deg, rgba(14,15,22,0.92), rgba(10,10,15,0.92));
  border: 1px solid rgba(201,168,76,0.18);
  border-radius: 16px;
  padding: 18px 18px 10px 18px;
}

hr{
  border-top: 1px solid rgba(201,168,76,0.18) !important;
}

input, textarea, div[data-baseweb="select"] > div{
  background: rgba(14,15,22,0.85) !important;
  border: 1px solid rgba(201,168,76,0.20) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  box-shadow: none !important;
}

input:focus, textarea:focus{
  outline: none !important;
  border: 1px solid rgba(201,168,76,0.70) !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.14) !important;
}

div.stButton > button{
  background: var(--gold) !important;
  color: #0A0A0F !important;
  border: 1px solid rgba(0,0,0,0.40) !important;
  border-radius: 14px !important;
  font-weight: 700 !important;
  padding: 0.85rem 1.05rem !important;
  letter-spacing: 0.3px;
}
div.stButton > button:hover{
  filter: brightness(1.02);
  box-shadow: 0 0 0 3px rgba(201,168,76,0.18);
}

label, .stMarkdown, p, li{
  color: var(--text);
}
.muted{
  color: var(--muted);
}
.gold{
  color: var(--gold);
}

.agency-header{
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0.25rem 0 0.75rem 0;
}
.agency-mark{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.75rem 1.1rem;
  border-radius: 999px;
  border: 1px solid rgba(201,168,76,0.22);
  background: linear-gradient(180deg, rgba(14,15,22,0.92), rgba(10,10,15,0.92));
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.agency-dot{
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--gold);
  box-shadow: 0 0 0 4px rgba(201,168,76,0.12);
}
.agency-title{
  color: var(--gold);
  font-weight: 800;
  letter-spacing: 2.2px;
  font-size: 0.95rem;
}

.terminal{
  background: rgba(8,8,12,0.80);
  border: 1px solid rgba(201,168,76,0.20);
  border-radius: 14px;
  padding: 14px 14px 10px 14px;
}
.terminal pre{
  margin: 0;
  color: var(--gold);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.92rem;
  line-height: 1.55;
  white-space: pre-wrap;
}

.video-card{
  border: 1px solid rgba(201,168,76,0.18);
  background: rgba(14,15,22,0.72);
  border-radius: 16px;
  padding: 12px;
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
scene_env = st.selectbox("Scene Environment", ["Hotel", "Beach", "Gym", "Home"], index=0)
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
