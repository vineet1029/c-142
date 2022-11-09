from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
df = pd.read_csv('articles.csv')
df = df[df['title'].notna()]
count = CountVectorizer(stop_words = 'english')
countMatrix = count.fit_transform(df['title'])
cosineSim2 = cosine_similarity(countMatrix, countMatrix)
df = df.reset_index()
indices = pd.Series(df.index, index = df['contentId'])
def getRecommendations(contentId):
    idx = indices[int(contentId)]
    simScores = list(enumerate(cosineSim2[idx]))
    simScores = sorted(simScores, key = lambda x: x[1], reverse = True)
    simScores = simScores[1:11]
    articleIndices = [i[0] for i in simScores]
    return df[['url', 'title', 'text', 'lang', 'total_events']].iloc[articleIndices].values.tolist()