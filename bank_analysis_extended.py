#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行账单数据分析脚本 - 扩展版
作者：Python数据分析专家
功能：提供基于关键词的自动分类和其他高级分析功能
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from bank_analysis_phase2 import BankDataAnalyzer

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class ExtendedBankAnalyzer(BankDataAnalyzer):
    """扩展的银行账单分析器"""
    
    def __init__(self, csv_file_path):
        super().__init__(csv_file_path)
        
        # 定义分类规则字典
        self.category_rules = {
            '餐饮': ['美团', '饿了么', '肯德基', '麦当劳', '星巴克', '瑞幸', '餐厅', '饭店', '食堂', '外卖'],
            '交通': ['滴滴', '出租车', '地铁', '公交', '高铁', '火车', '飞机', '机票', '加油', '停车', '打车'],
            '购物': ['淘宝', '天猫', '京东', '拼多多', '苏宁', '当当', '超市', '商场', '购物'],
            '医疗': ['医院', '药店', '诊所', '体检', '医疗', '疫苗', '挂号'],
            '娱乐': ['电影', '游戏', '娱乐', '健身', '运动', 'KTV', '旅游', '酒店'],
            '生活': ['水费', '电费', '燃气费', '物业费', '房租', '话费', '网费', '快递'],
            '金融': ['理财', '保险', '基金', '股票', '投资', '还款', '贷款'],
            '教育': ['培训', '学费', '书费', '教育', '考试'],
            '家居': ['装修', '家具', '家电', '日用品'],
            '服装': ['服装', '鞋子', '包包', '化妆品']
        }
    
    def auto_categorize_transactions(self):
        """
        基于关键词自动分类交易
        """
        print("\n" + "=" * 50)
        print("🤖 基于关键词自动分类交易")
        print("=" * 50)
        
        if self.clean_data is None:
            print("❌ 请先进行数据预处理")
            return
        
        df = self.clean_data.copy()
        
        # 创建自动分类列
        df['自动分类'] = '其他'
        
        # 需要检查的文本列
        text_columns = ['交易详情', '交易场所', '对方户名']
        
        for category, keywords in self.category_rules.items():
            for col in text_columns:
                if col in df.columns:
                    for keyword in keywords:
                        mask = df[col].str.contains(keyword, case=False, na=False)
                        df.loc[mask, '自动分类'] = category
        
        # 统计分类结果
        category_stats = df['自动分类'].value_counts()
        print("📊 自动分类统计:")
        for category, count in category_stats.items():
            percentage = (count / len(df)) * 100
            print(f"   {category}: {count} 笔 ({percentage:.1f}%)")
        
        # 按自动分类统计支出
        expense_by_auto_category = df[df['支出'] > 0].groupby('自动分类')['支出'].sum().sort_values(ascending=False)
        print(f"\n💸 按自动分类的支出统计:")
        for category, amount in expense_by_auto_category.items():
            percentage = (amount / expense_by_auto_category.sum()) * 100
            print(f"   {category}: ¥{amount:,.2f} ({percentage:.1f}%)")
        
        # 更新数据
        self.clean_data = df
        return category_stats, expense_by_auto_category
    
    def analyze_seasonal_patterns(self):
        """季节性消费模式分析"""
        print("\n" + "=" * 50)
        print("🌟 季节性消费模式分析")
        print("=" * 50)
        
        df = self.clean_data
        
        # 按季度分析
        seasonal_analysis = df.groupby(['年份', '季度']).agg({
            '收入': 'sum',
            '支出': 'sum',
            '净金额': 'sum'
        }).round(2)
        
        print("📊 季度收支分析:")
        print(seasonal_analysis.to_string())
        
        # 按月份分析（跨年度）
        monthly_pattern = df.groupby('月份').agg({
            '收入': 'mean',
            '支出': 'mean',
            '净金额': 'mean'
        }).round(2)
        
        print(f"\n📅 月度平均模式分析:")
        month_names = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        for i, (month, row) in enumerate(monthly_pattern.iterrows()):
            print(f"   {month_names[i]}: 平均收入¥{row['收入']:,.2f}, 平均支出¥{row['支出']:,.2f}, 平均净收入¥{row['净金额']:,.2f}")
        
        return seasonal_analysis, monthly_pattern
    
    def analyze_spending_frequency(self):
        """消费频率分析"""
        print("\n" + "=" * 50)
        print("📈 消费频率分析")
        print("=" * 50)
        
        df = self.clean_data
        
        # 按日期统计每日交易次数
        daily_transactions = df.groupby(df['日期'].dt.date).size()
        
        print(f"📊 交易频率统计:")
        print(f"   平均每日交易次数: {daily_transactions.mean():.1f}")
        print(f"   最高单日交易次数: {daily_transactions.max()}")
        print(f"   最低单日交易次数: {daily_transactions.min()}")
        
        # 找出交易最频繁的日期
        busiest_days = daily_transactions.nlargest(5)
        print(f"\n🔥 交易最频繁的5天:")
        for date, count in busiest_days.items():
            print(f"   {date}: {count} 笔交易")
        
        # 分析工作日vs周末的消费模式
        df['星期几'] = df['日期'].dt.dayofweek  # 0=Monday, 6=Sunday
        df['是否工作日'] = df['星期几'] < 5
        
        workday_vs_weekend = df.groupby('是否工作日').agg({
            '支出': ['sum', 'mean', 'count']
        }).round(2)
        
        print(f"\n📅 工作日vs周末消费对比:")
        print("   工作日:" if True in workday_vs_weekend.index else "")
        if True in workday_vs_weekend.index:
            workday_data = workday_vs_weekend.loc[True]
            print(f"     总支出: ¥{workday_data[('支出', 'sum')]:,.2f}")
            print(f"     平均支出: ¥{workday_data[('支出', 'mean')]:,.2f}")
            print(f"     交易次数: {workday_data[('支出', 'count')]}")
        
        print("   周末:" if False in workday_vs_weekend.index else "")
        if False in workday_vs_weekend.index:
            weekend_data = workday_vs_weekend.loc[False]
            print(f"     总支出: ¥{weekend_data[('支出', 'sum')]:,.2f}")
            print(f"     平均支出: ¥{weekend_data[('支出', 'mean')]:,.2f}")
            print(f"     交易次数: {weekend_data[('支出', 'count')]}")
        
        return daily_transactions, workday_vs_weekend
    
    def analyze_counterparty_patterns(self):
        """交易对方分析"""
        print("\n" + "=" * 50)
        print("🏢 交易对方分析")
        print("=" * 50)
        
        df = self.clean_data
        
        # 收入对方分析
        income_counterparties = df[df['收入'] > 0].groupby('对方户名').agg({
            '收入': ['sum', 'count']
        }).round(2)
        income_counterparties.columns = ['总收入', '交易次数']
        income_counterparties = income_counterparties.sort_values('总收入', ascending=False).head(10)
        
        print("💰 主要收入来源 (Top 10):")
        for name, row in income_counterparties.iterrows():
            print(f"   {str(name)[:40]}: ¥{row['总收入']:,.2f} ({int(row['交易次数'])}笔)")
        
        # 支出对方分析
        expense_counterparties = df[df['支出'] > 0].groupby('对方户名').agg({
            '支出': ['sum', 'count']
        }).round(2)
        expense_counterparties.columns = ['总支出', '交易次数']
        expense_counterparties = expense_counterparties.sort_values('总支出', ascending=False).head(10)
        
        print(f"\n💸 主要支出对象 (Top 10):")
        for name, row in expense_counterparties.iterrows():
            print(f"   {str(name)[:40]}: ¥{row['总支出']:,.2f} ({int(row['交易次数'])}笔)")
        
        return income_counterparties, expense_counterparties
    
    def generate_extended_report(self):
        """生成扩展分析报告"""
        print("\n" + "=" * 70)
        print("🚀 生成扩展财务分析报告")
        print("=" * 70)
        
        # 先运行基础分析
        base_results = super().generate_report()
        
        # 运行扩展分析
        category_stats, expense_by_auto_category = self.auto_categorize_transactions()
        seasonal_analysis, monthly_pattern = self.analyze_seasonal_patterns()
        daily_transactions, workday_vs_weekend = self.analyze_spending_frequency()
        income_counterparties, expense_counterparties = self.analyze_counterparty_patterns()
        
        print("\n" + "=" * 70)
        print("✅ 扩展财务分析报告生成完成！")
        print("=" * 70)
        
        # 合并结果
        extended_results = base_results.copy()
        extended_results.update({
            'auto_categories': (category_stats, expense_by_auto_category),
            'seasonal': (seasonal_analysis, monthly_pattern),
            'frequency': (daily_transactions, workday_vs_weekend),
            'counterparties': (income_counterparties, expense_counterparties)
        })
        
        return extended_results

