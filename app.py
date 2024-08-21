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
    
    # Defining train_group and test_group
    data['train_group'] = data['train'].str.split('-').str[0]
    data['test_group'] = data['test'].str.split('-').str[0]
    
    # Defining the final group column
    data['group'] = data['train'] + ' - ' + data['test']
        
    # Selecting relevant columns
    data = data[['group', 'train', 'test', 'train_group', 'test_group', 'content']]
    
    # Applying the extraction functions
    data['overall_accuracy'] = data['content'].apply(extract_overall_accuracy_v2)
    data['overall_fscore'] = data['content'].apply(extract_overall_fscore_v2)

    # Finalizing the dataset to display and download
    data = data[['group', 'train', 'test', 'train_group', 'test_group', 'overall_accuracy', 'overall_fscore']]
    
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

    # Plotting the line plots for overall_accuracy and overall_fscore by each train group (comp, freq3, missing)
    st.subheader("Line Plots of Overall Accuracy and Fscore by Train Group and Test Group (Including Clean)")

    train_groups = ['comp', 'freq3', 'missing', 'clean']
    test_groups = ['missing', 'comp', 'freq3', 'clean']  # Clean을 포함한 모든 그룹

    for train_group in train_groups:
        for test_group in test_groups:
            # Filter the data for the current train_group and test_group
            group_data = data[(data['train_group'] == train_group) & (data['test_group'] == test_group)]
            
            if not group_data.empty:
                # Sort the data by 'train' and 'test'
                group_data = group_data.sort_values(by=['train', 'test'])
                
                # Plotting overall_accuracy
                st.write(f"Train Group: {train_group}, Test Group: {test_group} - Overall Accuracy (Including Clean)")
                plt.figure(figsize=(10, 6))
                sns.lineplot(data=group_data, x='train', y='overall_accuracy', marker='o', label='Overall Accuracy')
                sns.lineplot(data=group_data, x='test', y='overall_accuracy', marker='o', label='Test Group Accuracy')
                
                # Include clean data in the plot
                clean_data = data[(data['train_group'] == 'clean') | (data['test_group'] == 'clean')]
                if not clean_data.empty:
                    clean_data = clean_data.sort_values(by=['train', 'test'])
                    sns.lineplot(data=clean_data, x='train', y='overall_accuracy', marker='o', label='Clean Accuracy')
                
                plt.title(f'Overall Accuracy for Train Group: {train_group} and Test Group: {test_group}')
                plt.xlabel('Train and Test Values')
                plt.ylabel('Overall Accuracy')
                plt.xticks(rotation=45)
                plt.legend()
                plt.tight_layout()
                st.pyplot(plt)

                # Plotting overall_fscore
                st.write(f"Train Group: {train_group}, Test Group: {test_group} - Overall Fscore (Including Clean)")
                plt.figure(figsize=(10, 6))
                sns.lineplot(data=group_data, x='train', y='overall_fscore', marker='o', label='Overall Fscore')
                sns.lineplot(data=group_data, x='test', y='overall_fscore', marker='o', label='Test Group Fscore')
                
                # Include clean data in the plot
                if not clean_data.empty:
                    sns.lineplot(data=clean_data, x='train', y='overall_fscore', marker='o', label='Clean Fscore')
                
                plt.title(f'Overall Fscore for Train Group: {train_group} and Test Group: {test_group}')
                plt.xlabel('Train and Test Values')
                plt.ylabel('Overall Fscore')
                plt.xticks(rotation=45)
                plt.legend()
                plt.tight_layout()
                st.pyplot(plt)

