import streamlit as st
import random
import time

# =========================================================
# MBTI 专业人格测试 ——  Streamlit 应用
# 核心逻辑：4 大维度二分法 | 行业默认判定规则 | 80 题完整版
# =========================================================

# ----------------------
# 1. 全局页面配置
# ----------------------
st.set_page_config(
    page_title="🔮 MBTI 专业测试",
    layout="wide",                # 宽屏展示，更舒适
    initial_sidebar_state="collapsed"  # 收起侧边栏，界面更简洁
)

# 导入外部配置：题库、选项、计分映射、人格名称字典
from Q_mbti2 import question_file, answer_file, score_map, mbti_names

# ----------------------
# 2. 页面标题与说明
# ----------------------
st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <h1>🔮 专业MBTI人格测试</h1>
    <div style="color:#666; font-size:16px; margin:10px 0 20px;">
        📝 共 80 道题目 | 无对错之分 | 请根据真实想法选择
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------
# 3. 题目顺序随机化（仅执行一次）
# ----------------------
if "question_keys" not in st.session_state:
    # 首次进入页面：打乱题目顺序并保存
    question_keys = list(question_file.keys())
    random.shuffle(question_keys)
    st.session_state["question_keys"] = question_keys
else:
    # 已存在顺序：直接读取，防止刷新重排
    question_keys = st.session_state["question_keys"]

# ----------------------
# 4. 题目展示 + 答案收集（Form 表单，无刷新体验）
# ----------------------
answers = {}

st.markdown('<div style="text-align:center; max-width:800px; margin:0 auto;">', unsafe_allow_html=True)
with st.form("mbti_form", clear_on_submit=False):
    # 渲染所有题目
    for key in question_keys:
        ans = st.radio(
            label=question_file[key],
            options=answer_file,
            horizontal=True,
            label_visibility="visible"
        )
        answers[key] = ans

    # 提交按钮
    submit_btn = st.form_submit_button(
        "✅ 完成答题，开始匹配人格",
        use_container_width=True,
        type="secondary"
    )

# ----------------------
# 5. 计算 8 个倾向维度得分
# ----------------------
E = I = S = N = T = F = J = P = 0

for key in answers:
    dim = key.split("_")[0]
    s = score_map[answers[key]]

    if dim == "E": E += s
    if dim == "I": I += s
    if dim == "S": S += s
    if dim == "N": N += s
    if dim == "T": T += s
    if dim == "F": F += s
    if dim == "J": J += s
    if dim == "P": P += s

# ----------------------
# 6. 维度判定（行业标准规则）
# 分数相等时默认取：I / N / F / P
# ----------------------
ei = "E" if E > I else "I"
sn = "S" if S > N else "N"
tf = "T" if T > F else "F"
jp = "J" if J > P else "P"

mbti = ei + sn + tf + jp

# ----------------------
# 7. 加载动画效果
# ----------------------
def show_loading_animation():
    loading_text = st.empty()
    progress_bar = st.progress(0)

    loading_text.info("正在匹配你的人格类型...")
    for i in range(101):
        progress_bar.progress(i)
        time.sleep(0.03)
    time.sleep(0.5)

    loading_text.empty()
    progress_bar.empty()

# ----------------------
# 8. 结果展示
# ----------------------
if submit_btn:
    show_loading_animation()
    st.balloons()

    # 美观化结果展示
    st.markdown(f"""
    <div style="text-align:center; margin:20px 0;">
        <h3>🎉 匹配完成</h3>
        <h1 style="color:#2196F3; font-weight:bold;">【{mbti}】</h1>
        <h2 style="color:#4CAF50;">{mbti_names[mbti]}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.success(f"✅ 你的最终MBTI类型：【{mbti}】{mbti_names[mbti]}")