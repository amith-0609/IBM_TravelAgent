import json
from typing import Any, Optional

import streamlit as st

from ibm_watsonx_orchestrate.client.chat.run_client import RunClient
from ibm_watsonx_orchestrate.client.threads.threads_client import ThreadsClient
from ibm_watsonx_orchestrate.client.utils import instantiate_client
from ibm_watsonx_orchestrate.cli.commands.agents.agents_helper import get_agent_id_by_name


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONSTANTS
# ============================================================

AGENT_NAME = "TravelMate_AI_2909XT"


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_SESSION_STATE = {
    "travel_request": None,
    "agent_response": None,
    "raw_agent_response": None,
    "thread_id": None,
    "run_id": None,
}

for key, value in DEFAULT_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# LOAD STREAMLIT SECRETS
# ============================================================

def get_secret(name: str) -> str:
    try:
        value = str(st.secrets[name]).strip()
    except Exception as exc:
        raise RuntimeError(
            f"Missing required Streamlit secret: {name}"
        ) from exc

    if not value:
        raise RuntimeError(
            f"Streamlit secret is empty: {name}"
        )

    return value


try:
    WATSONX_API_KEY = get_secret(
        "WATSONX_ORCHESTRATE_API_KEY"
    )

    WATSONX_URL = get_secret(
        "WATSONX_ORCHESTRATE_URL"
    ).rstrip("/")

    AGENT_ID = get_secret(
        "WATSONX_ORCHESTRATE_AGENT_ID"
    )

except RuntimeError as error:
    st.error(str(error))

    st.code(
        '''
WATSONX_ORCHESTRATE_API_KEY = "YOUR_API_KEY"

WATSONX_ORCHESTRATE_URL = "YOUR_FULL_IBM_SERVICE_URL"

WATSONX_ORCHESTRATE_AGENT_ID = "4b59a47d-a573-414d-8fb9-d323b89c95dd"
        '''.strip(),
        language="toml",
    )

    st.stop()


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                135deg,
                #e8f4fd 0%,
                #f5fbff 50%,
                #e8f4fd 100%
            );
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #0f4c81;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #2d6a9f;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }

    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f4c81;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #1a8fe3;
        padding-left: 0.6rem;
    }

    .success-box {
        background: #d9f7e8;
        border: 1px solid #45c486;
        border-radius: 10px;
        padding: 1rem;
        color: #146c43;
        margin: 1rem 0;
    }

    .stButton > button {
        background:
            linear-gradient(
                90deg,
                #0f4c81,
                #1a8fe3
            );

        color: white;
        font-size: 1.05rem;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        width: 100%;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f4c81 0%,
                #1a6fa8 100%
            );
    }

    [data-testid="stSidebar"] * {
        color: #e8f4fd !important;
    }

    .footer {
        text-align: center;
        color: #6b9ab8;
        font-size: 0.82rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #d0e8f5;
    }

    /* ============================================================
   TRAVELMATE AI — FRONTEND CONTRAST & READABILITY FIX
   ============================================================ */

/* Main app background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #eef8ff !important;
    color: #17324d !important;
}

/* Default text throughout main content area */
[data-testid="stMain"] p,
[data-testid="stMain"] span,
[data-testid="stMain"] label,
[data-testid="stMain"] li {
    color: #17324d;
}

/* Main headings */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4 {
    color: #124f80 !important;
}

/* ============================================================
   ITINERARY OUTPUT
   This is the main fix for the invisible response text.
   ============================================================ */

.itinerary-output,
.itinerary-output p,
.itinerary-output span,
.itinerary-output div,
.itinerary-output li,
.itinerary-output strong,
.itinerary-output em {
    color: #17324d !important;
    opacity: 1 !important;
    visibility: visible !important;
}

.itinerary-output {
    background: #ffffff !important;
    border: 1px solid #b8d9ef !important;
    border-radius: 16px !important;
    padding: 28px 32px !important;
    margin-top: 14px !important;
    box-shadow: 0 8px 24px rgba(20, 79, 128, 0.08) !important;
    line-height: 1.75 !important;
}

