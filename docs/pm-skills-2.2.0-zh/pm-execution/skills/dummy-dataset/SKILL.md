---
name: dummy-dataset
description: "生成逼真的模拟数据集用于测试，支持自定义列、约束与输出格式（CSV、JSON、SQL、Python 脚本）。适用于创建测试数据、构建 mock 数据集，或为开发与演示生成样本数据。"
---
# 生成模拟数据集

生成逼真的模拟数据集用于测试，支持自定义列、约束与输出格式（CSV、JSON、SQL、Python 脚本）。可直接产出可执行脚本或数据文件，立即使用。

**适用场景：** 创建测试数据、生成样本数据集、为开发构建逼真的 mock 数据，或填充测试环境。

**参数：**
- `$PRODUCT`：产品或系统名称
- `$DATASET_TYPE`：数据类型（例如客户反馈、交易、用户资料）
- `$ROWS`：要生成的行数（默认：100）
- `$COLUMNS`：要包含的具体列或字段
- `$FORMAT`：输出格式（CSV、JSON、SQL、Python 脚本）
- `$CONSTRAINTS`：额外的约束或业务规则

## 分步流程

1. **确定数据集类型** —— 理解数据所属领域
2. **定义列规格** —— 名称、数据类型与取值范围
3. **确定行数** —— 需要多少条样本记录
4. **选择输出格式** —— CSV、JSON、SQL INSERT 或 Python 脚本
5. **套用逼真的模式** —— 确保数据看起来真实且有效
6. **添加业务约束** —— 遵守业务逻辑与数据关联
7. **生成数据或编写脚本** —— 产出可执行的输出
8. **校验输出** —— 确保数据质量与完整性

## 模板：Python 脚本输出

```python
import csv
import json
from datetime import datetime, timedelta
import random

# 配置
ROWS = $ROWS
FILENAME = "$DATASET_TYPE.csv"

# 列定义与逼真的取值生成器
columns = {
    "id": "auto-increment",
    "name": "first_last_name",
    "email": "email",
    "created_at": "timestamp",
    # 可继续添加更多列……
}

def generate_dataset():
    """生成逼真的模拟数据集"""
    data = []
    for i in range(1, ROWS + 1):
        record = {
            "id": f"U{i:06d}",
            # 根据列定义生成取值
        }
        data.append(record)
    return data

def save_as_csv(data, filename):
    """将数据集保存为 CSV"""
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    dataset = generate_dataset()
    save_as_csv(dataset, FILENAME)
    print(f"Generated {len(dataset)} records in {FILENAME}")
```

## 示例数据集规格

**数据集类型：** 客户反馈

**列：**
- feedback_id（自增，U001、U002……）
- customer_name（逼真的姓名）
- email（有效的邮箱格式）
- feedback_date（最近 90 天内的日期）
- rating（1-5 星）
- category（Bug、功能需求、投诉、好评）
- text（逼真的反馈内容）
- product（电子产品、服装、家居）

**约束：**
- 评分分布偏斜：40% 为 5 星，30% 为 4 星，20% 为 3 星，10% 为 1-2 星
- Bug 类别只出现在 1-3 星的评分中
- 功能需求只出现在 3-5 星的评分中
- 邮箱域名要真实（gmail、yahoo、company.com）

## 输出交付物

- 可直接执行的 Python 脚本，或直接生成的数据文件
- 表头与格式规范的 CSV 文件
- 结构合法、类型正确的 JSON 文件
- 用于填充数据库的 SQL INSERT 语句
- 数据校验与约束合规性
- 逼真且符合业务场景的取值
- 数据生成逻辑的说明文档
- 使用该数据集的快速上手指引

## 输出格式

**CSV：** 扁平表格格式，便于导入电子表格与数据库

**JSON：** 嵌套结构，适合 API 与 NoSQL 数据库

**SQL：** INSERT 语句，可直接在关系型数据库上执行

**Python 脚本：** 可执行的生成器，适合自定义或大规模数据集
