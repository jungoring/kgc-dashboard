import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse  # 한글 주소 변환을 위해 필요합니다

# 1. 페이지 설정
st.set_page_config(page_title="KGC 주간 마케팅 대시보드", layout="wide")

# 2. 데이터 불러오기 설정
SHEET_ID = "1plSSNWnj1PZSZdhFXqukpJGtmUu2JtrLsxSjp8KV5Cw"
# [수정] 이미지 하단 탭 이름이 'KPI'이므로 이를 반영합니다.
SHEET_NAME = "KPI" 

# 한글 시트 이름을 웹 주소용으로 안전하게 변환 (ASCII 에러 방지)
encoded_sheet_name = urllib.parse.quote(SHEET_NAME)
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"

@st.cache_data(ttl=60)
def load_data():
    # 시트 데이터를 읽어옵니다.
    data = pd.read_csv(url)
    
    # 데이터 전처리: value 컬럼의 %, 숫자를 안전하게 변환
    # '에러' 메시지가 포함된 행이 있을 수 있어 에러 무시 옵션을 넣었습니다.
    data['value'] = pd.to_numeric(data['value'].astype(str).str.replace('%', ''), errors='coerce')
    return data

# --- 메인 실행부 ---
st.title("🚩 KGC 브랜드 전략실 주간 통찰 리포트")

try:
    df = load_data()
    
    # 데이터가 비어있거나 에러가 있는 행 제외 (값이 있는 데이터만 필터링)
    df = df.dropna(subset=['value'])

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

    # --- 차트 및 데이터 테이블 섹션 ---
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📊 주요 지표 비교 차트")
        fig = px.bar(df, x='label', y='value', color='label', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("💡 시트 원본 데이터")
        st.table(df)

    # --- 팀장 인사이트 ---
    if len(df) > 1:
        st.success(f"**팀장 인사이트:** {df.iloc[1]['label']} 수치가 {df.iloc[1]['value']}%로 매우 높습니다. 타겟 집중도를 유지합시다!")

except Exception as e:
    st.error("⚠️ 데이터를 불러오는데 실패했습니다.")
    st.info(f"**팀장의 체크리스트:**\n1. 시트 하단 탭 이름이 정말 **'{SHEET_NAME}'** 인지 확인해 보세요.\n2. 공유 설정이 [링크가 있는 모든 사용자]로 되어 있는지 확인해 보세요.")
    st.code(f"상세 에러 내역: {e}")
