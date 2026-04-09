"""
Streamlit UI: editorial “mid” background (warm, textured, not white) + optional darker
mode via toggle. Step titles use HTML badges — see ``step_title``.

Future UI work — keep in mind
-----------------------------
Many users are *weak readers* and want a short path (few fields, one obvious “next”
action). When changing themes or layout:

- Keep **one strong primary action** per screen where possible.
- Prefer **short labels** and placeholders over long copy; use ``help=`` for errors only.
- **Numbered steps** should match the real order of work; don’t skip numbers.
- **Accent color** for CTAs and step badges; avoid coloring every heading.
- Streamlit + CSS has limits; heavy branding may need custom components.

Default look is **mid** (warm charcoal + noise texture). Toggle “Dark theme” goes
deeper/dimmer. Adjust hex constants below together with ``.streamlit/config.toml``.
"""

from __future__ import annotations

import streamlit as st

# --- Darker optional mode (toggle) -------------------------------------------
_DARK_BG = "#141210"
_DARK_PANEL = "#1f1c1a"
_DARK_TEXT = "#e8e4e0"
_DARK_ACCENT = "#e8967a"

# --- Mid editorial (default): warm, visible controls, not white --------------
_MID_BG = "#2a2624"
_MID_PANEL = "#3d3834"
_MID_TEXT = "#f4eee8"
_MID_MUTED = "#a89f96"
_MID_ACCENT = "#d97852"

# SVG noise tile (very subtle grain)
_NOISE_SVG = (
    "%3Csvg xmlns='http://www.w3.org/2000/svg' width='256' height='256'%3E"
    "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' "
    "numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E"
    "%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E"
)


def step_title(num: int, title: str, hint: str = "") -> str:
    """HTML for a numbered section heading (use with ``unsafe_allow_html=True``)."""
    hint_html = f'<span class="mg-step-hint"> — {hint}</span>' if hint else ""
    return (
        f'<p class="mg-step-title">'
        f'<span class="mg-step-num">{num}</span>'
        f'<span class="mg-step-label">{title}</span>{hint_html}</p>'
    )


def init_theme_state() -> None:
    if "ui_theme" not in st.session_state:
        st.session_state.ui_theme = "mid"
    elif st.session_state.ui_theme not in ("mid", "dark"):
        st.session_state.ui_theme = "mid"
    if "ui_theme_dark" not in st.session_state:
        st.session_state.ui_theme_dark = st.session_state.ui_theme == "dark"


def sync_theme_from_toggle() -> None:
    st.session_state.ui_theme = "dark" if st.session_state.get("ui_theme_dark", False) else "mid"


def render_theme_toggle_header() -> None:
    init_theme_state()
    row_left, row_right = st.columns([8, 4])
    with row_left:
        st.empty()
    with row_right:
        st.toggle(
            "Dark theme",
            key="ui_theme_dark",
            help="Even lower brightness. Default is warm mid‑tone (not white).",
        )
    sync_theme_from_toggle()


def _shared_step_and_card_css(accent: str, muted: str, panel: str, text_color: str) -> str:
    return f"""
        .mg-step-title {{
            display: flex;
            flex-wrap: wrap;
            align-items: baseline;
            gap: 0.35rem 0.5rem;
            margin: 0 0 0.6rem 0;
            font-size: 1.2rem;
            font-weight: 650;
            color: {text_color} !important;
            line-height: 1.3;
        }}
        .mg-step-num {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 1.85rem;
            height: 1.85rem;
            padding: 0 0.35rem;
            background: linear-gradient(145deg, {accent}, #b85a38);
            color: #1a120e !important;
            border-radius: 999px;
            font-weight: 800;
            font-size: 0.95rem;
            flex-shrink: 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.35);
        }}
        .mg-step-label {{ color: inherit !important; }}
        .mg-step-hint {{
            font-weight: 450;
            font-size: 0.88rem;
            color: {muted} !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: linear-gradient(165deg, rgba(70,64,59,0.5) 0%, rgba(42,38,36,0.92) 100%) !important;
            border: 1px solid rgba(232, 150, 122, 0.22) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.04) !important;
            margin-bottom: 0.85rem !important;
            padding: 0.35rem 0.5rem 0.65rem 0.5rem !important;
        }}
    """


