# ADP & Big Data Practical Study System Roadmap

## Current Assessment

This project is a lightweight local study web app for Korean data analysis practical exams. It currently has a strong beginner-friendly shape: a dashboard, weekly HTML lessons, small CSV datasets, and a right-side Python runner.

Strengths:
- The split lesson/code-runner layout is good for beginners because the feedback loop is short.
- The current sequence covers pandas, EDA, statistics, basic ML, ensemble models, unsupervised learning, VIF/PCA, and mock exams.
- Titanic, tips, and iris are enough for first contact with pandas, testing, and simple ML.
- The writing lowers anxiety, which matters when Python and statistics foundations are weak.

Critical gaps:
- Content is still tutorial-heavy. It needs more exam-style repetition, scoring rubrics, and "why this answer is acceptable" explanations.
- ADP requires written reasoning, model interpretation, limitations, and analysis choices. The current pages mostly show code answers.
- Big Data Analysis Engineer practice needs a stronger type-by-type drill bank: type 1 single-value output, type 2 submission CSV, type 3 statistical test.
- The app does not yet save progress, code attempts, wrong answers, or repeated weak topics.
- CSS and JavaScript are duplicated across pages, making future changes fragile.
- The data pool is too small for serious exam readiness.
- There is no package/environment checker, even though the official Big Data Analysis Engineer practice environment warns that available packages can differ by exam round.

## Fixes Already Started

- Restored the Python runner panel in `public/week5_mock_test.html`.
- Removed a broken JavaScript fragment in `public/week5_mock_test.html`.
- Added the missing `runPython()` implementation to `public/week4_ml.html`.
- Verified `week5_mock_test.html` in the browser by running `print('hello')` through the web runner.
- Added a statistics/data mining content standard in `CONTENT_STANDARD.md`.
- Added `public/stats_mining_deep_dive.html` as the first deep-dive content page.
- Expanded `public/week3_stats.html` with test-selection logic, assumptions, ADP interpretation templates, chi-square, correlation, nonparametric alternatives, and 8 drills.
- Expanded `public/week4_1_ml_basic.html` with modeling workflow, metric selection, data leakage warnings, KNN/logistic regression/decision tree usage guidance, ADP modeling answer templates, and 4 model-selection drills.
- Expanded `public/week4_2_ensemble.html` with bagging vs boosting guidance, random forest and XGBoost usage notes, hyperparameter tuning, feature-importance interpretation, ADP ensemble answer templates, and 4 ensemble drills.
- Expanded `public/week6_1_unsupervised.html` with unsupervised-learning use cases, K selection, clustering interpretation, association-rule metrics, ADP unsupervised answer templates, and 4 drills.
- Started the problem-bank structure with `problems/week6_1_unsupervised.json`.
- Added `scripts/check-problems.js` and connected it to `npm test` so page checks and problem-bank schema checks run together.
- Added problem-bank APIs in `server.js` and the first training UI in `public/problem_bank.html`.
- Connected the dashboard to the problem-bank training room.
- Added first-pass automatic grading in `public/problem_bank.html` for `numeric_tolerance`, `multiple_numeric_tolerance`, and `rubric_keywords` problem types.
- Added per-problem attempt stats in `public/problem_bank.html`, including run count, grade count, last pass/fail result, last activity time, and problem-list status tags.
- Added `problems/week3_stats.json` with 5 statistics problems covering Welch t-test, ANOVA, chi-square, Pearson correlation, and ADP interpretation writing.
- Added `problems/week4_1_ml_basic.json` with 4 machine-learning problems covering logistic regression, KNN with scaling, decision-tree overfitting, and ADP model interpretation writing.
- Added `problems/week4_2_ensemble.json` with 5 ensemble problems covering random forest, feature importance, overfitting comparison, XGBoost, and ADP ensemble interpretation writing.
- Added a dashboard problem-bank progress summary in `public/index.html`, showing total problems, attempted problems, passed problems, overall progress, and per-set progress.
- Expanded `public/week6_2_adv_stats.html` with VIF/PCA usage guidance, interpretation warnings, ADP answer templates, and VIF/PCA drills.
- Added `problems/week6_2_adv_stats.json` with 4 problems covering VIF, PCA explained variance, and ADP PCA interpretation writing.
- Added `problems/week5_mock_test.json` with 4 Big Data mock-test problems covering Type 1 preprocessing, Type 2 submission planning, and Type 3 one-sample t-test.
- Added CSV submission grading for Type 2 problems: the runner now collects generated CSV files, summarizes columns/row counts/null counts/numeric ranges, and `public/problem_bank.html` grades `csv_submission` expectations.
- Strengthened CSV submission grading with unique-count, first/last value, strict-increasing ID, and minimum-distinct prediction checks so constant-probability or misordered submissions fail.
- Added per-problem timer controls in `public/problem_bank.html` so learners can start, pause, reset, and resume timed attempts using each problem's `timeLimitMinutes`.
- Improved tablet study UX in `public/problem_bank.html` with a collapsible problem list, sticky action buttons, larger touch targets, a code-editor jump button, and collapsible rubric/mistake sections.
- Added `public/python_pandas_foundation.html` and `problems/python_pandas_foundation.json` with 6 foundation drills for paths, row counts, missing values, filtering, aggregation, and feature engineering.
- Added `public/pandas_preprocessing_patterns.html` and `problems/pandas_preprocessing_patterns.json` with 8 drills for sorting, multi-condition filtering, value counts, crosstab, groupby, and ratio features.
- Added `public/statistics_foundation.html` and `problems/statistics_foundation.json` with 7 drills for test selection, p-value interpretation, t-tests, ANOVA, chi-square, correlation, and Levene equal-variance checks.
- Added `public/ml_mining_foundation.html` and `problems/ml_mining_foundation.json` with 6 drills for model choice, logistic regression, KNN scaling, decision-tree overfitting, random forest ROC-AUC, and ADP-style ML interpretation.
- Added `data/customer_churn.csv`, `public/customer_churn_practice.html`, and `problems/customer_churn_practice.json` with 7 churn EDA and business-interpretation drills to reduce reliance on Titanic/Tips/Iris.
- Added weak-topic diagnosis and next-problem recommendations to `public/index.html` based on problem-bank attempt stats stored in local storage.
- Added problem-bank deep links so dashboard recommendations open the exact target problem via `problem_bank.html?set=...&problem=...`.
- Added retry guidance to `public/problem_bank.html` so failed grading results show likely failure points, common mistakes, and rubric reminders.
- Added final review mode to `public/problem_bank.html`, hiding answer conditions before grading and starting study aids collapsed for exam-like attempts.
- Added `public/environment_check.html` to verify Python package imports, versions, data paths, and a small sklearn model fit before studying or exam practice.
- Added `public/final_study_guide.html` with daily study routine, 7-day/3-day/exam-day checklists, and final operating guidance.

