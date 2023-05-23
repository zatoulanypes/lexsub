from tqdm.auto import tqdm
from ruwordnet import RuWordNet
from wiki_ru_wordnet import WikiWordnet
from sklearn.neighbors import KDTree
from collections import Counter

import sys
import pickle
import gensim
import numpy as np

from WordNetWrapper import WordNetWrapper
from settings import BASE_DIR


class LexSub:
    def __init__(self, model_dir, wordnet_instance):
        self.wordnet = WordNetWrapper(wordnet_instance)
        self.model_path = BASE_DIR / "data" / "models" / model_dir / "model.model"
        self.model_name = model_dir.split("_")[0]
        self.model = self._load_model()

    def _load_model(self):
        return gensim.models.KeyedVectors.load(self.model_path.as_posix())

    def _get_synsets(self, word):
        synsets = self.wordnet.get_synsets_by_word(word)
        if not synsets:
            for most_similar, _ in self.model.similar_by_word(word):
                synsets = self.wordnet.get_synsets_by_word(most_similar)
                if synsets:
                    sys.stdout.write("Getting most similar: {}\n".format(most_similar))
                    sys.stdout.flush()
                    break
            else:
                raise Exception("No synsets for word {}".format(word))
        sys.stdout.write("Getting synsets: {}\n".format(synsets))
        sys.stdout.flush()
        return synsets

    def _get_synonym_candidates(self, word):
        synonyms = {
            self.wordnet.get_sense_name(sense)
            for synset in self._get_synsets(word)
            for sense in self.wordnet.get_synset_senses(synset)
        }
        sys.stdout.write("Synonym candidates: {}\n".format(synonyms))
        sys.stdout.flush()
        return synonyms

    def _get_hypernym_candidates(self, word):
        hypernyms = {
            self.wordnet.get_sense_name(sense)
            for synset in self._get_synsets(word)
            for hypernym in self.wordnet.get_synset_hypernyms(synset)
            for sense in self.wordnet.get_synset_senses(hypernym)
        }
        sys.stdout.write("Hypernym candidates: {}\n".format(hypernyms))
        sys.stdout.flush()
        return hypernyms

    def _get_hyponym_candidates(self, word):
        hyponyms = {
            self.wordnet.get_sense_name(sense)
            for synset in self._get_synsets(word)
            for hyponym in self.wordnet.get_synset_hyponyms(synset)
            for sense in self.wordnet.get_synset_senses(hyponym)
        }
        sys.stdout.write("Hyponymm candidates: {}\n".format(hyponyms))
        sys.stdout.flush()
        return hyponyms

    def _rank_candidates(self):
        return

    def _preprocess_sentence(self, sentence):
        return

    def get_substitutes(self, sentence, target_word):
        return

    # def _vectorize(self, text):
    #     try:
    #         vec = np.nanmean(
    #             [self.model[word] for word in text.lower().split() if len(word) >= 3],
    #             axis=0,
    #         )
    #     except KeyError:
    #         return
    #     if np.any(np.isnan(vec)):
    #         return
    #     vec /= sum(vec**2) ** 0.5
    #     return vec

    # def _distance2vote(self, d, a=3, b=5):
    #     sim = np.maximum(0, 1 - d**2 / 2)
    #     return np.exp(-(d**a)) * sim**b

    # def _load_wordnet_vectors(self):
    #     words, vectors, synset_ids = [], [], []
    #     for synset in tqdm(self.wordnet.synsets):
    #         for sense in synset.senses:
    #             vector = self._vectorize(sense.name)
    #             if vector is None or np.isnan(vector).any():
    #                 continue
    #             words.append(sense.name)
    #             vectors.append(vector)
    #             synset_ids.append(synset.id)
    #     return KDTree(np.stack(vectors)), synset_ids

    # def train(self):
    #     self.vectors, self.synset_ids = self._load_wordnet_vectors()
    #     return self

    # def save(self):
    #     with open(
    #         BASE_DIR
    #         / "data"
    #         / "vectors"
    #         / "{}_{}.pickle".format(self.model_name, self.wordnet_name),
    #         "wb",
    #     ) as file:
    #         pickle.dump((self.vectors, self.synset_ids), file)
    #     return self

    # def load(self):
    #     with open(
    #         BASE_DIR
    #         / "data"
    #         / "vectors"
    #         / "{}_{}.pickle".format(self.model_name, self.wordnet_name),
    #         "rb",
    #     ) as file:
    #         self.vectors, self.synset_ids = pickle.load(file)
    #     return self

    # def predict_hypernyms(self, word, pos):
    #     votes = Counter()
    #     dists, ids = self.vectors.query(self._vectorize(word).reshape(1, -1), k=100)
    #     for idx, distance in zip(ids[0], dists[0]):
    #         for hyper in self.wordnet[self.synset_ids[idx]].hypernyms:
    #             if pos and hyper.part_of_speech == pos:
    #                 votes[hyper.id] += self._distance2vote(distance)
    #     for sid, score in votes.most_common(10):
    #         sys.stdout.write("{}\t {}\n".format(score, self.wordnet[sid].title))
    #         sys.stdout.flush()


if __name__ == "__main__":
    lexsub = LexSub("geowac_fasttextskipgram_300_5_2020", WikiWordnet())
    lexsub._get_hypernym_candidates("кукарека")
    lexsub._get_hyponym_candidates("кукарека")
    lexsub._get_synonym_candidates("кукарека")
    # # lexsub.train().save().predict_hypernyms("найти", "V")
    # lexsub.load().predict_hypernyms("кукарека", "V")
