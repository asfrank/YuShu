def is_isbn_or_key(word):
    isbn_or_key = 'key'
    short_word = word.replace('-', '')
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
