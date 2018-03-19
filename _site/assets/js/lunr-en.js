var idx = lunr(function () {
  this.field('title')
  this.field('excerpt')
  this.field('categories')
  this.field('tags')
  this.ref('id')

  
  
    
    
      this.add({
          title: "Applied Machine Learning",
          excerpt: "test\n",
          categories: [],
          tags: [],
          id: 0
      })
      
    
      this.add({
          title: "Applied Machine Learning",
          excerpt: "\n",
          categories: [],
          tags: [],
          id: 1
      })
      
    
      this.add({
          title: "Course Calendar",
          excerpt: "You can find lecture dates, assignment out/due dates, project report deadlines, and exam dates in the following calendar. You can...",
          categories: [],
          tags: [],
          id: 2
      })
      
    
      this.add({
          title: "Applied Machine Learning",
          excerpt: "Welcome to applied machine learning, Fall 2018 course webpage!\n\n\n",
          categories: [],
          tags: [],
          id: 3
      })
      
    
      this.add({
          title: "This is 1st lecture.",
          excerpt: "Lecture 01 handout in PDF. In the morning Eat eggs Drink coffee In the evening Eat spaghetti Drink wine Conclusion...",
          categories: [],
          tags: [],
          id: 4
      })
      
    
      this.add({
          title: "This is lecture 2",
          excerpt: "In the second\n\n\n  Eat eggs\n  Drink coffee\n\n\nIn the evening\n\n\n  Eat spaghetti\n  Drink wine\n\n\nConclusion\n\n\n  And the answer is…\n  \n    \n  \n\n",
          categories: [],
          tags: [],
          id: 5
      })
      
    
      this.add({
          title: "Applied Machine Learning",
          excerpt: "\n",
          categories: [],
          tags: [],
          id: 6
      })
      
    
  
    
    
      this.add({
          title: "Indexing Data Frames in R",
          excerpt: "R provides many methods for indexing. Coming from other languages, it takes time to get comfortable with indexing in R....",
          categories: ["DailyReport"],
          tags: ["R","data.frame"],
          id: 7
      })
      
    
      this.add({
          title: "Merging Data Frames in R by Row Names",
          excerpt: "I was trying to read in different features for a cell line, e.g., mutations and expression from separate files and...",
          categories: ["DailyReport"],
          tags: ["R","data.frame"],
          id: 8
      })
      
    
      this.add({
          title: "Introducing Pandoc",
          excerpt: "I was trying to figure out a way to write math heavy blog posts where I found Pandoc. There are...",
          categories: ["DailyReport"],
          tags: ["Pandoc","MarkDown","KaTex"],
          id: 9
      })
      
    
      this.add({
          title: "Setting up KaTex for Jekyll",
          excerpt: "KaTex, the fastest library for displaying math on browsers, gradually increased its supported latex functions and is passing its rival...",
          categories: ["DailyReport"],
          tags: ["KaTex","Jekyll","MathJax","Pandoc"],
          id: 10
      })
      
    
      this.add({
          title: "Indexing with Factors",
          excerpt: "I spent a cycle figuring out, how R treats factors as an index. Major Lessons Any non-numeric thing that you...",
          categories: ["DailyReport"],
          tags: ["R","Factor"],
          id: 11
      })
      
    
      this.add({
          title: "The Curious Case of Ibrutinib-resistant CLL: Does Reverse-Mutations Exist? - Part I",
          excerpt: "The question is, can mutations vanish themselves? We discussed an applied example of CLL treatment with Ibrutinib. The following came...",
          categories: ["DailyReport"],
          tags: ["CLL","Cancer","Ibrutinib","Drug Resistance"],
          id: 12
      })
      
    
      this.add({
          title: "Introducing Jekyll-Scholar",
          excerpt: "Jekyll-Scholar is formatting references and citations on Jekyll blogs and “formats your bibliographies and reading lists for the web and...",
          categories: ["DailyReport"],
          tags: ["Jekyll","Plugin"],
          id: 13
      })
      
    
      this.add({
          title: "Gender Pay Gap, Why?",
          excerpt: "A reason for the gender pay gap and how to avoid it came up in our discussions with early career...",
          categories: ["DailyReport"],
          tags: ["Professional Development","Jordan B. Peterson"],
          id: 14
      })
      
    
      this.add({
          title: "Staticman vs. Disqus",
          excerpt: "On several rounds of effort, I tried to use Staticman as the comment manager service for this blog. I failed...",
          categories: ["DailyReport"],
          tags: ["Staticman","Disqus","Jekyll"],
          id: 15
      })
      
    
      this.add({
          title: "Elastic Net: An Intuitive Explanation",
          excerpt: "Elastic net is a proper tool when we have lots of correlated features in regression. Major Lessons In this scenario,...",
          categories: ["DailyReport"],
          tags: ["High Dimensional Statistics","Elastic Net"],
          id: 16
      })
      
    
      this.add({
          title: "The Miracle of Fresh Eyes",
          excerpt: "I’ve been working on an interesting high dimensional statistics problem 1 for which we needed to prove the usual Restricted...",
          categories: ["DailyReport"],
          tags: ["Small Ball Methods"],
          id: 17
      })
      
    
      this.add({
          title: "Switching to Trello",
          excerpt: "I recently gave the Trello another try and was impressed. I’m very interested in productivity apps. Every few month, I...",
          categories: ["DailyReport"],
          tags: ["Trello","Online Collaboration","Project Management","To-do List App"],
          id: 18
      })
      
    
  
});

