import sys, json, os
sys.path.insert(0, r"D:\QClawX\data\workspace\skills\today-task\scripts")
from create_task_json import main as create_json
task_name = "周一知识管理综合"
task_content = """模块1-GBrain: bun/Windows崩溃(bun 1.2.17 pglite wasm)跳过
模块2-学术论文: Self-Evolving综述(Princeton/Tsinghua) P2、JitRL(ICML 2026 Oral) P1成本$98替代$3500、腾讯云Agent Memory横评 P2、Memoria(Git记忆) P2、Hermes Agent爆发 P1(周+32.5k Stars)
模块2-IMA同步: Token未授权(需用户在QClaw中连接腾讯文档)
模块3-报告已生成: 学术论文周度报告_2026-08-10.md + 知识库同步报告_2026-08-10.md"""
os.chdir(r"D:\QClawX\data\workspace-ua58rsb93veqtxl7")
create_json(task_name, task_content)
print("Done")
