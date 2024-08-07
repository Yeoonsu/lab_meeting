import streamlit as st
import pandas as pd

# Streamlit 제목
st.title('Hello Professor!')
st.subheader('This is CSV viewer made by Yeonsu :star2:')

# 파일 업로드
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)
    
    # 데이터프레임 출력
    st.write(df)
