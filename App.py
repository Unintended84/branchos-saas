import streamlit as st
from openai import OpenAI

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
        A multi-agent simulation system that models possible future outcomes of any scenario.
    </p>
</div>
""", unsafe_allow_html=True)

# --- DESCRIPTION ---
st.info("""
ScenarioOS is not a chatbot.

It is a scenario simulation engine powered by multiple reasoning agents:

• Optimistic Scenario Agent → explores best possible outcomes  
• Realistic Scenario Agent → evaluates most likely outcomes  
• Risk Scenario Agent → analyzes potential downsides and failures  

It generates structured scenario forecasts instead of conversational answers.
""")

# --- OPENAI CLIENT (CORRETTO PER STREAMLIT) ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- INPUT ---
user_input = st.text_area(
    "Enter your scenario",
    placeholder="e.g. launching a startup, moving abroad, investing in a project...",
    height=120
)

# --- SIMULATION FUNCTION ---
def simulate(prompt):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a multi-agent scenario simulation system.

You must generate 3 structured outputs:

1. Optimistic Scenario
2. Realistic Scenario
3. Risk Scenario

Do NOT behave like a chatbot. Do NOT give advice. Only simulate outcomes.
"""
            },
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content

# --- BUTTON ---
if st.button("Simulate"):
    if user_input.strip() == "":
        st.warning("Please enter a scenario.")
    else:
        with st.spinner("Simulating scenarios..."):
            result = simulate(user_input)

        st.success("Simulation complete")

        st.markdown("## 📊 Scenario Output")
        st.write(result)            {"role": "system", "content": "You simulate 3 scenarios: optimistic, realistic, risky."},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content

if st.button("Simula") and user_input:
    result = simulate(user_input)
    st.write(result)
