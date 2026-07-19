-- Creates the tasks table for the Task API.
-- Run this once against your todo_db database to set up the schema.

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

-- Seed with the same 3 example tasks the in-memory version started with,
-- so behavior looks identical after the switch.
INSERT INTO tasks (title, done) VALUES
    ('Buy milk', FALSE),
    ('Walk the dog', FALSE),
    ('Finish assignment', TRUE)
ON CONFLICT DO NOTHING;
