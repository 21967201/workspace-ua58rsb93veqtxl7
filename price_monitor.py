#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摇粒绒面料价格全景监控系统
监控价格波动、异常预警、趋势预测
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

class PriceMonitor:
    def __init__(self):
        self.price_data = []
        self.history_file = Path("price_history.json")
        self.load_history()
    
    def load_history(self):
        """加载历史价格数据"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.price_data = json.load(f)
    
    def save_history(self):
        """保存价格数据"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.price_data, f, ensure_ascii=False, indent=2)
    
    def fetch_current_price(self):
        """获取当前摇粒绒面料价格（示例数据源）"""
        # 这里应该对接实际的面料价格API
        # 示例：返回模拟数据
        import random
        base_price = 28.5  # 基准价格（元/米）
        fluctuation = random.uniform(-2, 2)
        current_price = base_price + fluctuation
        
        return {
            'timestamp': datetime.now().isoformat(),
            'price': round(current_price, 2),
            'fabric_type': '摇粒绒面料',
            'unit': '元/米',
            'supplier': '示例供应商'
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
        
        # 简单线性回归
        n = len(prices)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(prices) / n
        
        numerator = sum((x[i] - x_mean) * (prices[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
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
        
        report = f"""# 摇粒绒面料价格全景监控报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 当前价格
- 价格: {current['price']} {current['unit']}
- 类型: {current['fabric_type']}
- 供应商: {current['supplier']}

## 异常预警
"""
        
        if anomaly:
            report += f"""⚠️ **检测到价格异常波动**
- 波动幅度: {anomaly['change_rate']}
- 当前价格: {anomaly['current_price']} 元/米
- 近期均价: {anomaly['avg_price']} 元/米
- 严重等级: {anomaly['severity']}
"""
        else:
            report += "✅ 价格波动正常，未检测到异常\n"
        
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
{'⚠️ 建议密切关注价格变化，考虑适时采购' if anomaly and anomaly['severity'] == '高' else '✅ 价格稳定，可按计划采购'}
"""
        
        return report

def main():
    monitor = PriceMonitor()
    report = monitor.generate_report()
    
    # 保存到文件
    output_file = f"价格全景监控_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"[SUCCESS] 报告已生成: {output_file}")
    print(report)
    
    # 返回报告路径供后续推送使用
    return output_file

if __name__ == "__main__":
    output = main()
    print(f"\n[INFO] 输出文件: {output}")
