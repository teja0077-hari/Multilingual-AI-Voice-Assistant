import streamlit as st
from stt import transcribe_audio
from llm import generate_response
from tts import generate_speech
from datetime import datetime


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Multilingual AI Voice Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "conversation_history": [],
    "saved_audio": None,
    "selected_language": "Telugu",
    "recorder_version": 0,
    "assistant_response": None,
    "generated_audio": None,
    "recognized_text": None,
    "last_language": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# CLEAR CONVERSATION
# ==========================================

def clear_conversation():

    st.session_state.conversation_history = []
    st.session_state.saved_audio = None
    st.session_state.assistant_response = None
    st.session_state.generated_audio = None
    st.session_state.recognized_text = None
    st.session_state.last_language = None

    st.session_state.recorder_version += 1


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #F6F7FC;
    color: #172033;
}

.block-container {
    max-width: 1420px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hide sidebar */

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}

/* Headings */

h1, h2, h3 {
    color: #172033 !important;
    font-weight: 700 !important;
}

/* Paragraphs */

p {
    color: #475467;
}

/* Buttons */

.stButton > button {
    background: linear-gradient(110deg, #6546E8, #3978F6);
    color: white !important;
    border: none;
    border-radius: 11px;
    min-height: 45px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #5535D5, #2865E5);
    box-shadow: 0 5px 15px rgba(85, 75, 220, 0.18);
    transform: translateY(-1px);
}

/* Download buttons */

.stDownloadButton > button {
    border-radius: 10px;
    border: 1px solid #D9D6FE;
    color: #6546E8;
    background: #F5F3FF;
    font-weight: 600;
    min-height: 43px;
}

/* Audio player */

[data-testid="stAudio"] {
    width: 100%;
}

/* Text areas */

textarea {
    background-color: white !important;
    color: #172033 !important;
    border-radius: 10px !important;
}

/* Cards */

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border: 1px solid #E8EAF2;
    border-radius: 16px;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Metrics */

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E8EAF2;
    padding: 15px;
    border-radius: 12px;
}

/* Responsive layout */

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER AND LANGUAGE SELECTOR
# ==========================================

header_left, header_right = st.columns(
    [3, 1.2],
    vertical_alignment="center"
)

with header_left:

    st.caption("YOUR PERSONAL AI COMPANION")

    st.title("🎙️ Multilingual AI Voice Assistant")

    st.write(
        "Speak naturally. Understand intelligently. "
        "Get AI responses in your preferred language."
    )

with header_right:

    st.markdown("**🌐 Select Language**")

    language = st.selectbox(
        "Choose your language",
        ["Telugu", "Hindi", "English"],
        key="selected_language",
        label_visibility="collapsed"
    )


st.write("")

# ==========================================
# SERVICE STATUS
# ==========================================

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "🎧 Speech Recognition",
        "Gnani Prisma"
    )

with metric2:
    st.metric(
        "🧠 AI Intelligence",
        "Groq LLM"
    )

with metric3:
    st.metric(
        "🔊 Voice Generation",
        "Gnani Timbre"
    )


# ==========================================
# WORKSPACE HEADER
# ==========================================

st.divider()

workspace_left, workspace_right = st.columns([3, 1])

with workspace_left:

    st.header("💬 Conversation Workspace")

    st.caption(
        f"Your assistant is ready to communicate in {language}."
    )

with workspace_right:

    st.button(
        "🗑️ Clear Conversation",
        on_click=clear_conversation,
        use_container_width=True
    )


# ==========================================
# MAIN WORKSPACE
# ==========================================

input_col, response_col = st.columns(
    [0.8, 1.2],
    gap="large"
)


# ==========================================
# LEFT SIDE - VOICE INPUT
# ==========================================

