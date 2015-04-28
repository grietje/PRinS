# List options for reference types

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
    "prepare": prepare,
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
                return "not in parent"
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

#{{{
typ = {}
typ["clause"] = []
typ["clause_atom"] = []
typ["phrase"] = []
typ["phrase_atom"] = []

for node in NN():
    otype = F.etcbc4_db_otype.v(node)
    if otype == "book" and F.etcbc4_sft_book.v(node) != "Genesis":
        break
    elif otype == "chapter":
        if int(F.etcbc4_sft_chapter.v(node)) < 1:    # Prevent re-doing already completed chapters
            completed = True
        elif int(F.etcbc4_sft_chapter.v(node)) > 22:    # Set a limit on the amount of data dealt with this time
            break
        else:
            completed = False
    elif otype == "verse" and completed == False:
        place = F.etcbc4_sft_label.v(node)
    elif otype == "clause" and completed == False:
        DSU = (F.etcbc4_ft_txt.v(node).count("Q") > 0)    # If the text_type contains a Q, we consider the clause as Direct Speech
        if DSU == True:
            if not F.etcbc4_ft_typ.v(node) in typ["clause"]:
                typ["clause"].append(F.etcbc4_ft_typ.v(node))
    elif otype == "clause_atom" and completed == False:
        if DSU == True:
            if not F.etcbc4_ft_typ.v(node) in typ["clause"] and not F.etcbc4_ft_typ.v(node) in typ["clause_atom"]:
                typ["clause_atom"].append(F.etcbc4_ft_typ.v(node))
    elif otype == "phrase" and completed == False:
        if DSU == True:
            if not F.etcbc4_ft_typ.v(node) in typ["phrase"]:
                typ["phrase"].append(F.etcbc4_ft_typ.v(node))
    elif otype == "phrase_atom" and completed == False:
        if DSU == True:
            if not F.etcbc4_ft_typ.v(node) in typ["phrase"] and not F.etcbc4_ft_typ.v(node) in typ["phrase_atom"]:
                typ["phrase_atom"].append(F.etcbc4_ft_typ.v(node))

#    elif F.etcbc4_db_otype.v(node) == "word" and DSU == True and completed == False:
#        WNr = node

print(typ)
#}}}

#{{{
types = {}

for node in NN():
    otype = F.etcbc4_db_otype.v(node)
    if otype == "book" and F.etcbc4_sft_book.v(node) != "Genesis":
        break
    elif otype == "chapter" and int(F.etcbc4_sft_chapter.v(node)) > 1:
        break
    elif otype == "verse":
        place = F.etcbc4_sft_label.v(node)
    elif otype == "clause":
        inphrase = False
        DSU = (F.etcbc4_ft_txt.v(node).count("Q") > 0)    # If the text_type contains a Q, we consider the clause as Direct Speech
        if DSU == True:
            type = F.etcbc4_ft_typ.v(node)
            if not type in types:
                types[F.etcbc4_ft_typ.v(node)] = {}
    elif otype == "clause_atom":
        if DSU == True:
            type = F.etcbc4_ft_typ.v(node)
            if not type in types:
                types[F.etcbc4_ft_typ.v(node)] = {}
    elif otype == "phrase":
        inphrase = True
        if DSU == True:
            ph_type = F.etcbc4_ft_typ.v(node)
            ph_func = F.etcbc4_ft_function.v(node)
            if not str((ph_func,ph_type)) in types[type]:
#            if not (ph_func, ph_type) in types[type]:
                types[type][str((ph_func, ph_type))] = []
#                print((ph_func, ph_type))
    elif otype == "word":
        if not inphrase:
            print(place, "Grote faalbaal")
