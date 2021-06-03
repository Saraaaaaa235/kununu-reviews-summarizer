from HanTa import HanoverTagger as ht

tagger = ht.HanoverTagger('morphmodel_ger.pgz')

def hanover_stemmer(word) -> str:
    return tagger.analyze(word)[0]
