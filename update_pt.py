

#{{{ Import all important libraries
import os, sys, time
if not '/projects/1fdd6b0b-5199-4b0e-9f7f-7759af4a5e7a/.local/lib/python3.4/site-packages/' in sys.path:
    sys.path.append('/projects/1fdd6b0b-5199-4b0e-9f7f-7759af4a5e7a/.local/lib/python3.4/site-packages/')
import collections
import random
import laf
from laf.fabric import LafFabric
import etcbc
from etcbc.preprocess import prepare
from etcbc.lib import Transcription, monad_set
from etcbc.trees import Tree
from etcbc.featuredoc import FeatureDoc
fabric = LafFabric()
tr = Transcription()

print("It works so far." )
#}}}

#{{{ Load the API
API = fabric.load('etcbc4', '--', 'feature-doc', {
    "xmlids": {"node": False, "edge": False},
    "features": ('''
            otype
            domain
            function
            g_cons
            g_cons_utf8
            g_lex
            g_lex_utf8
            g_nme
            g_nme_utf8
            g_pfm
            g_pfm_utf8
            g_prs
            g_prs_utf8
            g_uvf
            g_uvf_utf8
            g_vbe
            g_vbe_utf8
            g_vbs
            g_vbs_utf8
            g_word
            g_word_utf8
            gn
            lex
            lex_utf8
            ls
            nme
            nu
            number
            pdp
            pfm
            prs
            ps
            rela
            sp
            st
            tab
            trailer_utf8
            txt
            typ
            uvf
            vbe
            vbs
            vs
            vt
            book
            chapter
            label
            verse
    ''',""),
    "primary": False,
})
exec(fabric.localnames.format(var='fabric'))
#}}}

#{{{ Stuff necessary to load parents relationships
type_info = (
    ("word", ''),
    ("subphrase", 'U'),
    ("phrase", 'P'),
    ("clause", 'C'),
    ("sentence", 'S'),
)
type_table = dict(t for t in type_info)
type_order = [t[0] for t in type_info]

pos_table = {
    'adjv': 'aj',
    'advb': 'av',
    'art': 'dt',
    'conj': 'cj',
    'intj': 'ij',
    'inrg': 'ir',
    'nega': 'ng',
    'subs': 'n',
    'nmpr': 'n-pr',
    'prep': 'pp',
    'prps': 'pr-ps',
    'prde': 'pr-dem',
    'prin': 'pr-int',
    'verb': 'vb',
}

ccr_info = {
    'Adju': ('r', 'Cadju'),
    'Attr': ('r', 'Cattr'),
    'Cmpl': ('r', 'Ccmpl'),
    'CoVo': ('n', 'Ccovo'),
    'Coor': ('x', 'Ccoor'),
    'Objc': ('r', 'Cobjc'),
    'PrAd': ('r', 'Cprad'),
    'PreC': ('r', 'Cprec'),
    'Resu': ('n', 'Cresu'),
    'RgRc': ('r', 'Crgrc'),
    'Spec': ('r', 'Cspec'),
    'Subj': ('r', 'Csubj'),
    'NA':   ('n', 'C'),
}

tree_types = ('sentence', 'clause', 'clause_atom', 'phrase', 'subphrase', 'word')
(root_type, leaf_type, clause_type) = (tree_types[0], tree_types[-1], 'clause')
ccr_table = dict((c[0],c[1][1]) for c in ccr_info.items())
ccr_class = dict((c[0],c[1][0]) for c in ccr_info.items())

root_verse = {}
root_clause_atom = {}

for n in NN():
    otype = F.otype.v(n)
    if otype == "book" and F.etcbc4_sft_book.v(n) != "Genesis":
        break
    elif otype == "chapter" and int(F.etcbc4_sft_chapter.v(n)) > 5:
        break
    elif otype == 'verse': cur_verse = F.label.v(n)
    elif otype == "clause_atom":
        root_verse[n] = cur_verse
        cur_clause_atom = F.etcbc4_ft_number.v(n)
    elif otype == "word":
        root_verse[n] = cur_verse
        root_clause_atom[n] = cur_clause_atom
#        print(list(C.parent.v(n)))

tree = Tree(API, otypes = tree_types,
     clause_type=clause_type,
     ccr_feature='rela',
     pt_feature='typ',
     pos_feature='sp',
     mother_feature = 'mother',
     )
#tree.restructure_clauses(ccr_class)
results = tree.relations()
parent = results['eparent']
sisters = results['sisters']
children = results['echildren']
elder_sister = results['elder_sister']
print("Ready for processing") # Was msg()

