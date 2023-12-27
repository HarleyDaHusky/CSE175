#
# logic.py
#
# This script implements a first-order logic backward chaining inference
# procedure for definite clauses. The file provides a class, called
# "FolKB", which implements a first-order logic knowledge base (set of
# definite clauses). A number of useful functions are also defined in this
# file. The function that is typically used as an interface to this
# inference procedure is the "fol_bc_ask" function. This function takes a
# knowledge base and a query sentence as arguments. If the knowledge base
# entails the query for some substitution lists, then "fol_bc_ask" will
# return a generator of that set of substitution lists. In this
# implementation, substitution lists are implemented as Python dictionaries
# of variable/value pairs.
#
# The contents of this file are based on code assembled for the book
# "Artificial Intelligence: A Modern Approach" by Stuart Russell and
# Peter Norvig. In particular, the "fol_bc_ask" function, and its
# components, mirror pseudocode provided in that textbook. The Python
# implementation was originally written by Peter Norvig, with augmentations
# by Clay Morrison and David Noelle.
#
# This content is protected and may not be shared, uploaded, or distributed.
#
# David Noelle - Fri Oct 21 20:29:13 PDT 2022
#


import itertools
from utils import *


def is_symbol(s):
    """Return true iff the given string encodes a symbol. A symbol starts
    with an alphabetic character."""
    return isinstance(s, str) and s[:1].isalpha()

def is_var_symbol(s):
    """Return true iff the given string encodes a logical variable. A
    variable starts with a lowercase character."""
    return is_symbol(s) and s[0].islower()

def variables(s):
    """Return a set of the variables in the expression encoded by the given
    string argument."""
    result = set([])
    def walk(s):
        if is_variable(s):
            result.add(s)
        else:
            for arg in s.args:
                walk(arg)
    walk(s)
    return result

def is_definite_clause(s):
    """Return true iff the given string encodes a definite clause."""
    if is_symbol(s.op):
        return True
    elif s.op == '==>':
        body, head = s.args
        return (is_symbol(head.op) and all(is_symbol(arg.op) for arg in conjuncts(body)))
    else:
        return False

def parse_definite_clause(s):
    """Return the antecedents and the consequent of a definite clause encoded
    by the given string."""
    assert is_definite_clause(s)
    if is_symbol(s.op):
        return [], s
    else:
        body, head = s.args
        return conjuncts(body), head

def dissociate(op, sentence):
    """Given a specific associative operation, like conjunction or
    disjunction, return a flattened list of the arguments to that operation
    in the given sentence."""
    result = []
    def collect(subargs):
        for arg in subargs:
            if arg.op == op: collect(arg.args)
            else: result.append(arg)
    collect(sentence)
    return result

def conjuncts(s):
    """Return a list of the conjuncts in the argument sentence."""
    return dissociate('&', [s])

def disjuncts(s):
    """Return a list of the disjuncts in the argument sentence."""
    return dissociate('|', [s])


# Substitution

def subst(s, x):
    """Apply the given substitution list (s) to the given expression (x)."""
    if isinstance(x, list):
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([subst(s, xi) for xi in x])
    elif not isinstance(x, Expr):
        return x
    elif is_var_symbol(x.op):
        return s.get(x, x)
    else:
        return Expr(x.op, *[subst(s, arg) for arg in x.args])

def cascade_substitution(s):
    """Modify in place the given substitution list to replace
    variables bound to variables with variables bound to the
    other variables' values. This is a cascade substitution.
    If a value is replaced with a function, ensure that all of
    the function arguments are correct by passing over them
    another time."""
    for x in s:
        s[x] = subst(s, s.get(x))
        if isinstance(s.get(x), Expr) and not is_variable(s.get(x)):
            # Ensure function terms are correct by passing over them again
            s[x] = subst(s, s.get(x))


# Unification

def unify(x, y, s):
    """Unify the two given expressions (x and y), under the given substitution
    list (s). Return the most general unifier, or None if the expressions
    cannot be unified."""
    if s is None:
        return None
    elif x == y:
        return s
    elif is_variable(x):
        return unify_var(x, y, s)
    elif is_variable(y):
        return unify_var(y, x, s)
    elif isinstance(x, Expr) and isinstance(y, Expr):
        return unify(x.args, y.args, unify(x.op, y.op, s))
    elif isinstance(x, str) or isinstance(y, str):
        return None
    elif issequence(x) and issequence(y) and len(x) == len(y):
        if not x:
            return s
        return unify(x[1:], y[1:], unify(x[0], y[0], s))
    else:
        return None

