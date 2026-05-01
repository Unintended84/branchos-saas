import streamlit as st
import os
from openai import OpenAI

# ---------------- CONFIG ----------------

DEFAULT_MODEL = "llama-3.3-70b-versatile"

MODEL_NAME = os.getenv("MODEL_NAME", DEFAULT_MODEL)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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
Emergent Civilization Simulator — modeling how billions of actors react to world-changing events.
</p>
</div>
""", unsafe_allow_html=True)

st.info("""
ScenarioOS simulates emergent reactions across:

• Governments  
• Social classes  
• Cultures  
• Institutions  
• Markets  
• Online populations  
• Adversarial actors  
• Ordinary citizens  

Outcomes emerge from interaction, not scripts.
""")

# ---------------- API CHECK ----------------

if not GROQ_API_KEY:
    st.error("⚠️ Missing GROQ_API_KEY. Set it in your environment variables.")
    st.stop()

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ---------------- INPUT ----------------

user_input = st.text_area(
    "Enter an event",
    placeholder="Example: Global internet blackout... AI takes control of financial markets... Sudden oil collapse...",
    height=140
)

col1, col2 = st.columns(2)

with col1:
    temperature = st.slider("Creativity", 0.0, 1.0, 0.9)

with col2:
    max_tokens = st.slider("Detail level", 500, 4000, 2500)

# ---------------- SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """You are a civilization-scale simulation engine.

You do NOT explain. You simulate.

FORMAT STRICTLY:

[ACTOR: <actor name>]
LOCATION: <region>
INITIAL STATE: <before event>

TIME PROGRESSION:
- Within minutes: <immediate reaction>
- Early hours: <reaction evolves>
- By the end of the day: <state by evening>
- The following day: <stabilized behavior>

INTERACTS WITH: <who and how>
SECOND-ORDER TRIGGER: <unexpected consequence>

Minimum 8 actors with conflicting motives.

Then:

[COLLISION MATRIX]
3–5 concrete clashes or alliances.

[EMERGENT CASCADE]
2–3 system-wide unintended consequences.

[SYSTEM STATE — 7 DAYS LATER]
Describe the transformed world.

RULES:
- Past tense only
- No "would", "might"
- Be specific and grounded
- Use natural time references (no T+X format)
- When relevant, include real local times (e.g., 08:30, late evening)
- Include at least one irrational actor (mob, rogue AI, cartel, etc.)
- IMPORTANT: Respond in the SAME LANGUAGE as the user input.
"""

# ---------------- SIMULATION ----------------

def run_simulation(event: str):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"EVENT INJECTION AT T=0:\n{event}\n\nRun simulation."}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ERROR: {str(e)}"

# ---------------- RUN ----------------

if st.button("🚀 Simulate Civilization", use_container_width=True):

    if not user_input.strip():
        st.warning("Insert an event first.")
        st.stop()

    with st.spinner(f"Running simulation using {MODEL_NAME}..."):

        result = run_simulation(user_input)

        if result.startswith("ERROR"):
            st.error(result)
        else:
            st.success("Simulation complete")
            st.markdown("## 🌍 Output")
            st.markdown(result)

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption(f"Model: {MODEL_NAME} | Powered by Groq")
