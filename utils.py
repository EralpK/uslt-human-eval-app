import base64

import pandas as pd
import streamlit as st

from datamodule.configs import ModelNames


data = pd.read_csv("data_full_supreme.csv")


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

    results_df.to_csv("results.csv", index=False)
    st.session_state.results_df = results_df
    st.success("Evaluation saved!")

    # Provide a download link for the updated results.csv
    st.markdown(get_table_download_link(results_df), unsafe_allow_html=True)


def compute_evaluation_avgs():
    """
    To compute the mean and standard deviation of model performances.
    Note that this is only called when either a new evaluation is saved or an evaluation is deleted.
    Manual insertions and deletions over the results file are not automatically reflected over the average performances.
    """
    avg_data = []
    std_data = []
    #results = pd.read_csv(results_file_path)
    results = st.session_state.results_df
    all_model_ids = results["model_id"].unique()
    for model in ModelNames:
        if model.name in all_model_ids:
            model_id_results = results.loc[results["model_id"]==model.name]
            adequacy = model_id_results["adequacy"].mean()
            fluency = model_id_results["fluency"].mean()
            simplicity = model_id_results["simplicity"].mean()
            avg_data.append(
                {
                    "model_id": model.name,
                    "adequacy": adequacy,
                    "fluency": fluency,
                    "simplicity": simplicity,
                }
            )
            adequacy_std = model_id_results["adequacy"].std()
            fluency_std = model_id_results["fluency"].std()
            simplicity_std = model_id_results["simplicity"].std()
            std_data.append(
                {
                    "model_id": model.name,
                    "adequacy": adequacy_std,
                    "fluency": fluency_std,
                    "simplicity": simplicity_std,
                }
            )
    avg_df = pd.DataFrame(avg_data)
    avg_df.to_csv("model_performances_mean.csv")
    std_df = pd.DataFrame(std_data)
    std_df.to_csv("model_performances_std.csv")


def add_and_update_evals():
    save_evaluation()
    compute_evaluation_avgs()


def delete_evaluation():
    results_df = st.session_state.results_df
    current_id = int(data.iloc[st.session_state.current_index]["id"])

    if current_id in results_df["id"].values:
        results_df = results_df[results_df["id"] != current_id]
        results_df.to_csv("results.csv", index=False)
        st.session_state.results_df = results_df
        st.success("Evaluation deleted!")
    else:
        st.warning("No evaluation to delete for this text pair.")


def delete_and_update_evals():
    delete_evaluation()
    compute_evaluation_avgs()


def get_table_download_link(df: pd.DataFrame):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # B64 encode
    href = f'<a class="download-button" href="data:file/csv;base64,{b64}" download="results.csv">Download results.csv</a>'
    return f'<div style="text-align: center; margin-top: 20px;">{href}</div>'
