-- Active: 1669134495072@@127.0.0.1@5432@postgres
DROP TABLE IF EXISTS lms_TaskPacks_Tasks;
DROP TABLE IF EXISTS lms_Solutions;
DROP TABLE IF EXISTS lms_TaskPacks;
DROP TABLE IF EXISTS lms_Tasks;
DROP TABLE IF EXISTS lms_UserProfiles;

CREATE TABLE IF NOT EXISTS lms_UserProfiles ( 
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    password VARCHAR(100),
    username VARCHAR(100),
    grup VARCHAR(100),
    email VARCHAR(128),
    last_login DATE
);

-- CREATE TABLE IF NOT EXISTS lms_user(
--     user_profiles_id FOREIGN KEY lms,
    
-- )

ALTER TABLE lms_UserProfiles drop column user_id;

CREATE TABLE IF NOT EXISTS lms_Tasks(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    filename VARCHAR(100),
    theme VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS lms_TaskPacks(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Student_ID    int REFERENCES lms_UserProfiles (id) ON UPDATE CASCADE ON DELETE CASCADE,
    Teacher_ID    int REFERENCES lms_UserProfiles (id) ON UPDATE CASCADE,
    duetime Date
);

CREATE TABLE IF NOT EXISTS lms_Solutions(
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Student_ID    int REFERENCES lms_UserProfiles (id) ON UPDATE CASCADE ON DELETE CASCADE,
    Teacher_ID    int REFERENCES lms_UserProfiles (id) ON UPDATE CASCADE ON DELETE CASCADE,
    Taskpack_id  int REFERENCES lms_TaskPacks (id) ON UPDATE CASCADE ON DELETE CASCADE,
    grade INT,
    sendtime Date,
    filename VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS lms_TaskPacks_Tasks(
    Tasks_id   int REFERENCES lms_Tasks (id) ON UPDATE CASCADE ON DELETE CASCADE,
    TaskPacks_id int REFERENCES lms_TaskPacks (id) ON UPDATE CASCADE
    );

CREATE OR REPLACE FUNCTION set_sendtime() 
RETURNS TRIGGER AS $$
BEGIN
  NEW.sendtime = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_sendtime_trigger
BEFORE INSERT ON lms_Solutions
FOR EACH ROW
EXECUTE FUNCTION set_sendtime();

CREATE OR REPLACE FUNCTION update_grade_trigger()
RETURNS TRIGGER AS $$
BEGIN
IF NEW.sendtime < TaskPacks.duetime THEN
NEW.grade := 0;
END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

drop trigger check_sendtime_trigger on lms_solutions;
CREATE TRIGGER check_sendtime_trigger
BEFORE INSERT OR UPDATE ON lms_Solutions
FOR EACH ROW
EXECUTE FUNCTION update_grade_trigger();

select * from lms_tasks;

select * from lms_taskpacks_tasks;

select * from lms_taskpacks;

ALTER TABLE lms_userprofiles ADD COLUMN "has_module_perms" BOOLEAN;
ALTER TABLE lms_userprofiles DROP COLUMN has_module_perms;

UPDATE lms_userprofiles SET is_staff = False;

BEGIN;
TRUNCATE "lms_taskpacks", "django_session", "lms_solutions", "auth_user_user_permissions", "lms_taskpacks_tasks", "auth_user_groups", "auth_user", "django_content_type", "django_admin_log", "auth_group_permissions", "lms_userprofiles", "auth_group", "auth_permission", "lms_tasks" RESTART IDENTITY;
COMMIT;


TRUNCATE "django_content_type", "auth_user", "lms_tasks", "django_admin_log", "auth_permission", "auth_group_permissions", "lms_taskpacks_tasks", "auth_user_groups", "auth_group", "auth_user_user_permissions", "lms_taskpacks", "lms_solutions", "django_session", "lms_userprofiles" RESTART IDENTITY;

INSERT INTO LMS_TASKS VALUES
(0, '0.txt', 'Programming'),
(1, '1.txt', 'Philosophy'),
(2, '2.txt', 'Biology'),
(3, '3.txt', 'Literature'),
(4, '4.txt', 'Literature'),
(5, '5.txt', 'Mathematics'),
(6, '6.txt', 'Literature'),
(7, '7.txt', 'Literature'),
(8, '8.txt', 'Mathematics'),
(9, '9.txt', 'Philosophy'),
(10, '10.txt', 'Literature'),
(11, '11.txt', 'Programming'),
(12, '12.txt', 'Engineering'),
(13, '13.txt', 'Biology'),
(14, '14.txt', 'Biology'),
(15, '15.txt', 'Literature'),
(16, '16.txt', 'Biology'),
(17, '17.txt', 'Philosophy'),
(18, '18.txt', 'Literature'),
(19, '19.txt', 'Engineering'),
(20, '20.txt', 'Programming'),
(21, '21.txt', 'Biology'),
(22, '22.txt', 'Literature'),
(23, '23.txt', 'Biology'),
(24, '24.txt', 'Programming'),
(25, '25.txt', 'Programming'),
(26, '26.txt', 'Biology'),
(27, '27.txt', 'Literature'),
(28, '28.txt', 'Philosophy'),
(29, '29.txt', 'Programming'),
(30, '30.txt', 'Philosophy'),
(31, '31.txt', 'Philosophy'),
(32, '32.txt', 'Literature'),
(33, '33.txt', 'Biology'),
(34, '34.txt', 'Mathematics'),
(35, '35.txt', 'Engineering'),
(36, '36.txt', 'Mathematics'),
(37, '37.txt', 'Engineering'),
(38, '38.txt', 'Biology'),
(39, '39.txt', 'Mathematics'),
(40, '40.txt', 'Literature'),
(41, '41.txt', 'Biology'),
(42, '42.txt', 'Biology'),
(43, '43.txt', 'Mathematics'),
(44, '44.txt', 'Programming'),
(45, '45.txt', 'Mathematics'),
(46, '46.txt', 'Literature'),
(47, '47.txt', 'Literature'),
(48, '48.txt', 'Literature'),
(49, '49.txt', 'Engineering'),
(50, '50.txt', 'Programming'),
(51, '51.txt', 'Literature'),
(52, '52.txt', 'Mathematics'),
(53, '53.txt', 'Biology'),
(54, '54.txt', 'Programming'),
(55, '55.txt', 'Engineering'),
(56, '56.txt', 'Engineering'),
(57, '57.txt', 'Mathematics'),
(58, '58.txt', 'Literature'),
(59, '59.txt', 'Biology'),
(60, '60.txt', 'Mathematics'),
(61, '61.txt', 'Mathematics'),
(62, '62.txt', 'Programming'),
(63, '63.txt', 'Programming'),
(64, '64.txt', 'Biology'),
(65, '65.txt', 'Biology'),
(66, '66.txt', 'Biology'),
(67, '67.txt', 'Literature'),
(68, '68.txt', 'Literature'),
(69, '69.txt', 'Engineering'),
(70, '70.txt', 'Literature'),
(71, '71.txt', 'Biology'),
(72, '72.txt', 'Programming'),
(73, '73.txt', 'Biology'),
(74, '74.txt', 'Engineering'),
(75, '75.txt', 'Philosophy'),
(76, '76.txt', 'Programming'),
(77, '77.txt', 'Philosophy'),
(78, '78.txt', 'Philosophy'),
(79, '79.txt', 'Engineering'),
(80, '80.txt', 'Engineering'),
(81, '81.txt', 'Biology'),
(82, '82.txt', 'Literature'),
(83, '83.txt', 'Biology'),
(84, '84.txt', 'Mathematics'),
(85, '85.txt', 'Engineering'),
(86, '86.txt', 'Literature'),
(87, '87.txt', 'Philosophy'),
(88, '88.txt', 'Programming'),
(89, '89.txt', 'Philosophy'),
(90, '90.txt', 'Programming'),
(91, '91.txt', 'Mathematics'),
(92, '92.txt', 'Literature'),
(93, '93.txt', 'Engineering'),
(94, '94.txt', 'Programming'),
(95, '95.txt', 'Literature'),
(96, '96.txt', 'Mathematics'),
(97, '97.txt', 'Philosophy'),
(98, '98.txt', 'Literature'),
(99, '99.txt', 'Philosophy');