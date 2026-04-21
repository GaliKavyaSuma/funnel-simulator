
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Advanced Funnel Simulator", layout="wide")

st.title("🚀 Advanced Conversion Funnel Simulator")

# Load base
df = pd.read_csv("base_funnel.csv")
base = df["Base"].tolist()

st.sidebar.header("🎛 Scenario Builder")

signup = st.sidebar.slider("Signup Rate (%)", 10, 100, 60)
cart = st.sidebar.slider("Cart Rate (%)", 10, 100, 70)
purchase = st.sidebar.slider("Purchase Rate (%)", 10, 100, 60)

visited = base[0]
signed = int(visited * signup / 100)
cart_val = int(signed * cart / 100)
purchased = int(cart_val * purchase / 100)

scenario = [visited, signed, cart_val, purchased]

# Comparison
st.subheader("📊 Base vs Scenario Comparison")

fig = go.Figure()

fig.add_trace(go.Funnel(
    name="Base",
    y=df["Stage"],
    x=base,
    opacity=0.6
))

fig.add_trace(go.Funnel(
    name="Scenario",
    y=df["Stage"],
    x=scenario,
    opacity=0.6
))

st.plotly_chart(fig, use_container_width=True)

# KPIs
st.subheader("💰 Revenue Impact")

avg_order = st.slider("Average Order Value", 10, 500, 100)

base_revenue = base[-1] * avg_order
new_revenue = purchased * avg_order

col1, col2, col3 = st.columns(3)

col1.metric("Base Revenue", f"${base_revenue:,}")
col2.metric("Scenario Revenue", f"${new_revenue:,}")
col3.metric("Lift", f"{((new_revenue-base_revenue)/base_revenue)*100:.2f}%")

# Scenario Insights
st.subheader("🧠 Smart Insights")

if new_revenue > base_revenue:
    st.success("Scenario improves revenue significantly.")
else:
    st.warning("Scenario does not improve revenue.")

# Export
st.subheader("📥 Export Scenario")

export_df = pd.DataFrame({
    "Stage": df["Stage"],
    "Base": base,
    "Scenario": scenario
})

st.download_button("Download CSV", export_df.to_csv(index=False), "scenario.csv")

