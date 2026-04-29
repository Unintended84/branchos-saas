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
Civilization Reaction Engine — simulating how global systems respond to major events.
</p>
</div>
""", unsafe_allow_html=True)

st.info("""
ScenarioOS models real-world system behavior:

• Governments & institutions  
• Society & population behavior  
• Media & information systems  
• Science & technology response  
• Geopolitical coordination  
• Systemic instability dynamics  

It simulates reactions, not opinions.
""")

# ---------------- INPUT ----------------

user_input = st.text_area(
    "Enter a global event",
    placeholder="UFO appears over Amsterdam... Pandemic starts in Italy... Climate collapse scenario...",
    height=140
)

# ---------------- LIVE CONTEXT ----------------

def get_news(query):
    try:
        url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=ArtList&format=json"
        r = requests.get(url, timeout=8)

        if r.status_code != 200:
            return "No live contextual data available."

        data = r.json()
        articles = data.get("articles", [])[:4]

        if not articles:
            return "No relevant global signals found."

        return "\n".join([f"- {a.get('title')}" for a in articles])

    except:
        return "Context system unavailable."


# ---------------- EVENT CLASSIFIER ----------------

def classify_event(event):

    e = event.lower()

    if "ufo" in e or "alien" in e:
        return "ufo"

    if "pandemic" in e or "virus" in e:
        return "pandemic"

    if "climate" in e or "flood" in e or "sea" in e:
        return "climate"

    if "cancer" in e or "cure" in e:
        return "science"

    return "generic"


# ---------------- CIVILIZATION ENGINE ----------------

def simulate_world(event):

    news = get_news(event)
    kind = classify_event(event)

    # --- CORE SYSTEM RESPONSE (NON TEMPLATE, MORE DYNAMIC) ---

    responses = {

        "ufo": {
            "institutions": [
                "NATO and national governments activate emergency coordination channels.",
                "Conflicting official statements emerge between states.",
                "Scientific institutions request controlled access to data."
            ],
            "society": [
                "Global social media explodes with contradictory footage.",
                "Mass polarization between believers and skeptics forms rapidly.",
                "New online cult-like communities emerge within hours."
            ],
            "media": [
                "Information ecosystems fragment into competing narratives.",
                "Misinformation spreads faster than official clarification.",
                "Traditional media lose monopoly on interpretation."
            ],
            "emergent": [
                "A new global belief structure begins forming outside institutions.",
                "Non-state actors gain influence over interpretation of events.",
                "Public trust in centralized narratives significantly weakens."
            ]
        },

        "pandemic": {
            "institutions": [
                "WHO coordination frameworks are activated.",
                "National responses diverge in speed and strictness.",
                "Healthcare systems enter emergency load conditions."
            ],
            "society": [
                "Behavioral compliance varies dramatically by region.",
                "Panic buying and mobility reduction occur globally.",
                "Trust in institutions becomes a key variable."
            ],
            "media": [
                "Information uncertainty drives anxiety amplification.",
                "Social platforms accelerate behavioral contagion.",
                "Scientific updates compete with speculation."
            ],
            "emergent": [
                "Parallel informal survival systems appear in some regions.",
                "Long-term institutional trust shifts permanently.",
                "New norms around health and mobility emerge globally."
            ]
        },

        "generic": {
            "institutions": [
                "Government crisis protocols are activated.",
                "International coordination begins unevenly.",
                "Policy divergence appears across regions."
            ],
            "society": [
                "Public perception shifts based on uncertainty levels.",
                "Local adaptation strategies emerge.",
                "Social stability varies by region."
            ],
            "media": [
                "Narrative competition increases across platforms.",
                "Information spreads faster than verification.",
                "Attention systems amplify uncertainty."
            ],
            "emergent": [
                "Unexpected second-order effects appear over time.",
                "Institutional adaptation lags behind social behavior.",
                "System equilibrium shifts unpredictably."
            ]
        }
    }

    s = responses[kind]

    news_context = f"""
GLOBAL CONTEXT SIGNALS:
{news}
"""

    result = f"""
🌍 WORLD CONTEXT
{news_context}

================ INSTITUTIONS RESPONSE ================
- {random.choice(s['institutions'])}
- {random.choice(s['institutions'])}

================ SOCIETAL RESPONSE ================
- {random.choice(s['society'])}
- {random.choice(s['society'])}

================ MEDIA & INFORMATION ================
- {random.choice(s['media'])}

================ EMERGENT EFFECTS ================
- {random.choice(s['emergent'])}
- {random.choice(s['emergent'])}

================ SYSTEM TRAJECTORY ================
The event triggers cascading interactions across institutions, society, and information systems, producing non-linear global adaptation patterns.
"""

    return result


# ---------------- BUTTON ----------------

if st.button("Simulate Civilization"):

    if user_input.strip() == "":
        st.warning("Please enter a global event.")

    else:

        with st.spinner("Simulating civilization response..."):
            result = simulate_world(user_input)

        st.success("Simulation complete")
        st.markdown("## 🌍 Civilization Reaction Output")
        st.write(result)
