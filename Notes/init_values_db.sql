USE main.db;
GO

-- Init data roles
INSERT INTO role (name, has_access)
VALUES ('admin', True),('user', False);

-- Init data types
INSERT INTO note_type (name)
VALUES ('checklist'),('note');

-- Init data tags
INSERT INTO note_tags (name)
VALUES ('todo'),('grocary');

