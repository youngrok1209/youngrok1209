import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="AI 칭찬 생성기", page_icon="👏", layout="centered")

st.title("👏 AI 칭찬 생성기")
st.write("오늘 잘한 일이나 칭찬받고 싶은 내용을 입력해 보세요!")

# Secrets에서 API 키 가져오기 및 클라이언트 초기화
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except KeyError:
    st.error("Streamlit Secrets에 'OPENAI_API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 사용자 입력
user_input = st.text_area(
    "칭찬받고 싶은 내용:",
    placeholder="예: 오늘 아침 일찍 일어나서 운동을 30분 동안 하고 왔어!",
    height=120,
)

# 칭찬 생성 버튼
if st.button("✨ 칭찬받기", type="primary"):
    if not user_input.strip():
        st.warning("칭찬받고 싶은 내용을 먼저 입력해 주세요.")
    else:
        with st.spinner("AI가 당신을 위한 멋진 칭찬을 작성 중입니다..."):
            try:
                # API 호출 (gpt-5.4-nano 사용)
                response = client.chat.completions.create(
                    model="gpt-5.4-nano",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "너는 세상에서 가장 따뜻하고 다정한 칭찬 전문가야. "
                                "사용자가 작성한 내용을 바탕으로 진심 어린 격려와 칭찬, "
                                "그리고 기분 좋은 이모지를 섞어서 답변해 줘."
                            ),
                        },
                        {"role": "user", "content": user_input},
                    ],
                )

                # 결과 출력
                praise_result = response.choices[0].message.content
                st.success("칭찬 도착!")
                st.info(praise_result)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
