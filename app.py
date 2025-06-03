# (All import and utility code remains unchanged...)

def main():
    st.title("Modern CSV Data Analysis & Visualization")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], help="Upload a CSV with at least one categorical and one numerical column.")
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None and not df.empty:
            st.success(f"Loaded {len(df)} rows and {len(df.columns)} columns!")
            
            # Data Analysis
            st.header("Data Analysis")
            st.subheader("Full Data Table")
            page_size = 10
            total_rows = len(df)
            max_pages = (total_rows + page_size - 1) // page_size
            col1, col2 = st.columns([2, 3])
            with col1:
                current_page = st.number_input("Page", min_value=1, max_value=max_pages, value=1, step=1)
            with col2:
                st.write(f"Showing page {current_page} of {max_pages} (Total rows: {total_rows})")
            start_idx = (current_page - 1) * page_size
            end_idx = min(start_idx + page_size, total_rows)
            st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True, hide_index=False)
            
            if st.checkbox("Show Full Dataset", help="Display all rows (may be slow for large datasets)"):
                st.dataframe(df, use_container_width=True, hide_index=False, height=400)
            
            st.subheader("Summary Statistics")
            st.dataframe(df.describe(), use_container_width=True)
            
            st.subheader("Data Types")
            st.dataframe(pd.DataFrame({'Column': df.columns, 'Type': df.dtypes}), use_container_width=True, hide_index=True)
            
            # Visualizations
            st.header("Visualizations")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            if not categorical_cols or not numeric_cols:
                st.warning("CSV must have at least one categorical and one numerical column.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    cat_col = st.selectbox("Categorical Column", categorical_cols)
                with col2:
                    num_col = st.selectbox("Numerical Column", numeric_cols)
                bins = st.slider("Histogram Bins", 5, 50, 10, step=5)
                
                # Pie Chart
                st.subheader("Pie Chart")
                value_counts = df.groupby(cat_col)[num_col].sum().reset_index()
                fig1 = px.pie(value_counts, names=cat_col, values=num_col, title=f'Distribution of {num_col} by {cat_col}',
                              color_discrete_sequence=px.colors.qualitative.Pastel)
                fig1.update_layout(template='plotly_white', font=dict(family="Arial", size=12))
                st.plotly_chart(fig1, use_container_width=True)
                
                # Histogram
                st.subheader("Histogram")
                fig2 = px.histogram(df, x=num_col, nbins=bins, title=f'Distribution of {num_col}',
                                   color_discrete_sequence=['teal'])
                fig2.update_layout(template='plotly_white', font=dict(family="Arial", size=12))
                st.plotly_chart(fig2, use_container_width=True)
                
                # Bar Chart
                st.subheader("Bar Chart")
                fig3 = px.bar(df, x=cat_col, y=num_col, title=f'{num_col} by {cat_col}',
                             color_discrete_sequence=['coral'])
                fig3.update_layout(template='plotly_white', font=dict(family="Arial", size=12))
                st.plotly_chart(fig3, use_container_width=True)
                
                # Scatter Plot
                st.subheader("Scatter Plot")
                if len(numeric_cols) >= 2:
                    num_col2 = st.selectbox("Second Numerical Column", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="scatter_num")
                    fig4 = px.scatter(df, x=num_col, y=num_col2, color=cat_col, title=f'{num_col} vs {num_col2}',
                                     color_discrete_sequence=px.colors.qualitative.Dark2)
                    fig4.update_layout(template='plotly_white', font=dict(family="Arial", size=12))
                    st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.warning("Scatter plot requires at least two numerical columns.")
                
                # Box Plot
                st.subheader("Box Plot")
                fig5 = px.box(df, x=cat_col, y=num_col, title=f'{num_col} by {cat_col}',
                             color_discrete_sequence=['purple'])
                fig5.update_layout(template='plotly_white', font=dict(family="Arial", size=12))
                st.plotly_chart(fig5, use_container_width=True)
                
                # Q-Q Plot
                st.subheader("Q-Q Plot")
                fig6 = create_qq_plot(df, num_col)
                if fig6:
                    st.plotly_chart(fig6, use_container_width=True)
                else:
                    st.warning(f"No valid data for Q-Q plot of {num_col}.")
                
                # Conclusion
                st.header("Conclusion")
                conclusion = generate_conclusion(df, num_col, cat_col)
                st.markdown(conclusion)

if __name__ == "__main__":
    main()
