from Rappy import Rappy
from pprint import pprint

with open('rappy/example/output.html', 'w') as f:
    Rappy = Rappy('rappy/cmudict-0.7b')
    Rappy.get_syllables('ride')
    colors = Rappy.colorize('rappy/example/rap.txt')
    # pprint(colors)
    f.write(Rappy.out_html('rappy/example/rap.txt', colors))