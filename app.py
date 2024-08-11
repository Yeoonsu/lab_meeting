import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

st.title("Grouped Data Visualization with Line and Bar Plots")
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

    # Grouping the data by train and test and calculating the mean for overall_accuracy and overall_fscore
    grouped_data = data.groupby(['train', 'test']).mean().reset_index()

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

    # Plotting the bar plots for overall_accuracy and overall_fscore
    st.subheader("Bar Plots of Overall Accuracy and Fscore")
    plt.figure(figsize=(14, 8))

    # Bar Plotting overall_accuracy
    plt.subplot(1, 2, 1)
    sns.barplot(data=grouped_data, x='train', y='overall_accuracy', hue='test')
    plt.title('Overall Accuracy by train and test')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Bar Plotting overall_fscore
    plt.subplot(1, 2, 2)
    sns.barplot(data=grouped_data, x='test', y='overall_fscore', hue='test')
    plt.title('Overall Fscore by train and test')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the bar plots in Streamlit
    st.pyplot(plt)

    # Additional line plots for overall_accuracy and overall_fscore with 'train' and 'test'
    st.subheader("Additional Line Plots of Overall Accuracy and Fscore")
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

    # Display the additional line plots in Streamlit
    st.pyplot(plt)
