---
title: Causal Inference
tags:
  - causality
  - statistics
---

Causal inference is the process of determining the independent, actual effect of a particular phenomenon.

## Key Concepts

### Potential Outcomes Framework

For each unit $i$, we have potential outcomes:
- $Y_i(1)$: outcome if treated
- $Y_i(0)$: outcome if not treated

The **Individual Treatment Effect** is:
$$\tau_i = Y_i(1) - Y_i(0)$$

The **Average Treatment Effect** is:
$$\text{ATE} = \mathbb{E}[Y(1) - Y(0)]$$

### Fundamental Problem of Causal Inference

We can never observe both $Y_i(1)$ and $Y_i(0)$ for the same unit!

## Methods

1. **Randomized Controlled Trials (RCTs)** - Gold standard
2. **Observational Studies** - Require assumptions
3. **Instrumental Variables**
4. **Regression Discontinuity**

## Connections

- [[Machine Learning]] methods can estimate heterogeneous treatment effects
- Important for [[Bioinformatics]] and drug discovery
