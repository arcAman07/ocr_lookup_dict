import cv2 
import numpy as np
import pytesseract
import re
import requests
import csv

image_path = "/Users/deepaksharma/Documents/Languages/Python/ocr_dict_lookup/IMG_0023.PNG"

# Extract Highlighted Words
def extract_highlighted_words(image_filename):
    # Load the image
    img = cv2.imread(image_filename)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define a range of yellow color in HSV
    lower_yellow = (20, 100, 100)
    upper_yellow = (30, 255, 255)

    # Threshold the image to get the yellow regions
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Extract the text from each contour
    highlighted_words = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = img[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi)
        highlighted_words.extend(text.split())

    # Return the highlighted words
    return highlighted_words

# Word Meanings Retrieval => Just for searching up!
def get_word_meanings(word):
  url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"
  response = requests.get(url + word)
  if response.status_code != 200:
      raise ValueError('Error retrieving word meanings')
  data = response.json()[0]
  meanings = data['meanings']
  word_meanings = {}
  for meaning in meanings:
      definition = meaning['definitions'][0]['definition']
      example = meaning['definitions'][0]['example']
      word_meanings[meaning['partOfSpeech']] = {'definition': definition, 'example': example}
  return word_meanings

# Deals with the entire process of looking up the meanings of the words and writing them to a file
def write_word_meanings(words, filename):
    # Create or open the output file for writing
    with open(filename, 'a') as file:
        # Loop over each word and look up its meaning using the API
        for word in words:
            url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
            response = requests.get(url)
            if response.status_code == 200:
                # Extract the meaning from the API response and write to the file
                meaning = response.json()[0]['meanings'][0]['definitions'][0]['definition']
                file.write(f'{word}: {meaning}\n')
            else:
                file.write(f'{word}: Error - Word not found in dictionary\n')


# Print the highlighted words
highlighted_words = extract_highlighted_words(image_path)
write_word_meanings(highlighted_words, 'word_meanings.txt')
print(highlighted_words)
