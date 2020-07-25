
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

