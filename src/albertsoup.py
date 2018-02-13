'''Main Function Runner'''

from core.albertbowl import SoupBowl

# test
bowl = SoupBowl()
bowl.serve('https://bitcointalk.org/index.php?topic=2889704.0;all')

bowl.get('#bodyarea')
bowl.get('.smalltext')
bowl.get('tastysoup')
