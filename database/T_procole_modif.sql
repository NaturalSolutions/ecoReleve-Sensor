 -- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-01-09
-- Description:	Modify Portocole table + Ttheme etude_proto
-- set inactive protocole which have not .json model
-- =============================================



INSERT INTO [dbo].[TProtocole]
           ([Relation]
           ,[Caption]
           ,[Description]
           ,[Active]
           ,[Creation_date]
           ,[Creator]
           ,[Support])
     VALUES
           ('Vertebrate_Individual'	,'Vertebrate individual',	NULL,	1,	'2009-01-27, 11:10:06.167',	NULL,	NULL),
('Transects'	,'Transects',	NULL,	0,	'2014-01-09 08:10:10.237',	NULL,	NULL),
('Release_Individual',	'Release individual',	NULL,	0,	'2014-01-09 08:10:10.237',	NULL,	NULL),
('Phytosociology_habitat','Phytosociology habitat',	NULL,	1,	'2014-01-09 08:10:10.237',	NULL,	NULL),
('Phytosociology_releve',	'Phytosociology releve',	NULL,	1,	'2014-01-09 08:10:10.237',	NULL,	NULL),
('Sampling',	'Sampling',	NULL,	0,	'2014-01-09 08:10:10.237',	NULL,	NULL),
('Habitat_stratified',	'Habitat stratified',	NULL,	0,	'2014-01-09 08:10:10.237',	NULL,	NULL)

GO


UPDATE  [dbo].[TProtocole] SET Active = 0
where Relation not in ('Bird_Biomtry','Building_and_Activities','Chiroptera_capture',
'Chiroptera_detection','Phytosociology_habitat','Phytosociology_releve','Sighting_conditions',
'Simplified_Habitat','Station_Description','Station_equipment','Track_clue','Vertebrate_Group',
'Vertebrate_Individual_Death','Vertebrate_Individual')



INSERT INTO [dbo].[TProt_TTheEt] VALUES 
(53,	31),
(54,	31),
(24,	31),
(32,	34),
(9,	34),
(20,	34),
(22,	34),
(21,	34),
(59,	34),
(57,	34),
(58,	34),
(22,	35),
(9	,35),
(32,	35)