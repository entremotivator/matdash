import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import uuid

# Page configuration
st.set_page_config(
    page_title="Outbound Laundromat CRM", 
    layout="wide",
    page_icon="🧺",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
    }
    .call-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .call-button:hover {
        background-color: #45a049;
    }
    .status-pending {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    .status-progress {
        background-color: #cce5ff;
        color: #004085;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    .status-completed {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Load demo data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("demo_leads.csv")
    except FileNotFoundError:
        # Create empty dataframe with required columns if file doesn't exist
        columns = [
            "Full Name", "First Name", "Last Name", "Phone", "Email", "Order ID",
            "Pickup Time", "Status", "Wash", "Dry", "Pounds", "Special Instructions",
            "Total Cost", "Address", "Time Window", "Call Status", "Follow Up Required"
        ]
        return pd.DataFrame(columns=columns)

# Initialize session state
if 'leads' not in st.session_state:
    st.session_state.leads = load_data()

if 'call_history' not in st.session_state:
    st.session_state.call_history = []

# Sidebar: VAPI credentials and settings
st.sidebar.markdown("## 🔧 VAPI Settings")
st.sidebar.markdown("---")

vapi_key = st.sidebar.text_input(
    "VAPI API Key", 
    type="password",
    help="Enter your VAPI API key for making calls"
)

agent_id = st.sidebar.text_input(
    "Agent ID",
    help="Enter your VAPI Agent ID"
)

# Additional VAPI settings
st.sidebar.markdown("### Call Settings")
call_timeout = st.sidebar.slider("Call Timeout (seconds)", 30, 300, 120)
auto_record = st.sidebar.checkbox("Auto Record Calls", value=True)

# Connection status
if vapi_key and agent_id:
    st.sidebar.success("✅ VAPI Configured")
else:
    st.sidebar.warning("⚠️ VAPI Not Configured")

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
total_leads = len(st.session_state.leads)
pending_leads = len(st.session_state.leads[st.session_state.leads['Status'] == 'Pending'])
completed_leads = len(st.session_state.leads[st.session_state.leads['Status'] == 'Completed'])

st.sidebar.metric("Total Leads", total_leads)
st.sidebar.metric("Pending", pending_leads)
st.sidebar.metric("Completed", completed_leads)

# Main content
st.markdown("""
<div class="main-header">
    <h1>🧺 Outbound Laundromat CRM</h1>
    <p>Manage your laundromat leads and make calls with VAPI integration</p>
</div>
""", unsafe_allow_html=True)

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📋 Lead Management", "📞 Call Center", "➕ Add New Lead", "📊 Analytics"])

with tab1:
    st.subheader("Lead Database")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed"])
    with col2:
        follow_up_filter = st.selectbox("Follow Up Required", ["All", "Yes", "No"])
    with col3:
        call_status_filter = st.selectbox("Call Status", ["All", "Not Called", "Confirmed", "Voicemail Left", "No Answer", "Busy Line", "Rescheduled"])
    
    # Apply filters
    filtered_leads = st.session_state.leads.copy()
    
    if status_filter != "All":
        filtered_leads = filtered_leads[filtered_leads['Status'] == status_filter]
    if follow_up_filter != "All":
        filtered_leads = filtered_leads[filtered_leads['Follow Up Required'] == follow_up_filter]
    if call_status_filter != "All":
        filtered_leads = filtered_leads[filtered_leads['Call Status'] == call_status_filter]
    
    # Display and edit leads
    if not filtered_leads.empty:
        edited_df = st.data_editor(
            filtered_leads,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Phone": st.column_config.TextColumn("Phone", width="medium"),
                "Email": st.column_config.TextColumn("Email", width="medium"),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Pending", "In Progress", "Completed"],
                    width="small"
                ),
                "Call Status": st.column_config.SelectboxColumn(
                    "Call Status",
                    options=["Not Called", "Confirmed", "Voicemail Left", "No Answer", "Busy Line", "Rescheduled"],
                    width="medium"
                ),
                "Follow Up Required": st.column_config.SelectboxColumn(
                    "Follow Up Required",
                    options=["Yes", "No"],
                    width="small"
                ),
                "Total Cost": st.column_config.NumberColumn(
                    "Total Cost",
                    format="$%.2f",
                    width="small"
                )
            }
        )
        
        # Save changes button
        if st.button("💾 Save All Changes", type="primary"):
            # Update the main dataframe with edited data
            for idx, row in edited_df.iterrows():
                original_idx = filtered_leads.index[idx]
                for col in edited_df.columns:
                    st.session_state.leads.loc[original_idx, col] = row[col]
            
            # Save to CSV
            st.session_state.leads.to_csv("demo_leads.csv", index=False)
            st.success("✅ All changes saved successfully!")
            st.rerun()
    else:
        st.info("No leads match the current filters.")

