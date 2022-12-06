import spacy

def tokenize_paragraphs(document):
    start = 0
    for token in document:
        if token.is_space and token.text.count("\n") > 1:
            yield document[start:token.i]
            start = token.i
    yield document[start:]

def calculate_comment_steps(doc):
    re_tokenized = [str(sub).split(',') for sub in doc.sents]
    re_tokenized = [item for sublist in re_tokenized for item in sublist]
    # re_tokenized needs to be flattened.
    print(re_tokenized)
    print(len(list(doc.sents)))
    print(len(re_tokenized))
    return (len(list(doc.sents)))

nlp = spacy.load('en_core_web_md')
text = "this is some text, with, commas, and. periods."
doc = nlp(text)

print(calculate_comment_steps(doc))

# for sent in doc.sents:
# 	print(sent.text)


# text = "this is me testing some text. And here's some with a question mark? \nAlso one more with exclamation!"
# doc = nlp(text)

# paragraphs = tokenize_paragraphs(doc)

# for graph in paragraphs:
#     print(graph)

