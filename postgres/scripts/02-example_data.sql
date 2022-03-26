-- Create forums
INSERT INTO forum (name, description) VALUES ('General', 'General discussion on various topics');
INSERT INTO forum (name, description) VALUES ('Movies', 'Discussions related to movies and tv');
INSERT INTO forum (name, description) VALUES ('Meta', 'Discussion about discussions');
INSERT INTO forum (name, description) VALUES ('Technology', 'Everything related to technology');
INSERT INTO forum (name, description, private) VALUES ('Random', 'We do not talk about random', true);
-- Create accounts (non-login)
INSERT INTO account (username, password, email) VALUES ('matti', '', 'matti.meikalainen@eposti.com');
INSERT INTO account (username, password, email) VALUES ('maija', '', 'maija.meikalainen@eposti.com');
INSERT INTO account (username, password, email) VALUES ('<h1>HAXOR</h1>', '', '<h1>kaaleppi.meikalainen@eposti.com</h1>');
;
-- Create topics;
INSERT INTO topic (forum_id, account_id, title, body) VALUES (1, 1, 'Introduce yourself', 'Please introduce yourself here!');
INSERT INTO topic (forum_id, account_id, title, body) VALUES (1, 2, 'Am I the only one who thinks this?', 'Am I the only one who likes bread with butter?');
INSERT INTO topic (forum_id, account_id, title, body) VALUES (4, 3, 'I AM HAXOR', '<h1>I AM THE HAXOR! KNEEL BEFORE ME AND DESPAIR!!</h1>');
;
-- Create comments;
INSERT INTO comment (account_id, topic_id, body) VALUES (2, 1, 'Hi Im maija meikalainen. I like bread with butter.');
INSERT INTO comment (account_id, topic_id, body) VALUES (3, 1, '<h1>I AM HAXOR! LOLOLOLOLOLOLOLOLOLOLOLOLO</h1>');
INSERT INTO comment (account_id, topic_id, body) VALUES (1, 2, 'That sounds disgusting!');


-- Add kaaleppi to hidden forum 'Random'
INSERT INTO private_forum_account (account_id, forum_id) VALUES (3, 5);
