CREATE TABLE IF NOT EXISTS pt (
-- Place where reference is found
ID         INTEGER PRIMARY KEY,      -- Automatically created key
a          VARCHAR(10),              -- Place in corpus where participant reference is found
Node       VARCHAR(15),              -- Node ID
Nodetype   VARCHAR(10),              -- Type of node: suffix (on word node!), word, phrase, etc
ClANr      INTEGER,                  -- Clause_atom number, as indicated by ETCBC
PhANr      INTEGER,                  -- Phrase_atom number, as indicated by ETCBC
WNr        INTEGER,                  -- Word number, as indicated by ETCBC
Level      INTEGER,                  -- Level of embedding as used in task QF+DSU and SQLite tables
Emb        INTEGER,                  -- Levels of embedding as indicated by ETCBC
DSU        VARCHAR(10),              -- ID of the DSU to which reference belongs

-- Place where first found
a1         VARCHAR(10),              -- Place in corpus where participant is found for the first time
Node1      VARCHAR(15),              -- Node ID of first reference to this participant
Nodetype1  VARCHAR(10),              -- Node type of first reference
ClANr1     INTEGER,                  -- Clause_atom number where participant is found for the first time
PhANr1     INTEGER,                  -- Phrase_atom number where participant is found for the first time
WNr1       INTEGER,                  -- Word number where participant is found for the first time
DSU1       VARCHAR(10),              -- ID of the DSU to which first reference belongs
Name       VARCHAR(50),              -- Identifying name / label for this participant

-- Previous participant reference
Preva      VARCHAR(10),              -- Place in corpus where previous reference is found
PrevNode   VARCHAR(15),              -- Node ID of previous reference
PrevNodetype VARCHAR(10),            -- Type of node: suffix (on word node!), word, phrase, etc
PrevClANr  INTEGER,                  -- Clause_atom number of previous reference
PrevPhANr  INTEGER,                  -- Phrase_atom number of previous reference
PrevWNr    INTEGER,                  -- Word number of previous reference
PrevCon    VARCHAR(10),              -- Context of previous participant reference in text
PrevLevel  INTEGER,                  -- Level of embedding of previous participant reference in text, as used in task QF+DSU and SQLite tables
PrevEmb    INTEGER,                  -- Levels of embedding of previous participant reference as indicated by ETCBC
PrevDSU    VARCHAR(10),              -- ID of the DSU to which previous reference belongs
PrevDes    VARCHAR(85),              -- Surface consonants of previous participant reference in text
PrevDestype VARCHAR(15),             -- Type of designation of previous reference in text
PrevRole   VARCHAR(15),              -- Role or grammatical function of previous reference in text
PrevP      VARCHAR(5),               -- Person of previous reference
PrevN      VARCHAR(5),               -- Number of previous reference
PrevG      VARCHAR(5),               -- Gender of previous reference
PrevPartSpeech VARCHAR(15),          -- Part of speech of previous reference
PrevLexset VARCHAR(15),              -- Lexical set of previous reference
PrevName   VARCHAR(50),              -- Identifying name / label of participant in previous reference

-- Previous reference to same participant
Refa       VARCHAR(10),              -- Place in corpus where previous reference to same participant is found
RefNode    VARCHAR(15),              -- Node ID of previous reference to same participant
RefNodetype VARCHAR(10),             -- Type of node: suffix (on word node!), word, phrase, etc
RefClANr   INTEGER,                  -- Clause_atom number of previous reference to same participant
RefPhANr   INTEGER,                  -- Phrase_atom number of previous reference to same participant
RefWNr     INTEGER,                  -- Word number of previous reference to same participant
RefCon     VARCHAR(10),              -- Context of previous reference to same participant
RefLevel   INTEGER,                  -- Level of embedding of previous reference to same participant, as used in task QF+DSU and SQLite tables
RefEmb     INTEGER,                  -- Levels of embedding of previous reference to same participant, as indicated by ETCBC
RefDSU     VARCHAR(10),              -- ID of the DSU to which previous reference to same participant belongs
RefDes     VARCHAR(85),              -- Surface consonants of previous reference to same participant
RefDestype VARCHAR(15),              -- Type of designation by which this participant is mentioned in previous reference
RefRole    VARCHAR(15),              -- Role or grammatical function of previous reference to same participant
RefP       VARCHAR(5),               -- Person of previous reference to same participant
RefN       VARCHAR(5),               -- Number of previous reference to same participant
RefG       VARCHAR(5),               -- Gender of previous reference to same participant
RefPartSpeech VARCHAR(15),           -- Part of speech of previous reference to same participant
RefLexset VARCHAR(15),               -- Lexical set of previous reference to same participant
RefInt     INTEGER,                  -- Number of different intervening participants between current and ref

-- Current reference
Con        VARCHAR(10),              -- Context of current reference
Des        VARCHAR(85),              -- Surface consonants of designation
Destype    VARCHAR(15),              -- Type of designation by which this participant is mentioned
Role       VARCHAR(15),              -- Role or grammatical function within the clause
P          VARCHAR(5),               -- Person of current reference
N          VARCHAR(5),               -- Number of current reference
G          VARCHAR(5),               -- Gender of current reference
PartSpeech VARCHAR(15),              -- Part of speech of current reference
Lexset     VARCHAR(15),              -- Lexical set of current reference
Anim       VARCHAR(10),              -- Animate (1) or non-animate (2)
Human      VARCHAR(10),              -- Human or non-human (nonhuman)
MinGram    VARCHAR(10),              -- Minimal encoding possible in this grammatical context
MinSem     VARCHAR(10),              -- Minimal encoding that would be semantically unambiguous in this context
Ext        VARCHAR(10),              -- How extensive is the current reference?
Nr         INTEGER,                  -- Counter how often the current referent (name) has been referred to in the corpus (including current reference)
NewDSU     VARCHAR(10),              -- Is current reference a new participant, already mentioned, active participant in same role, or active participant in different role (all within DSU)? 
NewChap    VARCHAR(10),              -- Is current reference a new participant, already mentioned, active participant in same role, or active participant in different role (all within chapter)? 
Col        VARCHAR(10),              -- Is the participant an individual, collective or an individual in a compound design?
ColPart    VARCHAR(25),              -- Name of collective / compound / individuals to which current reference belongs
MajDSU     VARCHAR(10),              -- Importance of the participant in current DSU
MajChap    VARCHAR(10),              -- Importance of the participant in current chapter
Var        VARCHAR(85),              -- Textual variants influencing the reading of this reference and its context

Tag         VARCHAR(15),             -- Unique tag (node + node_type) to refer to in other scripts
Referents   VARCHAR(100),            -- Referents included in this reference (if not identical with Name, but relevant in textual context)
Cltype      VARCHAR(10),             -- Type of the clause\_atom to which reference belongs as given by F.etcbc4\_ft\_typ.v(node)
Phtype      VARCHAR(10),             -- Type of the phrase\_atom to which reference belongs as given by F.etcbc4\_ft\_typ.v(node)
Phfunc      VARCHAR(10),             -- Function of the phrase to which reference belongs as given by F.etcbc4\_ft\_function.v(node)
SPhNr       VARCHAR(10),             -- Subphrase number
Sub         VARCHAR(5),              -- Specifies participant type: independent or a kind of sub-participant
InfoStruc   VARCHAR(50),	     -- Gives information about Information Structure (topic, focus, etc)
Center      VARCHAR(50),             -- Gives the center of reference

);
