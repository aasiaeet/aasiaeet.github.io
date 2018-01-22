---
title:  "The curious case of Ibrutinib-resistant CLL: Does Reverse-Mutations Exist?"
categories: 
  - DailyReport 
tag: 
  - CLL
  - cancer
comments: true 
--- 


This came up during our lab meeting today with my great postdoc mentor Professor Kevin Coombes. 
<!--more-->

I asked a dumb question like: can mutations reverse during the growth of the cancer tumor? 
The short answer is no, but instead of that, like always, he came up with an eloquent explanation which involved a contrived example. 
I don't want to repeat him (because those are not my words and therefore I can't claim that I understood the argument!), so the following with all of its shortcomings is my recall of his argument.

# Major Lessons

Consider the regression problem when we have a meaningful grouping in
the sample space. We want to exploit this knowledge and perform better
in the prediction and parameter estimation tasks. The (linear) data
sharing (DS) model considers the following relation between covariates
and the output: 

$$\begin{aligned}
	y_i = \mathbf{x}_i ({\beta}_0 + {\beta}_g) + \epsilon_i 
\end{aligned}$$ 

where $${\beta}_0$$ and $${\beta}_g$$ are shared
(between all groups of samples) and the private (to group $g$)
parameters respectively. High dimensional structured data sharing model
considers the DS when the number of features is much larger than samples
and parameters have structure such as sparsity or group sparsity. We
consider the general form of data sharing where the structure of both
shared and private parameters can be characterized by any norm
$$R(\cdot)$$.

$$\begin{aligned}
	y_i &= \mathbf{x}_i ({\beta}_0 + {\beta}_g) + \epsilon_i 
	\\ 
	&\leq 2
\end{aligned}$$ 

> test this 

Assume a universe with only length one mutation where no deletion, insertion, etc. are possible. In other words, consider only missense/nonsense point mutations. Take the average length of a human gene roughly as 50 kbp and assume 20000 gene exist. Therefore the probability of a mutation happening is    and \[10^{-9}\], and this mutation should provide the cell with a selective advantage which makes it cancerous. 

$$
\begin{aligned}
g^2 &= 10^{-9} 
\\  
&\geq \int_{0}^\infty
\end{aligned}
$$


So to reverse this mutation we need a change in the exact same spot on the DNA and we need to convert it to one of the, say, two neutral SNP allele. This event has the probability of $$\frac{1}{4} \times 10^{-18}$$ which is considered zero in most branches of science. 

Now the question is that why in we see some 


Any non-numeric thing that you read from a data file is going to be a factor, i.e., categorical data. 
{: .notice--warning} 

Factors are implemented as numerics/integers in R. So when you use them to index another construct which has row/column name as character you need to do so by `as.character()`.
{: .notice--danger}

Here is a typical scenario: You read a column from a file and use it to index some construct. 
You either should read the column as string:
```R
myDataFrame <- read.csv("path/to/file.csv", stringsAsFactors=FALSE)
```
or convert the factors using as.character before indexing another construct:
```R
a <- myDataFrame2[as.character(myFactor)]
```