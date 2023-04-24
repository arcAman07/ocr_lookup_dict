from ocr_dict_lookup import extract_highlighted_words, get_word_meanings, write_word_meanings

# Compare this snippet from ocr_dict_lookup/ocr_dict_lookup.py:

image_path = "/Users/deepaksharma/Documents/Languages/Python/ocr_dict_lookup/images/IMG_0025.PNG"

words = extract_highlighted_words(image_path)
print(words)