console.log( jQuery.type(idx) );

var store = [
  
    
    
    
      
      {
        "title": "Applied Machine Learning",
        "url": "http://localhost:4000/courses/aml18/announcements",
        "excerpt": "test\n",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Applied Machine Learning",
        "url": "http://localhost:4000/courses/aml18/assignments",
        "excerpt": "\n",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Course Calendar",
        "url": "http://localhost:4000/courses/aml18/calendar",
        "excerpt": "You can find lecture dates, assignment out/due dates, project report deadlines, and exam dates in the following calendar. You can...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Applied Machine Learning",
        "url": "http://localhost:4000/courses/aml18/info",
        "excerpt": "Welcome to applied machine learning, Fall 2018 course webpage!\n\n\n",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "This is 1st lecture.",
        "url": "http://localhost:4000/courses/aml18/lec/md/lec01",
        "excerpt": "Lecture 01 handout in PDF. In the morning Eat eggs Drink coffee In the evening Eat spaghetti Drink wine Conclusion...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "This is lecture 2",
        "url": "http://localhost:4000/courses/aml18/lec/md/lec02",
        "excerpt": "In the second\n\n\n  Eat eggs\n  Drink coffee\n\n\nIn the evening\n\n\n  Eat spaghetti\n  Drink wine\n\n\nConclusion\n\n\n  And the answer is…\n  \n    \n  \n\n",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Applied Machine Learning",
        "url": "http://localhost:4000/courses/aml18/syllabus",
        "excerpt": "\n",
        "teaser":
          
            null
          
      },
    
  
    
    
    
      
      {
        "title": "Indexing Data Frames in R",
        "url": "http://localhost:4000/dailyreport/r-indexing/",
        "excerpt": "R provides many methods for indexing. Coming from other languages, it takes time to get comfortable with indexing in R....",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Merging Data Frames in R by Row Names",
        "url": "http://localhost:4000/dailyreport/r-merge/",
        "excerpt": "I was trying to read in different features for a cell line, e.g., mutations and expression from separate files and...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Introducing Pandoc",
        "url": "http://localhost:4000/dailyreport/pandoc/",
        "excerpt": "I was trying to figure out a way to write math heavy blog posts where I found Pandoc. There are...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Setting up KaTex for Jekyll",
        "url": "http://localhost:4000/dailyreport/KaTex-for-Jekyll/",
        "excerpt": "KaTex, the fastest library for displaying math on browsers, gradually increased its supported latex functions and is passing its rival...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Indexing with Factors",
        "url": "http://localhost:4000/dailyreport/r-factor-indexing/",
        "excerpt": "I spent a cycle figuring out, how R treats factors as an index. Major Lessons Any non-numeric thing that you...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "The Curious Case of Ibrutinib-resistant CLL: Does Reverse-Mutations Exist? - Part I",
        "url": "http://localhost:4000/dailyreport/cll-ibrutinib-resistence/",
        "excerpt": "The question is, can mutations vanish themselves? We discussed an applied example of CLL treatment with Ibrutinib. The following came...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Introducing Jekyll-Scholar",
        "url": "http://localhost:4000/dailyreport/jekyll-scholar/",
        "excerpt": "Jekyll-Scholar is formatting references and citations on Jekyll blogs and “formats your bibliographies and reading lists for the web and...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Gender Pay Gap, Why?",
        "url": "http://localhost:4000/dailyreport/gender-pay-gap/",
        "excerpt": "A reason for the gender pay gap and how to avoid it came up in our discussions with early career...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Staticman vs. Disqus",
        "url": "http://localhost:4000/dailyreport/staticman-vs-disqus/",
        "excerpt": "On several rounds of effort, I tried to use Staticman as the comment manager service for this blog. I failed...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Elastic Net: An Intuitive Explanation",
        "url": "http://localhost:4000/dailyreport/elastic-net-intuition/",
        "excerpt": "Elastic net is a proper tool when we have lots of correlated features in regression. Major Lessons In this scenario,...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "The Miracle of Fresh Eyes",
        "url": "http://localhost:4000/dailyreport/miracle-fresh-eyes/",
        "excerpt": "I’ve been working on an interesting high dimensional statistics problem 1 for which we needed to prove the usual Restricted...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Switching to Trello",
        "url": "http://localhost:4000/dailyreport/trello/",
        "excerpt": "I recently gave the Trello another try and was impressed. I’m very interested in productivity apps. Every few month, I...",
        "teaser":
          
            null
          
      }
    
  ]

