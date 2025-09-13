#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from src.map_generator import draw_china_map, draw_8000km_range_map, draw_world_map, draw_world_map_with_range
from src.data_handler.json_loader import download_china_map_data
from src.utils.config_loader import ConfigLoader  # 导入类而不是实例
import logging

# 获取日志级别映射关系
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def main():
    """
    地图生成器主程序入口
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='中国地图和8000公里范围地图生成器')
    
    # 添加全局参数
    parser.add_argument('--config', type=str, default=None, help='配置文件路径')
    parser.add_argument('--log-level', type=str, default=None, choices=LOG_LEVELS.keys(),
                        help='设置日志级别: debug, info, warning, error, critical')
    parser.add_argument('--generate-config', action='store_true', help='生成默认配置文件')
    
    # 添加子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 中国地图命令
    china_parser = subparsers.add_parser('china', help='生成中国地图')
    china_parser.add_argument('--output-dir', type=str, default=None, help='输出文件目录')
    china_parser.add_argument('--filename', type=str, default=None, help='输出文件名前缀')
    china_parser.add_argument('--no-show', action='store_true', help='不显示地图，仅保存文件')
    china_parser.add_argument('--data-path', type=str, default=None, help='自定义地图数据文件路径')
    
    # 8000公里范围地图命令
    range_parser = subparsers.add_parser('range', help='生成8000公里范围地图')
    range_parser.add_argument('--radius', type=int, default=None, help='范围半径（公里）')
    range_parser.add_argument('--output-dir', type=str, default=None, help='输出文件目录')
    range_parser.add_argument('--filename', type=str, default=None, help='输出文件名前缀')
    range_parser.add_argument('--no-show', action='store_true', help='不显示地图，仅保存文件')
    
    # 下载数据命令
    download_parser = subparsers.add_parser('download', help='从GitHub下载中国地图数据')
    download_parser.add_argument('--force', action='store_true', help='强制重新下载数据，即使本地已有')
    download_parser.add_argument('--output-path', type=str, default=None, help='数据保存路径')
    
    # 世界地图命令
    world_parser = subparsers.add_parser('world', help='生成世界地图')
    world_parser.add_argument('--output-dir', type=str, default=None, help='输出文件目录')
    world_parser.add_argument('--filename', type=str, default=None, help='输出文件名前缀')
    world_parser.add_argument('--no-show', action='store_true', help='不显示地图，仅保存文件')
    world_parser.add_argument('--data-path', type=str, default=None, help='自定义世界地图数据文件路径')
    
    # 添加世界地图与范围结合的命令
    world_range_parser = subparsers.add_parser('world-range', help='生成带8000公里范围的世界地图')
    world_range_parser.add_argument('--radius', type=int, default=None, help='范围半径（公里）')
    world_range_parser.add_argument('--output-dir', type=str, default=None, help='输出文件目录')
    world_range_parser.add_argument('--filename', type=str, default=None, help='输出文件名前缀')
    world_range_parser.add_argument('--no-show', action='store_true', help='不显示地图，仅保存文件')
    world_range_parser.add_argument('--data-path', type=str, default=None, help='自定义世界地图数据文件路径')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 创建ConfigLoader实例
    config_loader = ConfigLoader(config_path=args.config)
    
    # 确定日志级别并配置日志记录器
    log_level_str = args.log_level or config_loader.get('global', {}).get('log_level', 'info')
    log_level = LOG_LEVELS.get(log_level_str.lower(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.info("程序启动")
    
    # 处理生成配置文件命令
    if args.generate_config:
        config_loader.generate_default_config()
        logger.info('默认配置文件已生成')
        return
    
    # 处理各个命令
    if args.command == 'china':
        # 合并配置和命令行参数
        merged_args = config_loader.merge_with_args(args, 'china')
        # 生成中国地图
        files = draw_china_map(
            output_dir=merged_args.get('output_dir', 'outputs'),
            filename_prefix=merged_args.get('filename', 'china_map'),
            show_map=merged_args.get('show_map', True),
            data_path=merged_args.get('data_path')
        )
        logger.info(f"中国地图已生成并保存到以下文件：")
        for file in files:
            logger.info(f"- {os.path.abspath(file)}")
    elif args.command == 'range':
        # 合并配置和命令行参数
        merged_args = config_loader.merge_with_args(args, 'range')
        # 生成8000公里范围地图
        files = draw_8000km_range_map(
            radius_km=merged_args.get('radius', 8000),
            output_dir=merged_args.get('output_dir', 'outputs'),
            filename_prefix=merged_args.get('filename', 'china_8000km_range'),
            show_map=merged_args.get('show_map', True)
        )
        print(f"{merged_args.get('radius', 8000)}公里范围地图已生成并保存到以下文件：")
        for file in files:
            print(f"- {os.path.abspath(file)}")
    elif args.command == 'download':
        # 合并配置和命令行参数
        merged_args = config_loader.merge_with_args(args, 'download')
        try:
            output_path = merged_args.get('output_path')
            if not output_path:
                # 使用默认路径
                if not os.path.exists('data'):
                    os.makedirs('data')
                output_path = os.path.join('data', 'china.json')
            
            # 检查文件是否已存在
            if os.path.exists(output_path) and not merged_args.get('force', False):
                print(f"文件已存在，如需重新下载，请使用 --force 参数")
                return
            elif os.path.exists(output_path):
                os.remove(output_path)
                print(f"已删除原有文件: {output_path}")
            
            # 下载数据
            data = download_china_map_data(output_path=output_path)
            print(f"中国地图数据已成功下载并保存到: {os.path.abspath(output_path)}")
            print(f"数据包含 {len(data.get('features', []))} 个地理特征")
        except Exception as e:
            print(f"下载中国地图数据失败: {e}")
            import traceback
            traceback.print_exc()
    elif args.command == 'world':
        # 合并配置和命令行参数
        merged_args = config_loader.merge_with_args(args, 'world')
        # 生成世界地图
        files = draw_world_map(
            output_dir=merged_args.get('output_dir', 'outputs'),
            filename_prefix=merged_args.get('filename', 'world_map'),
            show_map=merged_args.get('show_map', True),
            data_path=merged_args.get('data_path')
        )
        print(f"世界地图已生成并保存到以下文件：")
        for file in files:
            print(f"- {os.path.abspath(file)}")
    elif args.command == 'world-range':
        # 合并配置和命令行参数
        merged_args = config_loader.merge_with_args(args, 'world-range')
        # 生成带8000公里范围的世界地图
        files = draw_world_map_with_range(
            radius_km=merged_args.get('radius', 8000),
            output_dir=merged_args.get('output_dir', 'outputs'),
            filename_prefix=merged_args.get('filename', 'world_with_8000km_range'),
            show_map=merged_args.get('show_map', True),
            data_path=merged_args.get('data_path')
        )
        print(f"带{merged_args.get('radius', 8000)}公里范围的世界地图已生成并保存到以下文件：")
        for file in files:
            print(f"- {os.path.abspath(file)}")
    else:
        # 未指定命令，显示帮助信息
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # 确保即使在main函数外部发生异常也能正确记录日志
        import logging
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.exception("程序发生异常")
        raise