def is_variable(x):
    """Return true iff the given expression (x) is a variable. A variable
    is an Expr object with no arguments, with the operation being encoded
    as a lowercase string."""
    return isinstance(x, Expr) and not x.args and is_var_symbol(x.op)

def unify_var(var, x, s):
    """Unify the given variable with the given expression, under the
    specified substitution list."""
    if var in s:
        return unify(s[var], x, s)
    elif x in s:
        return unify(var, s[x], s)
    elif occur_check(var, x, s):
        return None
    else:
        new_s = extend(s, var, x)
        cascade_substitution(new_s)
        return new_s

def occur_check(var, x, s):
    """Return true iff the given variable occurs in the given expression,
    with the given substitution list applied to the expression."""
    if var == x:
        return True
    elif is_variable(x) and x in s:
        return occur_check(var, s[x], s)
    elif isinstance(x, Expr):
        return (occur_check(var, x.op, s) or
                occur_check(var, x.args, s))
    elif isinstance(x, (list, tuple)):
        return first(e for e in x if occur_check(var, e, s))
    else:
        return False

def extend(s, var, val):
    """Return a copy of the given substitution list, extended by the
    specified variable/value binding."""
    s_copy = s.copy()
    s_copy[var] = val
    return s_copy


# Standardizing Variables Apart

def standardize_variables(sentence, d=None):
    """Replace all the variables in sentence with new variables."""
    if d is None:
        d = {}
    if not isinstance(sentence, Expr):
        return sentence
    elif is_var_symbol(sentence.op):
        if sentence in d:
            return d[sentence]
        else:
            var = Expr('v_{}'.format(next(standardize_variables.counter)))
            d[sentence] = var
            return var
    else:
        return Expr(sentence.op,
                    *[standardize_variables(a, d) for a in sentence.args])

standardize_variables.counter = itertools.count()


# First-Order Logic Knowledge Base

class FolKB:
    """A knowledge base containing first-order logic definite clauses."""

    def __init__(self, initial_clauses=None):
        self.clauses = []
        if initial_clauses is None:
            initial_clauses = []
        for clause in initial_clauses:
            self.tell(clause)

    def tell(self, sentence):
        """Assert the given sentence into the knowledge base."""
        if is_definite_clause(sentence):
            self.clauses.append(sentence)
        else:
            raise Exception("Not a definite clause: %s" % sentence)

    def ask_generator(self, query):
        return fol_bc_ask(self, query)

    def retract(self, sentence):
        """Retract the given sentence from the knowledge base."""
        self.clauses.remove(sentence)

    def fetch_rules_for_goal(self, goal):
        """Return the rules that might be used to prove the given goal."""
        # This is highly inefficient, treating every sentence in the
        # knowledge base as if it might be useful.
        return self.clauses


# First-Order Logic Backward Chaining

def fol_bc_ask(KB, query):
    """A simple backward-chaining algorithm for first-order logic definite
    clauses. Return a generator of substitution lists that allow the given
    query to be proven from the sentences in the given first-order logic
    knowledge base."""
    return fol_bc_or(KB, query, {})

def fol_bc_or(KB, goal, theta):
    for rule in KB.fetch_rules_for_goal(goal):
        lhs, rhs = parse_definite_clause(standardize_variables(rule))
        for theta1 in fol_bc_and(KB, lhs, unify(rhs, goal, theta)):
            yield theta1

def fol_bc_and(KB, goals, theta):
    if theta is None:
        pass
    elif not goals:
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        for theta1 in fol_bc_or(KB, subst(theta, first), theta):
            for theta2 in fol_bc_and(KB, rest, theta1):
                yield theta2


# Pretty Printing Utilities

def pretty(x):
    t = type(x)
    if t is dict:  return pretty_dict(x)
    elif t is set: return pretty_set(x)
    else:          return repr(x)

def pretty_dict(d):
    """Return dictionary d's repr but with the items sorted."""
    return '{%s}' % ', '.join('%r: %r' % (k, v)
                              for k, v in sorted(d.items(), key=repr))

def pretty_set(s):
    """Return set s's repr but with the items sorted."""
    return 'set(%r)' % sorted(s, key=repr)

def pretty_subst(s):
    """Pretty-print substitution list , s."""
    pretty_dict(s)
