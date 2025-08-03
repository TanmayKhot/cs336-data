import re
import unicodedata
import hashlib


def normalize_text(text):
    text_lower = text.lower()
    text_no_punctuation = re.sub(r'[^\w\s]', '', text_lower)
    text_spaces_normalized = re.sub(r'\s+', ' ', text_no_punctuation)
    text_nfd_normalized = unicodedata.normalize('NFD', text_spaces_normalized)

    # Filter out characters that are diacritical marks (category 'Mn')
    res = ''.join(char for char in text_nfd_normalized if unicodedata.category(char) != 'Mn')
    return res
    
def generate_ngrams(text, n):
    text = text.split()
    res = []
    l = 0
    r = n
    while r <= len(text):
        res.append(tuple(text[l:r]))
        l += 1
        r += 1
    return res

def generate_hash_ngrams(ngram_set, k):
    hash_value = []
    for ngram in ngram_set:
        data = f"{k}_" + " ".join(ngram)
        h = int(hashlib.sha256(data.encode()).hexdigest(), 16)
        hash_value.append(h)
    return hash_value

def generate_minHash(ngram_set, n_hash):
    res = []
    for k in range(n_hash):
        hash_value = generate_hash_ngrams(ngram_set, k)
        res.append(min(hash_value))
    return res

def jacobian_similarity(s1, s2):
    data = list(zip(s1,s2))
    match = 0
    for i in data:
        if i[0] == i[1]:
            match += 1

    return match/len(s1)

def compare_similarity(s1, s2):
    
    norm1 = normalize_text(s1)
    norm2 = normalize_text(s2)

    ngram1 = generate_ngrams(norm1, 2) 
    ngram2 = generate_ngrams(norm2, 2) 


    hash1 = generate_minHash(ngram1, 100)
    hash2 = generate_minHash(ngram2, 100)

    return jacobian_similarity(hash1, hash2)

s1 = "Meet me at the café tomorrow! "
s2 = "Let us meet at the cafe tomorrow"

print(compare_similarity(s1,s2))