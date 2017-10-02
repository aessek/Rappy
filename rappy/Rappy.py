import re

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
            color_min = 66
            color_max = 255
            r, g, b = color_min, color_min, color_min
            data = re.findall(r'\S+|\n', f.read())

            for i in range(len(data)):
                prepared_word = self.prepare_word(data[i])
                orig_word, syllables = self.get_syllables(data[i])

                if prepared_word is '\n':
                    color = None
                elif prepared_word not in color_key:
                    if ((r or g or b) < color_max):
                        r = r + 1
                        g = g + 1
                        b = b + 1
                    elif ((r or g or b) > color_min):
                        r = r - 1
                        g = g - 1
                        b = b - 1
                    
                    color = r, g, b

                color_key[orig_word] = { 
                    'prepared_word': prepared_word,
                    'syllables': syllables,
                    'color': color
                }
            
            return color_key

    def out_html(self, lyric_file, color_key):
        html = '''
        <!doctype html>
        <head>
            <title>{}</title>
            <style>
                body {
                    font-family: Arial;
                }

                .rhymed-word {
                    margin: 0 5px 0 0;
                    padding: 5px;
                    display: inline-block;
                }
            </style>
        </head>
        <body>
        '''
        
        with open(lyric_file, 'r') as f:
            data = re.findall(r'\S+|\n', f.read())
            for i in range(len(data)):
                word = data[i]
                if word is '\n':
                    html += '<br><br>'
                elif word in color_key:
                    html += '<span class="rhymed-word" style="background: rgb{};">{}</span>'.format(color_key[word]['color'], word)
        
        return html