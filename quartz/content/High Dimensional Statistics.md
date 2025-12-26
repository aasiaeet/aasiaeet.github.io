---
title: High Dimensional Statistics
tags:
  - statistics
  - theory
---

When $p \gg n$ (more features than samples), classical statistics breaks down.

## The Problem

In high dimensions:
- OLS doesn't have a unique solution
- Sample covariance is singular
- Curse of dimensionality

## Key Assumptions

### Sparsity

Assume only $s \ll p$ coefficients are non-zero:

$$\|\beta^*\|_0 = s$$

### Restricted Eigenvalue Condition

The design matrix $X$ satisfies:

$$\frac{\|X\delta\|_2^2}{n} \geq \kappa \|\delta\|_2^2 - \tau \|\delta\|_1^2$$

for some $\kappa > 0$.

## Main Results

LASSO achieves near-optimal rate:

$$\|\hat{\beta} - \beta^*\|_2 = O\left(\sqrt{\frac{s \log p}{n}}\right)$$

## Connections

- [[Regularization]] is the key tool
- Applications in [[Bioinformatics]] and [[Machine Learning]]
