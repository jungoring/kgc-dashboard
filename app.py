import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="KGC 주간 마케팅 대시보드", layout="wide")
st.markdown('<script src="https://cdn.tailwindcss.com"></script>', unsafe_allow_html=True)

# 2. 데이터 불러오기 함수
SHEET_ID = "1plSSNWnj1PZSZdhFXqukpJGtmUu2JtrLsxSjp8KV5Cw"
SHEET_NAME = "준영데이터260514"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=60)
def load_data():
    data = pd.read_csv(url)
    # 데이터 전처리: %, 숫자가 섞인 경우를 대비해 안전하게 변환
    data['value'] = data['value'].astype(str).str.replace('%', '').astype(float)
    return data

# --- 메인 실행부 ---
st.title("🚩 KGC 브랜드 전략실 주간 통찰 리포트")

try:
    # 데이터 로드 시도
    df = load_data()

    # --- 상단 KPI 카드 섹션 ---
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        with cols[i]:
            unit = "%" if "비율" in str(row['label']) or "타겟층" in str(row['label']) else ""
            st.metric(
                label=row['label'],
                value=f"{row['value']}{unit}",
                delta=row['delta']
            )

    st.divider()

    # --- 차트 및 표 섹션 ---
    col_chart1, col_chart2 = st.columns([1, 1])
    with col_chart1:
        st.subheader("📊 주요 지표 비교")
        fig = px.bar(df, x='label', y='value', color='label', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("💡 데이터 요약 표")
        st.table(df)

    # --- [중요] 팀장 인사이트: try 문 안으로 이동 ---
    # 데이터 로드에 성공했을 때만 실행되도록 위치를 조정했습니다.
    if len(df) > 1:
        insight_label = df.iloc[1]['label']
        insight_val = df.iloc[1]['value']
        st.success(f"**팀장 인사이트:** {insight_label}이 {insight_val}%로 압도적입니다. 2030 타겟팅 전략을 강화합시다!")

except Exception as e:
    # 에러 발생 시 df가 정의되지 않아도 NameError가 나지 않음
    st.error("⚠️ 데이터를 불러오는데 실패했습니다.")
    st.warning("1. 구글 시트가 [링크가 있는 모든 사용자]에게 [뷰어] 권한으로 공유되었는지 확인하세요.")
    st.warning("2. 시트의 컬럼명(label, value, delta)이 1행에 정확히 있는지 확인하세요.")
    st.info(f"기술적 에러 메시지: {e}")
