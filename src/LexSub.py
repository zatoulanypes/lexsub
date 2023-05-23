from ruwordnet import RuWordNet
from wiki_ru_wordnet import WikiWordnet

import sys
import gensim

from WordNetWrapper import WordNetWrapper
from LexSubScorer import LexSubScorer
from settings import BASE_DIR


class LexSub:
    def __init__(self, model_dir, wordnet_instance):
        self.wordnet = WordNetWrapper(wordnet_instance)
        self.model_path = BASE_DIR / "data" / "models" / model_dir / "model.model"
        self.model_name = model_dir.split("_")[0]
        self.model = self._load_model()

    def _load_model(self):
        print("Loading model {} from {}".format(self.model_name, self.model_path))
        return gensim.models.KeyedVectors.load(self.model_path.as_posix())

    def _get_synsets(self, word):
        synsets = self.wordnet.get_synsets_by_word(word)
        if not synsets:
            for most_similar, _ in self.model.similar_by_word(word):
                synsets = self.wordnet.get_synsets_by_word(most_similar)
                if synsets:
                    print("Getting most similar: {}".format(most_similar))
                    break
            else:
                raise Exception("No synsets for word {}".format(word))
        print("Getting synsets: {}".format(synsets))
        return synsets

    def _get_synonym_candidates(self, word):
        synonyms = {
            self.wordnet.get_sense_name(sense)
            for synset in self._get_synsets(word)
            for sense in self.wordnet.get_synset_senses(synset)
        }
        print("Synonym candidates: {}".format(synonyms))
        return synonyms

    def _get_hypernym_candidates(self, word):
        hypernyms = {
            self.wordnet.get_sense_name(sense)
            for synset in self._get_synsets(word)
            for hypernym in self.wordnet.get_synset_hypernyms(synset)
            for sense in self.wordnet.get_synset_senses(hypernym)
        }
        print("Hypernym candidates: {}".format(hypernyms))
        return hypernyms

    def _get_hyponym_candidates(self, word):
        hyponyms = {
            self.wordnet.get_sense_name(sense)
            for synset in self._get_synsets(word)
            for hyponym in self.wordnet.get_synset_hyponyms(synset)
            for sense in self.wordnet.get_synset_senses(hyponym)
        }
        print("Hyponymm candidates: {}".format(hyponyms))
        return hyponyms

    def _get_candidates(self, semtype, *args):
        semtypes = {
            "synonym": self._get_synonym_candidates,
            "hyponym": self._get_hyponym_candidates,
            "hypernym": self._get_hypernym_candidates,
        }
        return semtypes[semtype](*args)

    def _get_score(self, measure, *args):
        measures = {
            "add": LexSubScorer.add_measure,
            "bal_add": LexSubScorer.bal_add_measure,
            "mult": LexSubScorer.mult_measure,
            "bal_mult": LexSubScorer.bal_mult_measure,
        }
        return measures[measure](*args)

    def _rank_candidates(self, candidates, contexts, target_word, topn, measure):
        ranks = {
            candidate: self._get_score(
                measure, self.model.similarity, candidate, target_word, contexts
            )
            for candidate in candidates
        }
        return sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:topn]

    def _get_contexts(self, sentence, target_word, window):
        words = list(gensim.utils.tokenize(sentence))
        twx = words.index(target_word)
        left_context = words[twx - window : twx]
        right_context = words[twx + 1 : twx + 1 + window]
        return (*left_context, *right_context)

    def get_substitutes(
        self,
        sentence,
        target_word,
        semtype="synonym",
        topn=10,
        measure="add",
        context_window=2,
    ):
        print(
            "Looking for {} substitutes for '{}' in '{}'".format(
                semtype, target_word, sentence
            )
        )
        return self._rank_candidates(
            target_word=target_word,
            topn=topn,
            measure=measure,
            candidates=self._get_candidates(semtype, target_word),
            contexts=self._get_contexts(sentence, target_word, context_window),
        )


if __name__ == "__main__":
    lexsub = LexSub("geowac_fasttextskipgram_300_5_2020", RuWordNet())
    sent = "Сегодня я сдаю экзамен по математике"
    for sub, score in lexsub.get_substitutes(sent, "экзамен"):
        print("{}\t{}".format(score, sub))
    print()
    for sub, score in lexsub.get_substitutes(sent, "математике"):
        print("{}\t{}".format(score, sub))
