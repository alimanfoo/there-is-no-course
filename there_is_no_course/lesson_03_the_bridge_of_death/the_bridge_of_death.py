import streamlit as st

# To save on some typing, import the session state as a variable
# with a shorter name.
from streamlit import session_state as session


def render():
    init_session()
    render_header()

    # We are going to use URL query parameters here to manage the
    # main state of the game, because this allows us to hide an
    # easter egg question which the player can find by hacking
    # the URL.
    question = st.query_params.get("question", "intro")
    if question == "intro":
        render_intro()
    elif question == "1":
        render_question_one()
    elif question == "2":
        render_question_two()
    elif question == "4":
        render_question_four()
    # This is the easter egg option, can only be found by URL hacking.
    elif question == "3":
        render_question_three()
    elif question == "offyougo":
        render_success()
    else:
        render_bad_question()


def init_session():
    session.setdefault("question_one_tries", 0)
    session.setdefault("question_two_tries", 0)
    session.setdefault("question_three_tries", 0)
    session.setdefault("question_four_tries", 0)


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

        <a href="/?question=1" target="_self">Let's do this! &gt;&gt;&gt;</a>
    """,
        unsafe_allow_html=True,
    )


def render_question_one():
    tries = session.question_one_tries
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
    if tries < len(hints):
        with st.form(key="question_one_form"):
            st.markdown(
                """
                **Question 1:** Who invented the Python programming language?
            """
            )
            answer = st.text_input(label="``>>>``")
            submitted = st.form_submit_button(label="Submit")

        if submitted:
            if answer.lower() in correct_answers:
                st.markdown(
                    """
                    Correct! <a href="?question=2" target="_self">Next question &gt;&gt;&gt;</a>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(hints[tries])
                session.question_one_tries += 1
    else:
        render_death()


def render_question_two():
    tries = session.question_two_tries
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
    if tries < len(hints):
        with st.form(key="question_two_form"):
            st.markdown(
                """
                **Question 2**: What famous British comedy TV show is the 
                Python programming language named after?
            """
            )
            answer = st.text_input(label="``>>>``")
            submitted = st.form_submit_button(label="Submit")

        if submitted:
            if answer.lower() in correct_answers:
                # Deliberately skip over question 3, that is the easter egg.
                st.markdown(
                    """
                    Correct! <a href="?question=4" target="_self">Next question &gt;&gt;&gt;</a>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(hints[tries])
                session.question_two_tries += 1
    else:
        render_death()


def render_question_four():
    tries = session.question_four_tries
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
    if tries < len(hints):
        with st.form(key="question_four_form"):
            st.markdown(
                """
                **Question 4**: What website would you go to if you 
                wanted to download and install Python on your
                computer?
            """
            )
            answer = st.text_input(label="``>>>``")
            submitted = st.form_submit_button(label="Submit")

        if submitted:
            if answer.lower() in correct_answers:
                st.markdown(
                    """
                    Correct! <a href="?question=offyougo" target="_self">Off you go &gt;&gt;&gt;</a>
                """,
                    unsafe_allow_html=True,
                )
            elif answer.lower() in smart_answers:
                # This is a bit of fun, attempt to catch out any
                # smartypants people out there who already know a
                # lot about Python.
                raise SmartyPantsError
            else:
                st.markdown(hints[tries])
                session.question_four_tries += 1
    else:
        render_death()


def render_question_three():
    tries = session.question_three_tries
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
    if tries < len(hints):
        st.video(data="https://youtu.be/0D7hFHfLEyk")
        with st.form(key="question_three_form"):
            st.markdown(
                """
                **Question 3**: What is the air-speed velocity of an unladen swallow?
            """
            )
            answer = st.text_input(label="``>>>``")
            submitted = st.form_submit_button(label="Submit")

        if submitted:
            answer = answer.lower()
            # Be kind to the player, don't require a question mark.
            if answer and answer[-1] != "?":
                answer += "?"
            if answer in correct_answers:
                st.markdown(
                    """
                    Huh? I-- I don't know that. 
                    
                    ## Auuuuuuuugh!

                    (Well done! You have cast the bridgekeeper into the Gorge of Eternal Peril.)
                    
                    <a href="?question=offyougo" target="_self">Off you go &gt;&gt;&gt;</a>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(hints[tries])
                session.question_three_tries += 1
    else:
        render_death()


def render_death():
    st.markdown("## Auuuuuuuugh!")
    st.markdown("(You have been cast into the Gorge of Eternal Peril.)")


def render_success():
    st.markdown("## 🐍🐍🐍 Congratulations! 🐍🐍🐍")
    st.markdown("You have crossed the bridge of doom.")
    st.markdown("But the quest continues...")
    st.markdown("TODO link to next video.")
    st.markdown(
        "(Or you can <a href='?question=intro'>play again</a> if you like, just for fun.)",
        unsafe_allow_html=True,
    )


def render_bad_question():
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
    render()
