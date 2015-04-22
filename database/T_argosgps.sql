-- =============================================
-- Author:		Romain FABBRO
-- Create date: 2015-03-19
-- Description:	Rewrite T_argosgps Table
-- =============================================



USE [ecoReleve_Sensor]
GO

/****** Object:  Table [dbo].[T_argosgps]    Script Date: 19/03/2015 10:47:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

DROP Table [dbo].[T_argosgps]
GO


CREATE TABLE [dbo].[T_argosgps](
	[PK_id] [int] IDENTITY(1,1) NOT NULL,
	[FK_ptt] [int] NOT NULL,
	[type] [varchar](3) NOT NULL,
	[date] [datetime] NOT NULL,
	[lat] [numeric](9, 5) NOT NULL,
	[lon] [numeric](9, 5) NOT NULL,
	[ele] [int] NULL,
	[speed] [int] NULL,
	[course] [int] NULL,
	[checked] [bit] NOT NULL,
	[imported] [bit] NOT NULL,
	[lc] [varchar](1) NULL,
	[iq] [int] NULL,
	[nbMsg] [int] NULL,
	[nbMsg120] [int] NULL,
	[bestLevel] [int] NULL,
	[passDuration] [int] NULL,
	[nopc] [int] NULL,
	[freq] [float] NULL,
	[errorRadius] [int] NULL,
	[semiMajor] [int] NULL,
	[semiMinor] [int] NULL,
	[orientation] [tinyint] NULL,
	[hdop] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[PK_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

ALTER TABLE [dbo].[T_argosgps]  WITH CHECK ADD CHECK  (([checked]=(1) OR [checked]=(0)))
GO

ALTER TABLE [dbo].[T_argosgps]  WITH CHECK ADD CHECK  (([imported]=(1) OR [imported]=(0)))
GO

