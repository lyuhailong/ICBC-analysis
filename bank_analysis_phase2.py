#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行账单数据分析脚本 - 第二阶段：数据预处理与完整分析
作者：Python数据分析专家
目标：分析2023-2025年5月的银行账单数据
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class BankDataAnalyzer:
    """银行账单数据分析器"""
    
    def __init__(self, csv_file_path):
        """
        初始化分析器
        
        参数:
            csv_file_path (str): CSV文件路径
        """
        self.csv_file_path = csv_file_path
        self.raw_data = None
        self.clean_data = None
        
    def load_data(self):
        """加载原始数据"""
        print("📁 正在加载数据...")
        try:
            self.raw_data = pd.read_csv(self.csv_file_path)
            print(f"✅ 数据加载成功！共有 {len(self.raw_data)} 行数据")
            return True
        except Exception as e:
            print(f"❌ 数据加载失败：{str(e)}")
            return False
    
    def clean_and_preprocess_data(self):
        """
        数据清洗与预处理
        """
        print("\n" + "=" * 50)
        print("🧹 开始数据清洗与预处理")
        print("=" * 50)
        
        if self.raw_data is None:
            print("❌ 请先加载数据")
            return False
        
        # 复制原始数据
        df = self.raw_data.copy()
        
        # 0. 过滤掉汇总行和无效行
        print("🔍 过滤无效数据...")
        original_count = len(df)
        
        # 过滤掉交易日期为空或包含汇总信息的行
        df = df[df['交易日期'].notna()]  # 去除空值
        df = df[~df['交易日期'].str.contains('合计|总计|小计', na=False)]  # 去除汇总行
        df = df[df['交易日期'].str.match(r'^\d{4}-\d{2}-\d{2}', na=False)]  # 只保留日期格式的行
        
        filtered_count = len(df)
        print(f"   原始数据: {original_count} 行")
        print(f"   过滤后数据: {filtered_count} 行") 
        print(f"   移除了 {original_count - filtered_count} 行无效数据")
        
        # 1. 处理日期列
        print("📅 处理日期列...")
        df['交易日期'] = df['交易日期'].str.strip()  # 去除首尾空格
        df['日期'] = pd.to_datetime(df['交易日期'], format='%Y-%m-%d')
        print(f"   日期范围: {df['日期'].min()} 到 {df['日期'].max()}")
        
        # 2. 处理金额列
        print("💰 处理金额列...")
        
        # 清理收入列
        df['收入_清理'] = df['记账金额(收入)'].astype(str).str.strip()
        df['收入_清理'] = df['收入_清理'].replace(['', 'nan', 'NaN'], '0')
        df['收入_清理'] = df['收入_清理'].str.replace(',', '')
        df['收入'] = pd.to_numeric(df['收入_清理'], errors='coerce').fillna(0)
        
        # 清理支出列
        df['支出_清理'] = df['记账金额(支出)'].astype(str).str.strip()
        df['支出_清理'] = df['支出_清理'].replace(['', 'nan', 'NaN'], '0')
        df['支出_清理'] = df['支出_清理'].str.replace(',', '')
        df['支出'] = pd.to_numeric(df['支出_清理'], errors='coerce').fillna(0)
        
        # 3. 创建交易类型列
        df['交易类型'] = df.apply(lambda row: '收入' if row['收入'] > 0 else '支出' if row['支出'] > 0 else '未知', axis=1)
        
        # 4. 创建净金额列（收入为正，支出为负）
        df['净金额'] = df['收入'] - df['支出']
        
        # 5. 处理交易类别（摘要列）
        df['交易类别'] = df['摘要'].fillna('未分类').str.strip()
        
        # 6. 添加时间维度列
        df['年份'] = df['日期'].dt.year
        df['月份'] = df['日期'].dt.month
        df['年月'] = df['日期'].dt.to_period('M')
        df['季度'] = df['日期'].dt.quarter
        
        # 7. 处理余额列
        df['余额_清理'] = df['余额'].astype(str).str.strip().str.replace(',', '')
        df['账户余额'] = pd.to_numeric(df['余额_清理'], errors='coerce')
        
        # 8. 删除临时列
        columns_to_drop = ['收入_清理', '支出_清理', '余额_清理']
        df = df.drop(columns=columns_to_drop)
        
        # 保存清洗后的数据
        self.clean_data = df
        
        # 显示清洗结果
        print(f"✅ 数据清洗完成！")
        print(f"   处理后数据形状: {df.shape}")
        print(f"   收入记录数: {(df['收入'] > 0).sum()}")
        print(f"   支出记录数: {(df['支出'] > 0).sum()}")
        print(f"   总收入: ¥{df['收入'].sum():,.2f}")
        print(f"   总支出: ¥{df['支出'].sum():,.2f}")
        print(f"   净余额: ¥{df['净金额'].sum():,.2f}")
        
        return True
    
    def analyze_overall_summary(self):
        """总体收支情况分析"""
        print("\n" + "=" * 50)
        print("📊 总体收支情况分析")
        print("=" * 50)
        
        df = self.clean_data
        
        total_income = df['收入'].sum()
        total_expense = df['支出'].sum()
        net_balance = total_income - total_expense
        
        income_transactions = (df['收入'] > 0).sum()
        expense_transactions = (df['支出'] > 0).sum()
        
        print(f"💰 总收入: ¥{total_income:,.2f} ({income_transactions} 笔交易)")
        print(f"💸 总支出: ¥{total_expense:,.2f} ({expense_transactions} 笔交易)")
        print(f"💵 净余额: ¥{net_balance:,.2f}")
        print(f"📈 储蓄率: {(net_balance/total_income)*100:.1f}%" if total_income > 0 else "无法计算储蓄率")
        
        # 平均交易金额
        avg_income = df[df['收入'] > 0]['收入'].mean()
        avg_expense = df[df['支出'] > 0]['支出'].mean()
        print(f"📊 平均收入金额: ¥{avg_income:,.2f}")
        print(f"📊 平均支出金额: ¥{avg_expense:,.2f}")
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'income_transactions': income_transactions,
            'expense_transactions': expense_transactions
        }
    
    def analyze_monthly_trends(self):
        """月度趋势分析"""
        print("\n" + "=" * 50)
        print("📅 月度收支趋势分析")
        print("=" * 50)
        
        df = self.clean_data
        
        # 按月聚合
        monthly_summary = df.groupby('年月').agg({
            '收入': 'sum',
            '支出': 'sum',
            '净金额': 'sum'
        }).round(2)
        
        monthly_summary['储蓄率(%)'] = (monthly_summary['净金额'] / monthly_summary['收入'] * 100).round(1)
        monthly_summary['储蓄率(%)'] = monthly_summary['储蓄率(%)'].fillna(0)
        
        print("📊 月度收支汇总表:")
        print(monthly_summary.to_string())
        
        # 找出收入最高和最低的月份
        max_income_month = monthly_summary['收入'].idxmax()
        min_income_month = monthly_summary['收入'].idxmin()
        max_expense_month = monthly_summary['支出'].idxmax()
        min_expense_month = monthly_summary['支出'].idxmin()
        
        print(f"\n💡 关键发现:")
        print(f"   收入最高月份: {max_income_month} (¥{monthly_summary.loc[max_income_month, '收入']:,.2f})")
        print(f"   收入最低月份: {min_income_month} (¥{monthly_summary.loc[min_income_month, '收入']:,.2f})")
        print(f"   支出最高月份: {max_expense_month} (¥{monthly_summary.loc[max_expense_month, '支出']:,.2f})")
        print(f"   支出最低月份: {min_expense_month} (¥{monthly_summary.loc[min_expense_month, '支出']:,.2f})")
        
        return monthly_summary
    
    def analyze_yearly_trends(self):
        """年度趋势分析"""
        print("\n" + "=" * 50)
        print("📆 年度收支趋势分析")
        print("=" * 50)
        
        df = self.clean_data
        
        # 按年聚合
        yearly_summary = df.groupby('年份').agg({
            '收入': 'sum',
            '支出': 'sum',
            '净金额': 'sum'
        }).round(2)
        
        yearly_summary['储蓄率(%)'] = (yearly_summary['净金额'] / yearly_summary['收入'] * 100).round(1)
        yearly_summary['储蓄率(%)'] = yearly_summary['储蓄率(%)'].fillna(0)
        
        print("📊 年度收支汇总表:")
        print(yearly_summary.to_string())
        
        # 计算年度增长率
        if len(yearly_summary) > 1:
            print(f"\n📈 年度增长率分析:")
            for i in range(1, len(yearly_summary)):
                prev_year = yearly_summary.index[i-1]
                curr_year = yearly_summary.index[i]
                
                income_growth = ((yearly_summary.loc[curr_year, '收入'] - yearly_summary.loc[prev_year, '收入']) / yearly_summary.loc[prev_year, '收入'] * 100)
                expense_growth = ((yearly_summary.loc[curr_year, '支出'] - yearly_summary.loc[prev_year, '支出']) / yearly_summary.loc[prev_year, '支出'] * 100)
                
                print(f"   {prev_year} → {curr_year}: 收入增长 {income_growth:+.1f}%, 支出增长 {expense_growth:+.1f}%")
        
        return yearly_summary
    
    def analyze_categories(self):
        """交易类别分析"""
        print("\n" + "=" * 50)
        print("🏷️  交易类别分析")
        print("=" * 50)
        
        df = self.clean_data
        
        # 收入类别分析
        income_categories = df[df['收入'] > 0].groupby('交易类别').agg({
            '收入': ['sum', 'count', 'mean']
        }).round(2)
        income_categories.columns = ['总金额', '交易次数', '平均金额']
        income_categories['占比(%)'] = (income_categories['总金额'] / income_categories['总金额'].sum() * 100).round(1)
        income_categories = income_categories.sort_values('总金额', ascending=False)
        
        print("💰 收入类别分析:")
        print(income_categories.to_string())
        
        # 支出类别分析
        expense_categories = df[df['支出'] > 0].groupby('交易类别').agg({
            '支出': ['sum', 'count', 'mean']
        }).round(2)
        expense_categories.columns = ['总金额', '交易次数', '平均金额']
        expense_categories['占比(%)'] = (expense_categories['总金额'] / expense_categories['总金额'].sum() * 100).round(1)
        expense_categories = expense_categories.sort_values('总金额', ascending=False)
        
        print(f"\n💸 支出类别分析:")
        print(expense_categories.to_string())
        
        return income_categories, expense_categories
    
    def analyze_top_transactions(self, n=10):
        """重要交易识别"""
        print("\n" + "=" * 50)
        print(f"🔝 重要交易识别 (Top {n})")
        print("=" * 50)
        
        df = self.clean_data
        
        # Top收入交易
        top_income = df[df['收入'] > 0].nlargest(n, '收入')[['日期', '交易类别', '收入', '对方户名']].round(2)
        print(f"💰 金额最高的{n}笔收入:")
        for idx, row in top_income.iterrows():
            print(f"   {row['日期'].strftime('%Y-%m-%d')} | ¥{row['收入']:,.2f} | {row['交易类别']} | {str(row['对方户名'])[:30]}")
        
        # Top支出交易
        top_expense = df[df['支出'] > 0].nlargest(n, '支出')[['日期', '交易类别', '支出', '对方户名']].round(2)
        print(f"\n💸 金额最高的{n}笔支出:")
        for idx, row in top_expense.iterrows():
            print(f"   {row['日期'].strftime('%Y-%m-%d')} | ¥{row['支出']:,.2f} | {row['交易类别']} | {str(row['对方户名'])[:30]}")
        
        return top_income, top_expense
    
    def create_visualizations(self):
        """创建可视化图表"""
        print("\n" + "=" * 50)
        print("📈 生成可视化图表")
        print("=" * 50)
        
        df = self.clean_data
        
        # 设置图表样式
        plt.style.use('default')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. 月度收支趋势图
        plt.subplot(2, 3, 1)
        monthly_data = df.groupby('年月').agg({'收入': 'sum', '支出': 'sum'})
        x_labels = [str(period) for period in monthly_data.index]
        
        plt.plot(range(len(monthly_data)), monthly_data['收入'], marker='o', linewidth=2, label='收入', color='green')
        plt.plot(range(len(monthly_data)), monthly_data['支出'], marker='s', linewidth=2, label='支出', color='red')
        plt.title('月度收支趋势', fontsize=14, fontweight='bold')
        plt.xlabel('月份')
        plt.ylabel('金额 (¥)')
        plt.legend()
        plt.xticks(range(len(monthly_data)), x_labels, rotation=45)
        plt.grid(True, alpha=0.3)
        
        # 2. 年度收支对比
        plt.subplot(2, 3, 2)
        yearly_data = df.groupby('年份').agg({'收入': 'sum', '支出': 'sum'})
        x = range(len(yearly_data))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], yearly_data['收入'], width, label='收入', color='lightgreen')
        plt.bar([i + width/2 for i in x], yearly_data['支出'], width, label='支出', color='lightcoral')
        plt.title('年度收支对比', fontsize=14, fontweight='bold')
        plt.xlabel('年份')
        plt.ylabel('金额 (¥)')
        plt.legend()
        plt.xticks(x, yearly_data.index)
        
        # 3. 支出类别饼图
        plt.subplot(2, 3, 3)
        expense_by_category = df[df['支出'] > 0].groupby('交易类别')['支出'].sum().sort_values(ascending=False)
        # 只显示前8个类别，其余归为"其他"
        if len(expense_by_category) > 8:
            top_categories = expense_by_category.head(7)
            others = expense_by_category.tail(-7).sum()
            plot_data = pd.concat([top_categories, pd.Series([others], index=['其他'])])
        else:
            plot_data = expense_by_category
        
        plt.pie(plot_data.values, labels=plot_data.index, autopct='%1.1f%%', startangle=90)
        plt.title('支出类别分布', fontsize=14, fontweight='bold')
        
        # 4. 收入类别条形图
        plt.subplot(2, 3, 4)
        income_by_category = df[df['收入'] > 0].groupby('交易类别')['收入'].sum().sort_values(ascending=False)
        plt.bar(range(len(income_by_category)), income_by_category.values, color='lightblue')
        plt.title('收入类别分布', fontsize=14, fontweight='bold')
        plt.xlabel('类别')
        plt.ylabel('金额 (¥)')
        plt.xticks(range(len(income_by_category)), income_by_category.index, rotation=45)
        
        # 5. 净收入趋势
        plt.subplot(2, 3, 5)
        monthly_net = df.groupby('年月')['净金额'].sum()
        colors = ['green' if x > 0 else 'red' for x in monthly_net.values]
        plt.bar(range(len(monthly_net)), monthly_net.values, color=colors, alpha=0.7)
        plt.title('月度净收入趋势', fontsize=14, fontweight='bold')
        plt.xlabel('月份')
        plt.ylabel('净金额 (¥)')
        plt.xticks(range(len(monthly_net)), [str(period) for period in monthly_net.index], rotation=45)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.grid(True, alpha=0.3)
        
        # 6. 账户余额变化
        plt.subplot(2, 3, 6)
        # 按日期排序并绘制余额变化
        balance_data = df.dropna(subset=['账户余额']).sort_values('日期')
        plt.plot(balance_data['日期'], balance_data['账户余额'], linewidth=2, color='blue')
        plt.title('账户余额变化', fontsize=14, fontweight='bold')
        plt.xlabel('日期')
        plt.ylabel('余额 (¥)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('bank_analysis_charts.png', dpi=300, bbox_inches='tight')
        print("✅ 图表已保存为 'bank_analysis_charts.png'")
        plt.show()
    
    def generate_report(self):
        """生成完整分析报告"""
        print("\n" + "=" * 70)
        print("📋 生成完整财务分析报告")
        print("=" * 70)
        
        if self.clean_data is None:
            print("❌ 请先进行数据预处理")
            return
        
        # 执行所有分析
        overall_summary = self.analyze_overall_summary()
        monthly_summary = self.analyze_monthly_trends()
        yearly_summary = self.analyze_yearly_trends()
        income_categories, expense_categories = self.analyze_categories()
        top_income, top_expense = self.analyze_top_transactions()
        
        # 生成可视化
        self.create_visualizations()
        
        print("\n" + "=" * 70)
        print("✅ 完整财务分析报告生成完成！")
        print("=" * 70)
        
        return {
            'overall': overall_summary,
            'monthly': monthly_summary,
            'yearly': yearly_summary,
            'income_categories': income_categories,
            'expense_categories': expense_categories,
            'top_income': top_income,
            'top_expense': top_expense
        }

def main():
    """主函数"""
    print("=" * 70)
    print("🏦 银行账单数据分析系统 - 第二阶段")
    print("=" * 70)
    
    # 初始化分析器
    analyzer = BankDataAnalyzer("2023-2025May.csv")
    
    # 加载数据
    if not analyzer.load_data():
        return
    
    # 数据预处理
    if not analyzer.clean_and_preprocess_data():
        return
    
    # 生成完整报告
    results = analyzer.generate_report()
    
    print(f"\n🎉 分析完成！您可以查看生成的图表文件 'bank_analysis_charts.png'")
    print(f"📊 数据对象已保存在 analyzer.clean_data 中，可以进行进一步分析")

if __name__ == "__main__":
    main() 