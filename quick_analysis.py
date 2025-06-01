#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
银行账单数据分析 - 快速启动脚本
作者：Python数据分析专家
功能：一键快速分析银行账单数据
"""

from bank_analysis_improved import ImprovedBankAnalyzer
import os
import sys

def quick_analysis():
    """快速分析功能"""
    print("=" * 60)
    print("🚀 银行账单数据快速分析")
    print("=" * 60)
    
    # 查找CSV文件
    import glob
    csv_files = glob.glob("*.csv")
    
    if not csv_files:
        print("❌ 当前目录没有找到CSV文件")
        print("💡 请将银行账单CSV文件放在当前目录下")
        return
    
    if len(csv_files) == 1:
        # 只有一个文件，直接分析
        csv_file = csv_files[0]
        print(f"📁 发现CSV文件：{csv_file}")
        print("🔄 开始自动分析...")
        
    else:
        # 多个文件，显示选择
        print(f"📁 发现 {len(csv_files)} 个CSV文件：")
        for i, file in enumerate(csv_files, 1):
            size_mb = os.path.getsize(file) / (1024 * 1024)
            print(f"  {i}. {file} ({size_mb:.1f}MB)")
        
        try:
            choice = input(f"\n请选择文件编号 (1-{len(csv_files)}): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(csv_files):
                csv_file = csv_files[choice_num - 1]
            else:
                print("❌ 无效选择")
                return
        except:
            print("❌ 输入错误")
            return
    
    # 创建分析器并运行
    try:
        analyzer = ImprovedBankAnalyzer('analysis_results')
        
        print(f"\n📊 正在分析 {csv_file}...")
        
        if analyzer.load_data(csv_file):
            if analyzer.clean_and_preprocess_data():
                analyzer.generate_report()
                
                print(f"\n🎉 分析完成！")
                print(f"📁 结果保存在：{analyzer.output_dir.absolute()}")
                print(f"📋 包含以下文件：")
                print(f"   • 分析报告 (*.txt)")
                print(f"   • 可视化图表 (*.png)")
                print(f"   • 详细数据表格 (*.csv)")
                
                # 尝试打开结果目录
                try:
                    import subprocess
                    subprocess.run(['open', str(analyzer.output_dir)], check=False)
                    print(f"📂 已自动打开结果目录")
                except:
                    print(f"💡 请手动打开结果目录查看分析结果")
                    
            else:
                print("❌ 数据预处理失败")
        else:
            print("❌ 数据加载失败")
            
    except Exception as e:
        print(f"❌ 分析过程中出现错误：{str(e)}")
        print("💡 请检查CSV文件格式是否正确")

if __name__ == "__main__":
    quick_analysis() 