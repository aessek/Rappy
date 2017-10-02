from Rappy import Rappy
from pprint import pprint

with open('rappy/example/output.html', 'w') as f:
    Rappy = Rappy('rappy/cmudict-0.7b')
    Rappy.get_syllables('ride')

    colors = Rappy.colorize('rappy/example/rap.txt', min_h = 50, max_h = 50, min_s = 90, min_v = 50, max_v = 60)
    # pprint(colors)
    f.write(Rappy.out_html('rappy/example/rap.txt', colors))