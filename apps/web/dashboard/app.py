"""
BillLens Streamlit Dashboard
"""

import os
import sys
import asyncio
import httpx
import streamlit as st

# Page config
st.set_page_config(
    page_title="BillLens",
    page_icon="🏛️",
    layout="wide",
)

st.title("🏛️ BillLens")
st.markdown("**AI-powered parliamentary intelligence for everyone**")

# Get API URL from environment, with fallback options
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Try alternative addresses if localhost fails
FALLBACK_URLS = [
    API_URL,
    "http://127.0.0.1:8000",
    "http://host.docker.internal:8000",  # For Docker on Mac/Windows
]

# Session state
if "answer" not in st.session_state:
    st.session_state.answer = None

if "loading" not in st.session_state:
    st.session_state.loading = False

if "api_url" not in st.session_state:
    st.session_state.api_url = API_URL

if "api_status" not in st.session_state:
    st.session_state.api_status = None

# Function to find working API URL
def find_working_api():
    """Try to find a working API endpoint."""
    for url in [st.session_state.api_url] + FALLBACK_URLS:
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{url}/health")
                if response.status_code == 200:
                    return url
        except Exception:
            continue
    return None

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    BillLens helps you understand what Parliament has done,
    debated, or voted on, with verified evidence and confidence scores.
    """)
    
    st.markdown("---")
    
    # API Status
    st.subheader("API Status")
    if st.button("Check API Connection"):
        working_api = find_working_api()
        if working_api:
            st.session_state.api_status = working_api
            st.success(f"✅ Connected to {working_api}")
        else:
            st.session_state.api_status = None
            st.error("❌ Cannot reach API server. Make sure it's running on port 8000")
    
    if st.session_state.api_status:
        st.info(f"Using API: {st.session_state.api_status}")
    
    # API URL configuration
    st.subheader("Configuration")
    custom_api_url = st.text_input(
        "API URL:",
        value=st.session_state.api_url,
        help="Enter the API endpoint (e.g., http://localhost:8000)"
    )
    if custom_api_url:
        st.session_state.api_url = custom_api_url
    
    if st.button("Clear History"):
        st.session_state.answer = None
        st.rerun()

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_input(
        "Ask about UK Parliament:",
        placeholder="e.g., What laws have changed about housing?",
        max_chars=2000,
    )

with col2:
    submit_button = st.button(
        "Search",
        use_container_width=True,
        type="primary",
    )

# Process question
if submit_button and question:
    if len(question) < 3:
        st.error("Question must be at least 3 characters long.")
    else:
        st.session_state.loading = True
        
        try:
            # Try to find working API URL if not already known
            if not st.session_state.api_status:
                st.session_state.api_status = find_working_api()
            
            api_endpoint = st.session_state.api_status
            
            if not api_endpoint:
                st.error(
                    "❌ **Could not connect to API server.**\n\n"
                    "Please make sure the API is running:\n\n"
                    "```bash\n"
                    "python -m uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000\n"
                    "```\n\n"
                    "Then refresh this page and try again."
                )
            else:
                with st.spinner("🔍 Searching parliamentary records..."):
                    try:
                        with httpx.Client(timeout=120.0) as client:
                            response = client.post(
                                f"{api_endpoint}/api/v1/questions",
                                json={"question": question},
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                st.session_state.answer = result
                                st.success("✅ Answer generated!")
                            elif response.status_code == 405:
                                st.error(
                                    "❌ **Method Not Allowed (405)**\n\n"
                                    "The API endpoint is not responding correctly. "
                                    "Make sure you're using the correct API URL."
                                )
                            else:
                                st.error(
                                    f"❌ **Error {response.status_code}**\n\n"
                                    f"```\n{response.text}\n```"
                                )
                    except httpx.TimeoutException:
                        st.error("⏱️ **Request timed out.** The API is taking too long to respond. Try again.")
                    except Exception as e:
                        st.error(f"❌ **Error:** {str(e)}")
        
        finally:
            st.session_state.loading = False

# Display answer
if st.session_state.answer:
    answer = st.session_state.answer
    
    # Summary
    st.markdown("---")
    st.subheader("Summary")
    summary = answer.get("summary", "No summary available.")
    st.markdown(summary)
    
    # Confidence and warnings
    col1, col2 = st.columns(2)
    
    with col1:
        confidence = answer.get("confidence", 0.0)
        confidence_pct = int(confidence * 100)
        st.metric("Confidence Level", f"{confidence_pct}%")
    
    with col2:
        warnings = answer.get("warnings", [])
        if warnings:
            st.warning(f"⚠️ {len(warnings)} warning(s)")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "What Happened",
        "Legislation",
        "Parliamentary Activity",
        "Votes",
        "What Didn't Happen",
        "Claims & Sources",
    ])
    
    with tab1:
        what_happened = answer.get("what_happened", [])
        if what_happened:
            for item in what_happened:
                st.markdown(f"• {item}")
        else:
            st.info("No parliamentary activity found.")
    
    with tab2:
        legislation = answer.get("legislation", [])
        if legislation:
            for item in legislation:
                st.markdown(f"• {item}")
        else:
            st.info("No relevant legislation found.")
    
    with tab3:
        activity = answer.get("parliamentary_activity", [])
        if activity:
            for item in activity:
                st.markdown(f"• {item}")
        else:
            st.info("No debates or discussions found.")
    
    with tab4:
        votes = answer.get("votes", [])
        if votes:
            for item in votes:
                st.markdown(f"• {item}")
        else:
            st.info("No votes found.")
    
    with tab5:
        did_not_happen = answer.get("what_did_not_happen", [])
        if did_not_happen:
            for item in did_not_happen:
                st.markdown(f"• {item}")
        else:
            st.info("No unverified claims.")
    
    with tab6:
        claims = answer.get("claims", [])
        
        if claims:
            st.subheader("Verified Claims")
            
            for idx, claim in enumerate(claims, 1):
                with st.expander(
                    f"Claim {idx}: {claim.get('text', '')[:60]}..."
                ):
                    supported = claim.get("supported", False)
                    confidence = claim.get("confidence", 0.0)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        status = "✅ Supported" if supported else "❌ Unsupported"
                        st.markdown(f"**Status:** {status}")
                    
                    with col2:
                        conf_pct = int(confidence * 100)
                        st.markdown(f"**Confidence:** {conf_pct}%")
                    
                    st.markdown(claim.get("text", ""))
                    
                    sources = claim.get("sources", [])
                    if sources:
                        st.markdown("**Sources:**")
                        for source in sources:
                            url = source.get("url")
                            title = source.get("title", "Source")
                            source_type = source.get("source_type", "unknown")
                            
                            if url:
                                st.markdown(
                                    f"[{title}]({url}) "
                                    f"*({source_type})*"
                                )
                            else:
                                st.markdown(
                                    f"{title} *({source_type})*"
                                )
        
        else:
            st.info("No verified claims.")
    
    # Sources
    st.markdown("---")
    st.subheader("All Sources")
    
    sources = answer.get("sources", [])
    
    if sources:
        for idx, source in enumerate(sources, 1):
            url = source.get("url")
            title = source.get("title", "Source")
            source_type = source.get("source_type", "unknown")
            date = source.get("date")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if url:
                    st.markdown(f"[{title}]({url})")
                else:
                    st.markdown(f"{title}")
            
            with col2:
                st.caption(f"{source_type}")
            
            if date:
                st.caption(f"📅 {date}")
    
    else:
        st.info("No sources retrieved.")
    
    # Warnings
    if warnings:
        st.markdown("---")
        st.subheader("Warnings")
        for warning in warnings:
            st.warning(warning)
