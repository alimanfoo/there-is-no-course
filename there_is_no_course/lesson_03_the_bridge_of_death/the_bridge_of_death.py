from pathlib import Path
import streamlit as st

# To save on some typing, import the session state as a variable
# with a shorter name.
from streamlit import session_state as session


def render():
    """Main UI rendering function."""

    init_session()
    render_header()

    # We are going to use URL query parameters here to manage the
    # main state of the game, because this allows us to hide an
    # easter egg question which the player can find by hacking
    # the URL.
    question = st.query_params.get("question", "intro")

    # This is a hack, to make sure that the query parameters are
    # visible in the URL. This isn't necessary when running streamlit
    # locally, but is necessary when running on streamlit community
    # cloud, because the app is being run within an iframe. Fun eh?
    st.query_params["question"] = question

    # Deal with different rendering scenarios, based on value of
    # question parameter.
    if question == "intro":
        render_intro()
    elif question == "1":
        render_question_one()
    elif question == "2":
        render_question_two()
    # This is the easter egg option, can only be found by URL hacking.
    elif question == "3":
        render_question_three()
    elif question == "4":
        render_question_four()
    elif question == "offyougo":
        render_success()
    else:
        render_bad_query_param()


def init_session():
    session.setdefault("question_one_tries", 0)
    session.setdefault("question_one_answer", "")
    session.setdefault("question_two_tries", 0)
    session.setdefault("question_two_answer", "")
    session.setdefault("question_three_tries", 0)
    session.setdefault("question_three_answer", "")
    session.setdefault("question_four_tries", 0)
    session.setdefault("question_four_answer", "")


def render_header():
    st.markdown(
        """
        **There is no course**

        # The Bridge of Death
    """
    )


def render_intro():
    st.markdown(
        """
        **Are you on a quest to become an Awesome Python Programmer?
        Then step forward, brave knight!**

        Stop! 
        Who would cross the Bridge of Death must answer me these questions
        three, ere the other side he see.
        If you get them all right, you will be allowed to pass.
        If you get them wrong, you will be cast into the Gorge of Eternal 
        Peril.

        <a href="?question=1" rel="next" target="_self">Let's do this! &gt;&gt;&gt;</a>
    """,
        unsafe_allow_html=True,
    )


def render_correct(next, text):
    st.markdown(
        f"""
        **Correct!** <a href="?question={next}" rel="next" target="_self">{text} &gt;&gt;&gt;</a>
    """,
        unsafe_allow_html=True,
    )


def render_death():
    st.markdown("**Auuuuuuuugh!**")
    st.markdown("(You have been cast into the Gorge of Eternal Peril.)")


def submit_question_one():
    session.question_one_tries += 1


def submit_question_two():
    session.question_two_tries += 1


def submit_question_three():
    session.question_three_tries += 1


def submit_question_four():
    session.question_four_tries += 1


def render_question_one():
    # Set up question.
    hints = [
        "Sorry, try again.",
        "Still not right. Another try maybe?",
        "Nope, still not right.",
        "You're just guessing! Come on...",
        "I'll give you a clue. It rhymes with 'Speedo Man Possum'.",
        "Is 'Guido' really that hard to spell?",
        "I'm not helping any more.",
        "2 more tries left...",
        "Last try...",
    ]
    correct_answers = ["guido van rossum"]

    # Obtain session variables.
    tries = session.question_one_tries
    answer = session.question_one_answer.lower().strip()
    correct = answer in correct_answers

    # Render initial content.
    st.markdown(
        f"""
        ## Question 1

        **Who invented the Python programming language?**

        Tries: {tries}/{len(hints) + 1}
    """
    )

    if correct:
        # Answer is correct, render link to next question.
        render_correct(next=2, text="Next question")
        return

    if tries > len(hints):
        # Answer is not correct, and there are no more hints.
        render_death()
        return

    with st.form(key="question_one_form"):
        st.text_input(label="``>>>``", key="question_one_answer")
        st.form_submit_button(label="Submit", on_click=submit_question_one)
        if tries > 0:
            st.markdown(hints[tries - 1])


def render_question_two():
    # Set up question.
    hints = [
        "Incorrect.",
        "Also incorrect.",
        "Spam spam spam spam...",
        "This is an ex-Parrot!",
        "I'm a lumberjack and I'm OK...",
        "...I sleep all night and I work all day...",
        "...I cut down trees, I eat my lunch, I go to the lavatory...",
        "...On Wednesdays I go shopping, and have buttered scones for tea!",
        "Last try...",
    ]
    correct_answers = [
        "monty python",
        "monty python flying circus",
        "monty pythons flying circus",
        "monty python's flying circus",
    ]

    # Obtain session variables.
    tries = session.question_two_tries
    answer = session.question_two_answer.lower().strip()
    correct = answer in correct_answers

    # Render initial content.
    st.markdown(
        f"""
        ## Question 2

        **What famous British comedy TV show is the Python 
        programming language named after?**

        Tries: {tries}/{len(hints) + 1}
    """
    )

    if correct:
        # Answer is correct, render link to next question.
        # N.B., deliberately skip question 3 here.
        render_correct(next=4, text="Next question")
        return

    if tries > len(hints):
        # Answer is not correct, and there are no more hints.
        render_death()
        return

    with st.form(key="question_two_form"):
        st.text_input(label="``>>>``", key="question_two_answer")
        st.form_submit_button(label="Submit", on_click=submit_question_two)
        if tries > 0:
            st.markdown(hints[tries - 1])