.itinerary-output h1,
.itinerary-output h2,
.itinerary-output h3,
.itinerary-output h4 {
    color: #0f4f7d !important;
    font-weight: 700 !important;
}

.itinerary-output strong {
    color: #0d4168 !important;
    font-weight: 700 !important;
}

/* ============================================================
   STREAMLIT MARKDOWN RESPONSE
   Covers agent output rendered through st.markdown().
   ============================================================ */

[data-testid="stMain"] [data-testid="stMarkdownContainer"] {
    color: #17324d !important;
}

[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li {
    color: #17324d !important;
    opacity: 1 !important;
}

[data-testid="stMain"] [data-testid="stMarkdownContainer"] strong {
    color: #0d4168 !important;
}

/* ============================================================
   FORM INPUTS
   ============================================================ */

[data-testid="stMain"] input,
[data-testid="stMain"] textarea {
    color: #17324d !important;
    background-color: #ffffff !important;
    caret-color: #17324d !important;
}

[data-testid="stMain"] input::placeholder,
[data-testid="stMain"] textarea::placeholder {
    color: #6c8296 !important;
    opacity: 1 !important;
}

/* Select boxes */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #17324d !important;
}

/* ============================================================
   INFO / SUCCESS / ERROR BOXES
   ============================================================ */

[data-testid="stAlert"] {
    color: #17324d !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    color: inherit !important;
}

/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #c5deee !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary span {
    color: #17324d !important;
    font-weight: 600 !important;
}

/* ============================================================
   CODE / RAW IBM RESPONSE
   ============================================================ */

[data-testid="stCode"] {
    background-color: #172334 !important;
}

[data-testid="stCode"] code,
[data-testid="stCode"] pre {
    color: #eef6ff !important;
}

/* ============================================================
   BUTTONS
   ============================================================ */

[data-testid="stMain"] .stButton > button,
[data-testid="stMain"] .stFormSubmitButton > button {
    background: #163e63 !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 700 !important;
}

[data-testid="stMain"] .stButton > button:hover,
[data-testid="stMain"] .stFormSubmitButton > button:hover {
    background: #0f5688 !important;
    color: #ffffff !important;
}

/* ============================================================
   LINKS
   ============================================================ */

[data-testid="stMain"] a {
    color: #0969a8 !important;
    font-weight: 600;
}

/* ============================================================
   TEXT SELECTION
   ============================================================ */

::selection {
    background: #b9dcf5;
    color: #102f49;
}

/* ============================================================
   TRAVELMATE AI — FINAL BUTTON, EXPANDER & ALERT CONTRAST FIX
   ============================================================ */


/* ------------------------------------------------------------
   1. GENERATE MY TRIP / FORM SUBMIT BUTTON
   ------------------------------------------------------------ */

div[data-testid="stFormSubmitButton"] > button,
div[data-testid="stFormSubmitButton"] button,
.stFormSubmitButton > button {
    background: linear-gradient(
        135deg,
        #123f66 0%,
        #17689e 100%
    ) !important;

    color: #ffffff !important;
    border: 1px solid #0f3658 !important;
    border-radius: 10px !important;

    font-weight: 700 !important;
    font-size: 1rem !important;

    min-height: 48px !important;

    box-shadow:
        0 5px 14px rgba(18, 63, 102, 0.22) !important;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        background 0.18s ease !important;
}


/* Force every element inside the submit button to white */
div[data-testid="stFormSubmitButton"] button *,
.stFormSubmitButton > button * {
    color: #ffffff !important;
}


/* Hover */
div[data-testid="stFormSubmitButton"] > button:hover,
div[data-testid="stFormSubmitButton"] button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(
        135deg,
        #0f5688 0%,
        #1678b8 100%
    ) !important;

    color: #ffffff !important;

    transform: translateY(-1px) !important;

    box-shadow:
        0 8px 20px rgba(18, 63, 102, 0.28) !important;
}


/* Focus */
div[data-testid="stFormSubmitButton"] > button:focus,
.stFormSubmitButton > button:focus {
    color: #ffffff !important;

    border-color: #2388ca !important;

    box-shadow:
        0 0 0 3px rgba(35, 136, 202, 0.22) !important;
}


