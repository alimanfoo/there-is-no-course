from pathlib import Path
import re
import streamlit as st
from streamlit import session_state as session


menu_items = [
    "egg and bacon",
    "egg sausage and bacon",
    "egg and spam",
    "egg bacon and spam",
    "egg bacon sausage and spam",
    "spam bacon sausage and spam",
    "spam egg spam spam bacon and spam",
    "spam sausage spam spam spam bacon spam tomato and spam",
    "spam spam spam egg and spam",
    "spam spam spam spam spam spam baked beans spam spam spam and spam",
    "Lobster Thermidor aux Crevettes with a mornay sauce served in a Provencale manner with shallots and aubergines garnished with truffle pate, brandy and a fried egg on top and spam",
]


def exec_help():
    body = """
        Ask for the ``menu()`` if you'd like to know what we've got.

        Say ``order(N)`` to order dish number ``N`` on the menu.
        
        Ignore the ``vikings()``, they're a noisy lot.

        You can ``exit()`` when you're done.
    """
    output = [dict(function="markdown", body=body)]
    return output


def exec_menu():
    audio_path = Path(__file__).parent / "audio" / "menu.ogg"
    body = "### Menu\n"
    for i, item in enumerate(menu_items):
        body += f"{i}. {item}\n"

    output = [
        dict(function="markdown", body=body),
        dict(
            function="audio",
            data=audio_path.as_posix(),
            format="audio/ogg",
        ),
    ]
    return output


def exec_bad_order(item):
    body = f"Sorry, {item} isn't on the menu."
    output = [dict(function="markdown", body=body)]
    return output


def exec_order(item):
    item = menu_items[item]
    if "spam" not in item:
        body = "Uuuurgh! That hasn't got any spam in it."
    elif "baked beans" in item:
        body = "Baked beans are off."
    else:
        body = """
            An excellent choice! Coming right up...

            🐍🐍🐍🐍🐍🐍

            TODO URL
        """
    output = [dict(function="markdown", body=body)]
    return output


def exec_vikings():
    audio_path = Path(__file__).parent / "audio" / "vikings.ogg"
    output = [
        dict(
            function="audio",
            data=audio_path.as_posix(),
            format="audio/ogg",
        ),
    ]
    return output


order_regex = re.compile(r"order\(([^)]+)\)")


def on_input():
    history = session["history"]
    input = session["prompt"].strip()

    order_match = order_regex.match(input)

    if input == "help()":
        output = exec_help()

    elif input == "menu()":
        output = exec_menu()

    elif input == "vikings()":
        output = exec_vikings()

    elif order_match is not None:
        item = order_match.group(1)
        try:
            item = int(item)
        except Exception:
            output = exec_bad_order(item)
        else:
            if item >= len(menu_items):
                output = exec_bad_order(item)
            else:
                output = exec_order(item)

    ## TODO exit()
    ## TODO hint for order()
    ## TODO hint if forget parentheses
    ## TODO mr_bun()
    ## TODO mrs_bun()
    ## TODO lumberjack() -- easter egg

    else:
        output = [
            dict(
                function="markdown",
                body="Sorry, what?",
            ),
        ]

    item = dict(
        input=input,
        output=output,
    )
    history.append(item)
    session["history"] = history
    session["prompt"] = ""


def init_session():
    session.setdefault("history", [])
    session.setdefault("prompt", "")


def render():
    init_session()
    st.markdown(
        """
        # The Green Midget Café

        Morning!
        
        Shout ``help()`` if you need anything.           
    """
    )

    history = session["history"]
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

    st.divider()
    st.write(session)


if __name__ == "__main__":
    render()
