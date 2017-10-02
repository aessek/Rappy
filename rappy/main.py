from Rappy import Rappy

with open('rappy/example/output.html', 'w') as f:
    Rappy = Rappy('rappy/cmudict-0.7b')
    Rappy.get_syllables('ride')
    f.write(Rappy.out_html('rappy/example/rap.txt', Rappy.colorize('rappy/example/rap.txt')))