import csv, re, nltk
import pdb

class Translator:
  def __init__(self, spanish_filename, dict_filename):
    self.text = self.readFile(spanish_filename)
    self.dictionary = self.readDictionary(dict_filename)
  
  def readFile(self, filename):  
    with open(filename, "rb") as file:
      sentences = [line for line in file]
    return sentences

  def readDictionary(self, filename):
    dict = {}
    with open(filename, "rb") as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      for row in reader:
        dict[row[0].lower()] = row[1].lower()
    return dict
  
  def pos_translate(self):
    english = self.dick_translate()
    for sentence in english:
      print nltk.pos_tag(sentence)
    
  
  def dick_translate(self):
    sentences = []
    for line in self.text:
      tokenizer = nltk.PunktWordTokenizer()
      words = tokenizer.tokenize(line)      
      
      sentence = []
      for word in words:
        appendPeriod = False
        if word[-1] == ".":
          word = word[0:len(word)-1]
          appendPeriod = True
        
        if word.lower() in self.dictionary:
          sentence.append(self.dictionary[word.lower()])
        else:
          sentence.append(word)
          
        if appendPeriod:
          sentence.append(".")
      sentences.append(sentence)
    return sentences
     
      
if __name__ == '__main__':
    spanish_file = "./data/Spanish.txt"
    dictionary_file = "./data/Dictionary.csv"
    translator = Translator(spanish_file, dictionary_file)
    translator.pos_translate()