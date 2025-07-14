import streamlit as st
import whois
import socket
import requests
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="OSINT Tool", page_icon="🔍", layout="wide")

# Fungsi-fungsi OSINT
def whois_lookup(domain):
    try:
        return whois.whois(domain)
    except Exception as e:
        return {"Error": str(e)}

def dns_lookup(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {"Domain": domain, "IP Address": ip}
    except Exception as e:
        return {"Error": str(e)}

def ip_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response["status"] == "success":
            return response
        return {"Error": "Invalid IP or service unavailable"}
    except Exception as e:
        return {"Error": str(e)}

def format_output(data):
    if isinstance(data, dict):
        formatted = ""
        for key, value in data.items():
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            formatted += f"**{key}**: {value}\n\n"
        return formatted
    return str(data)

# UI Streamlit
st.title("🔍 Compact OSINT Tool")
st.markdown("Tool sederhana untuk investigasi OSINT dasar")

tab1, tab2, tab3 = st.tabs(["WHOIS Lookup", "DNS Lookup", "IP Geolocation"])

with tab1:
    st.subheader("WHOIS Lookup")
    domain_whois = st.text_input("Masukkan domain untuk WHOIS lookup:", "example.com")
    if st.button("Cari WHOIS"):
        with st.spinner("Mencari informasi WHOIS..."):
            result = whois_lookup(domain_whois)
            st.markdown(format_output(result))

with tab2:
    st.subheader("DNS Lookup")
    domain_dns = st.text_input("Masukkan domain untuk DNS lookup:", "example.com")
    if st.button("Cari DNS"):
        with st.spinner("Mencari informasi DNS..."):
            result = dns_lookup(domain_dns)
            st.markdown(format_output(result))

with tab3:
    st.subheader("IP Geolocation")
    ip_geo = st.text_input("Masukkan alamat IP untuk geolokasi:", "8.8.8.8")
    if st.button("Cari Geolokasi"):
        with st.spinner("Mencari informasi geolokasi..."):
            result = ip_geolocation(ip_geo)
            st.markdown(format_output(result))

# Footer
st.markdown("---")
st.markdown(f"© {datetime.now().year} Compact OSINT Tool | Untuk tujuan edukasi dan penelitian sah")