#        if DSU == True:
#            if not (F.etcbc4_ft_ps.v(node) in ("unknown", "NA") and F.etcbc4_ft_nu.v(node) in ("unknown","NA") and F.etcbc4_ft_gn.v(node) in ("unknown","NA")):
#                if not F.etcbc4_ft_sp.v(node) in types[type][str((ph_func,ph_type))]:
#                    types[type][str((ph_func,ph_type))].append(F.etcbc4_ft_sp.v(node))
#            if not F.etcbc4_ft_prs.v(node) in ("absent","n/a"):
#                if not "suffix" in types[type][str((ph_func,ph_type))]:
#                    types[type][str((ph_func,ph_type))].append("suffix")

#for x in types:
#    print(x)
#    print(types[x])

#}}}

#{{{ Try to find clause_types, phrase_types for existing data PHTYPE FAILS!!!
data = {}
for node in NN():
    otype = F.etcbc4_db_otype.v(node)
    if otype == "book" and F.etcbc4_sft_book.v(node) != "Genesis":
        break
    elif otype == "chapter":
        if int(F.etcbc4_sft_chapter.v(node)) > 1:
            break
    elif otype == "verse" and int(F.etcbc4_sft_verse.v(node)) > 15:
        break
    elif otype == "clause":
        cltype = F.etcbc4_ft_typ.v(node)
    elif otype == "clause_atom":
        data[node] = cltype
    elif otype == "phrase":
        phtype = F.etcbc4_ft_typ.v(node)
    elif otype == "phrase_atom":
        data[node] = phtype
print(data)

todo = list(c.execute("select ClANr, PhANr from pt"))
for (ClANr,PhANr) in todo:
    c.execute("update pt set Cltype=:Cltype,Phtype=:Phtype where ClANr=:ClANr and PhANr=:PhANr", {"Cltype":data[ClANr],"Phtype":data[PhANr],"ClANr":ClANr,"PhANr":PhANr})

#}}}

#{{{ Overview clause_types
clause_types = {}
clause_types["verbless"] = { "CPen":"Casus pendens" , "NmCl":"Nominal clause" , "AjCl":"Adjective clause" }
clause_types["verb"] = { "Ptcp":"Participle clause" , "Voct":"Vocative clause" , "Way0":"Wayyiqtol-null clause" , "WIm0":"We-imperative-null clause" , "WQt0":"We-qatal-null clause" , "WYq0":"We-yiqtol-null clause" , "InfC":"Infinitive construct clause" , "InfA":"Infinitive absolute clause" , "ZIm0":"Zero-imperative-null clause" , "ZQt0":"Zero-qatal-null clause" , "ZYq0":"Zero-yiqtol-null clause" }
clause_types["X-verb"] = { "WXIm":"We-X-imperative clause" , "WXQt":"We-X-qatal clause" , "WXYq":"We-X-yiqtol clause" , "XImp":"X-imperative clause" , "XQtl":"X-qatal clause" , "XYqt":"X-yiqtol clause" }
clause_types["verb-X"] = { "WayX":"Wayyiqtol-X clause" , "WImX":"We-imperative-X clause" , "WQtX":"We-qatal-X clause" , "WYqX":"We-yiqtol-X clause" , "ZImX":"Zero-imperative-X clause" , "ZQtX":"Zero-qatal-X clause" , "ZYqX":"Zero-yiqtol-X clause" }
clause_types["x-verb"] = { "WxI0":"We-x-imperative-null clause" , "WxQ0":"We-x-qatal-null clause" , "WxY0":"We-x-yiqtol-null clause" , "xIm0":"x-imperative-null clause" , "xQt0":"x-qatal-null clause" , "xYq0":"x-yiqtol-null clause" }
clause_types["x-verb-X"] = { "WxIX":"We-x-imperative-X clause" , "WxQX":"We-x-qatal-X clause" , "WxYX":"We-x-yiqtol-X clause" , "xImX":"x-imperative-X clause" , "xQtX":"x-qatal-X clause" , "xYqX":"x-yiqtol-X clause" }
clause_types["unclear"] = { "CPen":"Casus pendens" , "Defc":"Defective clause atom" , "Ellp":"Ellipsis" , "MSyn":"Macrosyntactic sign" , "XPos":"Extraposition" , "Reop":"Reopening" , "Unkn":"Unknown" }

#}}}
