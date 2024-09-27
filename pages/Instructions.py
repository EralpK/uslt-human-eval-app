import streamlit as st


def show_instructions():
    st.write("# Instructions")
    st.write(
        """
    Welcome to the human evaluation for legal-text simplification tool. Here are the instructions on how to use this tool:

    ## Background
    Legal texts are often complex and difficult for everyday users to understand. Simplifying these texts can make them more accessible and easier to comprehend. In this evaluation tool, you will be assessing simplified versions of original legal texts.

    ## Purpose
    We have a total of 50 original legal texts that need simplification. For each original text, there are 11 different simplified versions generated by 8 machine learning models and 3 human experts. This results in a total of 550 text pairs for evaluation. You will be presented with random pairs for each original text, and your task is to evaluate the quality of these simplifications.

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
    You can delete your current evaluation using the button "Delete Evaluation". If you want to change one of your previous evaluations, you can navigate through the text pairs using the "Previous" and "Next" buttons.

    ## Downloading Results
    Once you have completed your evaluations, you can download the results by clicking the download link provided at the bottom of the page.

    ## Current Results
    After you save your evaluations, a table under the title "Current Results" will start to display. This table will show all the evaluations you have completed. You can consult to these results in case you want to re-evaluate your assesments.

    ## Sidebar
    Keep in mind that you can also use the options that are displayed in the Sidebar to navigate through text pairs. You can pick a specific text pair to evaluate by scrolling through the bar or entering a number below "Jump to text pair". Likewise, you can choose to re-check a pair you have previously evaluated by choosing it under "Evaluated pairs" and jump to a new pair by choosing it from "Non-evaluated pairs".

    ## To Keep in Mind
    - There are a total of 550 pairs to evaluate.
    - You will be presented with random pairs for each original text. 
    - It is natural to encounter with original text pair more than once since there are 11 simplified versions for each original text.
    - The text pairs are not necessarily ordered, which means that you will not necessarily see the 11 simplifications of the same pair one after the other. This is done to ensure that your evaluations are not affected by the previous sentences, and that each simplification is assessed on its own.
    - The original text might be simple enough, so you might not see a significant difference between the original and simplified versions.

    ## Current Problems
    - You might encounter with absurd characters in the text. This is due to the encoding problem. These characters are generally encountered because of the interpretation of punctuation marks during the simplification process. Please ignore these characters and focus on the text content.

    Thank you for your participation!
    """
    )


show_instructions()
