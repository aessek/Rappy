import re
import colorsys
import random

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
            return word, None

    def prepare_word(self, word):
        '''
        Remove invalid characters from the word and convert it to uppercase to
        match the dictionary. 
        '''
        return re.sub('[\(\)\-\.!,\?"\']', '', word).upper()

    def colorize(self, lyric_file, min_h = 1, min_s = 1, min_v = 1, max_h = 100, max_s = 100, max_v = 100):
        '''
        Build a 'color key' which gives unique words a unique color. The color
        can be controlled by setting a min/max values for the Hue, Saturation, 
        or Value (Brightness). This number should be 0-100. 
        '''
        def get_rnd_color(pool_size):
            # Generate a new color pallete 
            # HSV = Hue, Saturation, Value/Brightness
            h_mod = round(random.randint(min_h, max_h * 10) / 1000, 2)
            s_mod = round(random.randint(min_s, max_s * 10) / 1000, 2)
            v_mod = round(random.randint(min_v, max_v * 10) / 1000, 2)

            hsv = [(h_mod, s_mod, v_mod) for x in range(1, pool_size)]
            rgb = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv))
            color = [round(v * 255) for v in rgb[round(random.randint(0, len(rgb) - 1))]]

            return '{}, {}, {}'.format(*color)

        with open(lyric_file, 'r') as f:
            color_key = {}
            used_colors = list()
            data = re.findall(r'\S+|\n', f.read())
            
            for i in range(len(data)):
                orig_word, syllables = self.get_syllables(data[i])
                prepared_word = self.prepare_word(orig_word)

                if prepared_word not in color_key:
                    if orig_word is '\n':
                        color = None
                    else:
                        color = get_rnd_color(len(data))
                        while color in used_colors:
                            color = get_rnd_color(len(data))
                        
                        used_colors.append(color)
            
                    color_key[prepared_word] = { 
                        'original_word': orig_word,
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
                    background: #252525;
                    font-family: Arial;
                    font-size: 12px;
                }

                .rhymed-word {
                    margin: 0 5px 5px 0;
                    padding: 5px;
                    display: inline-block;
                    color: #fff;
                }

                .debug { 
                    font-size: 12px;
                    color: #ddd;
                }
            </style>
        </head>
        <body>
        '''

        with open(lyric_file, 'r') as f:
            data = re.findall(r'\S+|\n', f.read())
            for i in range(len(data)):
                word = data[i]
                prepared_word = self.prepare_word(word)                
                if word is '\n':
                    html += '<br><br>'
                elif prepared_word in color_key:
                    html += '<span class="rhymed-word" style="background: rgb({});">{}<br><span class="debug">{}</span></span>'.format(color_key[prepared_word]['color'], word, color_key[prepared_word]['color'])
        
        return html