import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse
import time

# 1. 페이지 설정
st.set_page_config(page_title="KGC 주간 마케팅 대시보드", layout="wide")

# 2. 데이터 불러오기 설정
SHEET_ID = "1plSSNWnj1PZSZdhFXqukpJGtmUu2JtrLsxSjp8KV5Cw"
SHEET_NAME = "KPI" 

encoded_sheet_name = urllib.parse.quote(SHEET_NAME)
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"

@st.cache_data(ttl=60)
def load_raw_data():
    # pandas는 기본적으로 빈 행을 skip하므로 이를 고려한 인덱싱이 필요함
    return pd.read_csv(url)

# --- 메인 실행부 ---
try:
    raw_df = load_raw_data()
    
    # [검증된 데이터 추출] 
    # Index 0~3: KPI 지표들 (Row 2~5)
    # Index 4: AI 분석 내용 (Row 7 - '수도권 판매량이...')
    # Index 5: 팀장의 한마디 (Row 9 - '쌉가능!...')
    ai_analysis_data = raw_df.iloc[4, 0] if len(raw_df) > 4 else "데이터 로딩 실패"
    team_lead_word_data = raw_df.iloc[5, 0] if len(raw_df) > 5 else "데이터 로딩 실패"

    # --- 상단 레이아웃 (타이틀 & 우측 상단 AI 요약 버튼) ---
    head_col1, head_col2 = st.columns([0.7, 0.3])
    
    with head_col1:
        st.title("🚩 KGC 주간 통찰 리포트")
    
    with head_col2:
        st.write("") # 여백
        # [요청사항] 버튼 클릭 시 1초 로딩 효과 후 A7 내용 노출
        if st.button("✨ AI 요약보기", use_container_width=True):
            with st.spinner('AI가 리포트를 분석 중입니다...'):
                time.sleep(1) # 1초 로딩 연출
                st.info(f"🤖 **AI 상세 분석 (A7):** {ai_analysis_data}")

    # --- KPI 카드 섹션 ---
    kpi_df = raw_df.head(4).copy()
    kpi_df['value_clean'] = pd.to_numeric(kpi_df['value'].astype(str).str.replace('%', ''), errors='coerce')

    cols = st.columns(len(kpi_df))
    for i, (idx, row) in enumerate(kpi_df.iterrows()):
        with cols[i]:
            unit = "%" if "비율" in str(row['label']) or "타겟층" in str(row['label']) else ""
            st.metric(
                label=row['label'],
                value=f"{row['value_clean']}{unit}",
                delta=row['delta']
            )

    st.divider()

    # --- 중앙 차트 및 원본 데이터 섹션 ---
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.subheader("📊 주요 지표 비교")
        fig = px.bar(kpi_df, x='label', y='value_clean', color='label', text_auto=True)
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="수치")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("📋 실시간 데이터 테이블")
        st.dataframe(kpi_df[['label', 'value', 'delta']], use_container_width=True)

    # --- [요청사항] 중앙 하단 팀장의 한마디 (A9) ---
    st.divider()
    st.markdown(
        f"""
        <div style="background-color: #fff5f5; padding: 30px; border-radius: 15px; border: 2px solid #ff4b4b; text-align: center; margin-top: 20px;">
            <h3 style="color: #ff4b4b; margin-top: 0;">💬 팀장의 한마디 (A9)</h3>
            <p style="font-size: 1.4rem; font-weight: bold; color: #1f1f1f;">"{team_lead_word_data}"</p>
        </div>
        """, 
        unsafe_allow_html=True # HTML 렌더링 에러 수정 완료
    )

except Exception as e:
    st.error(f"⚠️ 시스템 오류: {e}")
