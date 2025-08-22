import streamlit as st
from datetime import datetime
import pandas as pd

# ===============================
# 🎉 앱 기본 설정
# ===============================
st.set_page_config(page_title="🌟💆 스트레스 자가 진단 월드 🧘‍♀️✨", page_icon="🧘‍♂️", layout="wide")

# ===============================
# 🌈 화려한 배경 + CSS
# ===============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 50%, #fad0c4 100%);
    background-attachment: fixed;
}
.glass {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(14px);
    border-radius: 28px;
    padding: 30px 40px;
    margin: 25px 0;
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    border: 1px solid rgba(255,255,255,0.6);
}
.shiny {
    background: linear-gradient(90deg, #f093fb, #f5576c, #f093fb);
    -webkit-background-clip: text;
    color: transparent;
    font-weight: 900;
    font-size:3.5rem;
    animation: glow 5s ease-in-out infinite;
    text-align:center;
}
@keyframes glow {
    0% { text-shadow: 0 0 15px #f5576c, 0 0 30px #f093fb; }
    50% { text-shadow: 0 0 25px #f093fb, 0 0 45px #f5576c; }
    100% { text-shadow: 0 0 15px #f5576c, 0 0 30px #f093fb; }
}
hr {border:0; height:1px; background:linear-gradient(to right, transparent, #000, transparent);}
.button-large {
    font-size: 1.5rem !important;
    padding: 20px 60px !important;
    background: linear-gradient(90deg, #f6d365 0%, #fda085 100%);
    color: white;
    font-weight: bold;
    border-radius: 20px;
}
.button-large:hover {
    filter: brightness(1.2);
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🧠 문항 정의 (20문항, 점수 1~5)
# ===============================
QUESTIONS = [
    "최근에 쉽게 짜증이 나거나 화가 나나요? 😤🔥",
    "잠을 충분히 자지 못하거나 불면이 있나요? 🌙💤",
    "일이나 공부에 대한 집중력이 떨어지나요? 🧠💥",
    "자주 피곤하고 힘이 없다고 느끼나요? 😴💦",
    "불안감이나 긴장감이 자주 나타나나요? 😰⚡",
    "사소한 일에도 신경이 많이 쓰이나요? 🧐🌀",
    "식사 습관이 불규칙하거나 편식이 있나요? 🍕🍔",
    "최근에 우울하거나 기분이 가라앉나요? 😞🌧️",
    "사람들과 관계에서 피곤함을 느끼나요? 😓💔",
    "계획대로 일이 잘 안 되어 스트레스를 느끼나요? 📅⏳",
    "머리가 자주 무겁거나 아픈 느낌이 있나요? 🤕💫",
    "예민해지고 작은 일에도 울컥하나요? 😢💥",
    "운동이나 활동할 시간이 줄어들었나요? 🏃‍♂️⏱️",
    "업무나 공부를 미루는 경우가 많나요? ⏳📝",
    "불안이나 걱정으로 밤에 잠을 설치나요? 🌃😓",
    "하루 중 마음이 편하지 않은 순간이 많나요? 😖🌪️",
    "무기력감이 느껴지거나 의욕이 줄었나요? 😔🛌",
    "스트레스로 인해 집중력이 흐트러지나요? 🌀📉",
    "최근에 감정 기복이 심한가요? 🎢😵",
    "스트레스 때문에 건강이 영향을 받는다고 느끼나요? ❤️‍🩹🏥"
]

# ===============================
# 응답 옵션 정의
# ===============================
OPTIONS = [
    "💚 전혀 그렇지 않아요",   # 1점
    "💛 그렇지 않아요",         # 2점
    "💙 보통이에요",           # 3점
    "🧡 조금 그래요",           # 4점
    "❤️ 많이 그래요"            # 5점
]

# ===============================
# 🧮 세션 상태 초기화
# ===============================
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'answers' not in st.session_state:
    st.session_state.answers = [0]*len(QUESTIONS)

# ===============================
# 🌟 홈 화면
# ===============================
if st.session_state.current_q is None:
    st.markdown("<h1 class='shiny'>🌟💆 스트레스 자가 진단 💖🧘‍♀️</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class='glass'>
    <p>이 자가 진단 앱은 20개의 질문을 통해 당신의 스트레스 수준을 점수화합니다.</p>
    <p>각 문항은 아래 응답 옵션에 따라 점수가 부여되며, 총점 100점 기준으로 스트레스 지수를 판단합니다.</p>
    <ul>
    <li>💚 전혀 그렇지 않아요 (1점)</li>
    <li>💛 그렇지 않아요 (2점)</li>
    <li>💙 보통이에요 (3점)</li>
    <li>🧡 조금 그래요 (4점)</li>
    <li>❤️ 많이 그래요 (5점)</li>
    </ul>
    <p>총점에 따라 스트레스 수준은 낮음 ⚡, 보통 🔥, 높음 💥으로 구분됩니다.</p>
    <p>아래 버튼을 눌러 테스트를 시작하세요!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 테스트 시작", key="start_test"):
        st.session_state.current_q = 0

# ===============================
# 🌟 문제 화면
# ===============================
else:
    q_idx = st.session_state.current_q
    st.markdown(f"<div class='glass'><b>질문 {q_idx+1} / {len(QUESTIONS)}</b><br>{QUESTIONS[q_idx]}</div>", unsafe_allow_html=True)

    answer = st.radio("응답을 선택하세요", options=OPTIONS, index=st.session_state.answers[q_idx]-1 if st.session_state.answers[q_idx]>0 else 2, horizontal=True, key=f"q{q_idx}")
    st.session_state.answers[q_idx] = OPTIONS.index(answer) + 1

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ 이전", disabled=(q_idx==0)):
            st.session_state.current_q = max(0, st.session_state.current_q - 1)
    with col2:
        if st.button("다음 ➡", disabled=(q_idx==len(QUESTIONS)-1)):
            st.session_state.current_q = min(len(QUESTIONS)-1, st.session_state.current_q + 1)

    if q_idx == len(QUESTIONS)-1:
        if st.button("🎯 결과 보기"):
            total = sum(st.session_state.answers)
            st.session_state.total_score = total
            if total <= 40:
                status = "⚡ 낮음"
                tip = "스트레스 수준이 낮아요. 규칙적인 생활과 가벼운 운동을 유지하세요! 🏃‍♂️🌿"
            elif total <= 70:
                status = "🔥 보통"
                tip = "적절한 스트레스 관리가 필요해요. 명상, 운동, 휴식 시간을 늘리세요! 🧘‍♀️🍵"
            else:
                status = "💥 높음"
                tip = "스트레스가 높은 상태입니다. 충분한 휴식과 전문가 상담을 권장합니다! 🩺🛌"
            st.markdown(f"<h2 class='shiny'>결과: {status} ({total}/100)</h2>", unsafe_allow_html=True)
            st.markdown(f"<div class='glass'><b>관리 팁:</b> {tip}</div>", unsafe_allow_html=True)
            st.balloons()
