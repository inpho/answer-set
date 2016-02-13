from inpho.model import *
import re

def from_dlv(filename, load_obj=False):
    """
    Function to build a taxonomy from the specified DLV output file.
    """
    # build regex for instance and link search
    regex_class = re.compile("class\(i(\d+)\)")
    regex_isa = re.compile("isa\(i(\d+),i(\d+)\)")
    regex_ins = re.compile("ins\(i(\d+),i(\d+)\)")
    regex_links = re.compile("link\(i(\d+),i(\d+)\)")

    # process DLV output file
    with open(filename) as f:
        dlv = f.read()

        classes = frozenset(regex_class.findall(dlv))
        subclasses = frozenset(regex_isa.findall(dlv))
        subclasses = dict(instances)
        instances = frozenset(regex_ins.findall(dlv))
        instances = dict(instances)
        nodes = dict()
        links = frozenset(regex_links.findall(dlv))

    # clear former ontotree table
    for node in Session.query(Node).all():
        Session.delete(node)
    Session.commit()

    # add new classes
    for cls in classes:
        idea = Session.query(Entity).get(cls)
        node = Node()
        node.label = idea.label
        node.concept_id = cls
        node.parent_id = None
        nodes[cls] = node
        print "adding", node.label
        Session.add(node)

    Session.commit()

    # add subclass relations
    for child, parent in subclasses.iteritems():
        nodes[child].parent_id = nodes[parent].ID
    Session.commit()

    # add instances
    for child, parent in instances.iteritems():
        idea1 = Session.query(Idea).get(i1)
        idea2 = Session.query(Idea).get(i2)
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
    from_dlv(sys.argv[-1]) 
