---
title: Structured High Dimensional Data Sharing Model
---

\maketitle 
Consider the regression problem when we have a meaningful grouping in
the sample space. We want to exploit this knowledge and perform better
in the prediction and parameter estimation tasks. The (linear) data
sharing (DS) model considers the following relation between covariates
and the output: $$\begin{aligned}
        y_i = \mathbf{x}_i ({\beta}_0 + {\beta}_g) + \epsilon_i 
        \end{aligned}$$ where ${\beta}_0$ and ${\beta}_g$ are shared
(between all groups of samples) and the private (to group $g$)
parameters respectively. High dimensional structured data sharing model
considers the DS when the number of features is much larger than samples
and parameters have structure such as sparsity or group sparsity. We
consider the general form of data sharing where the structure of both
shared and private parameters can be characterized by any norm
$R(\cdot)$.
