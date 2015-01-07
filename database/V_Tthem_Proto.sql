-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-01-06
-- Description:	create view for relationship between Field activity and Porotocoles
-- =============================================


USE [ecoReleve_Data]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




CREATE view [dbo].[V_TThem_Proto]
 AS
SELECT t.TProt_PK_ID as theme_id,
t.Caption as theme_name,
t.Actif as theme_active,
pt.TTheEt_PK_ID as proto_id,
p.Caption as proto_name,
p.Active as proto_active,
p.Relation as proto_relation

FROM [dbo].[TThemeEtude] t join [dbo].[TProt_TTheEt] pt on t.TProt_PK_ID=pt.TProt_PK_ID
JOIN [dbo].[TProtocole] p on pt.TTheEt_PK_ID= p.TTheEt_PK_ID

GO