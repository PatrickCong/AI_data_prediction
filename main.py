from cmd import Cmd
import os

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

# KnowledgeBase class implements the KnowledgeBase functionality by definition
class KnowledgeBase:
    atoms = set()
    rules = []

    def tell(self, atom):
        """Adds a single atom to the atoms set"""
        if atom in self.atoms:
            return False
        else:
            self.atoms.add(atom)
            return True

    def infer_all(self):
        """Finds every applicable rule to infer new atoms, repeats until no more atoms can be inferred"""
        new_atoms = set()
        while True:
            new_atoms_len = len(new_atoms)
            for rule in self.rules:
                if rule.head in self.atoms | new_atoms:
                    continue

                if rule.infer(self.atoms | new_atoms):
                    new_atoms.add(rule.head)

            if new_atoms_len == len(new_atoms):
                # no more rules to apply
                break

        self.atoms |= new_atoms

        return new_atoms

    def clear_atoms(self):
        self.atoms = set()


def atoms_to_str(atoms):
    """Converts an iterable of Atoms into a string to match behaviour in the assignment."""
    if len(atoms) == 0:
        return "<none>"
    else:
        return ", ".join(str(atom) for atom in atoms)


class REPL(Cmd):
    def __init__(self, knowledge_base, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.knowledge_base = knowledge_base

        self.prompt = 'kb> '

    # Override default empty-line handler
    def emptyline(self):
        pass

    # Override default handler for unrecognised commands
    def default(self, line):
        print("Error: unknown command", repr(line.split()[0]))

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit

    def do_EOF(self, args):
        """Quits the program."""
        self.do_quit(args)

    def do_load(self, args):
        """Loads a Knowledge Base file"""
        if len(args) == 0:
            print("Syntax: load <filepath>")
            return

        if not os.path.exists(args):
            print("File does not exists")
            return

        if not os.path.isfile(args):
            print(args, "is not a file")
            return

        try:
            rules = []
            with open(args) as f:
                for i, line in enumerate(f.readlines()):
                    if len(line.strip()) == 0: continue
                    if line[0] == '#': continue
                    try:
                        rules.append(Rule.from_str(line))
                    except ValueError as e:
                        print(f"Error at line {i}: {repr(line)}")
                        print(str(e))
                        print("Error: ", args, "is not a valid knowledge base")
                        raise e
            self.knowledge_base.rules = rules

            print(f"{len(rules)} definite clauses read in:")
            for i, rule in enumerate(rules):
                print(f"{i + 1:>5}: {rule}")

        except Exception as e:
            print("Failed to read file: " + str(e))

    def do_tell(self, args):
        """Adds the atom to the current Knowledge Base"""
        if len(args) == 0:
            print("Error: tell needs at least one atom")
            return

        try:
            atoms = [Atom(atom) for atom in args.split()]

            for atom in atoms:
                if self.knowledge_base.tell(atom):
                    print("Atom " + repr(atom) + " added to KB")
                else:
                    print("Atom " + repr(atom) + " already known to be true")
        except ValueError as e:
            print(str(e))

    def do_infer_all(self, args):
        """Calls infer_all on the knowledge_base"""
        atoms = self.knowledge_base.atoms.copy()
        new_atoms = self.knowledge_base.infer_all()

        print("Newly inferred atoms: \n\t", atoms_to_str(new_atoms))
        print("Already known atoms: \n\t", atoms_to_str(atoms))

    def do_clear_atoms(self, args):
        """Removes all Atoms from the KnowledgeBase."""
        self.knowledge_base.clear_atoms()

    def do_show_atoms(self, args):
        """Lists all learned atoms."""
        for i, atom in enumerate(self.knowledge_base.atoms):
            print(f"{i+1:>5}: {atom}")

    def do_show_rules(self, args):
        """Lists all loaded rules."""
        for i, rule in enumerate(self.knowledge_base.rules):
            print(f"{i+1:>5}: {rule}")

    def do_is_true(self, args):
        """Tells if all of the arguments are known to be true."""
        if len(args) == 0:
            print("Error: is_true needs at least one argument")
            return

        try:
            atoms = set(Atom(atom.strip()) for atom in args.split())
            print(str(atoms.issubset(self.knowledge_base.atoms)))
        except Exception as e:
            print(str(e))


# You mean these?

if __name__ == '__main__':
    prompt = REPL(KnowledgeBase())
    prompt.cmdloop('Starting prompt...')
