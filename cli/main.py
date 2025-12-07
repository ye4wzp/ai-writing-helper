"""
命令行工具

使用Click框架实现的命令行界面
"""

import click
import sys
from ai_humanizer import AIDetector, AIHumanizer


@click.group()
@click.version_option(version='1.0.0', prog_name='ai-humanizer')
def cli():
    """
    AI Writing Helper - 中文AI文本检测与人性化工具
    
    一个完全基于规则的本地工具，用于检测和改写AI生成的中文文本
    """
    pass


@cli.command()
@click.argument('text', type=str, required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='从文件读取文本')
@click.option('--report', '-r', is_flag=True, help='显示详细报告')
def detect(text, file, report):
    """
    检测文本的AI特征
    
    示例：
    
    \b
    1. 检测直接输入的文本：
       ai-humanizer detect "这是一段需要检测的文本"
    
    \b
    2. 检测文件中的文本：
       ai-humanizer detect -f input.txt
    
    \b
    3. 显示详细报告：
       ai-humanizer detect -f input.txt --report
    """
    # 获取要检测的文本
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif text:
        pass
    else:
        click.echo("错误：请提供要检测的文本或使用 --file 指定文件", err=True)
        sys.exit(1)
    
    if not text or not text.strip():
        click.echo("错误：文本内容为空", err=True)
        sys.exit(1)
    
    # 执行检测
    click.echo("正在检测文本...")
    detector = AIDetector()
    result = detector.detect(text)
    
    # 显示结果
    if report:
        # 显示详细报告
        report_text = detector.generate_report(result)
        click.echo(report_text)
    else:
        # 显示简要结果
        click.echo("\n" + "=" * 50)
        click.echo("检测结果")
        click.echo("=" * 50)
        click.echo(f"是否为AI生成: {'是' if result['is_ai'] else '否'}")
        click.echo(f"置信度: {result['confidence']:.2%}")
        click.echo(f"综合得分: {result['score']:.2f}/100")
        click.echo(f"文本长度: {result['text_length']}字")
        click.echo("\n" + result['summary']['conclusion'])
        click.echo(result['summary']['main_issue'])
        click.echo("=" * 50)
        click.echo("\n提示：使用 --report 参数查看详细分析报告")


@cli.command()
@click.argument('text', type=str, required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='从文件读取文本')
@click.option('--output', '-o', type=click.Path(), help='输出到文件')
@click.option('--intensity', '-i', 
              type=click.Choice(['light', 'medium', 'heavy'], case_sensitive=False),
              default='medium',
              help='处理强度（light/medium/heavy）')
@click.option('--compare', '-c', is_flag=True, help='显示对比报告')
def humanize(text, file, output, intensity, compare):
    """
    将文本人性化处理
    
    示例：
    
    \b
    1. 处理直接输入的文本：
       ai-humanizer humanize "这是一段需要处理的文本"
    
    \b
    2. 处理文件中的文本：
       ai-humanizer humanize -f input.txt
    
    \b
    3. 指定处理强度：
       ai-humanizer humanize -f input.txt -i heavy
    
    \b
    4. 输出到文件：
       ai-humanizer humanize -f input.txt -o output.txt
    
    \b
    5. 显示对比报告：
       ai-humanizer humanize -f input.txt --compare
    """
    # 获取要处理的文本
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif text:
        pass
    else:
        click.echo("错误：请提供要处理的文本或使用 --file 指定文件", err=True)
        sys.exit(1)
    
    if not text or not text.strip():
        click.echo("错误：文本内容为空", err=True)
        sys.exit(1)
    
    # 执行人性化处理
    click.echo(f"正在以 {intensity} 强度处理文本...")
    humanizer = AIHumanizer()
    result = humanizer.humanize(text, intensity=intensity)
    
    # 输出结果
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        click.echo(f"\n处理完成！结果已保存到: {output}")
    else:
        click.echo("\n" + "=" * 50)
        click.echo("处理结果")
        click.echo("=" * 50)
        click.echo(result['text'])
        click.echo("=" * 50)
    
    # 显示处理信息
    if compare:
        # 显示详细对比报告
        report = humanizer.compare(text, result)
        click.echo("\n" + report)
    else:
        # 显示简要信息
        click.echo(f"\n处理强度: {intensity}")
        click.echo(f"修改次数: {result['change_count']}处")
        click.echo(f"原文长度: {result['original_length']}字")
        click.echo(f"处理后长度: {result['modified_length']}字")
        click.echo("\n提示：使用 --compare 参数查看详细对比报告")


@cli.command()
@click.argument('text', type=str, required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='从文件读取文本')
@click.option('--output', '-o', type=click.Path(), help='输出到文件')
@click.option('--intensity', '-i', 
              type=click.Choice(['light', 'medium', 'heavy'], case_sensitive=False),
              default='medium',
              help='处理强度（light/medium/heavy）')
def process(text, file, output, intensity):
    """
    一键处理：检测并人性化（完整流程）
    
    示例：
    
    \b
    1. 一键处理文本：
       ai-humanizer process -f input.txt -o output.txt
    
    \b
    2. 指定处理强度：
       ai-humanizer process -f input.txt -o output.txt -i heavy
    """
    # 获取文本
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif text:
        pass
    else:
        click.echo("错误：请提供要处理的文本或使用 --file 指定文件", err=True)
        sys.exit(1)
    
    if not text or not text.strip():
        click.echo("错误：文本内容为空", err=True)
        sys.exit(1)
    
    # 步骤1：检测
    click.echo("步骤 1/2: 检测文本AI特征...")
    detector = AIDetector()
    detection_result = detector.detect(text)
    
    click.echo(f"检测完成 - AI得分: {detection_result['score']:.2f}/100")
    
    # 步骤2：人性化处理
    click.echo(f"\n步骤 2/2: 以 {intensity} 强度进行人性化处理...")
    humanizer = AIHumanizer()
    humanize_result = humanizer.humanize(text, intensity=intensity)
    
    click.echo(f"处理完成 - 修改了 {humanize_result['change_count']} 处")
    
    # 输出结果
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(humanize_result['text'])
        click.echo(f"\n✓ 结果已保存到: {output}")
    else:
        click.echo("\n" + "=" * 50)
        click.echo("处理后的文本")
        click.echo("=" * 50)
        click.echo(humanize_result['text'])
        click.echo("=" * 50)
    
    # 显示摘要
    click.echo("\n" + "=" * 50)
    click.echo("处理摘要")
    click.echo("=" * 50)
    click.echo(f"原始文本AI得分: {detection_result['score']:.2f}/100")
    click.echo(f"处理强度: {intensity}")
    click.echo(f"修改次数: {humanize_result['change_count']}处")
    click.echo("=" * 50)


@cli.command()
@click.option('--port', '-p', default=5000, help='端口号，默认5000')
@click.option('--host', '-h', default='127.0.0.1', help='主机地址，默认127.0.0.1')
@click.option('--debug', '-d', is_flag=True, help='启用调试模式')
def web(port, host, debug):
    """
    启动Web服务
    
    示例：
    
    \b
    1. 启动Web服务（默认端口5000）：
       ai-humanizer web
    
    \b
    2. 指定端口：
       ai-humanizer web -p 8080
    
    \b
    3. 启用调试模式：
       ai-humanizer web --debug
    """
    try:
        from web.app import app
        click.echo(f"启动Web服务...")
        click.echo(f"访问地址: http://{host}:{port}")
        click.echo("按 Ctrl+C 停止服务")
        app.run(host=host, port=port, debug=debug)
    except ImportError:
        click.echo("错误：无法导入Web模块，请确保已安装Flask", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"错误：{str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
