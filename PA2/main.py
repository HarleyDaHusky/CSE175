#
# main.py
#
# This script provides a top-level driver to exercise a knowledge base
# concerning a midnight murder by monsters. General knowledge is
# imported from the "knowledge.py" file. A specific murder case is
# encoded in the definite clauses in "case_sentences". General
# knowledge is concatenated with case knowledge to produce a
# first-order logic knowledge base, consisting only of definite
# clauses. The driver asks a backward chaining inference procedure
# to indicate which individuals can be proven to have participated
# in the death of innocent victims.
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# David Noelle - Fri Oct 21 20:29:34 PDT 2022
#


import sys
from logic import *
from knowledge import *


# Bob is dead.
# Celene and Wanda were at the crime scene.
# Bob's body is intact but cold, and his skin complexion is pale.

case_sentences = ['Dead(Bob)',
                  'Present(Celene)',
                  'Present(Wanda)',
                  'Intact(Bob)',
                  'Cold(Bob)',
                  'Complexion(Bob, Pale)']

murder_kb = FolKB(map(expr, (monster_sentences + case_sentences)))


def main():
    print("MURDER AT MIDNIGHT BY MONSTERS")
    print("Who can be proven to have contributed to this dastardly deed?")
    # Construct the query expression ...
    q = expr('Killed(killer, victim)')
    # Record variables that appear in the query ...
    all_vars = variables(q)
    # Perform backward chaining inference ...
    answers = fol_bc_ask(murder_kb, q)
    # Clean up the results ...
    pretty_answers = sorted([pretty(dict((var, val) for var, val in a.items()
                                         if var in all_vars))
                             for a in answers],
                            key=repr)
    # Output the result ...
    print(pretty_answers)
    print("MYSTERY SOLVED")
    sys.exit(0)


# In PyCharm, press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
