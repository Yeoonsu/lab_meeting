import streamlit as st
import pandas as pd
import re

# Streamlit 제목
st.title('Hello Professor!')
st.subheader('This is CSV viewer made by Yeonsu :star2:')

# 파일 업로드
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

def extract_info(file_name):
    # type1 추출
    if 'freq3' in file_name:
        type1 = 'freq3'
    elif 'clean' in file_name:
        type1 = 'clean'
    elif 'comp' in file_name:
        type1 = 'comp'
    else:
        type1 = None
    
    # type2 추출
    ratio_match = re.search(r'(\d\.\d)', file_name)
    type2 = ratio_match.group(1) if ratio_match else None
    
    return type1, type2

if uploaded_file is not None:
    # CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)
    
    # file_name에서 type1과 type2 추출하여 새로운 열 추가
    df[['type1', 'type2']] = df['file_name'].apply(
        lambda x: pd.Series(extract_info(x))
    )
    
    # content에서 accuracy 추출
    df['accuracy'] = df['content'].apply(
        lambda x: json.loads(x.replace("'", '"'))['overall_accuracy']
    )
    
    # 새로운 데이터프레임 생성
    new_df = df[['type1', 'type2', 'accuracy']]
    
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
