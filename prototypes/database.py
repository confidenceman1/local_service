import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

class Database:
    def __init__(self):
        self.config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', '5432'),
            'database': os.environ.get('DB_NAME', 'local_service'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD', 'postgres')
        }
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = None
        try:
            conn = psycopg2.connect(**self.config)
            yield conn
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            yield None
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query, params=None):
        """执行查询并返回结果"""
        with self.get_connection() as conn:
            if conn is None:
                return None
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    
    def execute_update(self, query, params=None):
        """执行更新/插入操作"""
        with self.get_connection() as conn:
            if conn is None:
                return False
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return True
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            with self.get_connection() as conn:
                if conn:
                    with conn.cursor() as cursor:
                        cursor.execute('SELECT version()')
                        return True, cursor.fetchone()[0]
            return False, "Connection failed"
        except Exception as e:
            return False, str(e)


class RestaurantDB:
    """餐厅数据库操作类"""
    
    def __init__(self, db=None):
        self.db = db or Database()
    
    def get_all_cities(self):
        """获取所有城市"""
        query = "SELECT DISTINCT city FROM restaurants ORDER BY city"
        result = self.db.execute_query(query)
        return [row['city'] for row in result] if result else []
    
    def get_categories_by_city(self, city):
        """获取城市的所有菜系类型"""
        query = """
            SELECT DISTINCT category 
            FROM restaurants 
            WHERE city = %s 
            ORDER BY category
        """
        result = self.db.execute_query(query, (city,))
        return [row['category'] for row in result] if result else []
    
    def get_restaurants(self, city, category=None, flavor=None, limit=10):
        """根据条件搜索餐厅"""
        query = """
            SELECT name, category, distance, rating, tags, price, address
            FROM restaurants
            WHERE city = %s
        """
        params = [city]
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        if flavor:
            query += " AND tags LIKE %s"
            params.append(f'%{flavor}%')
        
        query += " ORDER BY rating DESC, distance LIMIT %s"
        params.append(limit)
        
        result = self.db.execute_query(query, params)
        return result if result else []
    
    def get_restaurant_by_name(self, name):
        """根据名称搜索餐厅"""
        query = "SELECT * FROM restaurants WHERE name LIKE %s LIMIT 1"
        result = self.db.execute_query(query, (f'%{name}%',))
        return result[0] if result else None
    
    def add_restaurant(self, data):
        """添加餐厅"""
        query = """
            INSERT INTO restaurants (name, city, category, distance, rating, tags, price, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get('name'),
            data.get('city'),
            data.get('category'),
            data.get('distance'),
            data.get('rating'),
            ','.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else data.get('tags'),
            data.get('price'),
            data.get('address')
        )
        return self.db.execute_update(query, params)
    
    def init_sample_data(self):
        """初始化示例数据"""
        sample_data = [
            {"name": "海底捞火锅(王府井店)", "city": "北京", "category": "火锅", "distance": "0.8km", "rating": 4.7, "tags": ["服务好", "排队王", "24小时"], "price": "人均120元", "address": "王府井大街138号"},
            {"name": "巴奴毛肚火锅(朝阳大悦城店)", "city": "北京", "category": "火锅", "distance": "3.2km", "rating": 4.6, "tags": ["毛肚必点", "排队久", "网红店"], "price": "人均140元", "address": "朝阳北路101号"},
            {"name": "湊湊火锅(三里屯店)", "city": "北京", "category": "火锅", "distance": "5.1km", "rating": 4.5, "tags": ["奶茶免费", "氛围好", "约会首选"], "price": "人均130元", "address": "三里屯太古里"},
            {"name": "老北京铜锅涮肉(东四店)", "city": "北京", "category": "火锅", "distance": "2.4km", "rating": 4.8, "tags": ["老字号", "地道", "羊肉新鲜"], "price": "人均90元", "address": "东四南大街15号"},
            {"name": "陶陶居(国贸店)", "city": "北京", "category": "粤菜", "distance": "2.1km", "rating": 4.7, "tags": ["老字号", "点心精致", "必吃榜"], "price": "人均130元", "address": "国贸商城"},
            {"name": "捞王锅物料理(人民广场店)", "city": "上海", "category": "火锅", "distance": "0.5km", "rating": 4.7, "tags": ["猪肚鸡", "养生锅", "服务好"], "price": "人均130元", "address": "人民广场来福士"},
            {"name": "小龙坎火锅(春熙路店)", "city": "成都", "category": "火锅", "distance": "0.3km", "rating": 4.7, "tags": ["网红店", "锅底香", "菜品丰富"], "price": "人均90元", "address": "春熙路步行街"},
            {"name": "马路边边麻辣烫(建设路店)", "city": "成都", "category": "串串", "distance": "3.2km", "rating": 4.7, "tags": ["怀旧风", "串串自助", "学生党"], "price": "人均60元", "address": "建设路小吃街"},
            {"name": "陶陶居(上下九店)", "city": "广州", "category": "粤菜", "distance": "0.5km", "rating": 4.8, "tags": ["百年老店", "早茶必去", "点心精致"], "price": "人均80元", "address": "上下九步行街"},
            {"name": "点都德(天河城店)", "city": "广州", "category": "粤菜", "distance": "2.5km", "rating": 4.7, "tags": ["24小时", "点心丰富", "性价比高"], "price": "人均75元", "address": "天河城"},
        ]
        
        for data in sample_data:
            self.add_restaurant(data)
        
        return len(sample_data)


# 数据库初始化SQL
INIT_SQL = """
-- 创建餐厅表
CREATE TABLE IF NOT EXISTS restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    distance VARCHAR(50),
    rating DECIMAL(3,2),
    tags TEXT,
    price VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_restaurants_city ON restaurants(city);
CREATE INDEX IF NOT EXISTS idx_restaurants_category ON restaurants(category);
CREATE INDEX IF NOT EXISTS idx_restaurants_rating ON restaurants(rating DESC);

-- 创建城市表
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    region VARCHAR(50)
);

-- 插入示例城市数据
INSERT INTO cities (name, region) VALUES 
    ('北京', '华北'),
    ('上海', '华东'),
    ('成都', '西南'),
    ('广州', '华南'),
    ('深圳', '华南')
ON CONFLICT (name) DO NOTHING;
"""
