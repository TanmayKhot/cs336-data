import nltk
# nltk.download('punkt')
# nltk.download('punkt_tab')
import re

def gopher_quality_filter(text: str) -> bool:

    # Number of words check
    words = nltk.word_tokenize(text)
    n_words = len(words)
    if n_words < 50 or n_words > 100000:
        return False

    # Average word length check
    avg_word = sum(len(w) for w in words) / n_words
    if avg_word < 3 or avg_word > 10:
        return False
    
    # Number of lines ending with ellipsis check
    ellipsis = 0
    if text.split().endswith('...'):
        ellipsis += 1
    if ellipsis/len(text.split()) > 0.3:
        return False

    # Non alpha check
    non_alpha = 0
    for i in words:
        if not bool(re.search('[a-zA-Z]', i)):
            non_alpha += 1
    if non_alpha/n_words > 0.8:
        return False
    
    return True

