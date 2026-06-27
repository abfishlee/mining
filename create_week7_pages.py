import os

TEMPLATE_START = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <style>
        :root {{
            --bg-color: #0f172a;
            --surface-color: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: {accent};
            --accent-hover: {accent_hover};
            --glass-border: rgba(255, 255, 255, 0.1);
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
        }}
        
        .layout-wrapper {{ display: flex; width: 100vw; height: 100vh; }}
        .content-panel {{ flex: 1; overflow-y: auto; padding: 40px; background-image: radial-gradient(at 0% 0%, var(--accent) 0px, transparent 80%); background-color: var(--bg-color); }}
        .content-inner {{ max-width: 800px; margin: 0 auto; }}
        .ide-panel {{ flex: 1; background: rgba(10, 15, 30, 0.95); border-left: 2px solid var(--glass-border); padding: 30px; display: flex; flex-direction: column; box-shadow: -10px 0 30px rgba(0,0,0,0.5); }}
        .ide-panel h2 {{ margin-top: 0; border: none; }}
        
        #python-editor {{ flex: 1; min-height: 200px; background: #1e1e1e; color: #d4d4d4; font-family: 'Consolas', 'Courier New', monospace; font-size: 15px; border: 1px solid var(--glass-border); border-radius: 8px; padding: 15px; margin-bottom: 20px; resize: none; outline: none; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }}
        #python-editor:focus {{ border-color: var(--accent); }}
        #console-output {{ background: #000; color: #0f0; padding: 15px; border-radius: 8px; height: 250px; font-family: 'Consolas', monospace; white-space: pre-wrap; overflow-y: auto; border: 1px solid #333; }}

        .back-link {{ color: var(--text-muted); text-decoration: none; display: inline-flex; align-items: center; gap: 5px; margin-bottom: 20px; transition: color 0.3s; }}
        .back-link:hover {{ color: var(--text-main); }}
        header {{ text-align: center; margin-bottom: 50px; animation: fadeIn 1s ease-out; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 10px; color: var(--accent); }}
        .card {{ background: var(--surface-color); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid var(--glass-border); border-radius: 16px; padding: 30px; margin-bottom: 30px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); transform: translateY(20px); opacity: 0; animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
        h2 {{ border-bottom: 2px solid var(--glass-border); padding-bottom: 10px; margin-top: 0; display: flex; align-items: center; gap: 10px; }}
        .metaphor {{ background: rgba(255,255,255,0.05); border-left: 4px solid var(--accent); padding: 15px; border-radius: 0 8px 8px 0; font-style: italic; color: #bae6fd; margin-bottom: 20px; }}
        .pro-tip {{ border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.08); }}
        .pro-tip h2 {{ border-bottom: none; color: #fca5a5; }}
        pre {{ border-radius: 8px !important; margin: 20px 0 !important; border: 1px solid var(--glass-border); }}
        .btn {{ background-color: var(--accent); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.9rem; transition: all 0.3s ease; }}
        .btn:hover {{ background-color: var(--accent-hover); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(255,255,255,0.1); }}
        .answer-box {{ max-height: 0; overflow: hidden; transition: max-height 0.5s ease; opacity: 0; }}
        .answer-box.show {{ max-height: 2000px; opacity: 1; transition: max-height 0.5s ease-in-out, opacity 0.5s ease-in-out 0.2s; }}
        .drill-section {{ margin-top: 40px; }}
        .drill-item {{ background: rgba(0, 0, 0, 0.2); padding: 20px; border-radius: 8px; margin-bottom: 15px; border: 1px solid var(--glass-border); }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        @keyframes slideUp {{ to {{ transform: translateY(0); opacity: 1; }} }}
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg-color); }}
        ::-webkit-scrollbar-thumb {{ background: var(--glass-border); border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: var(--text-muted); }}
    </style>
</head>
<body>
    <div class="layout-wrapper">
        <div class="content-panel">
            <div class="content-inner">
                <a href="index.html" class="back-link">← 대시보드로 돌아가기</a>
                <header>
                    <h1>{title}</h1>
                    <p>{subtitle}</p>
                </header>
"""

TEMPLATE_END = """
            </div>
        </div>
        <div class="ide-panel">
            <h2 style="color: var(--accent);">💻 웹 파이썬 실행기</h2>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 20px;">
                왼쪽 창의 문제를 보고, 여기서 자유롭게 코딩하세요!<br>
                💡 <strong>데이터 경로:</strong> <code>pd.read_csv('data/titanic.csv')</code>
            </p>
            <textarea id="python-editor" spellcheck="false" placeholder="# 여기에 코드를 작성하세요..."></textarea>
            <button class="btn" id="run-btn" onclick="runPython()" style="width: 100%; justify-content: center; font-size: 1.1rem; padding: 15px; margin-bottom: 20px;">
                ▶ 파이썬 코드 실행
            </button>
            <h3 style="color: #94a3b8; font-size: 1rem; margin: 0 0 10px 0;">출력 결과 (Console)</h3>
            <pre id="console-output">대기 중...</pre>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script>
        function toggleAnswer(id) {
            const el = document.getElementById(id);
            if (el.classList.contains('show')) el.classList.remove('show');
            else el.classList.add('show');
        }
        async function runPython() {
            const code = document.getElementById('python-editor').value;
            const outputEl = document.getElementById('console-output');
            const runBtn = document.getElementById('run-btn');
            if (!code.trim()) { outputEl.innerText = '코드를 입력해주세요.'; return; }
            runBtn.innerText = '⏳ 실행 중...'; runBtn.disabled = true;
            outputEl.innerText = '서버에서 실행 중입니다...';
            try {
                const res = await fetch('/api/run-python', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code: code })
                });
                const result = await res.json();
                if (result.success) { outputEl.style.color = '#0f0'; outputEl.innerText = result.output || '실행 성공'; }
                else { outputEl.style.color = '#ff4444'; outputEl.innerText = result.output; }
            } catch (err) { outputEl.style.color = '#ff4444'; outputEl.innerText = '오류: ' + err.message; }
            finally { runBtn.innerText = '▶ 파이썬 코드 실행'; runBtn.disabled = false; }
        }
    </script>
