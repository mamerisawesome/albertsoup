'''Main Function Runner'''

from albertbowl import SoupBowl

# test
bowl = SoupBowl()
bowl.serve('https://bitcointalk.org/index.php?topic=2889704.0;all')

bowl.scoop('#bodyarea')
bowl.scoop('.smalltext')
bowl.scoop('tastysoup')
