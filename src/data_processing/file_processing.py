import nltk
import tiktoken
import re


def tag_text_with_router(router_layer, text):
    sentences = nltk.sent_tokenize(text)

    processed_sentences = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 30:
            first_50_words = ' '.join(words[:50])
            if not re.search(r'[.!?]', first_50_words):
                chunked_sentences = [
                    ' '.join(words[i:i + 30]) for i in range(0, len(words), 30)
                ]
                processed_sentences.extend(chunked_sentences)
            else:
                processed_sentences.append(sentence)
        else:
            processed_sentences.append(sentence)

    filtered_sentences = [sentence for sentence in processed_sentences if len(sentence.split()) >= 12]

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


def count_tokens(text):
    encoding = tiktoken.encoding_for_model('text-embedding-ada-002')
    tokens = encoding.encode(text)

    return len(tokens)