</body>
</html>
"""

PAGES = [
    {
        "filename": "week7_1_adp_mock.html",
        "title": "Week 7-1: ADP 실전 모의고사 (지도학습/회귀)",
        "subtitle": "다중공선성 처리부터 불균형 데이터 평가지표까지!",
        "accent": "#6366f1", "accent_hover": "#4f46e5",
        "content": """
                <div class="card pro-tip">
                    <h2>🔥 ADP 실기 시험 생존 팁</h2>
                    <ul>
                        <li><strong>코드보다 '왜?'가 중요합니다:</strong> 결측치를 왜 평균으로 채웠는지 주석이나 서술형으로 설명하세요.</li>
                        <li><strong>분석 결과 해석:</strong> "정확도가 85%입니다"에서 끝나지 말고, "ROC-AUC가 우수하여 변별력이 높다"고 서술해야 합니다.</li>
                    </ul>
                </div>

                <div class="card drill-section">
                    <h2>📝 모의고사 1: 다중공선성 처리 및 회귀 (50점)</h2>
                    <div class="drill-item">
                        <p><strong>[요구사항]</strong><br>1. <code>tips.csv</code>를 로드하고 범주형 변수를 원핫 인코딩(drop_first=True)하세요.<br>2. 'total_bill'과 파생변수 간 VIF를 확인하고 10 이상인 경우의 조치사항을 서술하세요.<br>3. RandomForestRegressor로 'tip'을 예측하고 RMSE를 구하세요.</p>
                        <button class="btn" onclick="toggleAnswer('ans1')">👁️ 정답 보기</button>
                        <div id="ans1" class="answer-box">
                            <pre><code class="language-python">import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv('data/tips.csv')
df_encoded = pd.get_dummies(df, drop_first=True)
X = df_encoded.drop('tip', axis=1)
y = df_encoded['tip']

vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif["features"] = X.columns
print(vif)
# 서술: VIF가 10을 초과하는 변수가 있다면 제거하거나 다중공선성에 강한 트리기반 모델을 사용합니다.

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, pred)):.3f}")</code></pre>
                        </div>
                    </div>
                </div>

                <div class="card drill-section">
                    <h2>📝 모의고사 2: 불균형 데이터 분류 평가 (50점)</h2>
                    <div class="drill-item">
                        <p><strong>[요구사항]</strong><br>1. <code>titanic.csv</code> 결측치 처리 후 Pclass, Sex(수치화), Age, Fare로 Survived를 예측합니다.<br>2. 데이터 불균형을 고려하여 F1-score와 ROC-AUC를 계산하세요.</p>
                        <button class="btn" onclick="toggleAnswer('ans2')">👁️ 정답 보기</button>
                        <div id="ans2" class="answer-box">
                            <pre><code class="language-python">import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score

