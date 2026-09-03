```python
"""
BillLens Streamlit Dashboard
"""

import os

import httpx
import streamlit as st


st.set_page_config(
    page_title="BillLens",
    page_icon="🏛️",
    layout="wide",
)


def get_api_url() -> str:
    """Get the API URL from environment variables or Streamlit secrets."""
    api_url = os.getenv("API_URL") or os.getenv("DASHBOARD_API_URL")

    if not api_url:
        try:
            api_url = st.secrets.get("API_URL") or st.secrets.get(
                "DASHBOARD_API_URL"
            )
        except Exception:
            api_url = None

    return (api_url or "").rstrip("/")


API_URL = get_api_url()

st.title("🏛️ BillLens")
st.markdown("**AI-powered parliamentary intelligence for everyone**")

if not API_URL:
    st.error(
        "The API is not configured. Add API_URL to the Streamlit Cloud "
        "secrets or environment variables."
    )
    st.code('API_URL = "https://your-public-api-url.example.com"')
    st.stop()


if "answer" not in st.session_state:
    st.session_state.answer = None


with st.sidebar:
    st.header("About")
    st.markdown(
        """
        BillLens helps you understand what Parliament has done,
        debated, or voted on, with verified evidence and confidence scores.
        """
    )

    st.markdown("---")

    if st.button("Clear History"):
        st.session_state.answer = None
        st.rerun()


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


if submit_button:
    if not question.strip():
        st.error("Please enter a question.")
    elif len(question.strip()) < 3:
        st.error("Question must be at least 3 characters long.")
    else:
        try:
            with st.spinner("Searching parliamentary records..."):
                response = httpx.post(
                    f"{API_URL}/api/v1/questions",
                    json={"question": question.strip()},
                    timeout=60.0,
                    follow_redirects=True,
                )

            if response.is_success:
                st.session_state.answer = response.json()
            else:
                st.error(
                    f"The API returned HTTP {response.status_code}."
                )

        except httpx.TimeoutException:
            st.error("The request timed out. Please try again.")
        except httpx.RequestError:
            st.error(
                "Could not connect to the API server. "
                "Please try again later."
            )
        except ValueError:
            st.error("The API returned an invalid response.")


if st.session_state.answer:
    answer = st.session_state.answer

    st.markdown("---")
    st.subheader("Summary")
    st.markdown(answer.get("summary", "No summary available."))

    col1, col2 = st.columns(2)

    with col1:
        confidence = answer.get("confidence", 0.0) or 0.0
        confidence_pct = int(float(confidence) * 100)
        st.metric("Confidence Level", f"{confidence_pct}%")

    warnings = answer.get("warnings", []) or []

    with col2:
        if warnings:
            st.warning(f"⚠️ {len(warnings)} warning(s)")
        else:
            st.success("No warnings")

    tabs = st.tabs(
        [
            "What Happened",
            "Legislation",
            "Parliamentary Activity",
            "Votes",
            "What Didn't Happen",
            "Claims & Sources",
        ]
    )

    sections = [
        ("what_happened", "No parliamentary activity found."),
        ("legislation", "No relevant legislation found."),
        ("parliamentary_activity", "No debates or discussions found."),
        ("votes", "No votes found."),
        ("what_did_not_happen", "No unverified claims."),
    ]

    for tab, (key, empty_message) in zip(tabs[:5], sections):
        with tab:
            items = answer.get(key, []) or []

            if items:
                for item in items:
                    st.markdown(f"• {item}")
            else:
                st.info(empty_message)

    with tabs[5]:
        claims = answer.get("claims", []) or []

        if claims:
            st.subheader("Verified Claims")

            for index, claim in enumerate(claims, 1):
                claim_text = claim.get("text", "")
                label = claim_text[:60]
                if len(claim_text) > 60:
                    label += "..."

                with st.expander(f"Claim {index}: {label}"):
                    supported = claim.get("supported", False)
                    claim_confidence = claim.get("confidence", 0.0) or 0.0

                    col1, col2 = st.columns(2)

                    with col1:
                        status = (
                            "✅ Supported"
                            if supported
                            else "❌ Unsupported"
                        )
                        st.markdown(f"**Status:** {status}")

                    with col2:
                        confidence_pct = int(
                            float(claim_confidence) * 100
                        )
                        st.markdown(
                            f"**Confidence:** {confidence_pct}%"
                        )

                    st.markdown(claim_text)

                    sources = claim.get("sources", []) or []
                    if sources:
                        st.markdown("**Sources:**")

                        for source in sources:
                            url = source.get("url")
                            title = source.get("title", "Source")
                            source_type = source.get(
                                "source_type",
                                "unknown",
                            )

                            label = f"{title} *({source_type})*"

                            if url:
                                st.markdown(f"[{label}]({url})")
                            else:
                                st.markdown(label)
        else:
            st.info("No verified claims.")

    st.markdown("---")
    st.subheader("All Sources")

    sources = answer.get("sources", []) or []

    if sources:
        for source in sources:
            url = source.get("url")
            title = source.get("title", "Source")
            source_type = source.get("source_type", "unknown")
            date = source.get("date")

            if url:
                st.markdown(f"[{title}]({url})")
            else:
                st.markdown(title)

            st.caption(source_type)

            if date:
                st.caption(f"📅 {date}")
    else:
        st.info("No sources retrieved.")

    if warnings:
        st.markdown("---")
        st.subheader("Warnings")

        for warning in warnings:
            st.warning(warning)
```