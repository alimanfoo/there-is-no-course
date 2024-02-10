from pathlib import Path
import re
import streamlit as st
from streamlit import session_state as session


menu_items = [
    "Egg and bacon.",
    "Egg sausage and bacon.",
    "Egg and spam.",
    "Egg bacon and spam.",
    "Egg bacon sausage and spam.",
    "Spam bacon sausage and spam.",
    "Spam egg spam spam bacon and spam.",
    "Spam sausage spam spam spam bacon spam tomato and spam.",
    "Spam spam spam egg and spam.",
    "Spam spam spam spam spam spam baked beans spam spam spam and spam.",
    "Lobster Thermidor aux crevettes with a mornay sauce served in a Provencale manner with shallots and aubergines garnished with truffle paté, brandy and a fried egg on top and spam.",
]


def exec_help_inside():
    body = """
        Welcome to the Green Midget Café!

        Ask for the ``menu()`` if you'd like to know what we've got.

        Say ``order(N)`` to order dish number ``N`` on the menu.
        
        Ignore the ``vikings()``, they're a noisy lot.

        You can ``exit()`` whenever you're done.
    """
    output = [dict(function="markdown", body=body)]
    return output


def exec_help_outside():
    body = """
        Would you like to ``enter()`` the Green Midget Café?

        I hear they do wonderful spam...
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
        session["success"] = True
        body = f"""
            {item}

            An excellent choice! Coming right up...

            🐍🐍🐍🐍🐍🐍

            TODO URL
        """
    output = [dict(function="markdown", body=body)]
    return output


def exec_order_nothing():
    output = [dict(function="markdown", body="Perhaps you meant to order something?")]
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


def exec_exit():
    success = session["success"]
    session["success"] = False
    session["inside"] = False
    if success:
        output = [
            dict(function="markdown", body="Thanks for visiting! Come back soon.")
        ]
    else:
        output = [
            dict(
                function="markdown",
                body="Shame you didn't order anything. Maybe some spam next time?",
            )
        ]
    return output


def exec_bad_command():
    output = [
        dict(
            function="markdown",
            body="Sorry, what?",
        ),
    ]
    return output


def exec_enter():
    session["inside"] = True
    output = [
        dict(
            function="markdown",
            body="Morning! Shout for ``help()`` if you need anything.",
        ),
    ]
    return output


def exec_hint_brackets():
    output = [
        dict(
            function="markdown",
            body="If you want something to happen, you'll need to add a pair of brackets.",
        ),
    ]
    return output


def exec_clear():
    session["history"] = []
    output = []
    return output


order_regex = re.compile(r"order\(([^)]+)\)")


def on_input():
    input = session["prompt"].strip()
    inside = session["inside"]
    if inside:
        output = on_input_inside()
    else:
        output = on_input_outside()
    history = session["history"]
    if input != "clear()":
        item = dict(
            input=input,
            output=output,
        )
        history.append(item)
    session["history"] = history
    session["prompt"] = ""


def on_input_outside():
    input = session["prompt"].strip()
    if input == "enter()":
        output = exec_enter()
    elif input == "clear()":
        output = exec_clear()
    elif input == "help()":
        output = exec_help_outside()
    elif input in ["enter", "clear", "help"]:
        output = exec_hint_brackets()
    else:
        output = exec_bad_command()
    return output


def on_input_inside():
    input = session["prompt"].strip()
    order_match = order_regex.match(input)

    if input == "help()":
        output = exec_help_inside()

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

    elif input == "exit()":
        output = exec_exit()

    elif input == "clear()":
        output = exec_clear()

    elif input == "order()":
        output = exec_order_nothing()

    elif input in ["help", "menu", "vikings", "exit", "clear", "order"]:
        output = exec_hint_brackets()

    ## TODO mr_bun()
    ## TODO mrs_bun()
    ## TODO lumberjack() -- easter egg

    else:
        output = exec_bad_command()

    return output


def init_session():
    session.setdefault("inside", False)
    session.setdefault("history", [])
    session.setdefault("prompt", "")
    session.setdefault("success", False)


def render():
    init_session()
    st.title("The Green Midget Café")

    history = session["history"]

    st.markdown(
        """
        Welcome to Bromley! 

        Would you like to ``enter()`` the Green Midget Café?

        I hear they do wonderful spam...
    """
    )

    for item in history:
        input = item["input"]
        output = item["output"]
        st.markdown(f"``>>> {input}``")
        for content in output:
            content = content.copy()
            function_name = content.pop("function")
            f = getattr(st, function_name)
            f(**content)

    st.text_input(
        label="``>>>``",
        key="prompt",
        on_change=on_input,
    )

    # Debug.
    st.divider()
    st.write(session)


if __name__ == "__main__":
    render()
