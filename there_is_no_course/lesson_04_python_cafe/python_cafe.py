import time
import sys


menu = [
    "egg and bacon",
    "egg sausage and bacon",
    "egg and spam",
    "egg bacon and spam",
    "egg bacon sausage and spam",
    "spam bacon sausage and spam",
    "spam egg spam spam bacon and spam",
    "spam sausage spam spam bacon spam tomato and spam",
    "spam spam spam egg and spam",
    "spam spam spam spam spam spam baked beans spam spam spam",
    "Lobster thermidor aux crevettes with a mornay sauce garnished with truffle pâté, brandy and with a fried egg on top and spam",
]


def output(message, line_sleep=1.5, word_sleep=0.15):
    for line in message.split("\n"):
        if word_sleep > 0:
            for word in line.split():
                print(word, end=" ", file=sys.stdout)
                sys.stdout.flush()
                time.sleep(word_sleep)
            print(file=sys.stdout)
            sys.stdout.flush()
        else:
            print(line, file=sys.stdout)
            sys.stdout.flush()
        time.sleep(line_sleep)


def enter_cafe():
    output(
        """\
 ____  _  _  ____  _  _   __   __ _     ___   __   ____  ____ 
(  _ \( \/ )(_  _)/ )( \ /  \ (  ( \   / __) / _\ (  __)(  __)
 ) __/ )  /   )(  ) __ ((  O )/    /  ( (__ /    \ ) _)  ) _) 
(__)  (__/   (__) \_)(_/ \__/ \_)__)   \___)\_/\_/(__)  (____)
    """,
        line_sleep=0.1,
        word_sleep=0,
    )
    output(
        f"""
Morning!
Welcome to the Python Cafe!
What have we got?
Well, there's:
[0] {menu[0]}
[1] {menu[1]}
[2] {menu[2]}
[3] {menu[3]}
[4] {menu[4]}
[5] {menu[5]}
[6] {menu[6]}
[7] {menu[7]}
[8] {menu[8]}
[9] {menu[9]}
[10] {menu[10]}
    """.strip(),
    )
    order = ""
    while True:
        order = input(">>> ")
        order = order.lower().strip()

        # Try to parse the order as a number.
        try:
            order = int(order)
        except Exception:
            pass
        else:
            if order < len(menu):
                order = menu[order]

        if order not in menu:
            # Only allow dishes that are on the menu.
            output("That's not on the menu.")
            continue

        if "spam" in order:
            # Keep going until the customer orders something
            # with spam in it.
            break

        output("Wouldn't you like something with spam in it?")

    output(
        f"""
{order}
An excellent choice!
Coming right up...
TODO URL
    """.strip(),
    )


if __name__ == "__main__":
    enter_cafe()
