import streamlit as st
from openai import OpenAI
import requests

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ScenarioOS",
    page_icon="🧠",
    layout="centered"
)

# --- HEADER ---
st.markdown("""
<div style="text-align:center; padding: 10px;">
    <h1>🧠 ScenarioOS</h1>
    <p style="color: gray; font-size: 16px;">
        A civilization simulation engine that models how global systems evolve after major events.
    </p>
</div>
""", unsafe_allow_html=True)

# --- INFO ---
st.info("""
ScenarioOS simulates a global civilization.

It models systemic reactions across:
• Health systems
• Governments
• Society
• Economy
• Technology
• Environment
• Geopolitics

The world evolves over time based on your input event.
""")

# --- OPENAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- INPUT ---
user_input = st.text_area(
    "Enter a global event",
    placeholder="e.g. pandemic starts in Italy, UFO lands in London, cure for cancer discovered, sea level rises 10cm...",
    height=120
)

# --- LIVE NEWS ---
def get_news(query):
    try:
        url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=ArtList&format=json"
        response = requests.get(url)

        if response.status_code != 200:
            return "No live news available."

        data = response.json()
        articles = data.get("articles", [])[:5]

        if not articles:
            return "No recent news found."

        return "\n".join([f"- {a.get('title')}" for a in articles])

    except:
        return "News fetch error."

# --- WORLD STATE ---
def create_world_state():
    return {
        "health": 0.7,
        "economy": 0.7,
        "society": 0.7,
        "technology": 0.7,
        "environment": 0.7,
        "geopolitics": 0.7
    }

# --- SIMULATION ENGINE (MINI CIVILIZATION) ---
def simulate_world(event):

    world = create_world_state()
    news = get_news(event)

    output = ""

    for step in range(3):

        prompt = f"""
WORLD STATE (0-1 scale):
{world}

LIVE NEWS:
{news}

GLOBAL EVENT:
{event}

You are simulating a global civilization over time.

Update the world state based on cascading systemic effects.

Return:
1. Updated world state values (health, economy, society, technology, environment, geopolitics)
2. Explanation of what changed and why
3. Interactions between systems
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are ScenarioOS Civilization Engine.

You simulate how entire global systems evolve after major events.

Rules:
- Focus on systems, not individuals
- Show cascading effects between systems
- Update world state realistically
- Think like a complexity simulator, not a chatbot
"""
                },
                {"role": "user", "content": prompt}
            ]
        )

        step_result = res.choices[0].message.content
        output += f"\n\n================ STEP {step} ================\n{step_result}"

    return output

# --- BUTTON ---
if st.button("Simulate Civilization"):
    if user_input.strip() == "":
        st.warning("Please enter a global event")
    else:
        with st.spinner("Simulating world evolution..."):
            result = simulate_world(user_input)

        st.success("Simulation complete")
        st.markdown("## 🌍 Civilization Output")
        st.write(result)
# --- INPUT ---
user_input = st.text_area(
    "Enter your scenario",
    placeholder="e.g. Iran war ends, interest rates change, oil shock, startup launch...",
    height=120
)

# --- LIVE NEWS FUNCTION ---
def get_news(query):
    try:
        url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=ArtList&format=json"
        response = requests.get(url)

        if response.status_code != 200:
            return "No live news available."

        data = response.json()
        articles = data.get("articles", [])[:5]

        if not articles:
            return "No recent news found."

        news_text = ""
        for a in articles:
            news_text += f"- {a.get('title')}\n"

        return news_text

    except:
        return "News fetch error."

# --- CONTEXT BUILDER ---
def build_context(prompt):
    news = get_news(prompt)

    return f"""
REAL-TIME WORLD CONTEXT:

LATEST NEWS:
{news}

USER SCENARIO:
{prompt}
"""

# --- SCENARIO ENGINE ---
def simulate(prompt):

    context = build_context(prompt)

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are ScenarioOS, a multi-agent real-time simulation system.

You must analyze the given real-world context and generate:

1. Optimistic Scenario
2. Realistic Scenario
3. Risk Scenario

Rules:
- Use provided live context
- Do NOT behave like a chatbot
- Do NOT give generic advice
- Focus on market/geopolitical/systemic reasoning
"""
            },
            {
                "role": "user",
                "content": context
            }
        ]
    )

    return res.choices[0].message.content

# --- BUTTON ---
if st.button("Simulate"):
    if user_input.strip() == "":
        st.warning("Please enter a scenario.")
    else:
        with st.spinner("Analyzing real-time context..."):
            result = simulate(user_input)

        st.success("Simulation complete")
        st.markdown("## 📊 Scenario Output")
        st.write(result)  
