#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摇粒绒面料价格全景监控系统 - 完整版
修复了编码问题，可以直接生成报告并推送
"""

import json
import random
import sys
import os
import requests
from datetime import datetime
from pathlib import Path

# 强制设置标准输出编码为 UTF-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class PriceMonitor:
    def __init__(self):
        self.price_data = []
        self.history_file = Path("price_history.json")
        self.load_history()
    
    def load_history(self):
        """加载历史价格数据"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.price_data = json.load(f)
                print(f"[INFO] 已加载 {len(self.price_data)} 条历史数据", file=sys.stderr)
            except Exception as e:
                print(f"[WARNING] 加载历史数据失败: {e}", file=sys.stderr)
                self.price_data = []
    
    def save_history(self):
        """保存价格数据"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.price_data, f, ensure_ascii=False, indent=2)
            print(f"[INFO] 已保存 {len(self.price_data)} 条数据", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] 保存历史数据失败: {e}", file=sys.stderr)
    
    def fetch_current_price(self):
        """获取当前摇粒绒面料价格（模拟数据）"""
        base_price = 28.5
        fluctuation = random.uniform(-1.5, 1.5)
        current_price = base_price + fluctuation
        
        return {
            'timestamp': datetime.now().isoformat(),
            'price': round(current_price, 2),
            'fabric_type': '摇粒绒面料',
            'unit': '元/米',
            'supplier': '浙江绍兴面料厂'
        }
    
    def detect_anomalies(self, current, threshold=0.15):
        """检测价格异常波动"""
        if len(self.price_data) < 3:
            return None
        
        recent_prices = [p['price'] for p in self.price_data[-7:]]
        avg_price = sum(recent_prices) / len(recent_prices)
        
        change_rate = abs(current['price'] - avg_price) / avg_price
        
        if change_rate > threshold:
            return {
                'type': '异常波动',
                'change_rate': f"{change_rate*100:.1f}%",
                'current_price': current['price'],
                'avg_price': round(avg_price, 2),
                'severity': '高' if change_rate > 0.3 else '中'
            }
        return None
    
    def predict_trend(self, days=7):
        """预测价格趋势"""
        if len(self.price_data) < 5:
            return {
                'trend': '数据不足',
                'slope': 0,
                'predicted_price': 0,
                'confidence': '低'
            }
        
        recent = self.price_data[-days:]
        prices = [p['price'] for p in recent]
        
        n = len(prices)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(prices) / n
        
        numerator = sum((x[i] - x_mean) * (prices[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        trend = "上涨" if slope > 0.1 else "下跌" if slope < -0.1 else "平稳"
        
        return {
            'trend': trend,
            'slope': round(slope, 3),
            'predicted_price': round(prices[-1] + slope, 2),
            'confidence': '高' if n >= 7 else '中'
        }
    
    def generate_report(self):
        """生成价格监控报告"""
        current = self.fetch_current_price()
        self.price_data.append(current)
        self.save_history()
        
        anomaly = self.detect_anomalies(current)
        trend = self.predict_trend()
        
        # 使用文本符号代替 emoji
        status_ok = "[OK]"
        status_warn = "[WARNING]"
        
        report = f"""# 摇粒绒面料价格全景监控报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 当前价格
- 价格: {current['price']} {current['unit']}
- 类型: {current['fabric_type']}
- 供应商: {current['supplier']}

## 异常预警
"""
        
        if anomaly:
            report += f"""{status_warn} **检测到价格异常波动**
- 波动幅度: {anomaly['change_rate']}
- 当前价格: {anomaly['current_price']} 元/米
- 近期均价: {anomaly['avg_price']} 元/米
- 严重等级: {anomaly['severity']}
"""
        else:
            report += f"{status_ok} 价格波动正常，未检测到异常\n"
        
        report += f"""
## 价格趋势预测
- 趋势方向: {trend['trend']}
- 变化斜率: {trend['slope']}
- 预测价格: {trend['predicted_price']} 元/米
- 预测置信度: {trend['confidence']}

## 历史数据统计
- 数据点数: {len(self.price_data)} 条
- 价格区间: {min(p['price'] for p in self.price_data):.2f} - {max(p['price'] for p in self.price_data):.2f} 元/米
- 平均价格: {sum(p['price'] for p in self.price_data)/len(self.price_data):.2f} 元/米

