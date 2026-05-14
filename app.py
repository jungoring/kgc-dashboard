import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 디자인 (Tailwind CSS 주입)
st.set_page_config(page_title="KGC 주간 마케팅 대시보드", layout="wide")
st.markdown('<script src="https://cdn.tailwindcss.com"></script>', unsafe_allow_html=True)

# 2. 데이터 불러오기 함수 (보안 스킵 버전 - CSV 직접 호출)
# 이미지에 있는 시트 URL의 ID부분을 본인의 시트 ID로 교체하세요.
SHEET_ID = "1plSSNWnj1PZSZdhFXqukpJGtmUu2JtrLsxSjp8KV5Cw" # 시트 주소창의 d/ 와 /edit 사이의 문자열
SHEET_NAME = "준영데이터260514"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=60) # 1분마다 새로고침
def load_data():
    df = pd.read_csv(url)
    # 데이터 정제: % 기호 제거 및 숫자 변환
    if df['value'].dtype == 'object':
        df['value'] = df['value'].str.replace('%', '').astype(float)
    return df

try:
    df = load_data()

    # --- 헤더 섹션 ---
    st.title("🚩 KGC 브랜드 전략실 주간 통찰 리포트")
    st.info(f"데이터 소스: 구글 스프레드시트 ({SHEET_NAME}) | 실시간 동기화 중")
    st.divider()

    # --- 상단 KPI 카드 섹션 ---
    cols = st.columns(len(df))

    for i, row in df.iterrows():
        with cols[i]:
            # % 기호가 필요한 항목 구분
            unit = "%" if "비율" in row['label'] or "타겟층" in row['label'] else ""
            st.metric(
                label=row['label'],
                value=f"{row['value']}{unit}",
                delta=row['delta']
            )

    st.divider()

    # --- 차트 섹션 ---
    col_chart1, col_chart2 = st.columns([1, 1])

    with col_chart1:
        st.subheader("📊 주요 지표 비교")
        fig = px.bar(df, x='label', y='value', color='label',
                     text_auto=True, title="항목별 수치 현황")
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("💡 데이터 요약 표")
        st.table(df)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다. 시트 공유 설정을 확인해주세요! : {e}")

# --- 마케팅 팀장의 한줄 평 (시트의 데이터 기반) ---
st.success(f"**팀장 인사이트:** {df.iloc[1]['label']}이 {df.iloc[1]['value']}%로 압도적입니다. 2030 타겟팅 전략을 강화합시다!")
