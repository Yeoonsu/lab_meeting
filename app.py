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
    data['train'] = data['file_name'].str.split('-').str[4] + '-' + data['file_name'].str.split('-').str[5]
    data['test'] = data['file_name'].str.split('-').str[9] + '-' + data['file_name'].str.split('-').str[10]
    
    # Selecting relevant columns
    data = data[['train', 'test', 'content']]
    
    # Applying the extraction functions
    data['overall_accuracy'] = data['content'].apply(extract_overall_accuracy_v2)
    data['overall_fscore'] = data['content'].apply(extract_overall_fscore_v2)

    # Finalizing the dataset to display and download
    data = data[['train', 'test', 'overall_accuracy', 'overall_fscore']]
    
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
    grouped_data = data.groupby(['train', 'test'])[numeric_columns].mean().reset_index()
    
    # Plotting the line plots for overall_accuracy and overall_fscore
    st.subheader("Line Plots of Overall Accuracy and Fscore")
    plt.figure(figsize=(14, 8))

    # Line Plotting overall_accuracy
    plt.subplot(1, 2, 1)
    sns.lineplot(data=grouped_data, x='train', y='overall_accuracy', hue='test', marker='o')
    plt.title('Overall Accuracy by train and test')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Line Plotting overall_fscore
    plt.subplot(1, 2, 2)
    sns.lineplot(data=grouped_data, x='train', y='overall_fscore', hue='test', marker='o')
    plt.title('Overall Fscore by train and test')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the line plots in Streamlit
    st.pyplot(plt)