/* ------------------------------------------------------------
   2. NORMAL STREAMLIT BUTTONS
   Example: Test IBM agent connection
   ------------------------------------------------------------ */

div[data-testid="stButton"] > button,
.stButton > button {
    background: #155b8f !important;
    color: #ffffff !important;

    border: 1px solid #104a76 !important;
    border-radius: 9px !important;

    font-weight: 650 !important;
}


/* Force inner text/icons white */
div[data-testid="stButton"] button *,
.stButton > button * {
    color: #ffffff !important;
}


div[data-testid="stButton"] > button:hover,
.stButton > button:hover {
    background: #0e4c79 !important;
    color: #ffffff !important;
}


/* ------------------------------------------------------------
   3. RAW IBM API RESPONSE EXPANDER
   ------------------------------------------------------------ */

div[data-testid="stExpander"] {
    background: #ffffff !important;

    border:
        1px solid #a9cee5 !important;

    border-radius: 12px !important;

    box-shadow:
        0 4px 14px rgba(20, 79, 128, 0.07) !important;

    overflow: hidden !important;
}


/* Expander header */
div[data-testid="stExpander"] details > summary {
    background: #e4f3fc !important;

    color: #123f66 !important;

    padding: 12px 16px !important;

    font-weight: 700 !important;
}


/* Every element inside expander header */
div[data-testid="stExpander"] details > summary *,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary p {
    color: #123f66 !important;
    opacity: 1 !important;
}


/* Hover */
div[data-testid="stExpander"] details > summary:hover {
    background: #d4ebf9 !important;
}


/* Expander body */
div[data-testid="stExpander"] details > div {
    background: #ffffff !important;
    color: #17324d !important;
}


/* Body text */
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] li,
div[data-testid="stExpander"] label {
    color: #17324d !important;
}


/* ------------------------------------------------------------
   4. INFO ALERT BOXES
   ------------------------------------------------------------ */

div[data-testid="stAlert"] {
    border-radius: 10px !important;
}


/* Force visible text inside every alert */
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div,
div[data-testid="stAlert"] strong {
    color: #17324d !important;
    opacity: 1 !important;
}


/* Info boxes */
div[data-testid="stAlert"][data-baseweb="notification"] {
    color: #17324d !important;
}


/* ------------------------------------------------------------
   5. BLUE INFO BOXES
   ------------------------------------------------------------ */

div[data-testid="stAlert"] {
    background-color: #dceffc !important;

    border:
        1px solid #a8d2eb !important;
}


/* ------------------------------------------------------------
   6. SUCCESS BOXES
   ------------------------------------------------------------ */

div[data-testid="stAlert"] svg {
    opacity: 1 !important;
}


/* ------------------------------------------------------------
   7. RAW JSON / CODE INSIDE EXPANDER
   ------------------------------------------------------------ */

div[data-testid="stExpander"]
div[data-testid="stJson"] {
    background: #172334 !important;
    border-radius: 8px !important;
}


div[data-testid="stExpander"]
div[data-testid="stCode"] {
    background: #172334 !important;
    border-radius: 8px !important;
}


div[data-testid="stExpander"]
div[data-testid="stCode"] pre,

div[data-testid="stExpander"]
div[data-testid="stCode"] code {
    color: #f2f7fb !important;
}


/* ------------------------------------------------------------
   8. DOWNLOAD BUTTONS, IF USED LATER
   ------------------------------------------------------------ */

div[data-testid="stDownloadButton"] > button {
    background: #155b8f !important;
    color: #ffffff !important;

    border: none !important;
    border-radius: 9px !important;

    font-weight: 650 !important;
}


div[data-testid="stDownloadButton"] button * {
    color: #ffffff !important;
}


/* ------------------------------------------------------------
   9. PREVENT WHITE TEXT FROM LEAKING INTO MAIN CONTENT
   ------------------------------------------------------------ */

section.main p,
section.main li,
section.main label,

[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] label {
    color: #17324d;
}


