import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="DNS Query Simulator",
    page_icon="🌐",
    layout="centered"
)

# Title
st.markdown("<h1 style='text-align: center;'>🌐 DNS Query Simulator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Network Analysis & Simulation Project</p>", unsafe_allow_html=True)

st.divider()

# Fake DNS Database
DNS_DATABASE = {
    "google.com": "142.250.190.14",
    "facebook.com": "157.240.241.35",
    "youtube.com": "142.251.32.46",
    "github.com": "140.82.121.4",
    "openai.com": "104.18.12.123"
}

# Cache
CACHE = {}

# Input
domain = st.text_input("🔍 Enter Domain Name", placeholder="e.g. google.com")

simulate = st.button("🚀 Simulate DNS Query")

if simulate and domain:
    st.subheader("🧩 DNS Resolution Process")

    steps = []
    latency = []

    with st.spinner("Checking Local Cache..."):
        time.sleep(1)
        if domain in CACHE:
            st.success("✔ Found in Local Cache")
            ip = CACHE[domain]
            steps.append("Local Cache")
            latency.append(random.randint(1, 5))
        else:
            st.warning("❌ Not in Cache")
            steps.append("Local Cache")
            latency.append(random.randint(5, 15))

            with st.spinner("Querying Recursive Resolver..."):
                time.sleep(1)
                steps.append("Recursive Resolver")
                latency.append(random.randint(10, 30))

            with st.spinner("Contacting Root DNS Server..."):
                time.sleep(1)
                steps.append("Root Server")
                latency.append(random.randint(20, 50))

            with st.spinner("Contacting TLD Server (.com)..."):
                time.sleep(1)
                steps.append("TLD Server")
                latency.append(random.randint(20, 50))

            with st.spinner("Contacting Authoritative Server..."):
                time.sleep(1)
                steps.append("Authoritative Server")
                latency.append(random.randint(30, 80))

            ip = DNS_DATABASE.get(domain, "Unknown")
            CACHE[domain] = ip

    st.divider()

    # Result
    st.subheader("✅ DNS Resolution Result")
    st.metric(label="Resolved IP Address", value=ip)

    # Table
    df = pd.DataFrame({
        "DNS Step": steps,
        "Latency (ms)": latency
    })

    st.subheader("📊 Query Analysis")
    st.dataframe(df, use_container_width=True)

    # Chart
    fig = px.bar(
        df,
        x="DNS Step",
        y="Latency (ms)",
        title="DNS Query Latency per Step",
        text="Latency (ms)"
    )
    st.plotly_chart(fig, use_container_width=True)

elif simulate:
    st.error("⚠ Please enter a domain name")
