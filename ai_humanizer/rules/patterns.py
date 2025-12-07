"""
AI写作模式库

包含AI文本中常见的固定句式和结构模式的正则表达式
"""

import re

# 固定句式模式 - AI喜欢用的句式结构
FIXED_SENTENCE_PATTERNS = [
    # "不仅...而且..." 句式
    r'不仅.{2,20}而且.{2,20}',
    r'不但.{2,20}而且.{2,20}',
    r'不只.{2,20}还.{2,20}',
    
    # "一方面...另一方面..." 句式
    r'一方面.{5,30}另一方面.{5,30}',
    r'一方面.{5,30}另外.{5,30}',
    
    # "既...又..." 句式
    r'既.{2,15}又.{2,15}',
    r'既.{2,15}也.{2,15}',
    
    # "只有...才能..." 句式
    r'只有.{3,20}才能.{3,20}',
    r'只有.{3,20}才.{3,20}',
    
    # "无论...都..." 句式
    r'无论.{3,20}都.{3,20}',
    r'不管.{3,20}都.{3,20}',
    
    # "如果...就..." 句式
    r'如果.{3,25}就.{3,25}',
    r'假如.{3,25}就.{3,25}',
    r'倘若.{3,25}就.{3,25}',
    
    # "虽然...但是..." 句式
    r'虽然.{3,25}但是.{3,25}',
    r'虽然.{3,25}然而.{3,25}',
    r'尽管.{3,25}但是.{3,25}',
    
    # "因为...所以..." 句式
    r'因为.{3,25}所以.{3,25}',
    r'由于.{3,25}因此.{3,25}',
    
    # "通过...实现..." 句式
    r'通过.{3,20}实现.{3,20}',
    r'通过.{3,20}达到.{3,20}',
    r'借助.{3,20}实现.{3,20}',
    
    # "随着...变化..." 句式
    r'随着.{3,20}的发展',
    r'随着.{3,20}的变化',
    r'随着.{3,20}的提高',
]

# 排比句模式 - AI喜欢用的排比结构
PARALLEL_PATTERNS = [
    # 三个或更多连续的相同结构
    r'(.{2,8})[，,](.{2,8})[，,](.{2,8})',
    
    # 连续的"要...要...要..."
    r'要.{2,15}[，,]要.{2,15}[，,]要.{2,15}',
    
    # 连续的"能...能...能..."
    r'能.{2,15}[，,]能.{2,15}[，,]能.{2,15}',
    
    # 连续的"有...有...有..."
    r'有.{2,15}[，,]有.{2,15}[，,]有.{2,15}',
    
    # "不仅...还...更..." 递进式排比
    r'不仅.{2,15}[，,]还.{2,15}[，,]更.{2,15}',
]

# 总分总结构模式
SUMMARY_DETAIL_PATTERNS = [
    # 开头总起
    r'^.{10,30}[。：:]',
    
    # 结尾总结
    r'(总之|综上所述|总而言之|归根结底|综上|因此).{10,50}[。！]$',
    
    # 中间过渡
    r'(首先|其次|再次|然后|接着|最后).{5,}[。]',
]

# 列表式表达模式
LIST_PATTERNS = [
    # "第一...第二...第三..."
    r'第一.{5,30}第二.{5,30}',
    r'第一.{5,30}第二.{5,30}第三.{5,30}',
    
    # "1...2...3..."
    r'[1１一].{5,30}[2２二].{5,30}',
    r'[1１一].{5,30}[2２二].{5,30}[3３三].{5,30}',
    
    # "首先...其次...最后..."
    r'首先.{5,30}其次.{5,30}',
    r'首先.{5,30}其次.{5,30}最后.{5,30}',
]

# AI开头模式
AI_OPENING_PATTERNS = [
    r'^在当今社会',
    r'^在现代社会',
    r'^随着.{2,10}的发展',
    r'^近年来',
    r'^众所周知',
    r'^毋庸置疑',
    r'^显而易见',
]

# AI结尾模式
AI_CLOSING_PATTERNS = [
    r'(总之|综上所述|总而言之).{10,}[。！]$',
    r'具有重要意义[。！]$',
    r'发挥重要作用[。！]$',
    r'产生深远影响[。！]$',
]

def compile_patterns(pattern_list):
    """编译正则表达式列表"""
    return [re.compile(p) for p in pattern_list]

# 编译所有模式
COMPILED_FIXED_PATTERNS = compile_patterns(FIXED_SENTENCE_PATTERNS)
COMPILED_PARALLEL_PATTERNS = compile_patterns(PARALLEL_PATTERNS)
COMPILED_SUMMARY_PATTERNS = compile_patterns(SUMMARY_DETAIL_PATTERNS)
COMPILED_LIST_PATTERNS = compile_patterns(LIST_PATTERNS)
COMPILED_OPENING_PATTERNS = compile_patterns(AI_OPENING_PATTERNS)
COMPILED_CLOSING_PATTERNS = compile_patterns(AI_CLOSING_PATTERNS)

def check_pattern(text, pattern_type='all'):
    """
    检查文本是否包含指定类型的AI模式
    
    Args:
        text: 要检查的文本
        pattern_type: 模式类型，可选值：
            'all' - 所有模式
            'fixed' - 固定句式
            'parallel' - 排比句
            'summary' - 总分总结构
            'list' - 列表式表达
            'opening' - AI开头
            'closing' - AI结尾
    
    Returns:
        匹配到的模式列表
    """
    matches = []
    
    if pattern_type in ['all', 'fixed']:
        for pattern in COMPILED_FIXED_PATTERNS:
            if pattern.search(text):
                matches.append(('fixed', pattern.pattern))
    
    if pattern_type in ['all', 'parallel']:
        for pattern in COMPILED_PARALLEL_PATTERNS:
            if pattern.search(text):
                matches.append(('parallel', pattern.pattern))
    
    if pattern_type in ['all', 'summary']:
        for pattern in COMPILED_SUMMARY_PATTERNS:
            if pattern.search(text):
                matches.append(('summary', pattern.pattern))
    
    if pattern_type in ['all', 'list']:
        for pattern in COMPILED_LIST_PATTERNS:
            if pattern.search(text):
                matches.append(('list', pattern.pattern))
    
    if pattern_type in ['all', 'opening']:
        for pattern in COMPILED_OPENING_PATTERNS:
            if pattern.search(text):
                matches.append(('opening', pattern.pattern))
    
    if pattern_type in ['all', 'closing']:
        for pattern in COMPILED_CLOSING_PATTERNS:
            if pattern.search(text):
                matches.append(('closing', pattern.pattern))
    
    return matches
