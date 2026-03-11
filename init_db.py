"""
数据库初始化脚本
用于创建数据库表并导入示例数据
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database_if_not_exists(config):
    """创建数据库（如果不存在）"""
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            dbname='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # 检查数据库是否存在
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{config['database']}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {config['database']}")
            print(f"Database '{config['database']}' created successfully!")
        else:
            print(f"Database '{config['database']}' already exists.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def init_tables(config):
    """创建数据库表"""
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # 创建餐厅表
        cursor.execute("""
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
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_restaurants_city ON restaurants(city);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_restaurants_category ON restaurants(category);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_restaurants_rating ON restaurants(rating DESC);")
        
        # 创建城市表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                region VARCHAR(50)
            );
        """)
        
        # 插入示例城市数据
        cursor.execute("""
            INSERT INTO cities (name, region) VALUES 
                ('北京', '华北'),
                ('上海', '华东'),
                ('成都', '西南'),
                ('广州', '华南'),
                ('深圳', '华南')
            ON CONFLICT (name) DO NOTHING;
        """)
        
        conn.commit()
        print("Tables created successfully!")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def import_sample_data(config):
    """导入示例餐厅数据"""
    sample_data = [
        {"name": "海底捞火锅(王府井店)", "city": "北京", "category": "火锅", "distance": "0.8km", "rating": 4.7, "tags": "服务好,排队王,24小时", "price": "人均120元", "address": "王府井大街138号"},
        {"name": "巴奴毛肚火锅(朝阳大悦城店)", "city": "北京", "category": "火锅", "distance": "3.2km", "rating": 4.6, "tags": "毛肚必点,排队久,网红店", "price": "人均140元", "address": "朝阳北路101号"},
        {"name": "湊湊火锅(三里屯店)", "city": "北京", "category": "火锅", "distance": "5.1km", "rating": 4.5, "tags": "奶茶免费,氛围好,约会首选", "price": "人均130元", "address": "三里屯太古里"},
        {"name": "老北京铜锅涮肉(东四店)", "city": "北京", "category": "火锅", "distance": "2.4km", "rating": 4.8, "tags": "老字号,地道,羊肉新鲜", "price": "人均90元", "address": "东四南大街15号"},
        {"name": "陶陶居(国贸店)", "city": "北京", "category": "粤菜", "distance": "2.1km", "rating": 4.7, "tags": "老字号,点心精致,必吃榜", "price": "人均130元", "address": "国贸商城"},
        {"name": "捞王锅物料理(人民广场店)", "city": "上海", "category": "火锅", "distance": "0.5km", "rating": 4.7, "tags": "猪肚鸡,养生锅,服务好", "price": "人均130元", "address": "人民广场来福士"},
        {"name": "小龙坎火锅(春熙路店)", "city": "成都", "category": "火锅", "distance": "0.3km", "rating": 4.7, "tags": "网红店,锅底香,菜品丰富", "price": "人均90元", "address": "春熙路步行街"},
        {"name": "马路边边麻辣烫(建设路店)", "city": "成都", "category": "串串", "distance": "3.2km", "rating": 4.7, "tags": "怀旧风,串串自助,学生党", "price": "人均60元", "address": "建设路小吃街"},
        {"name": "陶陶居(上下九店)", "city": "广州", "category": "粤菜", "distance": "0.5km", "rating": 4.8, "tags": "百年老店,早茶必去,点心精致", "price": "人均80元", "address": "上下九步行街"},
        {"name": "点都德(天河城店)", "city": "广州", "category": "粤菜", "distance": "2.5km", "rating": 4.7, "tags": "24小时,点心丰富,性价比高", "price": "人均75元", "address": "天河城"},
    ]
    
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        for data in sample_data:
            cursor.execute("""
                INSERT INTO restaurants (name, city, category, distance, rating, tags, price, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (data['name'], data['city'], data['category'], data['distance'], 
                  data['rating'], data['tags'], data['price'], data['address']))
        
        conn.commit()
        print(f"Imported {len(sample_data)} restaurant records!")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error importing data: {e}")
        return False

def main():
    """主函数"""
    import os
    
    config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_NAME', 'local_service'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'postgres')
    }
    
    print("="*50)
    print("数据库初始化")
    print("="*50)
    print(f"配置: {config}")
    print()
    
    # 创建数据库
    print("1. 创建数据库...")
    create_database_if_not_exists(config)
    
    # 创建表
    print("2. 创建数据表...")
    if init_tables(config):
        # 导入示例数据
        print("3. 导入示例数据...")
        import_sample_data(config)
    
    print()
    print("="*50)
    print("初始化完成！")
    print("="*50)

if __name__ == "__main__":
    main()
