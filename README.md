# Real-time News Scraping and Recommendation System
## Introduction:
Real-time News Scraping and Recommendation System is a single-page web application. The goal is to provide a reading news platform where users could read latest news, tagged by different topics and recommended based on users' behaviors. 

### News Pipeline：
In order to provide latest and distinct news, I build a data pipeline consists of news monitor, scraper, and dedeuper, connected with multiple message queues. 
* **Monitor**: 
By calling News API，monitor gets the abstract of latest news from multiple news resources(eg. BBC-news, CNN, IGN …). For each news fetched, hash it and compare the hash code with hash code of other recent news, if hash code already exists in Redis, ignore it, or one different news was found, and monitor passed the news to scrape_news message queue. This step guarantees each news passed to scrape_news message queue is not identical. 

* **Scraper**: 
Scraper is responsible for receiving tasks from scrape_news message queue, scraping news page content by URL and sending news content to dedupe_news message queue. 

* **Deduper**:
Deduper is designed for deduping reports from different news sources related to same event. Since TF-IDF(Term Frequency-Inverse Document Frequency) weights of similar news are similar, if TF-IDF of the latest news is similar to any news in the past 24 hours, that news would be discarded as a duplicate news. 

![](TODO: news_pipeline.png)

### Topic Modeling：
It’s tedious and unwise to tag each news manually. Thus, I implement Topic Modeling by tensorflow. After training the model, integrate Topic Modeling server side and client side with other services.

* **Vocabulary Embedding**:
	Only news title is taken into consideration for topic modeling. In order to interact between computer language and human(natural) language, a news title (string format) needs to be converted to number matrix (NLP).
	News title is encoded as index vector by VocaubularyProcessor. But if one uses number as a machine learning feature, number’s value would be taken into consideration, for example, 1 is more correlated with 2 than with 4. However, number’s value shouldn’t be am influential factor since it’s just the index. Thus, one-hot embedding is used to covert index to a vector.
	Finally, news title is converted to a number matrix.

* **CNNs (Convolutional Neural Networks)**:
	CNNs are basically just several layers of convolutions with nonlinear activation functions like ReLU or tanh applied to the results. 
	In CNNs, I use convolutions over the input layer (number matrix) to compute the output. This results in local connections, where each region of the input is connected to a neuron in the output. Each layer applies different filters and combines their results.

* **Filter Layer**: 	
	I typically use filters that slide over full rows of the matrix, since each row denotes an inseparable word. The height, or region size, may vary, but sliding windows over 2-5 words at a time is typical.

* **Pooling Layer**:
The goal of pooling is to provide a fixed size output matrix, which typically is required for classification (8 classes). Pooling also keeps the most salient information 

![](TODO: topic_modeling.png)
![](http://deeplearning.stanford.edu/wiki/images/6/6c/Convolution_schematic.gif "Convolution")


### Recommendation Service:
Recommendation service collects user’s clicks information, updates user’s preference model and tag user’s preferable news with “Recommend”.

* **Preference Model**:
	Time Decay Model (Moving Average) is used to indicate user’s preference. All topics start with same probability. Based on user’s clicks, selected topics probability increase and not selected topics decrease, while total sum of all topics’ probability is always 100%.
```
If selected: p = (1 - α) * p + α
If not selected: p = (1 - α) * p
α is time decay rate, larger α denotes more emphasis on recent clicks
```

* **Click Log Processor**:
	Since click logs might be time consuming and user doesn’t want to wait fro processing, click log processing is designed to be asynchronous. 
	When user click news card, click info (userId, newsId, timestamp) would be sent to click logger queue and also documented in database. ClickLogProcessor continuously fetch log from the queue and update user’s preference model and store it in database.

* **Recommendation Service**:
	When a user starts to browse news, backend service requests preference model from recommendation service, while recommendation service fetches user’s preference model from database. And all recommended topic would be tagged as “Recommend”.
  
![](TODO: recommendation_service)

### Authentication and Authorization：
Instead of using mature solutions like Auth0, I try to set up local strategy to do authentication and authorization.

* **Sign up & Log in**:
	Client side sends post request and server side validates if the user information is valid. At server side, all password is hashed with salt for storage. When user login, palin password is compared with hashed salt password ([bcrypt library](https://www.npmjs.com/package/bcrypt))

```
hashed password = hash (plain password + randomly generated salt)
```

* **Authentication**:
	When an user login in at the first time, a token (JWT) would be sent back to client side and stored in local storage. Since token should be unique, userId is used as payload with jwtSecret to generate token. 

* **Authorization**:
	After user’s login, each time user loads more news, request with token was sent to backend. AuthChecker, a middleware, decodes the token and verify it. Only if the token is valid, more news would be sent back to user.

![](TODO: auth.png)


* **Architecture**:
React is used to build frontend UI and Node serves as web server.
![](TODO: newsArchitecture.png)
