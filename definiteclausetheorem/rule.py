from .atom import Atom


class Rule:
    """Represents a rule in the problem domain."""

    def __init__(self, head, body):
        """Arguments: \n\tleft: an Atom\n\tright: a set of Atoms"""
        self.head = head
        self.body = body

    def infer(self, atoms):
        """Returns True if the right side of the rule is the subset of the <atoms> parameter."""
        return self.body.issubset(atoms)

    @classmethod
    def from_str(cls, line):
        """Parses a line of string into a Rule."""
        left, right = line.split("<--", 2)
        left = Atom(left.strip())

        atoms = [Atom(atom.strip()) for atom in right.split("&")]

        return cls(left, set(atoms))

    def __str__(self):
        return str(self.head) + " <-- " + " & ".join(str(atom) for atom in self.body)
