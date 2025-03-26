DROP TABLE IF EXISTS jobs CASCADE;

CREATE TABLE jobs (
    job_id	BIGSERIAL PRIMARY KEY,
    job_code VARCHAR(50) UNIQUE NOT NULL,
    job_title	VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO jobs (job_code, job_id, job_title) VALUES
	('AC_ACCOUNT', '1', 'Ac Account'),
	('AC_MGR', '2', 'Ac Mgr'),
	('AD_ASST', '3', 'Ad Asst'),
	('AD_PRES', '4', 'Ad Pres'),
	('AD_VP', '5', 'Ad Vp'),
	('FI_ACCOUNT', '6', 'Fi Account'),
	('FI_MGR', '7', 'Fi Mgr'),
	('HR_REP', '8', 'Hr Rep'),
	('IT_PROG', '9', 'It Prog'),
	('MK_MAN', '10', 'Mk Man'),
	('MK_REP', '11', 'Mk Rep'),
	('PR_REP', '12', 'Pr Rep'),
	('PU_CLERK', '13', 'Pu Clerk'),
	('PU_MAN', '14', 'Pu Man'),
	('SH_CLERK', '15', 'Sh Clerk'),
	('ST_CLERK', '16', 'St Clerk'),
	('ST_MAN', '17', 'St Man');