---
title:  "The Curious Case of Ibrutinib-resistant CLL: Does Reverse-Mutations Exist? - Part I"
comments: true 
categories: 
  - DailyReport 
tag: 
  - CLL
  - Cancer
  - Ibrutinib
  - Drug Resistance 
--- 
The question is, can mutations vanish themselves? We discussed an applied example of CLL treatment with Ibrutinib. 

The following came up during our lab meeting today with my great postdoc mentor Professor Kevin Coombes. I asked a dumb question like: can mutations reverse during the growth of the cancer tumor? The short answer is no, but instead of that, like always, he came up with an eloquent explanation with a contrived example. I don't want to repeat him (because those are not my words and therefore I can't claim that I understood the argument!), so the following with all of its shortcomings is my recall of his argument.

# Major Lessons

Assume a universe with only length one mutation where no deletion, insertion, etc. are possible. In other words, consider only missense/nonsense point mutations. Take the average length of a human gene to be roughly 50 kbp and assume 20000 genes exist. Therefore the probability of a mutation happening in a base pair is $$10^{-9}$$, and this mutation should escape every checkpoints and control mechanisms that prevent such a mutated cell to sustain and proliferate. For simplicity, we ignore the probability of a mutation "escaping through a mesh"[^1] of counter cancer measure. 

[^1]: [Gordon's theorem](https://dustingmixon.wordpress.com/2014/02/08/gordons-escape-through-a-mesh-theorem/) on a random subspace escaping through a subset of the hypersphere. 

So to reverse this mutation, we need a change in the exact same spot on the DNA, and we need to convert it to one of the, say, two neutral SNP allele. Such an event has the probability of $$\frac{1}{4} \times 10^{-18}$$ which is considered zero in most branches of science. 

Now the question is that why in we see some tumor sub-clones which does not have certain mutations. If the whole cancer definition is "accumulation of somatic mutation" and there is no going back after a mutation, then one would expect that all sub-clones have a similar core of mutation tree and only different leaves. 

Adding to my confusion, Kevin showed us a recent data from CLL patients treated with Ibrutinib[^2], a BTK inhibitor, and relapsed. The idea is to store blood samples without sequencing it, and when a patient relapsed go back and sequence the data to see if there is any meaningful predictor for the relapse before the actual detection of the mutation.  

[^2]: In 2013 Ibrutinib was introduced as a [targeted treatment](http://www.nejm.org/doi/full/10.1056/NEJMoa1215637) for relapsed/re-factored CLL patients harboring mutations in TP53 or deletion of 17p. [Two years later](http://www.nejm.org/doi/full/10.1056/NEJMoa1509388), it was suggested as an effective first line of attack for CLL. But as Kevin mentioned, I didn't check, the relapse (and/or drug resistant) rate after treatment is high when the patients pass the two years milestones, and ironically both studied followed up patients for about two years and missed this major issue. 

Looking at the history of mutation allele frequency of important genes (BTK and PLCG2), in some patients, we observe odd phenomena. We see a slow rise of those mutations over time and a sharp drop a few month before the actual relapse/resistant diagnosis. It seems PLCG2 mutation was reversing! 

So how should we explain this?!
