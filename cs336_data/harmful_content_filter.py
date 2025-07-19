from fasttext import load_model
from cs336_data.html_to_text import read_warc_file, extract_text_from_html_bytes

hatespeech_model = load_model('/home/tanmay/Desktop/python-projects/stanford_course/jigsaw_fasttext_bigrams_hatespeech_final.bin')
nsfw_model = load_model('/home/tanmay/Desktop/python-projects/stanford_course/jigsaw_fasttext_bigrams_nsfw_final.bin')

def classify_nsfw(text: str) -> tuple[str, float]:
    text = text.replace('\n', ' ')
    res = nsfw_model.predict(text)
    res = ([res[0][0].removeprefix('__label__'), res[1][0]])
    return res

def classify_toxic_speech(text: str) -> tuple[str, float]:
    text = text.replace('\n', ' ')
    res = hatespeech_model.predict(text)
    res = ([res[0][0].removeprefix('__label__'), res[1][0]])
    return res

records = read_warc_file(limit=10000)


nsfw = 0
toxic = 0
separator = "\n" + "-" * 80 + "\n"

for record in records:
    text = extract_text_from_html_bytes(record.reader.read())

    if classify_nsfw(text)[0] == 'nsfw':
        nsfw += 1
        with open("nsfw.txt", "a", encoding="utf-8") as f:
            f.write("NSFW text:\n")
            f.write(text + separator)

    if classify_toxic_speech(text)[0] == 'toxic':
        toxic += 1
        with open("toxic.txt", "a", encoding="utf-8") as f:
            f.write("Toxic text:\n")
            f.write(text + separator)