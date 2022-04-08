/*
    UserID          Username        Password

    1               dfriend         Hello
    2               billybob        World
    3               sallysam        securepassword
    4               asai            puppies
*/
INSERT INTO user (username, firstname, lastname, password, face_enabled)
VALUES
    ('dfriend', 'Devon', 'Friend', 'pbkdf2:sha256:260000$pbP7GqcpXKihT3o5$2b4f4dc5ffabc4a8e2aef264053dcd5a6cf27d7426e530bf7d91a5091db805bb', 1),
    ('billybob', 'Billy', 'Bob', 'pbkdf2:sha256:260000$X0qKzOSxvM0bLsiF$fb33388404b02069b9b6cda47ba8b37f673e6a64c90f497969bea117aa00871a', 0),
    ('sallysam', 'Sally', 'Sam', 'pbkdf2:sha256:260000$xGACic5TpCVmFVZE$6f6a4ff3bd688859a0ef3078ea4eb6eade0f6b69ccabbc6a6bf88b76b883139e', 0),
    ('asai', 'Aswin', 'S.', 'pbkdf2:sha256:260000$TY5EuLvxONEkdgCo$ae2ddf738c5892d02ac8e8e066a157d557bd8664e3ef81f94f570778be1da1d8', 0),
    ('declanb', 'Declan', 'Byrne', 'pbkdf2:sha256:260000$o6llXXwTVKK6BHpb$779002a371a828f41bead5999db8073ec31580c03e09cc745d109a0a60a183c6', 1);

INSERT INTO code (code, codename, user_id)
VALUES
    ('1234', 'Default', 1),
    ('2070254', "Devon's Super Secret Code", 1),
    ('30495', 'Cool Code', 1),
    ('42066', "Bob's Code", 2),
    ('98789', "Billy's Super Secret Code", 2),
    ('1984398', "Sally's Awesome Code", 3),
    ('4542', "Aswin's Code", 4),
    ('6561', "Declan's Code", 5);

-- Do not add anything after the current date
INSERT INTO log (user_id, username, codename, verifDate, verifTime, success)
VALUES
    (1, 'dfriend', 'N/A', '2020-12-06', '15:12:00', 0),
    (1, 'dfriend', 'Cool Code', '2020-12-06', '15:13:05', 1),
    (1, 'dfriend', 'Cool Code', '2019-11-16', '01:00:00', 1),
    (1, 'dfriend', 'N/A', '2022-01-01', '11:22:59', 0),
    (1, 'dfriend', 'Default', '2022-01-01', '11:24:14', 1),
    (1, 'dfriend', 'Default', '2022-01-01', '12:12:10', 1),
    (1, 'dfriend', "Devon's Super Secret Code", '2021-05-16', '21:45:04', 1),
    (1, 'dfriend', "Devon's Super Secret Code", '2021-05-16', '22:45:04', 1),
    (1, 'dfriend', "Devon's Super Secret Code", '2021-05-16', '23:45:04', 1),
    (1, 'dfriend', "Devon's Super Secret Code", '2021-05-16', '20:45:04', 1),
    (2, 'billybob', "N/A", '2020-02-06', '15:12:00', 0),
    (2, 'billybob', "Bob's Code", '2018-11-10', '15:13:05', 1),
    (2, 'billybob', "N/A", '2018-10-11', '01:01:00', 0),
    (2, 'billybob', "N/A", '2022-01-01', '02:23:33', 0),
    (2, 'billybob', "Billy's Super Secret Code", '2022-01-01', '05:10:14', 1),
    (2, 'billybob', "Billy's Super Secret Code", '2022-01-01', '06:09:12', 1),
    (2, 'billybob', "Bob's Code", '2018-05-16', '19:19:45', 1),
    (3, 'sallysam', "N/A", '2015-10-16', '10:22:00', 0),
    (3, 'sallysam', "Sally's Awesome Code", '2015-10-16', '10:23:05', 1),
    (3, 'sallysam', "Sally's Awesome Code", '2016-07-11', '01:03:00', 1),
    (3, 'sallysam', "N/A", '2017-01-01', '11:22:59', 0),
    (5, 'declanb', 'N/A', '2020-12-06', '15:12:00', 0),

    (4, 'asai', "Aswin's Code", '2022-03-02', '05:45:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-02', '06:20:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-09', '05:50:01', 1),
    (4, 'asai', "Aswin's Code", '2022-03-09', '07:00:10', 1),
    (4, 'asai', "Aswin's Code", '2022-03-16', '06:15:14', 1),
    (4, 'asai', "Aswin's Code", '2022-03-16', '05:20:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-23', '06:00:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-23', '05:30:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-23', '06:12:40', 1),
    (4, 'asai', "Aswin's Code", '2022-03-03', '05:35:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-03', '06:10:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-10', '05:30:01', 1),
    (4, 'asai', "Aswin's Code", '2022-03-10', '07:00:10', 1),
    (4, 'asai', "Aswin's Code", '2022-03-17', '06:05:14', 1),
    (4, 'asai', "Aswin's Code", '2022-03-17', '05:10:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-24', '06:10:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-24', '05:20:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-24', '06:12:40', 1),
    (4, 'asai', "Aswin's Code", '2022-03-24', '05:45:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-04', '05:35:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-04', '06:00:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-11', '05:10:01', 1),
    (4, 'asai', "Aswin's Code", '2022-03-11', '07:00:10', 1),
    (4, 'asai', "Aswin's Code", '2022-03-18', '06:02:14', 1),
    (4, 'asai', "Aswin's Code", '2022-03-18', '05:13:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-25', '06:10:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-25', '05:20:00', 1),
    (4, 'asai', "Aswin's Code", '2022-03-25', '06:11:40', 1),
    (4, 'asai', "Aswin's Code", '2022-03-25', '05:23:00', 1),
    
    (5, 'declanb', 'Face', '2020-12-06', '15:13:05', 1),
    (5, 'declanb', 'Face', '2019-11-16', '01:00:00', 1),
    (5, 'declanb', 'N/A', '2022-01-01', '11:22:59', 0),
    (5, 'declanb', "Declan's Code", '2022-01-01', '11:24:14', 1),
    (5, 'declanb', "Declan's Code", '2022-01-01', '12:12:10', 1),
    (5, 'declanb', "Face", '2021-05-16', '21:45:04', 1),
    (5, 'declanb', "Face", '2021-05-16', '22:45:04', 1),
    (5, 'declanb', "Declan's Code", '2021-05-16', '23:45:04', 1),
    (5, 'declanb', "Declan's Code", '2021-05-16', '20:45:04', 1);
