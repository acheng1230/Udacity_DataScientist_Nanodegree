## Udacity Data Scientist Nanodegree

### Project 03 - Recommendations with IBM

![ibm-recommendations](images/ibm-recommendations.png)

#### Table of Contents
1. [Overview](#summary)
2. [Data](#data)
3. [Project Files](#project_files)
4. [Credits](#credits)

#### 1. Overview <a name="summary"></a>
In this project, we analyze user-article interactions on the IBM Watson Studio platform and make various recommendations to users based on which new articles they may like. The types of recommendations we explore in this project include: rank based recommendations, user-user based collaborative filtering, and matrix factorization.

Rank based recommendations will be an analysis of the most popular articles based on the most interactions. Without any ratings to use, we will assume articles with most interactions are most popular.

User-user based collaborative filtering will look at user-article interactions and look for similar users on the basis of which similar articles the original users have interacted with. 

With matrix factorization, we will look at a machine learning approach to building recommendations. We will build out a user decomposition using the user-item interactions to get an idea of how well we can predict new articles for an individual to interact with. 


#### 2. Data <a name="data"></a> 
The data for this project is provided by the IBM Watson platform and is encapsulated within two CSV files:
	
1. articles_community.csv
2. user-item-interactions.csv

#### 3. Project Files <a name="project_files"></a>
The project files are contained within the file labeled, Recommendations with IBM, and are available in .ipynb and .html formats.

#### 4. Credits <a name="credits"></a>
This project was made available as part of the Udacity Data Scientist Nanodegree program and data was provided by the IBM Watson Studio platform.

