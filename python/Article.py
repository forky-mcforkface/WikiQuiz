import wikipedia as wiki
import nltk
from nltk.tokenize import sent_tokenize
import re

from Quiz import Quiz
from Question import Question

class Article():

    def __init__ (self, name):
        self.name = name
        self.page = wiki.page(name)

        self.propers = []
        self.locations = []
        self.quiz = Quiz([])

        self.iterate_sections()
        self.generate_questions_for(
            self.page.summary.encode('ascii', 'ignore'))

    def iterate_sections(self):
        # Iterate through article's sections
        for section in self.page.sections:
            sec = self.page.section(section).encode('ascii', 'ignore')
            if sec is None: 
                continue
            self.generate_questions_for(sec)

    def get_question_data(self, s):
        tokens = nltk.word_tokenize(s)
        tagged = nltk.pos_tag(tokens)
        grammar = """  
                    NUMBER: {<$>*<CD>+<NN>*}
                    DATE: {<IN>(<$>*<CD>+<NN>*)}
                    LOCATION: {<IN><NNP>+<,|IN><NNP>+}
                    PROPER: {<NNP|NNPS><NNP|NNPS>+}
                     """        
        # HIT!: {<PROPER><NN>?<VBZ|VBN>+}

        chunker = nltk.RegexpParser(grammar)
        result = chunker.parse(tagged)
        return result

    def generate_questions_for(self, sec):
        # Rid of all parentheses for easier processing
        _sec = "".join(re.split('\(', 
            sec.replace(")", "("))[0::2])

        for sentence in sent_tokenize(_sec):
            qdata = self.get_question_data(sentence)
            if len(qdata) >= 30:
                qdata = []

            self.create_questions(sentence, qdata)

    def create_questions(self, raw, chunked):
        for word in chunked:
            if type(word) != tuple:
                target = []
                for y in word:
                    target.append(y[0])
                self.quiz.add(
                    Question(raw, " ".join(target)))