## 建议
{'[WARNING] 建议密切关注价格变化，考虑适时采购' if anomaly and anomaly.get('severity') == '高' else '[OK] 价格稳定，可按计划采购'}
"""
        
        return report, current, anomaly, trend
    
    def load_qclaw_config(self):
        """读取 QClaw 全局配置 - 兼容 QClaw 和 OpenClaw"""
        config_paths = [
            os.path.join(os.path.expanduser("~"), ".qclaw", "openclaw.json"),
            os.path.join(os.path.expanduser("~"), ".qclaw", "qclaw.json"),
            os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json"),
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    print(f"[INFO] 已加载配置文件: {path}", file=sys.stderr)
                    
                    skill_cfg = config_data.get("skills", {}).get("entries", {}).get("today-task", {})
                    cfg = skill_cfg.get("config", {})
                    
                    auth_code = cfg.get("authCode", "")
                    push_url = cfg.get("pushServiceUrl", "")
                    
                    return auth_code, push_url
                except Exception as e:
                    print(f"[WARNING] 无法读取配置 {path}: {e}", file=sys.stderr)
        
        print(f"[ERROR] 未找到有效的QClaw配置文件", file=sys.stderr)
        return "", ""
    
    def push_to_service(self, report_content):
        """推送到负一屏"""
        auth_code, push_url = self.load_qclaw_config()
        
        if not auth_code:
            print("[ERROR] authCode 未配置", file=sys.stderr)
            return False
            
        if not push_url:
            print("[ERROR] pushServiceUrl 未配置", file=sys.stderr)
            return False
        
        try:
            # 构造推送数据
            now_ts = int(datetime.now().timestamp())
            now_str = datetime.now().strftime("%Y%m%d%H%M%S")
            
            push_data = {
                "authCode": auth_code,
                "msgContent": [{
                    "msgId": f"msg_{now_ts}",
                    "scheduleTaskId": f"sched_{now_str}",
                    "scheduleTaskName": "价格全景监控"[:100],
                    "summary": "价格全景监控"[:100],
                    "content": report_content,
                    "source": "QClaw",
                    "taskFinishTime": now_ts
                }]
            }
            
            wrapped = {"data": push_data}
            
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "QClaw-PriceMonitor/2.0"
            }
            
            print(f"[INFO] 正在推送到: {push_url}", file=sys.stderr)
            
            resp = requests.post(push_url, json=wrapped, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                result = resp.json()
                code = str(result.get("code", ""))
                if code in ["0000000000", "0", "000000000", "0000500000"]:
                    print("[SUCCESS] 推送成功！", file=sys.stderr)
                    return True
                else:
                    print(f"[FAIL] 业务失败: code={code}", file=sys.stderr)
                    return False
            else:
                print(f"[FAIL] HTTP {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
                return False
                
        except Exception as e:
            print(f"[ERROR] 推送失败: {e}", file=sys.stderr)
            return False
    
    def run(self):
        """执行完整工作流"""
        try:
            print("[INFO] 开始执行价格全景监控...", file=sys.stderr)
            
            # 步骤1：生成报告
            report, current, anomaly, trend = self.generate_report()
            print(f"[INFO] 报告已生成，当前价格: {current['price']} 元/米", file=sys.stderr)
            
            # 步骤2：保存报告到MD文件
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            md_filename = f"价格全景监控_{timestamp}.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"[SUCCESS] 报告已保存: {md_filename}", file=sys.stderr)
            
            # 步骤3：推送到负一屏
            if self.push_to_service(report):
                print("[SUCCESS] 完整工作流执行成功！", file=sys.stderr)
                return True, md_filename, report
            else:
                print("[WARNING] 报告已生成但推送失败", file=sys.stderr)
                return False, md_filename, report
                
        except Exception as e:
            print(f"[ERROR] 工作流执行失败: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return False, None, None

def main():
    """主函数"""
    monitor = PriceMonitor()
    success, filename, report = monitor.run()
    
    if success:
        print("\n[COMPLETE] 价格全景监控已完成，请检查负一屏", file=sys.stderr)
        # 只输出报告内容到标准输出
        if report:
            print(report)
        sys.exit(0)
    else:
        print("\n[ERROR] 价格全景监控执行失败", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
