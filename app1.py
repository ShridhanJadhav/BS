import streamlit as st

# Initialize session state if not already done
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

if 'poll_results' not in st.session_state:
    st.session_state.poll_results = {"boy": 0, "girl": 0}

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
            st.session_state.suggestions.append({'name': name, 'gender': gender})
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
    boy_suggestions = [suggestion['name'] for suggestion in st.session_state.suggestions if suggestion['gender'] == 'boy']
    if boy_suggestions:
        for suggestion in boy_suggestions:
            st.write(suggestion)
    else:
        st.write("No boy suggestions yet.")

# Display girl suggestions in the second column
with col2:
    st.subheader("Girls")
    girl_suggestions = [suggestion['name'] for suggestion in st.session_state.suggestions if suggestion['gender'] == 'girl']
    if girl_suggestions:
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
        st.session_state.poll_results["boy"] += 1
        st.success("Vote for boy recorded.")

with col2:
    if st.button('Vote for Girl'):
        st.session_state.poll_results["girl"] += 1
        st.success("Vote for girl recorded.")

# Display the current poll results as progress bars with custom colors
st.subheader("Poll Results")

# Calculate total votes
total_votes = st.session_state.poll_results['boy'] + st.session_state.poll_results['girl']

# Display progress bars with associated labels using st.text
if total_votes > 0:
    st.text(f"Boys: {st.session_state.poll_results['boy']}")
    st.markdown(
        f'<div style="background-color: #6a99ff; width: {st.session_state.poll_results["boy"]/total_votes*100}%; height: 25px; border-radius: 5px;"></div>',
        unsafe_allow_html=True
    )

    st.text(f"Girls: {st.session_state.poll_results['girl']}")
    st.markdown(
        f'<div style="background-color: #ff6699; width: {st.session_state.poll_results["girl"]/total_votes*100}%; height: 25px; border-radius: 5px;"></div>',
        unsafe_allow_html=True
    )
else:
    st.warning("No votes recorded yet.")