def render_question_three():
    """This is an easter egg question, can only be found by hacking
    URL query parameters."""

    # Set up question.
    hints = [
        "Did you watch the video?",
        "It's funny, isn't it.",
        "Especially the bit at the end.",
        "When King Arthur is answering the questions.",
        "His answer to the third question is very clever.",
        "Don't you think?",
        "The bridgekeeper didn't see that coming!",
        "Worth watching again, I'd say.",
        "Oh well, I gave you lots of chances...",
    ]
    correct_answers = [
        "What do you mean? An African or European swallow?".lower(),
        "An African or European swallow?".lower(),
        "African or European swallow?".lower(),
        "African or European?".lower(),
    ]

    # Obtain session variables.
    tries = session.question_three_tries
    answer = session.question_three_answer.lower().strip()
    # Be kind to the player, don't require a question mark.
    if answer and answer[-1] != "?":
        answer += "?"
    correct = answer in correct_answers

    # Render initial content.
    st.markdown(
        f"""
        ## Question 3

        **What is the air-speed velocity of an unladen swallow?**

        Tries: {tries}/{len(hints) + 1}
    """
    )

    if correct:
        # Answer is correct, render link to success.
        path = Path(__file__).parent / "bridgekeeper_stumped.jpg"
        st.image(path.as_posix())
        st.markdown(
            """
            Huh? I-- I don't know that. 
            
            **Auuuuuuuugh!**

            (Well done! You have cast the bridgekeeper into the Gorge of Eternal Peril.)
            
            <a href="?question=offyougo" rel="next" target="_self">Off you go &gt;&gt;&gt;</a>
        """,
            unsafe_allow_html=True,
        )
        return

    if tries > len(hints):
        # Answer is not correct, and there are no more hints.
        render_death()
        return

    st.video(data="https://youtu.be/0D7hFHfLEyk")
    with st.form(key="question_three_form"):
        st.text_input(label="``>>>``", key="question_three_answer")
        st.form_submit_button(label="Submit", on_click=submit_question_three)
        if tries > 0:
            st.markdown(hints[tries - 1])


def render_question_four():
    # Set up question.
    hints = [
        "Nope.",
        "Really?",
        "I despair.",
        "I don't why I bother.",
        "I mean, I go to all this trouble...",
        "Guido will not be happy with you.",
        "Three...",
        "Two...",
        "One...",
    ]
    correct_answers = [
        "python.org",
        "www.python.org",
        "http://python.org",
        "http://www.python.org",
        "https://python.org",
        "https://www.python.org",
        "http://python.org/",
        "http://www.python.org/",
        "https://python.org/",
        "https://www.python.org/",
        "python.org/downloads/",
        "www.python.org/downloads/",
        "http://python.org/downloads/",
        "http://www.python.org/downloads/",
        "https://python.org/downloads/",
        "https://www.python.org/downloads/",
    ]
    smart_answers = [
        "pypy.org",
        "www.pypy.org",
        "http://pypy.org",
        "http://www.pypy.org",
        "https://pypy.org",
        "https://www.pypy.org",
        "http://pypy.org/",
        "http://www.pypy.org/",
        "https://pypy.org/",
        "https://www.pypy.org/",
        "jython.org",
        "www.jython.org",
        "http://jython.org",
        "http://www.jython.org",
        "https://jython.org",
        "https://www.jython.org",
        "http://jython.org/",
        "http://www.jython.org/",
        "https://jython.org/",
        "https://www.jython.org/",
    ]

    # Obtain session variables.
    tries = session.question_four_tries
    answer = session.question_four_answer.lower().strip()
    correct = answer in correct_answers
    smart = answer in smart_answers

    # Render initial content.
    st.markdown(
        f"""
        ## Question 4

        **What website would you go to if you wanted to download 
        and install Python on your computer?**

        Tries: {tries}/{len(hints) + 1}
    """
    )

    if correct:
        # Answer is correct, render link to next question.
        render_correct(next="offyougo", text="Off you go")
        return

    if smart:
        # This is a bit of fun, attempt to catch out any
        # smartypants people out there who already know a
        # lot about Python.
        raise SmartyPantsError("Think you're clever, eh?")

    if tries > len(hints):
        # Answer is not correct, and there are no more hints.
        render_death()
        return

    with st.form(key="question_four_form"):
        st.text_input(label="``>>>``", key="question_four_answer")
        st.form_submit_button(label="Submit", on_click=submit_question_four)
        if tries > 0:
            st.markdown(hints[tries - 1])


def render_success():
    st.markdown("## Congratulations!")
    st.markdown("You have passed the test and crossed the Bridge of Death.")
    st.markdown("Here is your reward...")
    st.markdown("🐍🐍🐍🐍🐍🐍")

    # Final bit of fun, raise an exception and hide the next
    # video URL in the error message.
    i_am_a_lumberjack_error = RuntimeError(
        """
        Something unexpected has happened.
        It's probably a bug.
        I'm not maintaining this code any more, sorry.
        Here's a nice video about trees instead, to make you feel better...
        TODO URL
    """
    )
    raise i_am_a_lumberjack_error

    # st.markdown(
    #     "(Or <a href='?question=intro' target='_self'>play again</a> if you like, just for fun.)",
    #     unsafe_allow_html=True,
    # )


def render_bad_query_param():
    path = Path(__file__).parent / "bridgekeeper.webp"
    st.image(path.as_posix())
    st.markdown(
        """
        What do you think you are doing, hacking around with my URL 
        query parameters?
                
        I don't know what you expect to find.
    """
    )


class SmartyPantsError(Exception):
    pass


if __name__ == "__main__":
    # If we are running this as a script (as would be expected
    # if running via streamlit) then render the UI.
    render()
