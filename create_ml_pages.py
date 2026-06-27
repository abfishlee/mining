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
        .pro-tip {{ border-left: 4px solid #f59e0b; background: rgba(245, 158, 11, 0.08); }}
        .pro-tip h2 {{ border-bottom: none; color: #fbbf24; }}
        pre {{ border-radius: 8px !important; margin: 20px 0 !important; border: 1px solid var(--glass-border); }}
        .btn {{ background-color: var(--accent); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.9rem; transition: all 0.3s ease; }}
        .btn:hover {{ background-color: var(--accent-hover); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(255,255,255,0.1); }}
        .answer-box {{ max-height: 0; overflow: hidden; transition: max-height 0.5s ease; opacity: 0; }}
        .answer-box.show {{ max-height: 1500px; opacity: 1; transition: max-height 0.5s ease-in-out, opacity 0.5s ease-in-out 0.2s; }}
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
        "filename": "week4_1_ml_basic.html",
        "title": "Week 4-1: 머신러닝 기초 (단일 모델)",
        "subtitle": "데이터의 흐름을 이해하는 가장 직관적인 기초 알고리즘",
        "accent": "#3b82f6", "accent_hover": "#2563eb",
        "content": """
                <div class="card">
                    <h2>🎯 1. K-Nearest Neighbors (KNN)</h2>
                    <div class="metaphor">"당신의 친구 5명이 모두 짜장면을 좋아한다면, 당신도 짜장면을 좋아할 확률이 높습니다! KNN은 '가장 가까운 이웃'들의 성향을 보고 나의 성향을 예측하는 가장 직관적인 알고리즘입니다."</div>
                    <p>데이터 간의 <strong>거리(Distance)</strong>를 측정하여 분류나 회귀를 수행합니다. 거리를 계산하므로 반드시 <strong>스케일링(StandardScaler 등)</strong>이 선행되어야 합니다!</p>
                    <pre><code class="language-python">from sklearn.neighbors import KNeighborsClassifier
# 이웃 5명을 보고 판단하겠다 (n_neighbors=5)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)</code></pre>
                </div>

                <div class="card">
                    <h2>📈 2. 로지스틱 회귀 (Logistic Regression)</h2>
                    <div class="metaphor">"이름은 '회귀'지만 사실은 '분류' 모델입니다. 타이타닉 호에서 살 확률(0~100%)을 계산하여, 50%가 넘으면 생존(1), 아니면 사망(0)으로 도장을 쾅 찍습니다."</div>
                    <p>S자 형태의 시그모이드(Sigmoid) 함수를 이용하여 결과를 0과 1 사이의 확률로 변환합니다.</p>
                </div>

                <div class="card">
                    <h2>🌳 3. 의사결정나무 (Decision Tree)</h2>
                    <div class="metaphor">"20고개 게임을 아시나요? '나이가 30살 이상인가요?', '성별이 남자인가요?' 이렇게 데이터를 가장 잘 나눌 수 있는 질문(조건)을 찾아 나뭇가지처럼 계속 뻗어 내려가는 알고리즘입니다."</div>
                    <p>의사결정나무는 사람의 논리 구조와 비슷해서 설명하기(해석력)가 가장 좋습니다. 하지만 가지(Tree)를 너무 깊게 뻗으면(과적합, Overfitting) 오히려 예측력이 떨어지므로 가지치기(Pruning)가 필수입니다.</p>
                    <pre><code class="language-python">from sklearn.tree import DecisionTreeClassifier
# max_depth=3 으로 나뭇가지의 깊이를 제한하여 과적합을 방지!
tree_model = DecisionTreeClassifier(max_depth=3, random_state=42)
tree_model.fit(X_train, y_train)</code></pre>
                </div>
        """
    },
    {
        "filename": "week4_2_ensemble.html",
        "title": "Week 4-2: 앙상블과 부스팅",
        "subtitle": "집단 지성의 힘! 캐글 우승을 휩쓰는 현대 머신러닝의 핵심",
        "accent": "#8b5cf6", "accent_hover": "#7c3aed",
        "content": """
                <div class="card">
                    <h2>🌲 1. 배깅(Bagging): 랜덤 포레스트</h2>
                    <div class="metaphor">"의사결정나무 1그루는 오류를 범하기 쉽습니다. 하지만 나무 100그루를 심어서 숲(Forest)을 만들고, 100그루의 나무에게 투표(Voting)를 시키면 결과가 훨씬 정확해집니다!"</div>
                    <p>데이터를 무작위로 조금씩 다르게 뽑아서 여러 개의 나무를 만들고 결과를 합치는 방식입니다.</p>
                    <pre><code class="language-python">from sklearn.ensemble import RandomForestClassifier
# n_estimators=100 (나무 100그루를 심겠다)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)</code></pre>
                </div>

                <div class="card">
                    <h2>🚀 2. 부스팅(Boosting): XGBoost & LightGBM</h2>
                    <div class="metaphor">"랜덤 포레스트가 학생 100명이 각자 문제를 풀고 다수결을 하는 것이라면, 부스팅은 학생 1번이 틀린 문제를 학생 2번이 집중해서 풀고, 그걸 3번이 다시 보완하는 <strong>오답노트 릴레이</strong> 방식입니다."</div>
                    <p>현존하는 정형 데이터 분석 알고리즘 중 가장 빠르고 강력합니다. 시험과 실무에서 모델 성능을 극한으로 쥐어짜야 할 때 무조건 1순위로 사용됩니다.</p>
                    <pre><code class="language-python"># XGBoost는 scikit-learn과 사용법이 완벽하게 똑같습니다!
from xgboost import XGBClassifier

xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
xgb.fit(X_train, y_train)</code></pre>
                </div>
                
                <div class="card pro-tip">
                    <h2>💼 실무 노하우: 하이퍼파라미터 튜닝</h2>
                    <p>부스팅 모델들은 성능이 좋은 대신 설정할 변수(파라미터)가 너무 많습니다. 실무에서는 아래 두 가지만 기억하세요.</p>
                    <ul>
                        <li><code>n_estimators</code>: 나무의 개수 (보통 100~500)</li>
                        <li><code>learning_rate</code>: 학습률. 너무 크면 꼼꼼하지 못하고, 너무 작으면 시간이 오래 걸립니다. (보통 0.01 ~ 0.1 사이 사용)</li>
                    </ul>
                </div>
        """
    },
    {
        "filename": "week6_1_unsupervised.html",
        "title": "Week 6-1: 비지도학습 & 연관 분석",
        "subtitle": "정답 없는 데이터에서 숨겨진 보물(패턴) 찾기",
        "accent": "#10b981", "accent_hover": "#059669",
        "content": """
                <div class="card">
                    <h2>🧩 1. K-Means와 실루엣 스코어 (Silhouette Score)</h2>
                    <div class="metaphor">"K-Means로 나눈 조별 과제 그룹이 얼마나 똘똘 뭉쳐있는지(응집도), 다른 조원들과는 얼마나 멀리 떨어져 있는지(분리도)를 -1에서 1 사이의 점수로 평가합니다. 1에 가까울수록 완벽한 군집!"</div>
                    <pre><code class="language-python">from sklearn.metrics import silhouette_score

# kmeans 군집 결과에 대한 실루엣 점수 평가
score = silhouette_score(X_scaled, iris['cluster'])
print("실루엣 점수:", score)</code></pre>
                </div>

                <div class="card">
                    <h2>🌳 2. 계층적 군집화 (Hierarchical Clustering)</h2>
                    <div class="metaphor">"가장 가까운 두 명을 먼저 짝지어주고, 그 다음 가까운 사람을 붙여주면서 거대한 토너먼트 대진표(Dendrogram)를 그리는 방식입니다. K(군집 개수)를 미리 정하지 않아도 되는 장점이 있습니다."</div>
                </div>

                <div class="card drill-section">
                    <h2>🛒 3. 연관 분석 (Association Rule Mining, Apriori)</h2>
                    <div class="metaphor">"기저귀를 산 아빠들이 맥주도 같이 산다는 전설의 마케팅 분석법입니다! 'A를 사면 B도 산다'는 규칙을 찾아냅니다."</div>
                    <p>지지도(Support), 신뢰도(Confidence), 향상도(Lift)라는 3가지 지표를 이용해 규칙의 강도를 판단합니다. 특히 <strong>향상도(Lift)가 1보다 커야</strong> 진짜 의미 있는 연관성입니다.</p>
                </div>
        """
    },
    {
        "filename": "week6_2_adv_stats.html",
        "title": "Week 6-2: 고급 데이터 전처리 (ADP 대비)",
        "subtitle": "데이터 사이언티스트를 위한 궁극의 차원 관리 기법",
        "accent": "#f97316", "accent_hover": "#ea580c",
        "content": """
                <div class="card">
                    <h2>👯 1. 다중공선성 (VIF)</h2>
                    <div class="metaphor">"재판에 목격자가 2명 왔는데 둘이 똑같은 대본을 읽는 쌍둥이였습니다. 판사(모델)가 헷갈리지 않게 한 명을 집에 돌려보내는 작업입니다."</div>
                    <p>변수(X)들끼리 상관관계가 너무 높으면 회귀계수가 왜곡됩니다. VIF(Variance Inflation Factor) 값이 10을 넘으면 문제가 있다고 판단하고, 해당 변수를 제거하거나 릿지/라쏘 같은 규제 모델, 혹은 트리기반 모델(Random Forest)을 사용해야 합니다.</p>
                </div>

                <div class="card">
                    <h2>🗜️ 2. 차원 축소: 주성분 분석 (PCA)</h2>
                    <div class="metaphor">"3D 물체를 그림자로 비추면 2D가 됩니다. 특징(변수)이 100개나 되어서 모델이 힘들어할 때, 데이터의 정보(분산)를 최대한 보존하면서 변수를 2~3개의 '주성분(Principal Component)'으로 압축하는 마법입니다."</div>
                    <p>PCA를 수행하기 전에는 반드시 <strong>StandardScaler를 이용한 데이터 정규화</strong>가 필수입니다!</p>
                    <pre><code class="language-python">from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 1. 정규화 필수
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. 100개의 변수를 2개로 압축 (n_components=2)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)</code></pre>
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
        
print("4개의 HTML 파일 분할 생성 완료!")