$(document).ready(function() {
  $('input#search').on('keyup', function () {
    var resultdiv = $('#results');
    var query = $(this).val().toLowerCase().replace(":", "");
    var result =
      idx.query(function (q) {
        query.split(lunr.tokenizer.separator).forEach(function (term) {
          q.term(term, {  boost: 100 })
          if(query.lastIndexOf(" ") != query.length-1){
            q.term(term, {  usePipeline: false, wildcard: lunr.Query.wildcard.TRAILING, boost: 10 })
          }
          if (term != ""){
            q.term(term, {  usePipeline: false, editDistance: 1, boost: 1 })
          }
        })
      });
    resultdiv.empty();
    resultdiv.prepend('<p class="results__found">'+result.length+' Result(s) found</p>');
    for (var item in result) {
      var ref = result[item].ref;
      if(store[ref].teaser){
        var searchitem =
          '<div class="list__item">'+
            '<article class="archive__item" itemscope itemtype="http://schema.org/CreativeWork">'+
              '<h2 class="archive__item-title" itemprop="headline">'+
                '<a href="'+store[ref].url+'" rel="permalink">'+store[ref].title+'</a>'+
              '</h2>'+
              '<div class="archive__item-teaser">'+
                '<img src="'+store[ref].teaser+'" alt="">'+
              '</div>'+
              '<p class="archive__item-excerpt" itemprop="description">'+store[ref].excerpt+'</p>'+
            '</article>'+
          '</div>';
      }
      else{
    	  var searchitem =
          '<div class="list__item">'+
            '<article class="archive__item" itemscope itemtype="http://schema.org/CreativeWork">'+
              '<h2 class="archive__item-title" itemprop="headline">'+
                '<a href="'+store[ref].url+'" rel="permalink">'+store[ref].title+'</a>'+
              '</h2>'+
              '<p class="archive__item-excerpt" itemprop="description">'+store[ref].excerpt+'</p>'+
            '</article>'+
          '</div>';
      }
      resultdiv.append(searchitem);
    }
  });
});
