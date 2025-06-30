import streamlit as st
from vapi_python import Vapi

# Hardcoded API configuration
API_KEY = "be55f3ed-dde7-4cc1-8ac4-be6d1efd30bc"
DEFAULT_ASSISTANT_ID = "dffb2e5c-7d59-462b-a8aa-48746ea70cb1"

# Predefined agent configurations
AGENT_CONFIGS = [
    {"name": "Agent CEO", "assistant_id": "bf161516-6d88-490c-972e-274098a6b51a", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Social", "assistant_id": "bf161516-6d88-490c-972e-274098a6b51a", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Mindset", "assistant_id": "4fe7083e-2f28-4502-b6bf-4ae6ea71a8f4", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Blogger", "assistant_id": "f8ef1ad5-5281-42f1-ae69-f94ff7acb453", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Grant", "assistant_id": "7673e69d-170b-4319-bdf4-e74e5370e98a", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Prayer AI", "assistant_id": "339cdad6-9989-4bb6-98ed-bd15521707d1", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Metrics", "assistant_id": "4820eab2-adaf-4f17-a8a0-30cab3e3f007", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Researcher", "assistant_id": "f05c182f-d3d1-4a17-9c79-52442a9171b8", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Investor", "assistant_id": "1008771d-86ca-472a-a125-7a7e10100297", "phone_number_id": "431f1dc9-4888-41e6-933c-4fa2e97d34d6"},
    {"name": "Agent Newsroom", "assistant_id": "76f1d6e5-cab4-45b8-9aeb-d3e6f3c0c019", "phone_number_id": "c2f011d6-7855-4e00-8784-550e568c31ef"},
    {"name": "STREAMLIT Agent", "assistant_id": "538258da-0dda-473d-8ef8-5427251f3ad5", "phone_number_id": "c2f011d6-7855-4e00-8784-550e568c31ef"},
    {"name": "HTML/CSS Agent", "assistant_id": "14b94e2f-299b-4e75-a445-a4f5feacc522", "phone_number_id": "c2f011d6-7855-4e00-8784-550e568c31ef"},
    {"name": "Business Plan Agent", "assistant_id": "87d59105-723b-427e-a18d-da99fbf28608", "phone_number_id": "c2f011d6-7855-4e00-8784-550e568c31ef"},
    {"name": "Ecom Agent", "assistant_id": "d56551f8-0447-468a-872b-eaa9f830993d", "phone_number_id": "c2f011d6-7855-4e00-8784-550e568c31ef"},
    {"name": "Agent Health", "assistant_id": "7b2b8b86-5caa-4f28-8c6b-e7d3d0404f06", "phone_number_id": "c2f011d6-7855-4e00-8784-550e568c31ef"},
    {"name": "Cinch Closer", "assistant_id": "232f3d9c-18b3-4963-bdd9-e7de3be156ae", "phone_number_id": "c2f011d6-7855-4e00-8784-550e568c31ef"},
    {"name": "DISC Agent", "assistant_id": "41fe59e1-829f-4936-8ee5-eef2bb1287fe", "phone_number_id": "c2f011d6-7855-4e00-8784-550e568c31ef"},
]

# Agent type descriptions
AGENT_DESCRIPTIONS = {
    "Agent CEO": "Executive leadership and strategic business guidance",
    "Agent Social": "Social media management and community engagement",
    "Agent Mindset": "Personal development and mindset coaching",
    "Agent Blogger": "Content creation and blogging expertise",
    "Agent Grant": "Grant writing and funding opportunities",
    "Agent Prayer AI": "Spiritual guidance and prayer support",
    "Agent Metrics": "Data analysis and performance metrics",
    "Agent Researcher": "Research and information gathering",
    "Agent Investor": "Investment advice and financial planning",
    "Agent Newsroom": "News curation and journalism support",
    "STREAMLIT Agent": "Streamlit application development",
    "HTML/CSS Agent": "Web development and design",
    "Business Plan Agent": "Business planning and strategy development",
    "Ecom Agent": "E-commerce and online retail expertise",
    "Agent Health": "Health and wellness guidance",
    "Cinch Closer": "Sales closing and negotiation",
    "DISC Agent": "DISC personality assessment and coaching",
}