## High-Priority Upgrade Plan

### Phase 1: Make the App Reliable

Goal: every linked page must load cleanly and the runner must work everywhere.

Tasks:
- Add a basic page health-check script that verifies each HTML page has no obvious missing runner pieces.
- Consolidate duplicated runner JavaScript into one shared file.
- Consolidate common layout CSS into one shared file.
- Add mobile/tablet responsive layout so the right-side runner does not crush the content.
- Add a tablet study mode with larger touch targets, collapsible problem lists, comfortable code editor height, landscape/portrait checks, and reduced scrolling during code execution.
- Improve server error messages for missing Python, timeout, syntax error, and missing packages.

### Phase 2: Build the Exam Drill Engine

Goal: move from "read and reveal" to "attempt, check, retry".

Tasks:
- Add a problem metadata format, such as JSON files under `problems/`.
- Store problem type, dataset, required output, hint, reference solution, scoring rubric, and common mistakes.
- Add an answer checker for:
  - exact numeric outputs,
  - tolerance-based numeric outputs,
  - generated CSV column and row checks,
  - required interpretation keywords for ADP-style written answers.
- Add timers by exam type:
  - Big Data Analysis Engineer: 180-minute full mock plus short drills.
  - ADP: longer analysis sections with written interpretation checkpoints.
- Save attempts and wrong-answer history in local storage first.

### Phase 3: Strengthen Learning Content

Goal: cover weak foundations without becoming a passive textbook.

Modules to add:
- Python basics for exam coding: variables, lists, functions, imports, paths, print formatting, errors.
- Pandas patterns: filtering, sorting, grouping, missing values, datetime, string handling, merge, pivot.
- Statistics decision tree: which test to choose and why.
- Statistical assumptions: normality, equality of variance, independence, nonparametric alternatives.
- Big Data type 1 templates: quantile, outlier, groupby, datetime, conditional filtering.
- Big Data type 2 templates: train/test alignment, leakage prevention, encoding, scaling, metric selection, CSV output.
- Big Data type 3 templates: t-test, paired t-test, ANOVA, chi-square, correlation, regression result interpretation.
- ADP templates: EDA narrative, preprocessing justification, model comparison, hyperparameter tuning, residual/error analysis, limitation writing.

### Phase 4: Expand Data and Mock Exams

Goal: reduce memorization from three familiar datasets.

Datasets to add:
- House price or apartment-style regression data.
- Customer churn classification data.
- Credit/loan default imbalanced classification data.
- Marketing campaign or purchase behavior data.
- Time-series sales or traffic data.
- Synthetic dirty datasets with missing values, outliers, mixed types, and leakage traps.

Mock exam bank:
- Big Data Analysis Engineer: at least 10 full sets.
- ADP: at least 6 full sets with scoring rubrics and model written answers.
- Short daily drills: 5-15 minute drills for pandas, stats, and model metrics.

### Phase 5: Personal Coach Layer

Goal: the app should tell the learner what to do next.

Features:
- Dashboard progress by topic and exam type.
- Weak-topic diagnosis from failed attempts.
- Daily study queue.
- "I don't know why" explanations for common errors.
- Cheat-sheet builder: the app collects patterns the learner repeatedly missed.
- Final review mode that hides all answers and blocks hints until after a timed attempt.

## Content Quality Standard

Every serious problem should have:
- Question statement.
- Dataset path.
- Expected output form.
- Time limit.
- One small hint.
- Reference solution.
- Common mistakes.
- Scoring rubric.
- For ADP, a written answer template and a high-scoring sample interpretation.

## Useful Source Links

- Big Data Analysis Engineer official practice environment: https://dataq.goorm.io/exam/3/%EC%B2%B4%ED%97%98%ED%95%98%EA%B8%B0/quiz/1
- Data qualification official site: https://www.dataq.or.kr/www/main.do
