"""BillLens Streamlit dashboard."""

import os
from typing import Any

import httpx
import streamlit as st


st.set_page_config(
    page_title="BillLens",
    page_icon="🏛️",
    layout="wide",
)


def get_api_url() -> str:
    """Read the public API URL from environment variables or Streamlit secrets."""
    api_url = os.getenv("API_URL") or os.getenv("DASHBOARD_API_URL")

    if not api_url:
        try:
            api_url = st.secrets.get("API_URL") or st.secrets.get(
                "DASHBOARD_API_URL"
            )
        except Exception:
            api_url = None

    return (api_url or "").strip().rstrip("/")


def display_items(items: list[Any], empty_message: str) -> None:
    """Display API result items."""
    if not items:
        st.info(empty_message)
        return

    for item in items:
        if isinstance(item, dict):
            title = item.get("title") or item.get("name") or item.get(
                "text"
            )
            description = item.get("description") or item.get("summary")

            if title:
                st.markdown(f"**{title}**")
            if description:
                st.write(description)

            url = item.get("url") or item.get("source_url")
            if url:
                st.markdown(f"[View source]({url})")
        else:
            st.markdown(f"• {item}")


API_URL = get_api_url()

st.title("🏛️ BillLens")
st.caption("AI-powered parliamentary intelligence for everyone.")

if not API_URL:
    st.error("The API is not configured.")
    st.code('API_URL = "https://your-public-api-url.example.com"')
    st.info(
        "Add API_URL in Streamlit Cloud → Settings → Secrets, "
        "then reboot the app."
    )
    st.stop()


with st.sidebar:
    st.header("About")
    st.write(
        "BillLens helps you understand UK parliamentary activity "
        "using evidence and source citations."
    )

    if st.button("Clear answer"):
        st.session_state.pop("answer", None)
        st.rerun()


question = st.text_input(
    "Ask a question about UK Parliament",
    placeholder="What laws have changed about housing?",
    max_chars=2000,
)

if st.button("Search", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Searching parliamentary records..."):
                response = httpx.post(
                    f"{API_URL}/api/v1/questions",
                    json={"question": question.strip()},
                    timeout=90.0,
                    follow_redirects=True,
                )

            if response.is_success:
                st.session_state.answer = response.json()
            else:
                st.error(
                    f"API error: HTTP {response.status_code} "
                    f"from `{API_URL}`"
                )
                st.code(response.text[:2000])

        except httpx.TimeoutException:
            st.error("The API request timed out. Please try again.")
        except httpx.RequestError as error:
            st.error(f"Could not connect to API: {API_URL}")
            st.caption(str(error))
        except ValueError:
            st.error("The API returned invalid JSON.")


answer = st.session_state.get("answer")

if answer:
    st.divider()
    st.subheader("Summary")
    st.write(answer.get("summary") or "No summary available.")

    confidence = answer.get("confidence")
    if confidence is not None:
        try:
            confidence_percent = round(float(confidence) * 100)
            st.metric("Confidence", f"{confidence_percent}%")
        except (TypeError, ValueError):
            pass

    tabs = st.tabs(
        [
            "What happened",
            "Legislation",
            "Parliamentary activity",
            "Votes",
            "What did not happen",
            "Claims and sources",
        ]
    )

    result_sections = [
        ("what_happened", "No relevant activity found."),
        ("legislation", "No relevant legislation found."),
        ("parliamentary_activity", "No parliamentary activity found."),
        ("votes", "No votes found."),
        ("what_did_not_happen", "No information available."),
    ]

    for tab, (key, empty_message) in zip(tabs[:5], result_sections):
        with tab:
            display_items(answer.get(key, []) or [], empty_message)

    with tabs[5]:
        claims = answer.get("claims", []) or []

        if claims:
            for index, claim in enumerate(claims, start=1):
                if isinstance(claim, dict):
                    text = claim.get("text") or claim.get("claim") or ""
                    supported = claim.get("supported")
                    claim_confidence = claim.get("confidence")
                    sources = claim.get("sources", []) or []

                    with st.expander(f"Claim {index}"):
                        st.write(text)

                        if supported is not None:
                            st.write(
                                "✅ Supported"
                                if supported
                                else "❌ Not supported"
                            )

                        if claim_confidence is not None:
                            st.write(
                                f"Confidence: "
                                f"{float(claim_confidence) * 100:.0f}%"
                            )

                        for source in sources:
                            if isinstance(source, dict):
                                url = source.get("url")
                                title = source.get("title", "Source")
                                if url:
                                    st.markdown(f"[{title}]({url})")
                                else:
                                    st.write(title)
                else:
                    st.write(claim)
        else:
            st.info("No claims found.")

    warnings = answer.get("warnings", []) or []
    if warnings:
        st.divider()
        st.subheader("Warnings")
        for warning in warnings:
            st.warning(warning)

    sources = answer.get("sources", []) or []
    if sources:
        st.divider()
        st.subheader("Sources")
        for source in sources:
            if isinstance(source, dict):
                url = source.get("url")
                title = source.get("title", "Source")
                if url:
                    st.markdown(f"[{title}]({url})")
                else:
                    st.write(title)