import sys

class Verb:
  def __init__(self, verb, meaning, conjugations):
    assert(len(conjugations) == 6)
    self.verb = verb
    self.meaning = meaning
    self.conjugations = conjugations
    
  def __repr__(self):
    return "{}[{}]".format(self.verb, self.meaning)

class Noun:
  def __init__(self, noun, translation, gender, plural):
    self.noun = noun
    self.translation = translation
    self.gender = gender
    self.plural = plural
    
    assert gender == 'm' or gender == 'f', \
           'Bad noun gender: {}:{}'.format(noun, gender)
  
  def __repr__(self):
    return '{}[{}] ({}.)'.format(self.noun, self.translation, self.gender)
    
    
def main():
  files = sys.argv[1:]
  vocab = {'verbs': [], 'nouns': []}
  parseFiles(vocab, files)
  
  for v in vocab['verbs']:
    print(v)
   
  for n in vocab['nouns']:
    print(n)
  
def parseFiles(vocab, files):
  print('Loading files: {}'.format(files))
  for filename in files:
    with open(filename, 'r') as f:
      line = f.readline()
      while line != '':
        # Skip newlines
        if line == '\n':
          line = f.readline()
          continue
        
        # Parse verbs if the line is a v, noun if it's an n
        line = line.strip()
        if line == 'v':
          parseVerb(vocab['verbs'], f)
        elif line == 'n':
          parseNoun(vocab['nouns'], f)
        else:
          assert False, 'Got indicator line: {}'.format(line)
        
        # Get next indicator
        line = f.readline()

def parseVerb(verbs, file):
  verb, meaning = file.readline().strip().split(':')
  
  conjugations = []
  for i in range(6):
    line = file.readline().strip()
    assert line != '', 'LINE WAS EMPTY? {}:"{}"'.format(verb, line)
    conjugations.append(line)
  
  verbs.append(Verb(verb, meaning, conjugations))
 
def parseNoun(nouns, file):
  data = file.readline().strip().split(':')
  assert len(data) == 4, 'Noun data size mismatch: {}'.format(data)
  nouns.append(Noun(*data))

if __name__ == '__main__':
  main()
