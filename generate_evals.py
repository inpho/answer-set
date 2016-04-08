from inpho.model import *

from sqlalchemy import or_

def generate_input():
    """
    Prints the DLV input to STDOUT
    """
    # Set of terms which appear
    appearances = set()
    #appearances.update(print_taxonomy())
    appearances.update(print_evaluations(IdeaEvaluation))
    appearances.update(print_evaluations(AnonIdeaEvaluation))
    print_appearances(appearances)

def print_taxonomy():
    """
    Prints DLV input for the taxonomy, covering the class and isa atoms.
    Returns the list of terms which occur in the database.
    """
    # Set of terms which appear
    appearances = set()
    
    # Select concept_id and parent_concept_id pairs
    ids = Session.query(Node.concept_id, Node.parent_concept_id).all()

    # Build up atoms for hand-built taxonomy
    for concept_id, parent_concept_id in ids:
        appearances.update([concept_id, parent_concept_id])
    
        print "class(i%s)." % (concept_id)
        if parent_concept_id:
            print "isa(i%s, i%s)." % (concept_id, parent_concept_id)

    return appearances

def print_evaluations(type=IdeaEvaluation):
    """
    Prints DLV atoms for evaluations, covering the p#, mgi, msi, sgi, and ici.
    Returns the list of terms which occur in the database.
    """
    appearances = set()
    
    ic = defaultdict(lambda: [0,0,0,0,0])
    mg = defaultdict(lambda: [0,0,0,0,0])
    ms = defaultdict(lambda: [0,0,0,0,0])

    evals = Session.query(IdeaEvaluation).all()
    
    for eval in evals:
        appearances.update([eval.ante_id, eval.cons_id])
        
        if not eval.user:
            continue
        
        expertise_level = max(eval.user.first_area_level, eval.user.second_area_level)
        
        if not expertise_level:
            expertise_level = 0
        
        if eval.generality == 0:
            ms[(eval.ante_id, eval.cons_id)][expertise_level] += 1
        if eval.generality == 1:
            mg[(eval.ante_id, eval.cons_id)][expertise_level] += 1
        if eval.generality == 3:
            ic[(eval.ante_id, eval.cons_id)][expertise_level] += 1

    return appearances

def print_appearances(appearances):
    """
    Prints DLV atoms for appearances, covering the i atom.
    Returns the same as the input variable.
    """
    for idea in appearances:
        print "i(i%s)." % idea

    return appearances

if __name__ == '__main__':
    generate_input()