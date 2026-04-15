# Social Media Sentiment Analysis Project

## 🎯 Project Overview
This project analyzes sentiment of tweets/social media posts using TextBlob and stores data in MongoDB.

## 📊 Dataset
- **Source**: Kaggle - Sentiment140 Dataset
- **Link**: https://www.kaggle.com/datasets/kazanova/sentiment140
- **Size**: 1.6 million tweets
- **Format**: CSV

## 🛠️ Technologies Used
- **Python 3.9+**
- **TextBlob** - Sentiment Analysis
- **Pandas** - Data Processing
- **MongoDB** - Database
- **Matplotlib** - Visualization

## 📋 Features
✅ Loads tweets from CSV  
✅ Analyzes sentiment (Positive/Negative/Neutral)  
✅ Stores data in MongoDB  
✅ Extracts and counts hashtags  
✅ Creates visualization charts  
✅ Generates comprehensive report  

## 📈 Results
- **Total Tweets Analyzed**: 5000
- **Positive Sentiments**: 36%
- **Negative Sentiments**: 24%
- **Neutral Sentiments**: 40%
- **Top Hashtag**: #happy (145 mentions)

## 🚀 How to Run
1. Install Python 3.9+
2. Install MongoDB
3. Install dependencies:
```bash
   pip install pandas textblob matplotlib pymongo
   python -m textblob.download_corpora
```
4. Download dataset from Kaggle (link above)
5. Place CSV in same folder as script
6. Run:
```bash
   python sentiment_analysis.py
```

## 📁 Files
- `sentiment_analysis.py` - Main script
- `sentiment_analysis_chart.png` - Output visualization
- `README.md` - Project documentation

## 📸 Screenshots
- `01_python_output.png` - Script execution and final report
- `02_sentiment_chart.png` - Sentiment & hashtags visualization
- `03_mongodb_data.png` - MongoDB database contents

## 👤 Author
Mugesh Guru M

## 📝 License
Open source - Free to use and modify

---
**Assignment Submission**: Social Media Sentiment Analysis  
**Subject**: Data Analytics / Big Data  
**Date**: April 2024
