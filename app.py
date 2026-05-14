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
    # 전처리 전의 원본 데이터를 읽어옵니다.
    return pd.read_csv(url)

# --- 메인 실행부 ---
try:
    raw_df = load_raw_data()
    
    # [기능 1] A7(인덱스 5), A9(인덱스 7) 데이터 추출 
    # pandas는 0부터 시작하며 헤더를 제외하므로 시트의 행 번호와 차이가 있을 수 있음
    # 아래 인덱스는 시트의 'Row 7'과 'Row 9'를 타겟팅함 (헤더가 1행일 경우)
    ai_analysis = raw_df.iloc[5, 0] if len(raw_df) > 5 else "분석 데이터가 없습니다."
    fun_fact = raw_df.iloc[7, 0] if len(raw_df) > 7 else "오늘의 팁이 없습니다."

    # --- 헤더 섹션 (타이틀 + 우측 상단 버튼) ---
    head_col1, head_col2 = st.columns([0.8, 0.2])
    
    with head_col1:
        st.title("🚩 KGC 브랜드 전략실 주간 통찰 리포트")
    
    with head_col2:
        st.write("") # 간격 맞춤용
        # 우측 상단 AI 분석 버튼 (팝오버 형식)
        with st.popover("🤖 AI 상세 분석 보기"):
            st.markdown("### **AI 마케팅 분석 리포트**")
            st.info(ai_analysis)

    # --- 데이터 전처리 (KPI용) ---
    df = raw_df.copy()
    # 수치 데이터가 있는 상위 행만 필터링 (A7, A9 등 텍스트 행 제외)
    df['value_clean'] = pd.to_numeric(df['value'].astype(str).str.replace('%', ''), errors='coerce')
    kpi_df = df.dropna(subset=['value_clean']).head(5) # 상위 5개 지표만 사용

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

    # --- 차트 및 데이터 테이블 섹션 ---
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📊 주요 지표 비교 차트")
        fig = px.bar(kpi_df, x='label', y='value_clean', color='label', text_auto=True,
                     labels={'value_clean': '수치', 'label': '지표'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💡 실시간 데이터 요약")
        # [기능 2] A9 셀의 내용을 담은 재미난 박스
        st.chat_message("assistant", avatar="✨").write(f"**오늘의 마케팅 한줄평:** {fun_fact}")
        
        with st.expander("원본 데이터 테이블 확인"):
            st.table(kpi_df[['label', 'value', 'delta']])

    # --- 팀장 인사이트 ---
    if len(kpi_df) > 1:
        st.success(f"**팀장 인사이트:** {kpi_df.iloc[0]['label']} 성과가 눈에 띄네! 이번 주도 고생 많았어.")

except Exception as e:
    st.error("⚠️ 데이터를 불러오는데 실패했습니다.")
    st.info(f"**팀장의 체크리스트:**\n1. 시트 하단 탭 이름이 **'{SHEET_NAME}'** 인지 확인.\n2. 공유 설정 확인.")
    st.code(f"상세 에러 내역: {e}")
