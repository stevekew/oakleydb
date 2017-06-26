CREATE TABLE source ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(30)  NOT NULL  ,
	description          varchar(150)    ,
	active               bit  NOT NULL DEFAULT 1 ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  DEFAULT 0 ,
	validto              timestamp  DEFAULT 0 ,
	CONSTRAINT pk_source UNIQUE ( id ) ,
	CONSTRAINT pk_source_0 PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE TABLE style ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(100)  NOT NULL  ,
	basecurveid          int    ,
	url                  varchar(20000)    ,
	sourceid             int  NOT NULL  ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  DEFAULT 0 ,
	validto              timestamp  DEFAULT 0 ,
	CONSTRAINT pk_style UNIQUE ( id ) ,
	CONSTRAINT pk_style_0 PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_style ON style ( sourceid );

CREATE TABLE basecurve ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(20)  NOT NULL  ,
	sourceid             int    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	CONSTRAINT pk_basecurve PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_basecurve ON basecurve ( sourceid );

CREATE TABLE collection ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(100)  NOT NULL  ,
	url                  varchar(2000)    ,
	sourceid             int    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp   DEFAULT 0 ,
	validto              timestamp   DEFAULT 0 ,
	CONSTRAINT pk_collection PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_collection ON collection ( sourceid );

CREATE TABLE family ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(80)    ,
	sourceid             int  NOT NULL  ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  DEFAULT 0 ,
	validto              timestamp  DEFAULT 0 ,
	CONSTRAINT pk_family UNIQUE ( id ) ,
	CONSTRAINT pk_family_0 PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_family ON family ( sourceid );

CREATE TABLE familystylemap ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	familyid             int  NOT NULL  ,
	styleid              int  NOT NULL  ,
	sourceid             int    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  DEFAULT 0 ,
	validto              timestamp  DEFAULT 0 ,
	CONSTRAINT pk_familystylemap PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_familystylemap ON familystylemap ( familyid );

CREATE INDEX idx_familystylemap_0 ON familystylemap ( styleid );

CREATE TABLE fit ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(30)  NOT NULL  ,
	sourceid             int    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	CONSTRAINT pk_fit UNIQUE ( id ) ,
	CONSTRAINT pk_fit_0 PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_fit ON fit ( sourceid );

CREATE TABLE gender ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(30)    ,
	sourceid             int    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	CONSTRAINT pk_gender UNIQUE ( id ) ,
	CONSTRAINT pk_gender_0 PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_gender ON gender ( sourceid );

CREATE TABLE lenstype ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(100)  NOT NULL  ,
	sourceid             int    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  DEFAULT 0 ,
	validto              timestamp  DEFAULT 0 ,
	CONSTRAINT pk_lenstype UNIQUE ( id ) ,
	CONSTRAINT pk_lenstype_0 PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_lenstype ON lenstype ( sourceid );

CREATE TABLE material ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(100)  NOT NULL  ,
	sourceid             int    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  DEFAULT 0  ,
	validto              timestamp  DEFAULT 0  ,
	CONSTRAINT pk_material PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_material ON material ( sourceid );

CREATE TABLE lens ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(100)  NOT NULL  ,
	lenstypeid           int    ,
	base                 varchar(50)  NOT NULL  ,
	coating              varchar(50)    ,
	transmission         varchar(20)    ,
	transindex           int    ,
	purpose              varchar(50)    ,
	lighting             varchar(50)    ,
	url                  varchar(2000)    ,
	sourceid             int    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp   DEFAULT 0 ,
	validto              timestamp   DEFAULT 0 ,
	CONSTRAINT pk_lens UNIQUE ( id ) ,
	CONSTRAINT pk_lens_0 PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_lens ON lens ( sourceid );

CREATE INDEX idx_lens_0 ON lens ( lenstypeid );

CREATE TABLE model ( 
	id                   int  NOT NULL  AUTO_INCREMENT,
	name                 varchar(500)  NOT NULL  ,
	styleid              int    ,
	sku                  varchar(20)    ,
	framecolour          varchar(50)    ,
	lensid               int    ,
	fitid                int    ,
	genderid             int    ,
	listprice            varchar(20)    ,
	releasedate          varchar(30)    ,
	retiredate           varchar(30)    ,
	url                  varchar(2000)    ,
	sourceid             int    ,
	note                 varchar(100)    ,
	image                varchar(200)    ,
	imagesmall           varchar(200)    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp   DEFAULT 0 ,
	validto              timestamp   DEFAULT 0 ,
	CONSTRAINT pk_model PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE INDEX idx_model ON model ( sourceid );

CREATE INDEX idx_model_0 ON model ( styleid );

CREATE INDEX idx_model_1 ON model ( fitid );

CREATE INDEX idx_model_2 ON model ( genderid );

CREATE INDEX idx_model_3 ON model ( lensid );

ALTER TABLE basecurve ADD CONSTRAINT fk_basecurve_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE collection ADD CONSTRAINT fk_collection_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE family ADD CONSTRAINT fk_family_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE familystylemap ADD CONSTRAINT fk_familystylemap_family FOREIGN KEY ( familyid ) REFERENCES family( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE familystylemap ADD CONSTRAINT fk_familystylemap_style FOREIGN KEY ( styleid ) REFERENCES style( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE fit ADD CONSTRAINT fk_fit_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE gender ADD CONSTRAINT fk_gender_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE lens ADD CONSTRAINT fk_lens_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE lens ADD CONSTRAINT fk_lens_lenstype FOREIGN KEY ( lenstypeid ) REFERENCES lenstype( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE lenstype ADD CONSTRAINT fk_lenstype_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE material ADD CONSTRAINT fk_material_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE model ADD CONSTRAINT fk_model_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE model ADD CONSTRAINT fk_model_fit FOREIGN KEY ( fitid ) REFERENCES fit( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE model ADD CONSTRAINT fk_model_gender FOREIGN KEY ( genderid ) REFERENCES gender( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE model ADD CONSTRAINT fk_model_style FOREIGN KEY ( styleid ) REFERENCES style( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE model ADD CONSTRAINT fk_model_lens FOREIGN KEY ( lensid ) REFERENCES lens( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE style ADD CONSTRAINT fk_style_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

