import time
import os
from PIL import Image
import unittest
from ocr_dict_lookup import extract_highlighted_words, get_word_meanings, write_word_meanings

image_path_1 = "../images/IMG_0023.PNG"
image_path_2 = "../images/IMG_0024.PNG"
image_path_3 = "../images/IMG_0025.PNG"

# Unit tests for extract_highlighted_words
def test_extract_highlighted_words():
    assert extract_highlighted_words(image_path_1) == ['prioritized', 'performance', 'interpretation', 'forecasting', 'computational', 'problematic']
    assert extract_highlighted_words(image_path_3) == ['distribution', 'improvement', 'precision', 'distribution', 'modification', 'intuition', 'BatchNorm']

# Unit tests for get_word_meanings
def test_get_word_meanings():
    assert get_word_meanings('word1') == {'noun': {'definition': 'definition1', 'example': 'example1'}}
    assert get_word_meanings('word2') == {'verb': {'definition': 'definition2', 'example': 'example2'},
                                          'noun': {'definition': 'definition3', 'example': 'example3'}}

# Unit test for writing word meanings to file
def test_write_word_meanings():
    highlighted_words = ['word1', 'word2']
    with open('word_meanings.csv', 'w', newline='') as csvfile:
        fieldnames = ['Word', 'Part of Speech', 'Definition', 'Example']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for word in highlighted_words:
            meanings = get_word_meanings(word)
            for part_of_speech, meaning in meanings.items():
                writer.writerow({'Word': word, 'Part of Speech': part_of_speech,
                                  'Definition': meaning['definition'], 'Example': meaning['example']})


def test_performance(image_path, highlighted_words):
    image = Image.open(image_path)

    # Test OCR processing time
    start_time = time.time()
    ocr_text = extract_text_from_image(image)
    end_time = time.time()
    print(f"OCR processing time: {end_time - start_time:.4f} seconds")

    # Test highlighted words extraction processing time
    start_time = time.time()
    highlighted_words = extract_highlighted_words(ocr_text, highlighted_words)
    end_time = time.time()
    print(f"Highlighted words extraction processing time: {end_time - start_time:.4f} seconds")

    # Test word meaning extraction processing time
    start_time = time.time()
    for word in highlighted_words:
        get_word_meanings(word)
    end_time = time.time()
    print(f"Word meaning extraction processing time: {end_time - start_time:.4f} seconds")

    # Test write to file processing time
    test_output_file = os.path.join(os.path.dirname(__file__), 'test_output.csv')
    start_time = time.time()
    write_word_meanings(highlighted_words, test_output_file)
    end_time = time.time()
    print(f"Write to file processing time: {end_time - start_time:.4f} seconds")

words = extract_highlighted_words(image_path_1)
print(words)