with input_col:

    with st.container(border=True):

        st.subheader("🎤 Voice Input")

        st.caption(
            f"Record your question in {language}."
        )

        audio = st.audio_input(
            "Start recording",
            key=f"voice_recorder_{st.session_state.recorder_version}"
        )

        if audio is not None:

            st.success("Recording captured!")

            st.audio(
                audio.getvalue(),
                format="audio/wav"
            )

            if st.button(
                "💾 Save Recording",
                type="primary",
                use_container_width=True
            ):

                st.session_state.saved_audio = audio.getvalue()

                st.session_state.last_language = language

                st.session_state.recognized_text = None
                st.session_state.assistant_response = None
                st.session_state.generated_audio = None

                st.success("Recording saved successfully!")

        else:

            st.info(
                "Record your voice using the audio recorder above."
            )

        # Saved recording section

        if st.session_state.saved_audio is not None:

            st.divider()

            st.download_button(
                "⬇️ Download Recording",
                data=st.session_state.saved_audio,
                file_name="my_voice.wav",
                mime="audio/wav",
                use_container_width=True
            )

            st.divider()

            st.subheader("🧠 Speech Recognition")

            if st.button(
                "Convert Voice to Text",
                type="primary",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "Gnani Prisma is recognizing your speech..."
                    ):

                        recognized_text = transcribe_audio(
                            st.session_state.saved_audio,
                            st.session_state.last_language
                        )

                        st.session_state.recognized_text = recognized_text

                    st.success("Speech recognized successfully!")

                except Exception as error:

                    st.error(
                        f"Transcription failed: {error}"
                    )

        # Display recognized text

        if st.session_state.recognized_text:

            st.divider()

            st.subheader("📝 Recognized Text")

            st.text_area(
                "Your spoken words",
                value=st.session_state.recognized_text,
                height=150,
                disabled=True
            )


# ==========================================
# RIGHT SIDE - AI RESPONSE
# ==========================================

with response_col:

    with st.container(border=True):

        st.subheader("🤖 AI Assistant")

        st.caption(
            "Your intelligent assistant is ready to answer."
        )

        if st.session_state.recognized_text:

            st.success("Your question is ready for AI processing.")

            if st.button(
                "✨ Generate AI Response",
                type="primary",
                use_container_width=True
            ):

                try:

                    user_text = st.session_state.recognized_text.strip()

                    response_language = st.session_state.last_language

                    if not user_text:
                        raise ValueError(
                            "No recognized text found."
                        )

                    # Generate text response

                    with st.spinner(
                        "AI is thinking..."
                    ):

                        answer = generate_response(
                            user_text,
                            response_language,
                            st.session_state.conversation_history
                        )

                        st.session_state.assistant_response = answer

                        st.session_state.conversation_history.append({
                            "language": response_language,
                            "question": user_text,
                            "answer": answer,
                            "time": datetime.now().strftime(
                                "%d-%m-%Y %I:%M %p"
                            )
                        })

                    st.success("AI response generated!")

                    # Generate voice response

                    try:

                        with st.spinner(
                            "Generating AI voice response..."
                        ):

                            audio_bytes = generate_speech(
                                answer,
                                response_language
                            )

                            st.session_state.generated_audio = audio_bytes

                        st.success("AI voice generated successfully!")

                    except Exception as tts_error:

                        st.session_state.generated_audio = None

                        st.warning(
                            "Text answer is ready, but voice generation "
                            f"failed: {tts_error}"
                        )

                except Exception as error:

                    st.error(
                        f"AI response failed: {error}"
                    )

        else:

            st.info(
                "Your AI answer will appear here after speech recognition."
            )

        # ==================================
        # DISPLAY AI ANSWER
        # ==================================

        if st.session_state.assistant_response:

            st.divider()

            st.subheader("💬 AI Answer")

            with st.container(border=True):

                st.markdown(
                    st.session_state.assistant_response
                )

        # ==================================
        # DISPLAY AI VOICE
        # ==================================

        if st.session_state.generated_audio:

            st.divider()

            st.subheader("🔊 AI Voice Response")

            st.caption(
                "Listen to your assistant's spoken answer."
            )

            st.audio(
                st.session_state.generated_audio,
                format="audio/wav"
            )

            st.download_button(
                "⬇️ Download AI Voice Response",
                data=st.session_state.generated_audio,
                file_name="ai_response.wav",
                mime="audio/wav",
                use_container_width=True
            )


# ==========================================
# CONVERSATION HISTORY
# ==========================================

st.divider()

history_left, history_right = st.columns([3, 1])

with history_left:

    st.header("📚 Conversation History")

    st.caption(
        "Review your previous questions and AI responses."
    )

with history_right:

    st.metric(
        "Total Conversations",
        len(st.session_state.conversation_history)
    )


if st.session_state.conversation_history:

    for index, conversation in enumerate(
        reversed(st.session_state.conversation_history),
        start=1
    ):

        with st.expander(
            f"💬 Conversation {index} — "
            f"{conversation['language']} | {conversation['time']}"
        ):

            st.markdown("**You asked:**")

            st.write(conversation["question"])

            st.markdown("**AI response:**")

            st.write(conversation["answer"])

else:

    with st.container(border=True):

        st.info(
            "No conversations yet. Record your voice to start chatting!"
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

footer_left, footer_right = st.columns(2)

with footer_left:

    st.caption(
        "🎙️ Multilingual AI Voice Assistant"
    )

with footer_right:

    st.caption(
        "Powered by Python • Streamlit • Gnani AI • Groq"
    )