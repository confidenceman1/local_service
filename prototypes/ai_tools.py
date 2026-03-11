import os

class AITools:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('DASHSCOPE_API_KEY') or os.environ.get('OPENAI_API_KEY')
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.model = "qwen-turbo"
    
    def generate_content(self, prompt, system_prompt=None, model=None, max_tokens=1500):
        import requests
        
        if system_prompt is None:
            system_prompt = "你是一个本地生活服务领域的AI助手，擅长生成探店脚本、营销文案和美食推荐。生成的文案必须具备情绪价值和强交互感，符合抖音推流算法（高停留时长、高互动）。"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": model or self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.8
        }
        
        try:
            url = f"{self.base_url}/chat/completions"
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 401:
                print(f"认证失败 - 请检查API Key是否正确，是否已开通百炼服务")
                print(f"响应内容: {response.text}")
            elif response.status_code != 200:
                print(f"API错误 {response.status_code}: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"API调用错误: {e}")
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        if "探店脚本" in prompt:
            return self._mock_script(prompt)
        elif "小红书" in prompt:
            return self._mock_xiaohongshu(prompt)
        elif "抖音" in prompt and "文案" in prompt:
            return self._mock_douyin_copy(prompt)
        elif "推荐" in prompt or "美食" in prompt:
            return self._mock_recommendation(prompt)
        else:
            return "内容生成中...\n\n请设置有效的API密钥以获得完整的AI生成内容。"
    
    def _mock_script(self, prompt):
        return """# 🎬 AI探店脚本

## 📍 门店：海底捞火锅(王府井店)

---

### 🎯 黄金3秒开头（钩子）
"朋友来北京问我最推荐什么火锅？我说除了海底捞还能有谁？！今天带你们体验一下这家传说中服务天花板的火锅店！"

---

### 😱 痛点挖掘
"每次排队都要等一两个小时，但你知道吗？提前用小程序排队，到店直接入座！还有免费美甲、擦鞋服务，这待遇也太夸张了吧！"

---

### 🔄 反转点
"本来以为这种网红店味道一般，结果锅底一开，那香味直接把我整饿了！他们家的毛肚和虾滑真的是一绝，超级新鲜！"

---

### 🛒 CTA引导（行动号召）
"想要同款体验的宝子们，点击下方链接领取新人优惠券！记得提前排队哦～ 地址我放在评论区啦！"

---

### 📝 标签建议
#北京美食 #海底捞 #网红火锅 #探店打卡 #美食推荐
"""
    
    def _mock_xiaohongshu(self, prompt):
        return """📍 【店名】海底捞火锅王府井店

姐妹们！今天必须给你们安利这家宝藏火锅店！🔥

✨ 亮点推荐：
▫️ 服务真的绝！从进门到坐下，全程微笑服务
▫️ 菜品新鲜，毛肚虾滑必点！
▫️ 免费美甲+擦鞋，这待遇也太香了吧
▫️ 凌晨2点还营业，夜宵党狂喜！

💰 消费：人均120元左右

📍 地址：王府井大街138号

💬 小Tips：
提前用小程序排队！可以少等很久！

姐妹们快冲！评论区告诉我你们最爱海底捞的哪道菜！🙋‍♀️

#北京美食 #火锅推荐 #海底捞 #王府井 #美食探店 #北京周末去哪儿
"""
    
    def _mock_douyin_copy(self, prompt):
        return """🎬【北京必打卡火锅｜服务卷王海底捞】

🥘 锅底推荐：番茄锅+三鲜锅，经典搭配不会出错！

📍 位置：王府井大街138号

⏰ 营业时间：24小时营业

💰 人均：120元

🔥 亮点：
✅ 服务好到离谱！免费美甲擦鞋
✅ 菜品新鲜品质高
✅ 凌晨也能吃上热乎火锅
✅ 网红打卡地标

🎁 新人福利：点击头像领取优惠券！

评论区说说你最爱海底捞什么菜品？

#北京美食 #海底捞 #网红火锅 #探店 #美食推荐 #北京必吃
"""
    
    def _mock_recommendation(self, prompt):
        return """根据您的需求，为您推荐以下餐厅：

🏆 **强烈推荐**

**海底捞火锅(王府井店)** ⭐4.7
- 📍 距离：0.8km
- 💰 人均：120元
- 🏷️ 标签：服务好、排队王、24小时
- 📌 地址：王府井大街138号

**理由**：服务天花板的网红火锅店，适合朋友聚会、情侣约会，凌晨也能吃！

---

💡 **小贴士**：建议提前用小程序排队哦～
"""
