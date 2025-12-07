"""
AI文本人性化处理器

将AI味道浓厚的文本改写得更加自然、人性化
"""

import re
import random
import jieba
from .rules.ai_keywords import AI_HIGH_FREQ_WORDS, AI_CONNECTORS, AI_FORMAL_WORDS
from .rules.replacements import (
    WORD_REPLACEMENTS, PERSONAL_EXPRESSIONS, EMOTION_WORDS,
    FIRST_PERSON_EXPRESSIONS, UNCERTAINTY_EXPRESSIONS, COLLOQUIAL_MARKERS,
    get_replacement, get_personal_expressions
)
from .rules.patterns import check_pattern


class AIHumanizer:
    """AI文本人性化处理器"""
    
    def __init__(self):
        """初始化处理器"""
        self.replacements = WORD_REPLACEMENTS
        random.seed()
    
    def humanize(self, text, intensity='medium'):
        """
        将文本人性化
        
        Args:
            text: 要处理的文本
            intensity: 处理强度
                - 'light': 轻度处理，只替换最明显的AI词汇
                - 'medium': 中度处理，替换词汇并调整部分句式
                - 'heavy': 重度处理，全面改写，添加个性化表达
        
        Returns:
            字典，包含处理后的文本和修改详情
        """
        if not text or len(text.strip()) == 0:
            return {
                'text': text,
                'original_length': 0,
                'modified_length': 0,
                'changes': [],
                'change_count': 0,
                'intensity': intensity
            }
        
        original_text = text
        changes = []
        
        # 根据强度选择处理方法
        if intensity == 'light':
            text, change_list = self._light_humanize(text)
            changes.extend(change_list)
        elif intensity == 'medium':
            text, change_list = self._medium_humanize(text)
            changes.extend(change_list)
        elif intensity == 'heavy':
            text, change_list = self._heavy_humanize(text)
            changes.extend(change_list)
        else:
            raise ValueError(f"Invalid intensity: {intensity}. Must be 'light', 'medium', or 'heavy'")
        
        return {
            'text': text,
            'original_length': len(original_text),
            'modified_length': len(text),
            'changes': changes,
            'change_count': len(changes),
            'intensity': intensity
        }
    
    def _light_humanize(self, text):
        """轻度人性化处理"""
        changes = []
        
        # 1. 替换最明显的AI高频词
        for word in AI_HIGH_FREQ_WORDS[:20]:  # 只处理最常见的20个
            if word in text and word in self.replacements:
                replacements = self.replacements[word]
                if replacements:
                    new_word = random.choice(replacements)
                    text = text.replace(word, new_word, 1)  # 只替换第一次出现
                    changes.append(f"'{word}' → '{new_word}'")
        
        # 2. 简化部分书面语
        for word in AI_FORMAL_WORDS[:10]:  # 只处理最常见的10个
            if word in text and word in self.replacements:
                replacements = self.replacements[word]
                if replacements:
                    new_word = random.choice(replacements)
                    text = text.replace(word, new_word, 1)
                    changes.append(f"'{word}' → '{new_word}'")
        
        return text, changes
    
    def _medium_humanize(self, text):
        """中度人性化处理"""
        changes = []
        
        # 1. 词汇替换
        text, word_changes = self._replace_words(text, ratio=0.6)
        changes.extend(word_changes)
        
        # 2. 句式调整
        text, syntax_changes = self._adjust_syntax(text)
        changes.extend(syntax_changes)
        
        # 3. 添加少量口语化表达
        text, colloquial_changes = self._add_colloquial_expressions(text, count=2)
        changes.extend(colloquial_changes)
        
        return text, changes
    
    def _heavy_humanize(self, text):
        """重度人性化处理"""
        changes = []
        
        # 1. 全面词汇替换
        text, word_changes = self._replace_words(text, ratio=0.9)
        changes.extend(word_changes)
        
        # 2. 句式调整
        text, syntax_changes = self._adjust_syntax(text)
        changes.extend(syntax_changes)
        
        # 3. 添加个性化表达
        text, personal_changes = self._add_personal_expressions(text)
        changes.extend(personal_changes)
        
        # 4. 添加情感色彩
        text, emotion_changes = self._add_emotions(text)
        changes.extend(emotion_changes)
        
        # 5. 增加不确定性
        text, uncertainty_changes = self._add_uncertainty(text)
        changes.extend(uncertainty_changes)
        
        # 6. 添加口语化表达
        text, colloquial_changes = self._add_colloquial_expressions(text, count=5)
        changes.extend(colloquial_changes)
        
        return text, changes
    
    def _replace_words(self, text, ratio=0.7):
        """
        替换AI词汇
        
        Args:
            text: 文本
            ratio: 替换比例（0-1）
        """
        changes = []
        words = list(jieba.cut(text))
        
        for word in words:
            if word in self.replacements and random.random() < ratio:
                replacements = self.replacements[word]
                if replacements:
                    new_word = random.choice(replacements)
                    # 替换第一次出现的位置
                    if word in text:
                        text = text.replace(word, new_word, 1)
                        changes.append(f"词汇替换: '{word}' → '{new_word}'")
        
        return text, changes
    
    def _adjust_syntax(self, text):
        """调整句式"""
        changes = []
        
        # 1. 打破固定句式
        # 将"首先...其次...最后..."改为更自然的表达
        if '首先' in text and '其次' in text:
            text = text.replace('首先', '先说', 1)
            text = text.replace('其次', '再说', 1)
            changes.append("句式调整: 打破'首先...其次'固定句式")
        
        # 2. 简化"不仅...而且..."句式
        pattern = r'不仅(.{2,20})而且(.{2,20})'
        matches = re.findall(pattern, text)
        if matches:
            for match in matches[:2]:  # 最多处理2处
                original = f"不仅{match[0]}而且{match[1]}"
                # 随机选择简化方式
                simplified_patterns = [
                    f"{match[0]}，还{match[1]}",
                    f"{match[0]}，也{match[1]}",
                    f"既{match[0]}又{match[1]}",
                ]
                simplified = random.choice(simplified_patterns)
                text = text.replace(original, simplified, 1)
                changes.append(f"句式简化: '{original}' → '{simplified}'")
        
        # 3. 拆分过长的句子
        sentences = re.split(r'([。！？])', text)
        new_sentences = []
        for i in range(0, len(sentences), 2):
            if i + 1 < len(sentences):
                sentence = sentences[i] + sentences[i + 1]
            else:
                sentence = sentences[i]
            
            # 如果句子太长，尝试在逗号处断句
            if len(sentence) > 50 and '，' in sentence:
                parts = sentence.split('，')
                if len(parts) >= 2:
                    mid = len(parts) // 2
                    first_half = '，'.join(parts[:mid]) + '。'
                    second_half = '，'.join(parts[mid:])
                    new_sentences.append(first_half)
                    new_sentences.append(second_half)
                    changes.append("句式调整: 拆分过长句子")
                    continue
            
            new_sentences.append(sentence)
        
        text = ''.join(new_sentences)
        
        return text, changes
    
    def _add_personal_expressions(self, text):
        """添加个性化表达"""
        changes = []
        sentences = re.split(r'([。！？\n])', text)
        
        # 随机在1-2个句子中添加第一人称
        sentence_indices = [i for i in range(0, len(sentences), 2) if sentences[i].strip()]
        if sentence_indices:
            selected = random.sample(sentence_indices, min(2, len(sentence_indices)))
            for idx in selected:
                sentence = sentences[idx]
                if sentence and len(sentence) > 10:
                    # 在句首添加"我觉得"、"我认为"等
                    first_person = random.choice(['我觉得', '我认为', '个人觉得', '依我看'])
                    sentences[idx] = first_person + sentence
                    changes.append(f"添加第一人称: '{first_person}'")
        
        text = ''.join(sentences)
        return text, changes
    
    def _add_emotions(self, text):
        """添加情感色彩"""
        changes = []
        
        # 在句末随机添加感叹号
        sentences = re.split(r'([。！？])', text)
        sentence_indices = [i for i in range(0, len(sentences), 2) if sentences[i].strip()]
        
        if sentence_indices and len(sentence_indices) > 2:
            selected = random.sample(sentence_indices, min(2, len(sentence_indices)))
            for idx in selected:
                if idx + 1 < len(sentences) and sentences[idx + 1] == '。':
                    # 有一定概率添加情感词
                    if random.random() < 0.5:
                        emotion_word = random.choice(['真的', '确实', '挺'])
                        sentences[idx] = emotion_word + sentences[idx]
                        changes.append(f"添加情感词: '{emotion_word}'")
        
        text = ''.join(sentences)
        return text, changes
    
    def _add_uncertainty(self, text):
        """增加不确定性表达"""
        changes = []
        
        # 将一些绝对表达改为不确定表达
        absolute_words = ['一定', '必须', '肯定', '绝对']
        for word in absolute_words:
            if word in text:
                uncertain = random.choice(UNCERTAINTY_EXPRESSIONS[:5])
                text = text.replace(word, uncertain, 1)
                changes.append(f"降低绝对性: '{word}' → '{uncertain}'")
        
        return text, changes
    
    def _add_colloquial_expressions(self, text, count=3):
        """添加口语化表达"""
        changes = []
        
        sentences = re.split(r'([。！？])', text)
        sentence_indices = [i for i in range(0, len(sentences), 2) if sentences[i].strip()]
        
        if sentence_indices:
            # 随机选择几个句子添加语气词
            selected = random.sample(sentence_indices, min(count, len(sentence_indices)))
            for idx in selected:
                sentence = sentences[idx]
                if sentence and len(sentence) > 5:
                    # 在句末添加语气词
                    if idx + 1 < len(sentences) and sentences[idx + 1] in ['。', '！']:
                        marker = random.choice(COLLOQUIAL_MARKERS[:5])
                        sentences[idx] = sentence + marker
                        changes.append(f"添加语气词: '{marker}'")
        
        text = ''.join(sentences)
        return text, changes
    
    def batch_humanize(self, texts, intensity='medium'):
        """
        批量处理文本
        
        Args:
            texts: 文本列表
            intensity: 处理强度
        
        Returns:
            结果列表
        """
        results = []
        for text in texts:
            result = self.humanize(text, intensity)
            results.append(result)
        return results
    
    def compare(self, original, humanized_result):
        """
        比较原文和处理后的文本
        
        Args:
            original: 原始文本
            humanized_result: humanize()方法返回的结果
        
        Returns:
            格式化的比较报告
        """
        report_lines = []
        
        report_lines.append('=' * 50)
        report_lines.append('文本人性化处理报告')
        report_lines.append('=' * 50)
        report_lines.append('')
        
        report_lines.append(f"处理强度: {humanized_result['intensity']}")
        report_lines.append(f"原文长度: {humanized_result['original_length']}字")
        report_lines.append(f"处理后长度: {humanized_result['modified_length']}字")
        report_lines.append(f"修改次数: {humanized_result['change_count']}处")
        report_lines.append('')
        
        report_lines.append('-' * 50)
        report_lines.append('修改详情：')
        report_lines.append('-' * 50)
        
        for i, change in enumerate(humanized_result['changes'], 1):
            report_lines.append(f"{i}. {change}")
        
        report_lines.append('')
        report_lines.append('-' * 50)
        report_lines.append('原文：')
        report_lines.append('-' * 50)
        report_lines.append(original)
        report_lines.append('')
        
        report_lines.append('-' * 50)
        report_lines.append('处理后：')
        report_lines.append('-' * 50)
        report_lines.append(humanized_result['text'])
        
        report_lines.append('')
        report_lines.append('=' * 50)
        
        return '\n'.join(report_lines)
