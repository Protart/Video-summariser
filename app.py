import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
from youtube_transcript_api import YouTubeTranscriptApi
from punctuator import Punctuator
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/<vid_id>')
def summarize(vid_id):

    text = """ """
    subs = YouTubeTranscriptApi.get_transcript(vid_id)
    sentences = [i['text'] for i in subs]
    text = ' '.join(sentences)
    p = Punctuator('Demo-Europarl-EN.pcl')
    text = p.punctuate(text)

    stopWords = set(stopwords.words("english")) 
    words = word_tokenize(text) 
    freqTable = dict() 
    for word in words: 
        word = word.lower() 
        if word in stopWords: 
            continue
        if word in freqTable: 
            freqTable[word] += 1
        else: 
            freqTable[word] = 1
    sentences = sent_tokenize(text) 
    sentenceValue = dict() 
    for sentence in sentences: 
        for word, freq in freqTable.items(): 
            if word in sentence.lower(): 
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else: 
                    sentenceValue[sentence] = freq 
    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence] 
    average = int(sumValues / len(sentenceValue)) 
    summary = '' 
    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)): 
            summary += " " + sentence 
    return summary