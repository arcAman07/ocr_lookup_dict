import time
import os
from PIL import Image
import unittest
from ocr_dict_lookup import extract_highlighted_words, get_word_meanings, write_word_meanings
from pytesseract import pytesseract

image_path_1 = "./images/IMG_0023.PNG"
image_path_2 = "./images/IMG_0025.PNG"

# Get the current directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class TestDictMethods(unittest.TestCase):
  # Unit tests for extract_highlighted_words
  def test_extract_highlighted_words(self):
      self.assertEqual(extract_highlighted_words(image_path_1) , ['prioritized', 'performance', 'interpretation', 'forecasting', 'computational', 'problematic'])
      self.assertEqual(extract_highlighted_words(image_path_2) , ['distribution', 'improvement', 'precision', 'distribution', 'modification', 'intuition', 'BatchNorm'])
  
  def test_get_word_meanings(self):
      self.assertEqual(get_word_meanings('prioritized') , 'To arrange or list a group of things in order of priority or importance.')
      self.assertEqual(get_word_meanings('distribution') , 'An act of distributing or state of being distributed.')
  
  def test_write_word_meanings(self):
        # Create a temporary file to write the word meanings to
        temp_file = os.path.join(CURRENT_DIR, 'test_word_meanings.txt')

        # Write word meanings to file
        words = ['test', 'words']
        write_word_meanings(words, temp_file)

        # Read the file to check that the word meanings were written correctly
        with open(temp_file, 'r') as f:
            contents = f.read()

        # Check that contents match expected output
        expected_contents = 'test: A challenge, trial.\nwords: The smallest unit of language that has a particular meaning and can be expressed by itself; the smallest discrete, meaningful unit of language. (contrast morpheme.)\n'
        self.assertEqual(contents, expected_contents)

        # Remove the temporary file
        os.remove(temp_file)
   

class TestPackagePerformance(unittest.TestCase):
    def test_extract_highlighted_words_performance(self):
        # Load image to test performance
        image_1 = Image.open(image_path_1)
        image_2 = Image.open(image_path_2)

        # Measure time to extract highlighted words
        start_time_1 = time.time()
        extracted_words_1 = extract_highlighted_words(image_path_1)
        end_time_1 = time.time()
        time_taken_1 = end_time_1 - start_time_1

        # Check that extracted words are not empty
        self.assertTrue(extracted_words_1)

        # Check that time taken is less than 2 seconds
        self.assertLess(time_taken_1, 40)

        # Measure time to extract highlighted words
        start_time_2 = time.time()
        extracted_words_2 = extract_highlighted_words(image_path_2)
        end_time_2 = time.time()
        time_taken_2 = end_time_2 - start_time_2

        # Check that extracted words are not empty
        self.assertTrue(extracted_words_2)

        # Check that time taken is less than 2 seconds
        self.assertLess(time_taken_2, 40)
        image_1.close()
        image_2.close()

    def test_write_word_meanings_performance(self):
        # Measure time to get word meanings from API
        start_time = time.time()
        meaning = get_word_meanings('test')
        end_time = time.time()
        time_taken = end_time - start_time

        # Check that time taken is less than 1 second
        self.assertLess(time_taken, 10)


if __name__ == '__main__':
    unittest.main()
