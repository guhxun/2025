import streamlit as st
import pandas as pd

# ===================== 설정 =====================
st.set_page_config(
    page_title="💖🧠 스트레스 진단 게임💥🧠",
    page_icon="🧠",
    layout="wide"
)

# 초기 상태
if "answers" not in st.session_state: st.session_state.answers=[]
if "current_question" not in st.session_state: st.session_state.current_question=0
if "page" not in st.session_state: st.session_state.page="intro"

# ===================== 결과 계산 =====================
def calculate_result(answers):
    score = sum(answers)
    if score <= 20: return "😌 낮음", "💚 잘 관리 중! 🌿", "#A8E6CF"
    elif score <= 40: return "🙂 보통", "💛 조금 피곤해요 🎶", "#FFD3B6"
    elif score <= 60: return "😥 높음", "🧡 많이 힘들어요 🧘", "#FFAAA5"
    else: return "😢 심각", "❤️ 상담 고려 필요 💌", "#FF8B94"

# ===================== 질문 데이터 =====================
questions=[
"1️⃣ 잠들기 어려웠다 😴","2️⃣ 해야 할 일이 너무 많다 📚","3️⃣ 사소한 일에도 짜증난다 😡",
"4️⃣ 집중이 잘 안된다 🧠","5️⃣ 피곤함이 지속된다 🥱","6️⃣ 마음이 불안하거나 조급하다 😟",
"7️⃣ 주변 사람들과 갈등이 잦다 👥","8️⃣ 식습관이 불규칙하다 🍔","9️⃣ 두통/근육통 등 신체적 증상이 있다 🤕",
"🔟 우울감을 느낀다 😢","11️⃣ 사회적 모임에 피로를 느낀다 🏃‍♂️","12️⃣ 작은 일에도 걱정이 많다 🤯",
"13️⃣ 의사결정이 불안하다 ❓","14️⃣ 일을 끝까지 하지 못한다 ⏳","15️⃣ 주변 환경에 쉽게 짜증난다 🌪️",
"16️⃣ 몸이 긴장되고 뻐근하다 💪","17️⃣ 하루 중 기분 변화가 크다 🎭","18️⃣ 미래에 대한 불안감이 있다 🔮",
"19️⃣ 식사 패턴이 불규칙하거나 폭식을 한다 🍫","20️⃣ 쉬는 날에도 마음이 편하지 않다 🛌"
]

options=["0️⃣ 전혀 아니다","1️⃣ 가끔 그렇다","2️⃣ 자주 그렇다","3️⃣ 거의 항상 그렇다"]
score_mapping={"0️⃣ 전혀 아니다":0,"1️⃣ 가끔 그렇다":1,"2️⃣ 자주 그렇다":2,"3️⃣ 거의 항상 그렇다":3}

# ===================== 메인 화면 =====================
if st.session_state.page=="intro":
    st.markdown("""
    <div style='background: linear-gradient(135deg,#f6d365,#fda085);
                padding:80px; border-radius:30px; text-align:center;
                box-shadow: 10px 10px 50px #888888;'>
        <h1 style='font-size:4em;'>💖🧠 스트레스 진단 게임 🧠💖</h1>
        <p style='font-size:1.8em;'>20문항으로 나의 스트레스 상태를 확인! 🎉✨</p>
        <p style='font-size:1.5em;'>선택할 때마다 버튼 색이 변하고 이모지가 폭발합니다! 🌈💫</p>
    </div>
    """,unsafe_allow_html=True)
    if st.button("🚀 시작하기 🚀💥"): 
        st.session_state.page="quiz"
        st.rerun()

# ===================== 질문 화면 =====================
elif st.session_state.page=="quiz":
    q_idx=st.session_state.current_question
    st.markdown(f"""
    <div style='background-color:#FFF5E1;padding:50px;border-radius:30px;
                box-shadow: 10px 10px 30px #888888;text-align:center;'>
        <h2 style='font-size:3em;'>문제 {q_idx+1}/{len(questions)}</h2>
        <p style='font-size:2em;'>{questions[q_idx]}</p>
    </div>
    """,unsafe_allow_html=True)

    # 선택지 버튼 (클릭 시 강조)
    for opt in options:
        if st.button(f"{opt} 🌟",key=f"{q_idx}_{opt}"):
            st.session_state.answers.append(score_mapping[opt])
            st.session_state.current_question+=1
            if st.session_state.current_question>=len(questions):
                st.session_state.page="result"
            st.rerun()

    # 원형 느낌 진행률
    st.markdown(f"<p style='text-align:center;font-size:1.2em;'>진행률: {int((q_idx/len(questions))*100)}%</p>",unsafe_allow_html=True)
    st.progress(q_idx/len(questions))

# ===================== 결과 화면 =====================
elif st.session_state.page=="result":
    total_score=sum(st.session_state.answers)
    max_score=len(questions)*3
    result_type, description, color=calculate_result(st.session_state.answers)

    # 🎨 결과 카드
    st.markdown(f"""
    <div style='background:{color};padding:60px;border-radius:40px;
                text-align:center;box-shadow:10px 10px 50px #888888;'>
        <h1 style='font-size:4em;'>{result_type} 🎉✨</h1>
        <p style='font-size:2.5em;'>총점: {total_score}/{max_score}</p>
        <p style='font-size:2em;'>{description}</p>
    </div>
    """,unsafe_allow_html=True)

    st.progress(total_score/max_score)

    # 항목별 점수 그래프
    df=pd.DataFrame({"질문":[f"Q{i+1}" for i in range(len(st.session_state.answers))],
                     "점수":st.session_state.answers})
    st.bar_chart(df.set_index("질문"))

    # 완화 팁 카드
    st.markdown("""
    <div style='background-color:#FFF0F5;padding:40px;border-radius:25px;text-align:center;
                box-shadow: 5px 5px 20px #888888;'>
        <h2 style='font-size:2em;'>🌿 스트레스 완화 팁 🌿</h2>
        <ul style='font-size:1.5em;'>
            <li>🧘‍♀️ 심호흡 & 명상</li>
            <li>🚶‍♂️ 가벼운 산책</li>
            <li>🎶 음악 감상</li>
            <li>📞 친구/가족과 대화</li>
            <li>💤 규칙적인 숙면</li>
        </ul>
    </div>
    """,unsafe_allow_html=True)

    st.balloons()
    if st.button("🔄 다시 하기 💥"): 
        st.session_state.answers=[]
        st.session_state.current_question=0
        st.session_state.page="intro"
        st.rerun()
