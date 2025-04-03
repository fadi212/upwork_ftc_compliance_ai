import nltk
import tiktoken
from typing import List
from src.custom.custom_route_layer import RouteLayer
from src.config.config import logger


def tag_text_with_router(router_layer, text):
    sentences = nltk.sent_tokenize(text)

    filtered_sentences = [sentence for sentence in sentences if len(sentence.split()) >= 12]

    pre_tagged_sentences = [
        {"sentence": sentence, "category": router_layer(sentence).name, "severity": 3}
        for sentence in filtered_sentences
    ]
    tagged_sentences = [
        tag for tag in pre_tagged_sentences if tag["category"] and tag["category"] != "Compliance"
    ]
    return tagged_sentences


def process_text(router_layer, text):
    tagged_sentences = tag_text_with_router(router_layer, text)
    return tagged_sentences


def get_basis_sentences(router_layer: RouteLayer, sentence: str) -> List[str]:
    route, scores, utterances = router_layer._retrieve_top_route(router_layer._encode(sentence))

    logger.debug(f"Route: {route}, Scores: {scores}, Utterances: {utterances}")  # Debug print

    basis = [
        utterance
        for score, utterance in zip(scores, utterances)
        if route and route.name == router_layer(sentence).name
    ]

    logger.debug(f"Basis sentences: {basis}")

    return basis


def count_tokens(text):
    encoding = tiktoken.encoding_for_model('text-embedding-ada-002')
    tokens = encoding.encode(text)
    return len(tokens)
