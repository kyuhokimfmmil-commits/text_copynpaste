import streamlit as st
from pykospacing import Spacing

st.set_page_config(page_title="스마트 텍스트 리파이너", page_icon="📄", layout="centered")

@st.cache_resource
def load_model():
    return Spacing()

spacing = load_model()

st.title("텍스트 복사도구 (Smart Text Refiner)")
st.write("PDF에서 복사한 텍스트를 붙여넣으세요. AI가 문맥을 파악하여 끊어진 띄어쓰기를 완벽하게 복원합니다.")

input_text = st.text_area("PDF 원본 텍스트", height=200, placeholder="여기에 텍스트를 붙여넣으세요...")

if st.button("띄어쓰기 복원 및 변환", type="primary"):
    if input_text.strip():
        with st.spinner("AI가 문맥을 분석하며 띄어쓰기를 교정하고 있습니다..."):
            raw_text = input_text.replace('\n', ' ')
            raw_text = ' '.join(raw_text.split())
            
            result = spacing(raw_text)
        
        st.success("변환이 완료되었습니다. 아래 텍스트를 복사하여 사용하세요.")
        st.text_area("변환된 텍스트", value=result, height=200)
    else:
        st.warning("텍스트를 먼저 입력해주세요.")
