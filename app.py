import streamlit as st
import pandas as pd
import json
import re
import matplotlib.pyplot as plt

# Streamlit 제목
st.title('CSV 파일 업로드 및 시각화')

# 파일 업로드
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

def extract_info(file_name):
    freq_match = re.search(r'freq(\d+)', file_name)
    clean_match = re.search(r'clean', file_name, re.IGNORECASE)
    comp_match = re.search(r'comp', file_name, re.IGNORECASE)
    ratio_match = re.search(r'(\d\.\d+)', file_name)
    
    freq = freq_match.group(1) if freq_match else None
    clean = 'clean' if clean_match else None
    comp = 'comp' if comp_match else None
    ratio = ratio_match.group(1) if ratio_match else None
    
    return freq, clean, comp, ratio

if uploaded_file is not None:
    # CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)
    
    # file_name에서 정보 추출하여 새로운 열 추가
    df[['freq', 'clean', 'comp', 'ratio']] = df['file_name'].apply(
        lambda x: pd.Series(extract_info(x))
    )
    
    # content에서 overall_accuracy 추출
    df['overall_accuracy'] = df['content'].apply(
        lambda x: json.loads(x.replace("'", '"'))['overall_accuracy']
    )
    
    # 필요없는 열 제거
    df = df[['freq', 'clean', 'comp', 'ratio', 'overall_accuracy']]
    
    # 데이터프레임 출력
    st.subheader('DataFrame')
    st.write(df)
    
    # 기본 통계 정보 출력
    st.subheader('기본 통계 정보')
    st.write(df.describe())
    
    # overall_accuracy 히스토그램 시각화
    st.subheader('Overall Accuracy Distribution')
    fig, ax = plt.subplots()
    df['overall_accuracy'].hist(ax=ax, bins=20)
    ax.set_xlabel('Overall Accuracy')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    
    # CSV 파일을 다운로드할 수 있는 버튼 추가
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='cleaned_data.csv',
        mime='text/csv',
    )
