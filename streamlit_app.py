import streamlit as st
import json

# Load data from the streamlit.json file
def load_data():
    with open('streamlit.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Create the Streamlit app layout
def app():
    st.sidebar.title("🎯 Smart Resume Matching")

    # Load the data from streamlit.json
    data = load_data()

    # Broker websites (can be replaced with actual data)
    broker_websites = ["Upgraded.se"]

    # Sidebar options
    selected_broker = st.sidebar.selectbox("🌐 Choose a Broker Website:", broker_websites)

    # Get a list of all user IDs and names
    user_ids = [user['UserID'] for user in data]
    user_names = {user['UserID']: f"{user['UserName']} (ID: {user['UserID']})" for user in data}

    # Sidebar options for consultant selection and sorting
    selected_user_id = st.sidebar.selectbox("👤 Choose a Consultant:", user_ids, format_func=lambda x: user_names[x])
    sorting_options = ["⬆️ Highest Match Score", "⬇️ Lowest Match Score"]
    selected_sorting = st.sidebar.selectbox("📊 Choose Sorting:", sorting_options)

    # Retrieve selected user's data
    selected_user = next(user for user in data if user['UserID'] == selected_user_id)

    # Filter and sort matches
    matches = selected_user["Matches"]
    matches = sorted(matches, key=lambda x: x["SkillMatch"], reverse=(selected_sorting == "⬆️ Highest Match Score"))

    # Main section - Titles
    st.markdown("<h1 style='text-align: center; font-size: 30px;'>🎯 Smart Resume Matching Tool</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; font-size: 24px;'>Consultant: {selected_user['UserName']} (ID: {selected_user['UserID']})</h3>", unsafe_allow_html=True)
    st.write(f"🌐 Showing results for broker: {selected_broker}")

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
    .oval-skill {
        background-color: #e0e0e0;
        border-radius: 25px;
        padding: 5px 15px;
        display: inline-block;
        margin: 5px 5px;
        font-size: 14px;
    }
    .skill-container {
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Table header with icons
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
        job_role = match["Joblist"]
        match_score = f"{match['SkillMatch']}"
        job_link = match["Link"]

        # Display the data in a row using markdown with inline styles for columns
        col1, col2, col3 = st.columns([4, 4, 5])
        col1.markdown(f"<div style='font-size:20px;'>📋 {job_role}</div>", unsafe_allow_html=True)
        col2.markdown(f"<div style='font-size:20px;'>📈 {match_score}</div>", unsafe_allow_html=True)
        col3.markdown(f"<div style='font-size:20px;'>🔗 <a href='{job_link}'>View Job</a></div>", unsafe_allow_html=True)

        # Manage state for MustHave and ShouldHave buttons
        if f"musthave_shown_{job_role}" not in st.session_state:
            st.session_state[f"musthave_shown_{job_role}"] = False
        if f"shouldhave_shown_{job_role}" not in st.session_state:
            st.session_state[f"shouldhave_shown_{job_role}"] = False

        # Display missing skills with expander
        with st.expander("🚫 Missing Skills", expanded=False):
            # MustHave Skills
            if st.button(f"Show MustHave Skills", key=f"MustHaveButton_{job_role}"):
                st.session_state[f"musthave_shown_{job_role}"] = not st.session_state[f"musthave_shown_{job_role}"]

            if st.session_state[f"musthave_shown_{job_role}"]:
                st.markdown('<div class="skill-container">', unsafe_allow_html=True)
                for skill in match["MissedSkills"].get("MustHave", []):
                    st.markdown(f"<span class='oval-skill'>{skill}</span>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ShouldHave Skills
            if st.button(f"Show ShouldHave Skills", key=f"ShouldHaveButton_{job_role}"):
                st.session_state[f"shouldhave_shown_{job_role}"] = not st.session_state[f"shouldhave_shown_{job_role}"]

            if st.session_state[f"shouldhave_shown_{job_role}"]:
                st.markdown('<div class="skill-container">', unsafe_allow_html=True)
                for skill in match["MissedSkills"].get("ShouldHave", []):
                    st.markdown(f"<span class='oval-skill'>{skill}</span>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

# Run the app
if __name__ == "__main__":
    app()
