import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="에브리타임 밸런스 마케팅 대시보드",
    page_icon="📈",
    layout="wide",
)

# Tailwind CSS 및 Pretendard 폰트 로드
st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
        body { font-family: 'Pretendard', sans-serif ! sensitivity; }
        .stApp { background-color: #f8fafc; }
        /* 스트림릿 기본 여백 제거 및 커스텀 스타일 */
        .main .block-container { padding: 2rem 3rem; }
        .metric-card {
            background: white; padding: 2rem; border-radius: 1.5rem;
            border-top: 8px solid; transition: transform 0.3s;
        }
        .metric-card:hover { transform: translateY(-5px); }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="flex flex-col md:flex-row md:items-center justify-between border-b-2 border-slate-200 pb-8 mb-10 gap-4">
        <div>
            <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">주간 마케팅 통찰 <span class="text-blue-600">리포트 (Streamlit)</span></h1>
            <p class="text-slate-500 text-lg mt-2">정관장 에브리타임 밸런스 리뉴얼 성과 분석 (2026.03.W4)</p>
        </div>
        <div class="flex items-center gap-3">
            <div class="text-right">
                <p class="text-sm font-bold text-slate-400">REPORTED BY</p>
                <p class="text-slate-800 font-semibold">브랜드전략실 마케팅 팀장</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                <span class="text-blue-600 font-black">KGC</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="metric-card" style="border-color: #2563eb;">
            <p class="text-slate-500 font-bold text-xs uppercase tracking-widest">2030 구매 비중</p>
            <h2 class="text-5xl font-black text-slate-800 mt-2">45%</h2>
            <p class="text-blue-600 font-bold mt-2 text-sm">타겟 고객군 유입 가시화</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card" style="border-color: #10b981;">
            <p class="text-slate-500 font-bold text-xs uppercase tracking-widest">수도권 CVS 성장</p>
            <h2 class="text-5xl font-black text-slate-800 mt-2">+15%</h2>
            <p class="text-emerald-600 font-bold mt-2 text-sm">오피스 권역 편의점 견인</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card" style="border-color: #f43f5e;">
            <p class="text-slate-500 font-bold text-xs uppercase tracking-widest">아웃도어 키워드</p>
            <h2 class="text-5xl font-black text-slate-800 mt-2">30%</h2>
            <p class="text-rose-600 font-bold mt-2 text-sm">신규 TPO 확산 신호</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="mt-8 bg-blue-50 border-l-4 border-blue-600 p-6 rounded-r-2xl mb-12">
        <p class="text-blue-900 font-semibold leading-relaxed">
            리뉴얼의 핵심 기획 의도였던 '맛의 개선'과 '감각적 패키지'가 2030 사회초년생의 니즈와 부합하며 시장에 안착 중입니다.
        </p>
    </div>
""", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # 1. 인구 통계 도넛 차트
    labels = ['2030 사회초년생', '4050 기성세대', '기타 세대']
    values = [45, 35, 20]
    fig_age = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7, 
                                    marker=dict(colors=['#2563eb', '#cbd5e1', '#f1f5f9']))])
    fig_age.update_layout(title="구매 고객 인구 통계", showlegend=True, height=400, margin=dict(t=50, b=50, l=0, r=0))
    st.plotly_chart(fig_age, use_container_width=True)

    # 3. VOC 감성 파이 차트
    labels_voc = ['긍정 (맛/디자인)', '부정 (가격/포장)', '중립/기타']
    values_voc = [65, 25, 10]
    fig_voc = go.Figure(data=[go.Pie(labels=labels_voc, values=values_voc, 
                                    marker=dict(colors=['#10b981', '#f43f5e', '#94a3b8']))])
    fig_voc.update_layout(title="고객 경험(VOC) 심리 분석", height=400, margin=dict(t=50, b=50, l=0, r=0))
    st.plotly_chart(fig_voc, use_container_width=True)

with chart_col2:
    # 2. 지역별 판매 격차 바 차트
    fig_regional = go.Figure(data=[go.Bar(x=['수도권/편의점', '지방/대형마트'], y=[15, -2],
                                        marker_color=['#2563eb', '#f43f5e'])])
    fig_regional.update_layout(title="채널/지역별 판매 격차 (%)", height=400, margin=dict(t=50, b=50, l=0, r=0))
    st.plotly_chart(fig_regional, use_container_width=True)

    # 4. 아웃도어 트렌드 레이더 차트
    categories = ['피로 회복', '선물용 지수', '야외 활동', '데일리 루틴', '자기 관리']
    fig_radar = go.Figure(data=go.Scatterpolar(
      r=[85, 90, 95, 80, 88],
      theta=categories,
      fill='toself',
      line_color='#2563eb'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), 
                           showlegend=False, title="Athleisure TPO 강도", height=400, margin=dict(t=50, b=50, l=0, r=0))
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("""
    <div class="bg-slate-900 rounded-[3rem] p-10 md:p-16 text-white mt-12 relative overflow-hidden">
        <div class="relative z-10">
            <h2 class="text-3xl font-black mb-12">전략적 제언 <span class="text-blue-400">Action Items</span></h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
                <div class="space-y-8">
                    <div class="flex items-center gap-3">
                        <span class="bg-blue-600 px-4 py-1 rounded-full text-xs font-black">SHORT-TERM</span>
                        <span class="text-slate-400 font-bold">고객 경험 및 프로모션</span>
                    </div>
                    <div class="pl-4 border-l-2 border-blue-600/30 space-y-6">
                        <div>
                            <h4 class="text-lg font-bold text-blue-400">01 CX 개선: 패키지 공정 점검</h4>
                            <p class="text-slate-400 text-sm mt-1">'Easy-Open' 구조 도입 및 현 공정 즉각 점검 실시.</p>
                        </div>
                        <div>
                            <h4 class="text-lg font-bold text-blue-400">02 CVS 거점별 타켓 마케팅</h4>
                            <p class="text-slate-400 text-sm mt-1">수도권 오피스 권역 편의점 대상 프로모션 강화.</p>
                        </div>
                    </div>
                </div>
                <div class="space-y-8">
                    <div class="flex items-center gap-3">
                        <span class="bg-emerald-600 px-4 py-1 rounded-full text-xs font-black">MID-TERM</span>
                        <span class="text-slate-400 font-bold">브랜드 포지셔닝 확장</span>
                    </div>
                    <div class="pl-4 border-l-2 border-emerald-600/30 space-y-6">
                        <div>
                            <h4 class="text-lg font-bold text-emerald-400">03 아웃도어 TPO 캠페인</h4>
                            <p class="text-slate-400 text-sm mt-1">스포츠 브랜드 협업 및 등산로 팝업 스토어 기획.</p>
                        </div>
                        <div>
                            <h4 class="text-lg font-bold text-emerald-400">04 채널 Value-up</h4>
                            <p class="text-slate-400 text-sm mt-1">대형마트 채널 체험형 VMD 및 시음 마케팅 강화.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="text-center py-10 text-slate-400 text-sm font-medium">
        &copy; 2026 KGC 브랜드전략실 마케팅팀. 본 리포트는 내부 기밀 정보가 포함되어 있습니다.
    </div>
""", unsafe_allow_html=True)
