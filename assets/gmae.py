import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="Streamlit 오목 게임", page_icon="⚪", layout="centered")

BOARD_SIZE = 15

# 게임 상태 초기화 함수
def init_game():
    st.session_state.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.current_player = "🔴"  # 🔴(선공) / 🔵(후공)
    st.session_state.winner = None
    st.session_state.winning_line = []

# 초기 상태가 없으면 생성
if "board" not in st.session_state:
    init_game()

# 승리 조건 검사 함수 (5개 이상 연속 배치 체크)
def check_winner(r, c, player):
    directions = [
        (0, 1),   # 가로
        (1, 0),   # 세로
        (1, 1),   # 대각선 ↘
        (1, -1)   # 대각선 ↙
    ]
    
    for dr, dc in directions:
        count = 1
        line = [(r, c)]
        
        # 정방향 탐색
        nr, nc = r + dr, c + dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and st.session_state.board[nr][nc] == player:
            count += 1
            line.append((nr, nc))
            nr += dr
            nc += dc
            
        # 역방향 탐색
        nr, nc = r - dr, c - dc
        while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and st.session_state.board[nr][nc] == player:
            count += 1
            line.append((nr, nc))
            nr -= dr
            nc -= dc
            
        if count >= 5:
            return True, line
            
    return False, []

# 돌 놓기 클릭 이벤트 처리
def place_stone(r, c):
    if st.session_state.board[r][c] is not None or st.session_state.winner is not None:
        return
        
    current = st.session_state.current_player
    st.session_state.board[r][c] = current
    
    is_win, line = check_winner(r, c, current)
    if is_win:
        st.session_state.winner = current
        st.session_state.winning_line = line
    else:
        # 턴 교체
        st.session_state.current_player = "🔵" if current == "🔴" else "🔴"

# UI 헤더 및 리셋 버튼
st.title("⚪ Streamlit 오목 게임")

top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    if st.session_state.winner:
        st.success(f"🎉 승리: {st.session_state.winner} 플레이어!")
    else:
        st.info(f"현재 턴: {st.session_state.current_player}")

with top_col2:
    if st.button("게임 리셋", use_container_width=True):
        init_game()
        st.rerun()

st.markdown("---")

# 15x15 오목판 렌더링
for r in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for c in range(BOARD_SIZE):
        stone = st.session_state.board[r][c]
        
        # 버튼에 표시할 텍스트 지정 (빈 공간은 + 표시)
        label = stone if stone is not None else "+"
        
        # 버튼 생성 및 클릭 시 착수
        cols[c].button(
            label, 
            key=f"btn_{r}_{c}", 
            on_click=place_stone, 
            args=(r, c),
            disabled=(st.session_state.winner is not None or stone is not None)
        )

# 커스텀 CSS로 보드 패딩 및 버튼 크기 정렬
st.markdown("""
    <style>
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
    }
    div[data-testid="column"] button {
        height: 38px !important;
        width: 100% !important;
        padding: 0px !important;
        font-size: 14px !important;
    }
    </style>
""", unsafe_style_html=True)
