import streamlit as st
import pandas as pd
from datetime import datetime

# ===============================
# 🎉 Streamlit App Config
# ===============================
st.set_page_config(
    page_title="🎓✨ MBTI 진로교육 월드",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===============================
# 🌈 Custom CSS (화려함 MAX)
# ===============================
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #FFE3F1 0%, #E3F0FF 50%, #E9FFE3 100%);
            background-attachment: fixed;
        }
        /* 카드 느낌 */
        .glass {
            background: rgba(255,255,255,0.65);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 18px 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            border: 1px solid rgba(255,255,255,0.6);
        }
        /* 헤더 타이틀 반짝임 */
        .shiny {
            background: linear-gradient(90deg, #ff4d4d, #ff9f1c, #2ec4b6, #6a4c93);
            -webkit-background-clip: text;  background-clip: text;
            color: transparent;
            animation: glow 6s ease-in-out infinite;
            font-weight: 900;
        }
        @keyframes glow {
            0% { text-shadow: 0 0 10px rgba(255, 77, 77, .5); }
            50% { text-shadow: 0 0 18px rgba(46, 196, 182, .6); }
            100% { text-shadow: 0 0 10px rgba(106, 76, 147, .5); }
        }
        /* 배지 */
        .badge { display:inline-block; padding:6px 12px; border-radius:20px; font-size:0.85rem; font-weight:700; }
        .badge-pink { background:#ffd6e7; color:#b8005c; }
        .badge-blue { background:#d6ebff; color:#0052cc; }
        .badge-green{ background:#dcffe4; color:#007f3b; }
        .emoji-splash { font-size: 1.4rem; }
        .hr-soft { border:0; height:1px; background:linear-gradient(90deg, transparent, rgba(0,0,0,0.15), transparent); margin:16px 0 6px; }
        .subtle { color:#444; }
        /* 사이드바 제목 꾸미기 */
        section[data-testid="stSidebar"] .css-1d391kg, section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
            color:#1f2937 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===============================
# 🧠 데이터베이스 (MBTI 16유형)
# ===============================
MBTI_DB = {
    "INTJ": {"특징":"전략가 · 독립적 · 장기계획", "추천진로":["데이터과학자","전략기획","시스템엔지니어","UX리서처"], "전공":["컴퓨터공학","산업공학","경영학","수학"], "학습팁":"목표를 세부 단계로 분해하고, 딥워크 시간 확보 ⏳"},
    "INTP": {"특징":"분석적 · 호기심 · 아이디어 풍부", "추천진로":["연구원","개발자","교수","데이터분석가"], "전공":["물리","수학","컴공","인지과학"], "학습팁":"문제를 모델링하고 가설-검증 루프 반복 🔁"},
    "ENTJ": {"특징":"리더십 · 체계화 · 목표지향", "추천진로":["프로덕트매니저","컨설턴트","창업","전략가"], "전공":["경영","경제","산업공학","정치"], "학습팁":"OKR로 우선순위 관리, 발표로 이해 공고화 🎤"},
    "ENTP": {"특징":"토론가 · 혁신 · 유연", "추천진로":["창업가","마케팅전략","VC/스타트업","UX기획"], "전공":["경영","디자인","미디어","컴공"], "학습팁":"브레인스토밍 → 프로토타입 → 피드백 사이클 ⚙️"},
    "INFJ": {"특징":"통찰 · 가치지향 · 조화", "추천진로":["상담사","교육기획","브랜드전략","콘텐츠기획"], "전공":["심리","교육","철학","문헌정보"], "학습팁":"비전 보드로 장기 의미와 오늘 할 일 연결 🎯"},
    "INFP": {"특징":"이상가 · 공감 · 창의표현", "추천진로":["작가","디자이너","영상기획","사회복지"], "전공":["문예창작","디자인","미디어","사회복지"], "학습팁":"저널링으로 가치와 프로젝트 정렬 ✍️"},
    "ENFJ": {"특징":"코치 · 협업 · 영감부여", "추천진로":["교육자","HRD","커뮤니티매니저","PR"], "전공":["교육","경영","커뮤니케이션","사회"], "학습팁":"스터디 리드, 피어러닝 설계 🤝"},
    "ENFP": {"특징":"활기 · 연결 · 아이디어", "추천진로":["크리에이터","기획자","브랜드마케터","에반젤리스트"], "전공":["광고홍보","미디어","디자인","경영"], "학습팁":"다양한 시도를 캡처하는 아이디어 인박스 📮"},
    "ISTJ": {"특징":"신뢰성 · 꼼꼼함 · 규범", "추천진로":["회계","공무","품질관리","데이터관리"], "전공":["회계","행정","통계","법"], "학습팁":"체크리스트 기반 습관화 ✅"},
    "ISFJ": {"특징":"헌신 · 안정 · 세심", "추천진로":["간호","교직","CS전문가","운영"], "전공":["간호","교육","경영지원","행정"], "학습팁":"암기+사례 연결로 실전감각 상승 🧩"},
    "ESTJ": {"특징":"실행력 · 조직화 · 현실주의", "추천진로":["프로젝트매니저","운영관리","세무","영업리더"], "전공":["경영","물류","회계","법"], "학습팁":"간트차트/캘린더로 일정 엄수 📅"},
    "ESFJ": {"특징":"사교 · 배려 · 책임", "추천진로":["교사","간호사","사회복지","인사"], "전공":["교육","보건","사회복지","HR"], "학습팁":"팀 기반 학습과 역할 분담 최적화 👥"},
    "ISTP": {"특징":"문제해결 · 실험 · 냉철", "추천진로":["엔지니어","보안","파일럿","프로토타입"], "전공":["기계","전기","컴공","항공"], "학습팁":"손으로 만드는 Tinkering, 로그 기록 🔧"},
    "ISFP": {"특징":"감성실용 · 미적감각 · 유연", "추천진로":["디자이너","포토/영상","UX","핸드크래프트"], "전공":["시각디자인","공예","미디어","패션"], "학습팁":"무드보드·레퍼런스 라이브러리 🎨"},
    "ESTP": {"특징":"액션 · 현실감각 · 설득", "추천진로":["세일즈","이벤트","스포츠매니지먼트","트레이더"], "전공":["마케팅","경영","체육","경제"], "학습팁":"케이스 스터디와 현장학습 📊"},
    "ESFP": {"특징":"에너지 · 어울림 · 즉흥", "추천진로":["MC/크리에이터","호텔/관광","공연예술","홍보"], "전공":["관광","공연","미디어","커뮤니케이션"], "학습팁":"짧은 스프린트 학습 + 현장 발표 🎉"},
}

# ===============================
# 🔧 유틸 함수
# ===============================
DICHOTOMIES = [
    ("E", "I"),
    ("S", "N"),
    ("T", "F"),
    ("J", "P"),
]

QUIZ = [
    ("사람 많은 곳에서 에너지 충전 ✨", "조용한 혼자 시간에서 재충전 🌙", "E", "I"),
    ("현재의 사실·디테일에 강함 🔍", "미래 가능성·직관에 끌림 🌈", "S", "N"),
    ("논리·원칙으로 판단 ⚖️", "사람·가치로 판단 💞", "T", "F"),
    ("계획표 좋아함 📅", "즉흥도 환영 🎲", "J", "P"),
    ("잡담보다 활동! 🏃", "활동보다 깊은 대화 🧠", "E", "I"),
    ("경험·사례 중요 🧭", "아이디어·이론 중요 🧪", "S", "N"),
    ("직설·팩트 선호 🧊", "배려·분위기 중시 🌤", "T", "F"),
    ("마감 전 여유 있게 ⏰", "데드라인 스릴 ✨", "J", "P"),
]

@st.cache_data
def empty_results():
    return {"E":0, "I":0, "S":0, "N":0, "T":0, "F":0, "J":0, "P":0}

# ===============================
# 🧭 사이드바 (네비게이션)
# ===============================
with st.sidebar:
    st.markdown("## 🧭 네비게이션")
    page = st.radio(
        "이동할 페이지를 선택하세요",
        ["🏠 홈", "📝 MBTI 퀴즈", "🔎 결과 & 추천", "🌍 유형 탐색", "📚 리소스"],
        index=0,
    )
    st.markdown("<hr class='hr-soft' />", unsafe_allow_html=True)
    st.markdown(
        f"<span class='badge badge-blue'>오늘: {datetime.now().strftime('%Y-%m-%d')}</span>",
        unsafe_allow_html=True,
    )
    st.markdown("<span class='subtle'>Tips: 결과 페이지에서 🎊 이벤트가 있어요!</span>", unsafe_allow_html=True)

# ===============================
# 🏠 홈
# ===============================
if page == "🏠 홈":
    st.markdown("""
    <h1 class='shiny'>🎓 MBTI 기반 진로교육 월드 🌟</h1>
    <div class='emoji-splash'>🧠💼✨🎨🛰️📚🧭🚀💡🎯</div>
    <p class='subtle'>당신의 성격유형에 꼭 맞는 전공·직업·학습전략을 찾아보세요!</p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2,1,1])
    with c1:
        st.markdown("""
        <div class='glass'>
            <h3>🗺 무엇을 할 수 있나요?</h3>
            <ul>
                <li>📝 1분 퀴즈로 MBTI 경향 파악</li>
                <li>🎯 유형별 전공·직업 추천</li>
                <li>📈 강점 기반 학습전략 제안</li>
                <li>🔍 16유형 비교·탐색</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='glass'>
            <h3>✨ 빠른 시작</h3>
            <p>좌측 <b>📝 MBTI 퀴즈</b>로 이동하거나, 직접 유형을 선택해 보세요!</p>
            <p><span class='badge badge-pink'>Tip</span> 결과 페이지에서 그래프와 카드가 자동 생성돼요.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='glass'>
            <h3>🧩 16유형 요약</h3>
            <p>분석가(👓)·외교관(🕊)·관리자(🗂)·탐험가(🧭) 4그룹으로 살펴보세요.</p>
        </div>
        """, unsafe_allow_html=True)

# ===============================
# 📝 MBTI 퀴즈
# ===============================
if page == "📝 MBTI 퀴즈":
    st.markdown("<h2>📝 초간단 MBTI 경향 퀴즈</h2>", unsafe_allow_html=True)
    st.markdown("<div class='glass'>선호하는 문장을 선택하세요. (총 %d 문항)</div>" % len(QUIZ), unsafe_allow_html=True)

    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = empty_results()
        st.session_state.answers = [None]*len(QUIZ)

    for i, (a_text, b_text, a_code, b_code) in enumerate(QUIZ, start=1):
        st.markdown(f"<hr class='hr-soft' />", unsafe_allow_html=True)
        st.markdown(f"**Q{i}.** {a_text} **vs** {b_text}")
        choice = st.radio(
            label=f"q{i}",
            options=[a_text, b_text],
            horizontal=True,
            index=0 if st.session_state.answers[i-1] == a_text else (1 if st.session_state.answers[i-1] == b_text else 0),
            key=f"radio_{i}",
        )
        st.session_state.answers[i-1] = choice
        if choice == a_text:
            st.session_state.quiz_scores[a_code] += 1
        else:
            st.session_state.quiz_scores[b_code] += 1

    st.markdown("<hr class='hr-soft' />", unsafe_allow_html=True)
    if st.button("🎯 결과 보러가기 (자동 계산)"):
        st.session_state["go_result"] = True
        st.switch_page("streamlit_app.py") if False else None  # placeholder for multipage
        st.success("좌측 '🔎 결과 & 추천' 페이지로 이동해 주세요! 🚀")

# ===============================
# 🔎 결과 & 추천
# ===============================
if page == "🔎 결과 & 추천":
    st.markdown("<h2>🔎 결과 & 맞춤 추천</h2>", unsafe_allow_html=True)

    # 수동 입력 + 드롭다운
    col1, col2 = st.columns([1,2])
    with col1:
        manual = st.text_input("📥 MBTI 직접 입력 (예: INFP)").upper().strip()
        selected = st.selectbox("또는 목록에서 선택", sorted(list(MBTI_DB.keys())))
        final_type = manual if manual in MBTI_DB else selected
        st.markdown(f"<span class='badge badge-green'>선택된 유형: {final_type}</span>", unsafe_allow_html=True)
    with col2:
        # 퀴즈 스코어 시각화
        scores = st.session_state.get("quiz_scores", empty_results())
        df = (
            pd.DataFrame([
                {"축":"E vs I", "E": scores["E"], "I": scores["I"]},
                {"축":"S vs N", "S": scores["S"], "N": scores["N"]},
                {"축":"T vs F", "T": scores["T"], "F": scores["F"]},
                {"축":"J vs P", "J": scores["J"], "P": scores["P"]},
            ]).set_index("축")
        )
        st.markdown("<div class='glass'>📊 퀴즈 경향 그래프</div>", unsafe_allow_html=True)
        st.bar_chart(df)

    # 추천 카드
    data = MBTI_DB[final_type]
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class='glass'>
            <h3>🧠 특징</h3>
            <p>{data['특징']}</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='glass'>
            <h3>🎯 추천 진로</h3>
            <p>{' · '.join(data['추천진로'])}</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='glass'>
            <h3>🎓 추천 전공</h3>
            <p>{' · '.join(data['전공'])}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='glass'>
        <h3>📚 학습 전략</h3>
        <p>{data['학습팁']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

# ===============================
# 🌍 유형 탐색
# ===============================
if page == "🌍 유형 탐색":
    st.markdown("<h2>🌍 16유형 한눈에 보기</h2>", unsafe_allow_html=True)
    group_tabs = st.tabs(["👓 분석가 (NT)", "🕊 외교관 (NF)", "🗂 관리자 (SJ)", "🧭 탐험가 (SP)"])

    groups = {
        "👓 분석가 (NT)": ["INTJ","INTP","ENTJ","ENTP"],
        "🕊 외교관 (NF)": ["INFJ","INFP","ENFJ","ENFP"],
        "🗂 관리자 (SJ)": ["ISTJ","ISFJ","ESTJ","ESFJ"],
        "🧭 탐험가 (SP)": ["ISTP","ISFP","ESTP","ESFP"],
    }

    for tab, key in zip(group_tabs, groups.keys()):
        with tab:
            cols = st.columns(4)
            for i, t in enumerate(groups[key]):
                with cols[i % 4]:
                    card = MBTI_DB[t]
                    st.markdown(f"""
                    <div class='glass'>
                        <h4>{t} ✨</h4>
                        <div class='subtle'>🧠 {card['특징']}</div>
                        <hr class='hr-soft'/>
                        <div>🎯 {' • '.join(card['추천진로'][:3])}</div>
                        <div>🎓 {' • '.join(card['전공'][:3])}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ===============================
# 📚 리소스
# ===============================
if page == "📚 리소스":
    st.markdown("<h2>📚 진로 설계 체크리스트</h2>", unsafe_allow_html=True)
    with st.expander("🧭 나만의 커리어 나침반 만들기"):
        st.markdown("""
        - 🧩 강점 3가지 적기 → MBTI 설명과 매칭
        - 🎯 1년/3년 목표 정의 (성과지표 포함)
        - 🗺 전공 과목/활동 로드맵 만들기
        - 🤝 멘토·커뮤니티 연결 계획
        - 🔁 분기별 리셋 데이 운영
        """)
    with st.expander("🎨 포트폴리오 아이디어"):
        st.markdown("""
        - 📘 타입별 케이스 스터디 정리
        - 📹 3분 셀프 피치 영상
        - 🗂 과제→프로젝트화(깃허브/노션)
        - 🧪 해커톤·공모전 참가 기록
        """)

    st.info("✨ 사이드바에서 다른 페이지로 이동하며 계속 탐색해 보세요!")

# ===============================
# 🏁 Footer
# ===============================
st.markdown("""
<div class='subtle' style='text-align:center; margin-top:32px;'>
  Made with ❤️ & Streamlit · MBTI는 자기이해 도구일 뿐, 절대적 기준이 아니에요 🧡
</div>
""", unsafe_allow_html=True)

