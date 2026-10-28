## Import necessary libraries, configure Streamlit page settings, and apply custom CSS styling for the web app

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# Page Configuration - Wide Dashboard Layout
st.set_page_config(
    page_title="Burnout Analytics Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to look like a modern Web App
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    .main-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        padding: 20px 25px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 25px;
    }

    .header-title {
        color: #38bdf8;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }

    .header-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 5px;
    }

    .risk-alert-high {
        background-color: rgba(239, 68, 68, 0.15);
        border-left: 5px solid #ef4444;
        padding: 15px 20px;
        border-radius: 8px;
        color: #fca5a5;
    }

    .risk-alert-medium {
        background-color: rgba(245, 158, 11, 0.15);
        border-left: 5px solid #f59e0b;
        padding: 15px 20px;
        border-radius: 8px;
        color: #fde047;
    }

    .risk-alert-low {
        background-color: rgba(16, 185, 129, 0.15);
        border-left: 5px solid #10b981;
        padding: 15px 20px;
        border-radius: 8px;
        color: #6ee7b7;
    }
</style>
""", unsafe_allow_html=True)

# Top Header Bar
st.markdown("""
<div class="main-header">
    <div class="header-title"> Remote Employee Wellbeing & Burnout Analytics</div>
    <div class="header-subtitle">Princess Nourah Bint Abdulrahman University | DS111 Data Science Project</div>