with tab2:
    st.subheader("Call Center")
    
    if not vapi_key or not agent_id:
        st.warning("⚠️ Please configure VAPI credentials in the sidebar to make calls.")
    else:
        st.success("✅ Ready to make calls!")
    
    # Quick call section
    st.markdown("### Quick Call Actions")
    
    # Filter leads that need follow-up
    follow_up_leads = st.session_state.leads[st.session_state.leads['Follow Up Required'] == 'Yes']
    
    if not follow_up_leads.empty:
        st.markdown("#### Leads Requiring Follow-up")
        
        for idx, row in follow_up_leads.iterrows():
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
                
                col1.write(f"**{row['Full Name']}**")
                col2.write(f"📞 {row['Phone']}")
                col3.write(f"📧 {row['Email']}")
                col4.write(f"Status: {row['Status']}")
                col5.write(f"Last Call: {row['Call Status']}")
                
                if col6.button("📞 Call", key=f"call_{idx}", type="primary"):
                    if not (vapi_key and agent_id):
                        st.error("Please enter VAPI credentials in the sidebar.")
                    else:
                        with st.spinner(f"Calling {row['Full Name']}..."):
                            try:
                                # VAPI API call
                                response = requests.post(
                                    "https://api.vapi.ai/call",
                                    headers={
                                        "Authorization": f"Bearer {vapi_key}",
                                        "Content-Type": "application/json"
                                    },
                                    json={
                                        "phoneNumber": row["Phone"],
                                        "agent": {"id": agent_id},
                                        "metadata": {
                                            "lead_name": row["Full Name"],
                                            "email": row["Email"],
                                            "order_id": row["Order ID"],
                                            "pickup_time": row["Pickup Time"],
                                            "special_instructions": row["Special Instructions"]
                                        }
                                    },
                                    timeout=call_timeout
                                )
                                
                                if response.status_code == 200:
                                    call_data = response.json()
                                    st.success(f"✅ Call initiated to {row['Full Name']}!")
                                    
                                    # Log the call
                                    call_log = {
                                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "lead_name": row['Full Name'],
                                        "phone": row['Phone'],
                                        "call_id": call_data.get('id', 'N/A'),
                                        "status": "Initiated"
                                    }
                                    st.session_state.call_history.append(call_log)
                                    
                                    # Update call status
                                    st.session_state.leads.loc[idx, 'Call Status'] = 'Call Initiated'
                                    
                                else:
                                    st.error(f"❌ Call failed: {response.status_code} - {response.text}")
                                    
                            except requests.exceptions.Timeout:
                                st.error("❌ Call request timed out. Please try again.")
                            except Exception as e:
                                st.error(f"❌ API Error: {str(e)}")
                
                st.markdown("---")
    else:
        st.info("No leads currently require follow-up calls.")
    
    # Call history
    if st.session_state.call_history:
        st.markdown("### Recent Call History")
        call_df = pd.DataFrame(st.session_state.call_history)
        st.dataframe(call_df, use_container_width=True)

