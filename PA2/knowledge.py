#
# knowledge.py
#
# This file contains axioms for a midnight murder by monsters knowledge base.
#
# These sentences use the following ontology.
#
#   Bob, Celene, Lin, Alberto, Maria, Wanda : constants for individuals
#   Pale, Blue, Green, Purple : constants for skin complexion colors
#
#   Bitten(x) : true iff x has been bitten
#   Boils(x) : true iff the skin of x has boils
#   Cold(x) : true iff the body of x is cold to the touch
#   Complexion(x, y) : true iff the skin of x has the complexion y
#   Dead(x) : true iff x is dead
#   Disemboweled(x) : true iff the body of x is missing internal organs
#   Dismembered(x) : true iff the body of x is missing limbs
#   Drained(x) : true iff the body of x has been drained of blood
#   Eaten(x) : true iff x has been eaten
#   Incomplete(x) : true iff the body of x is missing parts
#   Intact(x) : true iff the body of x is relatively whole and intact
#   Killed(x, y) : true iff x murdered y
#   Monster(x) : true iff x is a monster
#   Person(x) : true iff x is a person
#   Poisoned(x) : true iff x has been poisoned
#   Present(x) : true iff x was present at the crime scene
#   Punctured(x) : true iff the body of x has puncture wounds
#   Suspect(x) : true iff x is a murder suspect
#   Vampire(x) : true iff x is a vampire
#   Victim(x) : true iff x was the victim of a murder
#   Werewolf(x) : true iff x is a werewolf
#   Witch(x) : true iff x is a witch
#
# No other constants, functions, or predicates should be used in the axioms
# contained in this file. All axioms must be definite clauses.
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# PLACE ANY COMMENTS, INCLUDING ACKNOWLEDGMENTS, HERE
#
# PLACE YOUR NAME AND THE DATE HERE
#


# An Example from Russell & Norvig (2020)

# noinspection SpellCheckingInspection
crime_sentences = ['(American(x) & Weapon(y) & Sells(x, y, z) & Hostile(z)) ==> Criminal(x)',
                   'Owns(Nono, M1)',
                   'Missile(M1)',
                   '(Missile(x) & Owns(Nono, x)) ==> Sells(West, x, Nono)',
                   'Missile(x) ==> Weapon(x)',
                   'Enemy(x, America) ==> Hostile(x)',
                   'American(West)',
                   'Enemy(Nono, America)']


# Midnight Murder by Monsters Sentences

# The first-order logic definite clauses below are intended to express the
# following knowledge.
#
# Celene is a vampire.
# Alberto is a werewolf.
# Wanda is a witch.
# Bob, Lin, and Maria are people.
# A person who is dead is a victim.
# All vampires, werewolves, and witches are monsters.
# Any monster present at the crime scene is a suspect.
# If a vampire is suspected and the victim was bitten, then
#   the vampire killed the victim.
# If a werewolf is suspected and the victim was eaten, then
#   the werewolf killed the victim.
# If a witch is suspected and the victim was poisoned, then
#   the witch killed the victim.
# If a victim is drained of blood but has an intact body, then
#   the victim was bitten.
# If a victim is drained of blood and has body pieces missing (i.e., is
#   incomplete), then the victim was eaten.
# If a victim's body is intact, and the victim's skin complexion is
#   green, blue, or purple, or if it is pale with boils, then
#   the victim was poisoned.
# If a victim's skin complexion is pale and the body is either
#   cold or punctured, then the victim is drained of blood.
# If a victim's body is complete (i.e., not incomplete), then
#   it is not dismembered or disemboweled.

# PLACE YOUR FOL SENTENCES IN THIS LIST

monster_sentences = [
    #The comment(s) after is how I would read it (just for me to double check)
    'Vampire(Celene)', #Celene is a vampire
    'Werewolf(Alberto)', #Alberto is a werewolf
    'Witch(Wanda)', #Wanda is a witch
    'Person(Bob)', 'Person(Lin)', 'Person(Maria)', #Bob, Lin, Maria are people
    'Person(x) & Dead(x) ==> Victim(x)', #A person who is Dead is a victim
    'Vampire(x) ==> Monster(x)', 'Werewolf(x) ==> Monster(x)', 'Witch(x) ==> Monster(x)', #Vampire, Wolf, Witch are monsters
    'Monster(x) & Present(x) ==> Suspect(x)', #All monsters that were present are suspects
    '(Vampire(x) & Suspect(x)) & (Victim(y) & Bitten(y)) ==> Killed(x,y)', #If Vampire is a Suspect & Victim was Bitten, Vampire is the murderer
    '(Werewolf(x) & Suspect(x)) & (Victim(y) & Eaten(y)) ==> Killed(x,y)', #If Werewolf is a Suspect & Victim was Eaten, Werewolf was the murderer
    '(Witch(x) & Suspect(x)) & (Victim(y) & Poisoned(y)) ==> Killed(x,y)', #If Witch is a Suspect & Victim was Poisoned, Witch was the murderer
    '(Victim(x) & Drained(x)) & Intact(x) ==> Bitten(x)', #If Victim is Drained and Intact, they were Bitten
    '(Victim(x) & Drained(x)) & Incomplete(x) ==> Eaten(x)', #If Victim is Drained and Incomplete, they were eaten
    #'Victim(x) & Intact(x) & (Complexion(x, Green) | Complexion(x, Blue) | Complexion(x, Purple) | (Complexion(x, Pale) & Boils(x)) ==> Poisoned(x)'
    'Victim(x) & Intact(x) & Complexion(x, Green) ==> Poisoned(x)', #If victim is intact & Green Complexion, they were poisoned
    'Victim(x) & Intact(x) & Complexion(x, Blue) ==> Poisoned(x)', #If victim is intact & Blue Complexion, they were poisoned
    'Victim(x) & Intact(x) & Complexion(x, Purple) ==> Poisoned(x)', #If victim is intact & Purple Complexion, they were poisoned
    'Victim(x) & Intact(x) & Complexion(x, Pale) & Boils(x) ==> Poisoned(x)', #If victim is intact & Pale Complexion, and they have boils, they were poisoned
    #'Victim(x) & Complexion(x, Pale) & (Cold(x) | Punctured(x)) ==> Drained(x)', #If Victim complexion is Pale & they are cold, they were drained
    'Victim(x) & Complexion(x, Pale) & Cold(x) ==> Drained(x)', #If their complexion is pale and they were cold then the victim was drained
    'Victim(x) & Complexion(x, Pale) & Punctured(x) ==> Drained(x)', #If their complexion is pale and they were punctured then the victim was drained
    #'Victim(x) & (Disemboweled(x) | Dismembered(x)) ==> Incomplete(x)'
    'Victim(x) & Disemboweled(x) ==> Incomplete(x)', 
    'Victim(x) & Dismembered(x) ==> Incomplete(x)'
]
#Notes:
#Or statements weren't working so I split them into two logic sentences

#Hints given when I asked Rebecca
#Instructions may say or but is "|" required