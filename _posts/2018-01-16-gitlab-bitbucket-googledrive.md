---
title:  "The Painful Part of Collaboration: Version Control and Shared Storage Spaces"
categories: 
  - DailyReport 
tag: 
  - GitLab
  - GitHub
  - Google Drive
  - Version Control  
---
Anyone who had online collaboration experience faced this question one way or another: What is a good version control system for code and manuscripts? Where should we store static data?

# Major Lessons
Of course, a version control system is a must-have for an online collaborative project. Putting aside the more classic Sub-version, Git and Mercurial are among the most used version control __softwares__. Git is supported by GitHub, GitLab, and Bitbucket web interfaces while Mercurial is mostly supported by Bitbucket. 

Then the collaboration problem reduces to selecting one of these, right? No! 
Different groups and companies have different preferences, and if you collaborate on the same project with more than one group, there will be a problem. 

## Case Study
In our lab ant [UMN](http://cs.umn.edu/) we were using Mercurial/Bitbucket, and here at BMI[^1] because we are using private (patient) data, we work with an internal version of the GitLab.
Now, I want to have a joint project with my thesis advisor and my postdoc mentor. What is a good setup? 

I'm fortunate because the software that each group uses is different (Mercurial vs. Git). So the hidden `.git` or `.hg` is considered as a directory in your repository, which you can tell the version control software even to ignore updating. But, I still don't know how to do this if both parties use, say, Git. 

## Hierarchical Folder Structure and Reproducibility
We are using a folder structure proposed for computational biology projects in [a paper](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000424) in PLOS Computational Biology. 

The goal is to keep a clean project folder with as many instruction file and documentation as possible to enable the future researcher to exactly replicate your claim. Roughly speaking, we have a directory for each of code, documentation(paper draft and relevant literature), data(raw and clean), and results (figure, raw experiment outcomes) each of them accompanied with a detail `README.md` file. 

## Data Files
Another critical issue is the strategy of handling the static files. In any data science project, there are static (input) files. Of course, you do some preprocessing or cleaning, but after that, you usually do not change those files. So, it doesn't make sense to put those in the repository. They eat up your space, and when you want to commit the software should check all of those for changes (use git or hg ignore for this!). Also, every participant may need to keep large files in different places, e.g., external hard drives. 

We are still playing with a standard way of handling this problem. The current approach is as follows:
Almost every reasonable operating system has an environment variable `$HOME`. 
One can store a `.json` file containing the user defined path to the data folder in the following address: 
```
$HOME/paths/[projectName].json
``` 
And the `[projectName].json` file will look like:
```
{
    "path" : {C:\Users\amira\google drive\[projectName]\data}
}
``` 
Instead of saving files in `data` folder and pushing all of the clean and raw files in the repository, here only `[projectName].json` will be in the repo. And when you set it once to your local data directory, you should put it in `.gitignore` list because no one else would need to know where you store your files. 

## Including Google Drive
I prefer to have another backup on cloud for ease of use and possible incidents [^2].
I have unlimited Drive storage. Google recently changed the name to Backup and Sync and supports instant both way sync. 

Through trial and error, I've come up with the following steps, which prevents Drive's always syncing feature from ruining your day: 

- Quit/Pause Drive and work on your project. 
- Commit, and push to a remote repository. 
- Open the Drive and let it sync. 

[^1]: I'm at [MBI](https://mbi.osu.edu/), my mentor is at [BMI](http://bmi.osu.edu/) department!  
[^2]: You think you can trust version control web interfaces? You are wrong! Read more about [GitLab.com database incident](https://about.gitlab.com/2017/02/01/gitlab-dot-com-database-incident/).