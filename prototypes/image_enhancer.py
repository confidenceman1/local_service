"""
图片美化工具
使用阿里云百炼 qwen-image-2.0 系列模型
"""
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

class ImageEnhancer:
    """图片美化工具类"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('DASHSCOPE_API_KEY')
    
    def image_to_base64(self, image_path):
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def call_api(self, prompt, image_base64=None, task_type="image-edit"):
        """调用阿里云百炼图像API"""
        if not self.api_key:
            return None, "未配置API Key"
        
        try:
            url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 构建消息
            messages = [
                {
                    "role": "user",
                    "content": []
                }
            ]
            
            # 添加图片
            if image_base64:
                messages[0]["content"].append({
                    "image": f"data:image/jpeg;base64,{image_base64}"
                })
            
            # 添加提示词
            messages[0]["content"].append({
                "text": prompt
            })
            
            data = {
                "model": "qwen-image-2.0-pro",
                "input": {
                    "messages": messages
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                return result, None
            else:
                return None, f"API错误 {response.status_code}: {response.text[:300]}"
            
        except Exception as e:
            return None, f"调用失败: {str(e)}"
    
    def enhance_image(self, image_path, output_path=None, enhance_type="food"):
        """图像增强"""
        if not self.api_key:
            return False, "未配置API Key"
        
        try:
            image_base64 = self.image_to_base64(image_path)
            
            prompt_map = {
                "food": "请美化这张美食图片，让食物看起来更美味、更有光泽、提升食欲",
                "general": "请增强这张图片，提升画质、添加专业灯光效果，让照片更美观",
                "quality": "请提升这张图片的质量和清晰度，减少噪点，让画面更清晰"
            }
            
            prompt = prompt_map.get(enhance_type, prompt_map["food"])
            
            result, error = self.call_api(prompt, image_base64)
            
            if error:
                return False, error
            
            # 解析结果 - 图像在 choices[0].message.content[0].image
            if result and 'output' in result:
                content = result['output']['choices'][0]['message']['content']
                if isinstance(content, list) and len(content) > 0:
                    image_url = content[0].get('image')
                    if image_url:
                        # 下载图片
                        output_path = output_path or image_path.replace('.', f'_{enhance_type}.')
                        response = requests.get(image_url, timeout=60)
                        if response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(response.content)
                            return True, output_path
            
            return False, "无法解析API返回结果"
            
        except Exception as e:
            return False, f"处理失败: {str(e)}"
    
    def remove_background(self, image_path, output_path=None):
        """背景去除"""
        if not self.api_key:
            return False, "未配置API Key"
        
        try:
            image_base64 = self.image_to_base64(image_path)
            prompt = "请去除这张图片的背景，只保留主体，使背景变为透明"
            
            result, error = self.call_api(prompt, image_base64)
            
            if error:
                return False, error
            
            if result and 'output' in result:
                content = result['output']['choices'][0]['message']['content']
                if isinstance(content, list) and len(content) > 0:
                    image_url = content[0].get('image')
                    if image_url:
                        output_path = output_path or image_path.replace('.', '_nobg.')
                        response = requests.get(image_url, timeout=60)
                        if response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(response.content)
                            return True, output_path
            
            return False, "无法解析API返回结果"
            
        except Exception as e:
            return False, f"处理失败: {str(e)}"
    
    def stylize_image(self, image_path, output_path=None, style="food_gourmet"):
        """图像风格化"""
        if not self.api_key:
            return False, "未配置API Key"
        
        try:
            image_base64 = self.image_to_base64(image_path)
            
            style_prompts = {
                "food_gourmet": "把这张图片转换成专业美食摄影风格，精致的摆盘，影棚灯光，看起来像高级餐厅的菜品照片",
                "anime": "把这张图片转换成日本动漫风格，动漫艺术，鲜艳的色彩，干净的线条",
                "oil_painting": "把这张图片转换成油画风格，古典艺术，油画笔触，丰富的色彩"
            }
            
            prompt = style_prompts.get(style, style_prompts["food_gourmet"])
            
            result, error = self.call_api(prompt, image_base64)
            
            if error:
                return False, error
            
            if result and 'output' in result:
                content = result['output']['choices'][0]['message']['content']
                if isinstance(content, list) and len(content) > 0:
                    image_url = content[0].get('image')
                    if image_url:
                        output_path = output_path or image_path.replace('.', f'_{style}.')
                        response = requests.get(image_url, timeout=60)
                        if response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(response.content)
                            return True, output_path
            
            return False, "无法解析API返回结果"
            
        except Exception as e:
            return False, f"处理失败: {str(e)}"


class MockImageEnhancer:
    """模拟图片美化"""
    
    def remove_background(self, image_path, output_path=None):
        return True, "模拟: 背景已去除 (需要开通图像API权限)"
    
    def enhance_image(self, image_path, output_path=None, enhance_type="food"):
        style_names = {"food": "美食增强", "general": "通用增强", "quality": "画质提升"}
        return True, f"模拟: {style_names.get(enhance_type, '增强')}已完成"
    
    def stylize_image(self, image_path, output_path=None, style="food_gourmet"):
        style_names = {"food_gourmet": "美食风格", "anime": "动漫风格", "oil_painting": "油画风格"}
        return True, f"模拟: {style_names.get(style, '风格化')}已完成"


def get_enhancer(api_key=None):
    key = api_key or os.environ.get('DASHSCOPE_API_KEY')
    if key:
        return ImageEnhancer(key)
    return MockImageEnhancer()
