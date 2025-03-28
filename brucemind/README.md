# BruceMind 思维导图工具

这是一个简单而实用的思维导图工具，使用Python和tkinter开发，支持树状结构的展示和编辑，以及YAML格式的数据导入导出。

## 功能特点

- 树状结构右侧展开显示
- 支持节点的添加、删除和编辑
- 支持节点的展开和收起
- 数据可保存为YAML格式
- 支持从YAML文件加载数据

## 使用方法

1. 运行程序：
   ```
   python main.py
   ```

2. 基本操作：
   - 点击"新建节点"添加新的节点
   - 双击节点可以编辑节点内容
   - 选中节点后点击"删除节点"可以删除节点
   - 使用"保存到YAML"将当前思维导图保存到文件
   - 使用"从YAML加载"可以读取已保存的思维导图

## 依赖项

- Python 3.x
- tkinter（Python标准库）
- PyYAML

## 安装依赖

```
pip install pyyaml
```

## 注意事项

- 保存的YAML文件默认名称为mindmap.yaml
- 编辑节点时按回车键或点击其他位置可以保存修改