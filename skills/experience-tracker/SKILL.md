# Experience Tracker Skill

## 功能描述
记录和分析技术突破集成的经验，优化未来集成决策。

## 数据结构
```json
{
  "integration_history": [
    {
      "tech_name": "headroom",
      "date": "2026-06-03",
      "priority": "P0",
      "score": 9.2,
      "integration_cost": "low",
      "status": "pending",
      "actual_benefit": null,
      "lessons_learned": []
    }
  ],
  "success_patterns": [
    "Low cost + High compatibility = High success rate",
    "P0 technologies should be integrated within 1 week"
  ],
  "failure_patterns": [
    "High cost + Low compatibility = High failure risk"
  ]
}
```

## 使用方式
1. 读取经验数据: `python skills/experience-tracker/track.py --read`
2. 记录集成经验: `python skills/experience-tracker/track.py --add --tech_name <name> --status <success/failed> --benefit <score>`
3. 分析成功模式: `python skills/experience-tracker/track.py --analyze`

## 自动化规则
- 每周自动分析集成经验
- 识别成功/失败模式
- 更新集成建议算法
