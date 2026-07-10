import streamlit as st
from openai import OpenAI

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

    .streaming-box {
        background-color: #f5f5f7;
        border: 1px solid #d2d2d7;
        border-radius: 12px;
        padding: 16px;
        font-size: 15px;
        line-height: 1.6;
        color: #1d1d1f;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
        min-height: 200px;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin-bottom: 1rem;
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

with st.sidebar:
    st.markdown("### 환경 설정")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.markdown("본인의 API 키를 입력해주세요. 팀원들과 링크 공유 시 각자의 환경에서 키를 입력하여 안전하게 사용할 수 있습니다.")

st.markdown('<h1 class="title-gradient">Text Refiner</h1>', unsafe_allow_html=True)

st.markdown("PDF에서 복사한 텍스트를 붙여넣으세요.<br>대형 언어 모델이 문맥을 파악하여 무작위로 끊어진 띄어쓰기만 완벽하게 복원합니다.", unsafe_allow_html=True)

st.text_area("입력", key="input_text", height=200, placeholder="텍스트를 이곳에 붙여넣어 주세요.", label_visibility="collapsed")

col1, col2, col3 = st.columns([5, 2, 2.5])

with col2:
    st.button("초기화", on_click=clear_text, use_container_width=True)

with col3:
    run_button = st.button("변환하기", type="primary", use_container_width=True)

if run_button:
    if not api_key:
        st.error("좌측 사이드바에서 OpenAI API Key를 먼저 입력해주세요.")
    elif not st.session_state.input_text.strip():
        st.warning("텍스트를 먼저 입력해주세요.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            prompt = '''당신은 텍스트의 띄어쓰기만 교정하는 기계입니다. 다음 규칙을 엄격히 지키십시오.
첫째 원본 텍스트에서 공백 기호를 제외한 모든 글자와 기호는 단 하나도 바뀌거나 삭제되거나 추가되어서는 안 됩니다. 공백을 제외한 모든 글자와 기호가 원본과 수학적으로 완벽하게 일치해야 합니다.
둘째 문장의 끝맺음을 습니다 혹은 입니다 등으로 절대 변형하지 마십시오. 예컨대 아 니다는 아니다로만 교정해야 하며 아닙니다로 바꾸는 것은 엄격히 금지됩니다.
셋째 오직 잘못된 띄어쓰기를 붙이거나 필요한 띄어쓰기를 추가하는 것만 허용됩니다.
넷째 문단 구분을 위한 이중 줄바꿈은 반드시 그대로 유지하십시오.
다섯째 부가 설명 없이 결과 텍스트만 출력하십시오.'''
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": st.session_state.input_text}
                ],
                temperature=0.0,
                stream=True
            )
            
            status_msg = st.empty()
            status_msg.info("AI가 문맥을 분석하며 띄어쓰기를 실시간으로 교정하고 있습니다...")
            
            res_box = st.empty()
            streamed_text = ""
            
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    streamed_text += chunk.choices[0].delta.content
                    res_box.markdown(f'<div class="streaming-box">{streamed_text}▌</div>', unsafe_allow_html=True)
            
            st.session_state.output_text = streamed_text
            st.rerun()
            
        except Exception as e:
            st.error(f"API 호출 중 오류가 발생했습니다. 키가 정확한지 확인해주세요.")

if st.session_state.output_text:
    st.success("변환이 완료되었습니다.")
    st.text_area("출력", value=st.session_state.output_text, height=200, label_visibility="collapsed")