/* Keep button text white despite global main-content rules */
[data-testid="stMain"] button,
[data-testid="stMain"] button p,
[data-testid="stMain"] button span {
    color: #ffffff !important;
}

/* ============================================================
   GENERATE MY TRIP BUTTON — CONTRAST FIX
   ============================================================ */

div[data-testid="stFormSubmitButton"] button {
    background: #163f63 !important;
    color: #ffffff !important;
    border: 2px solid #163f63 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    min-height: 50px !important;
    box-shadow: 0 5px 14px rgba(22, 63, 99, 0.22) !important;
}

/* Force the button's text and all inner elements to white */
div[data-testid="stFormSubmitButton"] button *,
div[data-testid="stFormSubmitButton"] button p,
div[data-testid="stFormSubmitButton"] button span {
    color: #ffffff !important;
    opacity: 1 !important;
}

/* Hover */
div[data-testid="stFormSubmitButton"] button:hover {
    background: #0f5688 !important;
    color: #ffffff !important;
    border-color: #0f5688 !important;
    box-shadow: 0 7px 18px rgba(15, 86, 136, 0.28) !important;
}

/* Keep text white on hover and focus */
div[data-testid="stFormSubmitButton"] button:hover *,
div[data-testid="stFormSubmitButton"] button:focus *,
div[data-testid="stFormSubmitButton"] button:active * {
    color: #ffffff !important;
    opacity: 1 !important;
}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# IBM WATSONX ORCHESTRATE — OFFICIAL ADK INTEGRATION
# ============================================================

def extract_text_from_content(content: Any) -> Optional[str]:
    """Extract readable text from an IBM watsonx Orchestrate message content value."""

    if isinstance(content, str):
        cleaned = content.strip()
        return cleaned or None

    if isinstance(content, list):
        collected = []

        for item in content:
            if isinstance(item, str) and item.strip():
                collected.append(item.strip())

            elif isinstance(item, dict):
                text = item.get("text")

                if isinstance(text, str) and text.strip():
                    collected.append(text.strip())

        if collected:
            return "\n\n".join(collected)

    return None


