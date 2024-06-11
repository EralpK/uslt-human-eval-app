import os

import pandas as pd
import streamlit as st

from utils import (
    get_table_download_link,
    next_text_pair,
    previous_text_pair,
    save_evaluation,
)

# Load the CSV file
file_path = "data.csv"  # Update this to the correct path if needed
data = pd.read_csv(file_path)


def show_evaluation():
    # Initialize session state variables
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    if "results_df" not in st.session_state:
        # Initialize results.csv with empty rows and load it
        if not os.path.exists("results.csv"):
            empty_df = pd.DataFrame(
                columns=[
                    "id",
                    "original_text_id",
                    "model_id",
                    "adequacy",
                    "fluency",
                    "simplicity",
                ]
            )
            empty_df.to_csv("results.csv", index=False)
        st.session_state.results_df = pd.read_csv("results.csv")

    # Display the current text pair
    index = st.session_state.current_index
    st.write(f"# Text Pair {index + 1}/{len(data)}")

    st.write("### Original Text")
    st.write(data.iloc[index]["original"])

    st.write("### Simplified Text")
    st.write(data.iloc[index]["simplified"])

    # Check if the current text pair has already been evaluated and display a warning message
    if data.iloc[index]["id"] in st.session_state.results_df["id"].values:
        st.warning(
            "This pair is already evaluated. If you like to change your evaluation, please feel free."
        )
        # Pre-fill the radio buttons with the existing evaluation
        existing_evaluation = st.session_state.results_df[
            st.session_state.results_df["id"] == data.iloc[index]["id"]
        ].iloc[0]
        st.session_state.adequacy = int(existing_evaluation["adequacy"])
        st.session_state.fluency = int(existing_evaluation["fluency"])
        st.session_state.simplicity = int(existing_evaluation["simplicity"])
    else:
        st.session_state.adequacy = 0
        st.session_state.fluency = 0
        st.session_state.simplicity = 0

    # Radio buttons for evaluations displayed in separate lines for readability
    options = [0, 1, 2, 3, 4]
    st.session_state.adequacy = st.radio(
        label="##### Adequacy (is the meaning preserved?)",
        options=options,
        index=st.session_state.adequacy,
        horizontal=True,
    )

    st.session_state.fluency = st.radio(
        label="##### Fluency (is the simplification fluent?)",
        options=options,
        index=st.session_state.fluency,
        horizontal=True,
    )

    st.session_state.simplicity = st.radio(
        label="##### Simplicity (is the simplification actually simpler?)",
        options=options,
        index=st.session_state.simplicity,
        horizontal=True,
    )

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button("Previous", on_click=previous_text_pair)
    with col2:
        st.button("Next", on_click=next_text_pair)
    with col3:
        st.button("Save Evaluation", on_click=save_evaluation)

    # Display current results table at the bottom of the page
    st.write("#### Current Results")
    st.write(st.session_state.results_df)

    # Provide a download link for the updated results.csv
    st.markdown(
        get_table_download_link(st.session_state.results_df), unsafe_allow_html=True
    )


show_evaluation()
