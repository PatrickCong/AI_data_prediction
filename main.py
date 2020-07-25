
from definiteclausetheorem.repl import REPL
from definiteclausetheorem.knowledgebase import KnowledgeBase

if __name__ == '__main__':
    prompt = REPL(KnowledgeBase())
    prompt.cmdloop('Starting prompt...')
