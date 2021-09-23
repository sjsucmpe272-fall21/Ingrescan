# Team-Project-15

## Idea 1 - Ingredients Analyser Mobile App
### Introduction to the Problem Statement
To analyse and give detailed suggestions about the ingredients used in the product, based on the user’s profile and health.

### Abstract
As per the Center for Disease Control and Prevention [2], [3] and [4] :-

   -  In the year 2018, around half a million deaths in the US included hypertension as a primary or contributing cause. 
   -  29 million adults in the US have cholesterol levels higher than 240 mg/dl. Which basically means he/she has a high probability of developing a heart disease.
   -  1 in 10 Americans have diabetes and 1 in 3 Americans have prediabetes.

Most of the causes for such life threatening diseases are caused by processed and ultra-processed foods. In [1] Baldridge et al, have stressed on the fact that more than 70% of the food products in the US are ultra processed. Ultra processed foods are those that typically have many ingredients including sugar, oils, fats, salt, stabilizers, and preservatives. Ultra-processed foods are unhealthy no matter where you look but compared to other countries, the US version is even worse, because it is generally processed with a higher sugar and sodium content, the study reports.

### Approach
The dataset would be hosted through a MongoDB database. The user would be able to scan any ingredient list and the app would basically give information about the pros and cons of each of the ingredients. Furthermore, based on the user profile, the application would rate the healthiness of the product.

### Persona
Our target audience would be individuals who do their grocery shopping. This tool will help the users to make an informed decision about their purchase.

### Dataset
https://www.kaggle.com/openfoodfacts/world-food-facts

#### References:
- Baldridge, A.S.; Huffman, M.D.; Taylor, F.; Xavier, D.; Bright, B.; Van Horn, L.V.; Neal, B.; Dunford, E. The Healthfulness of the US Packaged Food and Beverage Supply: A Cross-Sectional Study. Nutrients 2019, 11, 1704.
- https://www.cdc.gov/bloodpressure/facts.htm
- https://www.cdc.gov/cholesterol/facts.htm
- https://www.cdc.gov/diabetes/library/features/diabetes-stat-report.html


## Idea 2 - Search System for Covid Data
### Introduction to the Problem Statement
In the current covid situation, people have to keep track of covid related information being shared across social media and how this data is trending differently across different countries to plan their travel itinerary. So building a multilingual search-based application will help in browsing through covid related tweets and find about covid cases across different regions.

### Abstract
Residents are clamoring to see how the covid virus has been trending across their neighborhoods and different parts of the world across different dates and how the data has been trending in these places. This could help them to provide more insights in terms of virus spread, preventive measures and take more steps to avoid any contact.
A search system that can help users in browsing tweets, visualizing COVID cases data in different regions in a particular date range can be helpful to take a calculated decision and avoid contact. 

### Approach
The approach for building this application,
  - Get the data related to COVID from Twitter/other covid data-related APIs.
  - Indexing data retrieved from the previous step in Solr for indexing and fast retrieval of data through search results.
  - Functionalities (Can be extended based on features offered by solr)
    - Faceted search feature where users can filter search results by keywords and date range.
    - Data visualization of covid cases through maps and charts.

### Persona
This application will help the users be aware of the latest news and trending information related to COVID and also find where COVID cases are rapidly increasing i.e highly affected zones.

### Dataset
No dataset required

#### Reference
- https://www.nytimes.com/2020/03/28/us/coronavirus-data-privacy.html
- https://solr.apache.org/
- https://github.com/lucidworks/banana


## Idea 3 - Content Impact Analyser
### Introduction to the Problem Statement
Sharing opinions and ideas on social media has become a norm. People share their experiences and feedback on social media as well. The shared content can have positive or negative impact about the issue it is addressing. It can influence many people’s state of mind. If there is a disagreement or some negative feedback, it is going to create a certain image of the issue, product or person it is being shared about. People can like, comment and share the post if they agree/disagree with it. And sometimes, before even validating the reliability of the content, people jump on conclusions. This invites some serious consequences like, fake news spreading, mob lynching, engagement of people in protests without realising the depth of the issue, spread of hatred, increase in violence etcetera. There must be some tool where people can go to, before sharing their thoughts/post/content, get some idea of how much significant impact it is going to make. This type of tool will make people reevaluate the information they’re going to share. People might validate the shared content before agreeing or disagreeing to any information. We’re proposing to develop a software that will give people the impact analysis of the content they’re going to share along with sentiment analysis.

