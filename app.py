import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

st.title("Data Visualization Tool")
st.caption("made by Yeonsu Kim")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the CSV file
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())

    # Function to extract 'overall_accuracy'
    def extract_overall_accuracy_v2(dict_str):
        try:
            data_dict = ast.literal_eval(dict_str)  # Safely evaluate the string as a Python dictionary
            return data_dict.get('overall_accuracy', None)  # Extract the overall_accuracy value
        except (ValueError, SyntaxError):
            return None

    # Function to extract 'overall_fscore'
    def extract_overall_fscore_v2(dict_str):
        try:
            data_dict = ast.literal_eval(dict_str)  # Safely evaluate the string as a Python dictionary
            return data_dict.get('overall_fscore', None)  # Extract the overall_fscore value
        except (ValueError, SyntaxError):
            return None

    # Extracting 'train' and 'test'
    data['train'] = data['file_name'].str.split('--').str[0].str.split('-').str[3:5].str.join('-')
    data['test'] = data['file_name'].str.split('--').str[1].str.split('-').str[1:3].str.join('-')
    data['group'] = data['train'] + ' - ' + data['test']
        
    # Selecting relevant columns
    data = data[['group', 'train', 'test', 'content']]
    
    # Applying the extraction functions
    data['overall_accuracy'] = data['content'].apply(extract_overall_accuracy_v2)
    data['overall_fscore'] = data['content'].apply(extract_overall_fscore_v2)

    # Finalizing the dataset to display and download
    data = data[['group', 'train', 'test', 'overall_accuracy', 'overall_fscore']]
    
    # Display the processed data
    st.write("Processed Data:", data)

    # Option to download the processed data as a CSV file
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download Processed Data as CSV",
        data=csv,
        file_name='processed_data.csv',
        mime='text/csv',
    )
    
    # Ensure only numeric columns are included in the groupby mean calculation
    numeric_columns = ['overall_accuracy', 'overall_fscore']
    grouped_data = data.groupby('group')[numeric_columns].mean().reset_index()
    
    # Plotting the line plots for overall_accuracy and overall_fscore by each group
    st.subheader("Line Plots of Overall Accuracy and Fscore by Group")

    groups = grouped_data['group'].unique()
    
    for group in groups:
        group_data = grouped_data[grouped_data['group'] == group]

        # Plotting overall_accuracy
        st.write(f"Group: {group} - Overall Accuracy")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=group_data, x='group', y='overall_accuracy', marker='o')
        plt.title(f'Overall Accuracy for {group}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

        # Plotting overall_fscore
        st.write(f"Group: {group} - Overall Fscore")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=group_data, x='group', y='overall_fscore', marker='o')
        plt.title(f'Overall Fscore for {group}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)
