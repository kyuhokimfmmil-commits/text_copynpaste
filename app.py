import streamlit as st
from pykospacing import Spacing

st.set_page_config(page_title="Text Refiner", page_icon="📄", layout="centered")

st.markdown("""
<style>
    .title-gradient {
        background: -webkit-linear-gradient(45deg, #007aff, #34c759);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0px;
        padding-bottom: 10px;
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", sans-serif;
    }
    
    .stTextArea textarea {
        background-color: #ffffff !important;
        border: 2px solid #d2d2d7 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        color: #1d1d1f !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #007aff !important;
        box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return Spacing()

spacing = load_model()

st.markdown('<h1 class="title-gradient">Text Refiner</h1>', unsafe_allow_html=True)

st.markdown("PDF에서 복사한 텍스트를 붙여넣으세요.<br>형태소 분석 기반의 한국어 자연어 처리 기반 라이브러리를 통해 띄어쓰기를 복원하여 변환합니다.", unsafe_allow_html=True)

input_text = st.text_area("입력", height=200, placeholder="텍스트를 이곳에 붙여넣어 주세요.", label_visibility="collapsed")

if st.button("변환하기", type="primary"):
    if input_text.strip():
        with st.spinner("AI가 띄어쓰기를 교정하고 있습니다..."):
            raw_text = input_text.replace('\n', ' ')
            raw_text = ' '.join(raw_text.split())
            
            result = spacing(raw_text)
        
        st.success("변환이 완료되었습니다.")
        st.text_area("출력", value=result, height=200, label_visibility="collapsed")
    else:
        st.warning("텍스트를 먼저 입력해주세요.")
