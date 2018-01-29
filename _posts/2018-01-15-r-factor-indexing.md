---
title:  "Indexing with Factors"
categories: 
  - DailyReport 
tag: 
  - R
  - Factor   
---

I spent a cycle figuring out, how R treats factors as an index.

# Major Lessons

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