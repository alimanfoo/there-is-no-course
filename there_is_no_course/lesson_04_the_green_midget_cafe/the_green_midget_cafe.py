import streamlit as st
from streamlit import session_state as session


def on_input():
    history = session["history"]
    next_input = session["prompt"]
    next_output = [
        dict(
            function="markdown",
            body=next_input,
        ),
    ]
    next_item = dict(
        input=next_input,
        output=next_output,
    )
    history.append(next_item)
    session["history"] = history
    session["prompt"] = ""


session.setdefault("history", [])
session.setdefault("prompt", "")

history = session["history"]

st.title("The Green Midget Café")

for item in history:
    input = item["input"]
    output = item["output"]
    st.markdown(f"``>>> {input}``")
    for content in output:
        content = content.copy()
        function = content.pop("function")
        f = getattr(st, function)
        f(**content)

st.text_input(
    label="``>>>``",
    key="prompt",
    on_change=on_input,
)

st.write(session)
