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
        A real-time multi-agent simulation system that models possible future outcomes using live world context.
    </p>
</div>
""", unsafe_allow_html=True)

# --- INFO ---
st.info("""
ScenarioOS is not a chatbot.

It is a real-time scenario simulation engine powered by multiple reasoning agents:

• Optimistic Scenario Agent → best-case outcomes  
• Realistic Scenario Agent → most likely outcomes  
• Risk Scenario Agent → downside and volatility risks  

The system uses live news context to ground its reasoning.
""")

# --- OPENAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
