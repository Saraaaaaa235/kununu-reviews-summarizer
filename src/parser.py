import json
import functools
import operator

from sumy.models.dom import ObjectDocumentModel, Paragraph, Sentence
from sumy.utils import cached_property

# This parser can parse a list of kununu reviews as extracted by the kununu-data-collector (JSON format).
# It returns a collection of documents, where each document corresponds to one review factor
# A document itself consists of Paragraphs, where each Paragraph is the comment associated with
# the factor and belonging to one review.
# A paragraph itself may consist of one or more sentences, where a sentence is constructed by
# applying a sentence tokenizer to the comment.
# The summarizer will then operate on an individual document.
class KununuReviewsParser:
    @classmethod
    def from_file(cls, file_path: str, tokenizer):
        with open(file_path, encoding="utf-8") as file:
            return cls(json.load(file), tokenizer)
    
    @classmethod
    def from_files(cls, file_paths: list[str], tokenizer):
        file_contents = []
        for path in file_paths:
            with open(path, encoding="utf-8") as file:
                file_contents.append(json.load(file))
        all_reviews = functools.reduce(operator.iconcat, file_contents, [])
        return cls(all_reviews, tokenizer)

    def __init__(self, kununu_reviews, tokenizer):
        self._kununu_reviews = kununu_reviews
        self._tokenizer = tokenizer

    @cached_property
    def documents(self) -> dict[str, ObjectDocumentModel]:
        documents = dict()
        for review in self._kununu_reviews:
            factors = review['factors']
            factor_types = list(factors.keys())
            for factor_type in factor_types:
                factor_comment = factors[factor_type]['comment']
                if factor_comment:
                    sentences = (Sentence(s, self._tokenizer) for s in self._tokenizer.to_sentences(factor_comment) if s.strip())
                    if factor_type not in documents:
                        documents[factor_type] = []
                    documents[factor_type].append(Paragraph(sentences))
        return { factor_type: ObjectDocumentModel(paragraphs) for factor_type, paragraphs in documents.items() }

    @cached_property
    def factors(self) -> list[str]:
        return list(self.documents.keys())
