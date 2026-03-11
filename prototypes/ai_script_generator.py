import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_tools import AITools

class AIScriptGenerator:
    SYSTEM_PROMPT = """你是一个专业的短视频探店脚本专家，专门为抖音等短视频平台创作探店内容。

你的核心能力：
1. 创作具有"黄金3秒开头"的爆款脚本，快速抓住用户注意力
2. 挖掘用户痛点，引发共鸣
3. 设计反转点，制造惊喜感
4. 写出强CTA（Call To Action）引导，提升转化

脚本结构要求：
- 黄金3秒开头（Hook）：用悬念、争议或惊人事实抓住眼球
- 痛点挖掘：指出用户日常生活中遇到的问题
- 反转点：展示门店的独特亮点，让用户意外
- CTA引导：明确告诉用户下一步做什么（点赞、关注、点击链接等）

风格要求：
- 语言口语化、接地气
- 情绪价值拉满，让观众产生共鸣
- 符合抖音算法偏好（高停留、高互动）
- 适当使用emoji增加趣味性

请直接输出脚本内容，不要有多余的解释。"""

    def __init__(self, api_key=None, model="qwen-turbo"):
        self.ai_tools = AITools(api_key)
        self.model = model
    
    def generate_script(self, store_name, store_type, features, target_audience, tone="幽默风趣", model=None):
        prompt = f"""请为以下门店生成一个{tone}风格的抖音探店脚本：

门店名称：{store_name}
门店类型：{store_type}
特色/卖点：{features}
目标人群：{target_audience}

请按照以下结构生成脚本：
1. 黄金3秒开头（Hook）
2. 痛点挖掘
3. 反转点
4. CTA引导
5. 标签建议

要求：
- 语言生动有趣，符合短视频传播特点
- 能够引发用户共鸣和互动
- 引导用户到店消费"""

        return self.ai_tools.generate_content(prompt, system_prompt=self.SYSTEM_PROMPT, model=model or self.model)
    
    def generate_from_template(self, template_type, store_info):
        if template_type == "火锅":
            return self._generate_hotpot_script(store_info)
        elif template_type == "烧烤":
            return self._generate_bbq_script(store_info)
        elif template_type == "日料":
            return self._generate_japanese_script(store_info)
        elif template_type == "川菜":
            return self._generate_sichuan_script(store_info)
        else:
            return self.generate_script(
                store_info.get("name", ""),
                store_info.get("type", ""),
                store_info.get("features", ""),
                store_info.get("audience", "年轻人")
            )
    
    def _generate_hotpot_script(self, store_info):
        name = store_info.get("name", "火锅店")
        features = store_info.get("features", "锅底香、菜品新鲜")
        
        prompt = f"""请为{name}生成一个火锅探店脚本，突出以下特点：{features}

要求：
1. 黄金3秒：制造悬念，比如"北京最好吃的火锅居然是这家？"
2. 痛点：排队久、价格贵、味道一般等常见问题
3. 反转：展示这家店的独特优势
4. CTA：引导领取优惠券、到店打卡"""

        return self.ai_tools.generate_content(prompt, system_prompt=self.SYSTEM_PROMPT)
    
    def _generate_bbq_script(self, store_info):
        name = store_info.get("name", "烧烤店")
        prompt = f"""请为{name}生成一个烧烤探店脚本。

要求：
1. 黄金3秒：用"深夜放毒"或者"烧烤才是中国人的深夜食堂"开场
2. 痛点：深夜想吃东西但不知道去哪
3. 反转：展示烤串的香气和氛围
4. CTA：引导到店尝试"""

        return self.ai_tools.generate_content(prompt, system_prompt=self.SYSTEM_PROMPT)
    
    def _generate_japanese_script(self, store_info):
        name = store_info.get("name", "日料店")
        prompt = f"""请为{name}生成一个日料探店脚本，突出日料的精致和高品质。

要求：
1. 黄金3秒：用"人均100吃出1000的高级感"或"这家日料让我穿越东京"
2. 痛点：日料太贵不敢进
3. 反转：展示超高性价比
4. CTA：引导预约品尝"""

        return self.ai_tools.generate_content(prompt, system_prompt=self.SYSTEM_PROMPT)
    
    def _generate_sichuan_script(self, store_info):
        name = store_info.get("name", "川菜馆")
        prompt = f"""请为{name}生成一个川菜探店脚本，突出川菜的麻辣鲜香。

要求：
1. 黄金3秒：用"这才是正宗川菜的味道"或"辣到起飞但根本停不下来"
2. 痛点：怕太辣不敢尝试
3. 反转：展示香而不辣、辣而不燥的特点
4. CTA：引导到店挑战"""

        return self.ai_tools.generate_content(prompt, system_prompt=self.SYSTEM_PROMPT)


if __name__ == "__main__":
    generator = AIScriptGenerator(api_key="sk-7f7393fa2df44cfdabd40561651179f1")
    
    store_info = {
        "name": "海底捞火锅",
        "type": "火锅",
        "features": "服务好、24小时营业",
        "audience": "年轻人、朋友聚会"
    }
    
    script = generator.generate_script(
        store_name=store_info["name"],
        store_type=store_info["type"],
        features=store_info["features"],
        target_audience=store_info["audience"]
    )
    
    print("=== 生成的探店脚本 ===")
    print(script)
