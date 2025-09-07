# 地图生成器模块
"""
地图生成器模块负责生成各类地图，包括中国地图和8000公里范围地图。
"""

from .china_map import draw_china_map
from .range_map import draw_8000km_range_map
from .world_map import draw_world_map
from .world_range_map import draw_world_map_with_range

__all__ = ['draw_china_map', 'draw_8000km_range_map', 'draw_world_map', 'draw_world_map_with_range']