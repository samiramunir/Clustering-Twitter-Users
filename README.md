
# Clustering Twitter Users Based On News Article Retweet Behavior 

### A view of the network before any clustering analysis. 


![](/media/c.gif)



The light blue nodes are the articles. The lines are tweets and the pink nodes are users. 



## Objective
Perform Latent Dirichlet Allocation on article texts and Agglomerative Clustering on readers


## Process
Compiled over 3,000 NYT tweets and their retweeter (80,000) information using twitter API 
Collected article text (19 GB) from NYT website using bs4 and Newspaper3k libraries
Grouped articles into 5 news topics using LDA (Gensim). Performed unsupervised clustering to group retweeters into 5 user clusters based on the 5 news topics 



### A view of the network after articles were grouped into 5 topics 
![](/media/netxtopicuser100.png)



### Aggregated number of retweets of all articles under each topic


![](/media/agg_retweet_topic.png) 


### Number of articles grouped under each topic

![](/media/art_in_topic.png)



### User clusters based on retweet behavior
Converted the users into vectors of size equal to the number of topics. Each value in the vector is either 1 or 0 based on whether the user retweeted an article that belongs to the topic or not. 

Performed agglomerative clustering based on cosine similarity between each user vectors. 


*****************
User Cluster 1
![](/media/user_0.png)


*****************
User Cluster 2
![](/media/user_1.png)


*****************
User Cluster 3
![](/media/user_2.png)


*****************
User Cluster 4

![](/media/user_3.png)


*****************
User Cluster 5

![](/media/user_4.png)

