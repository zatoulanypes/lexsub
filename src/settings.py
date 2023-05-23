from pathlib import Path
from ruwordnet import RuWordNet
from wiki_ru_wordnet import WikiWordnet

BASE_DIR = Path(__file__).resolve().parent.parent
SUPPORTED_WORDNETS = (RuWordNet, WikiWordnet)
