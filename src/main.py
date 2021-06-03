from parser import KununuReviewsParser
from stemmer import hanover_stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.kl import KLSummarizer
from nltk.corpus import stopwords
from PyInquirer import prompt
import glob

all_files = sorted(list(glob.glob('data/*.json')))
questions = [
    {
        'type': 'checkbox',
        'name': 'reviews_file',
        'message': 'What file do you want to summarize?',
        'choices': [{ 'name': 'all' }] + list(map(lambda file_path: { 'name': file_path}, all_files)),
        'validate': lambda answer: 'You must choose at least on data set.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'list',
        'name': 'summarization_method',
        'message': 'What method do you want to use?',
        'choices': [
            'Luhn',
            'LSA',
            'LexRank',
            'TextRank',
            'KL-Sum'
        ]
    },
    {
        'type': 'input',
        'name': 'compression',
        'message': 'How many sentences should the summary have?'
    }
]

answers = prompt(questions)
files = answers['reviews_file']
summarization_method = answers['summarization_method']
compression = answers['compression']

methods = {
    'Luhn': LuhnSummarizer(hanover_stemmer),
    'LSA': LsaSummarizer(hanover_stemmer),
    'LexRank': LexRankSummarizer(hanover_stemmer),
    'TextRank': TextRankSummarizer(hanover_stemmer),
    'KL-Sum': KLSummarizer(hanover_stemmer)
}

if 'all' in files:
    files = all_files
parser = KununuReviewsParser.from_files(files, Tokenizer('german'))
documents = parser.documents

summarizer = methods.get(summarization_method, methods['Luhn'])
summarizer.stop_words = stopwords.words('german')
for factor in parser.factors:
    print(factor)
    factor_document = documents[factor]
    for sentence in summarizer(factor_document, compression):
        print(sentence)
    print('------------------------------------------------')
    print()
