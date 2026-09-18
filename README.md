# 💎 Real Gemstones FAQ Chatbot

A beginner-friendly Streamlit chatbot that answers common questions about real gemstones. It uses a local FAQ dataset—there is no database, external AI API, or OpenAI API.
open to view (https://8hqhd7fsr8ffkq355czzkp.streamlit.app/)

## Features

- 12 FAQs covering diamonds, rubies, emeralds, zircon, identification, treatments, natural vs synthetic gems, and care
- Streamlit chat interface with chat history stored in session state
- Sidebar with gemstone topics and example questions
- Similarity threshold to avoid confidently returning an unrelated answer
- Automatically downloads the required NLTK resources on first run

## Technologies

- Python
- Streamlit
- NLTK
- scikit-learn

## How it works

1. The question is lowercased and special characters are removed.
2. NLTK tokenizes the text and removes English stopwords.
3. `TfidfVectorizer` converts the cleaned FAQ questions and user question into numerical vectors.
4. Cosine similarity compares the user question to every FAQ.
5. The highest-scoring FAQ is returned only when it passes the similarity threshold.

## Project structure

```text
real-gemstone-chatbot/
├── app.py
├── requirements.txt
└── README.md
```

## Installation and running

From this directory, run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## Deploy for a permanent public link

`http://localhost:8501/` works only while the app is running on your computer. To publish the chatbot with a permanent public URL:

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Sign in with the GitHub account that owns this repository.
3. Select **Create app** and choose `kashish309/codeALpha_ProjectName-2-`.
4. Set the branch to `main` and the main file to `app.py`.
5. Click **Deploy**.

Streamlit will provide a public URL ending in `streamlit.app` and automatically redeploy the app when you push updates to GitHub.

## Example questions

- How can I identify a real gemstone?
- How can I tell if a diamond is real?
- What is a real ruby?
- What is a real emerald?
- What is zircon?
- Is zircon the same as diamond?
- What is the difference between zircon and cubic zirconia?
- Can gemstones be treated?
- How should I take care of my gemstone?
