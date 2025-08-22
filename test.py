import streamlit as st

# 🎨 앱 기본 세팅
st.set_page_config(page_title="이상형 심리테스트", page_icon="💘", layout="centered")

# 🧠 상태 초기화
if "answers" not in st.session_state:
    st.session_state.answers = []

if "page" not in st.session_state:
    st.session_state.page = "intro"


# 🎯 결과 계산 함수
def calculate_result(answers):
    score = sum(answers)

    if score <= 5:
        return "💖 따뜻한 배려형", "항상 내 편이 되어주고 마음을 챙겨주는 다정한 이상형이에요! 🥰🌸"
    elif score <= 10:
        return "😂 유머러스 인싸형", "언제나 분위기를 살리고 웃음을 주는 매력적인 이상형이에요! 🎉🤣"
    elif score <= 15:
        return "🧠 똑똑한 브레인형", "대화만 해도 똑똑함이 뿜뿜! 지적인 매력의 이상형이에요. 📚✨"
    else:
        return "🎨 자유로운 아티스트형", "창의적이고 독창적인 매력으로 가득한 이상형이에요! 🌈🎨"


# 📌 인트로 페이지
if st.session_state.page == "intro":
    st.title("💘 이상형 심리테스트 💘")
    st.subheader("나와 잘 맞는 이상형은 누구일까요?")

    st.markdown("👉 아래 버튼을 눌러 테스트를 시작해보세요!")
    if st.button("시작하기 🚀"):
        st.session_state.page = "quiz"
        st.rerun()


# 📌 질문 페이지
elif st.session_state.page == "quiz":
    st.title("📝 이상형 심리테스트")

    questions = [
        "데이트할 때 내가 선호하는 분위기는?",
        "상대방의 성격 중 더 끌리는 것은?",
        "이상형의 스타일은?",
        "대화할 때 나는?",
        "여행을 간다면 같이 하고 싶은 건?",
    ]

    options = [
        ["🍷 로맨틱한 분위기", "🎢 신나는 액티비티", "☕ 조용한 카페", "🌳 자연 속 산책"],
        ["😂 유머러스한 성격", "🧠 똑똑하고 논리적임", "💖 따뜻하고 배려심 많음", "🔥 열정적이고 적극적임"],
        ["👔 단정한 스타일", "🎨 개성 있는 스타일", "🏋️‍♂️ 운동 좋아하는 스타일", "🛋️ 편안한 캐주얼 스타일"],
        ["🎤 상대가 리드해주는 게 좋다", "🤔 주고받으며 의견 나누는 게 좋다", "👂 듣는 걸 좋아한다", "🤪 장난치면서 즐겁게 논다"],
        ["🏝️ 휴양지에서 힐링", "🏙️ 도시 탐험", "🏔️ 자연 속 트레킹", "🎉 축제/파티"],
    ]

    # 질문 진행
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}. {q}**")
        answer = st.radio("선택하세요", options[i], index=None, key=f"q{i}")
        if answer:
            if len(st.session_state.answers) < i + 1:
                st.session_state.answers.append(options[i].index(answer) + 1)
            else:
                st.session_state.answers[i] = options[i].index(answer) + 1

    if len(st.session_state.answers) == len(questions):
        if st.button("결과 보기 💘"):
            st.session_state.page = "result"
            st.rerun()


# 📌 결과 페이지
elif st.session_state.page == "result":
    st.title("💖 당신의 이상형은... 💖")

    result_type, description = calculate_result(st.session_state.answers)

    st.subheader(result_type)
    st.success(description)

    st.balloons()

    if st.button("🔄 다시 하기"):
        st.session_state.answers = []
        st.session_state.page = "intro"
        st.rerun()

