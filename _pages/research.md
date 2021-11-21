---
layout: single 
permalink: /research/
author_profile: true
title: Research Projects
---
Here is the list of ongoing projects of AA Lab:
    ## Whole Transcriptome Prediction
        - Transcriptome or gene expression profile captures the activity of all genes in a sample at once. One can hope to represent the state of a sample (cell) with its transcriptome (~20k genes). Although measuring gene expression using RNA-Seq is much cheaper than a decade ago, scaling it to millions of samples is expensive.
        - One recent idea is to measure a few key predictive genes (e.g., 1k genes) and predict the rest of the transcriptome (~19k genes) from that subset. These genes should be robust predictors across various environments. By environment, we broadly mean different cell states such as healthy/diseased, tissue-types, treated with various drugs, etc.
        - This project aims to design methods to select the most predictive genes and algorithms that improve the prediction performance across environments.
    ##  Combining RCT with Observational Studies
        - The gold standard data for causal effect estimation comes from Randomized Control Trial (RCT), which is hard to run and limited in scope. On the other hand, observational studies are easier to conduct, but causal effect estimation using such data needs some untestable assumptions.
        - An emerging body of literature suggests combining the two types of data to improve causal effect estimation. The goal of this project is to borrow ideas from transfer learning to design a more efficient causal effect estimator by merging RCT and observational data.
        - The merge of RCT and OD is challenging due to several issues. First, the covariates measured in the two studies are not usually the same (e.g., age is present in one and absent in the other data set). More importantly, the joint distribution of covariates, treatment, and potential outcomes in OD and RCT populations are different.
    ## Understanding Zero Inflation Phenomena in Biological Data
        - Bulk micro-RNA and single-cell gene expression data contain lots of zeros. Previously, it was believed that these zeros are technological artifacts. But we hypothesize that they are biologically relevant and are associated with the environment, e.g., the cell type in scRNA-seq and tissue type in microRNA.
        - To provide evidence of the importance of zero expression values, we explore multiple methods. We have been developing a Bayesian method to quantify the probability of zeros coming from a categorical
variable (such as the tissue type). Moreover, we want to explore the ability of present/absent binary data to predict (classify) the samples into categories. Gene enrichment analysis of co-unexpressed values is another avenue that we will explore.  
    ## Multi-Task Learning for Drug Response Prediction
        - It takes a lot of time and resources for a drug to get FDA approval. The rate of approval is very low, and many new drugs fail in various study phases.  Drug-repurposing suggests reusing the approved drugs for alternative diseases to avoid drug development challenges.
        - To generalize the drug response, we need to characterize the biomarkers associated with the efficacy of the treatment in samples. This problem is a high-dimensional inference problem because many features of samples (gene expression profile, mutation, etc.) are measured while a few samples are usually available, e.g., in Cancer Cell Line Encyclopedia (CCLE).
    ## Statistical Software/App Development for Combination Drug Screening
        - Drug screening aims to find combinations of two or more drugs for a disease to be less toxic and more effective than each one. Finding the best combination is a combinatorial problem, and we need to design experiments carefully to find promising combinations out of thousands of possible ones. We have been developing a pipeline for statistical analysis of data generated from these experiments and new models for capturing drug synergy. The pipeline consists of various outlier removal, batch effect correction, and regression methods.
        - This project aims to take the existing pipeline to a new level by making it into a reusable R package and potentially a user-friendly web application.
    ## Structural Equation Models for Cancer Progression Inference 
        - Cancer is defined as a disease caused by the accumulation of mutations/alterations. Inferring the order of mutations during tumorigenesis is of biological and clinical interest. A favorite class of models for order of events is based on Bayesian Networks, which are DAGs equipped with probabilities. But BNs are incapable of modeling some properties of cancer progression, such as mutual exclusivity of event subsets.
        - The goal of this project is to infer cancer progression networks from cross-sectional mutation allele frequency data using structural equation models. SEMs are flexible enough to capture complex progression trajectories, and the goal is to learn them from mutation allele frequency data.

