# Hermes CLI 修复记录（2026-08-04）

## 问题

`runtime:hermes:chat` IPC 报错：
```
[hermes-paths] 找不到 Hermes CLI 模块: D:\QClaw\v0.2.35.624\resources\hermes\libs\hermes_cli_main_.py
```

## 根因

hermes-sdk wheel 打包遗漏：
- `resources/hermes/libs/` 只装入了 `hermes_sdk-2026.6.19.dev12.dist-info/`（元数据）
- 但 RECORD 中 26 个实际包文件 **未部署到磁盘**
- 其中最关键的是 `hermes_cli/__main__.py`（`python -m hermes_cli` 入口）缺失
- Electron 主进程引用 `hermes_cli_main_.py`（带下划线尾缀）——该文件也不存在
- `hermes-paths` 只是运行时 logger 名称，非真实模块（全盘 0 命中）

## 修复动作

### 1. 创建兼容入口（499 字节）
`D:\QClaw\v0.2.35.624\resources\hermes\libs\hermes_cli_main_.py`
```python
from hermes_cli.main import main
if __name__ == "__main__":
    main()
```

### 2. 从 hermes_2.tar 提取 10 个缺失文件
- `hermes_cli/__main__.py`（194B，关键入口）
- `hermes_cli/memory_providers.py`（4652B）
- `plugins/cron/__init__.py`（12699B）
- `plugins/cron/chronos/__init__.py`（9525B）
- `plugins/cron/chronos/_nas_client.py`（4762B）
- `plugins/cron/chronos/plugin.yaml`（467B）
- `plugins/cron/chronos/verify.py`（3952B）
- `agent/gemini_cloudcode_adapter.py`（34078B）
- `agent/google_code_assist.py`（16854B）
- `agent/google_oauth.py`（38620B）

### 3. 从 hermes_1.tar 提取 16 个缺失文件
- `gateway/platforms/`：dingtalk、email、feishu、feishu_comment、feishu_comment_rules、feishu_meeting_invite、matrix、slack、sms、telegram、telegram_network、wecom、wecom_callback、wecom_crypto、whatsapp（15 个）
- `tools/mixture_of_agents_tool.py`（22166B）

## 验证结果（全部通过）

| 检查项 | 结果 |
|---|---|
| RECORD 797 文件完整性 | ✅ 0 缺失 |
| 20 个修复文件全部就位 | ✅ |
| `hermes_cli_main_` import | ✅ 749ms |
| `hermes_cli.__main__` import | ✅ 2ms |
| `hermes_cli.main` import | ✅ 0ms |
| gateway.platforms 全部 import | ✅ |
| plugins.cron / chronos | ✅ |
| agent 适配器 | ✅ |
| compat entry `main` callable | ✅ True |
| hermes.exe / agent / acp shim | ✅ 46080B 存在 |

## 影响

- `runtime:hermes:chat` IPC 路径现在能找到正确入口
- 所有缺失的 gateway 平台模块（飞书/微信/钉钉/Slack/Telegram 等）已恢复
- cron 插件（plugins/cron/chronos）已恢复
- 修复为文件级补丁，无需重装 QClaw

## 注意

- `hermes-paths` logger 名称仍不存在对应模块文件——但这是正常的（logger 名可以任意，报错源于文件缺失，现已解决）
- 若 QClaw 后续更新会覆盖 `resources/`，此修复需在更新后重做（可留存脚本）
- 建议反馈给 QClaw 官方：hermes-sdk wheel 打包时未完整部署 RECORD 文件
