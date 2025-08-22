import streamlit as st
from datetime import datetime
import pandas as pd

# ===============================
# 🎉 앱 기본 설정
# ===============================
st.set_page_config(page_title="💆 스트레스 자가 진단", page_icon="🧘", layout="centered")

# ===============================
# 🌈 화려한 배경 + CSS
# ===============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
    background-attachment: fixed;
}
.glass {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}
.shiny {
    background: linear-gradient(90deg, #f83600, #f9d423);
    -webkit-background-clip: text;
    color: transparent;
    font-weight: 900;
    font-size:2rem;
    animation: glow 5s ease-in-out infinite;
}
@keyframes glow {
    0% { text-shadow: 0 0 10px #f83600; }
    50% { text-shadow: 0 0 20px #f9d423; }
    100% { text-shadow: 0 0 10px #f83600; }
}
hr {border: 0; height: 1px; background: linear-gradient(to right, transparent, #000, transparent);}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🧠 문항 정의 (20문항, 점수 1~5)
# ===============================
QUESTIONS = [
    "최근에 쉽게 짜증이 나거나 화가 나나요? 😡",
    "잠을 충분히 자지 못하거나 불면이 있나요? 🌙",
    "일이나 공부에 대한 집중력이 떨어지나요? 🧠",
    "자주 피곤하고 힘이 없다고 느끼나요? 😴",
    "불안감이나 긴장감이 자주 나타나나요? 😰",
    "사소한 일에도 신경이 많이 쓰이나요? 🧐",
    "식사 습관이 불규칙하거나 편식이 있나요? 🍔",
    "최근에 우울하거나 기분이 가라앉나요? 😞",
    "사람들과 관계에서 피곤함을 느끼나요? 😓",
    "계획대로 일이 잘 안 되어 스트레스를 느끼나요? 📅",
    "머리가 자주 무겁거나 아픈 느낌이 있나요? 🤕",
    "예민해지고 작은 일에도 울컥하나요? 😢",
    "운동이나 활동할 시간이 줄어들었나요? 🏃",
    "업무나 공부를 미루는 경우가 많나요? ⏳",
    "불안이나 걱정으로 밤에 잠을 설치나요? 🌃",
    "하루 중 마음이 편하지 않은 순간이 많나요? 😖",
    "무기력감이 느껴지거나 의욕이 줄었나요? 😔",
    "스트레스로 인해 집중력이 흐트러지나요? 🌀",
    "최근에 감정 기복이 심한가요? 🎢",
    "스트레스 때문에 건강이 영향을 받는다고 느끼나요? ❤️"
]

# ===============================
# 🧮 세션 상태 초기화
# ===============================
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = [0]*len(QUESTIONS)

# ===============================
# 🌟 홈 / 문제 화면
# ===============================
st.markdown("<h1 class='shiny'>💆 스트레스 자가 진단 🧘</h1>", unsafe_allow_html=True)

st.markdown("<div class='glass'>한 화면당 한 질문이 표시됩니다. 아래에서 점수를 선택하세요 (1: 전혀, 5: 매우 심함)</div>", unsafe_allow_html=True)

q_idx = st.session_state.current_q
st.markdown(f"<div class='glass'><b>질문 {q_idx+1} / {len(QUESTIONS)}</b><br>{QUESTIONS[q_idx]}</div>", unsafe_allow_html=True)

score = st.radio("점수를 선택하세요", options=[1,2,3,4,5], index=st.session_state.answers[q_idx]-1 if st.session_state.answers[q_idx]>0 else 0, horizontal=True, key=f"q{q_idx}")
st.session_state.answers[q_idx] = score

col1, col2 = st.columns(2)
with col1:
    if st.button("⬅ 이전", disabled=(q_idx==0)):
        st.session_state.current_q -= 1
with col2:
    if st.button("다음 ➡", disabled=(q_idx==len(QUESTIONS)-1)):
        st.session_state.current_q += 1

if q_idx == len(QUESTIONS)-1:
    if st.button("🎯 결과 보기"):
        total = sum(st.session_state.answers)
        st.session_state.total_score = total
        # 결과 계산
        if total <= 40:
            status = "⚡ 낮음"
            tip = "스트레스 수준이 낮아요. 규칙적인 생활과 가벼운 운동을 유지하세요! 🏃‍♂️"
        elif total <= 70:
            status = "🔥 보통"
            tip = "적절한 스트레스 관리가 필요해요. 명상, 운동, 휴식 시간을 늘리세요! 🧘‍♀️"
        else:
            status = "💥 높음"
            tip = "스트레스가 높은 상태입니다. 충분한 휴식과 전문가 상담을 권장합니다! 🩺"
        
        st.markdown(f"<h2 class='shiny'>결과: {status} ({total}/100)</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='glass'><b>관리 팁:</b> {tip}</div>", unsafe_allow_html=True)
        st.balloons()
