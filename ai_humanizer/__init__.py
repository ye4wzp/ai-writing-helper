"""
AI Writing Helper - 中文AI文本检测与人性化工具

这是一个完全基于规则的本地工具，用于:
1. 检测AI生成的中文文本特征
2. 将AI味道浓厚的文本改写得更自然

作者: ye4wzp
版本: 1.0.0
"""

__version__ = '1.0.0'
__author__ = 'ye4wzp'

from .detector import AIDetector
from .humanizer import AIHumanizer

__all__ = ['AIDetector', 'AIHumanizer']
