# 本地生活服务 AI 原型 - 技术实现手册 (Tech_Spec)

## 1. 技术栈选型

- **框架：** Streamlit (用于快速构建交互式 Web 原型)
- **语言：** Python 3.10+
- **模型：** Claude 3.5 Sonnet / GPT-4o (通过 API 调用)
- **逻辑控制：** Trae (Vibe Coding 核心环境)

## 2. 核心架构说明

**Frontend:** Streamlit 侧边栏进行参数配置，主界面展示生成内容。

**LLM Layer:** 预设三套核心 System Prompt，分别对应脚本、文案、推荐。

**Data Layer:** 使用静态字典模拟 POI 数据，包含：name, category, distance, rating, tags。

## 3. 关键逻辑

**Prompt Engineering:** 要求生成的文案必须具备"情绪价值"和"强交互感"。

**Workflow:**
1. 用户选择功能
2. 输入参数
3. 调用模型生成
4. 实时渲染

## 4. 核心功能模块

### 4.1 AI 探店脚本专家
- 预设抖音爆款脚本模板
- 黄金3秒开头 + 痛点挖掘 + 反转点 + CTA引导

### 4.2 商家营销文案引擎
- 支持小红书风格
- 支持抖音风格
- 热门话题标签

### 4.3 LBS 美食助手
- Mock POI 数据
- 语义化匹配
- 距离/评分/标签过滤
