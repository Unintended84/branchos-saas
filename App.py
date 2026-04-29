import streamlit as st
from openai import OpenAI
import requests

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="ScenarioOS",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
<div style="text-align:center;padding:10px;">
<h1>🧠 ScenarioOS</h1>
<p style="color:gray;font-size:16px;">
A civilization simulation engine modeling how global systems evolve after major events.
</p>
</div>
""", unsafe_allow_html=True)

st.info("""
ScenarioOS simulates interacting global systems:

• Health  
• Governments  
• Society  
• Economy  
• Technology  
• Environment  
• Geopolitics  

It does not answer questions like a chatbot.
It simulates world evolution.
""")

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# ---------------- INPUT ----------------

user_input = st.text_area(
    "Enter a global event",
    placeholder="Pandemic starts in Italy... UFO lands in London... Cure for cancer discovered...",
    height=140
)

# ---------------- LIVE NEWS ----------------

def get_news(query):
    try:
        url=f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=ArtList&format=json"
        r=requests.get(url,timeout=8)

        if r.status_code!=200:
            return "No live news available."

        data=r.json()
        articles=data.get("articles",[])[:4]

        if not articles:
            return "No recent news found."

        return "\n".join(
            [f"- {a.get('title')}" for a in articles]
        )

    except:
        return "News fetch unavailable."


# ---------------- ONE-CALL CIVILIZATION SIM ----------------

def simulate_world(event):

    news=get_news(event)

    prompt=f"""
LIVE NEWS CONTEXT:
{news}

EVENT:
{event}

Simulate civilization response across:

STEP 1 — Immediate effects (Day 1)
STEP 2 — Medium-term adaptation (Month 1)
STEP 3 — Long-term world evolution (Year 1)

Consider:
- health
- economy
- society
- technology
- environment
- geopolitics

Show cascading interactions between systems.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
              "role":"system",
              "content":"""
You are ScenarioOS Civilization Engine.

Simulate emergent world dynamics.
Do not act like a chatbot.
Do not give generic advice.
Model civilization evolution.
"""
            },
            {
              "role":"user",
              "content":prompt
            }
        ]
    )

    return res.choices[0].message.content


# ---------------- BUTTON ----------------

if st.button("Simulate Civilization"):

    if user_input.strip()=="":
        st.warning("Please enter a global event.")

    else:

        try:
            with st.spinner("Simulating world evolution..."):
                result=simulate_world(user_input)

            st.success("Simulation complete")
            st.markdown("## 🌍 Civilization Output")
            st.write(result)

        except Exception:
            st.error(
                "Simulation unavailable (API rate limit or no billing credit)."
            )
