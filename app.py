import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse
import time  # 로딩 효과를 위해 추가

# 1. 페이지 설정
st.set_page_config(page_title="KGC 주간 마케팅 대시보드", layout="wide")

# 2. 데이터 불러오기 설정
SHEET_ID = "1plSSNWnj1PZSZdhFXqukpJGtmUu2JtrLsxSjp8KV5Cw"
SHEET_NAME = "KPI" 

encoded_sheet_name = urllib.parse.quote(SHEET_NAME)
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"

@st.cache_data(ttl=60)
def load_raw_data():
    return pd.read_csv(url)

# --- 메인 실행부 ---
try:
    raw_df = load_raw_data()
    
    # [데이터 추출] A7(Row 7) -> AI 분석 / A9(Row 9) -> 팀장의 한마디
    # pandas iloc은 0부터 시작, 헤더 제외 기준: 인덱스 5=7행, 7=9행
    # 사용자의 요청에 따라 A7은 AI 분석, A9는 팀장의 한마디로 확실히 고정
    ai_analysis_data = raw_df.iloc[5, 0] if len(raw_df) > 5 else "AI 분석 데이터가 없습니다."
    team_lead_word_data = raw_df.iloc[7, 0] if len(raw_df) > 7 else "오늘의 한마디가 없습니다."

    # --- 상단 레이아웃 (타이틀 & 우측 상단 AI 요약 버튼) ---
    head_col1, head_col2 = st.columns([0.7, 0.3])
    
    with head_col1:
        st.title("🚩 KGC 주간 통찰 리포트")
    
    with head_col2:
        st.write("") # 높이 맞춤용
        # [기능 개선] 버튼 클릭 시 로딩 후 데이터 노출
        if st.button("✨ AI 요약보기", use_container_width=True):
            with st.spinner('AI가 데이터를 분석 중입니다...'):
                time.sleep(1) # 1초 로딩 효과
                st.info(f"🤖 **AI 상세 분석 (A7):** {ai_analysis_data}")

    # --- 데이터 전처리 (KPI용) ---
    df = raw_df.copy()
    df['value_clean'] = pd.to_numeric(df['value'].astype(str).str.replace('%', ''), errors='coerce')
    kpi_df = df.dropna(subset=['value_clean']).head(4) 

    # --- KPI 카드 섹션 ---
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

    # --- [핵심 수정] 중앙 하단 팀장의 한마디 (A9) ---
    st.divider()
    st.markdown(
        f"""
        <div style="background-color: #f8f9fa; padding: 30px; border-radius: 20px; border: 2px solid #ff4b4b; text-align: center; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #ff4b4b;">💬 팀장의 한마디 (A9)</h3>
            <p style="font-size: 1.4rem; color: #262730; font-weight: bold; line-height: 1.6;">
                "{team_lead_word_data}"
            </p>
        </div>
        """, 
        unsafe_allow_html=True # 에러 났던 부분 수정 완료
    )

except Exception as e:
    st.error(f"⚠️ 데이터를 불러오는데 실패했습니다: {e}")
    st.info("시트의 A7(7행)과 A9(9행)에 텍스트가 제대로 입력되어 있는지 확인해 봐!")
