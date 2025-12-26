---
title: Machine Learning
tags:
  - ml
  - statistics
---

Machine learning is the study of algorithms that improve through experience.

## Core Concepts

### Supervised Learning

In supervised learning, we have labeled data $(x_i, y_i)$ and want to learn a function $f$ such that $f(x) \approx y$.

The goal is to minimize the expected loss:

$$\min_f \mathbb{E}_{(x,y)}[\ell(f(x), y)]$$

See also: [[Regularization]], [[High Dimensional Statistics]]

### Unsupervised Learning

No labels - we want to find structure in the data.

## Connections

- [[Causal Inference]] uses ML for effect estimation
- [[Bioinformatics]] applies ML to biological data
- [[Regularization]] is crucial for high-dimensional problems
