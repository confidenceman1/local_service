import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_tools import AITools

class AIMarketingGenerator:
    XIAOHONGSHU_SYSTEM_PROMPT = """你是一个小红书爆款文案专家，专门为本地生活商家创作小红书种草内容。

你的核心能力：
1. 创作具有高情绪价值的种草文案
2. 善用emoji和符号增加视觉效果
3. 结构清晰，重点突出
4. 引发用户共鸣和互动

文案结构要求（小红书风格）：
- 开头：用痛点/悬念/推荐抓住注意力
- 亮点：分点列出门店的核心优势
- 细节：加入具体的体验描述
- 小Tips：提供实用的建议
- 互动引导：引导评论、收藏

风格要求：
- 语气亲切自然，像朋友推荐
- 善用emoji和符号（✅、🔴、✨等）
- 适当使用小红书热门话题标签
- 文字量适中，段落分明

请直接输出文案内容，不要有多余的解释。"""

    DOUYIN_SYSTEM_PROMPT = """你是一个抖音爆款文案专家，专门为本地生活商家创作抖音短视频文案。

你的核心能力：
1. 创作具有强节奏感的短视频文案
2. 快速抓住用户注意力（3秒原则）
3. 制造悬念和反转
4. 强CTA引导互动

文案结构要求（抖音风格）：
- 开头：用悬念/争议/惊人事实抓住眼球
- 核心：突出门店最吸引人的1-2个亮点
- CTA：明确告诉用户做什么（点击、评论、收藏等）

风格要求：
- 语言简短有力，节奏感强
- 适当使用emoji
- 话题标签要精准
- 符合抖音算法偏好

请直接输出文案内容，不要有多余的解释。"""

    def __init__(self, api_key=None, model="qwen-turbo"):
        self.ai_tools = AITools(api_key)
        self.model = model
    
    def generate_xiaohongshu(self, store_name, store_type, features, promotion, atmosphere, address, model=None):
        prompt = f"""请为以下商家生成一篇小红书种草文案：

门店名称：{store_name}
门店类型：{store_type}
特色/卖点：{features}
促销活动：{promotion}
氛围描述：{atmosphere}
地址：{address}

请按照小红书风格生成文案，包含：
1. 吸引人的开头（用emoji开头）
2. 亮点推荐（用✅或▫️符号分点）
3. 消费信息
4. 小Tips
5. 互动引导
6. 热门话题标签（#店名 #城市+美食 #类型 #打卡）"""

        return self.ai_tools.generate_content(prompt, system_prompt=self.XIAOHONGSHU_SYSTEM_PROMPT, model=model or self.model)
    
    def generate_douyin(self, store_name, store_type, features, promotion, atmosphere, address, model=None):
        prompt = f"""请为以下商家生成一条抖音短视频文案：

门店名称：{store_name}
门店类型：{store_type}
特色/卖点：{features}
促销活动：{promotion}
氛围描述：{atmosphere}
地址：{address}

请按照抖音风格生成文案，要求：
1. 黄金3秒开头（制造悬念或用感叹句）
2. 突出1-2个最吸引人的亮点
3. 明确告诉用户"为什么值得去"
4. 强CTA引导（点赞、关注、点击链接等）
5. 热门话题标签
6. 简洁有力，符合短视频节奏"""

        return self.ai_tools.generate_content(prompt, system_prompt=self.DOUYIN_SYSTEM_PROMPT, model=model or self.model)
    
    def generate(self, store_name, store_type, features, promotion, atmosphere, address, platform="小红书", model=None):
        if platform == "小红书":
            return self.generate_xiaohongshu(store_name, store_type, features, promotion, atmosphere, address, model=model)
        else:
            return self.generate_douyin(store_name, store_type, features, promotion, atmosphere, address, model=model)


if __name__ == "__main__":
    generator = AIMarketingGenerator()
    
    store_info = {
        "name": "海底捞火锅",
        "type": "火锅",
        "features": "服务好、24小时营业、免费美甲擦鞋",
        "promotion": "新客8折，会员积分抵现",
        "atmosphere": "现代时尚，适合朋友聚会",
        "address": "王府井大街138号"
    }
    
    print("=== 小红书风格 ===")
    xiaohongshu = generator.generate_xiaohongshu(
        store_info["name"], store_info["type"], store_info["features"],
        store_info["promotion"], store_info["atmosphere"], store_info["address"]
    )
    print(xiaohongshu)
    print("\n" + "="*50 + "\n")
    
    print("=== 抖音风格 ===")
    douyin = generator.generate_douyin(
        store_info["name"], store_info["type"], store_info["features"],
        store_info["promotion"], store_info["atmosphere"], store_info["address"]
    )
    print(douyin)
