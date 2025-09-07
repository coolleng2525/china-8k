import matplotlib.pyplot as plt

def setup_fonts():
    """
    最简单的字体配置函数
    使用matplotlib默认配置，避免复杂的字体检测逻辑
    """
    try:
        print("使用matplotlib默认字体配置...")
        
        # 1. 使用matplotlib的默认配置
        # 这会使用系统默认的字体处理机制
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 2. 尝试添加一些常见的中文字体（如果系统中有的话）
        # 但不强制要求，让matplotlib使用系统默认字体
        default_fonts = plt.rcParams['font.sans-serif']
        chinese_fonts = ['Arial Unicode MS', 'Heiti TC', 'PingFang SC', 'SimHei']
        
        # 合并字体列表，保持默认字体优先
        combined_fonts = default_fonts + [f for f in chinese_fonts if f not in default_fonts]
        plt.rcParams['font.sans-serif'] = combined_fonts
        
        print(f"当前字体配置: {plt.rcParams['font.sans-serif'][:3]}...")
        print("字体配置完成（使用系统默认字体）")
        return True
        
    except Exception as e:
        print(f"字体配置出错: {e}")
        # 出错时使用最基本的配置
        try:
            plt.rcdefaults()
            print("已使用matplotlib默认配置")
        except:
            pass
        return False

# 如果直接运行此脚本，则执行字体配置测试
if __name__ == "__main__":
    import os
    setup_fonts()
    
    # 创建一个简单的测试图表
    try:
        plt.figure(figsize=(6, 4))
        plt.title('字体测试 Chart Title')
        plt.xlabel('X轴 Label')
        plt.ylabel('Y轴 Label')
        plt.text(0.5, 0.5, '中文测试文本', ha='center', fontsize=16, transform=plt.gca().transAxes)
        plt.text(0.5, 0.3, 'English Test Text', ha='center', fontsize=16, transform=plt.gca().transAxes)
        plt.grid(True)
        
        # 保存测试图像
        os.makedirs('font_test_output', exist_ok=True)
        plt.savefig('font_test_output/complete_font_test.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        print("字体测试图像已保存至: font_test_output/complete_font_test.png")
    except Exception as e:
        print(f"创建测试图像时出错: {e}")