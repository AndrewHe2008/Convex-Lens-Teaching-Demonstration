import math
import streamlit as st
import matplotlib.pyplot as plt

# 字体配置保留，不影响英文渲染
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ========== 页面配置 ==========
st.set_page_config(page_title="凸透镜成像动态演示", layout="wide")
st.title("🔍 凸透镜成像规律 动态演示")
st.markdown("基于几何光学公式：$\\frac{1}{f} = \\frac{1}{u} + \\frac{1}{v}$，其中 $f$ 为焦距，$u$ 为物距，$v$ 为像距")

# ========== 侧边栏参数控制 ==========
with st.sidebar:
    st.header("⚙️ 参数调节")
    f = st.slider("焦距 f (cm)", min_value=5.0, max_value=30.0, value=10.0, step=0.5)
    u = st.slider("物距 u (cm)", min_value=1.0, max_value=60.0, value=25.0, step=0.5)
    h_object = st.slider("物体高度 (cm)", min_value=2.0, max_value=15.0, value=8.0, step=0.5)
    show_light = st.checkbox("显示光路图", value=True)
    show_label = st.checkbox("显示标注", value=True)

# ========== 核心计算 ==========
if abs(u - f) < 1e-6:
    v = float('inf')
    m = float('-inf')
    image_type = "不成像（折射光线平行射出）"
else:
    v = 1 / (1/f - 1/u)
    m = -v / u
    abs_m = abs(m)

    if u > 2*f:
        image_type = "倒立、缩小、实像"
    elif abs(u - 2*f) < 1e-6:
        image_type = "倒立、等大、实像"
    elif f < u < 2*f:
        image_type = "倒立、放大、实像"
    elif u < f:
        image_type = "正立、放大、虚像"

# ========== 绘图（图内全英文标注，彻底规避乱码） ==========
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

x_min = -55
x_max = 55
y_min = -20
y_max = 20
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

# 1. 主光轴
ax.axhline(y=0, color='black', linewidth=1, zorder=1)
ax.text(x_max-2, -1.2, "Principal axis", fontsize=9)

# 2. 凸透镜
lens_height = 18
ax.plot([0, 0], [-lens_height, lens_height], color='red', linewidth=3, zorder=2)
ax.plot([0, -1], [lens_height, lens_height-2], color='red', linewidth=2)
ax.plot([0, 1], [lens_height, lens_height-2], color='red', linewidth=2)
ax.plot([0, -1], [-lens_height, -lens_height+2], color='red', linewidth=2)
ax.plot([0, 1], [-lens_height, -lens_height+2], color='red', linewidth=2)
ax.text(0.5, lens_height-1, "Convex lens", color='red', fontsize=10)

# 3. 焦点与2倍焦距点
points = [
    (-f, 0, "F"),
    (f, 0, "F"),
    (-2*f, 0, "2F"),
    (2*f, 0, "2F")
]
for px, py, label in points:
    if x_min < px < x_max:
        ax.scatter(px, py, color='blue', s=30, zorder=3)
        if show_label:
            ax.text(px, -1.5, label, ha='center', fontsize=9, color='blue')

# 4. 物体
obj_x = -u
obj_y_top = h_object
ax.arrow(obj_x, 0, 0, h_object*0.98, head_width=1, head_length=1.2,
         fc='orange', ec='orange', linewidth=2, zorder=4)
if show_label:
    ax.text(obj_x, h_object+1, "Object", ha='center', color='orange', fontsize=10)

# 5. 光线与像
if v == float('inf'):
    if show_light:
        ax.plot([obj_x, 0], [obj_y_top, obj_y_top], color='green', linestyle='-', linewidth=1.5)
        ax.plot([0, x_max], [obj_y_top, obj_y_top], color='green', linestyle='--', linewidth=1.5)
        ax.plot([obj_x, x_max], [obj_y_top, obj_y_top * (x_max / obj_x)], color='purple', linewidth=1.5)
else:
    img_x = v
    img_y_top = m * h_object

    if show_light:
        ax.plot([obj_x, 0], [obj_y_top, obj_y_top], color='green', linewidth=1.5)
        if u > f:
            ax.plot([0, img_x], [obj_y_top, img_y_top], color='green', linewidth=1.5)
        else:
            ax.plot([0, x_max], [obj_y_top, obj_y_top + (obj_y_top / f) * (x_max - 0)], color='green', linewidth=1.5)
            ax.plot([0, img_x], [obj_y_top, img_y_top], color='green', linestyle='--', linewidth=1)

        if u > f:
            ax.plot([obj_x, img_x], [obj_y_top, img_y_top], color='purple', linewidth=1.5)
        else:
            ax.plot([obj_x, x_max], [obj_y_top, obj_y_top * (x_max / obj_x)], color='purple', linewidth=1.5)
            ax.plot([img_x, 0], [img_y_top, 0], color='purple', linestyle='--', linewidth=1)

    if u > f:
        ax.arrow(img_x, 0, 0, img_y_top*0.98, head_width=1, head_length=1.2,
                 fc='steelblue', ec='steelblue', linewidth=2, zorder=4)
        if show_label:
            ax.text(img_x, img_y_top-2, "Real image", ha='center', color='steelblue', fontsize=10)
    else:
        ax.arrow(img_x, 0, 0, img_y_top*0.98, head_width=1, head_length=1.2,
                 fc='steelblue', ec='steelblue', linewidth=2, linestyle='--', zorder=4)
        if show_label:
            ax.text(img_x, img_y_top+1, "Virtual image", ha='center', color='steelblue', fontsize=10)

ax.scatter(0, 0, color='black', s=20, zorder=5)
if show_label:
    ax.text(0.5, 1, "O", fontsize=10, color='black')

ax.set_title("Convex Lens Imaging Diagram", fontsize=12)
ax.set_xlabel("Distance (cm)", fontsize=10)
ax.set_ylabel("Height (cm)", fontsize=10)

# ========== 右侧结果展示 ==========
col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(fig)

with col2:
    st.subheader("📐 计算结果")
    st.metric("焦距 f", f"{f:.2f} cm")
    st.metric("物距 u", f"{u:.2f} cm")
    
    if v == float('inf'):
        st.metric("像距 v", "无穷大")
        st.metric("放大率", "无意义")
    else:
        st.metric("像距 v", f"{v:.2f} cm")
        st.metric("放大率 |m|", f"{abs(m):.2f} 倍")
    
    st.divider()
    st.subheader("📌 成像性质")
    st.success(image_type)
    
    st.divider()
    st.subheader("📚 规律总结")
    if u > 2*f:
        st.info("应用：照相机、人眼")
    elif abs(u - 2*f) < 1e-6:
        st.info("应用：精确测焦距")
    elif f < u < 2*f:
        st.info("应用：投影仪、幻灯机")
    elif abs(u - f) < 1e-6:
        st.info("应用：平行光源")
    elif u < f:
        st.info("应用：放大镜")

        st.info("应用：平行光源")
    elif u < f:
        st.info("应用：放大镜")
