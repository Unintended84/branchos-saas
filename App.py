import streamlit as st
import os
from openai import OpenAI

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
Emergent Civilization Simulator — modeling how billions of diverse actors react to world-changing events.
</p>
</div>
""", unsafe_allow_html=True)

st.info("""
ScenarioOS does not use fixed scenarios.

It simulates emergent reactions across:

• Governments  
• Social classes  
• Cultures  
• Institutions  
• Markets  
• Online populations  
• Adversarial actors  
• Ordinary citizens  

Outcomes emerge from interacting behaviors.
""")

# ---------------- CLIENT (GROQ + LLAMA3) ----------------

GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    st.error("⚠️ Missing GROQ_API_KEY. Add it as a repository secret or environment variable.")
    st.stop()

client = OpenAI(
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
) 

# ---------------- INPUT ----------------

user_input = st.text_area(
    "Enter any event",
    placeholder="Example: Global internet blackout... Infinite clean energy discovered... Major war ends suddenly...",
    height=140
)

# ---------------- SIMULATION ENGINE ----------------

SYSTEM_PROMPT = """You are a civilization-scale simulator.

You do not analyze or comment — you simulate, producing concrete timelines.

Your structure must contain:

[ACTOR: <actor name>]
LOCATION: <region or country>
INITIAL STATE: <what they were doing before>
T+0h: <immediate action>
T+6h: <evolving reaction>
T+24h: <stabilized attitude or behavior>
INTERACTS WITH: <groups and nature of interaction>
SECOND-ORDER TRIGGER: <unexpected ripple effects>

At least 8 actor groups with conflicting motives must appear.

After listing actors, write:

[COLLISION MATRIX]
List 3–5 real clashes or cooperations between actors (what happens concretely).

[EMERGENT CASCADE]
List 2–3 unintended system-wide consequences emerging from those interactions.

[SYSTEM STATE T+7 DAYS]
Show the transformed social and political order.

Rules:
- Always write in the past tense (describe what happened).
- Never hedge with "would" or "might".
- Be concrete, detailed, specific.
- Include at least one irrational or wildcard actor (crime network, online mob, rogue AI, etc.).
"""

def simulate_civilization(event: str):
    prompt = f"EVENT INJECTION AT T=0:\n{event}\n\nRun the full simulation now."
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        temperature=0.9,
        max_tokens=4000,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# ---------------- RUN SIMULATION ----------------

if st.button("🚀 Simulate Civilization"):
    if not user_input.strip():
        st.warning("Please enter an event first.")
    else:
        with st.spinner("Simulating billions of interacting actors (via Llama 3 on Groq)..."):
            try:
                result = simulate_civilization(user_input)
                st.success("✅ Simulation complete!")
                st.markdown("## 🌍 Emergent Civilization Output")
                st.markdown(result)
            except Exception as e:
                st.error(f"Simulation failed: {e}")
