import re
import unicodedata
import hashlib
import itertools
from collections import defaultdict


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

def generate_hash_ngrams(ngram_set, k):
    hash_value = []
    MAX_HASH = 2**32 - 1
    for ngram in ngram_set:
        data = f"{k}_" + " ".join(ngram)
        h = int(hashlib.sha256(data.encode()).hexdigest(), 16) % MAX_HASH
        hash_value.append(h)
    return hash_value

def generate_minHash(ngram_set, num_hash):
    res = []
    for k in range(num_hash):
        hash_value = generate_hash_ngrams(ngram_set, k)
        res.append(min(hash_value))
    return res

def jacobian_similarity(s1, s2):
    print("Inside Jacob:", s1, s2)
    data = list(zip(s1,s2))
    match = 0
    for i in data:
        if i[0] == i[1]:
            match += 1

    return match/len(s1)

def generate_hash(docs):
    
    hashed_docs = {}
    for k in docs.keys():
        text = docs[k]
        normalized_text = normalize_text(text)
        ngrams_text = generate_ngrams(normalized_text, num_ngrams=2) 
        hashed_text = generate_minHash(ngrams_text, num_hash=6)
        hashed_docs[k] = hashed_text
    
    return hashed_docs

def generate_candidates_from_bands(hashed_docs, bin_size, num_bins):

    bands = defaultdict(list)
    for path in hashed_docs.keys():
        hashed_signature = hashed_docs[path]
        
        l = 0
        r = bin_size
        while r <= len(hashed_signature):
            key = tuple(hashed_signature[l:r])
            l = r
            r += bin_size
            bands[key].append(path)
    
    s = set()
    for i in bands.values():
        s.add(tuple(i))

    s = sorted(s)

    i = 0
    while i < len(s) - 1:
        if s[i][-1] == s[i+1][0]:
            if len(s[i]) < len(s[i+1]):
                s.pop(i)
            else:
                s.pop(i + 1)
        else:
            i += 1
            
    return s



def generate_candidates_combinations(bands):
    candidate_pairs = set()
    distinct_docs = set()
    for b in bands:
        if len(b) >= 2:
            pairs_list = list(itertools.combinations(b, 2))
            for i in pairs_list:
                candidate_pairs.add(i)
        else:
            distinct_docs.add(b)
    return (candidate_pairs,distinct_docs)

docs = {
"path1": "Meet me at the pool tomorrow adad dad  dsfs fs ff s",
"path2": "Meet us at the pool tomorrow adad dad  dsfs fs ff s",
"path3": "The weather is hot today",
"path4": "Getting late for school",
"path5": "The food is great! I will definitely come back. Thank you!",
"path9": "Meet us at the party tomorrow adad dad  dsfs fs ff s a"
}

res = generate_hash(docs)
print(res)

candidates = generate_candidates_from_bands(res, bin_size=2, num_bins=3)
candidate_pairs, distinct_docs = generate_candidates_combinations(candidates)

threshold = 0.5
similar_docs = set()
for x,y in candidate_pairs:
    if jacobian_similarity(res[x],res[y]) >= threshold:
        similar_docs.add((x,y))
    else:
        distinct_docs.add(x)
        distinct_docs.add(y)

print('Distinct Docs')
for i in distinct_docs:
    print(i)
print('Similar Docs')
for i in similar_docs:
    print(i)

# TODO: Implement function for bucketing, cleanup

# for i in res2.keys():
#     print(i, res2[i])
#     print()

# combinations_of_2 = list(itertools.combinations(res2[0], 2))

# for i in combinations_of_2:
#     print(i)


# def generate_bands(hashed_docs, bin_size, num_bands):

#     bands = {}
#     for filename in hashed_docs.keys():
#         hashed_signature = hashed_docs[filename]
#         for b in range(num_bands):
#             bins = []
#             l = b*bin_size
#             r = l + bin_size  
#             val = tuple(hashed_signature[l:r])
#             if b not in bands:
#                 bands[b] = [{filename: val}]
#             else:
#                 bands[b].append({filename: val})
                
#     return bands