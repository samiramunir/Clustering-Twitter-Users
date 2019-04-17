
# Clustering Twitter Users Based On News Article Retweet Behavior 

### Motivation 

> "Social network analysis (SNA) is the process of investigating social structures through the use of networks and graph theory.[1] It characterizes networked structures in terms of nodes (individual actors, people, or things within the network) and the ties, edges, or links (relationships or interactions) that connect them." - Wikipedia 

Thanks to the advent of twitter and facebook the practical applications of network analysis , especially for businesses, has become more and more relevant. One of the many problems it solves is the problem of Data-sparsity and cold start-problems for recomemndation systems. Recommendations systems either rely on a user's history on past usage of products to map a user's taste and predict similar item based of off that or they rely on other users with similar interests. This is where the challenges of Data-Sparsity and Cold start-problems comes in. Which basically mean, not enough user data is available to begin with to make valid recommendations. It is especially pronounced in terms of News Recommendation thanks to the diversity and the sheer amount of new content production and plethora of sources of news available. Analysis of social networks presents a valuable yet challenging opportunity to gain insight in that regards. This project aims to perform such network analysis and cluster/segment twitter users based on what kind of news they share on social media. 

To limit the scope of the project I chose to use Twitter as the social medium. For news source I used New York Times (NYT), more specifically its Twitter posts. NYT tweets out news articles regularly on its twitter page. Twitter users then retweet those tweets. 

NODE: Each retweeter is a node.
EDGE: If two nodes have reweeted the same NYT post, then that is calculated as one link/edge between those two nodes. 


#### Data Collection: 
I collected metadata of twitter posts by NYT for 30 days using twitter API in the form of JSON logs.
Extracted list of retwitter IDs of a each post, from the json logs. A retweeter is defined as a twitter user who has retweeted a particular NYT post. 

Extracted link to NYT article (associated with each tweet) from the JSON logs and scraped the text of those articles from NYT website using bs4 and Newspaper3k libraries. 





### A view of the network before any clustering analysis. 

To take an initial look at the project, I made a network graph that shows the link between an NYT post and twitter users. 
The light blue nodes are the articles. The lines links/edges between each reader and the article. This is an intial view, just to do some exploratory analysis. Later we will define the nodes and edges as defined in the first section of this readme. 
![](/media/c.gif)






## Objective
Perform Latent Dirichlet Allocation on article texts and Agglomerative Clustering on readers




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

References: 
Quote: https://link.springer.com/chapter/10.1007/978-3-642-35377-2_42
Inspiration: https://blog.insightdatascience.com/news4u-recommend-stories-based-on-collaborative-reader-behavior-9b049b6724c4
