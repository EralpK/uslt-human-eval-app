import os

import pandas as pd
import streamlit as st


# Generate simple text pairs
def generate_text_pairs(num_pairs=20):
    text_pairs = []
    for i in range(1, num_pairs + 1):
        reference_text = f"Reference text {i}"
        generated_text = f"Generated text {i}"
        text_pairs.append(
            {"id": i, "reference": reference_text, "generated": generated_text}
        )
    return text_pairs


# Load existing evaluations
def load_evaluations(filename="evaluations.csv"):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(
            columns=[
                "text_pair_id",
                "reference",
                "generated",
                "Fluency",
                "Relevance",
                "Coherence",
            ]
        )


# Save new evaluations to CSV file
def save_evaluations_to_csv(evaluations, filename="evaluations.csv"):
    df = pd.DataFrame(evaluations)
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.sort_values(by=["text_pair_id"], inplace=True)
    df.to_csv(filename, index=False)
    st.success(f"Evaluations saved to {filename}")


# Generate 20 text pairs
text_pairs = generate_text_pairs(20)
text_pairs = sorted(text_pairs, key=lambda x: x["id"])

# Load existing evaluations
evaluations_df = load_evaluations()

# Initialize session state
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "evaluated_pairs" not in st.session_state:
    st.session_state.evaluated_pairs = evaluations_df["text_pair_id"].tolist()
if "non_evaluated_pairs" not in st.session_state:
    st.session_state.non_evaluated_pairs = [
        pair["id"]
        for pair in text_pairs
        if pair["id"] not in st.session_state.evaluated_pairs
    ]

# Sidebar
st.sidebar.header("Text Pairs")
st.sidebar.subheader("Evaluated Text Pairs")
for pair_id in st.session_state.evaluated_pairs:
    if st.sidebar.button(f"Text Pair {pair_id}"):
        st.session_state.current_index = pair_id - 1
        st.rerun()

st.sidebar.subheader("Non-Evaluated Text Pairs")
for pair_id in st.session_state.non_evaluated_pairs:
    if st.sidebar.button(f"Text Pair {pair_id}"):
        st.session_state.current_index = pair_id - 1
        st.rerun()

# Metrics
metrics = ["Fluency", "Relevance", "Coherence"]

# Display current text pair
current_pair = text_pairs[st.session_state.current_index]
st.subheader(f"Text Pair {current_pair['id']}")
st.write(f"**Reference Text:** {current_pair['reference']}")
st.write(f"**Generated Text:** {current_pair['generated']}")

# Check if current pair has been evaluated
existing_evaluation = evaluations_df[
    evaluations_df["text_pair_id"] == current_pair["id"]
]
evaluation = {
    "text_pair_id": current_pair["id"],
    "reference": current_pair["reference"],
    "generated": current_pair["generated"],
}

# Display evaluation status message
if not existing_evaluation.empty:
    st.info(
        "This text pair has already been evaluated. If you would like to change it, please feel free to do so."
    )

for metric in metrics:
    if not existing_evaluation.empty:
        evaluation[metric] = existing_evaluation[metric].values[0]
    else:
        evaluation[metric] = 3

    options = [1, 2, 3, 4, 5]
    evaluation[metric] = st.radio(
        f"{metric} (1-5)",
        options,
        index=options.index(evaluation[metric]),
        key=f"{metric}_{current_pair['id']}",
        horizontal=True,
    )


# Save evaluation
def save_evaluation():
    new_eval = pd.DataFrame([evaluation])
    if os.path.exists("evaluations.csv"):
        existing_df = pd.read_csv("evaluations.csv")
        existing_df = existing_df[
            existing_df["text_pair_id"] != evaluation["text_pair_id"]
        ]
        updated_df = pd.concat([existing_df, new_eval], ignore_index=True)
    else:
        updated_df = new_eval
    updated_df.sort_values(by=["text_pair_id"], inplace=True)
    updated_df.to_csv("evaluations.csv", index=False)
    st.success("Evaluation saved")

    # Update evaluated and non-evaluated pairs
    if current_pair["id"] not in st.session_state.evaluated_pairs:
        st.session_state.evaluated_pairs.append(current_pair["id"])
    if current_pair["id"] in st.session_state.non_evaluated_pairs:
        st.session_state.non_evaluated_pairs.remove(current_pair["id"])
    return updated_df


# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("Previous") and st.session_state.current_index > 0:
        st.session_state.current_index -= 1
        st.rerun()
with col2:
    if st.button("Next") and st.session_state.current_index < len(text_pairs) - 1:
        st.session_state.current_index += 1
        st.rerun()
with col3:
    if st.button("Submit Evaluation"):
        evaluations_df = save_evaluation()
        st.rerun()

# Display collected evaluations for debugging purposes
st.write("Collected Evaluations (for debugging):")
st.write(evaluations_df)
