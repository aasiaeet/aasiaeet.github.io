---
title:  "Hyper-parameter Tuning, Cross-validation, and Bootstrp"
categories: 
  - DailyReport 
tag: 
  - Bootstrap
  - Linear Regression
---

I was looking at Cancer Cell Line Encyclopedia ((CCLE)[https://portals.broadinstitute.org/ccle]). I was trying to understand the regression method that they used for analyzing the cancer data in their well-known 2012 (paper)[https://www.nature.com/articles/nature11003].

The method itself is the celebrated elastic net of (Zou-Hastie)[https://web.stanford.edu/~hastie/Papers/B67.2%20(2005)%20301-320%20Zou%20&%20Hastie.pdf], but I was interested to understand all of the surrounding statitical jargon in the method part of the CCLE paper. Specifically, hyperparameter tuning and bootstrap procedure. 