### Abstract
Nowadays, social media has become a popular platform to express oneself. With the help of smartphones, people can post their ideas and opinions which can reach a wide range of audience within minutes. People can react to the posted content, comment on it and share the content on their timeline. It all happens within seconds to minutes. Content may be some good or bad news, some agreement or disagreement with any public policy, positive or negative feedback to any decisions, promotions, advertisement of any product or campaigns etcetera. Most of the time, content posted on social media influences people who read it. Content can have a specific impact on the audience it reaches and the way it can be interpreted. Impact can be positive or negative. Majority of people, while posting any content on social media, are not aware of how it is going to influence other people. What if users already know that whatever content they’re going to share, how it is going to make an impact. If they know beforehand that they’re going to share something that can have a negative impact on the people, they might choose to not to share harmful content or change the words used to avoid spreading negative social influence.

### Approach
Given historical data from a few social media platforms, we’re going to train our algorithm to understand what kind of content was negative and what kind of content made a positive impact. For example, we can have a large amount of tweets data which is also having sentiment labels, positive or negative. Based on the labeled data, our software will be able to get an impact of any new content that the user enters. This way users will be able to understand how their post is going to affect before even sharing it across social media platforms.

### Persona
The software is intended to work for any social media user.

### Dataset
https://www.kaggle.com/cosmos98/twitter-and-reddit-sentimental-analysis-dataset?select=Twitter_Data.csv
https://www.kaggle.com/kazanova/sentiment140


## Idea 4 - Crop- Weed Detection
### Introduction to the Problem Statement
To build an interface to help farmers detect weed in their crops with the help of image detection. This interface will help farmers detect and remove weed quickly before it destroys their crops, thus helping them save their only sources of income. In countries like India, crops can easily be polluted with weeds which are a menace to the farmers. Indian farmers are not technologically equipped to deal with such problems. In my opinion, the crop-weed detection using machine learning would be a game changer in the field of agriculture. With the use of algorithms, it would save a substantial time for the farmers and reduce their costs thereby improving their overall efficiency.

### Abstract
Artificial intelligence is a fast-growing field in today’s world. Amongst the many applications that it has, one of them is object recognition which makes use of computer vision. This project uses the same to develop a system for the identification of different crops and weeds. Images are assessed through the dataset link provided below, using computer vision for image processing, We can build a model with the help of transfer learning on YOLO/RCNN which would help perform the identification of plants autonomously. This project opens the doors to more advanced and intelligent systems and is an alternative to the traditional weed detectors in agriculture.

### Approach
Since the dataset is already annotated, we plan to build a ML model with the help of the dataset (shown below).
This ML pipeline would look something as follows:
- We would explore the data and find if there are any anomalies (for example: crops looking like weed or weed looking like a crop)
- If there are any anomalies, we would then try to deal with them either by removing them or collecting more data to ensure that they are anomalies
- Once this is done, we will then augment the data (by changing the angles of the images). This will help us build a more robust ML model.
- Then we will try YOLO/RCNN model with transfer learning to build a model on the training data.
- Once the model is built, we will predict on test data and check the F-1 score
- We are checking F-1 Score because we want our model to have high precision and high recall
Once we have built a model, we plan to build a simple interface so that it acts like an abstraction so that the end user can easily check the results.


### Persona
Farmers.

### Dataset
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7305380/


## Idea 5 - SecureWay
### Introduction to the Problem Statement
In today’s world, the crime rate has increased a lot. It has become easier than ever to commit a crime and still go undetected because of lack of safety measures. Hence, this project aims to provide commuters with a sense of safety as they will be able to avoid crime hotspots on their commute way home. This will also help women commuters travelling in the night as they will be able to know if commuting through a particular location is safe or not.

### Abstract
SecureWay would ensure a little more peace of mind to the commuters travelling alone at locations in the night or which are unknown to them. We plan to use Chicago crime data set which would show crime figures taken from monthly reports, such as sexual assault, mugging, knife attacks, murder etc. To build an ML model which would predict if the location is safe or not. We plan to give more weightage to sexual assault and murder as they are more heinous crimes and the location in which that happens frequently should be completely avoided. As a bonus feature, we will try to add a feature where the commuter can check in with friends/family if he/she feels unsafe. For example, the commuter can tap ‘fine’ every 1 minute or ‘nervous’ every 30 seconds before the loved ones are alerted and shown the commuter’s location.

### Approach
We plan to build an ML model which would detect if the location the commuter is traveling is safe or not.
The ML model pipeline would look as follows:
- We plan to use Chicago crime data set to build a binary classifier model.
- While training this model, we would give more weightage to “Sexual Assault” and “Murder”
- The model trained would detect if the location is safe for the commuter or not based on the parameters (data) we pass to the model.
- The metric we are using here is log loss as we want the probability of weather the location is safe or not.

### Persona
General Public/Commuters.

### Dataset
https://github.com/newsapps/chicagocrime/blob/master/docs/api_docs.md
