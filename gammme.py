import streamlit as st

# 페이지 기본 설정 (wide 모드로 설정하여 가로 공간 확보)
st.set_page_config(page_title="Streamlit 오목 게임", page_icon="⚪", layout="wide")

BOARD_SIZE = 15

# 게임 상태 초기화 함수
def init_game():
    st.session_state.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "🔴"  # 🔴(선공) / 🔵(후공)
    st.session_state.winner = None

# 초기 상태가 없으면 생성
if "board" not in st.session_state:
    init_game()

# 승리 조건 검사 함수 (5개 이상 연속 배치 체크)
def check_winner(r, c, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # 정방향 탐색
        nr, nc = r + dr, c + dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and st.session_state.board[nr][nc] == player:
            count += 1
            nr += dr
            nc += dc
        # 역방향 탐색
        nr, nc = r - dr, c - dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and st.session_state.board[nr][nc] == player:
            count += 1
            nr -= dr
            nc -= dc
            
        if count >= 5:
            return True
    return False

# 돌 놓기 클릭 이벤트 처리
def place_stone(r, c):
    if st.session_state.board[r][c] is not None or st.session_state.winner is not None:
        return
        
    current = st.session_state.current_player
    st.session_state.board[r][c] = current
    
    if check_winner(r, c, current):
        st.session_state.winner = current
    else:
        st.session_state.current_player = "🔵" if current == "🔴" else "🔴"

# UI 헤더 및 리셋 버튼
st.title("⚪ Streamlit 오목 게임")

col_status, col_reset = st.columns([3, 1])
with col_status:
    if st.session_state.winner:
        st.success(f"🎉 승리: {st.session_state.winner} 플레이어!")
    else:
        st.info(f"현재 턴: {st.session_state.current_player}")

with col_reset:
    if st.button("게임 리셋", use_container_width=True):
        init_game()
        st.rerun()

st.markdown("---")

# 오목판 중앙 정렬을 위한 컨테이너
_, board_container, _ = st.columns([1, 10, 1])

with board_container:
    # 15x15 오목판 렌더링
    for r in range(BOARD_SIZE):
        cols = st.columns(BOARD_SIZE)
        for c in range(BOARD_SIZE):
            stone = st.session_state.board[r][c]
            label = stone if stone is not None else "┼"
            
            cols[c].button(
                label, 
                key=f"btn_{r}_{c}", 
                on_click=place_stone, 
                args=(r, c),
                disabled=(st.session_state.winner is not None or stone is not None)
            )

# 그리드 깨짐 방지용 CSS (버튼 폭/여백 강제 고정)
st.markdown("""
    <style>
    /* 컬럼 간격 최소화 및 flex 래핑 방지 */
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        min-width: unset !important;
    }
    
    /* 오목판 버튼 크기 고정 */
    div[data-testid="column"] button {
        height: 32px !important;
        width: 32px !important;
        min-width: 32px !important;
        padding: 0px !important;
        margin: 0px !important;
        font-size: 13px !important;
        border-radius: 0px !important;
        line-height: 1 !important;
    }
    
    /* 15줄 가로 배치 정렬 */
    div[data-testid="stHorizontalBlock"] {
        gap: 0px !important;
        justify-content: center !important;
    }
    </style>
""", unsafe_style_html=True)
