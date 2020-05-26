from utils import DB

APP_VOCAB = {
    'READY!': {'TR': 'HAZIR!', 'EN': 'READY!'},
    'AGAIN!': {'TR': 'TEKRAR!', 'EN': 'AGAIN!'},
    'Best': {'TR': 'En İyi', 'EN': 'Best'},
    'Last': {'TR': 'Son', 'EN': 'Last'},
    'Home': {'TR': 'Geri', 'EN': 'Home'},
}


class Vocab:
    language = DB.store_get('language')

    def __call__(self, key):
        return APP_VOCAB.get(key, {'TR': key, 'EN': key}).get(self.language)


AppVocab = Vocab()
