#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trajectory Eval — 轨迹评估 (Harness 支柱4)
全轨迹质量评估：推理层(Plan) + 行动层(Execute) + 端到端(Result)

用法:
  python trajectory_eval.py --task tech-monitor --report report.md
  python trajectory_eval.py --task tech-monitor --report report.md --scores 8,7,9
  python trajectory_eval.py --history             # 查看历史评估记录
"""
import argparse
import datetime
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAJ_DIR = os.path.join(BASE_DIR, "..", "memory", "trajectory")

# 权重
W_PLAN = 0.3
W_EXEC = 0.4
W_RESULT = 0.3


def grade(score: float) -> str:
    if score >= 8.5:
        return "A"
    if score >= 7.0:
        return "B"
    if score >= 5.0:
        return "C"
    return "D"


def evaluate(task: str, report: str, scores=None):
    """执行轨迹评估。scores: (plan, exec, result) 三元组，缺省自动推导。"""
    os.makedirs(TRAJ_DIR, exist_ok=True)
    today = datetime.date.today().isoformat()

    # 自动推导评分 (基于文件存在性与大小)
    if scores is None:
        plan_score = 8 if os.path.exists(os.path.join(BASE_DIR, "..", "PLAN-tech-monitor.md")) else 5
        exec_score = 7
        result_score = 8 if report and os.path.exists(report) else 5
    else:
        plan_score, exec_score, result_score = scores

    overall = W_PLAN * plan_score + W_EXEC * exec_score + W_RESULT * result_score
    g = grade(overall)

    record = {
        "task": task,
        "date": today,
        "report": report,
        "scores": {"plan": plan_score, "execution": exec_score, "result": result_score},
        "overall": round(overall, 2),
        "grade": g,
    }

    out_file = os.path.join(TRAJ_DIR, f"{today}-{task}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(json.dumps(record, ensure_ascii=False, indent=2))
    if g == "D":
        print("⚠️ D级评估 → 触发改进机制: 记录到 self-improving/corrections.md")
    return record


def show_history():
    if not os.path.isdir(TRAJ_DIR):
        print("无评估记录")
        return
    for fn in sorted(os.listdir(TRAJ_DIR)):
        fp = os.path.join(TRAJ_DIR, fn)
        with open(fp, "r", encoding="utf-8") as f:
            r = json.load(f)
        print(f"{r['date']} | {r['task']} | overall={r['overall']} | grade={r['grade']}")


def main():
    ap = argparse.ArgumentParser(description="Trajectory Eval — 轨迹评估")
    ap.add_argument("--task", help="任务名称")
    ap.add_argument("--report", help="报告文件路径")
    ap.add_argument("--scores", help="手动评分 plan,exec,result (如 8,7,9)")
    ap.add_argument("--history", action="store_true", help="查看历史")
    args = ap.parse_args()

    if args.history:
        show_history()
        return

    if not args.task:
        print("错误: 需要 --task 参数", file=sys.stderr)
        sys.exit(1)

    scores = None
    if args.scores:
        scores = tuple(float(x) for x in args.scores.split(","))
    evaluate(args.task, args.report or "", scores)


if __name__ == "__main__":
    main()
