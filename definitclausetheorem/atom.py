
def is_atom(s):
    """Return true ony if <s> is a valid atom. Defined in the assignment."""
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])


def is_letter(s):
    """Return true ony if <s> is a letter in the domain language. Defined in the assignment."""
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"


class Atom:
    """Hashable representation of an atom"""
    def __init__(self, atom):
        if not is_atom(atom):
            raise ValueError(repr(atom) + ' is not a valid atom')
        self.atom = atom

    def __hash__(self):
        return hash(self.atom)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.atom == other.atom
        )

    def __str__(self):
        return self.atom

    def __repr__(self):
        return '"' + self.atom + '"'

