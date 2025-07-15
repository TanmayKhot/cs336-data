from resiliparse.extract.html2text import extract_plain_text
from resiliparse.parse.encoding import detect_encoding
from resiliparse.parse.encoding import bytes_to_str

def run_extract_text_from_html_bytes(html_bytes: bytes) -> str | None:
    decoded = bytes_to_str(html_bytes, detect_encoding(html_bytes))
    text = extract_plain_text(decoded)
    return text

html = '<html><body><h1>Hello, World!</h1></body></html>'
html = '''
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
html_bytes = html.encode("utf-8")
res = run_extract_text_from_html_bytes(html_bytes)
print(res)

'''
print(detect_encoding(html_bytes))
x = bytes_to_str(html_bytes)
print(x)
'''