import streamlit as st


def show_instructions():
    st.write("# Instructions")
    st.write(
        """
    Welcome to the text pair evaluation tool. Here are the instructions on how to use this tool:

    ## How to Evaluate
    For each text pair, you will be asked to evaluate three aspects: adequacy, fluency, and simplicity. Each aspect should be rated on a scale from 0 to 4.

    - **Adequacy**: How well does the simplified text preserve the meaning of the original text?
      - 0: Not at all
      - 1: Poorly
      - 2: Fairly
      - 3: Well
      - 4: Perfectly

    - **Fluency**: How fluent and natural does the simplified text read?
      - 0: Not at all
      - 1: Poorly
      - 2: Fairly
      - 3: Well
      - 4: Perfectly

    - **Simplicity**: How much simpler is the simplified text compared to the original text?
      - 0: Not at all
      - 1: Slightly simpler
      - 2: Moderately simpler
      - 3: Considerably simpler
      - 4: Extremely simpler

    ## Navigation
    You can navigate through the text pairs using the "Previous" and "Next" buttons. Make sure to save your evaluation for each pair using the "Save Evaluation" button.

    ## Downloading Results
    Once you have completed your evaluations, you can download the results by clicking the download link provided at the bottom of the page.

    Thank you for your participation!
    """
    )


show_instructions()
