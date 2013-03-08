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
  
  def printSentenceWithTags(self, pos_context):
    to_print = []
    for x,y in pos_context:
      to_print.append(x)
      to_print.append("(%s)" % y)
    print " ".join(to_print)
  
  
  def pos_translate(self):
    english = self.dick_translate()
    j = 0
    for sentence in english:
      pos_context = nltk.pos_tag(sentence)
      
      edited_pos_context = []
      for i in xrange(len(pos_context) - 1):
        
        to_append = None
        # rule 1 of 10 - remove multiple adverbs in a row
        if pos_context[i][1] != "RB" or pos_context[i+1][1] != "RB":
          to_append = pos_context[i]
        # rule 2
        # if pos_context[i][1] == "VB" and re.match("to .{1,}", pos_context[i][0]):
          # to_append = (pos_context[i][0][3:], pos_context[i][1])
        if to_append:
          edited_pos_context.append(to_append)

      edited_pos_context.append(pos_context[-1])
    
      # print " ".join([y for x,y in edited_pos_context])
      
      print
      print "SPANISH"
      print 
      print self.text[j]
      j += 1
      print
      
      self.printSentenceWithTags(edited_pos_context)
      print
      print " ".join([x for x,y in edited_pos_context])
      print "pos:"
      print "\t%s" % edited_pos_context 
      print

    
  
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
          translated_words = self.dictionary[word.lower()]
          for word in translated_words.split():
            sentence.append(word)
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