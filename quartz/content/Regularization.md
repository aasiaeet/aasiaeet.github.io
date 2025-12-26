---
title: Regularization
tags:
  - ml
  - statistics
  - optimization
---

Regularization adds constraints or penalties to prevent overfitting.

## Common Methods

### Ridge Regression (L2)

$$\hat{\beta} = \argmin_\beta \|y - X\beta\|_2^2 + \lambda\|\beta\|_2^2$$

### LASSO (L1)

$$\hat{\beta} = \argmin_\beta \|y - X\beta\|_2^2 + \lambda\|\beta\|_1$$

Produces **sparse** solutions - good for feature selection.

### Elastic Net

Combines L1 and L2:

$$\hat{\beta} = \argmin_\beta \|y - X\beta\|_2^2 + \lambda\left[\alpha\|\beta\|_1 + (1-\alpha)\|\beta\|_2^2\right]$$

Best for correlated features. See my blog post on [Elastic Net intuition](/blog/2018-01-22-elastic-net-intuition/).

## Connections

- Essential for [[High Dimensional Statistics]]
- Core technique in [[Machine Learning]]
