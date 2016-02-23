from inpho.model import *
import re
from progressbar import ProgressBar

def from_dlv(filename, load_obj=False):
    """
    Function to build a taxonomy from the specified DLV output file.
    """
    # build regex for instance and link search
    regex_class = re.compile("aclass\(i(\d+)\)")
    regex_isa = re.compile("isb\(i(\d+),i(\d+)\)")
    regex_ins = re.compile("ins\(i(\d+),i(\d+)\)")
    regex_links = re.compile("link\(i(\d+),i(\d+)\)")

    # process DLV output file
    with open(filename) as f:
        dlv = f.read()

        classes = frozenset(regex_class.findall(dlv))
        subclasses = frozenset(regex_isa.findall(dlv))
        subclasses = dict(subclasses)
        instances = frozenset(regex_ins.findall(dlv))
        instances = dict(instances)
        nodes = dict()
        links = frozenset(regex_links.findall(dlv))
        links = dict(links)

    # clear former ontotree table
    print "removing nodes"
    pbar = ProgressBar()
    for node in pbar(Session.query(Node).all()):
        Session.delete(node)

    print "removing instances and links"
    pbar = ProgressBar()
    for idea in pbar(Session.query(Idea).all()):
        idea.instances = []
        idea.links = []
    Session.commit()

    # add new classes
    print "adding new classes"
    pbar = ProgressBar()
    for cls in pbar(classes):
        idea = Session.query(Entity).get(cls)
        node = Node()
        node.label = idea.label
        node.concept_id = cls
        node.parent_id = None
        nodes[cls] = node
        Session.add(node)

    Session.commit()

    # add subclass relations
    for child, parent in subclasses.iteritems():
        nodes[child].parent_id = nodes[parent].ID
    Session.commit()

    # add instances
    for child, parent in instances.iteritems():
        idea1 = Session.query(Idea).get(parent)
        idea2 = Session.query(Idea).get(child)
        idea1.instances.append(idea2)
    Session.commit()

    # add links
    for i1, i2 in links.iteritems():
        idea1 = Session.query(Idea).get(i1)
        idea2 = Session.query(Idea).get(i2)
        idea1.links.append(idea2)
    Session.commit()


if __name__ == '__main__':
    import sys
    filename= sys.argv[-1]
    from_dlv(sys.argv[-1]) 

    regex_class = re.compile("aclass\(i(\d+)\)")
    regex_isb = re.compile("isb\(i(\d+),i(\d+)\)")
    regex_ins = re.compile("ins\(i(\d+),i(\d+)\)")
    with open(filename) as f:
        dlv = f.read()
        
        classes = frozenset(regex_class.findall(dlv))
        isb = frozenset(regex_isb.findall(dlv))
        ins = frozenset(regex_ins.findall(dlv))
    for sub, cls in ins:
        print Session.query(Idea).get(cls).label
        print "\t", Session.query(Idea).get(sub).label
    sys.exit()
    for cls in classes:
        print Session.query(Idea).get(cls).label
    for sub, cls in isb:
        print Session.query(Idea).get(cls).label
        print "\t", Session.query(Idea).get(sub).label
        for i, subcl in ins:
            if subcl == sub:
                print "\t\t", Session.query(Idea).get(i).label

    print len(classes), len(isb), len(ins)
    sys.exit() 
    # build regex for instance and link search
    regex_pclass = re.compile("[gs]pclass\(i(\d+)\)")
    regex_gpclass = re.compile("gpclass\(i(\d+)\)")
    regex_spclass = re.compile("spclass\(i(\d+)\)")
    regex_class = re.compile("aclass\(i(\d+)\)")
    regex_aclass = re.compile("aclass\(i(\d+)\)")
    regex_pisa = re.compile("pisa\(i(\d+),i(\d+)\)")
    regex_nisa = re.compile("nisa\(i(\d+),i(\d+)\)")
    regex_pins = re.compile("ains\(i(\d+),i(\d+)\)")
    regex_ins = re.compile("ins\(i(\d+),i(\d+)\)")

    # process DLV output file
    with open(filename) as f:
        dlv = f.read()

        classes = frozenset(regex_class.findall(dlv))
        aclasses = frozenset(regex_aclass.findall(dlv))
        pclasses = frozenset(regex_pclass.findall(dlv))
        gpclasses = frozenset(regex_gpclass.findall(dlv))
        spclasses = frozenset(regex_spclass.findall(dlv))
        #print len(gpclasses), "gpclasses", sorted(gpclasses)
        #print len(spclasses), "spclasses", sorted(spclasses)
        #print len(pclasses), "pclasses", len(classes.intersection(pclasses)), "instantiated"
        print gpclasses.intersection(spclasses), len(gpclasses), "gcls", len(spclasses), "scls"

        nisa = frozenset(regex_nisa.findall(dlv))
        print len(nisa), "nisa"
        pisa = frozenset(regex_pisa.findall(dlv))
        pins = frozenset(regex_pins.findall(dlv))
        ins = frozenset(regex_ins.findall(dlv))
        print sorted(pins)
        print len(pisa), "pisa have pins?", len(pisa) == len(pisa.intersection(pins))
        print len(pisa), "pisa have nisa?", len(pisa) == len(pisa.intersection(nisa)),len(pisa.intersection(nisa))
        print len(pins), '->', len(ins), len(ins.intersection(pins)) == len(ins)
        instances =  sorted([(ins,cls) for ins, cls in pins if ins in pclasses or cls in pclasses])
        #print len(instances), instances
        sys.exit()
