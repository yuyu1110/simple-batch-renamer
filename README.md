# 文件批量重命名

一个简单的 Python 办公自动化命令行工具。

## 快速开始

需要 Python 3.10 或以上。在项目目录打开终端，建议先建立虚拟环境：

```bash
python -m venv .venv
```

Windows：`.venv\Scripts\activate`；macOS/Linux：`source .venv/bin/activate`。然后运行：

```bash
python examples/create_demo.py
python renamer.py demo --prefix work_ --number
python renamer.py demo --prefix work_ --number --apply
```

示例生成器只创建虚构数据，并在 demo 目录已存在时退出，避免覆盖。

## 功能与边界

支持 --prefix 添加前缀、--number 添加三位起始编号、--start 设置起始值，以及 --replace OLD NEW 替换文件主名中的文字。扩展名保持不变。文件按文件名排序，不递归，跳过隐藏文件和符号链接。默认预览，--apply 执行；先检查重名和非法文件名。为保持简单，不支持名称互换、仅变更大小写或执行后的自动撤销。不要在运行时同时修改目标目录。

查看全部参数：`python renamer.py --help`。

## 测试

```bash
python -m unittest discover -s tests -v
```

测试使用临时目录，不修改个人文件。

## 项目结构

- `renamer.py`：核心功能及命令行入口
- `examples/create_demo.py`：生成示例输入
- `tests/test_tool.py`：功能及异常场景测试

## 简历表述参考

使用 argparse 和 pathlib 实现批量添加前缀、编号与文字替换，通过执行前校验避免常见重名错误。

这是学习与练习项目；请在理解实现后按实际参与情况描述，不包含生产使用或性能提升声明。
