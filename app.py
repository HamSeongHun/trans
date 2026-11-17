import streamlit as st

from translator import LANGUAGES, MAX_CHARS, TranslationError, translate

st.set_page_config(page_title="AI 번역기", page_icon="🌐", layout="centered")

FLAGS = {"영어": "🇺🇸", "일본어": "🇯🇵", "베트남어": "🇻🇳"}

# 라이트/다크 모드 모두에서 동작하도록 Streamlit 테마 변수만 사용한다.
st.markdown(
    """
<style>
.block-container { max-width: 720px; padding-top: 2.5rem; padding-bottom: 3rem; }

.app-title { text-align: center; margin: 0 0 .25rem; font-size: 2rem; font-weight: 700; }
.app-sub { text-align: center; opacity: .7; margin-bottom: 1.5rem; }

/* 카드 */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px;
    box-shadow: 0 1px 6px rgba(0, 0, 0, .06);
}

/* 텍스트 입력창 */
textarea { font-size: 1rem !important; line-height: 1.6 !important; }

/* 언어 버튼 */
div[data-testid="stButton"] button {
    border-radius: 10px;
    padding: .6rem .5rem;
    font-weight: 600;
    transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(79, 107, 237, .25);
}

/* 모바일에서도 버튼 3개를 한 줄로 유지 */
@media (max-width: 640px) {
    div[data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: .4rem !important; }
    div[data-testid="stHorizontalBlock"] > div { min-width: 0 !important; }
    div[data-testid="stButton"] button { padding: .5rem .2rem; font-size: .9rem; }
    .app-title { font-size: 1.6rem; }
}

/* 결과 텍스트 */
div[data-testid="stCode"] pre, div[data-testid="stCode"] code {
    font-family: inherit !important;
    font-size: 1.05rem !important;
    line-height: 1.7 !important;
    white-space: pre-wrap !important;
}

.footnote { text-align: center; font-size: .8rem; opacity: .6; margin-top: 2rem; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">🌐 AI 번역기</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-sub">텍스트를 입력하고 원하는 언어 버튼을 누르세요</div>',
    unsafe_allow_html=True,
)

# 입력 카드
with st.container(border=True):
    text = st.text_area(
        "번역할 텍스트",
        placeholder="번역할 텍스트를 입력하세요...",
        height=150,
        key="source_text",
        label_visibility="collapsed",
    )
    over = len(text) > MAX_CHARS
    if over:
        st.caption(f":red[{len(text):,} / {MAX_CHARS:,}자 — 글자 수를 초과했습니다]")
    else:
        st.caption(f"{len(text):,} / {MAX_CHARS:,}자")

# 버튼
cols = st.columns(len(LANGUAGES))
clicked = None
for col, lang in zip(cols, LANGUAGES):
    if col.button(f"{FLAGS[lang]} {lang}", use_container_width=True, key=f"btn_{lang}"):
        clicked = lang

# 번역 실행
if clicked:
    if not text.strip():
        st.warning("번역할 내용을 입력해주세요.")
    elif over:
        st.warning(f"입력은 {MAX_CHARS:,}자 이하여야 합니다. 글자 수를 줄여주세요.")
    else:
        try:
            with st.spinner(f"{clicked}로 번역 중..."):
                result = translate(text, clicked)
            st.session_state["result"] = (clicked, result)
        except TranslationError as e:
            st.session_state.pop("result", None)
            st.error(str(e))

# 결과 카드
saved = st.session_state.get("result")
if saved:
    lang, result = saved
    with st.container(border=True):
        st.caption(f"{FLAGS[lang]} {lang} 번역 결과")
        st.code(result, language=None, wrap_lines=True)

st.markdown(
    '<div class="footnote">입력한 텍스트는 번역을 위해 외부 AI API로 전달되며 서버에 저장되지 않습니다.</div>',
    unsafe_allow_html=True,
)
