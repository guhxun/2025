import streamlit as st
import pandas as pd

# 🎨 앱 기본 세팅
st.set_page_config(page_title="스트레스 자가 진단", page_icon="🧠", layout="centered")

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
        return "😌 스트레스 수준 낮음", "잘 관리하고 있어요! 꾸준히 자기 관리하세요 🌿", "#A8E6CF"
    elif score <= 40:
        return "🙂 보통 수준", "조금 지친 상태예요. 충분한 휴식과 취미 생활이 필요해요 🎶", "#FFD3B6"
    elif score <= 60:
        return "😥 스트레스 높음", "많이 힘들어 하고 있네요. 자기 돌봄이 꼭 필요합니다 🧘", "#FFAAA5"
    else:
        return "😢 심각한 스트레스", "전문가 상담을 고려해보세요. 혼자 감당하지 마세요 💌", "#FF8B94"

# 질문 리스트 (20문항)
questions = [
    "1️⃣ 최근 1주일 동안 잠들기 어려웠다 😴",
    "2️⃣ 해야 할 일이 너무 많다고 느낀다 📚",
    "3️⃣ 사소한 일에도 짜증이 난다 😡",
    "4️⃣ 집중이 잘 되지 않는다 🧠",
    "5️⃣ 피곤함이 지속된다 🥱",
    "6️⃣ 마음이 불안하거나 조급하다 😟",
    "7️⃣ 주변 사람들과 갈등이 잦다 👥",
    "8️⃣ 먹는 습관이 불규칙하다 🍔",
    "9️⃣ 두통이나 근육통 같은 신체적 증상이 있다 🤕",
    "🔟 기분이 가라앉고 우울감을 느낀다 😢",
    "11️⃣ 사회적 모임에 피로를 느낀다 🏃‍♂️",
    "12️⃣ 작은 일에도 걱정이 많다 🤯",
    "13️⃣ 의사결정을 할 때 불안하다 ❓",
    "14️⃣ 일을 끝까지 하지 못하는 경우가 많다 ⏳",
    "15️⃣ 주변 환경에 쉽게 짜증이 난다 🌪️",
    "16️⃣ 몸이 자주 긴장되고 뻐근하다 💪",
    "17️⃣ 하루 중 기분 변화가 크다 🎭",
    "18️⃣ 미래에 대해 불안감이 있다 🔮",
    "19️⃣ 식사 패턴이 불규칙하거나 폭식을 한다 🍫",
    "20️⃣ 쉬는 날에도 마음이 편하지 않다 🛌"
]

options = ["0: 전혀 아니다", "1: 가끔 그렇다", "2: 자주 그렇다", "3: 거의 항상 그렇다"]
score_mapping = {
    "0: 전혀 아니다": 0,
    "1: 가끔 그렇다": 1,
    "2: 자주 그렇다": 2,
    "3: 거의 항상 그렇다": 3
}

# 📌 인트로 페이지
if st.session_state.page == "intro":
    st.markdown("<h1 style='text-align: center;'>🧠 스트레스 자가 진단 테스트 🧠</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>당신의 스트레스 수준을 화려하게 확인해보세요 ✨</h4>", unsafe_allow_html=True)
    st.markdown("💡 한 화면에 한 문제씩 표시됩니다.")
    if st.button("시작하기 🚀"):
        st.session_state.page = "quiz"
        st.rerun()

# 📌 질문 페이지 (한 화면씩)
elif st.session_state.page == "quiz":
    q_idx = st.session_state.current_question
    st.markdown(f"### 문제 {q_idx + 1} / {len(questions)}")
    st.write(questions[q_idx])
    
    answer = st.radio("선택하세요", options, horizontal=True, key=f"q{q_idx}")

    # 진행률 표시
    st.progress((q_idx) / len(questions))

    if st.button("다음 ▶️"):
        st.session_state.answers.append(score_mapping[answer])
        st.session_state.current_question += 1

        if st.session_state.current_question >= len(questions):
            st.session_state.page = "result"
        st.rerun()

# 📌 결과 페이지
elif st.session_state.page == "result":
    total_score = sum(st.session_state.answers)
    max_score = len(questions) * 3
    result_type, description, color = calculate_result(st.session_state.answers)

    # 🎨 카드 스타일
    st.markdown(f"""
        <div style="background-color: {color}; padding: 20px; border-radius: 15px; text-align:center;">
            <h2 style="font-size: 2em;">{result_type}</h2>
            <p style="font-size: 1.2em;">총점: {total_score} / {max_score}</p>
            <p style="font-size: 1em;">{description}</p>
        </div>
    """, unsafe_allow_html=True)

    # 진행 게이지
    st.progress(total_score / max_score)

    # 항목별 점수 시각화
    df = pd.DataFrame({
        "질문 번호": [f"Q{i+1}" for i in range(len(st.session_state.answers))],
        "점수": st.session_state.answers
    })
    st.bar_chart(df.set_index("질문 번호"))

    # 스트레스 완화 팁
    st.markdown("### 🌿 스트레스 완화 팁")
    st.markdown("""
    - 🧘 **호흡 명상**: 눈을 감고 깊게 호흡하기  
    - 🚶 **가벼운 산책**: 10~20분 정도 걷기  
    - 🎶 **음악 감상**: 좋아하는 음악으로 기분 전환  
    - 📞 **대화하기**: 믿을 수 있는 사람과 이야기 나누기  
    - 💤 **숙면 습관**: 일정한 수면 패턴 유지  
    """)

    st.balloons()

    if st.button("🔄 다시 하기"):
        st.session_state.answers = []
        st.session_state.current_question = 0
        st.session_state.page = "intro"
        st.rerun()
