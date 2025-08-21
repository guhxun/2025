import streamlit as st

st.set_page_config(page_title="MBTI 진로교육 사이트", page_icon="🎓")

# 홈
st.title("🎓 MBTI 기반 진로교육 사이트")
st.write("당신의 성격유형(MBTI)을 기반으로 맞춤형 진로 추천을 제공합니다.")

# MBTI 입력
mbti = st.text_input("당신의 MBTI를 입력하세요 (예: INFP, ESTJ)").upper()

career_dict = {
    "INTP": {
        "특징": "논리적이고 분석적이며 창의적인 성향",
        "추천 진로": ["연구원", "개발자", "교수", "데이터 분석가"],
        "학습 팁": "깊이 있는 탐구와 자기 주도 학습이 효과적"
    },
    "ESFJ": {
        "특징": "사교적이고 협력적이며 책임감 있는 성향",
        "추천 진로": ["교사", "간호사", "사회복지사", "인사담당자"],
        "학습 팁": "팀 프로젝트와 협업 환경에서 성장"
    },
    # 다른 MBTI도 추가 가능
}

if mbti in career_dict:
    st.subheader(f"✨ {mbti} 유형 결과")
    st.write("**특징:**", career_dict[mbti]["특징"])
    st.write("**추천 진로:**", ", ".join(career_dict[mbti]["추천 진로"]))
    st.write("**학습 팁:**", career_dict[mbti]["학습 팁"])
else:
    if mbti:
        st.warning("아직 등록되지 않은 MBTI 유형입니다. (추가 예정)")
