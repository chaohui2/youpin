from decimal import Decimal

import youpin_client




def print_goods_info(goods):
    goods_id = goods.get("id")
    templateId = goods.get("templateId")
    commodityName = goods.get("commodityName")
    commodityPrice = goods.get("commodityPrice")
    commodityAbrade = goods.get("commodityAbrade")
    print(f"商品: {commodityName} (ID: {goods_id}, 模板ID: {templateId}, 价格: {commodityPrice} 元, 磨损度: {commodityAbrade})")



def create_order(params):
    return youpin_client.post("/open/v1/api/byGoodsIdAsyncCreateOrderV2",params)



def goods_query(input_params, page_size=200):
    page = 1
    while page <= 50:
        params = {
            "page": page,
            "pageSize": page_size,
        }
        params.update(input_params)

        resp = youpin_client.post("/open/v1/api/goodsQuery", params)
        data = resp.get("data", [])
        yield data
        print(f"[响应] 第 {page} 页，返回 {len(data)} 条数据")

        if not data:
            print("[结束] 数据为空，停止翻页")
            break

        if len(data) < page_size:
            print("[结束] 当前页数据不足 pageSize，已是最后一页")
            break

        page += 1

    print(f"[完成]")


def loop_goods_query(input_params,min_price,max_price):
    while True:
        for data in goods_query(input_params):
            for item in data:
                commodity_price= item.get("commodityPrice")
                if commodity_price and Decimal(commodity_price):
                    commodity_price= Decimal(commodity_price)
                    if Decimal(min_price) <= commodity_price <= Decimal(max_price):
                        print(f"找到匹配的[商品价格] {min_price}<={commodity_price}<={max_price} 元")
                        return item


if __name__ == "__main__":
    trade_links="!!!!!!!!!!!!!!!!!!!!!"#收货方的Steam交易链接
    template_id=999  # 商品模版ID，优先级高
    min_price="0.01" # 最小价格
    max_price="0.03" # 最大价格


    input_params = {
        "templateId": template_id,  # 商品模版ID，优先级高
        # "templateHashName": template_hash_name,  # 模板hash名称，和templateId二选一
        # "abradeStartInterval": abrade_start_interval,  # 最小磨损度（需与abradeEndInterval同时传）
        # "abradeEndInterval": abrade_end_interval,  # 最大磨损度
        # "dopplerProperty": doppler_property,  # 多普勒属性（1-8）
        # "fadeRangeMin": fade_range_min,  # 渐变区间最小值（%）
        # "fadeRangeMax": fade_range_max,  # 渐变区间最大值（%）
        # "hardeningProperty": hardening_property,  # 淬火属性（101-105）
        "sortType": "1"  # 排序方式：0更新时间倒序，1价格升序，2价格降序
    }
    goods=loop_goods_query(input_params,min_price=min_price,max_price=max_price)
    print_goods_info(goods)
    goods_id = goods.get("id")
    commodityPrice = goods.get("commodityPrice")
    order_params = {
        "merchantOrderNo": f"order_{goods_id}", #商户订单号	小于等于59位的数字或英文字符串
        "tradeLinks": trade_links, #收货方的Steam交易链接
        "commodityId": goods_id,
        "purchasePrice": str(commodityPrice) #购买最高价
    }
    print(f"开始创建订单...",order_params)
    order_response = create_order(order_params)
    print('下单结果',order_response)