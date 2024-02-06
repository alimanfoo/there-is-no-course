import streamlit as st


INTRO = 0
QUESTION_ONE = 1
QUESTION_TWO = 2
QUESTION_FIVE = 5
GAME_ABORTED = 6
GAME_COMPLETED = 7


def render():
    init_state()
    render_header()
    if st.session_state.game_state == INTRO:
        render_intro()
    elif st.session_state.game_state == QUESTION_ONE:
        render_question_one()
    elif st.session_state.game_state == QUESTION_TWO:
        render_question_two()
    elif st.session_state.game_state == QUESTION_FIVE:
        render_question_five()
    elif st.session_state.game_state == GAME_COMPLETED:
        render_game_completed()


def init_state():
    if "game_state" not in st.session_state:
        st.session_state.game_state = INTRO
    if "question_one_tries" not in st.session_state:
        st.session_state.question_one_tries = 0
    if "question_two_tries" not in st.session_state:
        st.session_state.question_two_tries = 0


def render_header():
    st.markdown(
        """
        ## There is no training course

        # Quiz
    """
    )


def render_intro():
    st.markdown(
        """
        Do you want to become an awesome Python programmer?
        Then this quiz is for you!

        I am going to ask you some questions.
        If you get them right, you will earn a reward.
        If you get them wrong, your computer will be infected
        with a virus that will turn your keyboard into spam.
    """
    )
    st.button(label="Let's do this!", on_click=lets_do_this)


def lets_do_this():
    st.session_state.game_state = QUESTION_ONE


def render_question_one():
    with st.form(key="question_one_form"):
        st.markdown(
            """
            **Question 1:** Who invented the Python programming language?
        """
        )
        answer = st.text_input(label="``>>>``")
        submitted = st.form_submit_button(label="Submit")

    if submitted:
        if answer.lower() == "guido van rossum":
            st.markdown("Correct!")
            st.button(label="Next question", on_click=question_one_correct)
        else:
            tries = st.session_state.question_one_tries
            if tries == 0:
                st.markdown("Sorry, try again.")
            elif tries == 1:
                st.markdown("Still not right. Another try maybe?")
            elif tries == 2:
                st.markdown("Nope, still not right.")
            elif tries == 3:
                st.markdown("You're just guessing! Come on...")
            elif tries == 4:
                st.markdown("Is 'Guido' really that hard to spell?")
            elif tries >= 5:
                st.markdown("I give up. You're on your own...")
            st.session_state.question_one_tries += 1


def question_one_correct():
    st.session_state.game_state = QUESTION_TWO


def render_question_two():
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
        acceptable_answers = [
            "monty python",
            "monty python's flying circus",
        ]
        if answer.lower() in acceptable_answers:
            st.markdown("Correct!")
            st.button(label="Next question", on_click=question_two_correct)
        else:
            tries = st.session_state.question_two_tries
            if tries == 0:
                st.markdown("Incorrect.")
            elif tries == 1:
                st.markdown("Very incorrect.")
            elif tries == 2:
                st.markdown("Spam spam spam spam...")
            elif tries == 3:
                st.markdown("This is an ex-Parrot!")
            elif tries == 4:
                st.markdown("I'm a lumberjack and I'm OK...")
            elif tries >= 5:
                # TODO maybe use the whole lumberjack song?
                st.markdown("I give up. You're on your own...")
            st.session_state.question_two_tries += 1


def question_two_correct():
    st.session_state.game_state = QUESTION_FIVE


def render_question_five():
    with st.form(key="question_five_form"):
        st.markdown(
            """
            **Question 5**: What website would you go to if you 
            wanted to download and install Python on your
            computer?
        """
        )
        answer = st.text_input(label="``>>>``")
        submitted = st.form_submit_button(label="Submit")

    # TODO


def render_game_completed():
    st.markdown("You win!")
    # TODO


if __name__ == "__main__":
    render()
