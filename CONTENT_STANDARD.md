# Content Standard for ADP & Big Data Practical Prep

The app should not teach only "which function to call." Each topic must train exam reasoning: why a method is needed, when it is appropriate, what can go wrong, how to interpret the output, and how it appears in practical work.

## Required Structure for Every Core Topic

Each statistics or data mining topic should include:

1. Why it matters
2. When to use it
3. When not to use it
4. Required assumptions or preconditions
5. Step-by-step practical workflow
6. Python implementation pattern
7. Interpretation template for ADP written answers
8. Common mistakes
9. Practical business use cases
10. Mini drill and exam-style problem

## Statistics Topics to Expand

- Descriptive statistics and distribution shape
- Sampling, population, estimator, bias, variance
- Confidence interval
- Hypothesis test framework
- p-value, significance level, Type I/II error, power
- Normality test and why normality is not always mandatory
- Equal variance test
- One-sample t-test
- Paired t-test
- Independent two-sample t-test
- ANOVA and post-hoc tests
- Chi-square goodness-of-fit and independence tests
- Correlation: Pearson, Spearman, Kendall
- Simple and multiple linear regression
- Logistic regression interpretation
- Multicollinearity and VIF
- Nonparametric tests: Mann-Whitney U, Wilcoxon, Kruskal-Wallis
- Effect size and practical significance
- Residual analysis

## Data Mining Topics to Expand

- Full modeling workflow
- Train/test split and data leakage
- Preprocessing pipelines
- Encoding and scaling selection
- Feature engineering
- Feature selection
- Classification metrics: accuracy, precision, recall, F1, ROC-AUC, PR-AUC
- Regression metrics: MAE, MSE, RMSE, RMSLE, R2
- Logistic regression
- KNN
- Decision tree
- Random forest
- Gradient boosting and XGBoost
- SVM
- Naive Bayes
- Clustering: K-Means, hierarchical, DBSCAN
- Clustering validation: elbow, silhouette
- PCA
- Association rules: support, confidence, lift
- Imbalanced data handling
- Cross-validation
- Hyperparameter tuning
- Model interpretation and limitations

## ADP Written Answer Formula

For each analysis method, learners should practice writing:

```text
문제 상황상 [목표/데이터 특성]이므로 [방법]을 사용하였다.
해당 방법은 [핵심 가정/장점]이 있으며, 본 분석에서는 [전처리/검정/평가지표]를 통해 적합성을 확인하였다.
분석 결과 [수치/방향/유의성]이 나타났고, 이는 [현업 의미]로 해석된다.
다만 [한계/주의사항]이 있으므로 실제 적용 시 [보완 방법]이 필요하다.
```

## Big Data Practical Answer Formula

For each task, learners should practice:

```text
1. 데이터 로드
2. 문제 조건 확인
3. 결측치/이상치 처리
4. 필요한 컬럼만 선택
5. 조건 필터링 또는 모델링
6. 요구 형식으로 출력
7. 중간 결과 print로 검산
```

