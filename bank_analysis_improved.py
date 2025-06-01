#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行账单数据分析系统 - 改进版
作者：Python数据分析专家
功能：支持文件选择、结果保存、正确的中文显示
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import glob
import warnings
import sys
from pathlib import Path

warnings.filterwarnings('ignore')

class ImprovedBankAnalyzer:
    """改进版银行账单数据分析器"""
    
    def __init__(self, output_dir="analysis_results"):
        """
        初始化分析器
        
        参数:
            output_dir (str): 结果输出目录
        """
        self.csv_file_path = None
        self.raw_data = None
        self.clean_data = None
        self.output_dir = Path(output_dir)
        self.report_file = None
        
        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        
        # 设置中文字体
        self._setup_chinese_fonts()
        
    def _setup_chinese_fonts(self):
        """设置中文字体支持"""
        try:
            # 尝试不同的中文字体
            chinese_fonts = [
                'Heiti TC',           # macOS 黑体
                'STHeiti',            # macOS 华文黑体  
                'SimHei',             # Windows 黑体
                'Microsoft YaHei',    # Windows 微软雅黑
                'PingFang SC',        # macOS 苹方
                'Arial Unicode MS',   # 通用字体
                'DejaVu Sans'         # 备用字体
            ]
            
            # 设置字体
            for font in chinese_fonts:
                try:
                    plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
                    break
                except:
                    continue
                    
            plt.rcParams['axes.unicode_minus'] = False
            plt.rcParams['figure.max_open_warning'] = 0
            
            # 测试中文显示
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.text(0.5, 0.5, '测试中文', fontsize=12, ha='center')
            plt.close(fig)
            
            print("✅ 中文字体设置成功")
            
        except Exception as e:
            print(f"⚠️  中文字体设置可能有问题: {e}")
    
    def find_csv_files(self, directory="."):
        """
        查找目录中的CSV文件
        
        参数:
            directory (str): 搜索目录
            
        返回:
            list: CSV文件列表
        """
        csv_files = []
        
        # 查找当前目录下的CSV文件
        pattern = os.path.join(directory, "*.csv")
        files = glob.glob(pattern)
        
        for file in files:
            # 获取文件大小和修改时间
            stat = os.stat(file)
            size_mb = stat.st_size / (1024 * 1024)
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            
            csv_files.append({
                'path': file,
                'name': os.path.basename(file),
                'size_mb': size_mb,
                'modified': mod_time
            })
        
        # 按修改时间排序
        csv_files.sort(key=lambda x: x['modified'], reverse=True)
        return csv_files
    
    def select_csv_file(self):
        """
        让用户选择要分析的CSV文件
        
        返回:
            str: 选择的文件路径，如果取消则返回None
        """
        csv_files = self.find_csv_files()
        
        if not csv_files:
            print("❌ 当前目录下没有找到CSV文件")
            return None
        
        print("\n" + "=" * 60)
        print("📁 发现以下CSV文件，请选择要分析的文件：")
        print("=" * 60)
        
        for i, file_info in enumerate(csv_files, 1):
            print(f"{i:2d}. {file_info['name']}")
            print(f"     大小: {file_info['size_mb']:.1f}MB | 修改时间: {file_info['modified'].strftime('%Y-%m-%d %H:%M')}")
            print()
        
        while True:
            try:
                choice = input(f"请输入文件编号 (1-{len(csv_files)}) 或 'q' 退出: ").strip()
                
                if choice.lower() == 'q':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(csv_files):
                    selected_file = csv_files[choice_num - 1]['path']
                    print(f"✅ 已选择文件: {csv_files[choice_num - 1]['name']}")
                    return selected_file
                else:
                    print(f"❌ 请输入 1-{len(csv_files)} 之间的数字")
                    
            except ValueError:
                print("❌ 请输入有效的数字")
            except KeyboardInterrupt:
                print("\n👋 用户取消操作")
                return None
    
    def _write_to_report(self, content, print_also=True):
        """
        写入报告文件
        
        参数:
            content (str): 要写入的内容
            print_also (bool): 是否同时打印到终端
        """
        if self.report_file:
            self.report_file.write(content + '\n')
            self.report_file.flush()  # 确保立即写入
        
        if print_also:
            print(content)
    
    def load_data(self, csv_file_path):
        """
        加载原始数据
        
        参数:
            csv_file_path (str): CSV文件路径
        """
        self.csv_file_path = csv_file_path
        
        # 创建报告文件
        file_name = Path(csv_file_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"analysis_report_{file_name}_{timestamp}.txt"
        self.report_file = open(self.output_dir / report_filename, 'w', encoding='utf-8')
        
        self._write_to_report("=" * 70)
        self._write_to_report("🏦 银行账单数据分析报告")
        self._write_to_report("=" * 70)
        self._write_to_report(f"分析文件: {csv_file_path}")
        self._write_to_report(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._write_to_report(f"结果保存位置: {self.output_dir.absolute()}")
        self._write_to_report("=" * 70)
        
        self._write_to_report("\n📁 正在加载数据...")
        try:
            self.raw_data = pd.read_csv(csv_file_path)
            self._write_to_report(f"✅ 数据加载成功！共有 {len(self.raw_data)} 行数据")
            return True
        except Exception as e:
            self._write_to_report(f"❌ 数据加载失败：{str(e)}")
            return False
    
    def clean_and_preprocess_data(self):
        """数据清洗与预处理"""
        self._write_to_report("\n" + "=" * 50)
        self._write_to_report("🧹 开始数据清洗与预处理")
        self._write_to_report("=" * 50)
        
        if self.raw_data is None:
            self._write_to_report("❌ 请先加载数据")
            return False
        
        # 复制原始数据
        df = self.raw_data.copy()
        
        # 0. 过滤掉汇总行和无效行
        self._write_to_report("🔍 过滤无效数据...")
        original_count = len(df)
        
        # 过滤掉交易日期为空或包含汇总信息的行
        df = df[df['交易日期'].notna()]  # 去除空值
        df = df[~df['交易日期'].str.contains('合计|总计|小计', na=False)]  # 去除汇总行
        df = df[df['交易日期'].str.match(r'^\d{4}-\d{2}-\d{2}', na=False)]  # 只保留日期格式的行
        
        filtered_count = len(df)
        self._write_to_report(f"   原始数据: {original_count} 行")
        self._write_to_report(f"   过滤后数据: {filtered_count} 行") 
        self._write_to_report(f"   移除了 {original_count - filtered_count} 行无效数据")
        
        # 1. 处理日期列
        self._write_to_report("📅 处理日期列...")
        df['交易日期'] = df['交易日期'].str.strip()  # 去除首尾空格
        df['日期'] = pd.to_datetime(df['交易日期'], format='%Y-%m-%d')
        self._write_to_report(f"   日期范围: {df['日期'].min()} 到 {df['日期'].max()}")
        
        # 2. 处理金额列
        self._write_to_report("💰 处理金额列...")
        
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
        
        # 保存清洗后的数据到CSV (添加BOM头解决中文乱码问题)
        clean_data_file = self.output_dir / f"cleaned_data_{Path(self.csv_file_path).stem}.csv"
        df.to_csv(clean_data_file, index=False, encoding='utf-8-sig')
        
        # 显示清洗结果
        self._write_to_report(f"✅ 数据清洗完成！")
        self._write_to_report(f"   处理后数据形状: {df.shape}")
        self._write_to_report(f"   收入记录数: {(df['收入'] > 0).sum()}")
        self._write_to_report(f"   支出记录数: {(df['支出'] > 0).sum()}")
        self._write_to_report(f"   总收入: ¥{df['收入'].sum():,.2f}")
        self._write_to_report(f"   总支出: ¥{df['支出'].sum():,.2f}")
        self._write_to_report(f"   净余额: ¥{df['净金额'].sum():,.2f}")
        self._write_to_report(f"   清洗后数据已保存: {clean_data_file}")
        
        return True
    
    def analyze_overall_summary(self):
        """总体收支情况分析"""
        self._write_to_report("\n" + "=" * 50)
        self._write_to_report("📊 总体收支情况分析")
        self._write_to_report("=" * 50)
        
        df = self.clean_data
        
        total_income = df['收入'].sum()
        total_expense = df['支出'].sum()
        net_balance = total_income - total_expense
        
        income_transactions = (df['收入'] > 0).sum()
        expense_transactions = (df['支出'] > 0).sum()
        
        self._write_to_report(f"💰 总收入: ¥{total_income:,.2f} ({income_transactions} 笔交易)")
        self._write_to_report(f"💸 总支出: ¥{total_expense:,.2f} ({expense_transactions} 笔交易)")
        self._write_to_report(f"💵 净余额: ¥{net_balance:,.2f}")
        self._write_to_report(f"📈 储蓄率: {(net_balance/total_income)*100:.1f}%" if total_income > 0 else "无法计算储蓄率")
        
        # 平均交易金额
        avg_income = df[df['收入'] > 0]['收入'].mean()
        avg_expense = df[df['支出'] > 0]['支出'].mean()
        self._write_to_report(f"📊 平均收入金额: ¥{avg_income:,.2f}")
        self._write_to_report(f"📊 平均支出金额: ¥{avg_expense:,.2f}")
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'income_transactions': income_transactions,
            'expense_transactions': expense_transactions
        }
    
    def analyze_monthly_trends(self):
        """月度趋势分析"""
        self._write_to_report("\n" + "=" * 50)
        self._write_to_report("📅 月度收支趋势分析")
        self._write_to_report("=" * 50)
        
        df = self.clean_data
        
        # 按月聚合
        monthly_summary = df.groupby('年月').agg({
            '收入': 'sum',
            '支出': 'sum',
            '净金额': 'sum'
        }).round(2)
        
        monthly_summary['储蓄率(%)'] = (monthly_summary['净金额'] / monthly_summary['收入'] * 100).round(1)
        monthly_summary['储蓄率(%)'] = monthly_summary['储蓄率(%)'].fillna(0)
        
        self._write_to_report("📊 月度收支汇总表:")
        self._write_to_report(monthly_summary.to_string())
        
        # 找出收入最高和最低的月份
        max_income_month = monthly_summary['收入'].idxmax()
        min_income_month = monthly_summary['收入'].idxmin()
        max_expense_month = monthly_summary['支出'].idxmax()
        min_expense_month = monthly_summary['支出'].idxmin()
        
        self._write_to_report(f"\n💡 关键发现:")
        self._write_to_report(f"   收入最高月份: {max_income_month} (¥{monthly_summary.loc[max_income_month, '收入']:,.2f})")
        self._write_to_report(f"   收入最低月份: {min_income_month} (¥{monthly_summary.loc[min_income_month, '收入']:,.2f})")
        self._write_to_report(f"   支出最高月份: {max_expense_month} (¥{monthly_summary.loc[max_expense_month, '支出']:,.2f})")
        self._write_to_report(f"   支出最低月份: {min_expense_month} (¥{monthly_summary.loc[min_expense_month, '支出']:,.2f})")
        
        # 保存月度数据到CSV (添加BOM头)
        monthly_file = self.output_dir / f"monthly_summary_{Path(self.csv_file_path).stem}.csv"
        monthly_summary.to_csv(monthly_file, encoding='utf-8-sig')
        self._write_to_report(f"   月度汇总数据已保存: {monthly_file}")
        
        return monthly_summary
    
    def analyze_yearly_trends(self):
        """年度趋势分析"""
        self._write_to_report("\n" + "=" * 50)
        self._write_to_report("📆 年度收支趋势分析")
        self._write_to_report("=" * 50)
        
        df = self.clean_data
        
        # 按年聚合
        yearly_summary = df.groupby('年份').agg({
            '收入': 'sum',
            '支出': 'sum',
            '净金额': 'sum'
        }).round(2)
        
        yearly_summary['储蓄率(%)'] = (yearly_summary['净金额'] / yearly_summary['收入'] * 100).round(1)
        yearly_summary['储蓄率(%)'] = yearly_summary['储蓄率(%)'].fillna(0)
        
        self._write_to_report("📊 年度收支汇总表:")
        self._write_to_report(yearly_summary.to_string())
        
        # 计算年度增长率
        if len(yearly_summary) > 1:
            self._write_to_report(f"\n📈 年度增长率分析:")
            for i in range(1, len(yearly_summary)):
                prev_year = yearly_summary.index[i-1]
                curr_year = yearly_summary.index[i]
                
                income_growth = ((yearly_summary.loc[curr_year, '收入'] - yearly_summary.loc[prev_year, '收入']) / yearly_summary.loc[prev_year, '收入'] * 100)
                expense_growth = ((yearly_summary.loc[curr_year, '支出'] - yearly_summary.loc[prev_year, '支出']) / yearly_summary.loc[prev_year, '支出'] * 100)
                
                self._write_to_report(f"   {prev_year} → {curr_year}: 收入增长 {income_growth:+.1f}%, 支出增长 {expense_growth:+.1f}%")
        
        # 保存年度数据到CSV (添加BOM头)
        yearly_file = self.output_dir / f"yearly_summary_{Path(self.csv_file_path).stem}.csv"
        yearly_summary.to_csv(yearly_file, encoding='utf-8-sig')
        self._write_to_report(f"   年度汇总数据已保存: {yearly_file}")
        
        return yearly_summary
    
    def analyze_categories(self):
        """交易类别分析"""
        self._write_to_report("\n" + "=" * 50)
        self._write_to_report("🏷️  交易类别分析")
        self._write_to_report("=" * 50)
        
        df = self.clean_data
        
        # 收入类别分析
        income_categories = df[df['收入'] > 0].groupby('交易类别').agg({
            '收入': ['sum', 'count', 'mean']
        }).round(2)
        income_categories.columns = ['总金额', '交易次数', '平均金额']
        income_categories['占比(%)'] = (income_categories['总金额'] / income_categories['总金额'].sum() * 100).round(1)
        income_categories = income_categories.sort_values('总金额', ascending=False)
        
        self._write_to_report("💰 收入类别分析:")
        self._write_to_report(income_categories.to_string())
        
        # 支出类别分析
        expense_categories = df[df['支出'] > 0].groupby('交易类别').agg({
            '支出': ['sum', 'count', 'mean']
        }).round(2)
        expense_categories.columns = ['总金额', '交易次数', '平均金额']
        expense_categories['占比(%)'] = (expense_categories['总金额'] / expense_categories['总金额'].sum() * 100).round(1)
        expense_categories = expense_categories.sort_values('总金额', ascending=False)
        
        self._write_to_report(f"\n💸 支出类别分析:")
        self._write_to_report(expense_categories.to_string())
        
        # 保存类别数据到CSV (添加BOM头)
        income_file = self.output_dir / f"income_categories_{Path(self.csv_file_path).stem}.csv"
        expense_file = self.output_dir / f"expense_categories_{Path(self.csv_file_path).stem}.csv"
        income_categories.to_csv(income_file, encoding='utf-8-sig')
        expense_categories.to_csv(expense_file, encoding='utf-8-sig')
        
        self._write_to_report(f"\n   收入类别数据已保存: {income_file}")
        self._write_to_report(f"   支出类别数据已保存: {expense_file}")
        
        return income_categories, expense_categories
    
    def analyze_top_transactions(self, n=10):
        """重要交易识别"""
        self._write_to_report("\n" + "=" * 50)
        self._write_to_report(f"🔝 重要交易识别 (Top {n})")
        self._write_to_report("=" * 50)
        
        df = self.clean_data
        
        # Top收入交易
        top_income = df[df['收入'] > 0].nlargest(n, '收入')[['日期', '交易类别', '收入', '对方户名']].round(2)
        self._write_to_report(f"💰 金额最高的{n}笔收入:")
        for idx, row in top_income.iterrows():
            self._write_to_report(f"   {row['日期'].strftime('%Y-%m-%d')} | ¥{row['收入']:,.2f} | {row['交易类别']} | {str(row['对方户名'])[:30]}")
        
        # Top支出交易
        top_expense = df[df['支出'] > 0].nlargest(n, '支出')[['日期', '交易类别', '支出', '对方户名']].round(2)
        self._write_to_report(f"\n💸 金额最高的{n}笔支出:")
        for idx, row in top_expense.iterrows():
            self._write_to_report(f"   {row['日期'].strftime('%Y-%m-%d')} | ¥{row['支出']:,.2f} | {row['交易类别']} | {str(row['对方户名'])[:30]}")
        
        # 保存重要交易到CSV (添加BOM头)
        top_income_file = self.output_dir / f"top_income_{Path(self.csv_file_path).stem}.csv"
        top_expense_file = self.output_dir / f"top_expense_{Path(self.csv_file_path).stem}.csv"
        top_income.to_csv(top_income_file, index=False, encoding='utf-8-sig')
        top_expense.to_csv(top_expense_file, index=False, encoding='utf-8-sig')
        
        self._write_to_report(f"\n   Top收入交易已保存: {top_income_file}")
        self._write_to_report(f"   Top支出交易已保存: {top_expense_file}")
        
        return top_income, top_expense
    
    def create_visualizations(self):
        """创建可视化图表"""
        self._write_to_report("\n" + "=" * 50)
        self._write_to_report("📈 生成可视化图表")
        self._write_to_report("=" * 50)
        
        df = self.clean_data
        
        # 设置图表样式
        plt.style.use('default')
        fig = plt.figure(figsize=(20, 15))
        
        # 确保中文字体正确设置
        plt.rcParams['font.sans-serif'] = ['Heiti TC', 'STHeiti', 'SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
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
        
        # 保存图表
        chart_file = self.output_dir / f"analysis_charts_{Path(self.csv_file_path).stem}.png"
        plt.savefig(chart_file, dpi=300, bbox_inches='tight', facecolor='white')
        self._write_to_report(f"✅ 图表已保存为: {chart_file}")
        
        # 不显示图表，避免阻塞
        plt.close(fig)
    
    def generate_report(self):
        """生成完整分析报告"""
        self._write_to_report("\n" + "=" * 70)
        self._write_to_report("📋 生成完整财务分析报告")
        self._write_to_report("=" * 70)
        
        if self.clean_data is None:
            self._write_to_report("❌ 请先进行数据预处理")
            return
        
        # 执行所有分析
        overall_summary = self.analyze_overall_summary()
        monthly_summary = self.analyze_monthly_trends()
        yearly_summary = self.analyze_yearly_trends()
        income_categories, expense_categories = self.analyze_categories()
        top_income, top_expense = self.analyze_top_transactions()
        
        # 生成可视化
        self.create_visualizations()
        
        self._write_to_report("\n" + "=" * 70)
        self._write_to_report("✅ 完整财务分析报告生成完成！")
        self._write_to_report("=" * 70)
        self._write_to_report(f"📁 所有结果文件保存在: {self.output_dir.absolute()}")
        
        # 关闭报告文件
        if self.report_file:
            self.report_file.close()
            self.report_file = None
        
        return {
            'overall': overall_summary,
            'monthly': monthly_summary,
            'yearly': yearly_summary,
            'income_categories': income_categories,
            'expense_categories': expense_categories,
            'top_income': top_income,
            'top_expense': top_expense
        }
    
    def __del__(self):
        """析构函数，确保文件正确关闭"""
        if hasattr(self, 'report_file') and self.report_file:
            self.report_file.close()

def main():
    """主函数"""
    print("=" * 70)
    print("🏦 银行账单数据分析系统 - 改进版")
    print("=" * 70)
    print("功能改进：")
    print("✅ 支持多文件选择")
    print("✅ 结果保存到文件")
    print("✅ 修复中文字体显示")
    print("✅ 自动创建结果目录")
    print("=" * 70)
    
    # 初始化分析器
    output_dir = input("请输入结果保存目录名称 (直接回车使用默认 'analysis_results'): ").strip()
    if not output_dir:
        output_dir = "analysis_results"
    
    analyzer = ImprovedBankAnalyzer(output_dir)
    
    # 选择CSV文件
    csv_file = analyzer.select_csv_file()
    if not csv_file:
        print("👋 分析已取消")
        return
    
    # 加载数据
    if not analyzer.load_data(csv_file):
        return
    
    # 数据预处理
    if not analyzer.clean_and_preprocess_data():
        return
    
    # 生成完整报告
    print("\n📊 正在生成分析报告，请稍候...")
    results = analyzer.generate_report()
    
    print(f"\n🎉 分析完成！")
    print(f"📁 所有结果文件已保存到: {analyzer.output_dir.absolute()}")
    print(f"📋 文本报告、数据表格、可视化图表都已生成")
    print(f"💡 您可以打开结果目录查看详细分析结果")

if __name__ == "__main__":
    main() 