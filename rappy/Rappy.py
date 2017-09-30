import re
import colored

class Rappy:
    def __init__(self, dictionary_file):
        '''
        Creating a new object from a dictionary file will scan that dictionary
        and convert it to a python dict for easier use when searching for words.
        '''
        self.dictionary_file = dictionary_file
        self.dictionary_file = open(self.dictionary_file, 'r')

        self.dictionary = {}

        for line in self.dictionary_file:
            words = line.split()
            val = []

            for i in range(len(words)):
                if(i is not 0):
                    val.append(words[i])

            self.dictionary[words[0]] = val

    def get_syllables(self, word):
        '''
        Attempts to look the word up in the dictionary and return a tuple of
        the input word and the accompanying syllables from the dictionary. 
        Uses Regex.
        '''       
        try:
            syllables = self.dictionary[self.prepare_word(word)]
            return word, syllables
        except:
            return word, False

    def prepare_word(self, word):
        '''
        Remove invalid characters from the word and convert it to uppercase to
        match the dictionary. 
        '''
        return re.sub(',.;!', '', word).upper()

    def colorize(self, lyric_file):
        '''
        Find matching words in the lyric_file and assign them the same color value. Uses the
        "colored" package.
        '''
        with open(lyric_file, 'r') as f:
            color_key = {}
            color_id = 1
            data = re.findall(r'\S+|\n', f.read())

            for i in range(len(data)):
                prepared_word = self.prepare_word(data[i])
                orig_word, syllables = self.get_syllables(prepared_word)

                if prepared_word is '\n':
                    print(prepared_word)
                elif prepared_word not in color_key:
                    color_key[prepared_word] = color_id
                    color_id = color_id + 1 % 256

                color = colored.fg(0) + colored.bg(color_key[prepared_word])
                out = "{}{}{}".format(color, orig_word, colored.attr(0))
                print(out, end=' ')