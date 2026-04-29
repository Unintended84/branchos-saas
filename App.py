import streamlit as st
import requests
import random

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

Live news is used as real-world context.
Simulation currently runs in prototype mode.
""")

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
        r=requests.get(url, timeout=8)

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


# ---------------- EVENT CLASSIFIER ----------------

def classify_event(event):

    e=event.lower()

    if "pandemic" in e or "virus" in e:
        return "pandemic"

    if "ufo" in e or "alien" in e:
        return "ufo"

    if "cancer" in e or "cure" in e:
        return "science"

    if "sea" in e or "climate" in e or "flood" in e:
        return "climate"

    return "generic"


# ---------------- CIVILIZATION SIM ----------------

def simulate_world(event):

    news=get_news(event)

    kind=classify_event(event)

    scenarios={

        "pandemic":{
            "day":"Emergency health responses spread globally.",
            "month":"Supply chains strain while governments diverge in strategy.",
            "year":"Public institutions and social behavior evolve permanently."
        },

        "ufo":{
            "day":"Global governments enter crisis coordination mode.",
            "month":"Scientific, military and social responses begin diverging.",
            "year":"Human civilization reorganizes around first-contact implications."
        },

        "science":{
            "day":"Medical systems react with disbelief and urgency.",
            "month":"Global health priorities shift rapidly.",
            "year":"Society restructures around longer life and lower disease burden."
        },

        "climate":{
            "day":"Coastal risk alerts trigger emergency planning.",
            "month":"Migration and infrastructure adaptation accelerate.",
            "year":"Political and environmental systems are restructured."
        },

        "generic":{
            "day":"Governments issue immediate responses.",
            "month":"Systems adapt under pressure.",
            "year":"The event reshapes long-term civilization dynamics."
        }

    }

    s=scenarios[kind]

    system_states=[
        "Health stability: adaptive stress",
        "Society: elevated uncertainty",
        "Technology: accelerated innovation",
        "Environment: systemic ripple effects",
        "Geopolitics: strategic instability",
        "Institutions: resilience under pressure"
    ]

    random.shuffle(system_states)

    result=f"""
🌍 LIVE WORLD CONTEXT

{news}

================ DAY 1 ================
{s['day']}

================ MONTH 1 ==============
{s['month']}

================ YEAR 1 ===============
{s['year']}

================ SYSTEM DYNAMICS ===============
- {system_states[0]}
- {system_states[1]}
- {system_states[2]}

Emergent civilization trajectory:
The event generates second-order effects beyond the initial shock and shifts long-term global equilibrium.
"""

    return result


# ---------------- BUTTON ----------------

if st.button("Simulate Civilization"):

    if user_input.strip()=="":
        st.warning("Please enter a global event.")

    else:

        with st.spinner("Simulating world evolution..."):
            result=simulate_world(user_input)

        st.success("Simulation complete")
        st.markdown("## 🌍 Civilization Output")
        st.write(result)
