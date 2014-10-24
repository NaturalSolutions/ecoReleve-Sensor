USE [ecoReleve_Data]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author        : Natural Solutions (Thomas PEEL)
-- Creation date : 12/08/2014
-- Description   : History of individuals' characteristics.
-- Modified on   : -
-- Modified by   : -
-- =============================================

/***** Indexes *****/
CREATE NONCLUSTERED INDEX [idx_TObjCaracValue_FKobjectFKcaracBeginDate_With_ValueValuePrecisionEndDate] ON [dbo].[TObj_Carac_value] 
(
	[fk_object] ASC,
	[Fk_carac] ASC,
	[begin_date] DESC
)
INCLUDE ( [value],
[value_precision],
[end_date]) WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = ON, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON, FILLFACTOR = 80) ON [PRIMARY]
GO
CREATE UNIQUE NONCLUSTERED INDEX [idx_TObjCaracType_PK_With_Label] ON [dbo].[TObj_Carac_type] 
(
	[Carac_type_Pk] ASC
)
INCLUDE ( [label]) WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
GO

/***** View *****/
Create VIEW [dbo].[V_Individuals_History] 
AS 
select fk_object as ind_id, Fk_carac, COALESCE(value_precision, value) as value, label, begin_date, end_date
from [dbo].[TObj_Carac_value]
inner join [dbo].[TObj_Carac_type]
  on Fk_carac = Carac_type_Pk
GO