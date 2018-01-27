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
          excerpt: "Major Lessons What is a Data Frame? Compared to intellectual math challenges, technological issues are very mind scratching for me....",
          categories: ["DailyReport"],
          tags: ["R","data.frame"],
          id: 7
      })
      
    
      this.add({
          title: "Merging Data Frames in R by Row Names",
          excerpt: "Major Lessons Merge Data Frames I needed to concatenate two data frames which had row names. The regular method is...",
          categories: ["DailyReport"],
          tags: ["R","data.frame"],
          id: 8
      })
      
    
      this.add({
          title: "Introducing Pandoc",
          excerpt: "I was trying to figure out a way to write math heavy blog posts. There are well known JavaScript libraries...",
          categories: ["DailyReport"],
          tags: ["R","factor"],
          id: 9
      })
      
    
      this.add({
          title: "Indexing with Factors",
          excerpt: "Major Lessons I spent a cycle figuring this out: Any non-numeric thing that you read from a data file is...",
          categories: ["DailyReport"],
          tags: ["R","factor"],
          id: 10
      })
      
    
      this.add({
          title: "The Painful Part of Collaboration: Version Control and Shared Storage Spaces",
          excerpt: "Major Lessons\n\n",
          categories: ["DailyReport"],
          tags: ["GitLab","GitHub","GoogleDrive","VersionControl"],
          id: 11
      })
      
    
      this.add({
          title: "The Curious Case of Ibrutinib-resistant CLL: Does Reverse-Mutations Exist? - Part I",
          excerpt: "This came up during our lab meeting today with my great postdoc mentor Professor Kevin Coombes. I asked a dumb...",
          categories: ["DailyReport"],
          tags: ["CLL","cancer"],
          id: 12
      })
      
    
      this.add({
          title: "Introducing the Jekyll-Scholar",
          excerpt: "Major Lessons\n\n",
          categories: ["DailyReport"],
          tags: ["Jekyll","Plugin"],
          id: 13
      })
      
    
      this.add({
          title: "Gender Pay Gap, Why?",
          excerpt: "I’m fortunate to be a postdoc at the MBI instead of a member of a regular lab. Here, there is...",
          categories: ["DailyReport"],
          tags: ["ProfessionalDevelopement","JordanBPeterson"],
          id: 14
      })
      
    
      this.add({
          title: "Gender Pay Gap, Why?",
          excerpt: "I’m fortunate to be a postdoc at the MBI instead of a member of a regular lab. Here, there is...",
          categories: ["DailyReport"],
          tags: ["ProfessionalDevelopement","JordanBPeterson"],
          id: 15
      })
      
    
      this.add({
          title: "Gender Pay Gap, Why?",
          excerpt: "I’m fortunate to be a postdoc at the MBI instead of a member of a regular lab. Here, there is...",
          categories: ["DailyReport"],
          tags: ["ProfessionalDevelopement","JordanBPeterson"],
          id: 16
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
        "excerpt": "Major Lessons What is a Data Frame? Compared to intellectual math challenges, technological issues are very mind scratching for me....",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Merging Data Frames in R by Row Names",
        "url": "http://localhost:4000/dailyreport/r-merge/",
        "excerpt": "Major Lessons Merge Data Frames I needed to concatenate two data frames which had row names. The regular method is...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Introducing Pandoc",
        "url": "http://localhost:4000/dailyreport/pandoc/",
        "excerpt": "I was trying to figure out a way to write math heavy blog posts. There are well known JavaScript libraries...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Indexing with Factors",
        "url": "http://localhost:4000/dailyreport/r-factor-indexing/",
        "excerpt": "Major Lessons I spent a cycle figuring this out: Any non-numeric thing that you read from a data file is...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "The Painful Part of Collaboration: Version Control and Shared Storage Spaces",
        "url": "http://localhost:4000/dailyreport/gitlab-bitbucket-googledrive-Copy/",
        "excerpt": "Major Lessons\n\n",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "The Curious Case of Ibrutinib-resistant CLL: Does Reverse-Mutations Exist? - Part I",
        "url": "http://localhost:4000/dailyreport/cll-ibrutinib-resistence/",
        "excerpt": "This came up during our lab meeting today with my great postdoc mentor Professor Kevin Coombes. I asked a dumb...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Introducing the Jekyll-Scholar",
        "url": "http://localhost:4000/dailyreport/jekyll-scholar/",
        "excerpt": "Major Lessons\n\n",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Gender Pay Gap, Why?",
        "url": "http://localhost:4000/dailyreport/gender-pay-gap-Copy-(2)/",
        "excerpt": "I’m fortunate to be a postdoc at the MBI instead of a member of a regular lab. Here, there is...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Gender Pay Gap, Why?",
        "url": "http://localhost:4000/dailyreport/gender-pay-gap/",
        "excerpt": "I’m fortunate to be a postdoc at the MBI instead of a member of a regular lab. Here, there is...",
        "teaser":
          
            null
          
      },
    
      
      {
        "title": "Gender Pay Gap, Why?",
        "url": "http://localhost:4000/dailyreport/elastic-net-intuition/",
        "excerpt": "I’m fortunate to be a postdoc at the MBI instead of a member of a regular lab. Here, there is...",
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
