# ADP & Big Data Practical Study App

Local study web app for ADP and Big Data Analysis Engineer practical exam practice.

## Start

```powershell
npm install
python -m pip install -r requirements.txt
npm start
```

Open:

```text
http://localhost:9001
```

Problem bank:

```text
http://localhost:9001/problem_bank.html
```

The problem bank currently supports:
- answer/code saving in browser local storage
- Python code execution
- automatic grading for numeric tolerance, multiple numeric tolerance, keyword-rubric, and CSV submission problems
- retry guidance after grading, including failed checks, common mistakes, and rubric reminders
- stricter CSV checks for row count, exact columns, nulls, numeric ranges, unique IDs, ID order, and non-constant probability submissions
- per-problem attempt stats for run count, grade count, last result, and last activity time
- per-problem timers with start, pause, reset, and resume behavior based on each problem's time limit
- final review mode that hides answer conditions before grading and starts study aids collapsed
- tablet-friendly problem-bank controls with collapsible problem lists, larger touch targets, sticky action buttons, and a shortcut to the code editor
- dashboard progress summary for total, attempted, passed, per-set progress, weak topics, and deep-linked next recommended problems
- environment check page for Python package imports, versions, data paths, and a tiny sklearn model fit
- final study guide with daily routine and exam countdown checklists

Current problem sets:
- Foundation: Python/Pandas basics
- Pandas preprocessing and EDA patterns
- Statistics foundation and p-value interpretation
- Data mining and machine-learning foundation
- Customer churn dataset practice
- Week 3: statistics and hypothesis testing
- Week 4-1: basic single-model machine learning
- Week 4-2: ensemble and boosting
- Week 5: Big Data Analysis Engineer mock test
- Week 6-1: unsupervised learning and association analysis
- Week 6-2: advanced preprocessing with VIF and PCA

## Check

```powershell
npm test
```

The page health check verifies that HTML pages with a Python runner have the editor, run button, console, and runnable JavaScript.
The problem-bank check verifies required JSON fields for problem sets under `problems/`.

## Python Runner

The browser sends Python code to the local Express server. Example:

```python
import pandas as pd

df = pd.read_csv('data/titanic.csv')
print(df.head())
```
