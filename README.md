

# 悠悠有品自动下单脚本

本项目用于通过有品开放平台自动查询符合条件的 Steam 商品，并下单购买。

## 功能说明

* **商品分页查询**：轮询有品平台的商品信息接口，自动翻页，直到满足条件或数据结束。
* **价格筛选**：通过设置最低价和最高价，筛选目标商品。
* **自动下单**：一旦发现满足条件的商品，立即发起创建订单请求。

## 使用方式

### 依赖安装
1、Python 3.11+ https://www.python.org/downloads/

2、依赖库
```bash
pip install -r requirements.txt
```

### 接口配置

请在 `youpin_client.py` 中配置以下认证信息：

```python
PRIVATE_KEY = 'your private_key'  # 请替换为你的私钥
APP_KEY = 'your appkey'           # 请替换为你的 App Key
```
### 配置参数

在 `main.py` https://github.com/chaohui2/youpin/blob/main/main.py#L63 部分可配置如下参数：

* `template_id`：商品模板ID，必填
* `min_price` / `max_price`：目标商品价格范围
* `trade_ldinks`：你的 Steam 收货链接，必填
* 可选参数：磨损度区间、Doppler 多普勒属性、排序方式等（已注释）

### 启动脚本

```bash
python main.py
```

脚本会输出每一页查询结果，直到找到符合价格的商品，并显示商品信息和下单结果。

## 示例输出

```
[响应] 第 1 页，返回 200 条数据
找到匹配的[商品价格] 0.01<=0.02<=0.03 元
商品: M9 刺刀 | 渐变大理石 (ID: 123456, 模板ID: 999, 价格: 0.02 元, 磨损度: 0.045)
开始创建订单... {'merchantOrderNo': 'order_123456', ...}
下单结果 {'code': 0, 'msg': '下单成功'}
```

## 注意事项
* 商品价格单位为元，请勿遗漏小数点。
* 使用前请仔细阅读有品平台的 API 接口文档，确保权限与参数合法。
## License

本项目仅用于学习与技术研究，禁止用于非法用途。

