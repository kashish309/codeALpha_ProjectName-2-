"""Real Gemstones FAQ Chatbot.

An intentionally small, local FAQ chatbot using NLTK and scikit-learn.
"""

import re
from typing import Dict, List

import nltk
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Download the two small NLTK resources needed by this app on first run.
@st.cache_resource
def prepare_nltk() -> set[str]:
    nltk.download("stopwords", quiet=True)
    # Newer NLTK releases use punkt_tab; older releases use punkt.
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    return set(stopwords.words("english"))


STOP_WORDS = prepare_nltk()


FAQS: List[Dict[str, str]] = [
    {
        "question": "How can I identify a real gemstone?",
        "answer": "Start with a trusted gemologist or an independent laboratory report. Examine the stone under magnification for natural inclusions, check that its properties match the claimed gem, and ask for clear disclosure of treatments or lab creation. Home tests alone are not proof of authenticity.",
        "topic": "Identification",
    },
    {
        "question": "How can I tell if a diamond is real?",
        "answer": "The most reliable method is a report from a respected gemological laboratory. A jeweler can also test thermal and optical properties with professional equipment. Fog, scratch, and newspaper tests are unreliable and can damage a stone or setting.",
        "topic": "Diamond",
    },
    {
        "question": "What is a real ruby?",
        "answer": "Ruby is the red variety of the mineral corundum. Its red color comes mainly from chromium, and it ranks 9 on the Mohs hardness scale. Natural rubies can contain inclusions, and many are heat-treated, so treatment disclosure matters.",
        "topic": "Ruby",
    },
    {
        "question": "How can I identify a real ruby?",
        "answer": "A ruby should be evaluated by its color, inclusions, refractive properties, and any evidence of treatment. Because natural, lab-created, and treated rubies can look alike, a qualified gemologist or lab report is the safest way to identify it.",
        "topic": "Ruby",
    },
    {
        "question": "What is a real emerald?",
        "answer": "Emerald is the green variety of the mineral beryl. Its color is usually caused by chromium or vanadium. Most natural emeralds have visible inclusions—often called a garden—and many are treated with oils or resins to improve apparent clarity.",
        "topic": "Emerald",
    },
    {
        "question": "How can I identify a real emerald?",
        "answer": "Identification considers color, inclusions, refractive properties, and treatment. A natural emerald may have characteristic internal features, but appearance alone cannot reliably separate natural from lab-created material. Use a qualified gemologist for confirmation.",
        "topic": "Emerald",
    },
    {
        "question": "What is zircon?",
        "answer": "Zircon is a natural mineral that occurs in many colors, including blue, golden, red, and colorless. It has strong brilliance and fire and is not the same mineral as diamond or cubic zirconia.",
        "topic": "Zircon",
    },
    {
        "question": "Is zircon the same as diamond?",
        "answer": "No. Zircon is a natural gemstone with different chemical composition and physical properties from diamond. Colorless zircon can resemble diamond because of its brilliance, but a gemologist can distinguish them with testing.",
        "topic": "Zircon",
    },
    {
        "question": "What is the difference between zircon and cubic zirconia?",
        "answer": "Zircon is a natural mineral. Cubic zirconia is a human-made crystalline material commonly used as a diamond alternative. They have different composition, durability, optical properties, and value.",
        "topic": "Zircon",
    },
    {
        "question": "What is the difference between natural and synthetic gemstones?",
        "answer": "A natural gemstone forms in nature, while a synthetic or lab-created gemstone is made by people but has essentially the same chemical composition and crystal structure as its natural counterpart. Synthetic does not mean fake; it should simply be disclosed accurately.",
        "topic": "Natural vs synthetic",
    },
    {
        "question": "Can gemstones be treated?",
        "answer": "Yes. Common treatments include heating, oiling, fracture filling, dyeing, and irradiation. Treatments can improve color or clarity and are common in the trade. Always ask what treatment was used because it can affect care, durability, and value.",
        "topic": "Treatments",
    },
    {
        "question": "How should I take care of my gemstone?",
        "answer": "Store each stone separately, keep it away from harsh chemicals and sudden temperature changes, and clean it with a soft cloth and mild soapy water unless a professional says otherwise. Some treated or delicate gems should not go in an ultrasonic cleaner.",
        "topic": "Care",
    },
]


def preprocess(text: str) -> str:
    """Lowercase, clean, tokenize, and remove English stopwords."""
    cleaned = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
    tokens = word_tokenize(cleaned)
    return " ".join(token for token in tokens if token not in STOP_WORDS)


@st.cache_resource
def build_search_index() -> tuple[TfidfVectorizer, object]:
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([preprocess(faq["question"]) for faq in FAQS])
    return vectorizer, matrix


def answer_question(question: str, threshold: float = 0.20) -> tuple[str, float, str | None]:
    """Return the best answer, score, and matched topic."""
    if not question.strip():
        return "Please enter a question about real gemstones.", 0.0, None

    vectorizer, faq_matrix = build_search_index()
    question_vector = vectorizer.transform([preprocess(question)])
    scores = cosine_similarity(question_vector, faq_matrix)[0]
    best_index = int(scores.argmax())
    best_score = float(scores[best_index])

    if best_score < threshold:
        return (
            "I couldn't find a suitable FAQ for that question. Try asking about diamonds, rubies, emeralds, zircon, gemstone identification, treatments, or care.",
            best_score,
            None,
        )
    return FAQS[best_index]["answer"], best_score, FAQS[best_index]["topic"]


st.set_page_config(page_title="Real Gemstones FAQ", page_icon="💎", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: #0b1020; }
    [data-testid="stHeader"] { background: transparent; }
    .hero { padding: 1.5rem 0 0.75rem; }
    .eyebrow { color: #a78bfa; letter-spacing: .14em; text-transform: uppercase; font-size: .72rem; font-weight: 700; }
    .hero h1 { color: #f8fafc; font-size: 2.35rem; margin: .25rem 0 .4rem; }
    .hero p { color: #aab4cc; font-size: 1rem; max-width: 620px; }
    [data-testid="stChatMessage"] { border: 1px solid rgba(148, 163, 184, .16); border-radius: 16px; padding: .65rem 1rem; margin: .65rem 0; }
    [data-testid="stSidebar"] { background: #11182d; }
    .topic-chip { display: inline-block; background: #202a49; color: #c4b5fd; border-radius: 999px; padding: .35rem .65rem; margin: .2rem .15rem 0 0; font-size: .78rem; }
    </style>
    <div class="hero">
      <div class="eyebrow">GemGuide AI · trusted basics</div>
      <h1>💎 Real Gemstones FAQ Chatbot</h1>
      <p>Ask simple questions about identifying, buying, caring for, and understanding real gemstones.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Explore topics")
    st.caption("This local chatbot matches your question to the closest FAQ using TF-IDF and cosine similarity.")
    for topic in ["Diamond", "Ruby", "Emerald", "Zircon", "Natural vs synthetic", "Identification", "Treatments", "Care"]:
        st.markdown(f'<span class="topic-chip">{topic}</span>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**Try asking**")
    st.caption("How can I tell if a diamond is real?\n\nWhat is the difference between zircon and cubic zirconia?")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! Ask me anything about real gemstones, from identification to care."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("topic"):
            st.caption(f"Matched topic: {message['topic']} · confidence {message['score']:.0%}")

if question := st.chat_input("Ask about diamonds, rubies, emeralds, zircon..."):
    st.session_state.messages.append({"role": "user", "content": question})
    response, score, topic = answer_question(question)
    st.session_state.messages.append({"role": "assistant", "content": response, "score": score, "topic": topic})
    st.rerun()
