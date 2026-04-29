st.markdown("""
<div style="text-align:center; padding: 10px;">
    <h1>🧠 ScenarioOS</h1>
    <p style="color: gray; font-size: 16px;">
        A multi-agent simulation system that models possible future outcomes of your decisions.
    </p>
</div>
""", unsafe_allow_html=True)

st.info("""
ScenarioOS is not a chatbot.

It is a decision simulation engine powered by multiple reasoning agents:

• Optimistic Scenario Agent → explores best possible outcomes  
• Realistic Scenario Agent → evaluates most likely outcomes  
• Risk Scenario Agent → analyzes potential downsides and failures  

The system generates structured scenario forecasts instead of conversational answers.
""")
import streamlit as st
from openai import OpenAI

st.title("Decision Simulator")

import os
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
user_input = st.text_area("Scrivi una decisione")

def simulate(prompt):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You simulate 3 scenarios: optimistic, realistic, risky."},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content

if st.button("Simula") and user_input:
    result = simulate(user_input)
    st.write(result)
