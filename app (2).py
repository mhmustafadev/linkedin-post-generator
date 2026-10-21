import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI LinkedIn Post Generator",
    page_icon="✍️",
    layout="wide",
)

st.title("✍️ AI LinkedIn Post Generator")
st.write("Create one engaging LinkedIn post with Gemini AI.")

try:
    api_key = st.secrets.get("GEMINI_API_KEY", "").strip()
except Exception:
    api_key = ""

with st.form("linkedin_post_form"):
    left, right = st.columns(2)

    with left:
        topic = st.text_area(
            "Post topic",
            placeholder="Example: My journey learning AI and web development",
            height=110,
        )
        audience = st.selectbox(
            "Target audience",
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
            "Writing tone",
            [
                "Conversational",
                "Professional",
                "Educational",
                "Storytelling",
                "Thought-provoking",
                "Personal and Authentic",
            ],
        )

    with right:
        length = st.selectbox(
            "Post length",
            [
                "Short (80-120 words)",
                "Medium (150-250 words)",
                "Long (250-350 words)",
            ],
            index=1,
        )
        language = st.selectbox("Language", ["English", "Urdu", "Roman Urdu"])
        context = st.text_area(
            "Personal experience (optional)",
            placeholder="What did you learn, build, or discover?",
            height=110,
        )

    submitted = st.form_submit_button("Generate LinkedIn Post", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic for your LinkedIn post.")
    elif not api_key:
        st.error(
            "Gemini API key is not configured. Open your Streamlit app's Settings → Secrets "
            "and add: GEMINI_API_KEY = \"your-key-here\""
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
            with st.spinner("Generating your LinkedIn post..."):
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
            st.error(f"Could not generate the post ({type(exc).__name__}). Please check your API key, model access, and API quota.")
            st.caption(str(exc))

if st.session_state.get("generated_linkedin_post"):
    st.subheader("Your generated LinkedIn post")
    generated_post = st.session_state["generated_linkedin_post"]
    st.text_area("Select and copy your post", value=generated_post, height=360)
    st.download_button(
        "Download post as a text file",
        data=generated_post,
        file_name="linkedin_post.txt",
        mime="text/plain",
    )