def call_travelmate_agent(
    travel_request: str,
) -> tuple[str, dict[str, Any], Optional[str], Optional[str]]:
    """
    Invoke TravelMate through IBM's official watsonx Orchestrate ADK.

    This follows the same mechanism used by the successfully tested command:
        orchestrate chat ask --agent-name TravelMate_AI_2909XT "..."

    Returns:
        agent_text,
        raw_response,
        thread_id,
        run_id
    """

    try:
        # Resolve the exact registered agent through the active IBM environment.
        resolved_agent_id = get_agent_id_by_name(AGENT_NAME)

        if not resolved_agent_id:
            raise RuntimeError(
                f"Could not find IBM watsonx Orchestrate agent '{AGENT_NAME}'. "
                "Make sure the 'travelmate' environment is active."
            )

        # Safety check: warn through an exception if the discovered agent differs
        # from the ID configured in Streamlit secrets.
        if AGENT_ID and str(resolved_agent_id) != str(AGENT_ID):
            raise RuntimeError(
                "The active IBM environment resolved a different TravelMate agent ID.\n\n"
                f"Resolved ID: {resolved_agent_id}\n"
                f"Configured ID: {AGENT_ID}"
            )

        run_client = instantiate_client(RunClient)
        threads_client = instantiate_client(ThreadsClient)

        run_response = run_client.create_run(
            message=travel_request,
            agent_id=resolved_agent_id,
            thread_id=None,
            capture_logs=False,
        )

        if not isinstance(run_response, dict):
            raise RuntimeError(
                "IBM returned an unexpected create_run response:\n\n"
                f"{run_response!r}"
            )

        thread_id = run_response.get("thread_id")
        run_id = run_response.get("run_id")

        if not thread_id or not run_id:
            raise RuntimeError(
                "IBM did not return the required thread_id and run_id.\n\n"
                f"Response: {run_response!r}"
            )

        run_status = run_client.wait_for_run_completion(run_id)

        if isinstance(run_status, dict):
            status = str(run_status.get("status", "")).strip().lower()

            if status in {"failed", "error", "cancelled", "canceled"}:
                raise RuntimeError(
                    "The TravelMate agent run did not complete successfully.\n\n"
                    f"Run ID: {run_id}\n"
                    f"Thread ID: {thread_id}\n"
                    f"Run status: {run_status!r}"
                )

        thread_messages_response = threads_client.get_thread_messages(thread_id)

        if isinstance(thread_messages_response, list):
            messages = thread_messages_response

        elif isinstance(thread_messages_response, dict):
            data = thread_messages_response.get("data")
            messages = data if isinstance(data, list) else []

        else:
            messages = []

        assistant_message = None

        for message in reversed(messages):
            if isinstance(message, dict) and message.get("role") == "assistant":
                assistant_message = message
                break

        if assistant_message is None:
            raise RuntimeError(
                "The IBM agent run completed, but no assistant response was found.\n\n"
                f"Run ID: {run_id}\n"
                f"Thread ID: {thread_id}\n"
                f"Messages: {messages!r}"
            )

        agent_text = extract_text_from_content(
            assistant_message.get("content")
        )

        if not agent_text:
            raise RuntimeError(
                "The IBM TravelMate agent returned an empty or unsupported response.\n\n"
                f"Assistant message: {assistant_message!r}"
            )

        raw_response = {
            "agent_name": AGENT_NAME,
            "agent_id": resolved_agent_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "run_response": run_response,
            "run_status": run_status,
            "assistant_message": assistant_message,
        }

        return (
            agent_text,
            raw_response,
            thread_id,
            run_id,
        )

    except Exception as exc:
        raise RuntimeError(
            "TravelMate AI could not complete the request through the official "
            "IBM watsonx Orchestrate ADK.\n\n"
            f"Error type: {type(exc).__name__}\n"
            f"Details: {exc}"
        ) from exc


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ✈️ TravelMate AI")
    st.markdown("---")

    st.markdown("### 🛠️ Powered By")

    st.markdown(
        "**🤖 IBM watsonx Orchestrate**"
    )

    st.markdown(
        "Agentic AI backbone that orchestrates "
        "travel planning tools and sub-agents."
    )

    st.markdown("**☁️ IBM Cloud**")

    st.markdown(
        "Enterprise-grade cloud infrastructure "
        "hosting the TravelMate agent."
    )

    st.markdown("**🔵 IBM Bob**")

    st.markdown(
        "AI-powered development assistant used "
        "while building TravelMate AI."
    )

    st.markdown(
        "**📚 RAG Knowledge Base**"
    )

    st.markdown(
        "Retrieval-Augmented Generation for "
        "contextual travel knowledge."
    )

    st.markdown("**🔍 Exa Web Search**")

    st.markdown(
        "Real-time search capability for current "
        "travel information when configured."
    )

    st.markdown("---")

    st.markdown("### 🔌 Connection")

    st.success(
        "IBM credentials loaded securely"
    )

    st.caption(
        f"Agent ID: {AGENT_ID}"
    )

    if st.session_state.run_id:

        st.caption("Latest IBM run ID:")

        st.code(
            st.session_state.run_id,
            language=None,
        )


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-title">'
    '✈️ TravelMate AI'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-subtitle">
        Your Intelligent Agentic AI Travel
        Planning Assistant
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ABOUT
# ============================================================

with st.expander(
    "ℹ️ About TravelMate AI",
    expanded=False,
):

    st.markdown(
        """
**TravelMate AI** is an agentic AI-powered
travel planning assistant built with
**IBM watsonx Orchestrate**.

The application sends your structured travel
preferences to the deployed TravelMate AI agent
and displays the generated itinerary directly
inside Streamlit.

It can generate:

- 🗺️ Day-by-day itineraries
- 🏨 Accommodation suggestions
- 🚕 Transportation guidance
- 🍽️ Local food recommendations
- 💰 Budget breakdowns
- 📸 Hidden gems
- ⚠️ Travel and safety considerations
        """
    )


st.markdown("---")


# ============================================================
# TRAVEL FORM
# ============================================================

