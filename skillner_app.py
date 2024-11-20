import streamlit as st
import json

# Load data from the matchingResults.json file
def load_data():
    with open('matchingResults.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Create the Streamlit app layout
def app():
    st.sidebar.title("🎯 Smart Resume Matching")

    # Load the data from matchingResults.json
    data = load_data()

    # Broker websites (can be replaced with actual data)
    broker_websites = ["Upgraded.se"]

    # Sidebar options
    selected_broker = st.sidebar.selectbox("🌐 Choose a Broker Website:", broker_websites)

    # Sidebar options
    user_ids = [user['userId'] for user in data]
    user_names = {user['userId']: f"{user['userName']} (ID: {user['userId']})" for user in data}
    selected_user_id = st.sidebar.selectbox("👤 Choose a Consultant:", user_ids, format_func=lambda x: user_names[x])

    sorting_options = ["⬆️ Highest Match Score", "⬇️ Lowest Match Score"]
    selected_sorting = st.sidebar.selectbox("📊 Choose Sorting:", sorting_options)

    # Find the selected user's data
    selected_user = next(user for user in data if user['userId'] == selected_user_id)

    # Filter and sort matches
    matches = selected_user["matches"]
    matches = sorted(matches, key=lambda x: float(x["skillMatch"].strip('%')), reverse=(selected_sorting == "⬆️ Highest Match Score"))

    # Main section - Titles
    st.markdown("<h1 style='text-align: center; font-size: 30px;'> Smart Resume Matching Tool</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; font-size: 24px;'>Consultant: {selected_user['userName']} (ID: {selected_user['userId']})</h3>", unsafe_allow_html=True)

    # Display a stylish table header
    st.markdown("""
    <style>
    .table-header {
        font-weight: bold;
        font-size: 18px;
        color: #333;
        background-color: #f2f2f2;
        padding: 8px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="table-header">
    <div style="width: 30%; display: inline-block;">📋 Role</div>
    <div style="width: 35%; display: inline-block;">📈 Match Score</div>
    <div style="width: 30%; display: inline-block;">🔗 Link</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Display rows of data
    for match in matches:
        job_role = ", ".join(match["roles"])  # Join multiple roles if present
        match_score = f"{match['skillMatch']}"
        job_link = match["jobLink"]

        # Display the data in a row using markdown with inline styles for columns
        col1, col2, col3 = st.columns([4, 4, 5])
        col1.markdown(f"<div style='font-size:20px;'> ○ {job_role}</div>", unsafe_allow_html=True)
        col2.markdown(f"<div style='font-size:20px;'> {match_score}</div>", unsafe_allow_html=True)
        col3.markdown(f"<div style='font-size:20px;'> <a href='{job_link}'>View Job in upgraded.se</a></div>", unsafe_allow_html=True)

        # Add a horizontal line between each row for better spacing
        st.markdown("<hr style='border: 1px solid #ddd;'/>", unsafe_allow_html=True)

    st.markdown("---")

# Run the app
if __name__ == "__main__":
    app()
