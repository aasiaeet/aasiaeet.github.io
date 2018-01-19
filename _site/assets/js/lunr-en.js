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
          title: "Applied Machine Learning",
          excerpt: "Lecture slides\n\n\n  \n    \n      Lecture Number\n      Notes\n      PDF\n      Content\n    \n  \n  \n    \n      1\n      00/00/00\n      00/00/00\n      Introduction and Logistic\n    \n  \n\n\n",
          categories: [],
          tags: [],
          id: 2
      })
      
    
      this.add({
          title: "Applied Machine Learning",
          excerpt: "\n",
          categories: [],
          tags: [],
          id: 3
      })
      
    
      this.add({
          title: "Applied Machine Learning",
          excerpt: "\n",
          categories: [],
          tags: [],
          id: 4
      })
      
    
      this.add({
          title: "Introduction and Logistics",
          excerpt: "In the morning Eat eggs Drink coffee In the evening Eat spaghetti Drink wine Conclusion And the answer is… $f(x)=\\sum_{n=0}^\\infty\\frac{f^{(n)}(a)}{n!}(x-a)^n$...",
          categories: [],
          tags: [],
          id: 5
      })
      
    
      this.add({
          title: "Theoretical Machine Learning",
          excerpt: "Minimal Mistakes has been developed as a Jekyll theme gem for easier use. It is also 100% compatible with GitHub...",
          categories: [],
          tags: [],
          id: 6
      })
      
    
      this.add({
          title: "Theoretical Machine Learning",
          excerpt: "Minimal Mistakes has been developed as a Jekyll theme gem for easier use. It is also 100% compatible with GitHub...",
          categories: [],
          tags: [],
          id: 7
      })
      
    
      this.add({
          title: "Theoretical Machine Learning",
          excerpt: "Minimal Mistakes has been developed as a Jekyll theme gem for easier use. It is also 100% compatible with GitHub...",
          categories: [],
          tags: [],
          id: 8
      })
      
    
      this.add({
          title: "Theoretical Machine Learning",
          excerpt: "\n",
          categories: [],
          tags: [],
          id: 9
      })
      
    
      this.add({
          title: "Theoretical Machine Learning",
          excerpt: "You can also install the theme by copying all of the theme files[^structure] into your project. To do so fork...",
          categories: [],
          tags: [],
          id: 10
      })
      
    
  
    
    
      this.add({
          title: "Indexing Data Frames in R",
          excerpt: "Major Lessons What is a Data Frame? Compared to intellectual math challenges, technological issues are very mind scratching for me....",
          categories: ["DailyReport"],
          tags: ["R","data.frame"],
          id: 11
      })
      
    
      this.add({
          title: "Merging Data Frames in R by Row Names",
          excerpt: "Major Lessons Merge Data Frames I needed to concatenate two data frames which had row names. The regular method is...",
          categories: ["DailyReport"],
          tags: ["R","data.frame"],
          id: 12
      })
      
    
      this.add({
          title: "Indexing with Factors",
          excerpt: "Major Lessons I spent a cycle figuring this out: Any non-numeric thing that you read from a data file is...",
          categories: ["DailyReport"],
          tags: ["R","factor"],
          id: 13
      })
      
    
      this.add({
          title: "Indexing with Factors",
          excerpt: "Major Lessons I spent a cycle figuring this out: Any non-numeric thing that you read from a data file is...",
          categories: ["DailyReport"],
          tags: ["R","factor"],
          id: 14
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
        "title": "Applied Machine Learning",
        "url": "http://localhost:4000/courses/aml18/calendar",
        "excerpt": "Lecture slides\n\n\n  \n    \n      Lecture Number\n      Notes\n      PDF\n      Content\n    \n  \n  \n    \n      1\n      00/00/00\n      00/00/00\n      Introduction and Logistic\n    \n  \n\n\n",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Applied Machine Learning",
        "url": "http://localhost:4000/courses/aml18/info/",
        "excerpt": "\n",
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
        "title": "Introduction and Logistics",
        "url": "http://localhost:4000/courses/aml18/test",
        "excerpt": "In the morning Eat eggs Drink coffee In the evening Eat spaghetti Drink wine Conclusion And the answer is… $f(x)=\\sum_{n=0}^\\infty\\frac{f^{(n)}(a)}{n!}(x-a)^n$...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Theoretical Machine Learning",
        "url": "http://localhost:4000/courses/tml/announcements",
        "excerpt": "Minimal Mistakes has been developed as a Jekyll theme gem for easier use. It is also 100% compatible with GitHub...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Theoretical Machine Learning",
        "url": "http://localhost:4000/courses/tml/assignments",
        "excerpt": "Minimal Mistakes has been developed as a Jekyll theme gem for easier use. It is also 100% compatible with GitHub...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Theoretical Machine Learning",
        "url": "http://localhost:4000/courses/tml/calendar",
        "excerpt": "Minimal Mistakes has been developed as a Jekyll theme gem for easier use. It is also 100% compatible with GitHub...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Theoretical Machine Learning",
        "url": "http://localhost:4000/courses/tml/info",
        "excerpt": "\n",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Theoretical Machine Learning",
        "url": "http://localhost:4000/courses/tml/syllabus",
        "excerpt": "You can also install the theme by copying all of the theme files[^structure] into your project. To do so fork...",
        "teaser":
          
            null
          
      },
    
  
    
    
    
      
      {
        "title": "Indexing Data Frames in R",
        "url": "http://localhost:4000/dailyreport/rindexing/",
        "excerpt": "Major Lessons What is a Data Frame? Compared to intellectual math challenges, technological issues are very mind scratching for me....",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Merging Data Frames in R by Row Names",
        "url": "http://localhost:4000/dailyreport/rmerge/",
        "excerpt": "Major Lessons Merge Data Frames I needed to concatenate two data frames which had row names. The regular method is...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Indexing with Factors",
        "url": "http://localhost:4000/dailyreport/rfactorindexing/",
        "excerpt": "Major Lessons I spent a cycle figuring this out: Any non-numeric thing that you read from a data file is...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Indexing with Factors",
        "url": "http://localhost:4000/dailyreport/gitlab-bitbucket-googledrive/",
        "excerpt": "Major Lessons I spent a cycle figuring this out: Any non-numeric thing that you read from a data file is...",
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
