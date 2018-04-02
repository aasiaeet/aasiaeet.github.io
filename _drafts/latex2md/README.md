---
author: Amir Asiaee T.
title: Latex to Markdown Instruction
date: 2018-01-11
---
# Steps 
This folder is used to generate Markdown files from Latex files using Pandoc. 
The Markdown files are usually the math-heavy README.md files which need to be typeset in Latex. 

Here are the steps:
1. Write your text in a .tex file. 
2. If you are using Github you should use the following command and you are done:

    ```
    pandoc -s source.tex --katex -o output.md -t gfm
    ```
3. If you are using Gitlab: Pandoc is not supporting Gitlab Flavored Markdown. So, we need another extra step after the following:

    ```
    pandoc -s source.tex --katex -o output.md
    ```
4. Go to the md file and replace the `$...$` with ```$`...`$``` and

    ```
    $$
    ...
    $$ 
    ```
    
    blocks with 
    
        ```math 
        ... 
        ```
