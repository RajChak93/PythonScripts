import random

grammar = dict(  # A grammar for a trivial subset of English.
    S=[['NP', 'VP']],
    NP=[['Art', 'Adj', 'N']],
    VP=[['V', 'NP']],
    Art=['the'],
    Adj = ['hunglyy','nerdy','cute','handsome'],
    N=['CheeChee', 'Poppins', 'Mommy', 'toys', 'potty machine','foodie','Babu Guda'],
    V=['ate', 'liked', 'killed', 'smelled','pooped on','farted on'])


def generate(phrase):
    "Generate a random sentence or phrase"
    if isinstance(phrase, list):
        return mappend(generate, phrase)
    elif phrase in grammar:
        return generate(random.choice(grammar[phrase]))
    else:
        return [phrase]


def generate_tree(phrase):
    """Generate a random sentence or phrase,
     with a complete parse tree."""
    if isinstance(phrase, list):
        return map(generate_tree, phrase)
    elif phrase in grammar:
        return [phrase] + generate_tree(random.choice(grammar[phrase]))
    else:
        return [phrase]


def mappend(fn, iterable):
    """Append the results of calling fn on each element of iterbale.
    Like iterools.chain.from_iterable."""
    return sum(map(fn, iterable), [])