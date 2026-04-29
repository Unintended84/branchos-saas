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
Civilization Reaction Engine — simulating cascading global responses to major events.
</p>
</div>
""", unsafe_allow_html=True)


st.info("""
ScenarioOS models interacting systems:

• Governments  
• Conflicts  
• Society  
• Markets  
• Information networks  
• Institutions  

It simulates causal reactions, not static predictions.
""")


# ---------------- INPUT ----------------

user_input = st.text_area(
    "Enter a global event",
    placeholder="Trump resigns tomorrow... UFO appears over Amsterdam... Strait of Hormuz closes...",
    height=140
)


# ---------------- CONTEXT ----------------

def get_news(query):

    try:
        url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=ArtList&format=json"
        r = requests.get(url, timeout=6)

        if r.status_code != 200:
            return "Using structural world knowledge simulation mode."

        data = r.json()

        articles = data.get("articles",[])[:3]

        if not articles:
            return "Using structural world knowledge simulation mode."

        return "\n".join(
            [f"- {a.get('title')}" for a in articles]
        )

    except:
        return "Using structural world knowledge simulation mode."



# ---------------- AFFECTED SYSTEMS ----------------

def infer_systems(event):

    e = event.lower()

    affected=[]

    if any(x in e for x in [
        "trump","president","resign","government","coup","election"
    ]):
        affected += [
            "executive power",
            "alliances",
            "active conflicts",
            "markets",
            "public legitimacy"
        ]


    if any(x in e for x in [
        "war","iran","nuclear","invasion"
    ]):
        affected += [
            "military deterrence",
            "energy markets",
            "geopolitics",
            "civilian stability"
        ]


    if any(x in e for x in [
        "ufo","alien"
    ]):
        affected += [
            "security doctrine",
            "scientific institutions",
            "mass psychology",
            "information systems"
        ]


    if any(x in e for x in [
        "pandemic","virus"
    ]):
        affected += [
            "health systems",
            "supply chains",
            "social compliance",
            "global coordination"
        ]


    if any(x in e for x in [
        "climate","flood","sea"
    ]):
        affected += [
            "migration",
            "infrastructure",
            "food systems",
            "state stability"
        ]


    if len(affected) < 2:
        affected = [
            "institutions",
            "society",
            "economy",
            "information networks"
        ]

    return list(dict.fromkeys(affected))


# ---------------- CIVILIZATION ENGINE ----------------

def simulate_world(event):

    news=get_news(event)

    systems=infer_systems(event)


    first_templates=[
        "Shock enters {a} and rapidly propagates into {b}.",
        "Disruption begins in {a}, triggering reactions in {b}.",
        "{a} destabilizes first, placing pressure on {b}."
    ]

    second_templates=[
        "Instability in {a} feeds back into {b}, amplifying consequences.",
        "{a} and {b} interact in ways producing secondary shocks.",
        "Adaptive responses in {a} unintentionally stress {b}."
    ]

    third_templates=[
        "Unexpected actors exploit shifts in {a}.",
        "Second-order effects become larger than the original trigger.",
        "A new equilibrium forms as {a} co-evolves with {b}."
    ]


    a,b=random.sample(systems,2)
    first=random.choice(first_templates).format(a=a,b=b)

    a,b=random.sample(systems,2)
    second=random.choice(second_templates).format(a=a,b=b)

    a,b=random.sample(systems,2)
    third=random.choice(third_templates).format(a=a,b=b)



    social=random.sample([
        "Social platforms amplify reactions faster than institutions respond.",
        "Public narratives fracture into competing interpretations.",
        "Grassroots coordination emerges outside formal systems.",
        "Information disorder alters behavior before facts stabilize."
    ],2)



    emergent=random.choice([
        "An unintended consequence becomes larger than the original event.",
        "Feedback loops generate outcomes no actor intended.",
        "Civilization adapts through emergent behavior rather than central control."
    ])



    war_logic=""

    if "trump" in event.lower():
        war_logic="""
ACTIVE CONFLICT IMPLICATIONS
• Existing wars may de-escalate during command uncertainty,
  or adversaries may test perceived weakness.
• Alliance signaling becomes critical for conflict direction.
"""



    output=f"""
🌍 WORLD CONTEXT
{news}

================ FIRST-ORDER EFFECTS ================
{first}

================ SECOND-ORDER CASCADES ================
{second}

================ SOCIAL / INFORMATION DYNAMICS ================
• {social[0]}
• {social[1]}

================ THIRD-ORDER EMERGENT EFFECTS ================
{third}

{war_logic}

================ CIVILIZATION TRAJECTORY ================
{emergent}
"""

    return output



# ---------------- BUTTON ----------------

if st.button("Simulate Civilization"):

    if user_input.strip()=="":
        st.warning("Please enter a global event.")

    else:

        with st.spinner("Simulating cascading civilization dynamics..."):
            result=simulate_world(user_input)

        st.success("Simulation complete")
        st.markdown("## 🌍 Civilization Output")
        st.write(result)
