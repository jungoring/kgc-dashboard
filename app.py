import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

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
    
    # [데이터 추출] A7(Row 7) -> AI 분석 / A9(Row 9) -> 팀장 인사이트
    # iloc은 0부터 시작하며 헤더(1행)를 제외하므로 인덱스 5=7행, 7=9행
    ai_analysis = raw_df.iloc[5, 0] if len(raw_df) > 5 else "AI 분석 데이터가 없습니다."
    team_insight = raw_df.iloc[7, 0] if len(raw_df) > 7 else "등록된 팀장 인사이트가 없습니다."

    # --- 상단 타이틀 ---
    st.title("🚩 KGC 브랜드 전략실 주간 통찰 리포트")
    
    # --- 데이터 전처리 (상단 KPI 카드용) ---
    df = raw_df.copy()
    df['value_clean'] = pd.to_numeric(df['value'].astype(str).str.replace('%', ''), errors='coerce')
    kpi_df = df.dropna(subset=['value_clean']).head(4) # 상단 4개 지표

    # --- 상단 KPI 카드 섹션 ---
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

    # --- 차트 및 데이터 요약 섹션 ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 주요 지표 비교 차트")
        fig = px.bar(kpi_df, x='label', y='value_clean', color='label', text_auto=True,
                     labels={'value_clean': '수치', 'label': '지표'})
        # 차트 범례 제거 및 레이아웃 조정
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💡 실시간 데이터 요약")
        # [기능 반영] A7 셀의 AI 상세 분석 내용 노출
        st.chat_message("assistant", avatar="🤖").write(f"**AI 상세 분석 (A7):** {ai_analysis}")
        
        with st.expander("원본 데이터 테이블 확인"):
            st.table(kpi_df[['label', 'value', 'delta']])

    # --- 하단 인사이트 섹션 ---
    # [기능 반영] A9 셀의 내용을 팀장 인사이트 박스에 노출
    st.success(f"**📢 팀장 인사이트 (A9):** {team_insight}")

except Exception as e:
    st.error("⚠️ 데이터를 불러오는데 실패했습니다.")
    st.info(f"**팀장의 체크리스트:**\n1. 시트 탭 이름이 **'{SHEET_NAME}'** 인지 확인.\n2. 공유 설정 확인.")
    st.code(f"상세 에러 내역: {e}")
