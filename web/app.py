"""
Flask Web应用

提供Web界面用于AI文本检测和人性化处理
"""

from flask import Flask, render_template_string, request, jsonify
from ai_humanizer import AIDetector, AIHumanizer

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 支持中文

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Writing Helper - AI文本检测与人性化工具</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .main-content {
            padding: 40px;
        }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid #e0e0e0;
            margin-bottom: 30px;
        }
        
        .tab {
            padding: 15px 30px;
            cursor: pointer;
            background: none;
            border: none;
            font-size: 1.1em;
            color: #666;
            transition: all 0.3s;
        }
        
        .tab.active {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            font-weight: bold;
        }
        
        .tab:hover {
            color: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #333;
        }
        
        textarea {
            width: 100%;
            min-height: 200px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .intensity-select {
            display: flex;
            gap: 15px;
            margin-top: 10px;
        }
        
        .intensity-option {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .intensity-option:hover {
            border-color: #667eea;
            background: #f5f7ff;
        }
        
        .intensity-option.selected {
            border-color: #667eea;
            background: #667eea;
            color: white;
            font-weight: bold;
        }
        
        .btn {
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .result {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            display: none;
        }
        
        .result.show {
            display: block;
        }
        
        .result h3 {
            margin-bottom: 15px;
            color: #333;
        }
        
        .score-display {
            display: flex;
            align-items: center;
            gap: 20px;
            margin: 20px 0;
        }
        
        .score-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2em;
            font-weight: bold;
            color: white;
        }
        
        .score-high {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        .score-medium {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }
        
        .score-low {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #333;
        }
        
        .score-info {
            flex: 1;
        }
        
        .score-info p {
            margin: 8px 0;
            font-size: 1.1em;
        }
        
        .details {
            margin-top: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .detail-card {
            padding: 15px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .detail-card h4 {
            margin-bottom: 10px;
            color: #667eea;
        }
        
        .detail-card p {
            margin: 5px 0;
            color: #666;
        }
        
        .output-text {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.8;
            margin-top: 20px;
        }
        
        .changes-list {
            margin-top: 15px;
            padding-left: 20px;
        }
        
        .changes-list li {
            margin: 5px 0;
            color: #666;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #999;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Writing Helper</h1>
            <p>中文AI文本检测与人性化工具</p>
        </div>
        
        <div class="main-content">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('detect')">AI检测</button>
                <button class="tab" onclick="switchTab('humanize')">人性化处理</button>
                <button class="tab" onclick="switchTab('process')">一键处理</button>
            </div>
            
            <!-- AI检测标签页 -->
            <div id="detect-tab" class="tab-content active">
                <div class="form-group">
                    <label for="detect-input">输入要检测的文本：</label>
                    <textarea id="detect-input" placeholder="请输入要检测的中文文本..."></textarea>
                </div>
                <button class="btn" onclick="detectText()">开始检测</button>
                
                <div class="loading" id="detect-loading">
                    <div class="spinner"></div>
                    <p>正在检测中...</p>
                </div>
                
                <div class="result" id="detect-result">
                    <h3>检测结果</h3>
                    <div class="score-display">
                        <div class="score-circle" id="detect-score-circle">
                            <span id="detect-score">0</span>
                        </div>
                        <div class="score-info">
                            <p><strong>结论：</strong><span id="detect-conclusion"></span></p>
                            <p><strong>置信度：</strong><span id="detect-confidence"></span></p>
                            <p><strong>主要问题：</strong><span id="detect-main-issue"></span></p>
                        </div>
                    </div>
                    <div class="details" id="detect-details"></div>
                </div>
            </div>
            
            <!-- 人性化处理标签页 -->
            <div id="humanize-tab" class="tab-content">
                <div class="form-group">
                    <label for="humanize-input">输入要处理的文本：</label>
                    <textarea id="humanize-input" placeholder="请输入要人性化处理的中文文本..."></textarea>
                </div>
                <div class="form-group">
                    <label>处理强度：</label>
                    <div class="intensity-select">
                        <div class="intensity-option" data-intensity="light" onclick="selectIntensity('humanize', 'light')">
                            <div><strong>轻度</strong></div>
                            <div style="font-size: 0.9em; color: #666;">保守处理</div>
                        </div>
                        <div class="intensity-option selected" data-intensity="medium" onclick="selectIntensity('humanize', 'medium')">
                            <div><strong>中度</strong></div>
                            <div style="font-size: 0.9em; color: #666;">推荐选项</div>
                        </div>
                        <div class="intensity-option" data-intensity="heavy" onclick="selectIntensity('humanize', 'heavy')">
                            <div><strong>重度</strong></div>
                            <div style="font-size: 0.9em; color: #666;">全面改写</div>
                        </div>
                    </div>
                </div>
                <button class="btn" onclick="humanizeText()">开始处理</button>
                
                <div class="loading" id="humanize-loading">
                    <div class="spinner"></div>
                    <p>正在处理中...</p>
                </div>
                
                <div class="result" id="humanize-result">
                    <h3>处理结果</h3>
                    <p><strong>修改次数：</strong><span id="humanize-changes"></span>处</p>
                    <p><strong>处理强度：</strong><span id="humanize-intensity"></span></p>
                    <div class="output-text" id="humanize-output"></div>
                    <details style="margin-top: 15px;">
                        <summary style="cursor: pointer; font-weight: 600;">查看修改详情</summary>
                        <ul class="changes-list" id="humanize-changes-list"></ul>
                    </details>
                </div>
            </div>
            
            <!-- 一键处理标签页 -->
            <div id="process-tab" class="tab-content">
                <div class="form-group">
                    <label for="process-input">输入要处理的文本：</label>
                    <textarea id="process-input" placeholder="请输入文本，系统将自动检测并人性化处理..."></textarea>
                </div>
                <div class="form-group">
                    <label>处理强度：</label>
                    <div class="intensity-select">
                        <div class="intensity-option" data-intensity="light" onclick="selectIntensity('process', 'light')">
                            <div><strong>轻度</strong></div>
                            <div style="font-size: 0.9em; color: #666;">保守处理</div>
                        </div>
                        <div class="intensity-option selected" data-intensity="medium" onclick="selectIntensity('process', 'medium')">
                            <div><strong>中度</strong></div>
                            <div style="font-size: 0.9em; color: #666;">推荐选项</div>
                        </div>
                        <div class="intensity-option" data-intensity="heavy" onclick="selectIntensity('process', 'heavy')">
                            <div><strong>重度</strong></div>
                            <div style="font-size: 0.9em; color: #666;">全面改写</div>
                        </div>
                    </div>
                </div>
                <button class="btn" onclick="processText()">一键处理</button>
                
                <div class="loading" id="process-loading">
                    <div class="spinner"></div>
                    <p>正在处理中...</p>
                </div>
                
                <div class="result" id="process-result">
                    <h3>处理完成</h3>
                    <div class="score-display">
                        <div class="score-circle" id="process-score-circle">
                            <span id="process-score">0</span>
                        </div>
                        <div class="score-info">
                            <p><strong>原始AI得分：</strong><span id="process-original-score"></span></p>
                            <p><strong>修改次数：</strong><span id="process-changes"></span>处</p>
                            <p><strong>处理强度：</strong><span id="process-intensity"></span></p>
                        </div>
                    </div>
                    <div class="output-text" id="process-output"></div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>AI Writing Helper v1.0.0 | 完全本地运行，保护隐私</p>
        </div>
    </div>
    
    <script>
        let currentIntensity = {
            humanize: 'medium',
            process: 'medium'
        };
        
        function switchTab(tabName) {
            // 切换标签样式
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // 切换内容
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tabName + '-tab').classList.add('active');
        }
        
        function selectIntensity(tab, intensity) {
            currentIntensity[tab] = intensity;
            const container = document.getElementById(tab + '-tab');
            container.querySelectorAll('.intensity-option').forEach(option => {
                option.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
        }
        
        async function detectText() {
            const text = document.getElementById('detect-input').value.trim();
            if (!text) {
                alert('请输入要检测的文本');
                return;
            }
            
            // 显示加载状态
            document.getElementById('detect-loading').classList.add('show');
            document.getElementById('detect-result').classList.remove('show');
            
            try {
                const response = await fetch('/api/detect', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                
                // 隐藏加载状态
                document.getElementById('detect-loading').classList.remove('show');
                
                // 显示结果
                displayDetectResult(result);
                document.getElementById('detect-result').classList.add('show');
            } catch (error) {
                alert('检测失败：' + error.message);
                document.getElementById('detect-loading').classList.remove('show');
            }
        }
        
        function displayDetectResult(result) {
            const score = result.score;
            document.getElementById('detect-score').textContent = score.toFixed(0);
            document.getElementById('detect-conclusion').textContent = result.summary.conclusion;
            document.getElementById('detect-confidence').textContent = (result.confidence * 100).toFixed(1) + '%';
            document.getElementById('detect-main-issue').textContent = result.summary.main_issue;
            
            // 设置分数圈颜色
            const circle = document.getElementById('detect-score-circle');
            circle.className = 'score-circle';
            if (score >= 60) {
                circle.classList.add('score-high');
            } else if (score >= 40) {
                circle.classList.add('score-medium');
            } else {
                circle.classList.add('score-low');
            }
            
            // 显示详细信息
            const details = result.details;
            const detailsHtml = `
                <div class="detail-card">
                    <h4>词汇层面</h4>
                    <p>得分: ${details.lexical.score.toFixed(1)}/100</p>
                    <p>AI高频词: ${details.lexical.details.high_freq_words}个</p>
                    <p>连接词: ${details.lexical.details.connectors}个</p>
                </div>
                <div class="detail-card">
                    <h4>句式层面</h4>
                    <p>得分: ${details.syntactic.score.toFixed(1)}/100</p>
                    <p>平均句长: ${details.syntactic.details.avg_sentence_length.toFixed(1)}字</p>
                    <p>固定句式: ${details.syntactic.details.fixed_patterns}处</p>
                </div>
                <div class="detail-card">
                    <h4>结构层面</h4>
                    <p>得分: ${details.structural.score.toFixed(1)}/100</p>
                    <p>段落数: ${details.structural.details.paragraph_count}段</p>
                    <p>总分总结构: ${details.structural.details.has_opening_pattern || details.structural.details.has_closing_pattern ? '是' : '否'}</p>
                </div>
                <div class="detail-card">
                    <h4>语义层面</h4>
                    <p>得分: ${details.semantic.score.toFixed(1)}/100</p>
                    <p>限定词: ${details.semantic.details.qualifier_count}个</p>
                    <p>情感词: ${details.semantic.details.emotion_count}个</p>
                </div>
            `;
            document.getElementById('detect-details').innerHTML = detailsHtml;
        }
        
        async function humanizeText() {
            const text = document.getElementById('humanize-input').value.trim();
            if (!text) {
                alert('请输入要处理的文本');
                return;
            }
            
            const intensity = currentIntensity.humanize;
            
            // 显示加载状态
            document.getElementById('humanize-loading').classList.add('show');
            document.getElementById('humanize-result').classList.remove('show');
            
            try {
                const response = await fetch('/api/humanize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text, intensity: intensity })
                });
                
                const result = await response.json();
                
                // 隐藏加载状态
                document.getElementById('humanize-loading').classList.remove('show');
                
                // 显示结果
                displayHumanizeResult(result);
                document.getElementById('humanize-result').classList.add('show');
            } catch (error) {
                alert('处理失败：' + error.message);
                document.getElementById('humanize-loading').classList.remove('show');
            }
        }
        
        function displayHumanizeResult(result) {
            document.getElementById('humanize-changes').textContent = result.change_count;
            document.getElementById('humanize-intensity').textContent = result.intensity;
            document.getElementById('humanize-output').textContent = result.text;
            
            // 显示修改列表
            const changesList = document.getElementById('humanize-changes-list');
            changesList.innerHTML = '';
            result.changes.forEach(change => {
                const li = document.createElement('li');
                li.textContent = change;
                changesList.appendChild(li);
            });
        }
        
        async function processText() {
            const text = document.getElementById('process-input').value.trim();
            if (!text) {
                alert('请输入要处理的文本');
                return;
            }
            
            const intensity = currentIntensity.process;
            
            // 显示加载状态
            document.getElementById('process-loading').classList.add('show');
            document.getElementById('process-result').classList.remove('show');
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ text: text, intensity: intensity })
                });
                
                const result = await response.json();
                
                // 隐藏加载状态
                document.getElementById('process-loading').classList.remove('show');
                
                // 显示结果
                displayProcessResult(result);
                document.getElementById('process-result').classList.add('show');
            } catch (error) {
                alert('处理失败：' + error.message);
                document.getElementById('process-loading').classList.remove('show');
            }
        }
        
        function displayProcessResult(result) {
            const score = result.detection.score;
            document.getElementById('process-score').textContent = score.toFixed(0);
            document.getElementById('process-original-score').textContent = score.toFixed(1) + '/100';
            document.getElementById('process-changes').textContent = result.humanize.change_count;
            document.getElementById('process-intensity').textContent = result.humanize.intensity;
            document.getElementById('process-output').textContent = result.humanize.text;
            
            // 设置分数圈颜色
            const circle = document.getElementById('process-score-circle');
            circle.className = 'score-circle';
            if (score >= 60) {
                circle.classList.add('score-high');
            } else if (score >= 40) {
                circle.classList.add('score-medium');
            } else {
                circle.classList.add('score-low');
            }
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """首页"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/detect', methods=['POST'])
def api_detect():
    """检测API"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        
        detector = AIDetector()
        result = detector.detect(text)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/humanize', methods=['POST'])
def api_humanize():
    """人性化API"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        intensity = data.get('intensity', 'medium')
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        
        if intensity not in ['light', 'medium', 'heavy']:
            return jsonify({'error': '无效的处理强度'}), 400
        
        humanizer = AIHumanizer()
        result = humanizer.humanize(text, intensity=intensity)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
def api_process():
    """一键处理API"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        intensity = data.get('intensity', 'medium')
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        
        if intensity not in ['light', 'medium', 'heavy']:
            return jsonify({'error': '无效的处理强度'}), 400
        
        # 检测
        detector = AIDetector()
        detection_result = detector.detect(text)
        
        # 人性化处理
        humanizer = AIHumanizer()
        humanize_result = humanizer.humanize(text, intensity=intensity)
        
        return jsonify({
            'detection': detection_result,
            'humanize': humanize_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
