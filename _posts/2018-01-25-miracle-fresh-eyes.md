---
title:  "The Miracle of Fresh Eyes"
categories: 
  - DailyReport 
tag: 
  - Small Ball Methods
---

I've been working on an interesting high dimensional statistics problem [^1] for which we needed to prove the usual Restricted Eigenvalue (RE) condition and stuck. 

# Major Lesson

In a nutshell, RE condition helps to prove non-asymptotic consistency of an estimator. Meaning that using the RE condition one can show that for a finite number of samples $$n$$ the estimation error of a parameter of interest is upper bounded by some number.[^2] 

There are a few methods for showing the RE condition among which [Mendelson's small ball method](https://arxiv.org/abs/1401.0304) is very popular. Describing the method needs another post (and actually is not necessary because Joel Tropp has already done a great job explaining it [here](https://arxiv.org/pdf/1405.1102.pdf).).

I just wanted to mention that after stalling over the problem for a while I completely stopped thinking about it and worked on other things for a few weeks and when I re-examined it today (after some context switch warm up) I looked through the problem and quickly saw the answer!

The main point that I want to share with other knowledge-workers out there is that living with a problem seems desirable and one feels that he makes progress by continually thinking and pursuing a solution but unfortunately, this is not true in many situations for abstract problems. You need to relax or switch to another task for a while and let your  __diffuse mode^[3]__ take over and find a solution in the back of your mind. Then when you come back to the tough problem, you can see with the fresh eyes and hopefully come up with a novel line of attack. 

[^3]: As Barbara Oakley named it in [LHTL](https://www.coursera.org/learn/learning-how-to-learn).
[^2]: We hope to have an upper bound as a decreasing function of the number of samples $$n$$.
[^1]: The paper is almost done, I'll advertise it after polishing it and uploading it on the arXiv. 