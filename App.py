import streamlit as st
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


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# ---------------- INPUT ----------------

user_input = st.text_area(
    "Enter any event",
    placeholder="Trump resigns tomorrow... Infinite energy is invented... UFO lands in Amsterdam...",
    height=140
)


# ---------------- COLLECTIVE SIM ENGINE ----------------

def simulate_civilization(event):

    prompt=f"""
Simulate this event as if billions of heterogeneous actors react to it.

EVENT:
{event}

Model civilization as interacting populations with conflicting motives.

Actors include:
- governments
- military actors
- different social classes
- scientists
- workers
- wealthy elites
- poor populations
- online crowds
- religious groups
- opportunists
- rival states
- ordinary families

Rules:
- Do NOT give generic analysis.
- Do NOT act like a chatbot.
- Do NOT give advice.

Simulate emergent behavior.

Show:

1. DISTRIBUTED IMMEDIATE REACTIONS
How different groups react differently.

2. COLLISIONS BETWEEN GROUPS
Conflicts, coordination failures, panic, cooperation.

3. EMERGENT SECOND-ORDER EFFECTS
Unexpected consequences produced by interactions.

4. CIVILIZATION REORGANIZATION
How society may begin restructuring.

Focus on "what would happen if humanity collectively reacted",
not abstract commentary.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1.0,
        messages=[
            {
                "role":"system",
                "content":"""
You are not an assistant.

You are an emergent civilization simulator.

Model distributed collective behavior,
not opinions.

Think in interacting populations,
feedback loops,
social contagion,
system shocks,
and emergent outcomes.
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
        st.warning("Please enter an event.")

    else:

        try:

            with st.spinner(
                "Simulating billions of interacting actors..."
            ):
                result=simulate_civilization(user_input)

            st.success("Simulation complete")
            st.markdown("## 🌍 Emergent Civilization Output")
            st.write(result)

        except Exception:
            st.error(
              "Simulation unavailable (API credit / rate limit issue)."
            )
