
import streamlit as st
import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Data Processing and Visualization App")

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

    # Display processed data
    st.write("Processed Data:", data)

    # Save the processed data to a new CSV (optional)
    save_option = st.checkbox("Save processed data to CSV")
    if save_option:
        data.to_csv('output2.csv', index=False)
        st.write("Processed data saved to `output2.csv`.")

    # Visualization
    st.subheader("Data Visualization")

    # Set the aesthetic style of the plots
    sns.set_style('whitegrid')

    # Create a figure and a set of subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plotting the 'overall_accuracy' values
    sns.histplot(data['overall_accuracy'], bins=10, ax=axes[0])
    axes[0].set_title('Distribution of Overall Accuracy')

    # Plotting the 'overall_fscore' values
    sns.histplot(data['overall_fscore'], bins=10, ax=axes[1])
    axes[1].set_title('Distribution of Overall F-score')

    # Display the plots in Streamlit
    st.pyplot(fig)
