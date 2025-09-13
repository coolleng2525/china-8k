import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import logging

# 初始化日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_fonts():
    # 中文字体优先级列表（macOS适用）
    font_priority = [
        'PingFang SC',    # macOS系统字体
        'Arial Unicode MS',  # Office附带字体
        'Songti SC',      # macOS简体中文
        'Heiti SC',       # 黑体简体
        'STHeiti',        # 华文黑体
        'Hiragino Sans GB' # 冬青黑体
    ]
    
    # 自动选择第一个可用的中文字体
    for font in font_priority:
        if any(f.name == font for f in fm.fontManager.ttflist):
            plt.rcParams['font.sans-serif'] = [font, 'Arial']
            plt.rcParams['axes.unicode_minus'] = False
            logger.info(f"已自动选择中英文字体：{font}")
            return True
    
    # 回退方案
    plt.rcParams['font.sans-serif'] = ['Arial']
    logger.warning("未找到中文字体，中文可能显示异常")


# 额外的工具函数：测试特定字体是否可用
def is_font_available(font_name):
    """检查指定字体是否可用"""
    try:
        available_fonts = [f.lower() for f in fm.findSystemFonts(fontpaths=None, fontext='ttf')]
        return font_name.lower() in available_fonts
    except Exception as e:
        logger.error(f"检查字体可用性时出错: {e}")
        return False


# 额外的工具函数：获取系统中可用的中文字体列表
def get_available_chinese_fonts():
    """获取系统中可用的中文字体列表"""
    try:
        # 中文字体通常包含这些关键词
        chinese_keywords = ['sim', 'hei', 'song', 'kai', 'microsoft', 'yahei', 
                           'heiti', 'pingfang', 'wenquanyi', 'noto', 'cjk']
        
        available_fonts = []
        for font_path in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
            try:
                font_name = fm.FontProperties(fname=font_path).get_name()
                if any(keyword in font_name.lower() for keyword in chinese_keywords):
                    available_fonts.append(font_name)
            except Exception as e:
                logger.debug(f"处理字体路径 {font_path} 时出错: {e}")
                continue
        
        return list(set(available_fonts))  # 去重
    except Exception as e:
        logger.error(f"获取中文字体列表时出错: {e}")
        return []


# 如果直接运行此脚本，则执行字体配置测试
if __name__ == "__main__":
    setup_fonts()
    
    # 显示系统可用的中文字体
    chinese_fonts = get_available_chinese_fonts()
    logger.info(f"系统中可用的中文字体数量: {len(chinese_fonts)}")
    if chinese_fonts:
        logger.info(f"前5个可用中文字体: {', '.join(chinese_fonts[:5])}")
    
    # 创建一个简单的测试图表
    try:
        plt.figure(figsize=(8, 6), dpi=100)
        plt.title('中文字体测试 Chart Title')
        plt.xlabel('X轴 标签')
        plt.ylabel('Y轴 标签')
        plt.text(0.5, 0.7, '中文测试文本', ha='center', fontsize=16, transform=plt.gca().transAxes)
        plt.text(0.5, 0.5, 'English Test Text', ha='center', fontsize=16, transform=plt.gca().transAxes)
        plt.text(0.5, 0.3, '中文显示测试 12345', ha='center', fontsize=14, transform=plt.gca().transAxes)
        plt.grid(True)
        
        # 保存测试图像
        os.makedirs('font_test_output', exist_ok=True)
        plt.savefig('font_test_output/complete_font_test.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info("字体测试图像已保存至: font_test_output/complete_font_test.png")
    except Exception as e:
        logger.error(f"创建测试图像时出错: {e}")


