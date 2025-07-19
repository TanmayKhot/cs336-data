import re
from html_to_text import read_warc_file, extract_text_from_html_bytes
from language_identification import identify_language

def mask_emails(text: str) -> tuple[str, int]:
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_replacement = '|||EMAIL_ADDRESS|||'
    res, counts = re.subn(email_pattern, email_replacement, text)
    return (res, counts)

def mask_phone_numbers(text: str) -> tuple[str, int]:
    phone_patterns = (
        r'\+1\s+\d{3}-\d{3}-\d{4}|'
        r'\+1\s+\d{10}|'
        r'\+1\s+\d{3}\.\d{3}\.\d{4}|'
        r'\+1\d{10}|'
        r'\b\d{3}-\d{3}-\d{4}\b|'
        r'\b\d{10}\b|'
        r'\b\d{3}\.\d{3}\.\d{4}\b|'
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    )

    phone_replacement = '|||PHONE_NUMBER|||'
    res, counts = re.subn(phone_patterns, phone_replacement, text)
    return (res,counts)

def mask_ips(text: str) -> tuple[str, int]:
    ipv4_pattern = r'\b(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.' \
                r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.' \
                r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.' \
                r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b'
    ipv4_replacement = '|||IP_ADDRESS|||'
    res, counts = re.subn(ipv4_pattern, ipv4_replacement, text)
    return (res,counts)

records = read_warc_file(limit=50)

for record in records:
    text = extract_text_from_html_bytes(record.reader.read())
    if identify_language(text)[0] == 'en':
        res, ne = mask_phone_numbers(text)
        res, np = mask_emails(res)
        res, nip = mask_ips(res)
        if ne + np + nip > 0:
            print("Original text:\n", text, "\n\nPII Masked text\n", res)
    