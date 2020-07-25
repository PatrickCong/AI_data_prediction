
from definitclausetheorem.repl import REPL
from definitclausetheorem.knowledgebase import KnowledgeBase

if __name__ == '__main__':
    prompt = REPL(KnowledgeBase())
    prompt.cmdloop('Starting prompt...')
