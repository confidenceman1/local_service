import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_tools import AITools
from poi_data import POI_DATA, DEFAULT_LOCATIONS, TIME_SLOTS, FLAVOR_PREFERENCES, get_poi_data
import random

class AIFoodRecommender:
    SYSTEM_PROMPT = """你是一个城市美食推荐助手，专门为用户推荐本地美食。

你的能力：
1. 根据用户的城市、位置、口味偏好、时段等条件推荐合适的餐厅
2. 理解语义化的用户需求
3. 提供个性化的推荐理由

推荐逻辑：
- 首先筛选符合条件的餐厅
- 按评分和距离排序
- 生成个性化的推荐理由

输出格式要求：
- 开头：根据用户需求给出推荐结论
- 主体：列出推荐餐厅，包含名称、评分、距离、价格、标签、地址
- 结尾：给出实用的小贴士

风格要求：
- 语气亲切，像朋友推荐
- 推荐理由要具体
- 适当使用emoji增加趣味性

请直接输出推荐内容，不要有多余的解释。"""

    def __init__(self, api_key=None, model="qwen-turbo"):
        self.ai_tools = AITools(api_key)
        self.poi_data = POI_DATA
        self.model = model
        self.db = get_poi_data()
    
    def get_cities(self):
        if self.db:
            return self.db.get_all_cities()
        return list(POI_DATA.keys())
    
    def get_categories(self, city):
        if self.db:
            return self.db.get_categories_by_city(city)
        if city in POI_DATA:
            return list(POI_DATA[city].keys())
        return []
    
    def get_locations(self, city):
        return DEFAULT_LOCATIONS.get(city, ["市中心"])
    
    def get_time_slots(self):
        return list(TIME_SLOTS.keys())
    
    def get_flavors(self):
        return list(FLAVOR_PREFERENCES.keys())
    
    def recommend(self, city, location, category, flavor, time_slot, max_results=5, model=None):
        restaurants = self._search_restaurants(city, category, flavor, time_slot)
        
        if not restaurants:
            return self._generate_empty_result(city, category)
        
        restaurants = sorted(restaurants, key=lambda x: (-x["rating"], x["distance"]))[:max_results]
        
        prompt = self._build_recommendation_prompt(
            city, location, category, flavor, time_slot, restaurants
        )
        
        return self.ai_tools.generate_content(prompt, system_prompt=self.SYSTEM_PROMPT, model=model or self.model)
    
    def _search_restaurants(self, city, category, flavor, time_slot):
        if self.db:
            db_results = self.db.get_restaurants(city, category, flavor)
            results = []
            for r in db_results:
                restaurant = {
                    "name": r.get("name"),
                    "category": r.get("category"),
                    "distance": r.get("distance"),
                    "rating": float(r.get("rating", 0)),
                    "tags": r.get("tags", "").split(",") if r.get("tags") else [],
                    "price": r.get("price"),
                    "address": r.get("address")
                }
                restaurant["match_score"] = self._calculate_match_score(restaurant, flavor)
                results.append(restaurant)
            return results
        
        results = []
        
        if city not in POI_DATA:
            return results
        
        target_categories = [category] if category else list(POI_DATA[city].keys())
        
        for cat in target_categories:
            if cat in POI_DATA[city]:
                for restaurant in POI_DATA[city][cat]:
                    score = self._calculate_match_score(restaurant, flavor)
                    restaurant_copy = restaurant.copy()
                    restaurant_copy["match_score"] = score
                    results.append(restaurant_copy)
        
        return results
    
    def _calculate_match_score(self, restaurant, flavor):
        score = 0
        
        if flavor and flavor in FLAVOR_PREFERENCES:
            flavor_keywords = FLAVOR_PREFERENCES[flavor]
            for tag in restaurant.get("tags", []):
                for fk in flavor_keywords:
                    if fk in tag:
                        score += 2
        
        score += restaurant.get("rating", 0)
        
        return score
    
    def _build_recommendation_prompt(self, city, location, category, flavor, time_slot, restaurants):
        restaurant_list = "\n".join([
            f"- {r['name']} | 评分:{r['rating']} | 距离:{r['distance']} | 人均:{r['price']} | 标签:{','.join(r['tags'])} | 地址:{r['address']}"
            for r in restaurants
        ])
        
        prompt = f"""请为用户推荐{city}的美食：

用户条件：
- 位置：{location}
- 偏好类型：{category if category else '不限'}
- 口味偏好：{flavor if flavor else '不限'}
- 用餐时段：{time_slot}

候选餐厅：
{restaurant_list}

请根据用户需求，从候选餐厅中选择最合适的推荐，给出推荐理由。
如果用户选择了特定口味，请重点推荐符合该口味的餐厅。
最后给出实用的小贴士。"""

        return prompt
    
    def _generate_empty_result(self, city, category):
        return f"""抱歉，在{city}暂时没有找到符合条件的{category}餐厅。

💡 小贴士：
- 尝试选择其他菜系类型
- 调整口味偏好设置
- 扩大搜索范围

欢迎换个条件再试一次！
"""
    
    def semantic_search(self, user_query, city, max_results=5, model=None):
        city_data = POI_DATA.get(city, {})
        all_restaurants = []
        
        for category, restaurants in city_data.items():
            for r in restaurants:
                r_copy = r.copy()
                r_copy["category"] = category
                all_restaurants.append(r_copy)
        
        if not all_restaurants:
            return "抱歉，暂无相关数据"
        
        prompt = f"""用户搜索：{user_query}

候选餐厅：
{chr(10).join([f"- {r['name']} | 类型:{r['category']} | 评分:{r['rating']} | 标签:{','.join(r['tags'])}" for r in all_restaurants[:20]])}

请根据用户语义化搜索意图，推荐最匹配的餐厅，解释推荐理由。"""

        return self.ai_tools.generate_content(prompt, system_prompt=self.SYSTEM_PROMPT, model=model or self.model)


if __name__ == "__main__":
    recommender = AIFoodRecommender()
    
    print("=== 美食推荐测试 ===")
    result = recommender.recommend(
        city="北京",
        location="朝阳区",
        category="火锅",
        flavor="鲜",
        time_slot="晚餐"
    )
    print(result)
