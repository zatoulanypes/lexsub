from pymorphy2 import MorphAnalyzer
from gensim.utils import tokenize


class TargetWord:
    def __init__(self, word, sentence):
        morph = MorphAnalyzer()
        self.lemma = morph.parse(word)[0].normal_form or word
        self.idx = sentence.lemmas.index(self.lemma)
        self.instance = sentence.tokens[self.idx]
        self.grammemes = morph.parse(self.instance)[0].tag.grammemes


class Substitute:
    def __init__(self, word):
        self.name = word
        self.parse = MorphAnalyzer().parse(word)[0]

    def inflect(self, grammemes):
        if len(self.name.split()) > 1:
            return self.name
        inflected = self.parse
        for grammeme in grammemes:
            inflected = inflected.inflect({grammeme}) or inflected
        return inflected.word


class Sentence:
    def __init__(self, string):
        self.string = string
        self.tokens = list(tokenize(string))
        morph = MorphAnalyzer()
        self.lemmas = [morph.parse(word)[0].normal_form for word in self.tokens]
