"""
使用示例

展示ai-writing-helper的三种使用方式
"""

from ai_humanizer import AIDetector, AIHumanizer


def example_1_detection():
    """示例1：文本检测"""
    print("=" * 60)
    print("示例1：AI文本检测")
    print("=" * 60)
    
    # 创建检测器
    detector = AIDetector()
    
    # 测试文本（典型的AI生成文本）
    ai_text = """
在当今社会，人工智能技术发挥着至关重要的作用。首先，它能够有效地提升工作效率，
使企业能够在激烈的市场竞争中占据优势。其次，人工智能可以显著地优化资源配置，
从而实现成本的有效控制。最后，它还能够深入地改善用户体验，为客户提供更加个性化的服务。

综上所述，人工智能具有重要意义，值得我们持续关注和深入研究。只有充分利用人工智能技术，
才能在未来的发展中取得更大的突破。
    """
    
    # 执行检测
    result = detector.detect(ai_text)
    
    # 显示简要结果
    print("\n【简要结果】")
    print(f"是否为AI生成: {'是' if result['is_ai'] else '否'}")
    print(f"置信度: {result['confidence']:.2%}")
    print(f"综合得分: {result['score']:.2f}/100")
    print(f"\n结论: {result['summary']['conclusion']}")
    print(f"主要问题: {result['summary']['main_issue']}")
    
    # 生成详细报告
    print("\n" + "=" * 60)
    print("【详细报告】")
    print("=" * 60)
    report = detector.generate_report(result)
    print(report)


def example_2_humanization():
    """示例2：文本人性化"""
    print("\n\n" + "=" * 60)
    print("示例2：文本人性化处理")
    print("=" * 60)
    
    # 创建人性化处理器
    humanizer = AIHumanizer()
    
    # 测试文本
    ai_text = """
在当今社会，学习编程变得尤为重要。首先，编程能够有效地提升逻辑思维能力。
其次，它可以显著地增强问题解决能力。最后，编程技能在就业市场上具有重要价值。
综上所述，学习编程具有重要意义。
    """
    
    print("\n【原始文本】")
    print(ai_text)
    
    # 轻度处理
    print("\n" + "-" * 60)
    print("【轻度处理】")
    print("-" * 60)
    result_light = humanizer.humanize(ai_text, intensity='light')
    print(result_light['text'])
    print(f"\n修改次数: {result_light['change_count']}处")
    
    # 中度处理
    print("\n" + "-" * 60)
    print("【中度处理】（推荐）")
    print("-" * 60)
    result_medium = humanizer.humanize(ai_text, intensity='medium')
    print(result_medium['text'])
    print(f"\n修改次数: {result_medium['change_count']}处")
    
    # 重度处理
    print("\n" + "-" * 60)
    print("【重度处理】")
    print("-" * 60)
    result_heavy = humanizer.humanize(ai_text, intensity='heavy')
    print(result_heavy['text'])
    print(f"\n修改次数: {result_heavy['change_count']}处")
    
    # 显示修改详情
    print("\n" + "-" * 60)
    print("【修改详情】（中度处理）")
    print("-" * 60)
    for i, change in enumerate(result_medium['changes'][:10], 1):
        print(f"{i}. {change}")


def example_3_full_workflow():
    """示例3：完整工作流（检测 + 人性化 + 再检测）"""
    print("\n\n" + "=" * 60)
    print("示例3：完整工作流")
    print("=" * 60)
    
    # 创建检测器和处理器
    detector = AIDetector()
    humanizer = AIHumanizer()
    
    # 测试文本
    text = """
随着科技的发展，远程办公变得越来越普遍。首先，远程办公能够有效地节省通勤时间，
提升工作效率。其次，它可以显著地降低企业的运营成本。然而，远程办公也面临一些挑战，
需要我们采取相应措施加以解决。
    """
    
    print("\n【原始文本】")
    print(text)
    
    # 步骤1：检测原始文本
    print("\n" + "=" * 60)
    print("步骤1：检测原始文本")
    print("=" * 60)
    result_before = detector.detect(text)
    print(f"AI得分: {result_before['score']:.2f}/100")
    print(f"结论: {result_before['summary']['conclusion']}")
    print(f"主要问题: {result_before['summary']['main_issue']}")
    
    # 步骤2：人性化处理
    print("\n" + "=" * 60)
    print("步骤2：人性化处理（中度）")
    print("=" * 60)
    humanize_result = humanizer.humanize(text, intensity='medium')
    print("处理后的文本：")
    print(humanize_result['text'])
    print(f"\n修改次数: {humanize_result['change_count']}处")
    
    # 步骤3：检测处理后的文本
    print("\n" + "=" * 60)
    print("步骤3：检测处理后的文本")
    print("=" * 60)
    result_after = detector.detect(humanize_result['text'])
    print(f"AI得分: {result_after['score']:.2f}/100")
    print(f"结论: {result_after['summary']['conclusion']}")
    
    # 对比结果
    print("\n" + "=" * 60)
    print("对比结果")
    print("=" * 60)
    print(f"处理前AI得分: {result_before['score']:.2f}/100")
    print(f"处理后AI得分: {result_after['score']:.2f}/100")
    print(f"得分变化: {result_after['score'] - result_before['score']:.2f}")
    print(f"修改次数: {humanize_result['change_count']}处")


def example_4_batch_processing():
    """示例4：批量处理"""
    print("\n\n" + "=" * 60)
    print("示例4：批量处理多个文本")
    print("=" * 60)
    
    humanizer = AIHumanizer()
    
    # 多个文本
    texts = [
        "首先，这是一个重要的问题。",
        "其次，我们需要深入研究。",
        "最后，我们要采取有效措施。",
        "综上所述，这具有重要意义。"
    ]
    
    print("\n【原始文本】")
    for i, text in enumerate(texts, 1):
        print(f"{i}. {text}")
    
    # 批量处理
    results = humanizer.batch_humanize(texts, intensity='medium')
    
    print("\n【处理后】")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['text']}")
        print(f"   修改: {result['change_count']}处")


def example_5_api_usage():
    """示例5：作为库使用（简洁API）"""
    print("\n\n" + "=" * 60)
    print("示例5：作为Python库使用")
    print("=" * 60)
    
    # 简单的检测
    print("\n【简单检测】")
    detector = AIDetector()
    text = "在当今社会，这个问题至关重要。"
    result = detector.detect(text)
    print(f"文本: {text}")
    print(f"AI得分: {result['score']:.2f}/100")
    
    # 简单的处理
    print("\n【简单处理】")
    humanizer = AIHumanizer()
    result = humanizer.humanize(text)
    print(f"原文: {text}")
    print(f"处理后: {result['text']}")
    
    # 一行代码实现检测+处理
    print("\n【一行流】")
    text2 = "首先，我们要了解问题。其次，要采取措施。"
    processed = AIHumanizer().humanize(text2, intensity='heavy')
    print(f"原文: {text2}")
    print(f"处理后: {processed['text']}")


def main():
    """运行所有示例"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  AI Writing Helper - 使用示例".center(56) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    
    # 运行所有示例
    example_1_detection()
    example_2_humanization()
    example_3_full_workflow()
    example_4_batch_processing()
    example_5_api_usage()
    
    print("\n\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)
    print("\n提示：")
    print("1. 命令行工具: ai-humanizer --help")
    print("2. Web界面: ai-humanizer web")
    print("3. Python库: from ai_humanizer import AIDetector, AIHumanizer")


if __name__ == '__main__':
    main()
