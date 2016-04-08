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

    for (topic1, topic2) in ic.keys():
        for i in range(4):
            #1. if msi > mgi and msi > ici --> msi
            if ms[(topic1,topic2)][i] > mg[(topic1,topic2)][i] and ms[(topic1,topic2)][i] > ic[(topic1,topic2)][i]:
                print "msi(i%s, i%s, %s)." % (topic1, topic2, i)
            #2. if mgi > msi and mgi > ici --> mgi
            if mg[(topic1,topic2)][i] > ms[(topic1,topic2)][i] and mg[(topic1,topic2)][i] > ic[(topic1,topic2)][i]:
                print "mgi(i%s, i%s, %s)." % (topic1, topic2, i)
            #3. if ici > msi and ici > mgi --> ici
            if ic[(topic1,topic2)][i] > ms[(topic1,topic2)][i] and ic[(topic1,topic2)][i] > mg[(topic1,topic2)][i]:
                print "ici(i%s, i%s, %s)." % (topic1, topic2, i)
            #1. msi case 1: bias against IC in input; where ICI(A, B, C) = MSI(A, B, C), but MSI(A, B, C) > MGI(A, B, C) choose MSI.
            if ic[(topic1,topic2)][i] == ms[(topic1,topic2)][i] and ms[(topic1,topic2)][i] > mg[(topic1,topic2)][i]:
                print "msi(i%s, i%s, %s)." % (topic1, topic2, i)
            #2. mgi case 2: bias against IC in input; where ICI(A, B, C) = MGI(A, B, C), but MGI(A, B, C) > MSI(A, B, C) choose MGI
            if ic[(topic1,topic2)][i] == mg[(topic1,topic2)][i] and mg[(topic1,topic2)][i] > ms[(topic1,topic2)][i]:
                print "mgi(i%s, i%s, %s)." % (topic1, topic2, i)
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