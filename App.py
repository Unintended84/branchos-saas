# ---------------- EVENT PARSER ----------------

def infer_systems(event):

    e=event.lower()

    affected=[]

    # non categorie rigide, sistemi perturbati

    if any(x in e for x in ["trump","president","government","resign","coup","election"]):
        affected += [
            "executive power",
            "alliances",
            "active conflicts",
            "markets",
            "public legitimacy"
        ]

    if any(x in e for x in ["war","iran","nuclear","invasion"]):
        affected += [
            "military deterrence",
            "energy markets",
            "geopolitics",
            "civilian stability"
        ]

    if any(x in e for x in ["ufo","alien"]):
        affected += [
            "scientific institutions",
            "security doctrine",
            "mass psychology",
            "information systems"
        ]

    if any(x in e for x in ["pandemic","virus"]):
        affected += [
            "health systems",
            "supply chains",
            "social compliance",
            "global coordination"
        ]

    if any(x in e for x in ["climate","flood","sea"]):
        affected += [
            "infrastructure",
            "migration",
            "food systems",
            "state stability"
        ]

    if not affected:
        affected = [
            "institutions",
            "society",
            "economy",
            "information networks"
        ]

    return list(dict.fromkeys(affected))


# ---------------- CASCADE ENGINE ----------------

def simulate_world(event):

    news=get_news(event)

    systems=infer_systems(event)

    first_order_templates=[
      "Immediate stress appears in {a} while {b} begins adjusting.",
      "{a} is disrupted first, triggering reactions in {b}.",
      "Shock enters {a} and rapidly propagates into {b}."
    ]

    second_order_templates=[
      "Instability in {a} feeds back into {b}, amplifying secondary consequences.",
      "{a} interacts with {b}, producing nonlinear side effects.",
      "Adaptive responses in {a} unintentionally pressure {b}."
    ]

    third_order_templates=[
      "Unexpected actors exploit shifts in {a}, changing outcomes.",
      "Second-order effects become larger than the original trigger.",
      "A new equilibrium emerges as {a} and {b} co-evolve."
    ]

    # pick systems dynamically
    a,b=random.sample(systems,2)

    first=random.choice(first_order_templates).format(a=a,b=b)

    a,b=random.sample(systems,2)
    second=random.choice(second_order_templates).format(a=a,b=b)

    a,b=random.sample(systems,2)
    third=random.choice(third_order_templates).format(a=a,b=b)


    war_logic=""

    # dynamic reasoning layer (esempio che volevi)
    if "trump" in event.lower():
        war_logic="""
ACTIVE CONFLICT IMPLICATIONS
• Ongoing wars may temporarily de-escalate during command uncertainty,
  or adversaries may test perceived weakness.
• Conflict trajectories depend on alliance signaling during succession.
"""


    social_dynamics=random.sample([
       "Social platforms accelerate polarization faster than institutions respond.",
       "Public narratives split into competing interpretations of reality.",
       "Grassroots coordination emerges outside formal institutions.",
       "Information disorder alters behavior before facts stabilize."
    ],2)


    emergent=random.choice([
      "An unintended consequence becomes historically more important than the event itself.",
      "System feedback loops create outcomes no actor originally intended.",
      "Civilization adapts through emergent behavior rather than central control."
    ])


    result=f"""
🌍 CURRENT WORLD CONTEXT
{news}

================ FIRST-ORDER EFFECTS ================
{first}

================ SECOND-ORDER CASCADES ================
{second}

================ SOCIAL/INFORMATION DYNAMICS ================
• {social_dynamics[0]}
• {social_dynamics[1]}

================ THIRD-ORDER EMERGENT EFFECTS ================
{third}

{war_logic}

================ CIVILIZATION TRAJECTORY ================
{emergent}
"""

    return result
