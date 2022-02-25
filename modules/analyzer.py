from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

class CommentAnalyzer:

    def __init__(self, comment) -> None:
        self.comment = comment

    def clean(self):

        # 1) lower case and strip trailing white spaces
        comment = self.comment.lower().strip() 

        # 2) remove emojis, source: https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        comment = emoji_pattern.sub(r'', comment)

        # ) tokenize words into a list of strings
        word_tokens = word_tokenize(comment)

        # 3) remove stop words
        filtered_tokens = [w for w in word_tokens if not w in stopwords.words('english')]

        # 4) join word tokens
        word = ' '.join(filtered_tokens)

        return word

    def get_polarity(self):

        sid = SentimentIntensityAnalyzer()
        polarity = sid.polarity_scores(self.clean())

        # sample output: {'neg': 0.0, 'neu': 0.281, 'pos': 0.719, 'compound': 0.8264}
        return polarity['compound']

    def get_sentiment(self):

        polarity = self.get_polarity()

        if polarity >= 0.05:
            return "pos"
        elif polarity <= 0.05:
            return "neg"
        else:
            return "neu"