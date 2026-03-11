"""
生成更多餐厅数据并导入数据库
"""
import os
from dotenv import load_dotenv

load_dotenv()

import psycopg2

# 扩展的餐厅数据 (目标100条，目前10条，需要再生成90条)
SAMPLE_DATA = [
    # 北京 - 火锅 (已有4条)
    {"name": "海底捞火锅(合生汇店)", "city": "北京", "category": "火锅", "distance": "5.5km", "rating": 4.6, "tags": "服务好,排队,24小时", "price": "人均120元", "address": "合生汇商场"},
    {"name": "海底捞火锅(大望路店)", "city": "北京", "category": "火锅", "distance": "3.2km", "rating": 4.5, "tags": "服务好,地铁直达,VIP", "price": "人均130元", "address": "大望路地铁站"},
    {"name": "楠火锅(五道口店)", "city": "北京", "category": "火锅", "distance": "6.8km", "rating": 4.4, "tags": "重庆火锅,辣,地道", "price": "人均100元", "address": "五道口购物中心"},
    {"name": "珮姐老火锅(三里屯店)", "city": "北京", "category": "火锅", "distance": "4.9km", "rating": 4.7, "tags": "网红店,锅底香,排队久", "price": "人均140元", "address": "三里屯SOHO"},
    {"name": "左庭右院鲜牛肉火锅(朝阳大悦城店)", "city": "北京", "category": "火锅", "distance": "6.1km", "rating": 4.6, "tags": "鲜牛肉,潮汕火锅,清淡", "price": "人均110元", "address": "朝阳大悦城"},
    
    # 北京 - 烧烤 (已有2条)
    {"name": "很久以前羊肉串(望京店)", "city": "北京", "category": "烧烤", "distance": "7.2km", "rating": 4.5, "tags": "自助烤,羊肉串,学生党", "price": "人均85元", "address": "望京美食街"},
    {"name": "木屋烧烤(五道口店)", "city": "北京", "category": "烧烤", "distance": "6.5km", "rating": 4.3, "tags": "连锁,食材新鲜,实惠", "price": "人均80元", "address": "五道口华联"},
    {"name": "串亭烧烤(簋街店)", "city": "北京", "category": "烧烤", "distance": "2.5km", "rating": 4.4, "tags": "串串,氛围好,夜宵", "price": "人均75元", "address": "东直门簋街"},
    {"name": "鸟亭烧鸟(国贸店)", "city": "北京", "category": "烧烤", "distance": "3.8km", "rating": 4.7, "tags": "日式烧鸟,精致,高端", "price": "人均150元", "address": "国贸商城"},
    {"name": "老北京烤肉(什刹海店)", "city": "北京", "category": "烧烤", "distance": "1.8km", "rating": 4.5, "tags": "老北京,传统,铜锅", "price": "人均90元", "address": "什刹海"},
    
    # 北京 - 日料 (已有2条)
    {"name": "鮨·日本料理(朝阳大悦城店)", "city": "北京", "category": "日料", "distance": "6.2km", "rating": 4.8, "tags": "omakase,高端,食材进口", "price": "人均450元", "address": "朝阳大悦城"},
    {"name": "大雄寿司(望京店)", "city": "北京", "category": "日料", "distance": "7.5km", "rating": 4.6, "tags": "平价,寿司新鲜,老板热情", "price": "人均100元", "address": "望京SOHO"},
    {"name": "牛角烧肉(国贸店)", "city": "北京", "category": "日料", "distance": "3.5km", "rating": 4.7, "tags": "烧肉自助,肉类丰富,性价比", "price": "人均180元", "address": "国贸商城"},
    {"name": "平成屋日料(五道口店)", "city": "北京", "category": "日料", "distance": "6.8km", "rating": 4.4, "tags": "日式料理,拉面,定食", "price": "人均70元", "address": "五道口"},
    {"name": "鮨禅日本料理(金融街店)", "city": "北京", "category": "日料", "distance": "2.2km", "rating": 4.9, "tags": "米其林,omakase,私密", "price": "人均600元", "address": "金融街购物中心"},
    
    # 北京 - 川菜 (已有2条)
    {"name": "川菜王(望京店)", "city": "北京", "category": "川菜", "distance": "7.0km", "rating": 4.4, "tags": "地道川味,辣,实惠", "price": "人均65元", "address": "望京美食街"},
    {"name": "蜀大侠火锅(五道口店)", "city": "北京", "category": "川菜", "distance": "6.5km", "rating": 4.5, "tags": "武侠风,锅底香,菜品新鲜", "price": "人均105元", "address": "五道口"},
    {"name": "蓉上坊川菜(国贸店)", "city": "北京", "category": "川菜", "distance": "3.6km", "rating": 4.6, "tags": "精致川菜,商务,环境好", "price": "人均120元", "address": "国贸商城"},
    {"name": "川国演义(簋街店)", "city": "北京", "category": "川菜", "distance": "2.3km", "rating": 4.3, "tags": "川味,麻辣,夜宵", "price": "人均80元", "address": "东直门簋街"},
    {"name": "老成都家常菜(中关村店)", "city": "北京", "category": "川菜", "distance": "5.5km", "rating": 4.5, "tags": "家常味,价格实惠,必点回锅肉", "price": "人均55元", "address": "中关村"},
    
    # 北京 - 粤菜 (已有2条)
    {"name": "利苑酒家(国贸店)", "city": "北京", "category": "粤菜", "distance": "3.2km", "rating": 4.7, "tags": "米其林,粤菜标杆,烧腊", "price": "人均180元", "address": "国贸商城"},
    {"name": "陶陶居(西单店)", "city": "北京", "category": "粤菜", "distance": "2.8km", "rating": 4.6, "tags": "老字号,点心精致,必吃榜", "price": "人均125元", "address": "西单大悦城"},
    {"name": "粤菜小厨(望京店)", "city": "北京", "category": "粤菜", "distance": "7.2km", "rating": 4.4, "tags": "平价粤菜,烧腊,煲仔饭", "price": "人均70元", "address": "望京SOHO"},
    {"name": "海门鱼仔(朝阳门店)", "city": "北京", "category": "粤菜", "distance": "2.5km", "rating": 4.5, "tags": "潮汕菜,海鲜,新鲜", "price": "人均150元", "address": "朝阳门商圈"},
    {"name": "惠食佳(潘家园店)", "city": "北京", "category": "粤菜", "distance": "4.8km", "rating": 4.8, "tags": "米其林,煲仔饭,招牌菜", "price": "人均160元", "address": "潘家园"},
    
    # 上海 - 火锅 (已有1条)
    {"name": "海底捞火锅(南京路店)", "city": "上海", "category": "火锅", "distance": "1.2km", "rating": 4.6, "tags": "服务好,排队,24小时", "price": "人均120元", "address": "南京路步行街"},
    {"name": "捞王锅物料理(徐家汇店)", "city": "上海", "category": "火锅", "distance": "4.5km", "rating": 4.7, "tags": "猪肚鸡,养生锅,服务好", "price": "人均135元", "address": "徐家汇港汇"},
    {"name": "电台巷火锅(静安寺店)", "city": "上海", "category": "火锅", "distance": "3.8km", "rating": 4.5, "tags": "成都味,辣,网红", "price": "人均115元", "address": "静安寺商圈"},
    {"name": "湊湊火锅(南京西路店)", "city": "上海", "category": "火锅", "distance": "2.5km", "rating": 4.6, "tags": "奶茶免费,氛围好,约会", "price": "人均130元", "address": "南京西路"},
    {"name": "左庭右院鲜牛肉火锅(人广店)", "city": "上海", "category": "火锅", "distance": "1.0km", "rating": 4.5, "tags": "鲜牛肉,潮汕,清淡", "price": "人均110元", "address": "人民广场"},
    
    # 上海 - 本帮菜 (已有2条)
    {"name": "上海老饭店(外滩店)", "city": "上海", "category": "本帮菜", "distance": "2.8km", "rating": 4.7, "tags": "百年老店,地道本帮,红烧肉", "price": "人均120元", "address": "外滩"},
    {"name": "绿波廊(南京路店)", "city": "上海", "category": "本帮菜", "distance": "1.5km", "rating": 4.6, "tags": "老字号,点心精美,游客打卡", "price": "人均95元", "address": "南京路步行街"},
    {"name": "老吉士酒家(天平路店)", "city": "上海", "category": "本帮菜", "distance": "5.2km", "rating": 4.8, "tags": "本帮菜,浓油赤酱,老上海", "price": "人均150元", "address": "徐家汇"},
    {"name": "福1088(镇宁路店)", "city": "上海", "category": "本帮菜", "distance": "4.0km", "rating": 4.7, "tags": "米其林,本帮菜,预约难", "price": "人均280元", "address": "镇宁路"},
    {"name": "海金滋(进贤路店)", "city": "上海", "category": "本帮菜", "distance": "3.2km", "rating": 4.5, "tags": "老字号,性价比,本地人爱", "price": "人均60元", "address": "进贤路"},
    
    # 上海 - 日料 (已有2条)
    {"name": "割烹·哲(新天地店)", "city": "上海", "category": "日料", "distance": "3.5km", "rating": 4.9, "tags": "omakase,主厨推荐,隐蔽", "price": "人均550元", "address": "新天地"},
    {"name": "大江户日本料理(人民广场店)", "city": "上海", "category": "日料", "distance": "1.2km", "rating": 4.6, "tags": "放题,刺身拼盘,性价比", "price": "人均198元", "address": "人民广场"},
    {"name": " sushi Oyama(古北店)", "city": "上海", "category": "日料", "distance": "6.0km", "rating": 4.8, "tags": "法式日料,融合,精致", "price": "人均400元", "address": "古北"},
    {"name": "酒吞(虹口店)", "city": "上海", "category": "日料", "distance": "4.2km", "rating": 4.7, "tags": "放题,清酒,寿司", "price": "人均250元", "address": "虹口足球场"},
    {"name": "鮨吞(浦东店)", "city": "上海", "category": "日料", "distance": "5.5km", "rating": 4.6, "tags": "江户前寿司,时令,新鲜", "price": "人均350元", "address": "陆家嘴"},
    
    # 成都 - 火锅 (已有3条)
    {"name": "小龙坎火锅(太古里店)", "city": "成都", "category": "火锅", "distance": "1.8km", "rating": 4.7, "tags": "网红店,锅底香,菜品丰富", "price": "人均95元", "address": "远洋太古里"},
    {"name": "蜀九香火锅(春熙路店)", "city": "成都", "category": "火锅", "distance": "0.5km", "rating": 4.8, "tags": "本地人推荐,牛油锅底,食材新鲜", "price": "人均90元", "address": "春熙路"},
    {"name": "大龙燚火锅(玉林店)", "city": "成都", "category": "火锅", "distance": "2.5km", "rating": 4.6, "tags": "明星打卡,辣,氛围好", "price": "人均100元", "address": "玉林"},
    {"name": "皇城老妈火锅(红瓦寺店)", "city": "成都", "category": "火锅", "distance": "3.0km", "rating": 4.7, "tags": "老成都,牛肉,锅底醇厚", "price": "人均110元", "address": "红瓦寺"},
    {"name": "川西坝子火锅(宽窄巷子店)", "city": "成都", "category": "火锅", "distance": "1.5km", "rating": 4.5, "tags": "自助火锅,菜品多,性价比", "price": "人均85元", "address": "宽窄巷子"},
    
    # 成都 - 串串 (已有2条)
    {"name": "马路边边麻辣烫(玉林店)", "city": "成都", "category": "串串", "distance": "2.8km", "rating": 4.7, "tags": "怀旧风,串串自助,学生党", "price": "人均65元", "address": "玉林"},
    {"name": "钢管厂五区小郡肝串串(春熙路店)", "city": "成都", "category": "串串", "distance": "0.8km", "rating": 4.8, "tags": "老牌,小郡肝,味道稳定", "price": "人均75元", "address": "春熙路"},
    {"name": "冒椒火辣串串(玉林店)", "city": "成都", "category": "串串", "distance": "3.2km", "rating": 4.6, "tags": "网红店,麻辣,必打卡", "price": "人均70元", "address": "玉林"},
    {"name": "十年沉淀小郡肝串串(建设路店)", "city": "成都", "category": "串串", "distance": "4.0km", "rating": 4.5, "tags": "老店,小郡肝,辣", "price": "人均60元", "address": "建设路"},
    {"name": "凹串串(春熙路店)", "city": "成都", "category": "串串", "distance": "0.6km", "rating": 4.7, "tags": "环境好,食材新鲜,味道棒", "price": "人均80元", "address": "春熙路"},
    
    # 成都 - 川菜 (已有2条)
    {"name": "老成都家常菜(春熙路店)", "city": "成都", "category": "川菜", "distance": "0.5km", "rating": 4.5, "tags": "家常味,价格实惠,必点回锅肉", "price": "人均55元", "address": "春熙路"},
    {"name": "陈麻婆豆腐(春熙路店)", "city": "成都", "category": "川菜", "distance": "0.7km", "rating": 4.6, "tags": "老字号,麻婆豆腐,川菜代表", "price": "人均70元", "address": "春熙路"},
    {"name": "努力餐(宽窄巷子店)", "city": "成都", "category": "川菜", "distance": "1.8km", "rating": 4.7, "tags": "老字号,革命菜,味道正", "price": "人均80元", "address": "宽窄巷子"},
    {"name": "银杏川菜(科华北路店)", "city": "成都", "category": "川菜", "distance": "4.5km", "rating": 4.6, "tags": "老牌川菜,商务,环境好", "price": "人均120元", "address": "科华北路"},
    {"name": "红杏酒家(羊西线店)", "city": "成都", "category": "川菜", "distance": "5.0km", "rating": 4.8, "tags": "老字号,川菜代表,婚宴", "price": "人均130元", "address": "羊西线"},
    
    # 广州 - 粤菜 (已有3条)
    {"name": "点都德(北京路店)", "city": "广州", "category": "粤菜", "distance": "1.5km", "rating": 4.7, "tags": "24小时,点心丰富,性价比", "price": "人均78元", "address": "北京路步行街"},
    {"name": "广州酒家(上下九店)", "city": "广州", "category": "粤菜", "distance": "0.8km", "rating": 4.8, "tags": "老字号,月饼有名,婚宴首选", "price": "人均125元", "address": "上下九"},
    {"name": "陶陶居(天河城店)", "city": "广州", "category": "粤菜", "distance": "3.0km", "rating": 4.7, "tags": "百年老店,早茶必去,点心精致", "price": "人均85元", "address": "天河城"},
    {"name": "惠食佳(滨江店)", "city": "广州", "category": "粤菜", "distance": "2.5km", "rating": 4.9, "tags": "米其林,煲仔饭,招牌菜", "price": "人均165元", "address": "滨江路"},
    {"name": "炳胜品味(天河店)", "city": "广州", "category": "粤菜", "distance": "3.8km", "rating": 4.8, "tags": "老字号,粤菜标杆,烧腊", "price": "人均140元", "address": "天河"},
    
    # 广州 - 早茶 (已有2条)
    {"name": "点点心茶楼(天河城店)", "city": "广州", "category": "早茶", "distance": "3.2km", "rating": 4.7, "tags": "本地人爱,流沙包,虾饺皇", "price": "人均68元", "address": "天河城"},
    {"name": "荣记茶楼(荔湾湖店)", "city": "广州", "category": "早茶", "distance": "5.0km", "rating": 4.6, "tags": "老式茶楼,传统味道,民国风", "price": "人均55元", "address": "荔湾湖"},
    {"name": "银记肠粉(上下九店)", "city": "广州", "category": "早茶", "distance": "1.0km", "rating": 4.5, "tags": "肠粉,老字号,平价", "price": "人均35元", "address": "上下九"},
    {"name": "莲香楼(第十甫路店)", "city": "广州", "category": "早茶", "distance": "1.2km", "rating": 4.6, "tags": "百年老店,莲蓉包,手信", "price": "人均60元", "address": "第十甫路"},
    {"name": "南园酒家(前进路店)", "city": "广州", "category": "早茶", "distance": "4.5km", "rating": 4.7, "tags": "老字号,园林酒家,早茶", "price": "人均80元", "address": "前进路"},
    
    # 广州 - 煲仔饭 (已有2条)
    {"name": "煲仔饭皇后(北京路店)", "city": "广州", "category": "煲仔饭", "distance": "1.5km", "rating": 4.7, "tags": "锅巴脆,腊味香,排队久", "price": "人均38元", "address": "北京路"},
    {"name": "民记煲仔饭(天河店)", "city": "广州", "category": "煲仔饭", "distance": "3.5km", "rating": 4.6, "tags": "老店,食材新鲜,味道稳定", "price": "人均40元", "address": "天河"},
    {"name": "好彩煲仔饭(荔湾店)", "city": "广州", "category": "煲仔饭", "distance": "4.2km", "rating": 4.5, "tags": "平价,锅巴脆,学生党", "price": "人均30元", "address": "荔湾"},
    {"name": "万兴煲仔饭(越秀店)", "city": "广州", "category": "煲仔饭", "distance": "2.0km", "rating": 4.6, "tags": "老店,经典,味道好", "price": "人均35元", "address": "越秀公园"},
    {"name": "锦记煲仔饭(海珠店)", "city": "广州", "category": "煲仔饭", "distance": "3.8km", "rating": 4.4, "tags": "实惠,地道,街坊生意", "price": "人均28元", "address": "海珠"},
    
    # 深圳 - 粤菜 (已有2条)
    {"name": "潮汕牛肉火锅(海岸城店)", "city": "深圳", "category": "粤菜", "distance": "5.5km", "rating": 4.8, "tags": "手打牛肉,牛肉丸,汤底清甜", "price": "人均125元", "address": "海岸城"},
    {"name": "利宝阁(福田店)", "city": "深圳", "category": "粤菜", "distance": "2.8km", "rating": 4.6, "tags": "粤菜代表,点心精致,环境好", "price": "人均135元", "address": "福田CBD"},
    {"name": "潮汕菜馆(南山店)", "city": "深圳", "category": "粤菜", "distance": "6.0km", "rating": 4.7, "tags": "潮汕风味,牛肉火锅,食材新鲜", "price": "人均115元", "address": "南山科技园"},
    {"name": "粤菜王(罗湖店)", "city": "深圳", "category": "粤菜", "distance": "2.0km", "rating": 4.5, "tags": "老字号,粤菜,性价比", "price": "人均90元", "address": "罗湖"},
    {"name": "丹桂轩(福田店)", "city": "深圳", "category": "粤菜", "distance": "3.5km", "rating": 4.7, "tags": "米其林,精致粤菜,约会", "price": "人均200元", "address": "福田"},
    
    # 深圳 - 湘菜 (已有2条)
    {"name": "湘菜馆(福田店)", "city": "深圳", "category": "湘菜", "distance": "3.5km", "rating": 4.5, "tags": "剁椒鱼头,辣,下饭菜", "price": "人均72元", "address": "福田CBD"},
    {"name": "炊烟小炒黄牛肉(南山店)", "city": "深圳", "category": "湘菜", "distance": "5.8km", "rating": 4.6, "tags": "网红湘菜,小炒黄牛肉,必打卡", "price": "人均88元", "address": "南山"},
    {"name": "费大厨辣椒炒肉(福田店)", "city": "深圳", "category": "湘菜", "distance": "4.0km", "rating": 4.7, "tags": "辣椒炒肉,必点,味道正", "price": "人均75元", "address": "福田"},
    {"name": "老灶柴火鱼(龙岗店)", "city": "深圳", "category": "湘菜", "distance": "8.0km", "rating": 4.4, "tags": "柴火菜,乡村风,实惠", "price": "人均60元", "address": "龙岗"},
    {"name": "壹品湘(罗湖店)", "city": "深圳", "category": "湘菜", "distance": "2.5km", "rating": 4.5, "tags": "湘菜,口味重,下饭", "price": "人均68元", "address": "罗湖"},
    
    # 深圳 - 火锅 (已有1条)
    {"name": "潮汕牛肉火锅(罗湖店)", "city": "深圳", "category": "火锅", "distance": "1.8km", "rating": 4.7, "tags": "手打牛肉,牛肉丸,汤底清甜", "price": "人均120元", "address": "罗湖"},
    {"name": "海底捞火锅(南山店)", "city": "深圳", "category": "火锅", "distance": "6.2km", "rating": 4.6, "tags": "服务好,排队,24小时", "price": "人均125元", "address": "南山"},
    {"name": "椰子鸡火锅(福田店)", "city": "深圳", "category": "火锅", "distance": "3.5km", "rating": 4.8, "tags": "椰子鸡,清甜,深圳特色", "price": "人均110元", "address": "福田"},
    {"name": "捞王锅物料理(南山店)", "city": "深圳", "category": "火锅", "distance": "5.8km", "rating": 4.7, "tags": "猪肚鸡,养生锅,服务好", "price": "人均135元", "address": "南山"},
    {"name": "顺德鱼生火锅(宝安店)", "city": "深圳", "category": "火锅", "distance": "10km", "rating": 4.5, "tags": "鱼生,顺德菜,新鲜", "price": "人均100元", "address": "宝安"},
]

def main():
    config = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_NAME', 'local_service'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'postgres')
    }
    
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    
    # 检查当前数据量
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    current_count = cursor.fetchone()[0]
    print(f"当前餐厅数量: {current_count}")
    
    # 插入新数据
    print(f"准备插入 {len(SAMPLE_DATA)} 条数据...")
    for data in SAMPLE_DATA:
        cursor.execute("""
            INSERT INTO restaurants (name, city, category, distance, rating, tags, price, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['name'], data['city'], data['category'], data['distance'], 
              data['rating'], data['tags'], data['price'], data['address']))
    
    conn.commit()
    
    # 验证
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    new_count = cursor.fetchone()[0]
    print(f"插入后餐厅数量: {new_count}")
    print(f"成功插入 {new_count - current_count} 条数据!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
