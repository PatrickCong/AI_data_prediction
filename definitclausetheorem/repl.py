from cmd import Cmd
import os

from .atom import Atom
from .rule import Rule


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
