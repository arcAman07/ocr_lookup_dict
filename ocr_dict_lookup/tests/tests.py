import time
import os
from PIL import Image
from ocr import extract_text_from_image
from word_meaning import extract_highlighted_words, get_word_meanings, write_word_meanings
import unittest
import os
from PIL import Image
from ocr import extract_text_from_image
from word_meaning import extract_highlighted_words, get_word_meanings, write_word_meanings


# Unit tests for extract_highlighted_words
def test_extract_highlighted_words():
    assert extract_highlighted_words('test_image1.jpg') == ['word1', 'word2', 'word3']
    assert extract_highlighted_words('test_image2.jpg') == ['word4', 'word5']

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


class TestOCRAndWordMeaning(unittest.TestCase):

    def setUp(self):
        self.test_image_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
        self.test_output_file = os.path.join(os.path.dirname(__file__), 'test_output.csv')
        self.highlighted_words = ['python', 'code', 'programming']
    
    def tearDown(self):
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)

    def test_integration(self):
        # Test OCR and word meaning extraction functionality
        image = Image.open(self.test_image_path)
        ocr_text = extract_text_from_image(image)
        highlighted_words = extract_highlighted_words(ocr_text, self.highlighted_words)
        write_word_meanings(highlighted_words, self.test_output_file)
        self.assertTrue(os.path.exists(self.test_output_file))
        
        # Verify the results
        with open(self.test_output_file) as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 4)
            self.assertIn('python', lines[1])
            self.assertIn('code', lines[2])
            self.assertIn('programming', lines[3])

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
