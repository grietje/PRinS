CREATE TABLE IF NOT EXISTS enc (
ID         INTEGER PRIMARY KEY,      -- Automatically created key
Cl_type    VARCHAR(10),              -- Clause_type (F.etcbc4_ft_typ.v(node))
Ph_type    VARCHAR(10),              -- Phrase_type (F.etcbc4_ft_typ.v(node))
Ph_func    VARCHAR(15),              -- Phrase_function (F.etcbc4_ft_function.v(node))
Enc_options VARCHAR(100),            -- Options for encoding, given Cl_type and Ph_function
Enc_options_coded VARCHAR(15)       -- Options for encoding, coded with numbers indicating prominence

);
