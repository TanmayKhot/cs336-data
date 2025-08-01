
#if __name__ == "__main__":
#cs336_data
from cs336_data.html_to_text import read_warc_file, extract_text_from_html_bytes
from cs336_data.language_identification import identify_language
from cs336_data.mask_pii import *
from cs336_data.harmful_content_filter import *
from cs336_data.quality_check import *
import re
import fasttext
import random

def mask_pii(text):
    text = mask_emails(text)[0]
    text = mask_phone_numbers(text)[0]
    text = mask_ips(text)[0]
    return text

def data_quality_label(text):
    
    '''
    Returns 1 line string output with the quality label followed by the pre processed text
    '''
    
    text = re.sub(r'\s+', ' ', text)
    text = mask_pii(text)

    lowlabel = '__label__low ' + text
    highlabel = '__label__high ' + text
    
    if not gopher_quality_filter(text):
        return lowlabel
    if identify_language(text)[0] != 'en' and identify_language(text)[1] < 0.85:
        return lowlabel
    if classify_nsfw(text)[0] == 'nsfw' and classify_nsfw(text)[1] > 0.85:
        return lowlabel
    if classify_toxic_speech(text)[0] == 'toxic' and classify_nsfw(text)[1] > 0.85:
        return lowlabel
    
    return highlabel
        

def prep_training_data():
    i = 0
    l = 0
    h = 0
    wiki = '/home/tanmay/Desktop/python-projects/stanford_course/first_10000_wiki.warc.warc.gz'
    records = read_warc_file(path=wiki, limit=10000)
    with open('data2.txt', 'a', encoding='utf-8') as f:
        for record in records:
            text = extract_text_from_html_bytes(record.reader.read())
            text = re.sub(r'\s+', ' ', text)
            #label = data_quality_label(text)+'\n'
            label = '__label__high ' + text + '\n'
            f.write(label)
            if label[9:12]== 'low':
                l += 1
            elif label[9:12]== 'hig':
                h += 1
    
    records = read_warc_file(limit=10000)
    with open('data2.txt', 'a', encoding='utf-8') as f:
        for record in records:
            text = extract_text_from_html_bytes(record.reader.read())
            text = re.sub(r'\s+', ' ', text)
            #label = data_quality_label(text)+'\n'
            label = '__label__low ' + text + '\n'
            f.write(label)
            if label[9:12]== 'low':
                l += 1
            elif label[9:12]== 'hig':
                h += 1

    print(f"Total Low quality: {l} High quality {h}")


def split_data(input_file='data2.txt', train_file='data2.train', valid_file='data2.valid', train_ratio=0.8):
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    random.shuffle(lines)
    
    split_point = int(len(lines) * train_ratio)
    
    train_lines = lines[:split_point]
    valid_lines = lines[split_point:]
    
    with open(train_file, 'w', encoding='utf-8') as f:
        f.writelines(train_lines)
    
    with open(valid_file, 'w', encoding='utf-8') as f:
        f.writelines(valid_lines)

    print("Training and Validation datasets are ready")

def train_model(dataset_path):

    model = fasttext.train_supervised(input=dataset_path, lr=1, epoch=50,wordNgrams=2)
    print(model.test("/home/tanmay/Desktop/python-projects/stanford_course/cs336/cs336_data/data2.valid"))
    model.save_model("/home/tanmay/Desktop/python-projects/stanford_course/cs336/cs336_data/model_quality_classifier2.bin")
    
#prep_training_data()
#split_data()
#train_model('data.train')

def classify(text):
    print("running...")
    text = re.sub(r'\s+', ' ', text)
    model = fasttext.load_model("/home/tanmay/Desktop/python-projects/stanford_course/cs336/cs336_data/model_quality_classifier2.bin")
    res = model.predict(text)
    return (res[0][0].removeprefix("__label__"), res[1][0])
