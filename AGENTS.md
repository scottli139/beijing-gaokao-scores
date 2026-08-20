# AGENTS.md

## 项目概述

北京市高考本科普通批录取投档线数据集，来源为北京教育考试院 (bjeea.cn) 官方发布。

## 数据结构

每年一个独立 CSV（`data/{year}.csv`），同时维护全量合并表 `data/beijing-admission-scores.csv`。

字段：`year, seq, school_code, school_name, major_group, selection_requirement, score, remark`

- `seq` — 官方序号，从 1 开始连续
- `school_code` — 院校代码（4 位数字字符串，保留前导零）
- `major_group` — 专业组编号（2 位数字字符串，如 "01"）
- `selection_requirement` — 选考要求，多科目用全角 `＋` 分隔（非 `/` 或 `+`），中外合办标记在括号内
- `score` — 投档总分（整数）
- `remark` — 格式为 `语文 数学 外语 三科选考 [附加要求]`，部分高分记录（北大清华等）可能为空

CSV 编码：`utf-8-sig`（带 BOM）

## 数据来源模式

北京教育考试院每年 7 月 20 日前后发布投档线：

- 2023/2024：网页 HTML 表格
- 2025/2026：PDF 文件

新增年份时，在 README "数据来源"表中追加一行，附发布日期和链接。

## 提取注意事项

- PDF 文件可能带有"北京教育考试院"水印（"院试考育教京北"七字），会随机污染 `selection_requirement`、数值字段和 `other_requirement`
- 学校名称字段在原始数据中通常干净，只有水印字符+换行的组合才需要清理（如 `"京\n温州肯恩大学"`）
- 部分专业组不公布各科分数，只有总分，属正常现象
- 提取后应抽查与 PDF 原文对比，并检查分数范围是否合理（通常 430-700）

## 合并表维护

每次新增年份数据后，重新生成 `beijing-admission-scores.csv`：按年份顺序合并所有年度 CSV。

## 2023 年特殊处理

原始选考分隔符为 `/`（如 `物理/化学`），已统一规范为全角 `＋`（`物理＋化学`）。后续年份无需此转换。
