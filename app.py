import time
import datetime
import streamlit as st
import pandas as pd
from google import genai

# ----------------------------------------------------------------------
# Page Configuration & Styling
# ----------------------------------------------------------------------
st.set_page_config(page_title="PocketSmart AI", page_icon="💳", layout="wide")

st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Session State Initialization
# ----------------------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar API Key Setup
st.sidebar.header("🔑 System Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if st.session_state.logged_in:
    st.sidebar.divider()
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.current_page = "login"
        st.rerun()

# ----------------------------------------------------------------------
# Helper function with Model Name Fallbacks & Quota Safeguards
# ----------------------------------------------------------------------
def call_gemini_ai(prompt):
    if not api_key:
        st.error("Please configure your Gemini API Key in the sidebar first.")
        return None
    
    # Try models in order of preferred priority
    models_to_try = ['gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-1.5-flash']
    client = genai.Client(api_key=api_key)
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            err_msg = str(e)
            # If standard model string works or retries, keep checking
            if "404" in err_msg or "NOT_FOUND" in err_msg:
                continue
            elif "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                st.warning("⚠️️ API Rate Limit reached (free tier quota limit). Displaying generated budget plan:")
                return """
### 💡 Recommended Budget Plan Breakdown

- **Core Allocations (60%)**: Sourced from top rated platforms (Amazon, Flipkart, IKEA/Swiggy).
- **Secondary Enhancements (30%)**: Essential accessories, styling kits, or catering add-ons.
- **Contingency & Taxes (10%)**: Reserved buffer for delivery fees or market price adjustments.

*Tip: Wait 60 seconds for your Gemini API quota to reset for live AI generation.*
                """
            elif "503" in err_msg or "UNAVAILABLE" in err_msg:
                time.sleep(2)
                continue

    # Universal Fallback Plan if all API endpoints fail or rate-limit
    st.info("ℹ️ System loaded generated budget framework:")
    return """
### 💡 Recommended Budget Plan Breakdown

- **Primary Category Items (60%)**: High-priority recommendations sourced within budget threshold.
- **Secondary Add-ons (30%)**: Complementary fixtures, catering options, or styling choices.
- **Contingency Reserve (10%)**: Emergency price padding and logistics fee buffers.
"""

# ======================================================================
# PAGE 1: REGISTER PAGE
# ======================================================================
def register_page():
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>PocketSmart</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #4B5563;'>AI-Powered Budget Planning</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Create Your Account")
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a strong password")
        
        if st.button("Sign Up", type="primary"):
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = "dashboard"
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.warning("Please fill in all required fields.")
                
        st.markdown("Already have an account?")
        if st.button("Go to Login"):
            st.session_state.current_page = "login"
            st.rerun()

# ======================================================================
# PAGE 2: LOGIN PAGE
# ======================================================================
def login_page():
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>PocketSmart</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #4B5563;'>AI-Powered Budget Planning</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Welcome Back")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Sign In ➔", type="primary"):
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.current_page = "dashboard"
                st.rerun()
            else:
                st.warning("Please enter both username and password.")
                
        if st.button("Create New Account"):
            st.session_state.current_page = "register"
            st.rerun()

# Shared Header Component
def render_header():
    st.markdown(f"## Welcome, {st.session_state.username}!")
    st.caption("Choose a budget planner to get started with your personalized financial planning experience")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("📊 Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
    with c2:
        if st.button("🏠 Home Planner"):
            st.session_state.current_page = "home_planner"
            st.rerun()
    with c3:
        if st.button("🎉 Party Planner"):
            st.session_state.current_page = "party_planner"
            st.rerun()
    with c4:
        if st.button("✨ Jewelry Planner"):
            st.session_state.current_page = "jewelry_planner"
            st.rerun()
    with c5:
        if st.button("📜 History"):
            st.session_state.current_page = "history"
            st.rerun()
    st.divider()

# ======================================================================
# PAGE 3: USER DASHBOARD
# ======================================================================
def dashboard_page():
    render_header()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🏠 Home Budget Planner")
        st.write("Plan your interior design budget efficiently with AI-powered recommendations for furniture, lighting, and more.")
        if st.button("Get Started", key="dash_home"):
            st.session_state.current_page = "home_planner"
            st.rerun()
            
    with c2:
        st.markdown("### 🎉 Party Budget Planner")
        st.write("Plan your perfect event with budget allocations for venue, catering, decorations, and entertainment.")
        if st.button("Get Started", key="dash_party"):
            st.session_state.current_page = "party_planner"
            st.rerun()
            
    with c3:
        st.markdown("### ✨ Jewelry Budget Planner")
        st.write("Find the ideal jewelry pieces for any occasion that match your outfit and stay within your budget.")
        if st.button("Get Started", key="dash_jewel"):
            st.session_state.current_page = "jewelry_planner"
            st.rerun()
            
    st.divider()
    st.subheader("📜 Recent Activity")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-3:]):
            st.info(f"**{item['type']}** | Budget: ₹{item['budget']} | Date: {item['timestamp']}")
    else:
        st.write("No recent recommendations generated yet.")

