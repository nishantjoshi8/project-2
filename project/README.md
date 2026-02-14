# 📊 Interactive Curve Visualization System

A powerful and user-friendly Streamlit application for interactive curve fitting and visualization.

## ✨ Features

### Core Functionality
- **Multiple Curve Types**: Linear, Polynomial, Exponential, Logarithmic, Power, and Spline interpolation
- **Interactive Visualization**: Real-time 2D and 3D plotting with Plotly
- **Data Upload**: Support for CSV file uploads
- **Fit Metrics**: Automatic calculation of R², RMSE, and MAE
- **Residuals Analysis**: Optional residuals plot for model evaluation

### Advanced Features
- Customizable point size and line width
- Equation display with formatted mathematical notation
- Dataset statistics and preview
- Multiple download options (PNG, CSV, TXT report)
- Responsive design with sidebar controls
- Error handling and data validation

## 🚀 Installation

1. **Clone or download the repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run curve_visualization_app.py
   ```

## 📖 Usage Guide

### Basic Workflow

1. **Upload Data** (Optional)
   - Click "Upload CSV File" in the sidebar
   - Or use the built-in sample dataset

2. **Select Columns**
   - Choose X and Y columns from your dataset

3. **Choose Curve Type**
   - Linear: Straight line fit
   - Polynomial: Flexible curve (adjust degree)
   - Exponential: Exponential growth/decay
   - Logarithmic: Logarithmic relationship
   - Power: Power law relationship
   - Spline: Smooth interpolation

4. **Customize Visualization**
   - Select 2D or 3D view mode
   - Adjust point size and line width
   - Enable/disable equation, metrics, and residuals

5. **Download Results**
   - Download graph as PNG
   - Export fitted data as CSV
   - Save analysis report as TXT

### Curve Types Explained

#### Linear
- **Equation**: y = mx + b
- **Best for**: Data with constant rate of change
- **Example**: Distance vs. time at constant speed

#### Polynomial
- **Equation**: y = a₀ + a₁x + a₂x² + ... + aₙxⁿ
- **Best for**: Data with curves and inflection points
- **Parameters**: Degree (2-10)
- **Example**: Projectile motion

#### Exponential
- **Equation**: y = ae^(bx)
- **Best for**: Growth or decay processes
- **Example**: Population growth, radioactive decay

#### Logarithmic
- **Equation**: y = a·ln(x) + b
- **Best for**: Diminishing returns relationships
- **Example**: Learning curves, pH scale

#### Power
- **Equation**: y = ax^b
- **Best for**: Scaling relationships
- **Example**: Area vs. radius, energy vs. frequency

#### Spline
- **Type**: Cubic spline interpolation
- **Best for**: Smooth curves through all points
- **Parameters**: Smoothness (100-1000 points)
- **Example**: Smooth transitions, animation paths

## 📊 Understanding the Metrics

### R² Score (Coefficient of Determination)
- **Range**: 0 to 1 (or negative for poor fits)
- **Interpretation**:
  - 1.0: Perfect fit
  - 0.7-0.9: Good fit
  - 0.5-0.7: Moderate fit
  - <0.5: Poor fit

### RMSE (Root Mean Square Error)
- **Interpretation**: Average prediction error in Y units
- **Lower is better**
- **Use**: Compare different models on same data

### MAE (Mean Absolute Error)
- **Interpretation**: Average absolute prediction error
- **Lower is better**
- **Advantage**: Less sensitive to outliers than RMSE

## 📁 CSV File Format

Your CSV file should have:
- Header row with column names
- Numerical data
- At least 3 rows of data

Example:
```csv
Time,Temperature
0,20
1,22
2,25
3,29
4,34
```

## 🎨 Customization Options

### Sidebar Controls
- **Upload Dataset**: Load your own CSV files
- **Show Equation**: Display mathematical formula
- **Show Residuals Plot**: Analyze fit quality
- **Show Fit Metrics**: Display R², RMSE, MAE
- **Point Size**: Adjust marker size (3-15)
- **Line Width**: Adjust curve thickness (1-5)

### View Modes
- **2D**: Traditional scatter plot with fitted curve
- **3D**: Three-dimensional visualization (Z=0 plane)

## 🔧 Troubleshooting

### Common Issues

**"Need at least 3 data points"**
- Ensure your dataset has at least 3 valid rows
- Check for missing values

**"Error fitting curve"**
- Try a different curve type
- Check for extreme values or outliers
- Ensure data is appropriate for chosen model

**Image export not working**
- Install kaleido: `pip install kaleido`
- Or use the "Download Fitted Data" option

### Data Validation
- Negative/zero values are handled automatically
- Data is sorted by X values for better visualization
- Missing values are removed automatically

## 💡 Tips for Best Results

1. **Choose the Right Curve Type**:
   - Start with Linear to understand the trend
   - Use Polynomial for complex relationships
   - Try Exponential/Logarithmic for specific patterns

2. **Polynomial Degree**:
   - Lower degrees (2-3): Smoother, less overfitting
   - Higher degrees (4+): More flexible, risk of overfitting
   - Rule of thumb: Use lowest degree with good R²

3. **Data Quality**:
   - Remove outliers for better fits
   - Ensure sufficient data points (20+ recommended)
   - Check for measurement errors

4. **Interpretation**:
   - Always check residuals plot for patterns
   - Compare multiple models
   - Consider domain knowledge, not just metrics

## 📚 Dependencies

- **streamlit**: Web application framework
- **numpy**: Numerical computing
- **pandas**: Data manipulation
- **plotly**: Interactive plotting
- **scipy**: Scientific computing (curve fitting)
- **kaleido**: Image export (optional)

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your data format
3. Try with the sample dataset
4. Check Python/package versions

## 📝 License

This project is open source and available for educational and commercial use.

## 🎯 Future Enhancements

Potential additions:
- Custom equation input
- Multiple datasets comparison
- Confidence intervals
- Cross-validation
- More curve types (sigmoid, Gaussian, etc.)
- Animation capabilities
- Report generation with charts

---

**Version**: 1.0  
**Last Updated**: 2026  
**Author**: Interactive Visualization Tool