def create_category_classification_template():
    """创建分类规则模板"""
    template = """
# 交易分类规则配置文件
# 您可以根据需要修改这些关键词来改进自动分类效果

category_rules = {
    '餐饮': ['美团', '饿了么', '肯德基', '麦当劳', '星巴克', '瑞幸', '餐厅', '饭店', '食堂', '外卖'],
    '交通': ['滴滴', '出租车', '地铁', '公交', '高铁', '火车', '飞机', '机票', '加油', '停车', '打车'],
    '购物': ['淘宝', '天猫', '京东', '拼多多', '苏宁', '当当', '超市', '商场', '购物'],
    '医疗': ['医院', '药店', '诊所', '体检', '医疗', '疫苗', '挂号'],
    '娱乐': ['电影', '游戏', '娱乐', '健身', '运动', 'KTV', '旅游', '酒店'],
    '生活': ['水费', '电费', '燃气费', '物业费', '房租', '话费', '网费', '快递'],
    '金融': ['理财', '保险', '基金', '股票', '投资', '还款', '贷款'],
    '教育': ['培训', '学费', '书费', '教育', '考试'],
    '家居': ['装修', '家具', '家电', '日用品'],
    '服装': ['服装', '鞋子', '包包', '化妆品']
}

# 使用方法：
# 1. 修改上述关键词列表以适应您的交易数据
# 2. 添加新的分类和关键词
# 3. 在ExtendedBankAnalyzer中加载此配置
"""
    
    with open('category_rules_template.py', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("📝 已创建分类规则模板文件: category_rules_template.py")

def main():
    """主函数"""
    print("=" * 70)
    print("🚀 银行账单数据分析系统 - 扩展版")
    print("=" * 70)
    
    # 初始化扩展分析器
    analyzer = ExtendedBankAnalyzer("2023-2025May.csv")
    
    # 加载数据
    if not analyzer.load_data():
        return
    
    # 数据预处理
    if not analyzer.clean_and_preprocess_data():
        return
    
    # 生成扩展报告
    results = analyzer.generate_extended_report()
    
    # 创建分类规则模板
    create_category_classification_template()
    
    print(f"\n🎉 扩展分析完成！")
    print(f"📊 可视化图表: bank_analysis_charts.png")
    print(f"📝 分类规则模板: category_rules_template.py")
    print(f"💾 完整数据已保存在 analyzer.clean_data 中")

if __name__ == "__main__":
    main() 