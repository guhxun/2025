import streamlit as st
import pandas as pd

# 🎨 앱 기본 세팅
st.set_page_config(page_title="🧠💖 스트레스 자가 진단 테스트 💖🧠",
                   page_icon="🧠",
                   layout="centered")

# 🧠 상태 초기화
if "answers" not in st.session_state:
    st.session_state.answers = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "page" not in st.session_state:
    st.session_state.page = "intro"

# 🎯 결과 계산 함수
def calculate_result(answers):
    score = sum(answers)
    if score <= 20:
        return "😌 스트레스 낮음", "💚 잘 관리하고 있어요! 꾸준히 자기 관리하세요 🌿", "#A8E6CF"
    elif score <= 40:
        return "🙂 스트레스 보통", "💛 조금 지친 상태예요. 충분한 휴식과 취미 생활이 필요해요 🎶", "#FFD3B6"
    elif score <= 60:
        return "😥 스트레스 높음", "🧡 많이 힘들어 하고 있네요. 자기 돌봄이 꼭 필요합니다 🧘", "#FFAAA5"
    else:
        return "😢 스트레스 심각", "❤️ 전문가 상담을 고려해보세요. 혼자 감당하지 마세요 💌", "#FF8B94"

# 질문 리스트 (20문항)
questions = [
    "1️⃣ 잠들기 어려웠다 😴",
    "2️⃣ 해야 할 일이 너무 많다 📚",
    "3️⃣ 사소한 일에도 짜증난다 😡",
    "4️⃣ 집중이 잘 안된다 🧠",
    "5️⃣ 피곤함이 지속된다 🥱",
    "6️⃣ 마음이 불안하거나 조급하다 😟",
    "7️⃣ 주변 사람들과 갈등이 잦다 👥",
    "8️⃣ 식습관이 불규칙하다 🍔",
    "9️⃣ 두통/근육통 등 신체적 증상이 있다 🤕",
    "🔟 우울감을 느낀다 😢",
    "11️⃣ 사회적 모임에 피로를 느낀다 🏃‍♂️",
    "12️⃣ 작은 일에도 걱정이 많다 🤯",
    "13️⃣ 의사결정이 불안하다 ❓",
    "14️⃣ 일을 끝까지 하지 못한다 ⏳",
    "15️⃣ 주변 환경에 쉽게 짜증난다 🌪️",
    "16️⃣ 몸이 긴장되고 뻐근하다 💪",
    "17️⃣ 하루 중 기분 변화가 크다 🎭",
    "18️⃣ 미래에 대한 불안감이 있다 🔮",
    "19️⃣ 식사 패턴이 불규칙하거나 폭식을 한다 🍫",
    "20️⃣ 쉬는 날에도 마음이 편하지 않다 🛌"
]

options = ["0️⃣ 전혀 아니다", "1️⃣ 가끔 그렇다", "2️⃣ 자주 그렇다", "3️⃣ 거의 항상 그렇다"]
score_mapping = {
    "0️⃣ 전혀 아니다": 0,
    "1️⃣ 가끔 그렇다": 1,
    "2️⃣ 자주 그렇다": 2,
    "3️⃣ 거의 항상 그렇다": 3
}

# 📌 인트로 페이지
if st.session_state.page == "intro":
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
                padding: 50px; border-radius: 25px; text-align:center;'>
        <h1 style='font-size:3em;'>🧠💖 스트레스 자가 진단 테스트 💖🧠</h1>
        <p style='font-size:1.5em;'>한 화면에 한 문제씩! 🎉✨</p>
        <p style='font-size:1.2em;'>최대한 많은 이모지와 화려한 스타일로 진행됩니다! 🌈💫</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("시작하기 🚀💥"):
        st.session_state.page = "quiz"
        st.rerun()

# 📌 질문 페이지
elif st.session_state.page == "quiz":
    q_idx = st.session_state.current_question
    st.markdown(f"""
    <div style='background-color:#FFF5E1; padding:30px; border-radius:20px; box-shadow: 5px 5px 15px #888888;'>
        <h2 style='font-size:2em; text-align:center;'>문제 {q_idx+1} / {len(questions)}</h2>
        <p style='font-size:1.5em; text-align:center;'>{questions[q_idx]}</p>
    </div>
    """, unsafe_allow_html=True)

    answer = st.radio("선택하세요 ✨", options, horizontal=True, key=f"q{q_idx}")

    # 진행률 표시
    st.progress((q_idx) / len(questions))

    if st.button("다음 ▶️💫"):
        st.session_state.answers.append(score_mapping[answer])
        st.session_state.current_question += 1
        if st.session_state.current_question >= len(questions):
            st.session_state.page = "result"
        st.rerun()

# 📌 결과 페이지
elif st.session_state.page == "result":
    total_score = sum(st.session_state.answers)
    max_score = len(questions)*3
    result_type, description, color = calculate_result(st.session_state.answers)

    st.markdown(f"""
    <div style='background: {color}; padding: 40px; border-radius: 30px; 
                text-align:center; box-shadow: 5px 5px 20px #888888;'>
        <h1 style='font-size:3em;'>{result_type} 🎉✨</h1>
        <p style='font-size:1.5em;'>총점: {total_score} / {max_score}</p>
        <p style='font-size:1.3em;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(total_score / max_score)

    # 항목별 막대그래프
    df = pd.DataFrame({
        "질문": [f"Q{i+1}" for i in range(len(st.session_state.answers))],
        "점수": st.session_state.answers
    })
    st.bar_chart(df.set_index("질문"))

    # 스트레스 완화 팁
    st.markdown("""
    <div style='background-color:#FFF0F5; padding:20px; border-radius:15px;'>
    <h2 style='text-align:center;'>🌿 스트레스 완화 팁 🌿</h2>
    <ul style='font-size:1.2em;'>
        <li>🧘‍♀️ 심호흡 & 명상</li>
        <li>🚶‍♂️ 가벼운 산책</li>
        <li>🎶 음악 감상</li>
        <li>📞 친구/가족과 대화</li>
        <li>💤 규칙적인 숙면</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

    if st.button("🔄 다시 하기 💥"):
        st.session_state.answers = []
        st.session_state.current_question = 0
        st.session_state.page = "intro"
        st.rerun()
