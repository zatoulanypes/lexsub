from ruwordnet import RuWordNet
from wiki_ru_wordnet import WikiWordnet

from settings import SUPPORTED_WORDNETS

class WordNetWrapper:
    def __init__(self, wordnet):
        if not isinstance(wordnet, SUPPORTED_WORDNETS):
            raise UnsupportedWordNetException(wordnet)
        self.wordnet = wordnet
        self.wordnet_name = str(wordnet).split(".")[1]

    def get_synsets_by_word(self, word):
        if isinstance(self.wordnet, RuWordNet):
            return self.wordnet.get_synsets(word)
        if isinstance(self.wordnet, WikiWordnet):
            return self.wordnet.get_synsets(word)

    def get_synset_senses(self, synset):
        if isinstance(self.wordnet, RuWordNet):
            return synset.senses
        if isinstance(self.wordnet, WikiWordnet):
            return synset.get_words()

    def get_synset_hypernyms(self, synset):
        if isinstance(self.wordnet, RuWordNet):
            return synset.hypernyms
        if isinstance(self.wordnet, WikiWordnet):
            return self.wordnet.get_hypernyms(synset)

    def get_synset_hyponyms(self, synset):
        if isinstance(self.wordnet, RuWordNet):
            return synset.hyponyms
        if isinstance(self.wordnet, WikiWordnet):
            return self.wordnet.get_hyponyms(synset)

    def get_sense_name(self, sense):
        if isinstance(self.wordnet, RuWordNet):
            return sense.name.lower()
        if isinstance(self.wordnet, WikiWordnet):
            return sense.lemma().lower()


class UnsupportedWordNetException(Exception):
    def __init__(self, wordnet_instance):
        super().__init__(
            """WordNet type {} is not supported. Pass an instance of one of the following types: {}""".format(
                wordnet_instance.__class__, SUPPORTED_WORDNETS
            )
        )
