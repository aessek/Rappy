from Rappy import Rappy

Rappy = Rappy('rappy/cmudict-0.7b')
Rappy.get_syllables('ride')
print(Rappy.colorize('rappy/example/rap.txt'))