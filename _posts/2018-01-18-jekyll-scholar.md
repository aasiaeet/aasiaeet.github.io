---
title:  "Introducing Jekyll-Scholar"
categories: 
  - DailyReport 
tag: 
  - Jekyll
  - Plugin   
---

[Jekyll-Scholar](https://github.com/inukshuk/jekyll-scholar) is formatting references and citations on Jekyll blogs and "formats your bibliographies and reading lists for the web and gives your blog posts citation super-powers." 

# Major Lessons
Publication page is necessary for an academic website. Since I'm very lazy, I always wanted to be able to have a single `.bib` file and a **system** which generates a webpage from it. Such a pipeline will make it much easier to maintain the website[^1]. 

Jekyll-Scholar is a great plugin for this purpose. I spent sometime during the holidays to customize and integrate it to this website. Here, I some challenges that I needed to overcome. 

## Using a Non-supported Plugin on GitHub
GitHub is very stringent about the plugins that supported on the GitHub-Pages. 
[Here](https://pages.github.com/versions/) is the small set of supported plugins which does not include Jekyll-Scholar.

So to use Jekyll-Scholar you need a third party service, which allows other plugins, to serve your website and deploy it to your `_site` folder on the master/Github-pages branch of your repository. 

It seems [Netlify](https://www.netlify.com/) is the most popular and user-friendly tool for **Continuous Deployment** out there and comparing my experience with [Wercker](http://www.wercker.com/), I can confirm that. 

It is very easy to link your GitHub repository to Netlify and deploy your website with arbitrary plugins. You can refer to the [step-by-step](https://www.netlify.com/blog/2016/09/29/a-step-by-step-guide-deploying-on-netlify/) guide on the Netlify website. 

## Sorting Publication by Year and Topic
After looking around for options, I found that I either should learn and write some Ruby code for this or I can use Jekyll-Scholar ability to work with multiple `.bib` files and hack through it. 

I didn't want to spend time learning Ruby, so I ended up copy/pasting BibTex entries to separate files, one for each topic, and read them in inside the `By Topic` page:
```html
{% raw %}
<!-- High Dimensional Statistics -->
<h3  class="pubyear">High Dimensional Statistics</h3>
{% bibliography -f hds %}

<!-- Social Network Analysis --> 
<h3  class="pubyear">Social Network Analysis</h3>
{% bibliography -f sna %}
{% endraw %}
```
Sorting by year is simpler because it needs only a single file. I'm borrowing the code partially from [al-folio](https://github.com/alshedivat/al-folio/blob/master/_pages/publications.md) theme:
```html
{% raw %}
{% for y in page.years %}
  <h3  id="{{y}}" class="pubyear">{{y}}</h3>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}
{% endraw %}
```
And you should put `years: [2016, 2015, 2013, 2012]` in the front matter of the related page. 

## Adding Abstract, BibTex, PDF Buttons for each Item
Inside the `_layouts` folder I added the following `bibtemplate.html` file:
```html
{% raw %}
---
---
{{reference}}
    {% if entry.abstract %}
    <button class="btn btnId btnPub--abstract" id="b_{{key}}-abstract" style="outline:none;">Abstract</button>
    {% endif %}

    <button class="btn btnId btnPub--BibTex" id="b_{{key}}-bibtex" style="outline:none;">BibTeX</button>
    
    {% if link %}
    <a href="{{link}}"><button class="btn btnId btnPub--download" style="outline:none; position:relative;white-space: normal;">PDF</button></a>
    {% endif %}
    
    {% if links['sup.pdf'] %}
    <a href="{{links['sup.pdf']}}"><button class="btn btnId btnPub--supplement" style="outline:none; position:relative;white-space: normal;">Supplement</button></a>
    {% endif %}

    <div class="dropDownBibtex" id="{{key}}-bibtex">
    <pre>{{entry.bibtex}}</pre>
    </div>
    
    <div class="dropDownAbstract" id="{{key}}-abstract">
    {{entry.abstract}}
    </div>
{% endraw %}
```
And set the Jekyll-Scholar configuration in `_config.yml` file to work with this layout:
```yml 
  bibliography_template: bibtemplate 
```
I'll explain different parts of the above file in the following sections. 

### Drop Down Abstract and BibTeX
I wanted to have a drop-down effect for some of the buttons. The mainstream method is to use [Twitter's Bootstrap](http://getbootstrap.com/2.3.2/), but the problem is that I'm using a Jekyll theme which is not supporting the Bootstrap and adding it to the theme just for these two buttons was inefficient. 

So I just added the following simple jQuery script in the footer template of the website:
```html
{% raw %}
<script>
$(document).ready(function(){
    var str =$(this).attr('id');
    
    $(".btnId").click(function(){
        var str = $(this).attr('id');
        var ret = str.split("_");
        var id = ret[1];
        $('#' + id).toggle();
    });
});
</script>
{% endraw %}
```

### Providing PDF Download Link 
Jekyll-Scholar can read PDF files from a specific directly fixed in the `_config.yml`:
```yml 
  repository: /publications
``` 
The `publications` directory should be in the root of your repository. 
Inside of it, you can add files that have the BibTeX keys as their names.
So `pubName.pdf` corresponds to a BibTeX entry with the name `pubName` which is accessible through `{% raw %}{{ key }}{% endraw %}` in the `bibtemplate.html`.

### Supplement Files
If you want to include supplement, presentation, etc. to your publication entry, you can have your extra file in the `publications` folder as `key.sup.pdf` which is read into `links['sup.pdf']`. 

[^1]: This is the general philosophy of Jekyll as a static website/blog generator: separating the content from the generation process. 