---
title:  "Setting up KaTex for Jekyll"
categories: 
  - DailyReport 
tag: 
  - KaTex
  - Jekyll
  - MathJax
  - Pandoc 
---

KaTex, the fastest library for displaying math on browsers, gradually increased its supported latex functions and is passing its rival MathJax. 

I was reassured about this when saw the great [Erik Demaine's](http://erikdemaine.org/) active involvement in KaTex's GitHub community. So I started to set it up for this blog. 

If you want to write a few latex math, it is easy to find a way to do it with available resources. For example, if you use KramDown like me, you can choose the MathJax engine and put whatever you want inside a double-dollar sign, and that is about it. But if you may have a math-heavy posts, you should probably go with the KaTex which is not supported in KramDown, and even if you find a way (mentioned below) around it you won't be able to use your LaTex macro library which will eventually wast your time. 
 
Therefore for a possible math-heavy posts, you should think about an efficient pipeline. There is a [suggestion](http://shuvomoy.github.io/blog/non-technical/2016/01/16/Writing-math-heavy-blogs.html) of using Pandoc to generate HTML from your LaTex source for a Jekyll blog. I'm not satisfied with this solution because I may end up looking at the destination file and modifying things, e.g., adding images [^1], and I want to use MarkDown for that. 

[^1]: I'm not sure how Pandoc handles images, and I don't want to leave it to Pandoc to decide those formatting decisions when I have a theme and customized CSS style for each element. 

Another idea was to use Pandoc and convert the LaTex file to MarkDown. Here the problem was two-fold. First, my website MarkDown (`KramDown`) only supports MathJax engine. Secondly, the output MarkDown of Pandoc (known as GitHub Flavored MarkDown) has a single-dollar sign reserved for the in-line math and double ones for equations which is problematic for the KaTex engine.

Considering these difficulties and lack of time, I ended up hacking through the obstacles and developed my own "heavy math blogging" pipeline. :

First set the KramDown to work with MathJax engine: 
```yml
markdown: kramdown
kramdown:
  math_engine: mathjax
```

Then you need to put the following code in the footer of your website to convert MathJax scripts to KaTex:
```html 
<!-- Changing MathJax to KaTex -->
<script>
  $("script[type='math/tex']").replaceWith(function() {
      var tex = $(this).text();
      return katex.renderToString(tex.replace(/%.*/g, ''), {displayMode: false});
  });

  $("script[type='math/tex; mode=display']").replaceWith(function() {
      var tex = $(this).html();
      return katex.renderToString(tex.replace(/%.*/g, ''), {displayMode: true});
  });
</script>
```
Now for each math heavy posts you should do the followings: 
1) User your dear LaTex macro file and write your post in TexStudio (or any other editor for that matter). 
2) Use Pandoc to generate a GFM MarkDown file. 
3) Use Notepad++ to record a macro for doing the following:
  i. Replace `$` with `$$`
  ii. Replace `$$$$` with `$$`
4) Modify the resulted `.md` file as needed and publish it. 

When you publish the post, the MathJax scripts will be generated in your HTML file which are replaced with KaTex scripts and the final file gets ready.   




