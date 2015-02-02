

Create VIEW [dbo].[T_User_Full]
AS
SELECT
 SECURITE.dbo.TUsers.TUse_PK_ID as PK_id,
 SECURITE.dbo.TUsers.TUse_FirstName as firstname,
 SECURITE.dbo.TUsers.TUse_LastName as lastname,
 SECURITE.dbo.TUsers.TUse_Language as language_,
 SECURITE.dbo.TUsers.TUse_CreationDate as creation_date
FROM SECURITE.dbo.TUsers