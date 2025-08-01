from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import detect_encoding
from resiliparse.parse.encoding import bytes_to_str
from fastwarc.warc import ArchiveIterator

def extract_text_from_html_bytes(html_bytes: bytes) -> str | None:
    decoded = bytes_to_str(html_bytes, detect_encoding(html_bytes))
    text = extract_plain_text(decoded)
    return text

def encode_html(html, encoding):
    return html.encode(encoding)
    
# Manual HTML input
test_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>UTF-8 Demo</title>
</head>
<body>
  <h1>Welcome! 🎉</h1>
  <p>This page supports UTF-8 characters like:</p>
  <ul>
    <li>Emojis: 😀 👍 ❤️</li>
    <li>Currency symbols: € ¥ ₹</li>
    <li>Math symbols: ∑ ∞ ≈</li>
    <li>Non-Latin text: こんにちは, नमस्ते, مرحبا</li>
  </ul>
</body>
</html>
'''
res = extract_text_from_html_bytes(encode_html(test_html, "utf-8"))

# Reading contents from WARC file
path_commonCrawl = '/home/tanmay/Desktop/python-projects/stanford_course/CC-MAIN-20250417135010-20250417165010-00065.warc.gz'
path_wiki = '/home/tanmay/Desktop/python-projects/stanford_course/enwiki_10.warc.gz'

# <urn:uuid:95395b72-f7ac-484b-80f0-9d4f5ac4d2b6> // First English webpage found in the WARC file
target_id = '<urn:uuid:95395b72-f7ac-484b-80f0-9d4f5ac4d2b6>'

def read_warc_file(path=path_commonCrawl, target_id=None, limit=20):
    if target_id:
        for record in ArchiveIterator(open(path, 'rb')):
          if record.record_id == target_id:
              record.freeze()
              break
        return [record]
    else:
      i = 0
      res = []
      for record in ArchiveIterator(open(path, 'rb')):    
        record.freeze()      
        res.append(record)
        i += 1
        if i == limit:
            break
      return res