def _css_mid() -> str:
    return f"""
        html {{ color-scheme: dark; }}
        .stApp, [data-testid="stAppViewContainer"] {{
            background-color: {_MID_BG} !important;
            background-image:
                radial-gradient(ellipse 90% 45% at 50% -15%, rgba(217, 120, 82, 0.14), transparent 55%),
                radial-gradient(ellipse 60% 40% at 100% 100%, rgba(90, 70, 60, 0.12), transparent 45%),
                url("data:image/svg+xml,{_NOISE_SVG}");
            background-attachment: fixed;
            color: {_MID_TEXT} !important;
        }}
        section[data-testid="stMain"] > div, [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        [data-testid="stHeader"] {{
            border-bottom: 1px solid rgba(255,255,255,0.06) !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {_MID_BG} !important;
        }}
        section.main h1 {{
            font-weight: 750 !important;
            letter-spacing: -0.03em;
            border-bottom: 2px solid {_MID_ACCENT};
            padding-bottom: 0.35rem;
            color: {_MID_TEXT} !important;
        }}
        section.main .stCaption {{ color: {_MID_MUTED} !important; }}
        section.main label, section.main p, section.main li {{ color: {_MID_TEXT} !important; }}
        section.main a {{ color: {_MID_ACCENT} !important; }}
        section.main [data-baseweb="input"], section.main input, section.main textarea {{
            background-color: {_MID_PANEL} !important;
            color: {_MID_TEXT} !important;
            border-color: #5c534c !important;
        }}
        section.main [data-baseweb="select"] > div {{
            background-color: {_MID_PANEL} !important;
            border-color: #5c534c !important;
        }}
        div[data-testid="stExpander"] details {{
            background-color: {_MID_PANEL} !important;
            border-color: #5c534c !important;
        }}
        div[data-testid="stAlert"] {{
            background-color: rgba(62, 57, 53, 0.9) !important;
            color: {_MID_TEXT} !important;
        }}
        div[data-testid="stDataFrame"] {{ background-color: {_MID_PANEL} !important; }}
        div[data-testid="stButton"] button[data-testid="baseButton-primary"],
        div[data-testid="stButton"] button[kind="primary"] {{
            font-weight: 650;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
        }}
        div[data-testid="stButton"] button[data-testid="baseButton-secondary"] {{
            background-color: {_MID_PANEL} !important;
            color: {_MID_TEXT} !important;
            border-color: #6b625a !important;
        }}
        section.main pre, section.main code {{
            background-color: #1e1b19 !important;
            color: #e8e2dc !important;
        }}
        section.main [data-testid="stFileUploader"] {{
            background-color: {_MID_PANEL} !important;
        }}
        {_shared_step_and_card_css(_MID_ACCENT, _MID_MUTED, _MID_PANEL, _MID_TEXT)}
    """


