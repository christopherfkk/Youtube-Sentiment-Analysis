from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

class CommentAnalyzer:

    def __init__(self, comment) -> None:
        self.comment = comment

    def clean(self):
        comment = self.comment.lower().strip()
        word_tokens = word_tokenize(comment)
        filtered_tokens = [w for w in word_tokens if not w in stopwords.words('english')]
        word = ' '.join(filtered_tokens)
        return word

    def get_polarity(self):
        pass

    def get_sentiment(self):
        pass


analyzer = CommentAnalyzer("  I am very FUNNY tell me otherwise love !! ;df")
print(analyzer.clean())