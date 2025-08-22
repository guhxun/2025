import streamlit as st
import pandas as pd

# 🎨 앱 기본 세팅
st.set_page_config(page_title="스트레스 자가 진단", page_icon="🧠", layout="centered")

# 🧠 상태 초기화
if "answers" not in st.session_state:
    st.session_state.answers = []

if "page" not in st.session_state:
    st.session_state.page = "intro"

# 🎯 결과 계산 함수
def calculate_result(answers):
    score = sum(answers)
    if score <= 12:
        return "😌 스트레스 수준 낮음", "잘 관리하고 있어요! 꾸준히 자기 관리하세요 🌿"
    elif score <= 20:
        return "🙂 보통 수준", "조금 지친 상태예요. 충분한 휴식과 취미 생활이 필요해요 🎶"
    elif score <= 28:
        return "😥 스트레스 높음", "많이 힘들어 하고 있네요. 자기 돌봄이 꼭 필요합니다 🧘"
    else:
        return "😢 심각한 스트레스", "전문가 상담을 고려해보세요. 혼자 감당하지 마세요 💌"

# 📌 인트로 페이지
if st.session_state.page == "intro":
    st.title("🧠 스트레스 자가 진단 테스트")
    st.subheader("당신의 스트레스 수준을 확인해보세요")
    st.markdown("👉 최근 1주일 ~ 1개월 동안의 경험을 바탕으로 답해주세요.")
    
    if st.button("시작하기 🚀"):
        st.session_state.page = "quiz"
        st.rerun()

# 📌 질문 페이지
elif st.session_state.page == "quiz":
    st.title("📝 스트레스 체크리스트")

    questions = [
        "1. 최근 1주일 동안 잠들기 어려웠다 😴",
        "2. 해야 할 일이 너무 많다고 느낀다 📚",
        "3. 사소한 일에도 짜증이 난다 😡",
        "4. 집중이 잘 되지 않는다 🧠",
        "5. 피곤함이 지속된다 🥱",
        "6. 마음이 불안하거나 조급하다 😟",
        "7. 주변 사람들과 갈등이 잦다 👥",
        "8. 먹는 습관이 불규칙하다 🍔",
        "9. 두통이나 근육통 같은 신체적 증상이 있다 🤕",
        "10. 기분이 가라앉고 우울감을 느낀다 😢",
    ]

    options = ["0: 전혀 아니다", "1: 가끔 그렇다", "2: 자주 그렇다", "3: 거의 항상 그렇다"]
    
    # 점수 매핑
    score_mapping = {
        "0: 전혀 아니다": 0,
        "1: 가끔 그렇다": 1,
        "2: 자주 그렇다": 2,
        "3: 거의 항상 그렇다": 3
    }

    st.session_state.answers = []  # 초기화 후 다시 담기
    for i, q in enumerate(questions):
        answer = st.radio(q, options, horizontal=True, key=f"q{i}")
        st.session_state.answers.append(score_mapping[answer])

    if st.button("결과 보기 🎉"):
        st.session_state.page = "result"
        st.rerun()

# 📌 결과 페이지
elif st.session_state.page == "result":
    st.title("📊 스트레스 진단 결과")

    result_type, description = calculate_result(st.session_state.answers)
    total_score = sum(st.session_state.answers)
    max_score = len(st.session_state.answers) * 3

    # 결과 표시
    st.subheader(result_type)
    st.info(f"👉 총점: {total_score} / {max_score}")
    st.success(description)

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
        st.session_state.page = "intro"
        st.rerun()

