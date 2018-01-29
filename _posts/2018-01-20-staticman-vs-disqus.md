---
title:  "Staticman vs. Disqus"
categories: 
  - DailyReport 
tag: 
  - Staticman
  - Disqus
  - Jekyll 
---
On several rounds of effort, I tried to use Staticman as the comment manager service for this blog. I failed and finally gave up trying and fall back to Disqus. Here is why. 

The awesome theme that I'm using is [minimal mistakes](https://mmistakes.github.io/minimal-mistakes/) which supports many commenting platform like [Staticman](https://staticman.net/) and [Disqus](https://disqus.com/).

# Major Lessons 
I prefer Staticman over all other commenting tools because it keeps the user data where it belongs: on your GitHub repository. Disqus and similar services keep the comments on their servers and (I think for the exact reason) are filtered in some countries like Iran. 

The problem is that I'm using [non-supported Jekyll plugins]){{ site.baseurl }}{% post_url 2018-01-18-jekyll-scholar %}), I have delegated the deploy process to the [Netlify](https://www.netlify.com/) for the website links to work properly I needed to set the `url` in the `config.yml` to `https://aasiaeet.netlify.com`. 

I think this url setup is the main reason that Staticman is not working for me. By default it tries to commit to the `{url}\{GitHub username}\repository name` and having the Netlify as the url confuses it. 

In any event, for now, I gave up on Staticman and am content with Disqus. Maybe someday ...  
