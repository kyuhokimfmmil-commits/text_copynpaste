import streamlit as st
import re
from kiwipiepy import Kiwi

st.set_page_config(page_title="Text Refiner", page_icon="📄", layout="centered")

if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""

def clear_text():
    st.session_state.input_text = ""
    st.session_state.output_text = ""

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
        background-color: #f5f5f7 !important;
        border: 1px solid #d2d2d7 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        color: #1d1d1f !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02) !important;
    }
    
    .stTextArea textarea:focus {
        background-color: #ffffff !important;
        border-color: #007aff !important;
        box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1) !important;
    }

    div[data-testid="stButton"] > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
        height: 46px !important;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(45deg, #007aff, #34c759) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(0, 122, 255, 0.2) !important;
    }
    
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(0, 122, 255, 0.3) !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #e5e5ea !important;
        color: #1d1d1f !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: #d1d1d6 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return Kiwi()

kiwi = load_model()

st.markdown('<h1 class="title-gradient">Text Refiner</h1>', unsafe_allow_html=True)

st.markdown("PDF에서 복사한 텍스트를 붙여넣으세요.<br>형태소 분석 기반의 한국어 자연어 처리 기반 라이브러리를 통해 띄어쓰기를 복원하여 변환합니다.", unsafe_allow_html=True)

st.text_area("입력", key="input_text", height=200, placeholder="텍스트를 이곳에 붙여넣어 주세요.", label_visibility="collapsed")

col1, col2, col3 = st.columns([5, 2, 2.5])

with col2:
    st.button("초기화", on_click=clear_text, use_container_width=True)

with col3:
    if st.button("변환하기", type="primary", use_container_width=True):
        if st.session_state.input_text.strip():
            with st.spinner("AI가 띄어쓰기를 교정하고 있습니다..."):
                paragraphs = st.session_state.input_text.split('\n\n')
                result_paragraphs = []
                
                for p in paragraphs:
                    if not p.strip():
                        continue
                    
                    raw_text = p.replace('\n', ' ')
                    raw_text = re.sub(r'\s+', ' ', raw_text)
                    result_paragraphs.append(kiwi.space(raw_text))
                    
                st.session_state.output_text = '\n\n'.join(result_paragraphs)
        else:
            st.warning("텍스트를 먼저 입력해주세요.")

if st.session_state.output_text:
    st.success("변환이 완료되었습니다.")
    st.text_area("출력", value=st.session_state.output_text, height=200, label_visibility="collapsed")
