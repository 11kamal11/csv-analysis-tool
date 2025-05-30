import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import base64

# Set page configuration
st.set_page_config(page_title="Data Analysis & Visualization Tool", layout="wide")

# Title
st.title("Comprehensive CSV Data Analysis Tool")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], help="Upload a CSV with categorical and numerical columns.")

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Data Analysis Section
        st.subheader("Data Analysis")
        st.write("**Preview (First 5 Rows):**")
        st.dataframe(df.head())
        
        st.write("**Summary Statistics:**")
        st.write(df.describe())
        
        st.write("**Missing Values:**")
        st.write(df.isnull().sum())
        
        st.write("**Data Types:**")
        st.write(df.dtypes)
        
        # Column selection for visualization
        st.subheader("Visualization Options")
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        if not categorical_cols or not numerical_cols:
            st.warning("CSV must have at least one categorical and one numerical column.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                cat_col = st.selectbox("Categorical Column (for Pie/Bar Chart)", categorical_cols)
            with col2:
                num_col = st.selectbox("Numerical Column (for Charts)", numerical_cols)
            
            bins = st.slider("Number of Histogram Bins", 5, 50, 10)
            chart_type = st.multiselect("Select Chart Types", ["Pie Chart", "Histogram", "Bar Chart", "Scatter Plot"], default=["Pie Chart", "Histogram"])
            
            # Visualization Section
            if chart_type:
                st.subheader("Visualizations")
                figs = []
                
                if "Pie Chart" in chart_type:
                    st.write("**Pie Chart**")
                    fig1, ax1 = plt.subplots(figsize=(6, 4))
                    ax1.pie(df[num_col], labels=df[cat_col], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
                    ax1.set_title(f'Distribution of {num_col} by {cat_col}')
                    ax1.axis('equal')
                    st.pyplot(fig1)
                    figs.append((fig1, "pie_chart.png"))
                
                if "Histogram" in chart_type:
                    st.write("**Histogram**")
                    fig2, ax2 = plt.subplots(figsize=(6, 4))
                    sns.histplot(df[num_col], bins=bins, ax=ax2, color='skyblue')
                    ax2.set_title(f'Distribution of {num_col}')
                    ax2.set_xlabel(num_col)
                    ax2.set_ylabel('Frequency')
                    st.pyplot(fig2)
                    figs.append((fig2, "histogram.png"))
                
                if "Bar Chart" in chart_type:
                    st.write("**Bar Chart**")
                    fig3, ax3 = plt.subplots(figsize=(6, 4))
                    sns.barplot(x=num_col, y=cat_col, data=df, ax=ax3, palette='muted')
                    ax3.set_title(f'{num_col} by {cat_col}')
                    st.pyplot(fig3)
                    figs.append((fig3, "bar_chart.png"))
                
                if "Scatter Plot" in chart_type:
                    st.write("**Scatter Plot**")
                    if len(numerical_cols) >= 2:
                        num_col2 = st.selectbox("Second Numerical Column (for Scatter Plot)", numerical_cols, index=1 if len(numerical_cols) > 1 else 0)
                        fig4, ax4 = plt.subplots(figsize=(6, 4))
                        sns.scatterplot(x=df[num_col], y=df[num_col2], hue=df[cat_col], ax=ax4, palette='deep')
                        ax4.set_title(f'{num_col} vs {num_col2}')
                        ax4.set_xlabel(num_col)
                        ax4.set_ylabel(num_col2)
                        st.pyplot(fig4)
                        figs.append((fig4, "scatter_plot.png"))
                    else:
                        st.warning("Scatter plot requires at least two numerical columns.")
                
                # Report Generation
                st.subheader("Generate PDF Report")
                if st.button("Generate Report"):
                    buffer = BytesIO()
                    c = canvas.Canvas(buffer, pagesize=letter)
                    c.setFont("Helvetica", 12)
                    
                    # Title
                    c.drawString(50, 750, "Data Analysis Report")
                    c.drawString(50, 730, f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Summary
                    c.drawString(50, 700, "Summary Statistics:")
                    stats = df.describe().to_string().split('\n')
                    y = 680
                    for line in stats[:5]:  # Limit to avoid overflow
                        c.drawString(50, y, line)
                        y -= 20
                    
                    # Missing Values
                    c.drawString(50, y-20, "Missing Values:")
                    missing = df.isnull().sum().to_string().split('\n')
                    y -= 40
                    for line in missing[:5]:
                        c.drawString(50, y, line)
                        y -= 20
                    
                    # Save charts to PDF
                    for fig, fname in figs:
                        fig.savefig(fname, dpi=100)
                        c.drawImage(fname, 50, y-150, width=300, height=200)
                        y -= 220
                    
                    c.save()
                    buffer.seek(0)
                    
                    # Download button
                    b64 = base64.b64encode(buffer.getvalue()).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="data_report.pdf">Download PDF Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.success("Report generated! Click the link above to download.")
                
                # Download individual charts
                st.subheader("Download Charts")
                for _, fname in figs:
                    with open(fname, 'rb') as file:
                        st.download_button(f"Download {fname}", file, file_name=fname, mime="image/png")
    except Exception as e:
        st.error(f"Error processing CSV: {e}")
else:
    st.info("Upload a CSV file to analyze and visualize.")