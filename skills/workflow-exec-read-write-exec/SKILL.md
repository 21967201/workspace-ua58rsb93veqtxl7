# workflow-exec-read-write-exec

## 工作流模式

**工具调用序列**: exec -> read -> write -> exec

**出现次数**: 8 次  
**置信度**: 0.8

## 描述

这个 skill 封装了从会话历史中识别出的常见工作流模式。

### 使用场景

当任务需要按顺序调用以下工具时，使用此 skill：

1. exec
2. read
2. write
2. exec

### 示例

\\\powershell
# 示例：使用此工作流
tool1 -> tool2 -> tool3
\\\

## 安装

此 skill 由 Distill 工作流发现任务自动创建。

- 创建时间: 2026-06-23 10:26:58
- 源: Distill 自动发现
- 置信度: 0.8
