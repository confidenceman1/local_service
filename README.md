# 本地生活服务 AI 原生原型

基于 LLM 的本地生活服务产品原型，展示 AI 在抖音等内容平台种草-决策-到店闭环中的应用价值。

## 🎯 项目背景

针对抖音等内容平台"种草-决策-到店"的闭环，利用 LLM 能力解决：
- 商家营销成本高
- 达人创作效率低
- 用户搜索链路长

## 🚀 核心功能

### 1. AI 探店脚本生成器
- 预设抖音爆款脚本模板
- 黄金3秒开头 + 痛点挖掘 + 反转点 + CTA引导
- 支持多种门店类型和风格

### 2. 商家营销文案引擎
- 支持小红书风格
- 支持抖音风格
- 热门话题标签智能推荐

### 3. LBS 美食推荐助手
- Mock POI 数据（5个城市，30+餐厅）
- 语义化匹配
- 距离/评分/标签过滤

## 🛠️ 技术栈

- **框架：** Streamlit
- **语言：** Python 3.10+
- **模型：** GPT-4o / Claude 3.5 Sonnet（通过 API 调用）
- **数据：** Mock POI 数据

## 📦 安装运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

## 📁 项目结构

```
local_service/
├── app.py                      # Streamlit 主应用
├── prototypes/
│   ├── ai_tools.py            # AI 工具基类
│   ├── ai_script_generator.py  # 探店脚本生成器
│   ├── ai_marketing_generator.py  # 营销文案引擎
│   ├── ai_food_recommender.py # 美食推荐助手
│   └── poi_data.py           # Mock POI 数据
├── PRD.md                     # 产品需求文档
├── Tech_Spec.md               # 技术实现手册
└── requirements.txt           # 依赖列表
```

## 📊 核心用户路径

```
流量端： 短视频内容驱动 → 搜索意图触发
转化端： POI详情页 → 优惠券/预约 → 到店核销
AI赋能： 极速产出高质量营销素材，缩短用户决策时间
```

## 🎨 使用说明

1. **AI 探店脚本**：输入门店名称、类型、特色卖点，选择目标人群和风格，一键生成爆款脚本
2. **营销文案**：选择平台（小红书/抖音），输入商家信息，生成适配的营销文案
3. **美食推荐**：选择城市、口味偏好，获取个性化餐厅推荐

## ⚙️ 配置

可选配置 OpenAI API Key 以获得更准确的 AI 生成内容：

```python
# 在 Streamlit 侧边栏输入 API Key
# 或者设置环境变量
export OPENAI_API_KEY=your_api_key
```

---

Let's Vibe Coding! 🚀
