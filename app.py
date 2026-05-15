import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import time

# --- 1. 환경 설정 ---
st.set_page_config(page_title="서울 대기질 관제 시스템", layout="wide")
plt.style.use("ggplot")

# --- 2. 데이터 처리 함수 ---
@st.cache_data
def get_processed_data():
    # 파일 경로는 로컬에 맞게 수정 (예: 'seoul micro dust.csv')
    df = pd.read_csv("seoul micro dust.csv", encoding='cp949')
    df.columns = ['timestamp', 'district', 'pm10', 'pm25']
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['pm_ratio'] = df['pm25'] / df['pm10']
    df['warning_flag'] = (df['pm10'] > 80).astype(int)
    return df

def calc_cpk(group):
    mean, std = group["pm10"].mean(), group["pm10"].std()
    if std == 0 or np.isnan(std): return 0.0
    usl, lsl = 80, 0
    return round(min((usl - mean) / (3 * std), (mean - lsl) / (3 * std)), 3)

# --- 3. 모델 학습 함수 ---
@st.cache_resource
def train_model(df):
    model_cols = ["pm25", "hour", "day_of_week", "pm_ratio"]
    clean_df = df.dropna(subset=model_cols + ["warning_flag"])
    X = clean_df[model_cols]
    y = clean_df["warning_flag"]
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X, y)
    return model, model_cols

# --- 4. 메인 실행 로직 ---
try:
    df = get_processed_data()
    model, model_cols = train_model(df)

    st.sidebar.title("⚙️ 설정")
    selected_district = st.sidebar.selectbox("분석 대상 구", df['district'].unique())

    tab1, tab2, tab3 = st.tabs(["📊 통계 분석", "📈 관리도", "📡 실시간 관제 시뮬레이션"])

    with tab1:
        st.subheader("구별 대기질 관리 능력 (Cpk) 및 경고 비율")
        cpk_df = df.groupby("district").apply(calc_cpk).reset_index(name="cpk")
        warn_df = df.groupby("district")['warning_flag'].mean().reset_index(name="ratio")
        summary = pd.merge(cpk_df, warn_df, on="district").sort_values("cpk")
        st.dataframe(summary.style.background_gradient(cmap='RdYlGn_r', subset=['cpk']))

    with tab2:
        st.subheader(f"[{selected_district}] 미세먼지 관리도")
        chart_df = df[df['district'] == selected_district].sort_values('timestamp').tail(200)
        mean_v, std_v = chart_df['pm10'].mean(), chart_df['pm10'].std()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(chart_df['timestamp'], chart_df['pm10'], marker='o', markersize=2)
        ax.axhline(mean_v, color='g', linestyle='--', label='평균')
        ax.axhline(mean_v + 3*std_v, color='r', linestyle='--', label='UCL')
        ax.legend()
        st.pyplot(fig)

    with tab3:
        st.subheader("24시간 가상 시나리오 관제")
        if st.button("시뮬레이션 시작"):
            status_area = st.empty()
            log_area = st.container()
            for h in range(24):
                # 가상 데이터 생성 로직 (생략 가능, 노트북의 sim_df 로직)
                val_pm25 = 10 if h < 12 else (95 if h == 15 else 15)
                sim_row = pd.DataFrame([{'pm25': val_pm25, 'hour': h, 'day_of_week': 4, 'pm_ratio': 0.65}])
                prob = model.predict_proba(sim_row)[0, 1]
                
                with status_area:
                    if prob > 0.5: st.error(f"🚨 {h:02d}:00 위기 상황! 확률: {prob:.2f}")
                    else: st.success(f"✅ {h:02d}:00 정상 운용 중. 확률: {prob:.2f}")
                time.sleep(0.3)

except Exception as e:
    st.error(f"오류 발생: {e}")
