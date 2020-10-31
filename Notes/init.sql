-- sqlite3 main.db < init.sql

-- Init data roles
INSERT INTO role (name, has_full_access)
VALUES ('admin', 1),('user', 0);

-- Init data types
INSERT INTO note_type (name)
VALUES ('checklist'),('note');

-- Init data tags
INSERT INTO note_tag (name)
VALUES ('todo'),('grocary');

