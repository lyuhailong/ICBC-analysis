#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行账单数据分析脚本 - 第一阶段：数据加载与探查
作者：Python数据分析专家
目标：分析2023-2025年5月的银行账单数据
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def load_and_explore_data(csv_file_path):
    """
    加载CSV文件并进行初步数据探查
    
    参数:
        csv_file_path (str): CSV文件路径
    
    返回:
        pandas.DataFrame: 加载的数据框
    """
    print("=" * 60)
    print("银行账单数据分析 - 第一阶段：数据加载与探查")
    print("=" * 60)
    
    try:
        # 1. 加载数据
        print(f"\n📁 正在加载文件: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        print(f"✅ 数据加载成功！共有 {len(df)} 行数据")
        
        # 2. 显示前5行数据
        print("\n" + "=" * 40)
        print("📊 数据前5行预览 (head())")
        print("=" * 40)
        print(df.head())
        
        # 3. 显示数据信息
        print("\n" + "=" * 40)
        print("📋 数据结构信息 (info())")
        print("=" * 40)
        print(f"数据形状: {df.shape}")
        print(f"列数: {len(df.columns)}")
        print(f"行数: {len(df)}")
        print("\n列信息详情:")
        df.info()
        
        # 4. 显示基本描述性统计
        print("\n" + "=" * 40)
        print("📈 数值列描述性统计 (describe())")
        print("=" * 40)
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            print(df[numeric_columns].describe())
        else:
            print("⚠️  没有检测到数值类型的列")
        
        # 5. 显示所有列名和数据类型
        print("\n" + "=" * 40)
        print("📝 所有列名和数据类型")
        print("=" * 40)
        for i, (col_name, dtype) in enumerate(zip(df.columns, df.dtypes)):
            print(f"{i+1:2d}. 列名: '{col_name}' | 数据类型: {dtype}")
        
        # 6. 检查缺失值情况
        print("\n" + "=" * 40)
        print("🔍 缺失值检查")
        print("=" * 40)
        missing_info = df.isnull().sum()
        total_rows = len(df)
        print("各列缺失值统计:")
        for col in df.columns:
            missing_count = missing_info[col]
            missing_percent = (missing_count / total_rows) * 100
            print(f"  {col}: {missing_count} 个缺失值 ({missing_percent:.1f}%)")
        
        # 7. 显示每列的唯一值数量（用于识别可能的分类列）
        print("\n" + "=" * 40)
        print("🏷️  各列唯一值数量")
        print("=" * 40)
        for col in df.columns:
            unique_count = df[col].nunique()
            total_count = len(df[col])
            print(f"  {col}: {unique_count} 个唯一值 (占总数的 {unique_count/total_count*100:.1f}%)")
        
        # 8. 显示文本列的样本数据（前5个唯一值）
        print("\n" + "=" * 40)
        print("📄 文本列样本数据")
        print("=" * 40)
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            print(f"\n列 '{col}' 的前5个唯一值:")
            unique_values = df[col].dropna().unique()[:5]
            for i, value in enumerate(unique_values, 1):
                # 限制显示长度，避免过长的描述
                display_value = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                print(f"    {i}. {display_value}")
        
        print("\n" + "=" * 60)
        print("✅ 第一阶段数据探查完成！")
        print("=" * 60)
        
        print("\n" + "🔔 请根据以上输出信息回答以下问题：")
        print("   1. 哪一列是【日期】(Date)？")
        print("   2. 哪一列是【交易描述】(Description)？")
        print("   3. 哪一列是【交易金额】(Amount)？")
        print("   4. 如何区分【收入】和【支出】？")
        print("      - 是否通过金额的正负值区分？")
        print("      - 还是存在单独的交易类型列？")
        print("   5. 是否存在【交易类别】(Category)列？如果有，列名是什么？")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 {csv_file_path}")
        return None
    except Exception as e:
        print(f"❌ 读取文件时发生错误：{str(e)}")
        return None

def main():
    """主函数"""
    csv_file_path = "2023-2025May.csv"
    
    # 执行第一阶段分析
    df = load_and_explore_data(csv_file_path)
    
    if df is not None:
        print(f"\n📊 数据已成功加载到变量 'df' 中")
        print(f"   数据形状: {df.shape}")
        print(f"   可以使用 df.head(), df.info(), df.describe() 等命令进一步探查")

if __name__ == "__main__":
    main() 