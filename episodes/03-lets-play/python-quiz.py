from textwrap import dedent, fill
import time
import sys


AFFIRMATIVE_RESPONSES = {"y", "yes", "yep", "yup", "ya", "yeah", "hell yeah"}


class SmartypantsError(Exception):
    pass


def pause(length=1):
    time.sleep(length)


def message(content):
    # Always pause for dramatic effect.
    pause()
    print()
    print(fill(dedent(content)))


def game_intro():
    message(
        """\
        Hello and wellcome to \"THERE IS NO COURSE\", the game for
        people who want to become awesome Python programmers!
    """
    )

    message(
        """\
        I'm going to ask you some questions.
                  
        If you get them right, you will earn a reward.
                  
        If you get them wrong, I will infect your computer with
        a virus that turns your keyboard into cheese.
                  
        Do you dare to play?
    """
    )


def question_one():
    while True:
        message(
            """\
            Question 1. Who invented the Python programming language?
        """
        )
        response = input(">>> ").lower()
        if response == "guido van rossum":
            break
        else:
            message("Incorrect, try again.")
    message("Correct!")


def question_two():
    while True:
        message(
            """\
            Question 2. What famous British TV comedy show is the Python 
            programming language named after?
        """
        )
        response = input(">>> ").lower()
        if response == "monty python":
            break
        else:
            message("Incorrect, try again.")
    message("Correct!")


def question_five():
    while True:
        message(
            """\
            Question 5. What website would you go to if you wanted to
            download and install Python on your computer?
        """
        )
        response = input(">>> ").lower()
        if response in {
            "www.python.org",
            "http://www.python.org",
            "https://www.python.org",
        }:
            break
        elif "pypy" in response or "jython" in response or "ironpython" in response:
            raise SmartypantsError
        else:
            message("Incorrect, try again.")
    message("Correct!")


def game_completed():
    message(
        """\
        Congratulations, you have completed the game!
                    
        I will now give you your reward...
    """
    )
    print()
    pause(2)
    raise RuntimeError(
        fill(
            dedent(
                """\
        Something unexpected has happened. It is probably a bug.
        I'm not maintaining this software any more, sorry. Here
        is a nice cat video to make you feel better...
                                    
        @@TODO URL
        
    """
            )
        )
    )


def game_aborted():
    message(
        """\
        Very wise. You will live a long and happy life. 
        Thanks for not playing. Goodbye.
    """
    )
    sys.exit(0)


def main():
    game_intro()
    response = input(">>> ")
    if response.lower() in AFFIRMATIVE_RESPONSES:
        message(
            """\
            You are brave indeed! Or foolish. We shall see...
        """
        )
        question_one()
        question_two()
        question_five()
        game_completed()

    else:
        game_aborted()


if __name__ == "__main__":
    main()
