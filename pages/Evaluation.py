import streamlit as st
import os
import pandas as pd

from utils import (
    delete_evaluation,
    get_table_download_link,
    get_performance_table_download_link,
    next_text_pair,
    previous_text_pair,
    save_evaluation,
    add_and_update_evals,
    delete_and_update_evals,
)

st.write("# Evaluation")
st.write("Make sure that you have carefully read the guidelines presented in the Instructions page.")

# Load the CSV file
#file_path = "data.csv"  # Update this to the correct path if needed
file_path = "data_full_supreme.csv"  # Update this to the correct path if needed
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

    # Initialize mean results with empty rows and load it into session state
    if "mean_df" not in st.session_state:
        if not os.path.exists("model_performances/results_mean.csv"):
            empty_df = pd.DataFrame(
                columns=[
                    "model_id",
                    "adequacy",
                    "fluency",
                    "simplicity",
                ]
            )
            empty_df.to_csv("model_performances/results_mean.csv", index=False)
        st.session_state.mean_df = pd.read("model_performances/results_mean.csv")
    
    if "std_df" not in st.session_state:
        if not os.path.exists("model_performances/results_std.csv"):
            empty_df = pd.DataFrame(
                columns=[
                    "model_id",
                    "adequacy",
                    "fluency",
                    "simplicity",
                ]
            )
            empty_df.to_csv("model_performances/results_std.csv", index=False)
        st.session_state.std_df = pd.read("model_performances/results_std.csv")    

    # Display navigation controls
    st.sidebar.write("### Navigation")
    total_pairs = len(data)
    st.sidebar.slider(
        "Go to text pair",
        min_value=1,
        max_value=total_pairs,
        value=st.session_state.current_index + 1,
        key="slider",
        on_change=lambda: st.session_state.update(
            {"current_index": st.session_state.slider - 1}
        ),
    )
    st.sidebar.text_input(
        "Jump to text pair",
        key="jump_to",
        on_change=lambda: st.session_state.update(
            {"current_index": int(st.session_state.jump_to) - 1}
        ),
    )

    # Dropdown for evaluated and non-evaluated pairs
    evaluated_ids = st.session_state.results_df["id"].tolist()
    non_evaluated_ids = [i for i in data["id"].tolist() if i not in evaluated_ids]

    selected_evaluated = st.sidebar.selectbox(
        "Evaluated pairs",
        options=[None] + evaluated_ids,
        key="evaluated_select",
        on_change=lambda: st.session_state.update(
            {
                "current_index": data.index[
                    data["id"] == st.session_state.evaluated_select
                ][0]
            }
            if st.session_state.evaluated_select
            else None
        ),
    )
    selected_non_evaluated = st.sidebar.selectbox(
        "Non-evaluated pairs",
        options=[None] + non_evaluated_ids,
        key="non_evaluated_select",
        on_change=lambda: st.session_state.update(
            {
                "current_index": data.index[
                    data["id"] == st.session_state.non_evaluated_select
                ][0]
            }
            if st.session_state.non_evaluated_select
            else None
        ),
    )

    # Display the current text pair
    index = st.session_state.current_index
    st.write(f"# Text Pair {index + 1}/{total_pairs}")

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.button(
            "Previous",
            on_click=previous_text_pair,
            key="previous",
            use_container_width=True,
            type="primary",
        )
    with col2:
        st.button(
            "Next",
            on_click=next_text_pair,
            key="next",
            use_container_width=True,
            type="primary",
        )

    st.write(f"## Sentence Label: {1+index//11}")

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
        st.session_state.model_id = existing_evaluation["model_id"]
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

    # Action buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button(
            "Save Evaluation",
            #on_click=save_evaluation,
            on_click=add_and_update_evals,
            key="save",
            use_container_width=True,
            type="primary",
        )
    with col2:
        st.button(
            "Delete Evaluation",
            on_click=delete_and_update_evals,
            key="delete",
            use_container_width=True,
            type="primary",
        )

    # Display current results table at the bottom of the page
    st.write("#### Current Results")
    st.write(st.session_state.results_df)

    # Provide a download link for the updated results.csv
    st.markdown(
        get_table_download_link(st.session_state.results_df), unsafe_allow_html=True
    )
    st.markdown(
        get_performance_table_download_link(st.session_state.mean_df, st.session_state.std_df), unsafe_allow_html=True
    )

try:
    show_evaluation()
except Exception as e:
    print("Error: ", e)
