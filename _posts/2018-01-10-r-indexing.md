---
title:  "Indexing Data Frames in R"
categories: 
  - DailyReport 
tag: 
  - R
  - data.frame 
---

R provides many methods for indexing. Coming from other languages, it takes time to get comfortable with indexing in R. 

# Major Lessons

## What is a Data Frame? 
Compared to intellectual math challenges, technological issues are very mind scratching for me. After understanding/solving a math problem I feel great, but it is entirely different when I find a bug in my code, I feel dumb. I mean, you can spend a lot of time to be able to do a simple thing, or you may waste a day finding a small bug in your program. And that is the time when I have the most mixed feeling: happy about the achievement and very very angry that my day is gone to fix a single piece. 

Recently, I started to learn R, the programming language for statisticians. Unlike other programming languages that I coded in, R has several ways of representing and indexing the abstract object that I call *table*. A table can be **matrix** construct or **data.frame** is R. Data frames are more flexible and are the main point of working with R. You can easily have different data types like factor, numeric, characters in a data frame, and index them with column and row names or numeric indices. 

It seems that data frame is implemented as a particular **list of lists** object. The actual list has a list of columns where each column is a list itself. The only constraint is that the columns should have the same length. 
This fact became clear when I did this:
```R
> d <- data.frame()
> class(d)
[1] "data.frame"
> mode(d)
[1] "list"
```
So at first, I found it less confusing to index the data frame as a list of lists using the regular single and double bracket. 
For the ith column as a list (data.frame) one can do `d[i]`, while to view it as the actual type of elements, say numeric, we can do `d[[i]]` and then proceed with the row indexing by `d[[i]][j]`, noting that `d[i][j]` is wrong and `d[[i]][[j]]` is correct but not efficient.  
After spending another round cleaning up the code, I got it to the more traditional form of indexing `d[i,j]` without any problem. 


# Minor Lessons

## Spell Checker Plugin for Notepad++ 

I started to write most of my notes in Notepad++. The auto-complete feature is very convenient, but there is no spell checking by default. I had to install it as a plugin. You can download plugins from [here](http://docs.notepad-plus-plus.org/index.php/Plugin_Central) and put it in the `C:\Program Files\Notepad++\plugins` folder and then import it from the `Setting`. I needed to find x64 compatible because the x32 ones didn't work. I finally ended up using [DSpellCheck](https://github.com/Predelnik/DSpellCheck/releases/tag/1.2.14.2). 

## String Concatenation in R

`paste("str1", ...)` does the job but the default separator is space to have actual concatenation you need `sep=""` argument. 


## Data frames with matrix operations
Interestingly, some matrix operations like transpose accept data frame but spit out `matrix` class (Again I think the matrix class is implemented as an array `c()` with two dimensions. So, the  `class(A)` is `matrix` but the `mode(A)` is the mode of constituent elements of the corresponding vector. 


