import streamlit as st
import pandas as pd
import os

# File paths for storing data
SUGGESTIONS_FILE = 'suggestions.csv'
POLL_RESULTS_FILE = 'poll_results.csv'

# Load or initialize data
if os.path.exists(SUGGESTIONS_FILE):
    suggestions_df = pd.read_csv(SUGGESTIONS_FILE)
else:
    suggestions_df = pd.DataFrame(columns=['name', 'gender'])

if os.path.exists(POLL_RESULTS_FILE):
    poll_results_df = pd.read_csv(POLL_RESULTS_FILE)
    poll_results = poll_results_df.to_dict('records')[0]
else:
    poll_results = {"boy": 0, "girl": 0}

# Title of the app
st.title("Baby Shower App")

# Section for Name Suggestions
st.header("Name Suggestions")

# Form for submitting name suggestions
with st.form("suggest_name_form"):
    gender = st.selectbox("Select gender:", ["boy", "girl"])
    name = st.text_input("Enter a name:")
    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if name:
            new_suggestion = pd.DataFrame({'name': [name], 'gender': [gender]})
            suggestions_df = pd.concat([suggestions_df, new_suggestion], ignore_index=True)
            suggestions_df.to_csv(SUGGESTIONS_FILE, index=False)
            st.success(f"Name suggestion '{name}' for a {gender} added.")
        else:
            st.error("Please enter a name.")

# Display the current suggestions in separate columns for boys and girls
st.subheader("Current Suggestions")

# Create columns for displaying suggestions
col1, col2 = st.columns(2)

# Display boy suggestions in the first column
with col1:
    st.subheader("Boys")
    boy_suggestions = suggestions_df[suggestions_df['gender'] == 'boy']['name']
    if not boy_suggestions.empty:
        for suggestion in boy_suggestions:
            st.write(suggestion)
    else:
        st.write("No boy suggestions yet.")

# Display girl suggestions in the second column
with col2:
    st.subheader("Girls")
    girl_suggestions = suggestions_df[suggestions_df['gender'] == 'girl']['name']
    if not girl_suggestions.empty:
        for suggestion in girl_suggestions:
            st.write(suggestion)
    else:
        st.write("No girl suggestions yet.")

# Section for Voting on the Baby's Gender
st.header("Guess the Baby's Gender")

# Create columns for side-by-side voting
col1, col2 = st.columns(2)

with col1:
    if st.button('Vote for Boy'):
        poll_results["boy"] += 1
        pd.DataFrame([poll_results]).to_csv(POLL_RESULTS_FILE, index=False)
        st.success("Vote for boy recorded.")

with col2:
    if st.button('Vote for Girl'):
        poll_results["girl"] += 1
        pd.DataFrame([poll_results]).to_csv(POLL_RESULTS_FILE, index=False)
        st.success("Vote for girl recorded.")

# Display the current poll results as progress bars with custom colors
st.subheader("Poll Results")

# Calculate total votes
total_votes = poll_results['boy'] + poll_results['girl']

# Display progress bars with associated labels using st.text
if total_votes > 0:
    st.text(f"Boys: {poll_results['boy']}")
    st.markdown(
        f'<div style="background-color: #6a99ff; width: {poll_results["boy"]/total_votes*100}%; height: 25px; border-radius: 5px;"></div>',
        unsafe_allow_html=True
    )

    st.text(f"Girls: {poll_results['girl']}")
    st.markdown(
        f'<div style="background-color: #ff6699; width: {poll_results["girl"]/total_votes*100}%; height: 25px; border-radius: 5px;"></div>',
        unsafe_allow_html=True
    )
else:
    st.warning("No votes recorded yet.")
