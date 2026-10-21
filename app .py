import html
import streamlit as st
from google import genai

st.set_page_config(
    page_title="PostCraft AI | LinkedIn Post Generator",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Premium visual design
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #17233f;
        --muted: #65718b;
        --line: #e5eaf4;
        --blue: #536dfe;
        --violet: #8257e5;
        --panel: #ffffff;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 7% 0%, rgba(116, 139, 255, 0.10), transparent 26rem),
            radial-gradient(circle at 95% 8%, rgba(174, 119, 255, 0.10), transparent 24rem),
            #f6f8fc;
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(246, 248, 252, 0.75);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu, footer { visibility: hidden; }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.25rem;
        color: #34415f;
        font-size: 0.94rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    .brand-mark {
        width: 34px;
        height: 34px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 11px;
        color: white;
        font-size: 1.15rem;
        background: linear-gradient(135deg, #526dfe 0%, #8c5de8 100%);
        box-shadow: 0 7px 18px rgba(91, 95, 235, 0.24);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.2rem 2.35rem 2.15rem;
        border-radius: 25px;
        color: #ffffff;
        background: linear-gradient(118deg, #172747 0%, #253c70 47%, #5941a8 100%);
        box-shadow: 0 18px 45px rgba(35, 48, 92, 0.16);
        margin-bottom: 1.7rem;
    }

    .hero:after {
        content: "";
        position: absolute;
        right: -75px;
        top: -145px;
        width: 360px;
        height: 360px;
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 50%;
        box-shadow: 0 0 0 38px rgba(255,255,255,0.035), 0 0 0 78px rgba(255,255,255,0.025);
        pointer-events: none;
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        border: 1px solid rgba(255,255,255,0.24);
        border-radius: 999px;
        padding: 6px 11px;
        background: rgba(255,255,255,0.09);
        color: #e7eaff;
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0.045em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .hero h1 {
        position: relative;
        z-index: 1;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 4vw, 3.15rem);
        line-height: 1.13;
        letter-spacing: -0.055em;
        color: #ffffff;
        font-weight: 800;
        margin: 0 0 0.8rem 0;
        max-width: 730px;
    }

    .hero p {
        position: relative;
        z-index: 1;
        max-width: 690px;
        color: #dce4ff;
        font-size: 1.03rem;
        line-height: 1.7;
        margin: 0;
    }

    .hero-pills {
        position: relative;
        z-index: 1;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 1.35rem;
    }

    .hero-pill {
        color: #f4f5ff;
        border: 1px solid rgba(255,255,255,0.19);
        background: rgba(255,255,255,0.08);
        border-radius: 9px;
        padding: 7px 10px;
        font-size: 0.79rem;
    }

    .section-heading {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        margin: 0 0 0.25rem 0;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 0.92rem;
        margin: 0 0 1rem 0;
        line-height: 1.6;
    }

    .stForm, [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--line) !important;
        border-radius: 19px !important;
    }

    [data-testid="stForm"] {
        background: rgba(255,255,255,0.94);
        border: 1px solid var(--line) !important;
        padding: 1.35rem 1.45rem 1.15rem;
        box-shadow: 0 8px 28px rgba(37, 53, 91, 0.045);
    }

    [data-testid="stWidgetLabel"] p {
        color: #34415f;
        font-weight: 650;
        font-size: 0.88rem;
    }

    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div,
    [data-baseweb="textarea"] > div {
        background: #fbfcff !important;
        border-color: #dfe5f1 !important;
        border-radius: 11px !important;
    }

    [data-baseweb="input"] > div:focus-within,
    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="textarea"] > div:focus-within {
        border-color: #7484ff !important;
        box-shadow: 0 0 0 3px rgba(100, 116, 255, 0.12) !important;
    }

    textarea, input {
        color: #1b2742 !important;
    }

    .field-note {
        color: #7a849a;
        font-size: 0.8rem;
        line-height: 1.5;
        margin-top: -0.45rem;
        margin-bottom: 0.85rem;
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        border: 0 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        background: linear-gradient(100deg, #536dfe 0%, #7657ec 100%) !important;
        font-weight: 750 !important;
        min-height: 3rem;
        box-shadow: 0 8px 18px rgba(92, 99, 237, 0.22);
        transition: transform 0.16s ease, box-shadow 0.16s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 11px 23px rgba(92, 99, 237, 0.28);
    }

    [data-testid="stDownloadButton"] > button {
        border: 1px solid #dfe5f1 !important;
        border-radius: 11px !important;
        min-height: 2.8rem;
        color: #34415f !important;
        background: #ffffff !important;
        font-weight: 650 !important;
    }

    .mini-stat {
        height: 100%;
        padding: 1rem 1.05rem;
        border: 1px solid #e5eaf4;
        border-radius: 15px;
        background: rgba(255,255,255,0.86);
    }

    .mini-stat-label {
        color: #77829a;
        font-size: 0.76rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.055em;
        margin-bottom: 0.35rem;
    }

    .mini-stat-value {
        color: #263555;
        font-family: 'Manrope', sans-serif;
        font-size: 0.97rem;
        font-weight: 800;
    }

    .preview-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin: 1.8rem 0 0.9rem 0;
    }

    .preview-title {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        margin: 0;
    }

    .preview-badge {
        color: #4f5fd5;
        background: #eeefff;
        border: 1px solid #dedfff;
        font-size: 0.76rem;
        font-weight: 700;
        padding: 6px 10px;
        border-radius: 999px;
        white-space: nowrap;
    }

    .post-preview {
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        background: #ffffff;
        border: 1px solid #e5eaf4;
        border-radius: 18px;
        padding: 1.45rem 1.55rem;
        color: #27334d;
        font-size: 0.98rem;
        line-height: 1.85;
        box-shadow: 0 8px 28px rgba(37, 53, 91, 0.045);
    }

    .preview-footnote {
        color: #7b8599;
        font-size: 0.82rem;
        line-height: 1.6;
        margin-top: 0.75rem;
    }

    .footer-note {
        margin-top: 2.5rem;
        padding-top: 1.1rem;
        border-top: 1px solid #e5eaf4;
        text-align: center;
        color: #8a94a8;
        font-size: 0.79rem;
    }

    @media (max-width: 700px) {
        .block-container { padding-top: 1rem; }
        .hero { padding: 1.6rem 1.3rem; border-radius: 19px; }
        [data-testid="stForm"] { padding: 1rem; }
        .post-preview { padding: 1.1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Brand and hero header
# -----------------------------
st.markdown(
    """
    <div class="brand-row">
        <span class="brand-mark">✦</span>
        <span>PostCraft <span style="color:#6b63e8">AI</span></span>
    </div>
    <section class="hero">
        <div class="hero-kicker">✦ AI-powered writing studio</div>
        <h1>Make your next LinkedIn post stand out.</h1>
        <p>Turn your ideas, lessons, and experiences into thoughtful professional content — ready for you to review, personalize, and share.</p>
        <div class="hero-pills">
            <span class="hero-pill">✧ Human-sounding writing</span>
            <span class="hero-pill">◎ Your audience, your tone</span>
            <span class="hero-pill">↗ Built for LinkedIn</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Read the API key from Streamlit Community Cloud Secrets.
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
except Exception:
    api_key = ""

st.markdown('<div class="section-heading">Create your post</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Tell us what you want to say. Customize the details, then let AI help you shape the first draft.</div>',
    unsafe_allow_html=True,
)

with st.form("linkedin_post_form", border=True):
    left, right = st.columns(2, gap="large")

    with left:
        topic = st.text_area(
            "✍️  What is your post about?",
            placeholder="Example: My journey learning AI and web development",
            height=135,
            help="Choose one clear idea, lesson, milestone, or question.",
        )
        audience = st.selectbox(
            "👥  Target audience",
            [
                "Students",
                "Software Developers",
                "AI Professionals",
                "Recruiters",
                "Entrepreneurs",
                "General Professionals",
            ],
        )
        tone = st.selectbox(
            "🎙️  Writing tone",
            [
                "Conversational",
                "Professional",
                "Educational",
                "Storytelling",
                "Thought-provoking",
                "Personal and Authentic",
            ],
            index=0,
        )

    with right:
        length = st.selectbox(
            "📏  Post length",
            [
                "Short (80-120 words)",
                "Medium (150-250 words)",
                "Long (250-350 words)",
            ],
            index=1,
        )
        language = st.selectbox("🌐  Language", ["English", "Urdu", "Roman Urdu"])
        context = st.text_area(
            "💡  Your experience or extra details (optional)",
            placeholder="What did you learn, build, overcome, or discover?",
            height=135,
            help="Add real details to make the post more personal. The AI should not invent experiences for you.",
        )

    st.markdown(
        '<div class="field-note">Tip: A specific topic and a little real-world context usually produce a stronger, more authentic post.</div>',
        unsafe_allow_html=True,
    )
    submitted = st.form_submit_button("✦  Generate my LinkedIn post", type="primary", use_container_width=True)

# -----------------------------
# Generation logic
# -----------------------------
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic for your LinkedIn post.")
    elif not api_key:
        st.error(
            'Gemini API key is not configured. Open your Streamlit app → Settings → Secrets and add: GEMINI_API_KEY = "your-key-here"'
        )
    else:
        prompt = f"""You are an expert LinkedIn content writer.

Generate exactly ONE engaging LinkedIn post using the details below.

TOPIC: {topic.strip()}
TARGET AUDIENCE: {audience}
TONE: {tone}
LENGTH: {length}
LANGUAGE: {language}
PERSONAL EXPERIENCE: {context.strip() or "Not provided"}

WRITING RULES:
1. Start with a compelling hook.
2. Use short, readable paragraphs.
3. Provide useful insights and practical examples.
4. Sound natural, human, and professional.
5. Do not invent personal experiences, achievements, or statistics.
6. Use emojis sparingly.
7. End with a relevant question or call to action.
8. Include 3-5 relevant hashtags.
9. Follow the selected language and requested length.
10. Return only the finished LinkedIn post.
"""
        try:
            with st.spinner("Crafting your post… finding the right hook and flow"):
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-flash-lite-latest",
                    contents=prompt,
                )
                post = (response.text or "").strip()

            if post:
                st.session_state["generated_linkedin_post"] = post
            else:
                st.error("Gemini returned an empty response. Please try again.")
        except Exception as exc:
            st.error(
                f"Could not generate the post ({type(exc).__name__}). Please check your API key, model access, and API quota."
            )
            st.caption(str(exc))

# -----------------------------
# Result area
# -----------------------------
generated_post = st.session_state.get("generated_linkedin_post", "")
if generated_post:
    st.markdown(
        '''<div class="preview-header">
            <div class="preview-title">Your post is ready</div>
            <span class="preview-badge">✦ AI draft · Ready to review</span>
        </div>''',
        unsafe_allow_html=True,
    )

    safe_post = html.escape(generated_post)
    st.markdown(f'<div class="post-preview">{safe_post}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="preview-footnote">Before posting, review the draft and personalize any details so the final post reflects your own voice and experience.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("✎  Edit or copy the post text", expanded=False):
        edited_post = st.text_area(
            "Your post text",
            value=generated_post,
            height=320,
            key="editable_linkedin_post",
            help="You can make final edits here. Select the text and copy it, or download it below.",
        )
        download_col, info_col = st.columns([1, 2], vertical_alignment="center")
        with download_col:
            st.download_button(
                "⬇  Download .txt",
                data=edited_post,
                file_name="linkedin_post.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with info_col:
            st.caption("To copy: click inside the text, press Ctrl+A, then Ctrl+C (or use your device's select-and-copy option).")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("↻  Create another post", use_container_width=False):
        st.session_state.pop("generated_linkedin_post", None)
        st.session_state.pop("editable_linkedin_post", None)
        st.rerun()

st.markdown(
    '<div class="footer-note">Made for clearer ideas and better professional storytelling · Powered by Gemini AI</div>',
    unsafe_allow_html=True,
)
