CREATE TABLE IF NOT EXISTS enc (
ID         INTEGER PRIMARY KEY,      -- Automatically created key
Cl_type    VARCHAR(10),              -- Clause_type
Ph_func    VARCHAR(15),              -- Phrase_function
Enc_types  VARCHAR(100),             -- Types of encoding occurring in phrases with clause_type and phrase_function
Enc_coded  VARCHAR(50),              -- Types of encoding, coded with numbers according to prominence

);
