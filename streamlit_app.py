import pandas as pd
import streamlit as st


# Set page configuration
st.set_page_config(page_title="Client Leasing Dashboard", layout="wide")

# Load the uploaded file to inspect its contents
# File Upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


# Display title and header
st.title("Client Leasing Data Analysis")
st.header("Overview of Client Financial Data")

st.code("import pandas as pd ", language = "python")
st.code("import streamlit as st ", language = "python")
st.code("st.set_page_config(page_title=\"Client Leasing Dashboard\", layout=\"wide\")", language = "python")

st.code("""
st.title("Client Leasing Data Analysis")
st.header("Overview of Client Financial Data")
""", language="python")
if uploaded_file:
    # Show the entire dataset
    st.write("Here is the client dataset:")
    data = pd.read_csv(uploaded_file)
    st.subheader("Show the entire dataset")
    st.dataframe(data)

    # Show specific columns in a static table
    st.subheader("Show specific columns in a static table")
    st.table(data[['ID_CLIENT', 'NAME_CLIENT', 'JOB', 'INCOME_PER_YEAR']].head())

    # Line chart of annual income for visualization
    st.line_chart(data[['INCOME_PER_YEAR']])

    import plotly.express as px
    # Pie chart for 'JOB' (Profession) if it exists

      # Create 3 columns for side-by-side charts
    col1, col2, col3 = st.columns(3)

    # if 'JOB' in data.columns:
    #     profession_counts = data['JOB'].value_counts()
    #     fig_profession = px.pie(values=profession_counts.values, names=profession_counts.index, title="Distribution of Professions")
    #     st.plotly_chart(fig_profession)


    if 'JOB' in data.columns:
        profession_counts = data['JOB'].value_counts()
        fig_profession = px.pie(
            values=profession_counts.values, 
            names=profession_counts.index, 
            title="Distribution of Professions"
        )
        with col1:
            st.plotly_chart(fig_profession, use_container_width=True)
    # Pie chart for 'SEX' (Gender) if it exists
    # if 'SEX' in data.columns:
    #     gender_counts = data['SEX'].value_counts()
    #     fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index, title="Gender Distribution")
    #     st.plotly_chart(fig_gender)
    if 'SEX' in data.columns:
        gender_counts = data['SEX'].value_counts()
        fig_gender = px.pie(
            values=gender_counts.values, 
            names=gender_counts.index, 
            title="Gender Distribution"
        )
        with col2:
            st.plotly_chart(fig_gender, use_container_width=True)
    # Pie chart for another categorical column example, 'MARITAL_STATUS, if it exists
    # if 'MARITAL_STATUS' in data.columns:
    #     active_member_counts = data['MARITAL_STATUS'].value_counts()
    #     fig_active_member = px.pie(values=active_member_counts.values, names=active_member_counts.index, title="Marital Status Distribution")
    #     st.plotly_chart(fig_active_member)
        
    if 'MARITAL_STATUS' in data.columns:
        marital_counts = data['MARITAL_STATUS'].value_counts()
        fig_marital = px.pie(
            values=marital_counts.values, 
            names=marital_counts.index, 
            title="Marital Status Distribution"
        )
        with col3:
            st.plotly_chart(fig_marital, use_container_width=True)
    # Sidebar for user input
    st.sidebar.header("Filter Data")

    # Text input for searching client by name
    client_name = st.sidebar.text_input("Search by client name")

    # Select a profession to filter by
    profession = st.sidebar.selectbox("Select Profession", data['JOB'].unique())

    # Number input for minimum annual income
    min_income = st.sidebar.number_input("Minimum Income per Year", min_value=0, step=500)

    # Slider to select an age range
    age_range = st.sidebar.slider("Select Age Range", int(data['AGE'].min()), int(data['AGE'].max()), (25, 45))

    # Filter data based on user input
    filtered_data = data[
        (data['NAME_CLIENT'].str.contains(client_name, case=False)) &
        (data['JOB'] == profession) &
        (data['INCOME_PER_YEAR'] >= min_income) &
        (data['AGE'].between(age_range[0], age_range[1]))
    ]

    st.write("Filtered Data:", filtered_data)

    # Display a success message if data is filtered successfully
    if not filtered_data.empty:
        st.success("Data filtered successfully!")
    else:
        st.warning("No data matches the specified filters.")
        
    # Display progress bar during data loading or processing
    import time
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)  # simulate processing time
        progress_bar.progress(i + 1)


    # Create expandable section
    with st.expander("Show Descriptions"):
        st.write(data['DESCRIPTION'].head())

    # Create two columns for side-by-side comparison
    col1, col2 = st.columns(2)
    col1.metric("Average Income", data['INCOME_PER_YEAR'].mean())
    col2.metric("Average Deposit", data['DEPOSIT_AMOUNT'].mean())

    summary_stats = data.describe()

    # Display header
    # st.header("Summary Statistics of Clients")
    st.markdown("<h1 style='color:green;'>Summary Statistics of Clients</h1>", unsafe_allow_html=True)
    # Display summary statistics
    st.write("Below are the summary statistics for the numerical columns in the dataset:")
    st.dataframe(summary_stats)

    # Additional optional feature: Display specific metrics
    st.subheader("Key Metrics")
    st.markdown("<h2 style='color:red;'>Key Metrics</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Annual Income", f"{summary_stats['INCOME_PER_YEAR']['mean']:.2f}")
    col2.metric("Average Current Account", f"{summary_stats['ACCOUNT']['mean']:.2f}")
    col3.metric("Average Deposit", f"{summary_stats['DEPOSIT_AMOUNT']['mean']:.2f}")

    # Non-Numeric Summary Statistics
    st.subheader("Non-Numeric Columns Analysis")
    st.markdown("<h2 style='color:green;'>Non-Numeric Columns Analysis</h1>", unsafe_allow_html=True)

    # Analyze non-numeric columns in two-column layout
    non_numeric_data = data.select_dtypes(include='object')

    columns = st.columns(2)  # Create two columns for layout
    col_idx = 0  # Column index to alternate between columns

    for column in non_numeric_data.columns:
        with columns[col_idx]:  # Place the analysis in alternating columns
            st.write(f"**{column}**")
            st.write(f"Unique values: {non_numeric_data[column].nunique()}")
            st.write(f"Most frequent value: {non_numeric_data[column].mode()[0]} (appears {non_numeric_data[column].value_counts().max()} times)")
            st.write("Value counts:")
            st.write(non_numeric_data[column].value_counts())
            st.write("---")  # Separator line for readability
        # Toggle column index to alternate between the two columns
        col_idx = (col_idx + 1) % 2

    # Example breakdown of specific columns (optional)
    st.subheader("Detailed Analysis of Specific Columns")
    st.markdown("<h2 style='color:red;'>Detailed Analysis of Specific Columns</h1>", unsafe_allow_html=True)
    if 'SEX' in data.columns:
        st.write("Gender Distribution")
        st.bar_chart(data['SEX'].value_counts())

    if 'JOB' in data.columns:
        st.write("Profession Distribution (Top 10)")
        st.bar_chart(data['JOB'].value_counts().head(10))

    # Summary Statistics Completed
    st.success("Summary Statistics and Non-Numeric Analysis Completed")

    # Initialize session state for data
    if 'data' not in st.session_state:
        if uploaded_file is not None:
            st.session_state['data'] = data
            st.success("File loaded successfully! You can now select a client to update.")

    # Display title
    st.title("Client Leasing Data Update")
    st.header("Update Client Information Using Client ID")
    st.markdown("<h1 style='color:blue;'>Update Client Information Using Client ID</h1>", unsafe_allow_html=True)

    if 'data' in st.session_state and st.session_state['data'] is not None:
    # Select a specific client by ID
        client_id = st.selectbox("Choose Client ID", st.session_state['data']['ID_CLIENT'].unique())

        # Show current information for the selected client
        client_data = st.session_state['data'][st.session_state['data']['ID_CLIENT'] == client_id].iloc[0]
        st.write("Current Information for Selected Client:")
        st.write(client_data)

        # Form for submitting client data updates
        with st.form("client_update"):
            # Input fields to update client details
            new_income = st.number_input(
                "Update Annual Income", 
                min_value=0.0, 
                step=1000.0, 
                value=float(client_data['INCOME_PER_YEAR'])
            )
            new_age = st.number_input(
                "Update Age", 
                min_value=0, 
                step=1, 
                value=int(client_data['AGE'])
            )
            
            # Submit button for updating
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                # Update the selected client’s data in the DataFrame
                st.session_state['data'].loc[st.session_state['data']['ID_CLIENT'] == client_id, 'INCOME_PER_YEAR'] = new_income
                st.session_state['data'].loc[st.session_state['data']['ID_CLIENT'] == client_id, 'AGE'] = new_age
                
                # Display success message and updated client information
                st.success(f"Updated client ID {client_id}")
                st.write("Updated Client Information:")
                st.write(st.session_state['data'][st.session_state['data']['ID_CLIENT'] == client_id])

        # Save button outside the form
        if st.button("Save Changes to CSV"):
            st.session_state['data'].to_csv('updated_clienti_leasing.csv', index=False)
            st.success("Data saved to updated_clienti_leasing.csv")
            # Convert DataFrame to CSV
        csv = st.session_state['data'].to_csv(index=False).encode('utf-8')  
        # Download button
        st.download_button(
                label="Download data as CSV", 
                data = csv,
                file_name='updated_client_data.csv',
                mime='text/csv',)
              

    else:
        st.warning("Please upload a CSV file to proceed.")

    # Displaying an image (if you have a related file path or URL)
    st.image("https://st.depositphotos.com/2309453/4248/i/450/depositphotos_42483789-stock-photo-smiling-young-man-shaking-hands.jpg", caption="Sample Image")

    # Adding audio or video files, if available
    #st.audio("/path/to/sample_audio.mp3")
    st.video("https://youtu.be/G6WtlnWjZC8")
    

