from fasttext import load_model
from html_to_text import read_warc_file, extract_text_from_html_bytes

model = load_model('/home/tanmay/Desktop/python-projects/stanford_course/lid.176.bin')

def identify_language(text):
    text = text.replace('\n', ' ')
    res = model.predict(text, k=1)
    res = ([res[0][0].removeprefix('__label__'), res[1][0]])
    return res

records = read_warc_file()

for record in records:
    text = extract_text_from_html_bytes(record.reader.read())
    print(identify_language(text), '\n', text[:20], '\n', record.record_id)
    # Compare the language results with WET file