ALTER TABLE users DROP COLUMN id;
ALTER TABLE users CHANGE COLUMN gitlab_id id INTEGER;
ALTER TABLE users ADD PRIMARY KEY (id);
ALTER TABLE projects DROP COLUMN id;
UPDATE rel_project_host SET project_id=121 WHERE id > 2 AND id <= 7;
ALTER TABLE projects CHANGE COLUMN project_id id INTEGER;
