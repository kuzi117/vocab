import sys
from random import choice

_vowels = 'aeéèiou'

class Verb:
  def __init__(self, verb, meaning, conjugations):
    assert(len(conjugations) == 6)
    self.verb = verb
    self.meaning = meaning
    self.conjugations = conjugations

  def __repr__(self):
    return "{}[{}]".format(self.verb, self.meaning)

class Noun:
  def __init__(self, noun, translation, gender, pluralFR, pluralEN, \
               genderedNoun):
    self.noun = noun
    self.translation = translation
    self.gender = gender
    self.pluralFR = pluralFR
    self.pluralEN = pluralEN
    self.genderedNoun = genderedNoun

    assert gender == 'm' or gender == 'f', \
           'Bad noun gender: {}:{}'.format(noun, gender)

  def __repr__(self):
    return '{}[{}] ({}.)'.format(self.noun, self.translation, self.gender)

  def toFRString(self, definite, plural):
    if definite:
      if plural:
        return 'les ' + self.pluralFR
      elif self.noun[0] in _vowels:
        return 'l\'' + self.noun
      elif self.gender == 'm':
          return 'le ' + self.noun
      else:
          return 'la ' + self.noun
    else:
      if plural:
        return 'des ' + self.pluralFR
      elif self.gender == 'm':
        return 'un ' + self.noun
      else:
        return 'une ' + self.noun

  def toENString(self, definite, plural):
    rv = ''
    if plural:
      if definite:
        rv = 'the ' + self.pluralEN
      else:
        rv = self.pluralEN
    else:
      if definite:
        rv = 'the ' + self.translation
      else:
        article = ''
        if self.translation[0] in _vowels:
          article = 'an'
        else:
          article = 'a'

        rv = article + ' ' + self.translation

    if self.genderedNoun:
      rv += ' ({}.)'.format(self.gender)

    return rv

def main():
  files = sys.argv[1:]
  vocab = {'verbs': [], 'nouns': []}
  parseFiles(vocab, files)

  print('Loaded {} verbs and {} nouns'\
        .format(len(vocab['verbs']), len(vocab['nouns'])))

  for noun in vocab['nouns']:
    print(noun)

  askQuestions(vocab)

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
        elif line == 'ng':
          parseNoun(vocab['nouns'], f, True)
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

def parseNoun(nouns, file, genderedNoun=False):
  data = file.readline().strip().split(':')
  assert len(data) == 5, 'Noun data size mismatch: {}'.format(data)
  nouns.append(Noun(*data, genderedNoun))

def askQuestions(vocab):
  qfs = []

  if len(vocab['nouns']) > 0:
    qfs.append(askFRToENNoun)
    qfs.append(askFRtoENPluralNoun)
    qfs.append(askENToFRNoun)
    qfs.append(askENToFRPluralNoun)

  if len(vocab['verbs']) > 0:
    qfs.append(askVerb)

  if not qfs:
    return

  # We've done set up.. just ask questions forever
  asked = 0
  correct = 0
  try:
    while True:
      right = choice(qfs)(vocab)
      asked += 1
      if right:
        correct += 1
  except KeyboardInterrupt:
    print("\nStats: {}/{} questions correct".format(correct, asked))

def askFRToENNoun(vocab):
  nouns = vocab['nouns']
  noun = choice(nouns)
  definite = choice((True, False))
  ans = input(noun.toFRString(definite, False) + ': ')
  enStr = noun.toENString(definite, False)
  if ans == enStr:
    return True
  else:
    print('--> ' + enStr)
    return False

def askFRtoENPluralNoun(vocab):
  nouns = vocab['nouns']
  noun = choice(nouns)
  definite = choice((True, False))
  ans = input(noun.toFRString(definite, True) + ': ')
  enStr = noun.toENString(definite, True)
  if ans == enStr:
    return True
  else:
    print('--> ' + enStr)
    return False

def askENToFRNoun(vocab):
  nouns = vocab['nouns']
  noun = choice(nouns)
  definite = choice((True, False))
  ans = input(noun.toENString(definite, False) + ': ')
  frStr = noun.toFRString(definite, False)
  if ans == frStr:
    return True
  else:
    print('--> ' + frStr)
    return False

def askENToFRPluralNoun(vocab):
  nouns = vocab['nouns']
  noun = choice(nouns)
  definite = choice((True, False))
  ans = input(noun.toENString(definite, True) + ': ')
  frStr = noun.toFRString(definite, True)
  if ans == frStr:
    return True
  else:
    print('--> ' + frStr)
    return False

def askVerb(vocab):
  pass

if __name__ == '__main__':
  main()
