"""
AI文本检测器

检测文本中的AI写作特征，包括词汇、句式、结构和语义层面的分析
"""

import re
import jieba
from .rules.ai_keywords import (
    AI_HIGH_FREQ_WORDS, AI_CONNECTORS, AI_FORMAL_WORDS,
    AI_QUALIFIERS, AI_FIXED_PHRASES, get_ai_keywords
)
from .rules.patterns import (
    check_pattern, COMPILED_FIXED_PATTERNS, COMPILED_PARALLEL_PATTERNS,
    COMPILED_LIST_PATTERNS, COMPILED_OPENING_PATTERNS, COMPILED_CLOSING_PATTERNS
)
from .rules.replacements import FIRST_PERSON_EXPRESSIONS, EMOTION_WORDS


class AIDetector:
    """AI文本检测器"""
    
    def __init__(self):
        """初始化检测器"""
        self.ai_keywords = get_ai_keywords()
        
    def detect(self, text):
        """
        检测文本的AI特征
        
        Args:
            text: 要检测的文本
        
        Returns:
            字典，包含检测结果和详细分析
        """
        if not text or len(text.strip()) == 0:
            return {
                'is_ai': False,
                'confidence': 0.0,
                'score': 0,
                'details': {},
                'text_length': 0
            }
        
        # 各层面分析
        lexical_result = self._analyze_lexical(text)
        syntactic_result = self._analyze_syntactic(text)
        structural_result = self._analyze_structural(text)
        semantic_result = self._analyze_semantic(text)
        
        # 计算综合得分
        total_score = (
            lexical_result['score'] * 0.3 +
            syntactic_result['score'] * 0.25 +
            structural_result['score'] * 0.25 +
            semantic_result['score'] * 0.2
        )
        
        # 判断是否为AI生成
        is_ai = total_score >= 60
        confidence = total_score / 100.0
        
        return {
            'is_ai': is_ai,
            'confidence': confidence,
            'score': round(total_score, 2),
            'details': {
                'lexical': lexical_result,
                'syntactic': syntactic_result,
                'structural': structural_result,
                'semantic': semantic_result,
            },
            'text_length': len(text),
            'summary': self._generate_summary(total_score, lexical_result, 
                                              syntactic_result, structural_result, 
                                              semantic_result)
        }
    
    def _analyze_lexical(self, text):
        """
        词汇层面分析
        
        检测AI高频词、连接词、书面语等
        """
        words = list(jieba.cut(text))
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0, 'details': {}}
        
        # 统计各类词汇出现次数
        high_freq_count = sum(1 for w in words if w in AI_HIGH_FREQ_WORDS)
        connector_count = sum(1 for w in words if w in AI_CONNECTORS)
        formal_count = sum(1 for w in words if w in AI_FORMAL_WORDS)
        qualifier_count = sum(1 for w in words if w in AI_QUALIFIERS)
        
        # 检测固定短语
        fixed_phrase_count = sum(1 for phrase in AI_FIXED_PHRASES if phrase in text)
        
        # 计算比例
        high_freq_ratio = high_freq_count / total_words * 100
        connector_ratio = connector_count / total_words * 100
        formal_ratio = formal_count / total_words * 100
        
        # 词汇层面得分（0-100）
        score = min(100, (
            high_freq_ratio * 15 +
            connector_ratio * 15 +
            formal_ratio * 10 +
            qualifier_count * 2 +
            fixed_phrase_count * 5
        ))
        
        return {
            'score': round(score, 2),
            'details': {
                'high_freq_words': high_freq_count,
                'connectors': connector_count,
                'formal_words': formal_count,
                'qualifiers': qualifier_count,
                'fixed_phrases': fixed_phrase_count,
                'high_freq_ratio': round(high_freq_ratio, 2),
                'connector_ratio': round(connector_ratio, 2),
                'formal_ratio': round(formal_ratio, 2),
            }
        }
    
    def _analyze_syntactic(self, text):
        """
        句式层面分析
        
        检测句子长度、固定句式、排比句等
        """
        # 分句
        sentences = re.split(r'[。！？\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {'score': 0, 'details': {}}
        
        # 句子长度分析
        sentence_lengths = [len(s) for s in sentences]
        avg_length = sum(sentence_lengths) / len(sentences)
        
        # 统计过长和过短的句子
        too_long = sum(1 for l in sentence_lengths if l > 40)
        too_short = sum(1 for l in sentence_lengths if l < 5)
        
        # 检测固定句式
        fixed_patterns = []
        for sentence in sentences:
            matches = check_pattern(sentence, 'fixed')
            fixed_patterns.extend(matches)
        
        # 检测排比句
        parallel_patterns = []
        for sentence in sentences:
            matches = check_pattern(sentence, 'parallel')
            parallel_patterns.extend(matches)
        
        # 检测列表式表达
        list_patterns = check_pattern(text, 'list')
        
        # 句式层面得分（0-100）
        score = min(100, (
            (avg_length / 50) * 20 +  # 句子越长分数越高
            len(fixed_patterns) * 8 +
            len(parallel_patterns) * 10 +
            len(list_patterns) * 12 +
            too_long * 5
        ))
        
        return {
            'score': round(score, 2),
            'details': {
                'sentence_count': len(sentences),
                'avg_sentence_length': round(avg_length, 2),
                'fixed_patterns': len(fixed_patterns),
                'parallel_patterns': len(parallel_patterns),
                'list_patterns': len(list_patterns),
                'too_long_sentences': too_long,
                'too_short_sentences': too_short,
            }
        }
    
    def _analyze_structural(self, text):
        """
        结构层面分析
        
        检测段落结构、总分总、列表式等
        """
        # 分段
        paragraphs = text.split('\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        # 检测总分总结构
        has_opening = any(check_pattern(text, 'opening'))
        has_closing = any(check_pattern(text, 'closing'))
        
        # 检测列表式结构
        list_indicators = ['第一', '第二', '第三', '首先', '其次', '最后']
        list_structure_count = sum(1 for indicator in list_indicators if indicator in text)
        
        # 段落长度分析
        if paragraphs:
            para_lengths = [len(p) for p in paragraphs]
            avg_para_length = sum(para_lengths) / len(paragraphs)
        else:
            avg_para_length = len(text)
        
        # 结构层面得分（0-100）
        score = min(100, (
            (30 if has_opening else 0) +
            (30 if has_closing else 0) +
            list_structure_count * 8 +
            (20 if avg_para_length > 100 else 0)
        ))
        
        return {
            'score': round(score, 2),
            'details': {
                'paragraph_count': len(paragraphs),
                'has_opening_pattern': has_opening,
                'has_closing_pattern': has_closing,
                'list_structure_count': list_structure_count,
                'avg_paragraph_length': round(avg_para_length, 2),
            }
        }
    
    def _analyze_semantic(self, text):
        """
        语义层面分析
        
        检测限定词、情感词、第一人称等
        """
        words = list(jieba.cut(text))
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0, 'details': {}}
        
        # 统计限定词
        qualifier_count = sum(1 for w in words if w in AI_QUALIFIERS)
        
        # 统计情感词
        emotion_count = 0
        for emotion_list in EMOTION_WORDS.values():
            emotion_count += sum(1 for w in words if w in emotion_list)
        
        # 统计第一人称
        first_person_count = sum(1 for w in words if w in FIRST_PERSON_EXPRESSIONS)
        
        # 计算比例
        emotion_ratio = emotion_count / total_words * 100
        first_person_ratio = first_person_count / total_words * 100
        
        # 语义层面得分（0-100）
        # 注意：情感词和第一人称越多，AI特征越弱
        score = min(100, (
            qualifier_count * 5 +
            max(0, 50 - emotion_ratio * 10) +  # 情感词多则扣分
            max(0, 30 - first_person_ratio * 10)  # 第一人称多则扣分
        ))
        
        return {
            'score': round(score, 2),
            'details': {
                'qualifier_count': qualifier_count,
                'emotion_count': emotion_count,
                'first_person_count': first_person_count,
                'emotion_ratio': round(emotion_ratio, 2),
                'first_person_ratio': round(first_person_ratio, 2),
            }
        }
    
    def _generate_summary(self, total_score, lexical, syntactic, structural, semantic):
        """生成检测摘要"""
        if total_score >= 80:
            level = '极高'
            conclusion = '文本具有非常明显的AI生成特征'
        elif total_score >= 60:
            level = '较高'
            conclusion = '文本很可能由AI生成'
        elif total_score >= 40:
            level = '中等'
            conclusion = '文本具有一些AI特征，但不明显'
        elif total_score >= 20:
            level = '较低'
            conclusion = '文本AI特征较少，较为自然'
        else:
            level = '很低'
            conclusion = '文本非常自然，几乎无AI特征'
        
        # 找出得分最高的维度
        dimensions = {
            '词汇': lexical['score'],
            '句式': syntactic['score'],
            '结构': structural['score'],
            '语义': semantic['score'],
        }
        max_dim = max(dimensions.items(), key=lambda x: x[1])
        
        return {
            'level': level,
            'conclusion': conclusion,
            'main_issue': f'{max_dim[0]}层面的AI特征最为明显（得分：{max_dim[1]:.2f}）'
        }
    
    def generate_report(self, detection_result):
        """
        生成详细的检测报告
        
        Args:
            detection_result: detect()方法返回的结果
        
        Returns:
            格式化的报告文本
        """
        result = detection_result
        report_lines = []
        
        report_lines.append('=' * 50)
        report_lines.append('AI文本检测报告')
        report_lines.append('=' * 50)
        report_lines.append('')
        
        # 综合结论
        report_lines.append(f"检测结论: {result['summary']['conclusion']}")
        report_lines.append(f"AI特征等级: {result['summary']['level']}")
        report_lines.append(f"综合得分: {result['score']}/100")
        report_lines.append(f"置信度: {result['confidence']:.2%}")
        report_lines.append('')
        
        # 各维度详情
        report_lines.append('-' * 50)
        report_lines.append('各维度分析：')
        report_lines.append('-' * 50)
        
        # 词汇层面
        lex = result['details']['lexical']
        report_lines.append(f"\n【词汇层面】得分: {lex['score']:.2f}/100")
        report_lines.append(f"  - AI高频词: {lex['details']['high_freq_words']}个 ({lex['details']['high_freq_ratio']:.2f}%)")
        report_lines.append(f"  - 连接词: {lex['details']['connectors']}个 ({lex['details']['connector_ratio']:.2f}%)")
        report_lines.append(f"  - 书面语: {lex['details']['formal_words']}个 ({lex['details']['formal_ratio']:.2f}%)")
        report_lines.append(f"  - 限定词: {lex['details']['qualifiers']}个")
        report_lines.append(f"  - 固定短语: {lex['details']['fixed_phrases']}个")
        
        # 句式层面
        syn = result['details']['syntactic']
        report_lines.append(f"\n【句式层面】得分: {syn['score']:.2f}/100")
        report_lines.append(f"  - 句子数量: {syn['details']['sentence_count']}句")
        report_lines.append(f"  - 平均句长: {syn['details']['avg_sentence_length']:.2f}字")
        report_lines.append(f"  - 固定句式: {syn['details']['fixed_patterns']}处")
        report_lines.append(f"  - 排比句: {syn['details']['parallel_patterns']}处")
        report_lines.append(f"  - 列表式表达: {syn['details']['list_patterns']}处")
        
        # 结构层面
        struct = result['details']['structural']
        report_lines.append(f"\n【结构层面】得分: {struct['score']:.2f}/100")
        report_lines.append(f"  - 段落数量: {struct['details']['paragraph_count']}段")
        report_lines.append(f"  - 平均段长: {struct['details']['avg_paragraph_length']:.2f}字")
        report_lines.append(f"  - 总起句式: {'是' if struct['details']['has_opening_pattern'] else '否'}")
        report_lines.append(f"  - 总结句式: {'是' if struct['details']['has_closing_pattern'] else '否'}")
        report_lines.append(f"  - 列表结构: {struct['details']['list_structure_count']}处")
        
        # 语义层面
        sem = result['details']['semantic']
        report_lines.append(f"\n【语义层面】得分: {sem['score']:.2f}/100")
        report_lines.append(f"  - 限定词: {sem['details']['qualifier_count']}个")
        report_lines.append(f"  - 情感词: {sem['details']['emotion_count']}个 ({sem['details']['emotion_ratio']:.2f}%)")
        report_lines.append(f"  - 第一人称: {sem['details']['first_person_count']}个 ({sem['details']['first_person_ratio']:.2f}%)")
        
        report_lines.append('')
        report_lines.append('-' * 50)
        report_lines.append(f"主要问题: {result['summary']['main_issue']}")
        report_lines.append('=' * 50)
        
        return '\n'.join(report_lines)
