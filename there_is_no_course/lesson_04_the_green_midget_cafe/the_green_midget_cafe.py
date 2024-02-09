from pathlib import Path

import streamlit as st
from streamlit import session_state as session


def menu():
    audio_path = Path(__file__).parent / "audio" / "menu.ogg"
    output = [
        dict(function="markdown", body="TODO menu"),
        dict(
            function="audio",
            data=audio_path.as_posix(),
            format="audio/ogg",
        ),
    ]
    return output


def vikings():
    audio_path = Path(__file__).parent / "audio" / "vikings.ogg"
    output = [
        dict(
            function="audio",
            data=audio_path.as_posix(),
            format="audio/ogg",
        ),
    ]
    return output


def on_input():
    history = session["history"]
    next_input = session["prompt"].strip()

    if next_input == "menu()":
        next_output = menu()

    elif next_input == "vikings()":
        next_output = vikings()

    else:
        next_output = [
            dict(
                function="markdown",
                body="Sorry, I didn't understand that.",
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

# path = Path(__file__).parent / "audio" / "spam-skit.ogg"
# st.audio(path.as_posix(), format="audio/ogg")

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