with st.form("travel_form"):

    st.markdown(
        '<div class="section-header">'
        '🌍 Where are you headed?'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        destination = st.text_input(
            "Destination *",
            placeholder="e.g. Goa, India",
        )

    with col2:

        origin = st.text_input(
            "Starting Location / Origin",
            placeholder="e.g. Mumbai, India",
        )


    st.markdown(
        '<div class="section-header">'
        '📅 Trip Details'
        '</div>',
        unsafe_allow_html=True,
    )

    col3, col4 = st.columns(2)

    with col3:

        duration = st.number_input(
            "Trip Duration (days) *",
            min_value=1,
            max_value=365,
            value=7,
            step=1,
        )

    with col4:

        num_travelers = st.number_input(
            "Number of Travelers *",
            min_value=1,
            max_value=100,
            value=1,
            step=1,
        )


    st.markdown(
        '<div class="section-header">'
        '💰 Budget'
        '</div>',
        unsafe_allow_html=True,
    )

    col5, col6 = st.columns([3, 1])

    with col5:

        budget = st.number_input(
            "Total Budget *",
            min_value=1.0,
            value=1000.0,
            step=100.0,
            format="%.2f",
        )

    with col6:

        currency = st.selectbox(
            "Currency",
            [
                "INR",
                "USD",
                "EUR",
                "GBP",
                "JPY",
                "AUD",
                "Other",
            ],
        )


    st.markdown(
        '<div class="section-header">'
        '🧳 Travel Preferences'
        '</div>',
        unsafe_allow_html=True,
    )

    col7, col8 = st.columns(2)

    with col7:

        travel_type = st.selectbox(
            "Travel Type",
            [
                "Solo",
                "Couple",
                "Family",
                "Friends",
                "Student",
                "Business",
            ],
        )

    with col8:

        travel_style = st.selectbox(
            "Travel Style",
            [
                "Budget",
                "Moderate",
                "Luxury",
                "Adventure",
                "Relaxation",
                "Cultural",
                "Eco-friendly",
            ],
            index=1,
        )


    st.markdown(
        '<div class="section-header">'
        '🎯 Travel Interests'
        '</div>',
        unsafe_allow_html=True,
    )

    interests = st.multiselect(
        "Select your interests",
        [
            "History",
            "Local Food",
            "Photography",
            "Beaches",
            "Adventure",
            "Nature",
            "Shopping",
            "Nightlife",
            "Culture",
            "Wildlife",
            "Wellness",
            "Technology",
        ],
        default=[
            "Local Food",
            "Culture",
        ],
    )


    st.markdown(
        '<div class="section-header">'
        '📝 Special Requirements'
        '</div>',
        unsafe_allow_html=True,
    )

    special_requirements = st.text_area(
        "Any special needs, preferences, or requests?",
        placeholder=(
            "e.g. Vegetarian food, wheelchair access, "
            "anniversary trip..."
        ),
        height=120,
    )


    submitted = st.form_submit_button(
        "🚀 Generate My Trip with TravelMate AI"
    )


# ============================================================
# PROCESS SUBMISSION
# ============================================================

if submitted:

    if not destination.strip():

        st.error(
            "Please enter a destination."
        )

    else:

        interests_text = (
            ", ".join(interests)
            if interests
            else "Not specified"
        )

        origin_text = (
            origin.strip()
            if origin.strip()
            else "Not specified"
        )

        requirements_text = (
            special_requirements.strip()
            if special_requirements.strip()
            else "None"
        )

        travel_request = f"""
You are TravelMate AI, an intelligent agentic
travel planning assistant.

Create a complete, realistic, personalized travel
itinerary based on these traveler requirements.

TRAVELER REQUIREMENTS

Destination: {destination.strip()}
Origin: {origin_text}
Trip duration: {duration} day(s)
Number of travelers: {num_travelers}
Total budget: {currency} {budget:,.2f}
Travel type: {travel_type}
Travel style: {travel_style}
Interests: {interests_text}
Special requirements: {requirements_text}

REQUIRED OUTPUT

Please provide:

1. A concise trip overview.
2. A complete day-by-day itinerary.
3. Morning, afternoon, and evening activities.
4. Accommodation suggestions appropriate for the budget.
5. Local transportation guidance.
6. Local food and restaurant recommendations.
7. An estimated budget breakdown.
8. Important practical travel tips.
9. Relevant safety considerations.
10. Hidden gems when appropriate.

IMPORTANT

- Respect the traveler's stated total budget.
- Tailor recommendations to the stated travel style.
- Tailor recommendations to the stated interests.
- Clearly identify estimates.
- Avoid claiming exact live prices when unavailable.
- Produce a polished, detailed, readable itinerary.
""".strip()

        st.session_state.travel_request = (
            travel_request
        )

        st.session_state.agent_response = None
        st.session_state.raw_agent_response = None
        st.session_state.thread_id = None
        st.session_state.run_id = None

        with st.spinner(
            "🤖 TravelMate AI is creating your "
            "personalized itinerary..."
        ):

            try:

                (
                    agent_text,
                    raw_response,
                    thread_id,
                    run_id,
                ) = call_travelmate_agent(
                    travel_request
                )

                st.session_state.agent_response = (
                    agent_text
                )

                st.session_state.raw_agent_response = (
                    raw_response
                )

                st.session_state.thread_id = (
                    thread_id
                )

                st.session_state.run_id = (
                    run_id
                )

                st.success(
                    "✅ TravelMate AI generated your "
                    "itinerary successfully!"
                )

            except Exception as error:

                st.error(
                    "TravelMate AI could not complete "
                    "the request."
                )

                st.exception(error)


# ============================================================
# DISPLAY STRUCTURED REQUEST
# ============================================================

if st.session_state.travel_request:

    with st.expander(
        "📋 View request sent to TravelMate AI",
        expanded=False,
    ):

        st.code(
            st.session_state.travel_request,
            language=None,
        )


# ============================================================
# DISPLAY AGENT RESPONSE
# ============================================================

if st.session_state.agent_response:

    st.markdown("---")

    st.markdown(
        '<div class="section-header">'
        '🤖 Your TravelMate AI Itinerary'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        st.session_state.agent_response
    )


# ============================================================
# RAW API RESPONSE
# ============================================================

if st.session_state.raw_agent_response:

    with st.expander(
        "🔧 Raw IBM API response",
        expanded=False,
    ):

        st.json(
            st.session_state.raw_agent_response
        )


# ============================================================
# CONNECTION DIAGNOSTICS
# ============================================================

st.markdown("---")

with st.expander(
    "🔌 IBM watsonx Orchestrate connection details",
    expanded=False,
):

    st.write(
        "**Agent name:**",
        AGENT_NAME,
    )

    st.write(
        "**Agent ID:**",
        AGENT_ID,
    )

    st.write(
        "**Configured service URL:**",
        WATSONX_URL,
    )

    st.info(
        "Agent requests use IBM's official watsonx Orchestrate ADK "
        "and the currently active Orchestrate environment."
    )

    if st.session_state.thread_id:
        st.write("**Latest thread ID:**")
        st.code(
            st.session_state.thread_id,
            language=None,
        )

    if st.session_state.run_id:
        st.write("**Latest run ID:**")
        st.code(
            st.session_state.run_id,
            language=None,
        )

    if st.button("Test IBM agent connection"):

        with st.spinner(
            "Testing the active IBM watsonx Orchestrate environment..."
        ):

            try:
                resolved_agent_id = get_agent_id_by_name(AGENT_NAME)

                if not resolved_agent_id:
                    raise RuntimeError(
                        f"Agent '{AGENT_NAME}' was not found."
                    )

                st.success(
                    "IBM watsonx Orchestrate connection succeeded."
                )

                st.caption(
                    f"Found {AGENT_NAME} with agent ID "
                    f"{resolved_agent_id}."
                )

            except Exception as error:
                st.error(
                    "IBM watsonx Orchestrate connection test failed."
                )
                st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Built with IBM watsonx Orchestrate,
        IBM Cloud, IBM Bob, and Streamlit.
    </div>
    """,
    unsafe_allow_html=True,
)