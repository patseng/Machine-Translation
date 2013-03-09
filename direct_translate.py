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
      
      for i in range(len(pos_context)):
        # rule 8 if indirect object precedes a verb
        if pos_context[i][0] == "him" and "VB" in pos_context[i+1][1]:
          tmp = pos_context[i]
          pos_context[i] = pos_context[i+1]
          pos_context[i+1] = tmp
      
      
      edited_pos_context = []
      skipThisRound = False
      for i in range(0, len(pos_context) - 1, 1):
        if skipThisRound:
          skipThisRound = False
          continue
        to_append = pos_context[i]
        
        # rule 5 - No obstante -> not nevertheless
        if pos_context[i][0].lower() == "not" and pos_context[i+1][0] == "nevertheless":
          continue
          
        # rule 6 - deal with passive voice
        if i < len(pos_context) - 2 and pos_context[i][0].lower() == "his" and pos_context[i+1][0].lower() == "own" and "VB" in pos_context[i+2][1]:
          to_append = ("it", "NN")
          skipThisRound = True
          
        # rule 12 - removal of a determiner followed by a wh-determiner such as "the that"
        if pos_context[i][1] == "DT" and pos_context[i+1][1] == "WDT":
          continue
          
        # rule 2 - remove 'to' after modal word
        if pos_context[i][1] == "MD" and pos_context[i+1][1] == "TO":
          skipThisRound = True
          
        # rule 3 - remove preposition before 'to'
        if pos_context[i][1] == "IN" and pos_context[i+1][1] == "TO":
          continue
        
        # rule 4 - bad rule?
        if pos_context[i][1] == "IN" and pos_context[i][0].lower() != "because" and pos_context[i+1][1] == "IN":
          continue
        
        # rule 9 - Sin Embargo phrase catching
        if pos_context[i][0] == "without" and pos_context[i+1][0] == "confiscate":
          to_append = ("nevertheless", 'RB')
          skipThisRound = True
        
        # rule 10 - In fact phrase catching
        if pos_context[i][0] == "of" and pos_context[i+1][0] == "done":
          edited_pos_context.append(("in", "IN"))
          to_append = ("fact", "NN")
          skipThisRound = True

        if to_append:
          edited_pos_context.append(to_append)
      edited_pos_context.append(pos_context[-1])
      
      for i in xrange(len(edited_pos_context) - 1):
        # rule 1 - reverse order of nouns and modifying adjectives
        if "NN" in edited_pos_context[i][1] and edited_pos_context[i+1][1] == "JJ":
          tmp = edited_pos_context[i]
          edited_pos_context[i] = edited_pos_context[i+1]
          edited_pos_context[i+1] = tmp
          
        # rule 11 - remove 'se' that are between noun and verb
        if i < len(edited_pos_context) - 2 and "NN" in edited_pos_context[i][1] and "VB" in edited_pos_context[i+2][1] and edited_pos_context[i+1][0] == "it":
          edited_pos_context[i+1] = ("","")
        
        # rule 7 - negation
        if edited_pos_context[i][0].lower() == "not" and edited_pos_context[i+1][1] == "NN":
          tmp = edited_pos_context[i]
          edited_pos_context[i] = edited_pos_context[i+1]
          edited_pos_context[i+1] = tmp
          
        # rule 13 - it not VB NN
        if i < len(edited_pos_context) - 2 and edited_pos_context[i][0].lower() == 'it' and edited_pos_context[i+1][0].lower() == 'not' and "VB" in edited_pos_context[i+2][1]:
          edited_pos_context[i+1] = ("wasn't", "RB")
        
        # rule 14 - it wasn't VB DT NN
        if i < len(edited_pos_context) - 4 and edited_pos_context[i][0].lower() == 'it' and edited_pos_context[i+1][0].lower() == "wasn't" and "VB" in edited_pos_context[i+2][1] and "DT" in edited_pos_context[i+3][1] and "NN" in edited_pos_context[i+4][1]:
          edited_pos_context[i] = edited_pos_context[i+3]
          edited_pos_context[i+3] = edited_pos_context[i+2]
          edited_pos_context[i+2] = edited_pos_context[i+1]
          edited_pos_context[i+1] = edited_pos_context[i+4]
          edited_pos_context[i+4] = ('', '')

    
      # print " ".join([y for x,y in edited_pos_context])
      
      # print
      # print "SPANISH"
      # print 
      # print self.text[j]
      # j += 1
      # print
      
      # self.printSentenceWithTags(edited_pos_context)
      print " ".join([x for x,y in edited_pos_context])
      # print
      # self.printSentenceWithTags(edited_pos_context)
      # print

    
  
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