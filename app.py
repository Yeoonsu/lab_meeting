import streamlit as st
import pandas as pd
import re

# Streamlit 제목
st.title('Hello Professor!')
st.subheader('This is CSV viewer made by Yeonsu :star2:')

# 파일 업로드
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)

    # Extracting 'type1' and 'type2'
    df['type1'] = df['file_name'].str.split('-').str[4] + '-' + df['file_name'].str.split('-').str[5]
    df['type2'] = df['file_name'].str.split('-').str[9] + '-' + df['file_name'].str.split('-').str[10]

    # 새로운 데이터프레임 생성
    new_df = df[['type1', 'type2', 'content']]
    
    # Sorting the DataFrame by type1 and type2
    new_df = new_df.sort_values(by=['type1', 'type2'])
    
    # 데이터프레임 출력
    st.subheader('Transformed DataFrame')
    st.write(new_df)
    
    # CSV 파일을 다운로드할 수 있는 버튼 추가
    csv = new_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download transformed data as CSV",
        data=csv,
        file_name='transformed_data.csv',
        mime='text/csv',
    )
