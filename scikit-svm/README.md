# Scikit Content Based SVM Regression
Scikit-regression approach. It first aggregates multi-value features, then it runs the svm regression.
Difects in this version: feature values are not normalized, e.g. value of job titles could be 15243,12324,53234 ..., it has been kept as it is,
multi-value features are aggregated by similarity between test instance and training instance.