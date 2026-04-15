"""
SOCIAL MEDIA SENTIMENT ANALYSIS PROJECT
========================================
This script:
1. Loads tweets from CSV file
2. Analyzes sentiment (positive/negative/neutral)
3. Stores in MongoDB database
4. Extracts hashtags
5. Creates visualizations
6. Generates report
"""

# Import libraries
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from pymongo import MongoClient
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("🚀 SOCIAL MEDIA SENTIMENT ANALYSIS - STARTING")
print("="*70)

# ============================================================
# STEP 1: CONNECT TO MONGODB
# ============================================================
print("\n[STEP 1] 🔗 Connecting to MongoDB Database...")
print("-" * 70)

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['twitter_db']
    tweets_collection = db['tweets']
    server_info = client.server_info()
    print("✅ Successfully connected to MongoDB!")
    print(f"   Database: twitter_db")
    print(f"   Collection: tweets")
    
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    print("   Make sure MongoDB is running!")
    exit()

# ============================================================
# STEP 2: LOAD DATASET FROM CSV
# ============================================================
print("\n[STEP 2] 📂 Loading Tweet Dataset...")
print("-" * 70)
filename = 'twitter_us_airline_sentiment.csv' 

try:
    # ⚠️ CHANGE THIS TO YOUR FILENAME   
    df = pd.read_csv(filename)
    if 'tweet' in df.columns:
          df.rename(columns={'tweet': 'text'}, inplace=True)
    elif 'content' in df.columns:
          df.rename(columns={'content': 'text'}, inplace=True)
    
    print(f"✅ Successfully loaded dataset!")
    print(f"   File: {filename}")
    print(f"   Total tweets: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    
    print(f"\n   First 3 tweets:")
    for i in range(min(3, len(df))):
        print(f"   {i+1}. {str(df.iloc[i]['text'])[:80]}...")
    
except FileNotFoundError:
    print(f"❌ Error: File '{filename}' not found!")
    print("   Make sure your CSV file is in the same folder as this script")
    exit()

except Exception as e:
    print(f"❌ Error loading file: {e}")
    exit()

# ============================================================
# STEP 3: ANALYZE SENTIMENT
# ============================================================
print("\n[STEP 3] 🔍 Analyzing Sentiment of Each Tweet...")
print("-" * 70)

def analyze_sentiment(text):
    """
    Analyze sentiment of tweet
    Returns: 'Positive', 'Negative', or 'Neutral'
    """
    if pd.isna(text):
        return 'Neutral'
    
    try:
        text = str(text)
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    
    except:
        return 'Neutral'

# Apply sentiment analysis
print("⏳ Analyzing sentiment for each tweet...")
print("   This might take 1-3 minutes...")

df['sentiment'] = df['text'].apply(analyze_sentiment)

print("✅ Complete!")
print(f"✅ Sentiment analysis finished!")
print(f"   Total tweets analyzed: {len(df)}")

# Show sample results
print(f"\n   Sample Results:")
for i in range(min(5, len(df))):
    text = str(df.iloc[i]['text'])[:50]
    sentiment = df.iloc[i]['sentiment']
    print(f"   Tweet: '{text}...' → {sentiment}")

# ============================================================
# STEP 4: SENTIMENT STATISTICS
# ============================================================
print("\n[STEP 4] 📊 Sentiment Statistics...")
print("-" * 70)

sentiment_counts = df['sentiment'].value_counts()

print("Sentiment Distribution:")
total = len(df)
for sentiment_type in ['Positive', 'Negative', 'Neutral']:
    count = sentiment_counts.get(sentiment_type, 0)
    percentage = (count / total * 100) if total > 0 else 0
    bar = "█" * int(percentage / 2)
    print(f"  {sentiment_type:10s}: {count:5d} tweets ({percentage:5.1f}%) {bar}")

# ============================================================
# STEP 5: STORE IN MONGODB
# ============================================================
print("\n[STEP 5] Storing Data in MongoDB...")
print("-" * 70)

try:
    tweets_collection.delete_many({})
    print("Cleared old data from MongoDB")

    records = df[['text', 'sentiment']].to_dict('records')
    result = tweets_collection.insert_many(records)

    print("✅ Successfully stored data!")
    print(f"Total records inserted: {len(result.inserted_ids)}")

except Exception as e:
    print(f"❌ Error storing in MongoDB: {e}")

# ============================================================
# STEP 6: EXTRACT HASHTAGS
# ============================================================
print("\n[STEP 6] #️⃣  Extracting Hashtags...")
print("-" * 70)

hashtags = []

for text in df['text']:
    if pd.isna(text):
        continue
    found_tags = re.findall(r'#\w+', str(text).lower())
    hashtags.extend(found_tags)

hashtag_counts = Counter(hashtags).most_common(15)

print(f"✅ Hashtag extraction complete!")
print(f"   Total unique hashtags: {len(set(hashtags))}")
print(f"   Total hashtag mentions: {len(hashtags)}")

if hashtag_counts:
    print(f"\n   Top 15 Hashtags:")
    for i, (tag, count) in enumerate(hashtag_counts, 1):
        bar = "█" * int(count / max([c[1] for c in hashtag_counts]) * 20)
        print(f"   {i:2d}. {tag:20s} : {count:3d} {bar}")
else:
    print("   No hashtags found")

# ============================================================
# STEP 7: CREATE VISUALIZATIONS
# ============================================================
print("\n[STEP 7] 📈 Creating Charts...")
print("-" * 70)

try:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']  # Green, Red, Gray
    
    # Chart 1: Sentiment Pie Chart
    sentiment_counts.plot(
        kind='pie', 
        autopct='%1.1f%%', 
        colors=colors, 
        ax=axes[0],
        textprops={'fontsize': 11}
    )
    axes[0].set_title('📊 Sentiment Distribution of Tweets', 
                      fontsize=14, fontweight='bold', pad=20)
    axes[0].set_ylabel('')
    
    # Chart 2: Top Hashtags
    if hashtag_counts:
        tags, counts = zip(*hashtag_counts)
        
        bars = axes[1].barh(range(len(tags)), counts, color='#3498db')
        axes[1].set_yticks(range(len(tags)))
        axes[1].set_yticklabels(tags)
        axes[1].set_title('🔝 Top 15 Hashtags', 
                         fontsize=14, fontweight='bold', pad=20)
        axes[1].set_xlabel('Frequency', fontsize=12)
        axes[1].invert_yaxis()
        
        for i, (bar, count) in enumerate(zip(bars, counts)):
            axes[1].text(count, i, f' {count}', va='center', fontsize=10)
    else:
        axes[1].text(0.5, 0.5, 'No hashtags found', 
                    ha='center', va='center', fontsize=14)
    
    plt.tight_layout()
    
    filename_chart = 'sentiment_analysis_chart.png'
    plt.savefig(filename_chart, dpi=300, bbox_inches='tight')
    
    print(f"✅ Chart created and saved!")
    print(f"   File: {filename_chart}")
    
    plt.savefig("sentiment_analysis_chart.png")
    plt.close()
    
except Exception as e:
    print(f"❌ Error creating chart: {e}")

# ============================================================
# STEP 8: GENERATE FINAL REPORT
# ============================================================
print("\n" + "="*70)
print("📋 FINAL SENTIMENT ANALYSIS REPORT")
print("="*70)

print(f"\n📊 DATASET SUMMARY")
print("-" * 70)
print(f"Total Tweets Analyzed:     {len(df)}")
print(f"Analysis Date:             {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

print(f"\n💭 SENTIMENT BREAKDOWN")
print("-" * 70)
for sentiment_type in ['Positive', 'Negative', 'Neutral']:
    count = sentiment_counts.get(sentiment_type, 0)
    percentage = (count / len(df) * 100) if len(df) > 0 else 0
    print(f"  {sentiment_type:10s}: {count:6d} tweets ({percentage:6.2f}%)")

print(f"\n#️⃣  TOP HASHTAGS")
print("-" * 70)
if hashtag_counts:
    for i, (tag, count) in enumerate(hashtag_counts[:10], 1):
        percentage = (count / len(hashtags) * 100) if len(hashtags) > 0 else 0
        print(f"  {i:2d}. {tag:20s} : {count:4d} mentions ({percentage:5.2f}%)")
else:
    print("  No hashtags found")

print(f"\n📁 OUTPUT FILES GENERATED")
print("-" * 70)
print(f"  ✅ sentiment_analysis_chart.png  (Visualization)")
print(f"  ✅ MongoDB database 'twitter_db' (Data storage)")
print(f"  ✅ Collection 'tweets'            (Stored records)")

print("\n" + "="*70)
print("✅ ANALYSIS COMPLETE!")
print("="*70)

print("\n📌 NEXT STEPS:")
print("-" * 70)
print("1. Take screenshot of sentiment_analysis_chart.png")
print("2. Check MongoDB data: mongosh → use twitter_db → db.tweets.find()")
print("3. Upload sentiment_analysis.py to GitHub")
print("4. Add dataset link to GitHub README")
print("5. Create Word documentation")
print("-" * 70)