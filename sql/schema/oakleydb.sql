CREATE TABLE basecurve ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(20)  NOT NULL  
 ) engine=InnoDB;

CREATE TABLE fit ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(30)  NOT NULL  
 ) engine=InnoDB;

CREATE TABLE gender ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(30)    
 ) engine=InnoDB;

CREATE TABLE source ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(30)  NOT NULL  ,
	description          varchar(150)    ,
	enabled              bit  NOT NULL DEFAULT 1 ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  NOT NULL DEFAULT '0000-00-00 00:00:00' ,
	validto              timestamp  NOT NULL DEFAULT '0000-00-00 00:00:00' ,
	CONSTRAINT pk_source UNIQUE ( id ) 
 ) engine=InnoDB;

CREATE TABLE collection ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(100)  NOT NULL  ,
	url                  varchar(2000)    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp    ,
	validto              timestamp    ,
	sourceid             int UNSIGNED   
 ) engine=InnoDB;

CREATE INDEX idx_collection ON collection ( sourceid );

CREATE TABLE family ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(60)    ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  NOT NULL DEFAULT '0000-00-00 00:00:00' ,
	validto              timestamp  NOT NULL DEFAULT '0000-00-00 00:00:00' ,
	sourceid             int UNSIGNED NOT NULL  ,
	CONSTRAINT pk_family UNIQUE ( id ) 
 );

CREATE INDEX idx_family ON family ( sourceid );

CREATE TABLE lens ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(100)  NOT NULL  ,
	base                 varchar(50)  NOT NULL  ,
	coating              varchar(50)    ,
	transmission         int UNSIGNED   ,
	transindex           int UNSIGNED   ,
	purpose              varchar(50)    ,
	lighting             varchar(50)    ,
	typeid               int UNSIGNED   ,
	url                  varchar(2000)    ,
	inserttime           timestamp   DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp    ,
	validto              timestamp    ,
	sourceid             int UNSIGNED   
 ) engine=InnoDB;

CREATE INDEX idx_lens ON lens ( sourceid );

CREATE TABLE material ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(100)  NOT NULL  ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp    ,
	validto              timestamp    ,
	sourceid             int UNSIGNED   
 ) engine=InnoDB;

CREATE INDEX idx_material ON material ( sourceid );

CREATE TABLE style ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(100)  NOT NULL  ,
	inserttime           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp  NOT NULL DEFAULT '0000-00-00 00:00:00' ,
	validto              timestamp  NOT NULL DEFAULT '0000-00-00 00:00:00' ,
	sourceid             int UNSIGNED NOT NULL  ,
	familyid             int UNSIGNED NOT NULL  ,
	url                  varchar(20000)    ,
	basecurve            double UNSIGNED   ,
	CONSTRAINT pk_style UNIQUE ( id ) 
 );

CREATE INDEX idx_style ON style ( sourceid );

CREATE INDEX idx_style_0 ON style ( familyid );

CREATE TABLE model ( 
	id                   int UNSIGNED NOT NULL  ,
	name                 varchar(500)  NOT NULL  ,
	inserttime           timestamp   DEFAULT CURRENT_TIMESTAMP ,
	validfrom            timestamp    ,
	validto              timestamp    ,
	sourceid             int UNSIGNED   ,
	styleid              int UNSIGNED   ,
	sku                  varchar(20)    ,
	listprice            varchar(20)    ,
	url                  varchar(2000)    
 ) engine=InnoDB;

CREATE INDEX idx_model ON model ( sourceid );

CREATE INDEX idx_model_0 ON model ( styleid );

ALTER TABLE collection ADD CONSTRAINT fk_collection_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE family ADD CONSTRAINT fk_family_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE lens ADD CONSTRAINT fk_lens_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE material ADD CONSTRAINT fk_material_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE model ADD CONSTRAINT fk_model_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE model ADD CONSTRAINT fk_model_style FOREIGN KEY ( styleid ) REFERENCES style( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE style ADD CONSTRAINT fk_style_source FOREIGN KEY ( sourceid ) REFERENCES source( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE style ADD CONSTRAINT fk_style_family FOREIGN KEY ( familyid ) REFERENCES family( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

