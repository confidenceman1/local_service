import streamlit as st
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'prototypes'))

from ai_script_generator import AIScriptGenerator
from ai_marketing_generator import AIMarketingGenerator
from ai_food_recommender import AIFoodRecommender

st.set_page_config(
    page_title="本地生活服务 AI 原生原型",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2C3E50;
        margin-top: 1rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
        border-left: 4px solid #FF6B6B;
    }
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #FF5252, #3DBDB5);
    }
    .sidebar-content {
        background-color: #fafafa;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header">🍜 本地生活服务 AI 原生原型</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("🔧 功能导航")
        
        st.markdown("---")
        
        selected = st.radio(
            "选择功能模块",
            ["🏠 首页", "🎬 AI探店脚本", "📝 营销文案", "🍜 美食推荐", "🖼️ 图片美化"]
        )
        
        st.markdown("---")
        
        st.markdown("### 💡 关于项目")
        st.info("""
        本项目是一个基于 LLM 的本地生活服务 AI 原型
        
        **核心功能：**
        - AI 探店脚本生成
        - 商家营销文案创作
        - LBS 美食推荐（支持PostgreSQL数据库）
        
        **数据库配置（环境变量）：**
        - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
        """)
        
        st.markdown("### ⚙️ 设置")
        
        api_key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("OPENAI_API_KEY")
        model = st.selectbox("选择模型", ["qwen-turbo", "qwen-plus", "qwen-max"], index=0)
        
        if api_key:
            st.session_state["api_key"] = api_key
            st.session_state["model"] = model
            st.success("API Key 已配置 ✅")
        else:
            st.warning("请设置环境变量 DASHSCOPE_API_KEY")
    
    if selected == "🏠 首页":
        show_homepage()
    elif selected == "🎬 AI探店脚本":
        show_script_generator()
    elif selected == "📝 营销文案":
        show_marketing_generator()
    elif selected == "🍜 美食推荐":
        show_food_recommender()
    elif selected == "🖼️ 图片美化":
        show_image_enhancer()


def show_homepage():
    st.markdown("""
    ## 🎯 项目介绍
    
    本原型旨在展示 **AI 在本地生活服务场景** 中的应用价值，解决商家营销成本高、达人创作效率低、用户搜索链路长的问题。
    
    ### 🚀 核心功能
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎬 AI 探店脚本</h3>
            <p>预设抖音爆款脚本模板，黄金3秒开头 + 痛点挖掘 + 反转点 + CTA引导</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 营销文案引擎</h3>
            <p>支持小红书和抖音双平台风格切换，热门话题标签智能推荐</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🍜 LBS 美食推荐</h3>
            <p>语义化理解用户需求，基于 Mock 数据智能匹配餐厅</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 用户路径")
    
    st.markdown("""
    ```
    流量端： 短视频内容驱动 → 搜索意图触发
    ↓
    转化端： POI详情页 → 优惠券/预约 → 到店核销
    ↓
    AI赋能： 极速产出高质量营销素材，缩短用户从"看到"到"下单"的思考时长
    ```
    """)
    
    st.markdown("""
    ### 🎨 技术栈
    - **框架：** Streamlit
    - **语言：** Python 3.10+
    - **模型：** GPT-4o / Claude 3.5 Sonnet
    - **数据：** Mock POI 数据
    """)


def show_script_generator():
    st.markdown("## 🎬 AI 探店脚本生成器")
    st.markdown("输入门店信息，自动生成具有爆款潜力的抖音探店脚本")
    
    with st.expander("📖 使用说明", expanded=False):
        st.info("""
        **脚本结构：**
        1. 黄金3秒开头 - 快速抓住用户注意力
        2. 痛点挖掘 - 引发用户共鸣
        3. 反转点 - 制造惊喜感
        4. CTA引导 - 提升转化
        """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📝 门店信息")
        
        store_name = st.text_input("门店名称", placeholder="例如：海底捞火锅")
        store_type = st.selectbox(
            "门店类型",
            ["火锅", "烧烤", "日料", "川菜", "粤菜", "本帮菜", "串串", "湘菜", "其他"]
        )
        
        features = st.text_area(
            "特色/卖点",
            placeholder="例如：服务好、24小时营业、免费美甲擦鞋",
            height=100
        )
        
        target_audience = st.multiselect(
            "目标人群",
            ["年轻人", "朋友聚会", "情侣约会", "家庭聚餐", "学生党", "白领", "游客"]
        )
        
        tone = st.select_slider(
            "文案风格",
            options=["幽默风趣", "专业严谨", "情感共鸣", "种草推荐", "搞笑整活"],
            value="幽默风趣"
        )
        
        generate_btn = st.button("🚀 生成脚本", use_container_width=True)
    
    with col2:
        st.markdown("### 📄 生成的脚本")
        
        if generate_btn:
            if not store_name:
                st.warning("请输入门店名称")
            else:
                with st.spinner("AI 正在生成探店脚本..."):
                    api_key = st.session_state.get("api_key")
                    model = st.session_state.get("model", "qwen-turbo")
                    generator = AIScriptGenerator(api_key)
                    
                    audience_str = "、".join(target_audience) if target_audience else "年轻人"
                    
                    script = generator.generate_script(
                        store_name=store_name,
                        store_type=store_type,
                        features=features,
                        target_audience=audience_str,
                        tone=tone,
                        model=model
                    )
                    
                    st.markdown('<div class="success-box">✅ 脚本生成成功！</div>', unsafe_allow_html=True)
                    st.markdown(script)
                    
                    st.markdown("---")
                    col_copy, col_download = st.columns(2)
                    with col_copy:
                        st.code(script, language="markdown")
                    with col_download:
                        pass
        else:
            st.info("👈 请在左侧填写门店信息，点击生成按钮")


def show_marketing_generator():
    st.markdown("## 📝 商家营销文案引擎")
    st.markdown("为商家生成适配小红书/抖音风格的营销文案")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📝 商家信息")
        
        store_name = st.text_input("商家名称", placeholder="例如：海底捞火锅")
        store_type = st.selectbox(
            "商家类型",
            ["火锅", "烧烤", "日料", "川菜", "粤菜", "本帮菜", "串串", "湘菜", "咖啡厅", "甜品店", "其他"]
        )
        
        features = st.text_area(
            "特色/卖点",
            placeholder="例如：服务好、食材新鲜、性价比高",
            height=100
        )
        
        promotion = st.text_input(
            "促销活动",
            placeholder="例如：新客8折、满100减20",
        )
        
        atmosphere = st.text_input(
            "门店氛围",
            placeholder="例如：现代时尚、温馨舒适、复古怀旧",
        )
        
        address = st.text_input("地址", placeholder="例如：王府井大街138号")
        
        platform = st.radio(
            "选择平台",
            ["小红书", "抖音"]
        )
        
        generate_btn = st.button("🚀 生成文案", use_container_width=True)
    
    with col2:
        st.markdown("### 📄 生成的文案")
        
        if generate_btn:
            if not store_name:
                st.warning("请输入商家名称")
            else:
                with st.spinner("AI 正在生成营销文案..."):
                    api_key = st.session_state.get("api_key")
                    model = st.session_state.get("model", "qwen-turbo")
                    generator = AIMarketingGenerator(api_key)
                    
                    if platform == "小红书":
                        result = generator.generate_xiaohongshu(
                            store_name, store_type, features, promotion, atmosphere, address, model=model
                        )
                    else:
                        result = generator.generate_douyin(
                            store_name, store_type, features, promotion, atmosphere, address, model=model
                        )
                    
                    st.markdown('<div class="success-box">✅ 文案生成成功！</div>', unsafe_allow_html=True)
                    st.markdown(result)
                    
                    st.markdown("---")
                    st.code(result, language="markdown")
        else:
            st.info("👈 请在左侧填写商家信息，点击生成按钮")


def show_food_recommender():
    st.markdown("## 🍜 LBS 美食推荐助手")
    st.markdown("基于语义化理解，为你推荐附近美食")
    
    with st.expander("📖 功能说明", expanded=False):
        st.info("""
        **推荐逻辑：**
        1. 用户选择城市、位置、口味偏好和用餐时段
        2. 系统从 Mock 数据中筛选符合条件的餐厅
        3. AI 根据语义匹配度生成个性化推荐
        
        **数据来源：** 模拟高德/抖音 POI 接口
        """)
    
    col1, col2 = st.columns([1, 2])
    
    recommender = AIFoodRecommender(None, "qwen-turbo")
    
    with col1:
        st.markdown("### 🎯 搜索条件")
        
        city = st.selectbox(
            "选择城市",
            recommender.get_cities()
        )
        
        if city:
            location = st.selectbox(
                "所在区域",
                recommender.get_locations(city)
            )
        
        category = st.selectbox(
            "选择菜系",
            ["", "火锅", "烧烤", "日料", "川菜", "粤菜", "本帮菜", "串串", "湘菜", "早茶", "煲仔饭"]
        )
        
        flavor = st.selectbox(
            "口味偏好",
            ["", "辣", "鲜", "甜", "酸", "清淡", "重口"]
        )
        
        time_slot = st.selectbox(
            "用餐时段",
            recommender.get_time_slots()
        )
        
        search_btn = st.button("🔍 开始推荐", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🔍 语义搜索")
        semantic_query = st.text_input("用自然语言描述你的需求", placeholder="例如：适合情侣约会的浪漫餐厅")
        semantic_btn = st.button("🎯 语义搜索")
    
    with col2:
        st.markdown("### 🍽️ 推荐结果")
        
        if search_btn:
            with st.spinner("AI 正在为你推荐美食..."):
                api_key = st.session_state.get("api_key")
                model = st.session_state.get("model", "qwen-turbo")
                recommender = AIFoodRecommender(api_key, model)
                
                result = recommender.recommend(
                    city=city,
                    location=location or "市中心",
                    category=category,
                    flavor=flavor,
                    time_slot=time_slot
                )
                
                st.markdown('<div class="success-box">✅ 推荐生成成功！</div>', unsafe_allow_html=True)
                st.markdown(result)
        
        elif semantic_btn and semantic_query:
            with st.spinner("AI 正在理解你的需求..."):
                api_key = st.session_state.get("api_key")
                model = st.session_state.get("model", "qwen-turbo")
                recommender = AIFoodRecommender(api_key, model)
                
                result = recommender.semantic_search(semantic_query, city or "北京")
                
                st.markdown('<div class="success-box">✅ 搜索完成！</div>', unsafe_allow_html=True)
                st.markdown(result)
        else:
            st.info("👈 请选择搜索条件，点击开始推荐")
            
            st.markdown("---")
            st.markdown("### 💡 示例推荐")
            
            if city:
                with st.spinner("加载示例数据..."):
                    api_key = st.session_state.get("api_key")
                    model = st.session_state.get("model", "qwen-turbo")
                    recommender = AIFoodRecommender(api_key, model)
                    
                    example_result = recommender.recommend(
                        city=city,
                        location="市中心",
                        category="火锅",
                        flavor="鲜",
                        time_slot="晚餐"
                    )
                    st.markdown(example_result)


def show_image_enhancer():
    """图片美化工具"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'prototypes'))
    from image_enhancer import get_enhancer
    
    st.markdown("""
    ## 🖼️ 商户图片美化工具
    
    上传商品图片，AI自动美化，适合餐饮商家展示菜品
    """)
    
    # 功能选择
    st.markdown("### 📸 选择功能")
    func_option = st.radio(
        "功能",
        ["🍽️ 美食增强", "🔲 背景去除", "🎨 风格化"],
        horizontal=True
    )
    
    # 上传图片
    st.markdown("### 📤 上传图片")
    uploaded_file = st.file_uploader(
        "选择图片文件",
        type=['jpg', 'jpeg', 'png', 'webp'],
        help="支持 jpg, png, webp 格式"
    )
    
    if uploaded_file:
        # 保存上传的图片
        import tempfile
        import shutil
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, uploaded_file.name)
        output_path = os.path.join(temp_dir, f"output_{uploaded_file.name}")
        
        # 保存上传文件
        with open(input_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # 显示原图
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📷 原图")
            st.image(input_path, use_container_width=True)
        
        # 处理选项
        enhance_type = "food"
        style = "food_gourmet"
        
        if func_option == "🍽️ 美食增强":
            st.markdown("#### ✨ 美食增强")
            enhance_type = st.select_slider(
                "增强类型",
                options=["food", "general", "quality"],
                format_func=lambda x: {"food": "🍽️ 美食增强", "general": "🌟 通用增强", "quality": "🔍 画质提升"}[x],
                value="food"
            )
        elif func_option == "🔲 背景去除":
            st.markdown("#### ✨ 背景去除")
            st.info("去除图片背景，突出商品主体，适合菜单制作")
        elif func_option == "🎨 风格化":
            st.markdown("#### ✨ 风格化")
            style = st.select_slider(
                "风格",
                options=["food_gourmet", "anime", "oil_painting"],
                format_func=lambda x: {"food_gourmet": "🍜 美食风格", "anime": "🎌 动漫风格", "oil_painting": "🖼️ 油画风格"}[x],
                value="food_gourmet"
            )
        
        # 处理按钮
        if st.button("🚀 开始处理", type="primary"):
            with st.spinner("AI 正在处理图片..."):
                enhancer = get_enhancer(st.session_state.get("api_key"))
                
                if func_option == "🍽️ 美食增强":
                    success, result = enhancer.enhance_image(input_path, output_path, enhance_type)
                elif func_option == "🔲 背景去除":
                    success, result = enhancer.remove_background(input_path, output_path)
                else:
                    success, result = enhancer.stylize_image(input_path, output_path, style)
                
                if success:
                    with col2:
                        st.markdown("#### ✨ 处理结果")
                        st.image(output_path, use_container_width=True)
                        
                        # 下载按钮
                        with open(output_path, 'rb') as f:
                            st.download_button(
                                label="📥 下载图片",
                                data=f.read(),
                                file_name=f"enhanced_{uploaded_file.name}",
                                mime=uploaded_file.type
                            )
                else:
                    st.error(f"处理失败: {result}")
        
        # 清理临时文件
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    else:
        st.info("👆 请上传图片文件开始处理")
        
        # 示例
        st.markdown("---")
        st.markdown("### 💡 使用场景")
        st.markdown("""
        - **餐饮商家**: 菜品照片美化，让食物看起来更诱人
        - **菜单制作**: 去除背景，制作专业菜单
        - **外卖平台**: 菜品图片优化，提升下单率
        - **社交媒体**: 一键风格化，发朋友圈更吸睛
        """)


if __name__ == "__main__":
    main()