</div>
""", unsafe_allow_html=True)

# Sidebar - Parameters Input
st.sidebar.markdown("### 🎛️ Assessment Control Panel")
st.sidebar.markdown("---")

age = st.sidebar.slider("👤 Employee Age", 18, 65, 30)
hours_per_week = st.sidebar.slider("⏰ Weekly Working Hours", 10, 80, 48)
work_life_balance = st.sidebar.select_slider(
    "⚖️ Work-Life Balance Rating",
    options=[1, 2, 3, 4, 5],
    value=2
)
social_isolation = st.sidebar.select_slider(
    "🤝 Social Isolation Level",
    options=[1, 2, 3, 4, 5],
    value=4
)

# Calculate Burnout Risk Index
risk_score = min(
    100,
    max(
        0,
        int(
            (hours_per_week * 1.15)
            + (social_isolation * 7.5)
            + ((6 - work_life_balance) * 8.5)
            - (age * 0.1)
        )
    )
)

# Color status determination
if risk_score >= 65:
    status_label = "HIGH RISK"
    status_color = "#ef4444"
    alert_class = "risk-alert-high"
elif risk_score >= 40:
    status_label = "MODERATE RISK"
    status_color = "#f59e0b"
    alert_class = "risk-alert-medium"
else:
    status_label = "LOW RISK"
    status_color = "#10b981"
    alert_class = "risk-alert-low"

# Key Performance Indicators Row
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <span style="color: #94a3b8; font-size: 0.9rem;">Weekly Workload</span>
        <h2 style="color: #38bdf8; margin: 10px 0 0 0;">{hours_per_week} hrs/wk</h2>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <span style="color: #94a3b8; font-size: 0.9rem;">Work-Life Balance</span>
        <h2 style="color: #818cf8; margin: 10px 0 0 0;">{work_life_balance} / 5</h2>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <span style="color: #94a3b8; font-size: 0.9rem;">Isolation Index</span>
        <h2 style="color: #c084fc; margin: 10px 0 0 0;">{social_isolation} / 5</h2>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <span style="color: #94a3b8; font-size: 0.9rem;">Burnout Status</span>
        <h2 style="color: {status_color}; margin: 10px 0 0 0;">{status_label}</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Main Dashboard Grid
left_col, right_col = st.columns([1.2, 1], gap="large")

with left_col:
    st.markdown("### 🎯 Burnout Risk Gauge Meter")

    # Logistic Regression - Sigmoid Curve
    pressure_score = (
        ((hours_per_week - 10) / 70) * 0.45
        + ((social_isolation - 1) / 4) * 0.30
        + ((5 - work_life_balance) / 4) * 0.25
    ) * 100

    # Sigmoid function
    def sigmoid(z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    # Generate the logistic curve
    x_values = np.linspace(0, 100, 500)
    probabilities = sigmoid((x_values - 50) / 10) * 100

    # Estimate current employee position on the curve
    employee_probability = float(
        sigmoid((pressure_score - 50) / 10) * 100
    )

    fig_gauge = go.Figure()

    # Low-risk background
    fig_gauge.add_vrect(
        x0=0, x1=40,
        fillcolor="rgba(16, 185, 129, 0.12)",
        line_width=0,
        layer="below"
    )

    # Moderate-risk background
    fig_gauge.add_vrect(
        x0=40, x1=65,
        fillcolor="rgba(245, 158, 11, 0.12)",
        line_width=0,
        layer="below"
    )

    # High-risk background
    fig_gauge.add_vrect(
        x0=65, x1=100,
        fillcolor="rgba(239, 68, 68, 0.12)",
        line_width=0,
        layer="below"
    )

    # Main Logistic Regression curve
    fig_gauge.add_trace(go.Scatter(
        x=x_values,
        y=probabilities,
        mode="lines",
        name="Logistic Regression Curve",
        line=dict(
            color="#38bdf8",
            width=4
        ),
        hovertemplate=(
            "Pressure Score: %{x:.1f}<br>"
            "Probability: %{y:.1f}%"
            "<extra></extra>"
        )
    ))

    # 50% probability reference
    fig_gauge.add_hline(
        y=50,
        line_dash="dash",
        line_color="#94a3b8",
        opacity=0.7,
        annotation_text="50% Probability",
        annotation_font_color="#cbd5e1"
    )

    # Current employee marker
    fig_gauge.add_trace(go.Scatter(
        x=[pressure_score],
        y=[employee_probability],
        mode="markers+text",
        name="Current Employee",
        marker=dict(
            size=15,
            color=status_color,
            line=dict(
                color="#ffffff",
                width=2
            )
        ),
        text=[f"{employee_probability:.1f}%"],
        textposition="top center",
        textfont=dict(
            color="#f8fafc",
            size=13
        ),
        hovertemplate=(
            "Employee Pressure Score: %{x:.1f}<br>"
            "Estimated Probability: %{y:.1f}%"
            "<extra></extra>"
        )
    ))

    fig_gauge.update_layout(
        title=dict(
            text="Logistic Regression — Burnout Probability",
            font=dict(
                size=20,
                color="#f8fafc"
            ),
            x=0.5
        ),
        paper_bgcolor="rgba(30, 41, 59, 0.5)",
        plot_bgcolor="#1e293b",
        font=dict(
            color="#f8fafc",
            family="sans-serif"
        ),
        height=420,
        margin=dict(
            l=50,
            r=30,
            t=85,
            b=65
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            title="Employee Workload Pressure Score",
            range=[0, 100],
            dtick=20,
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.15)",
            zeroline=False
        ),
        yaxis=dict(
            title="Burnout Probability (%)",
            range=[0, 105],
            dtick=20,
            ticksuffix="%",
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.15)",
            zeroline=False
        )
    )

    st.plotly_chart(fig_gauge, use_container_width=True)

    # Display curve output
    st.markdown(f"""
    <div class="metric-card">
        <span style="color:#94a3b8;font-size:0.9rem;">
            Logistic Curve Output
        </span>
        <h2 style="color:{status_color};margin:10px 0;">
            {employee_probability:.1f}%
        </h2>
        <span style="color:#cbd5e1;">
            Pressure Score: {pressure_score:.1f} / 100
        </span>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown("### 📋 Executive Diagnostic Summary")

    if risk_score >= 65:
        st.markdown(f"""
        <div class="{alert_class}">
            <h4 style="margin-top:0;">🚨 High Burnout Risk Detected</h4>
            <p>The system predicts a critical likelihood of work-related fatigue and stress.</p>
            <b>Recommended HR Interventions:</b>
            <ul>
                <li>Mandatory workload re-allocation and overtime cap.</li>
                <li>Schedule employee well-being check-ins.</li>
                <li>Promote flexible working hours.</li>
            </ul>
        </div>
         """, unsafe_allow_html=True)
    elif risk_score >= 40:
         st.markdown(f"""

        <div class="{alert_class}">
            <h4 style="margin: 0; color: #b45309;">⚠️ Moderate Burnout Risk</h4>
            <p style="margin: 5px 0 0 0;">The employee shows moderate indicators of work-related stress. Consider scheduling a check-in.</p>
        </div>
        """, unsafe_allow_html=True)
