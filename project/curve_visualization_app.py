import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline
from scipy.optimize import curve_fit
import io

# Page configuration
st.set_page_config(
    page_title="Interactive Curve Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 Interactive Curve Visualization System</p>', unsafe_allow_html=True)
st.write("**Dynamic curve generation and analysis based on your dataset and parameters**")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Upload dataset
    uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])
    
    st.markdown("---")
    
    # Advanced options
    st.subheader("Advanced Options")
    show_equation = st.checkbox("Show Equation", value=True)
    show_residuals = st.checkbox("Show Residuals Plot", value=False)
    show_metrics = st.checkbox("Show Fit Metrics", value=True)
    point_size = st.slider("Point Size", 3, 15, 8)
    line_width = st.slider("Line Width", 1, 5, 2)

# Load or generate dataset
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        df = None
else:
    # Generate sample data
    np.random.seed(42)
    x_sample = np.linspace(0, 10, 20)
    y_sample = 2*x_sample + 5 + np.random.randn(20) * 2
    df = pd.DataFrame({"X": x_sample, "Y": y_sample})
    st.info("ℹ️ Using sample dataset. Upload your own CSV to analyze custom data.")

if df is not None:
    # Dataset preview
    with st.expander("📋 Dataset Preview", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df.head(10), use_container_width=True)
        with col2:
            st.write("**Dataset Statistics:**")
            st.dataframe(df.describe(), use_container_width=True)
    
    # Column selection
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("📈 Select X Column", df.columns, index=0)
    with col2:
        y_col = st.selectbox("📊 Select Y Column", df.columns, index=min(1, len(df.columns)-1))
    
    # Extract and validate data
    try:
        x = df[x_col].dropna().values
        y = df[y_col].dropna().values
        
        # Ensure x and y have same length
        min_len = min(len(x), len(y))
        x = x[:min_len]
        y = y[:min_len]
        
        if len(x) < 3:
            st.error("❌ Need at least 3 data points for curve fitting.")
            st.stop()
        
        # Sort by x for better visualization
        sort_idx = np.argsort(x)
        x = x[sort_idx]
        y = y[sort_idx]
        
    except Exception as e:
        st.error(f"Error processing data: {e}")
        st.stop()
    
    # Curve type selection
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        curve_type = st.selectbox(
            "🔄 Select Curve Type",
            ["Linear", "Polynomial", "Exponential", "Logarithmic", "Power", "Spline"]
        )
    
    with col2:
        view_mode = st.radio("👁️ View Mode", ["2D", "3D"], horizontal=True)
    
    # Curve-specific parameters
    degree = 2
    smooth_points = 300
    
    if curve_type == "Polynomial":
        degree = st.slider("Polynomial Degree", 2, min(10, len(x)-1), 3)
    elif curve_type == "Spline":
        smooth_points = st.slider("Smoothness (points)", 100, 1000, 300)
    
    # Curve calculation
    equation_text = ""
    y_fit = None
    x_fit = x.copy()
    r_squared = 0
    
    try:
        if curve_type == "Linear":
            coeff = np.polyfit(x, y, 1)
            model = np.poly1d(coeff)
            y_fit = model(x)
            equation_text = f"y = {coeff[0]:.4f}x + {coeff[1]:.4f}"
            
        elif curve_type == "Polynomial":
            coeff = np.polyfit(x, y, degree)
            model = np.poly1d(coeff)
            y_fit = model(x)
            
            # Build equation string
            terms = []
            for i, c in enumerate(coeff):
                power = degree - i
                if power == 0:
                    terms.append(f"{c:.4f}")
                elif power == 1:
                    terms.append(f"{c:.4f}x")
                else:
                    terms.append(f"{c:.4f}x^{power}")
            equation_text = "y = " + " + ".join(terms)
            
        elif curve_type == "Exponential":
            # Handle negative or zero values
            y_pos = np.where(y <= 0, 0.001, y)
            coeff = np.polyfit(x, np.log(y_pos), 1)
            a = np.exp(coeff[1])
            b = coeff[0]
            y_fit = a * np.exp(b * x)
            equation_text = f"y = {a:.4f} * e^({b:.4f}x)"
            
        elif curve_type == "Logarithmic":
            # Handle negative or zero x values
            x_pos = np.where(x <= 0, 0.001, x)
            coeff = np.polyfit(np.log(x_pos), y, 1)
            a, b = coeff[0], coeff[1]
            y_fit = a * np.log(x_pos) + b
            equation_text = f"y = {a:.4f} * ln(x) + {b:.4f}"
            
        elif curve_type == "Power":
            # Handle negative or zero values
            x_pos = np.where(x <= 0, 0.001, x)
            y_pos = np.where(y <= 0, 0.001, y)
            coeff = np.polyfit(np.log(x_pos), np.log(y_pos), 1)
            a = np.exp(coeff[1])
            b = coeff[0]
            y_fit = a * (x_pos ** b)
            equation_text = f"y = {a:.4f} * x^{b:.4f}"
            
        elif curve_type == "Spline":
            x_fit = np.linspace(x.min(), x.max(), smooth_points)
            spline = make_interp_spline(x, y, k=min(3, len(x)-1))
            y_fit = spline(x_fit)
            equation_text = "Cubic Spline Interpolation"
        
        # Calculate R-squared
        if y_fit is not None:
            if curve_type == "Spline":
                # For spline, evaluate at original x points
                spline = make_interp_spline(x, y, k=min(3, len(x)-1))
                y_pred = spline(x)
            else:
                y_pred = y_fit
                
            ss_res = np.sum((y - y_pred[:len(y)]) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
    except Exception as e:
        st.error(f"Error fitting curve: {e}")
        st.stop()
    
    # Display metrics
    if show_metrics and y_fit is not None:
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("R² Score", f"{r_squared:.4f}")
        with col2:
            rmse = np.sqrt(np.mean((y - y_fit[:len(y)]) ** 2))
            st.metric("RMSE", f"{rmse:.4f}")
        with col3:
            st.metric("Data Points", len(x))
        with col4:
            mae = np.mean(np.abs(y - y_fit[:len(y)]))
            st.metric("MAE", f"{mae:.4f}")
    
    if show_equation and equation_text:
        st.info(f"**Equation:** {equation_text}")
    
    # Visualization
    st.markdown("---")
    st.subheader("📈 Visualization")
    
    if view_mode == "2D":
        fig = go.Figure()
        
        # Add scatter points
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='markers',
            name='Data Points',
            marker=dict(size=point_size, color='#636EFA', opacity=0.7),
            hovertemplate='X: %{x:.4f}<br>Y: %{y:.4f}<extra></extra>'
        ))
        
        # Add fitted curve
        if y_fit is not None:
            fig.add_trace(go.Scatter(
                x=x_fit, y=y_fit,
                mode='lines',
                name=f'{curve_type} Fit',
                line=dict(color='#EF553B', width=line_width),
                hovertemplate='X: %{x:.4f}<br>Y: %{y:.4f}<extra></extra>'
            ))
        
        fig.update_layout(
            title=f"2D {curve_type} Curve Visualization",
            xaxis_title=x_col,
            yaxis_title=y_col,
            hovermode='closest',
            template='plotly_white',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # 3D mode
        z = np.zeros_like(x)
        z_fit = np.zeros_like(x_fit)
        
        fig = go.Figure()
        
        # Add scatter points
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            name='Data Points',
            marker=dict(size=point_size, color='#636EFA', opacity=0.7)
        ))
        
        # Add fitted curve
        if y_fit is not None:
            fig.add_trace(go.Scatter3d(
                x=x_fit, y=y_fit, z=z_fit,
                mode='lines',
                name=f'{curve_type} Fit',
                line=dict(color='#EF553B', width=line_width)
            ))
        
        fig.update_layout(
            title=f"3D {curve_type} Curve Visualization",
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title='Z'
            ),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Residuals plot
    if show_residuals and y_fit is not None:
        st.markdown("---")
        st.subheader("📉 Residuals Analysis")
        
        residuals = y - y_fit[:len(y)]
        
        fig_res = go.Figure()
        fig_res.add_trace(go.Scatter(
            x=x, y=residuals,
            mode='markers',
            marker=dict(size=8, color='#00CC96'),
            name='Residuals'
        ))
        fig_res.add_hline(y=0, line_dash="dash", line_color="red")
        
        fig_res.update_layout(
            title="Residuals Plot",
            xaxis_title=x_col,
            yaxis_title="Residuals",
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig_res, use_container_width=True)
    
    # Download options
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download graph as PNG
        try:
            img_bytes = fig.to_image(format="png", width=1200, height=800)
            st.download_button(
                label="⬇️ Download Graph (PNG)",
                data=img_bytes,
                file_name=f"curve_visualization_{curve_type.lower()}.png",
                mime="image/png"
            )
        except:
            st.warning("Install kaleido for image export: pip install kaleido")
    
    with col2:
        # Download fitted data as CSV
        if y_fit is not None:
            fitted_df = pd.DataFrame({
                'X': x_fit,
                'Y_fitted': y_fit
            })
            csv = fitted_df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Fitted Data (CSV)",
                data=csv,
                file_name=f"fitted_data_{curve_type.lower()}.csv",
                mime="text/csv"
            )
    
    with col3:
        # Download report
        report = f"""Curve Fitting Report
========================
Curve Type: {curve_type}
Equation: {equation_text}
R² Score: {r_squared:.4f}
Data Points: {len(x)}
X Column: {x_col}
Y Column: {y_col}
========================
"""
        st.download_button(
            label="⬇️ Download Report (TXT)",
            data=report,
            file_name=f"curve_report_{curve_type.lower()}.txt",
            mime="text/plain"
        )
    
    st.success("✨ Change dataset or parameters to update the curve in real time!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
    💡 <b>Tip:</b> Use the sidebar to access advanced options and upload your own datasets.
    </div>
    """, unsafe_allow_html=True)