#}}}

#{{{ Import the helper functions
def give_me_your_words(n):
        global F
        if F.etcbc4_db_otype.v(n) == 'word':
                return [n]
        else:
            list_of_word_lists = [give_me_your_words(c) for c in children[n]]
            return [item for sublist in list_of_word_lists for item in sublist]

def get_text_of_word_list(word_list):
        global F
        return ' '.join(map(F.etcbc4_ft_g_cons_utf8.v, word_list))

def get_cons_of_word_list(word_list):
        global F
        return ' '.join(map(F.etcbc4_ft_g_cons.v, word_list))

def give_me_your_parents_up_to(node, parent_type='clause', limit=19):
    # This function is very dangerous. If you feed it something larger than a clause, stuff explodes.
        global parent
        if limit < 0:
                return []
        if not node in parent:
#                return []
                return ["not in parent"]
        p = parent[node]
        if F.etcbc4_db_otype.v(p) == parent_type:
                return [p]
        else:
                return [p] + give_me_your_parents_up_to(p, parent_type, limit-1)

suffix_dict = {
'W'   : { 'ps' : 'p3', 'nu' : 'sg', 'gn' : 'm' },
'K'   : { 'ps' : 'p2', 'nu' : 'sg', 'gn' : 'm' },
'J'   : { 'ps' : 'p1', 'nu' : 'sg', 'gn' : 'unknown' },
'M'   : { 'ps' : 'p3', 'nu' : 'pl', 'gn' : 'm' },
'H'   : { 'ps' : 'p3', 'nu' : 'sg', 'gn' : 'f' },
'HM'  : { 'ps' : 'p3', 'nu' : 'pl', 'gn' : 'm' },
'KM'  : { 'ps' : 'p2', 'nu' : 'pl', 'gn' : 'm' },
'NW'  : { 'ps' : 'p1', 'nu' : 'pl', 'gn' : 'unknown' },
'HW'  : { 'ps' : 'p3', 'nu' : 'sg', 'gn' : 'm' },
'NJ'  : { 'ps' : 'p1', 'nu' : 'sg', 'gn' : 'unknown' },
'K='  : { 'ps' : 'p2', 'nu' : 'sg', 'gn' : 'f' },
'HN'  : { 'ps' : 'p3', 'nu' : 'pl', 'gn' : 'f' },
'H='  : { 'ps' : 'p3', 'nu' : 'sg', 'gn' : 'unknown' },
'MW'  : { 'ps' : 'p3', 'nu' : 'pl', 'gn' : 'm' },
'N'   : { 'ps' : 'p3', 'nu' : 'pl', 'gn' : 'f' },
'KN'  : { 'ps' : 'p2', 'nu' : 'pl', 'gn' : 'f' },
}


def insert_dict_in_db(cursor, table, values):
        columns = ', '.join(values.keys())
        placeholders = ':'+', :'.join(values.keys())
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, placeholders)
        print(query)
        cursor.execute(query, values)
        
#}}}

#{{{ Load database
import sqlite3

db = sqlite3.connect('gcdata.sqlite')
c = db.cursor()
#}}}

#{{{ Update Cltype,Phtype
todo= list(c.execute("select ClANr,PhANr from pt"))
for (ClANr,PhANr) in todo:
    c.execute("update pt set Cltype=:Cltype,Phtype=:Phtype,Phfunc=:Phfunc where ClANr=:ClANr and PhANr=:PhANr", {"Cltype":F.etcbc4_ft_typ.v(ClANr),"Phtype":F.etcbc4_ft_typ.v(PhANr),"Phfunc":F.etcbc4_ft_function.v(PhANr),"ClANr":ClANr,"PhANr":PhANr})
#}}}

#{{{ Update Phfunc, SPhNr
todo2 = list(c.execute("select Node from pt"))

for Node in todo2:
    check=False
    Node = eval(Node[0])
    parents = give_me_your_parents_up_to(Node)
    print(F.etcbc4_db_otype.v(Node),parents)
    for x in parents:
        print(x,F.etcbc4_db_otype.v(x))
        if F.etcbc4_db_otype.v(x) == "phrase":
            check=True
    if check == False:
        print("Strange behaviour!")
#            c.execute("update pt set Phfunc=:Phfunc where Node=:Node", {"Phfunc":F.etcbc4_ft_function.v(x),"Node":Node})
#        elif F.etcbc4_db_otype.v(x) == "subphrase":
#            c.execute("update pt set SPhNr=:SPhNr where Node=:Node", {"SPhNr":Node,"Node":Node})
#}}}
