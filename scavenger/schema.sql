DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS rounds;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  phone_number TEXT UNIQUE NOT NULL
);

CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  item_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  points INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE TABLE rounds (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(item_id) REFERENCES items(id)
);

INSERT INTO items (name) VALUES ('Hat');
INSERT INTO items (name) VALUES ('Dog');
INSERT INTO items (name) VALUES ('Computer');
INSERT INTO items (name) VALUES ('Apple');
INSERT INTO items (name) VALUES ('Flower');
INSERT INTO items (name) VALUES ('Book');
INSERT INTO items (name) VALUES ('Shoe');
INSERT INTO items (name) VALUES ('Bus');
INSERT INTO items (name) VALUES ('Basketball');
INSERT INTO items (name) VALUES ('Cat');
INSERT INTO items (name) VALUES ('Brush');
INSERT INTO items (name) VALUES ('Broccoli');
INSERT INTO items (name) VALUES ('Cloud');
INSERT INTO items (name) VALUES ('Tree');
INSERT INTO items (name) VALUES ('Fish');
INSERT INTO items (name) VALUES ('Trophy');
INSERT INTO items (name) VALUES ('Lamp');
INSERT INTO items (name) VALUES ('Piano');
INSERT INTO items (name) VALUES ('Squirrel');
INSERT INTO items (name) VALUES ('Guitar');