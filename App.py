import streamlit as st
from openai import OpenAI

st.title("Decision Simulator")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
