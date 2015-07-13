delete from core_casestate;
vacuum;
insert into core_casestate (id,title,add_date,add_user_id) VALUES (1,'Opened','2014-01-01',1);
insert into core_casestate (id,title,add_date,add_user_id) VALUES (2,'Closed','2014-01-01',1);
insert into core_casestate (id,title,add_date,add_user_id) VALUES (3,'Archived','2014-01-01',1);
delete from core_client;
vacuum;
insert into core_client (id, name, surname, add_date, add_user_id) VALUES (1,'John', 'White', '2014-01-01', 1);
insert into core_client (id, name, surname, add_date, add_user_id) VALUES (2,'Mister', 'Black', '2014-01-01', 1);
delete from core_entrystate;
vacuum;
insert into core_entrystate (id, title, add_date, add_user_id) VALUES (1, 'Fee', '2014-01-01', 1);
insert into core_entrystate (id, title, add_date, add_user_id) VALUES (2, 'Disbursement', '2014-01-01', 1);
delete from core_matter;
vacuum;
insert into core_matter (id,title,add_date,add_user_id) VALUES (1, 'Matter One', '2014-01-01', 1);
insert into core_matter (id,title,add_date,add_user_id) VALUES (2, 'Matter Two', '2014-01-01', 1);

-- trigger
CREATE TRIGGER [case_after_insert]
AFTER INSERT
ON [core_case]
FOR EACH ROW
BEGIN
 update core_case set number =  (SELECT strftime('%Y','now') || '-' || substr('00' || new.id, -3, 3)) where id = new.id; 
END
