import os
import re

files = [
    'public/week1_pandas.html',
    'public/week2_eda.html',
    'public/week3_stats.html',
    'public/week4_ml.html',
    'public/week5_mock_test.html'
]

NEW_CSS = """
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden; /* 전체 페이지 스크롤 방지 */
        }
        
        .layout-wrapper {
            display: flex;
            width: 100vw;
            height: 100vh;
        }

        .content-panel {
            flex: 1;
            overflow-y: auto;
            padding: 40px;
            /* 기존 바디에 있던 배경 효과를 이쪽으로 옮김 */
            background-image: radial-gradient(at 0% 0%, var(--accent) 0px, transparent 80%);
            background-color: var(--bg-color);
        }

        .content-inner {
            max-width: 800px;
            margin: 0 auto;
        }

        .ide-panel {
            flex: 1;
            background: rgba(10, 15, 30, 0.95);
            border-left: 2px solid var(--glass-border);
            padding: 30px;
            display: flex;
            flex-direction: column;
            box-shadow: -10px 0 30px rgba(0,0,0,0.5);
        }

        .ide-panel h2 { margin-top: 0; border: none; }
        
        #python-editor {
            flex: 1;
            min-height: 200px;
            background: #1e1e1e; color: #d4d4d4; 
            font-family: 'Consolas', 'Courier New', monospace; font-size: 15px;
            border: 1px solid var(--glass-border); border-radius: 8px; 
            padding: 15px; margin-bottom: 20px; resize: none; outline: none;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }

        #python-editor:focus {
            border-color: var(--accent);
        }

        #console-output {
            background: #000; color: #0f0; 
            padding: 15px; border-radius: 8px; 
            height: 250px; font-family: 'Consolas', monospace; 
            white-space: pre-wrap; overflow-y: auto; border: 1px solid #333;
        }
"""

IDE_HTML = """
        <div class="ide-panel">
            <h2 style="color: var(--accent);">💻 웹 파이썬 실행기</h2>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 20px;">
                왼쪽 창의 설명을 보면서 자유롭게 코딩해 보세요!<br>
                💡 <strong>데이터 경로:</strong> <code>pd.read_csv('data/titanic.csv')</code> (../ 생략)
            </p>
            
            <textarea id="python-editor" spellcheck="false" placeholder="# 여기에 파이썬 코드를 작성하세요...
import pandas as pd
df = pd.read_csv('data/titanic.csv')
print(df.head())"></textarea>
            
            <button class="btn" id="run-btn" onclick="runPython()" style="width: 100%; justify-content: center; font-size: 1.1rem; padding: 15px; margin-bottom: 20px;">
                ▶ 파이썬 코드 실행
            </button>

            <h3 style="color: #94a3b8; font-size: 1rem; margin: 0 0 10px 0;">출력 결과 (Console)</h3>
            <pre id="console-output">대기 중...</pre>
        </div>
"""

JS_LOGIC = """
        async function runPython() {
            const code = document.getElementById('python-editor').value;
            const outputEl = document.getElementById('console-output');
            const runBtn = document.getElementById('run-btn');
            
            if (!code.trim()) {
                outputEl.innerText = '코드를 입력해주세요.';
                return;
            }

            runBtn.innerText = '⏳ 실행 중...';
            runBtn.style.opacity = '0.7';
            runBtn.disabled = true;
            outputEl.innerText = '서버에서 파이썬 코드를 실행 중입니다...';

            try {
                const response = await fetch('/api/run-python', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code: code })
                });

                const result = await response.json();
                
                if (result.success) {
                    outputEl.style.color = '#0f0';
                    outputEl.innerText = result.output || '실행 성공 (출력 없음)';
                } else {
                    outputEl.style.color = '#ff4444';
                    outputEl.innerText = result.output;
                }
            } catch (error) {
                outputEl.style.color = '#ff4444';
                outputEl.innerText = '서버 통신 오류: ' + error.message;
            } finally {
                runBtn.innerText = '▶ 파이썬 코드 실행';
                runBtn.style.opacity = '1';
                runBtn.disabled = false;
            }
        }
"""

for fpath in files:
    full_path = os.path.join('d:/dev/mining', fpath)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 기존 5주차에 있던 수동 IDE 섹션과 JS 스크립트 깔끔하게 제거
    content = re.sub(r'<div class="card" id="ide-section".*?</div>\s*</div>', '</div>', content, flags=re.DOTALL)
    content = re.sub(r'async function runPython\(\).*?\}\s*\}', '', content, flags=re.DOTALL)
    
    # 2. CSS 정리 (기존 body, .container 속성 삭제)
    content = re.sub(r'body\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.container\s*\{[^}]*\}', '', content)
    content = content.replace('</style>', NEW_CSS + '\n    </style>')
    
    # 3. HTML 레이아웃 정리
    # <body> 태그 뒤에 layout-wrapper 추가
    content = content.replace('<body>', '<body>\n    <div class="layout-wrapper">')
    # <div class="container"> 를 <div class="content-panel"><div class="content-inner"> 로 대체
    content = content.replace('<div class="container">', '<div class="content-panel">\n        <div class="content-inner">')
    
    # 왼쪽 패널의 끝을 알맞게 닫고 오른쪽 패널 추가
    # 마지막 </div> 닫는 부분을 찾아야 한다.
    # Prism.js 포함하는 스크립트 앞부분이 전체 컨테이너가 끝나는 곳이다.
    parts = content.split('<!-- 구문 강조를 위한 Prism.js -->')
    if len(parts) == 2:
        part1 = parts[0]
        # part1의 마지막 </div>를 두 번 닫음 (content-inner, content-panel)
        # 문자열 뒤에서부터 첫번째 </div>를 찾는다
        last_div_idx = part1.rfind('</div>')
        if last_div_idx != -1:
            part1 = part1[:last_div_idx] + '</div>\n        </div>\n' + IDE_HTML + '\n    </div>\n\n'
        content = part1 + '<!-- 구문 강조를 위한 Prism.js -->' + parts[1]
    
    # 4. 자바스크립트 추가
    if 'runPython' not in content:
        content = content.replace('</script>\n</body>', JS_LOGIC + '\n    </script>\n</body>')
        
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"✅ {len(files)}개 파일 분할 레이아웃 변환 완료!")