df = pd.read_csv('data/titanic.csv').fillna(0)
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
X = df[['Pclass', 'Sex', 'Age', 'Fare']]
y = df['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
pred_proba = model.predict_proba(X_test)[:, 1] # 1일 확률

print(f"F1: {f1_score(y_test, pred):.3f}")
print(f"ROC-AUC: {roc_auc_score(y_test, pred_proba):.3f}")</code></pre>
                        </div>
                    </div>
                </div>
        """
    },
    {
        "filename": "week7_2_adp_mock.html",
        "title": "Week 7-2: ADP 실전 모의고사 (고급/최적화)",
        "subtitle": "비지도학습부터 하이퍼파라미터 튜닝까지!",
        "accent": "#8b5cf6", "accent_hover": "#7c3aed",
        "content": """
                <div class="card drill-section">
                    <h2>📝 모의고사 3: 비지도학습과 ANOVA 검정 (30점)</h2>
                    <div class="drill-item">
                        <p><strong>[요구사항]</strong><br>1. <code>iris.csv</code>에서 종(species)을 제거하고 스케일링하세요.<br>2. K-Means 군집화(K=3)를 수행하고 파생변수로 추가하세요.<br>3. 3개 군집 간 'sepal_length' 평균 차이가 유의미한지 일원 분산 분석(ANOVA)을 수행하세요.</p>
                        <button class="btn" onclick="toggleAnswer('ans3')">👁️ 정답 보기</button>
                        <div id="ans3" class="answer-box">
                            <pre><code class="language-python">import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy import stats

iris = pd.read_csv('data/iris.csv')
X = iris.drop('species', axis=1)

X_scaled = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
iris['cluster'] = kmeans.fit_predict(X_scaled)

c0 = iris[iris['cluster'] == 0]['sepal_length']
c1 = iris[iris['cluster'] == 1]['sepal_length']
c2 = iris[iris['cluster'] == 2]['sepal_length']

f_stat, p_val = stats.f_oneway(c0, c1, c2)
print(f"ANOVA p-value: {p_val:.5f}")
# 서술: p-value가 0.05 미만이므로 군집 간 평균 차이가 유의미함.</code></pre>
                        </div>
                    </div>
                </div>

                <div class="card drill-section">
                    <h2>📝 모의고사 4: 시계열 데이터 가공 (30점)</h2>
                    <div class="drill-item">
                        <p><strong>[요구사항]</strong><br>1. <code>tips.csv</code>에 <code>pd.date_range()</code>를 써서 2023-01-01부터 1일 간격의 'date' 열을 추가하세요.<br>2. '월(month)'을 추출하여 파생변수를 만들고, 월별 'total_bill' 총합을 집계하세요.</p>
                        <button class="btn" onclick="toggleAnswer('ans4')">👁️ 정답 보기</button>
                        <div id="ans4" class="answer-box">
                            <pre><code class="language-python">import pandas as pd
df = pd.read_csv('data/tips.csv')
df['date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
df['month'] = df['date'].dt.month
monthly_bill = df.groupby('month')['total_bill'].sum()
print(monthly_bill)</code></pre>
                        </div>
                    </div>
                </div>

                <div class="card drill-section">
                    <h2>📝 [추가] 모의고사 5: 그리드 서치 최적화 (40점)</h2>
                    <div class="metaphor">"하이퍼파라미터를 손으로 하나씩 맞추는 건 노가다입니다. 기계가 알아서 최고의 조합을 찾도록 GridSearchCV를 활용하세요!"</div>
                    <div class="drill-item">
                        <p><strong>[요구사항]</strong><br>1. <code>titanic.csv</code> 데이터를 불러와 <code>RandomForestClassifier</code>를 준비합니다. (Pclass, Sex, Age 만 사용, 결측치는 0 처리)<br>2. <code>GridSearchCV</code>를 사용해 <code>n_estimators: [50, 100]</code>, <code>max_depth: [3, 5]</code> 중 최고의 파라미터 조합을 찾으세요.<br>3. <code>best_params_</code>를 출력하세요.</p>
                        <button class="btn" onclick="toggleAnswer('ans5')">👁️ 정답 보기</button>
                        <div id="ans5" class="answer-box">
                            <pre><code class="language-python">import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

df = pd.read_csv('data/titanic.csv').fillna(0)
df['Sex'] = df['Sex'].map({'male':0, 'female':1})
X = df[['Pclass', 'Sex', 'Age']]
y = df['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 파라미터 그리드 딕셔너리
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [3, 5]
}

# GridSearchCV 세팅 (cv=3 은 3번의 교차검증을 의미)
grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3)
grid_search.fit(X_train, y_train)

print("최고의 파라미터 조합:", grid_search.best_params_)
print("최고 점수:", round(grid_search.best_score_, 3))</code></pre>
                        </div>
                    </div>
                </div>
        """
    }
]

for page in PAGES:
    html_content = TEMPLATE_START.format(
        title=page["title"], 
        subtitle=page["subtitle"],
        accent=page["accent"],
        accent_hover=page["accent_hover"]
    )
    html_content += page["content"]
    html_content += TEMPLATE_END
    
    filepath = os.path.join('d:/dev/mining/public', page["filename"])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
print("7주차 분할 생성 완료!")
