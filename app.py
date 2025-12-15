import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime
import plotly.express as px
import hashlib

# Page setup
st.set_page_config(
    page_title="DNS Query Simulator",
    page_icon="🌐",
    layout="centered"
)

st.markdown("<h1 style='text-align:center;'>🌐 DNS Query Simulator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Network Analysis & Simulation</p>", unsafe_allow_html=True)

st.divider()

# Fake DNS records
DNS_DATABASE = {
    "google.com": "142.250.190.14",
    "facebook.com": "157.240.241.35",
    "youtube.com": "142.251.32.46",
    "github.com": "140.82.121.4",
    "openai.com": "104.18.12.123"
}

CACHE = {}

# User Inputs
domain = st.text_input("🔍 Enter Domain Name", placeholder="e.g. google.com")
mode = st.radio("🔐 Query Mode", ["Normal DNS", "DNS over HTTPS (Encrypted)"])
simulate = st.button("🚀 Start Simulation")

# Containers
packet_box = st.empty()
progress_bar = st.empty()
log_container = st.empty()

logs = []
steps = []
latency = []

def add_log(src, dst, protocol, info):
    logs.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Source": src,
        "Destination": dst,
        "Protocol": protocol,
        "Info": info
    })

def animate_packet(text, delay=1):
    packet_box.info(text)
    time.sleep(delay)

if simulate and domain:
    st.subheader("📦 Packet Flow Animation")

    progress = progress_bar.progress(0)

    # Encrypt domain if DoH
    if mode == "DNS over HTTPS (Encrypted)":
        encrypted_domain = hashlib.sha256(domain.encode()).hexdigest()
        query_data = encrypted_domain
        protocol = "HTTPS (DoH)"
    else:
        query_data = domain
        protocol = "DNS"

    # Step 1: Client → Cache
    animate_packet("🖥️ Client → Local DNS Cache")
    add_log("Client", "Local Cache", protocol, f"Query: {query_data}")
    progress.progress(15)
    latency.append(random.randint(5, 15))
    steps.append("Local Cache")

    if domain in CACHE:
        ip = CACHE[domain]
        add_log("Local Cache", "Client", protocol, f"Response: {ip}")
    else:
        # Step 2: Recursive Resolver
        animate_packet("📡 Cache → Recursive Resolver")
        add_log("Cache", "Recursive Resolver", protocol, "Forward Query")
        progress.progress(35)
        latency.append(random.randint(15, 30))
        steps.append("Recursive Resolver")

        # Step 3: Root Server
        animate_packet("🌍 Resolver → Root Server")
        add_log("Resolver", "Root Server", protocol, "Request TLD Info")
        progress.progress(55)
        latency.append(random.randint(25, 45))
        steps.append("Root Server")

        # Step 4: TLD Server
        animate_packet("📂 Root → TLD Server (.com)")
        add_log("Root", "TLD Server", protocol, "Request Authoritative Server")
        progress.progress(75)
        latency.append(random.randint(25, 45))
        steps.append("TLD Server")

        # Step 5: Authoritative Server
        animate_packet("🏢 TLD → Authoritative Server")
        ip = DNS_DATABASE.get(domain, "Unknown")
        add_log("Authoritative Server", "Resolver", protocol, f"IP Address: {ip}")
        progress.progress(90)
        latency.append(random.randint(35, 70))
        steps.append("Authoritative Server")

        CACHE[domain] = ip

    # Final Response
    animate_packet("✅ Resolver → Client (Response Received)")
    add_log("Resolver", "Client", protocol, f"Resolved IP: {ip}")
    progress.progress(100)

    st.divider()

    # Result
    st.subheader("✅ DNS Resolution Result")
    st.metric("Resolved IP Address", ip)

    if mode == "DNS over HTTPS (Encrypted)":
        st.success("🔐 Query was encrypted using DNS over HTTPS (DoH)")
        st.code(f"Encrypted Payload (SHA-256):\n{encrypted_domain}")

    # Wireshark Logs
    st.subheader("🧪 Wireshark-Style Packet Logs")
    log_df = pd.DataFrame(logs)
    st.dataframe(log_df, use_container_width=True)

    # Latency Analysis
    st.subheader("📊 Latency Analysis")
    df = pd.DataFrame({
        "DNS Step": steps,
        "Latency (ms)": latency
    })

    fig = px.line(
        df,
        x="DNS Step",
        y="Latency (ms)",
        markers=True,
        title="DNS Packet Latency Flow"
    )
    st.plotly_chart(fig, use_container_width=True)

elif simulate:
    st.error("⚠ Please enter a domain name")