with tab3:
    st.subheader("Add New Lead")
    
    with st.form("add_lead_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name*", placeholder="John")
            last_name = st.text_input("Last Name*", placeholder="Doe")
            phone = st.text_input("Phone*", placeholder="555-123-4567")
            email = st.text_input("Email*", placeholder="john.doe@email.com")
            address = st.text_input("Address", placeholder="123 Main St")
        
        with col2:
            pickup_date = st.date_input("Pickup Date", value=datetime.now().date() + timedelta(days=1))
            pickup_time_str = st.time_input("Pickup Time", value=datetime.now().time().replace(hour=10, minute=0))
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
            wash = st.selectbox("Wash Service", ["Yes", "No"])
            dry = st.selectbox("Dry Service", ["Yes", "No"])
            pounds = st.number_input("Pounds", min_value=0, value=10)
        
        special_instructions = st.text_area("Special Instructions", placeholder="Any special handling requirements...")
        
        col3, col4 = st.columns(2)
        with col3:
            total_cost = st.number_input("Total Cost ($)", min_value=0.0, value=15.0, step=0.50)
        with col4:
            time_window = st.text_input("Time Window", placeholder="10:00 AM - 12:00 PM")
        
        submitted = st.form_submit_button("➕ Add Lead", type="primary")
        
        if submitted:
            if first_name and last_name and phone and email:
                # Generate order ID
                order_id = f"ORD{len(st.session_state.leads) + 1:03d}"
                full_name = f"{first_name} {last_name}"
                
                # Combine date and time
                pickup_datetime = datetime.combine(pickup_date, pickup_time_str)
                
                new_lead = {
                    "Full Name": full_name,
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Phone": phone,
                    "Email": email,
                    "Order ID": order_id,
                    "Pickup Time": pickup_datetime.strftime("%Y-%m-%d %I:%M %p"),
                    "Status": status,
                    "Wash": wash,
                    "Dry": dry,
                    "Pounds": pounds,
                    "Special Instructions": special_instructions,
                    "Total Cost": f"${total_cost:.2f}",
                    "Address": address,
                    "Time Window": time_window,
                    "Call Status": "Not Called",
                    "Follow Up Required": "Yes"
                }
                
                # Add to dataframe
                new_row_df = pd.DataFrame([new_lead])
                st.session_state.leads = pd.concat([st.session_state.leads, new_row_df], ignore_index=True)
                
                # Save to CSV
                st.session_state.leads.to_csv("demo_leads.csv", index=False)
                
                st.success(f"✅ Lead {full_name} added successfully! Order ID: {order_id}")
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields (marked with *)")

with tab4:
    st.subheader("Analytics Dashboard")
    
    if not st.session_state.leads.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        # Key metrics
        total_revenue = st.session_state.leads['Total Cost'].str.replace('$', '').astype(float).sum()
        avg_order_value = total_revenue / len(st.session_state.leads)
        total_pounds = st.session_state.leads['Pounds'].sum()
        
        with col1:
            st.metric("Total Revenue", f"${total_revenue:.2f}")
        with col2:
            st.metric("Average Order Value", f"${avg_order_value:.2f}")
        with col3:
            st.metric("Total Pounds", f"{total_pounds} lbs")
        with col4:
            completion_rate = (completed_leads / total_leads * 100) if total_leads > 0 else 0
            st.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Status Distribution")
            status_counts = st.session_state.leads['Status'].value_counts()
            st.bar_chart(status_counts)
        
        with col2:
            st.markdown("#### Call Status Distribution")
            call_status_counts = st.session_state.leads['Call Status'].value_counts()
            st.bar_chart(call_status_counts)
        
        # Service breakdown
        st.markdown("#### Service Breakdown")
        col1, col2 = st.columns(2)
        
        with col1:
            wash_counts = st.session_state.leads['Wash'].value_counts()
            st.write("**Wash Service:**")
            st.bar_chart(wash_counts)
        
        with col2:
            dry_counts = st.session_state.leads['Dry'].value_counts()
            st.write("**Dry Service:**")
            st.bar_chart(dry_counts)
    else:
        st.info("No data available for analytics. Add some leads first!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🧺 Outbound Laundromat CRM | Powered by VAPI | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