def _css_dark() -> str:
    return f"""
        html {{ color-scheme: dark; }}
        .stApp, [data-testid="stAppViewContainer"] {{
            background-color: {_DARK_BG} !important;
            background-image:
                radial-gradient(ellipse 80% 40% at 50% 0%, rgba(217, 120, 82, 0.08), transparent 50%),
                url("data:image/svg+xml,{_NOISE_SVG}");
            background-attachment: fixed;
            color: {_DARK_TEXT} !important;
        }}
        section[data-testid="stMain"] > div, [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        [data-testid="stHeader"] {{
            border-bottom: 1px solid #2e2a27 !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {_DARK_BG} !important;
        }}
        [data-testid="stSidebar"] * {{ color: {_DARK_TEXT} !important; }}
        section.main h1 {{
            font-weight: 750 !important;
            border-bottom: 2px solid {_DARK_ACCENT};
            padding-bottom: 0.35rem;
            color: {_DARK_TEXT} !important;
        }}
        section.main label, section.main p, section.main li, section.main span {{
            color: {_DARK_TEXT} !important;
        }}
        section.main .stCaption {{ color: #9c948c !important; }}
        section.main a, section.main a:visited {{ color: {_DARK_ACCENT} !important; }}
        section.main [data-baseweb="input"], section.main input, section.main textarea {{
            background-color: {_DARK_PANEL} !important;
            color: {_DARK_TEXT} !important;
            border-color: #4a4540 !important;
        }}
        section.main [data-baseweb="select"] > div {{
            background-color: {_DARK_PANEL} !important;
            border-color: #4a4540 !important;
        }}
        div[data-testid="stExpander"] details {{
            background-color: {_DARK_PANEL} !important;
            border-color: #4a4540 !important;
        }}
        div[data-testid="stAlert"] {{
            background-color: {_DARK_PANEL} !important;
            color: {_DARK_TEXT} !important;
            border-color: #4a4540 !important;
        }}
        div[data-testid="stDataFrame"] {{ background-color: {_DARK_PANEL} !important; }}
        div[data-testid="stButton"] button[data-testid="baseButton-primary"],
        div[data-testid="stButton"] button[kind="primary"] {{
            font-weight: 650;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            background-color: {_DARK_ACCENT} !important;
            color: #1a1512 !important;
            border: none !important;
        }}
        div[data-testid="stButton"] button[data-testid="baseButton-secondary"] {{
            background-color: {_DARK_PANEL} !important;
            color: {_DARK_TEXT} !important;
            border-color: #57534e !important;
        }}
        section.main pre, section.main code {{
            background-color: #0f0e0d !important;
            color: #d6d3d1 !important;
        }}
        section.main [data-testid="stFileUploader"] {{
            background-color: {_DARK_PANEL} !important;
        }}
        {_shared_step_and_card_css(_DARK_ACCENT, "#9c948c", _DARK_PANEL, _DARK_TEXT)}
    """


def apply_editorial_styles(theme: str | None = None) -> None:
    if theme is None:
        theme = st.session_state.get("ui_theme", "mid")
    css = _css_dark() if theme == "dark" else _css_mid()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_new_event_start_focus_if_needed() -> None:
    """
    After a successful **Add event** (any source: MTP, GA4 template, or Custom), scroll to
    step 2 and focus the first field (GA4 documentation column) so the user can add another
    event from the top.

    Call once at the **end** of the Event setup container (after that ``st.text_input``).
    """
    _focus = st.session_state.pop("_focus_new_event_start", False) or st.session_state.pop(
        "_focus_ga4_after_add", False
    )
    if not _focus:
        return
    import streamlit.components.v1 as components

    # height=1: some browsers skip scripts in 0-height iframes
    components.html(
        """
        <script>
        (function () {
          const docs = [];
          try { docs.push(window.parent.document); } catch (e) {}
          try {
            if (window.parent.parent && window.parent.parent.document) {
              docs.push(window.parent.parent.document);
            }
          } catch (e2) {}

          function findGa4DocInput(doc) {
            if (!doc || !doc.querySelectorAll) return null;
            let el = doc.querySelector(
              'input[aria-label*="GA4 event name"][aria-label*="documentation"]'
            );
            if (el) return el;
            el = doc.querySelector('input[placeholder*="generate_lead"]');
            if (el) return el;
            const labels = doc.querySelectorAll('label');
            for (const lab of labels) {
              const t = (lab.textContent || '').trim();
              if (t.indexOf('GA4 event name') !== -1 && t.indexOf('documentation') !== -1) {
                const fid = lab.getAttribute('for');
                if (fid) {
                  const byId = doc.getElementById(fid);
                  if (byId) return byId;
                }
                const inner = lab.querySelector('input');
                if (inner) return inner;
              }
            }
            return null;
          }

          for (const doc of docs) {
            const inp = findGa4DocInput(doc);
            if (inp && inp.focus) {
              try {
                inp.scrollIntoView({ block: 'center', behavior: 'smooth' });
              } catch (e) {}
              setTimeout(function () {
                try {
                  inp.focus({ preventScroll: true });
                } catch (e3) {
                  inp.focus();
                }
              }, 250);
              break;
            }
          }
        })();
        </script>
        """,
        height=1,
        width=1,
    )
