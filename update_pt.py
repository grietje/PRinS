

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
    Node = eval(Node[0])
    parents = give_me_your_parents_up_to(Node)
    for x in parents:
        if F.etcbc4_db_otype.v(x) == "phrase":
            c.execute("update pt set Phfunc=:Phfunc where Node=:Node", {"Phfunc":F.etcbc4_ft_function.v(x),"Node":Node})
        elif F.etcbc4_db_otype.v(x) == "subphrase":
            c.execute("update pt set SPhNr=:SPhNr where Node=:Node", {"SPhNr":F.etcbc4_ft_number.v(x),"Node":Node})
#}}}
