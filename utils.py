import base64

import pandas as pd
import streamlit as st

data = pd.read_csv("data.csv")


def next_text_pair():
    if st.session_state.current_index < len(data) - 1:
        st.session_state.current_index += 1


def previous_text_pair():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1


def save_evaluation():
    evaluation = {
        "id": int(data.iloc[st.session_state.current_index]["id"]),
        "original_text_id": int(
            data.iloc[st.session_state.current_index]["original_text_id"]
        ),
        "model_id": data.iloc[st.session_state.current_index]["model_id"],
        "adequacy": int(st.session_state.adequacy),
        "fluency": int(st.session_state.fluency),
        "simplicity": int(st.session_state.simplicity),
    }

    # Check if the current text pair has already been evaluated
    results_df = st.session_state.results_df
    if evaluation["id"] in results_df["id"].values:
        st.warning(
            "This pair is already evaluated. If you like to change your evaluation, please feel free."
        )
        # Update the existing evaluation
        results_df.loc[
            results_df["id"] == evaluation["id"], ["adequacy", "fluency", "simplicity"]
        ] = (evaluation["adequacy"], evaluation["fluency"], evaluation["simplicity"])
    else:
        # Append new evaluation
        results_df = pd.concat(
            [results_df, pd.DataFrame([evaluation])], ignore_index=True
        )
    results_df.sort_values("id", inplace=True)
    results_df.to_csv("results.csv", index=False)
    st.session_state.results_df = results_df
    st.success("Evaluation saved!")

    # Provide a download link for the updated results.csv
    st.markdown(get_table_download_link(results_df), unsafe_allow_html=True)


def get_table_download_link(df: pd.DataFrame):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # B64 encode
    href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download results.csv</a>'
    return href