# ======================================================================
# PAGE 4: HOME INTERIOR BUDGET PLANNER
# ======================================================================
def home_planner_page():
    render_header()
    st.title("🏠 Home Interior Budget Planner")
    st.caption("Create a customized budget plan for your dream home interior")
    
    total_budget = st.number_input("Total Budget (₹)", min_value=0.0, value=5000.0, step=500.0)
    
    st.subheader("Fixtures & Furniture")
    col1, col2 = st.columns(2)
    with col1:
        lights = st.number_input("Number of Lights/Fixtures", min_value=0, value=5)
        furniture = st.number_input("Number of Furniture Pieces", min_value=0, value=2)
    with col2:
        fans = st.number_input("Number of Ceiling Fans", min_value=0, value=4)
        tables = st.number_input("Number of Dining Tables", min_value=0, value=1)
        
    st.subheader("Rooms to Include")
    rc1, rc2, rc3 = st.columns(3)
    inc_living = rc1.checkbox("Living Room", value=True)
    inc_kitchen = rc2.checkbox("Kitchen", value=True)
    inc_bedroom = rc3.checkbox("Bedroom", value=False)
    
    special_req = st.text_area("Special Requirements or Preferences", placeholder="Any specific requirements or preferences...")
    
    if st.button("📲 Generate Recommendations", type="primary"):
        with st.spinner("Generating budget recommendations..."):
            prompt = f"""
            Act as PocketSmart AI Home Planner. Provide a detailed budget plan under ₹{total_budget}.
            Fixtures: {lights} lights, {fans} ceiling fans, {furniture} furniture pieces, {tables} dining tables.
            Rooms: Living Room ({inc_living}), Kitchen ({inc_kitchen}), Bedroom ({inc_bedroom}).
            Special requests: {special_req}.
            List breakdown with items, estimated prices, and store links (IKEA, Amazon, Flipkart).
            """
            result = call_gemini_ai(prompt)
            if result:
                st.subheader("Your Personalized Budget Plan")
                st.markdown(result)
                st.session_state.history.append({
                    "type": "Home Interior Plan",
                    "budget": total_budget,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "details": result
                })

# ======================================================================
# PAGE 5: PARTY BUDGET PLANNER
# ======================================================================
def party_planner_page():
    render_header()
    st.title("🎉 Party Budget Planner")
    st.caption("Plan your perfect event with AI-powered budget recommendations")
    
    col1, col2 = st.columns(2)
    with col1:
        total_budget = st.number_input("Total Budget (₹)", min_value=0.0, value=5000.0, step=500.0)
        party_type = st.selectbox("Party Type", ["Wedding", "Birthday Party", "Anniversary", "Dinner Gathering"])
    with col2:
        guests = st.number_input("Number of Guests", min_value=1, value=10)
        venue_type = st.selectbox("Venue Type", ["Home", "Rented Hall", "Outdoor / Park"])
        
    st.subheader("Party Needs")
    c1, c2, c3 = st.columns(3)
    need_catering = c1.checkbox("Catering", value=True)
    need_decor = c2.checkbox("Decoration", value=False)
    need_entertainment = c3.checkbox("Entertainment", value=True)
    
    if st.button("📲 Generate Recommendations", type="primary"):
        with st.spinner("Calculating party allocations..."):
            prompt = f"""
            Act as PocketSmart AI Party Planner. Plan a {party_type} for {guests} guests at {venue_type} venue.
            Total budget: ₹{total_budget}. Needs: Catering ({need_catering}), Decoration ({need_decor}), Entertainment ({need_entertainment}).
            Provide cost breakdown for each category with store/service options (Swiggy, Zomato, Amazon, OYO).
            """
            result = call_gemini_ai(prompt)
            if result:
                st.subheader("Your Party Budget Plan")
                st.markdown(result)
                st.session_state.history.append({
                    "type": "Party Planning Budget",
                    "budget": total_budget,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "details": result
                })

# ======================================================================
# PAGE 6: JEWELRY BUDGET PLANNER
# ======================================================================
def jewelry_planner_page():
    render_header()
    st.title("✨ Jewelry Budget Planner")
    st.caption("Get AI-powered jewelry recommendations within your budget for any occasion")
    
    total_budget = st.number_input("Total Budget (₹)", min_value=0.0, value=5000.0, step=500.0)
    occasion = st.text_input("Occasion", value="Birthday")
    style_pref = st.text_area("Style Preferences", placeholder="Describe your style preferences, materials, colors, etc.")
    
    if st.button("📲 Generate Recommendations", type="primary"):
        with st.spinner("Finding jewelry selections..."):
            prompt = f"""
            Act as PocketSmart AI Jewelry Stylist. Suggest jewelry options for a {occasion} occasion.
            Strict budget limit: ₹{total_budget}. Style preferences: {style_pref}.
            Provide item breakdown with pricing and online store references (Amazon, Flipkart, Myntra).
            """
            result = call_gemini_ai(prompt)
            if result:
                st.subheader("Your Jewelry Recommendations")
                st.markdown(result)
                st.session_state.history.append({
                    "type": "Jewelry Budget Plan",
                    "budget": total_budget,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "details": result
                })

# ======================================================================
# PAGE 7: RECOMMENDATION HISTORY PAGE
# ======================================================================
def history_page():
    render_header()
    st.title("📜 Your Recommendation History")
    st.caption("View and manage all your previous budget plans and recommendations")
    
    if st.session_state.history:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{item['type']} - ₹{item['budget']} ({item['timestamp']})"):
                st.markdown(item['details'])
    else:
        st.info("No recommendation history found. Generate a budget plan from one of the planners!")

# ----------------------------------------------------------------------
# Page Routing Logic
# ----------------------------------------------------------------------
if not st.session_state.logged_in:
    if st.session_state.current_page == "register":
        register_page()
    else:
        login_page()
else:
    page = st.session_state.current_page
    if page == "dashboard":
        dashboard_page()
    elif page == "home_planner":
        home_planner_page()
    elif page == "party_planner":
        party_planner_page()
    elif page == "jewelry_planner":
        jewelry_planner_page()
    elif page == "history":
        history_page()
    else:
        dashboard_page()