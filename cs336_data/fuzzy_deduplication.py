import re
import unicodedata
import hashlib
import itertools
from collections import defaultdict
from .deduplication import exact_line_deduplication
import os

def normalize_text(text):
    text_lower = text.lower()
    text_no_punctuation = re.sub(r'[^\w\s]', '', text_lower)
    text_spaces_normalized = re.sub(r'\s+', ' ', text_no_punctuation)
    text_nfd_normalized = unicodedata.normalize('NFD', text_spaces_normalized)

    # Filter out characters that are diacritical marks (category 'Mn')
    res = ''.join(char for char in text_nfd_normalized if unicodedata.category(char) != 'Mn')
    return res
    
def generate_ngrams(text, num_ngrams):
    text = text.split()
    res = []
    l = 0
    r = num_ngrams
    while r <= len(text):
        res.append(tuple(text[l:r]))
        l += 1
        r += 1
    return res

def generate_minHash(ngram_set, num_hash):
    res = []
    for k in range(num_hash):
        hash_value = generate_hash_ngrams(ngram_set, k)
        res.append(min(hash_value))
    return res

def jaccard_similarity(s1, s2):
    data = list(zip(s1,s2))
    match = 0
    for i in data:
        if i[0] == i[1]:
            match += 1

    return match/len(s1)

def generate_minhash_signatures(input_files, ngram_size, num_hashes):
    result = {}
    for k, text in input_files.items():
        norm = normalize_text(text)
        ngrams = generate_ngrams(norm, ngram_size)
        result[k] = generate_minHash(ngrams, num_hashes)
    return result

def generate_lsh_bands(hashed_docs, band_size):
    buckets = defaultdict(list)
    for doc_id, sig in hashed_docs.items():
        for i in range(0, len(sig), band_size):
            band = tuple(sig[i:i+band_size])
            buckets[band].append(doc_id)
    seen = set()
    for docs in buckets.values():
        if len(docs) > 0:
            seen.add(tuple(sorted(docs)))
    return sorted(seen)

def generate_candidate_pairs_and_distinct_docs(bands):
    pairs = set()
    distinct = set()
    for band in bands:
        if len(band) >= 2:
            pairs.update(itertools.combinations(band, 2))
        else:
            distinct.add(band[0])
    return pairs, distinct

def classify_docs_by_similarity(hashes, pairs, threshold):
    similar = set()
    distinct = set()
    for a, b in pairs:
        sim = jaccard_similarity(hashes[a], hashes[b])
        if sim >= threshold:
            similar.add((a, b))
        else:
            distinct.update([a, b])
    return similar, distinct

def build_similarity_groups(pairs):
    parent = {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px
    all_docs = set()
    for a, b in pairs:
        all_docs.update([a, b])
        if a not in parent:
            parent[a] = a
        if b not in parent:
            parent[b] = b
        union(a, b)
    groups = defaultdict(set)
    for doc in all_docs:
        groups[find(doc)].add(doc)
    return list(groups.values())

def fuzzy_deduplication(input_files, num_hashes, num_bands, ngrams, jaccard_threshold, output_directory):
    band_size = num_hashes // num_bands
    hashed = generate_minhash_signatures(input_files, ngrams, num_hashes)
    bands = generate_lsh_bands(hashed, band_size)
    pairs, initial_distinct = generate_candidate_pairs_and_distinct_docs(bands)
    similar, distinct = classify_docs_by_similarity(hashed, pairs, jaccard_threshold)
    distinct.update(initial_distinct)

    groups = build_similarity_groups(similar)
    keep_one = {sorted(group)[0] for group in groups}
    all_similar = set().union(*groups)
    final_distinct = {doc for doc in distinct if doc not in all_similar}
    final_distinct.update(keep_one)

    exact_line_deduplication(input_files=final_distinct, output_directory=output_directory)
    return

if __name__ == "__main__":
    docs = {
        "path1": "Meet me at the pool tomorrow ",
        "path2": "Meet us at the pool tomorrow ",
        "path3": "I will meet you at the pool tomorrow",
        "path4": "We can meet at the pool tomorrow",
        "path5": "You meet me at the pool tomorrow",
        "path6": "This is a completely different sentence",
        "path7": "This is a check. Super duper long sentence. Has too many words. Different words. Just keeps going. Hope it ends soon. Not yet",
        "path8": "This is a check. Super duper long sentence",
        "path9": "Apple apple apple apple",
        "path10": "paple paple paple paple"
    }

    ngram_size = 2
    num_hashes = 6
    num_bands = 3
    similarity_threshold = 0.8
    output_directory = './output/'

    fuzzy_deduplication(
        input_files=list(docs.keys()),
        num_hashes=num_hashes,
        num_bands=num_bands,
        ngrams=ngram_size,
        jaccard_threshold=similarity_threshold,
        output_directory=output_directory
    )
