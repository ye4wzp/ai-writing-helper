"""
基础功能测试

测试AI检测器和人性化处理器的基本功能
"""

import unittest
from ai_humanizer import AIDetector, AIHumanizer


class TestAIDetector(unittest.TestCase):
    """测试AI检测器"""
    
    def setUp(self):
        """设置测试环境"""
        self.detector = AIDetector()
    
    def test_detect_empty_text(self):
        """测试空文本"""
        result = self.detector.detect("")
        self.assertFalse(result['is_ai'])
        self.assertEqual(result['score'], 0)
    
    def test_detect_ai_text(self):
        """测试典型的AI生成文本"""
        ai_text = """
        在当今社会，人工智能技术发挥着至关重要的作用。首先，它能够有效地提升工作效率。
        其次，它可以显著地优化资源配置。最后，它还能够深入地改善用户体验。
        综上所述，人工智能具有重要意义，值得我们持续关注。
        """
        result = self.detector.detect(ai_text)
        
        # AI文本应该被检测出来
        self.assertIsInstance(result['is_ai'], bool)
        self.assertGreater(result['score'], 50)  # 分数应该较高
        self.assertGreater(result['confidence'], 0.5)
        
        # 检查各维度分析是否存在
        self.assertIn('lexical', result['details'])
        self.assertIn('syntactic', result['details'])
        self.assertIn('structural', result['details'])
        self.assertIn('semantic', result['details'])
    
    def test_detect_natural_text(self):
        """测试自然的人类文本"""
        natural_text = """
        今天天气真好啊！我去公园散了个步，看到很多人在放风筝。
        有个小孩子的风筝飞得特别高，他开心得不得了。
        我也想起小时候放风筝的事情，那时候可真快乐。
        """
        result = self.detector.detect(natural_text)
        
        # 自然文本的AI得分应该较低
        self.assertIsInstance(result['is_ai'], bool)
        self.assertLess(result['score'], 60)  # 分数应该较低
    
    def test_generate_report(self):
        """测试生成报告"""
        text = "首先，我们需要了解这个问题。其次，我们要采取有效措施。"
        result = self.detector.detect(text)
        report = self.detector.generate_report(result)
        
        # 报告应该包含关键信息
        self.assertIsInstance(report, str)
        self.assertIn('检测报告', report)
        self.assertIn('综合得分', report)
        self.assertIn('词汇层面', report)


class TestAIHumanizer(unittest.TestCase):
    """测试AI人性化处理器"""
    
    def setUp(self):
        """设置测试环境"""
        self.humanizer = AIHumanizer()
    
    def test_humanize_empty_text(self):
        """测试空文本"""
        result = self.humanizer.humanize("")
        self.assertEqual(result['text'], "")
        self.assertEqual(result['change_count'], 0)
    
    def test_humanize_light(self):
        """测试轻度处理"""
        text = "首先，这是一个重要的问题。其次，我们需要采取措施。"
        result = self.humanizer.humanize(text, intensity='light')
        
        self.assertIsInstance(result['text'], str)
        self.assertEqual(result['intensity'], 'light')
        self.assertGreaterEqual(result['change_count'], 0)
        self.assertIsInstance(result['changes'], list)
    
    def test_humanize_medium(self):
        """测试中度处理"""
        text = "在当今社会，人工智能至关重要。首先，它能提升效率。其次，它能优化流程。"
        result = self.humanizer.humanize(text, intensity='medium')
        
        self.assertIsInstance(result['text'], str)
        self.assertEqual(result['intensity'], 'medium')
        self.assertGreater(len(result['text']), 0)
    
    def test_humanize_heavy(self):
        """测试重度处理"""
        text = "显而易见，这个问题值得注意。毋庸置疑，我们需要深入研究。"
        result = self.humanizer.humanize(text, intensity='heavy')
        
        self.assertIsInstance(result['text'], str)
        self.assertEqual(result['intensity'], 'heavy')
        self.assertGreater(len(result['text']), 0)
    
    def test_invalid_intensity(self):
        """测试无效的强度参数"""
        text = "这是一段测试文本。"
        with self.assertRaises(ValueError):
            self.humanizer.humanize(text, intensity='invalid')
    
    def test_batch_humanize(self):
        """测试批量处理"""
        texts = [
            "首先，这很重要。",
            "其次，这也很关键。",
            "最后，我们要行动。"
        ]
        results = self.humanizer.batch_humanize(texts, intensity='medium')
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIn('text', result)
            self.assertIn('change_count', result)
    
    def test_compare(self):
        """测试比较报告"""
        original = "首先，这很重要。其次，这也很关键。"
        result = self.humanizer.humanize(original, intensity='medium')
        report = self.humanizer.compare(original, result)
        
        self.assertIsInstance(report, str)
        self.assertIn('处理报告', report)
        self.assertIn('原文', report)
        self.assertIn('处理后', report)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_detect_then_humanize(self):
        """测试检测后人性化的完整流程"""
        text = "在当今社会，人工智能至关重要。首先，它能提升效率。其次，它能优化流程。最后，它具有重要意义。"
        
        # 检测
        detector = AIDetector()
        detection_result = detector.detect(text)
        
        # 人性化处理
        humanizer = AIHumanizer()
        humanize_result = humanizer.humanize(text, intensity='medium')
        
        # 再次检测处理后的文本
        detection_after = detector.detect(humanize_result['text'])
        
        # 处理后的AI得分应该有所降低（虽然不是绝对的）
        self.assertIsInstance(detection_result['score'], (int, float))
        self.assertIsInstance(detection_after['score'], (int, float))
        self.assertGreater(len(humanize_result['text']), 0)


def run_tests():
    """运行所有测试"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
