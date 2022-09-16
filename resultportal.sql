CREATE TABLE student(
	s_id varchar2(10) PRIMARY KEY,
	fname varchar2(15) NOT NULL,
	mname varchar2(15) NOT NULL,
	lname varchar2(15) NOT NULL,
	f_id varchar2(10),
	mobile_id varchar2(10),
	user_id varchar2(10),
	d_id varchar2(4)
);

CREATE TABLE faculty(
	f_id varchar2(10) PRIMARY KEY,
	fname varchar2(15) NOT NULL,
	mname varchar2(15) NOT NULL,
	lname varchar2(15) NOT NULL,
	join_date date,
	mobile_id varchar2(10),
	user_id varchar2(10),
	d_id varchar2(4)
);

CREATE TABLE login(
	user_id varchar2(10) PRIMARY KEY,
	password varchar2(20) NOT NULL,
	question varchar2(30) DEFAULT 'Choose Recovery Question',
	answer varchar2(30) NOT NULL
);

CREATE TABLE result(
	r_id varchar2(6) PRIMARY KEY,
	totalmarks number(5) NOT NULL,
	grade varchar2(2) NOT NULL,
	SPI number(4,2) NOT NULL,
	sem number(2) NOT NULL,
	s_id varchar2(10),
	f_id varchar2(10)
);

CREATE TABLE department(
	d_id varchar2(4) PRIMARY KEY,
	d_name varchar2(30) NOT NULL,
	est_year varchar2(4)
);

CREATE TABLE course(
	c_id varchar2(6) PRIMARY KEY,
	c_name varchar2(50) NOT NULL,
	credits number(1) NOT NULL,
	sem number(2) NOT NULL,
	marks number(3) NOT NULL,
	s_id varchar2(10),
	f_id varchar2(10),
	d_id varchar2(4),
	r_id varchar2(6)
);

CREATE TABLE mobile_number(
	mobile_id varchar2(10),
	mobileno number(15) NOT NULL,
	PRIMARY KEY(mobile_id,mobileno)
);

ALTER TABLE student ADD CONSTRAINT s_idverify CHECK(s_id LIKE '__BCE___');
ALTER TABLE student ADD CONSTRAINT S2F_refer FOREIGN KEY (f_id) REFERENCES faculty(f_id) on delete cascade;
ALTER TABLE student ADD CONSTRAINT smobileno FOREIGN KEY (mobile_id) REFERENCES mobile_number(mobile_id) on delete cascade;
ALTER TABLE student ADD CONSTRAINT slogininfo FOREIGN KEY (user_id) REFERENCES login(user_id) on delete cascade;
ALTER TABLE student ADD CONSTRAINT S2D_refer FOREIGN KEY (d_id) REFERENCES department(d_id) on delete cascade;

ALTER TABLE faculty ADD CONSTRAINT f_idverify CHECK(f_id LIKE 'NUFCE___');
ALTER TABLE faculty ADD CONSTRAINT fmobileno FOREIGN KEY (mobile_id) REFERENCES mobile_number(mobile_id) on delete cascade;
ALTER TABLE faculty ADD CONSTRAINT flogininfo FOREIGN KEY (user_id) REFERENCES login(user_id) on delete cascade;
ALTER TABLE faculty ADD CONSTRAINT F2D_refer FOREIGN KEY (d_id) REFERENCES department(d_id) on delete cascade;

ALTER TABLE login ADD CONSTRAINT user_idverify CHECK(user_id LIKE '__BCE___' or 'NUFCE___');
ALTER TABLE login ADD CONSTRAINT loginquestion CHECK(question IN ('Your Primary School Name','Your Favourite Sports Man','Your Favourite Hero','Your Favorite Color');

ALTER TABLE result ADD CONSTRAINT R2S_refer FOREIGN KEY (s_id) REFERENCES student(s_id) on delete cascade;
ALTER TABLE result ADD CONSTRAINT R2F_refer FOREIGN KEY (f_id) REFERENCES faculty(f_id) on delete cascade;

ALTER TABLE course ADD CONSTRAINT C2S_refer FOREIGN KEY (s_id) REFERENCES student(s_id) on delete cascade;
ALTER TABLE course ADD CONSTRAINT C2F_refer FOREIGN KEY (f_id) REFERENCES faculty(f_id) on delete cascade;
ALTER TABLE course ADD CONSTRAINT C2D_refer FOREIGN KEY (d_id) REFERENCES department(d_id) on delete cascade;
ALTER TABLE course ADD CONSTRAINT C2R_refer FOREIGN KEY (r_id) REFERENCES result(r_id) on delete cascade;

ALTER TABLE mobile_number ADD CONSTRAINT smnumber FOREIGN KEY (mobile_id) REFERENCES student(s_id) on delete cascade;



INSERT INTO mobile_number VALUES('19BCE059','9913472659');
INSERT INTO mobile_number VALUES('NUFCE001','9925565278');
INSERT INTO department VALUES('D001','CSE','2002');
INSERT INTO login VALUES('19BCE059','harshit','Your Primary School','Nirma');
INSERT INTO login VALUES('NUFCE001','ajay','Your Primary School','Nirma');
INSERT INTO faculty VALUES('NUFCE001','ajay','k','patel','12/May/2003','NUFCE001','NUFCE001','D001');
INSERT INTO student VALUES('19BCE059','harshit','r','gajipara','NUFCE001','M01','19BCE059','D001');
INSERT INTO result VALUES('R001','50','F','2.25','4','19BCE059','NUFCE001');
INSERT INTO course VALUES('2SP202','PS','3','2','98','19BCE059','NUFCE001','D001','R001');

drop table course;
drop table result;
drop table student;
drop table faculty;
drop table department;
drop table login;
drop table mobile_number;