# Page configuration
st.set_page_config(
    page_title="AI Agent Caller",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .agent-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f9f9f9;
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-inactive {
        color: #dc3545;
        font-weight: bold;
    }
    .call-controls {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "vapi" not in st.session_state:
    try:
        st.session_state.vapi = Vapi(api_key=API_KEY)
        st.session_state.call_active = False
        st.session_state.current_agent = None
        st.session_state.call_logs = []
    except Exception as e:
        st.error(f"❌ Failed to initialize Vapi client: {e}")
        st.session_state.vapi = None

# Header
st.markdown("""
<div class="main-header">
    <h1>📞 AI Agent Caller</h1>
    <p>Connect with specialized AI agents for various business needs</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    
    # API Status
    if st.session_state.get("vapi"):
        st.success("✅ API Connected")
    else:
        st.error("❌ API Not Connected")
    
    st.markdown("---")
    
    # Call Status
    st.header("📊 Call Status")
    if st.session_state.get("call_active"):
        st.markdown('<p class="status-active">🟢 Call Active</p>', unsafe_allow_html=True)
        if st.session_state.get("current_agent"):
            st.info(f"Connected to: {st.session_state.current_agent['name']}")
    else:
        st.markdown('<p class="status-inactive">🔴 No Active Call</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.header("⚡ Quick Actions")
    if st.button("📋 View All Agents"):
        st.session_state.show_agent_list = True
    
    if st.button("📞 Emergency Stop All"):
        if st.session_state.get("vapi") and st.session_state.get("call_active"):
            try:
                st.session_state.vapi.stop()
                st.session_state.call_active = False
                st.session_state.current_agent = None
                st.success("🛑 All calls stopped")
            except Exception as e:
                st.error(f"Error stopping calls: {e}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🤖 Select Your AI Agent")
    
    # User information
    with st.expander("👤 User Information", expanded=True):
        user_name = st.text_input("Your Name (for personalized greeting):", placeholder="Enter your name...")
        user_company = st.text_input("Company (optional):", placeholder="Your company name...")
        user_purpose = st.text_area("Call Purpose (optional):", placeholder="Brief description of what you need help with...")
    
    # Agent selection
    st.subheader("Choose an Agent:")
    
    # Create agent selection grid
    cols = st.columns(3)
    selected_agent = None
    
    for i, agent in enumerate(AGENT_CONFIGS):
        col_idx = i % 3
        with cols[col_idx]:
            agent_description = AGENT_DESCRIPTIONS.get(agent["name"], "Specialized AI assistant")
            
            if st.button(
                f"📞 {agent['name']}", 
                key=f"agent_{i}",
                help=agent_description,
                use_container_width=True
            ):
                selected_agent = agent
                st.session_state.selected_agent = agent
    
    # Display selected agent info
    if st.session_state.get("selected_agent"):
        selected_agent = st.session_state.selected_agent
        st.success(f"✅ Selected: {selected_agent['name']}")
        st.info(f"Description: {AGENT_DESCRIPTIONS.get(selected_agent['name'], 'Specialized AI assistant')}")

with col2:
    st.header("🎮 Call Controls")
    
    with st.container():
        st.markdown('<div class="call-controls">', unsafe_allow_html=True)
        
        # Start Call Button
        if st.button(
            "▶️ Start Call", 
            type="primary",
            disabled=not st.session_state.get("selected_agent") or st.session_state.get("call_active"),
            use_container_width=True
        ):
            if st.session_state.get("vapi") and st.session_state.get("selected_agent"):
                try:
                    agent = st.session_state.selected_agent
                    
                    # Prepare variable overrides
                    overrides = {}
                    if user_name:
                        overrides["variableValues"] = {"name": user_name}
                        if user_company:
                            overrides["variableValues"]["company"] = user_company
                        if user_purpose:
                            overrides["variableValues"]["purpose"] = user_purpose
                    
                    # Start the call
                    st.session_state.vapi.start(
                        assistant_id=agent["assistant_id"],
                        assistant_overrides=overrides if overrides else None
                    )
                    
                    st.session_state.call_active = True
                    st.session_state.current_agent = agent
                    
                    # Log the call
                    import datetime
                    call_log = {
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "agent": agent["name"],
                        "user": user_name or "Anonymous",
                        "status": "Started"
                    }
                    st.session_state.call_logs.append(call_log)
                    
                    st.success(f"📞 Call started with {agent['name']}")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error starting call: {e}")
        
        # Stop Call Button
        if st.button(
            "⛔ Stop Call", 
            type="secondary",
            disabled=not st.session_state.get("call_active"),
            use_container_width=True
        ):
            if st.session_state.get("vapi"):
                try:
                    st.session_state.vapi.stop()
                    st.session_state.call_active = False
                    
                    # Log the call end
                    if st.session_state.call_logs:
                        st.session_state.call_logs[-1]["status"] = "Ended"
                    
                    st.session_state.current_agent = None
                    st.success("📴 Call stopped")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error stopping call: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Call Information
        if st.session_state.get("call_active") and st.session_state.get("current_agent"):
            st.markdown("---")
            st.subheader("📋 Current Call Info")
            agent = st.session_state.current_agent
            st.write(f"**Agent:** {agent['name']}")
            st.write(f"**Assistant ID:** {agent['assistant_id'][:8]}...")
            st.write(f"**User:** {user_name or 'Anonymous'}")
            if user_company:
                st.write(f"**Company:** {user_company}")

# Agent List Modal
if st.session_state.get("show_agent_list"):
    st.header("📋 All Available Agents")
    
    for agent in AGENT_CONFIGS:
        with st.expander(f"🤖 {agent['name']}", expanded=False):
            st.write(f"**Description:** {AGENT_DESCRIPTIONS.get(agent['name'], 'Specialized AI assistant')}")
            st.write(f"**Assistant ID:** {agent['assistant_id']}")
            st.write(f"**Phone Number ID:** {agent['phone_number_id']}")
    
    if st.button("❌ Close Agent List"):
        st.session_state.show_agent_list = False
        st.rerun()

# Call History
if st.session_state.get("call_logs"):
    st.header("📞 Call History")
    
    for i, log in enumerate(reversed(st.session_state.call_logs[-5:])):  # Show last 5 calls
        with st.expander(f"Call {len(st.session_state.call_logs) - i}: {log['agent']} - {log['timestamp']}", expanded=False):
            st.write(f"**Agent:** {log['agent']}")
            st.write(f"**User:** {log['user']}")
            st.write(f"**Time:** {log['timestamp']}")
            st.write(f"**Status:** {log['status']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 AI Agent Caller - Powered by Vapi | Built with Streamlit</p>
    <p>💡 Need help? Select an agent and start a conversation!</p>
</div>
""", unsafe_allow_html=True)
