SELECT 
dbo.Transactions.TransDate as DateAdded,
dbo.ItemMaster.ItemNo,
dbo.ItemMaster.CertAgency, 
dbo.ItemMaster.Description,
dbo.ItemMaster.SellPrice as CurrentSellPrice,
dbo.Inventory.Quantity,
dbo.ItemMaster.CertNo, 
dbo.ItemMaster.DiamondShape, 
ROUND(dbo.ItemMaster.SizeNominal, 2) as Carats,
dbo.ItemMaster.DiamondColor,
dbo.ItemMaster.DiamondQuality, 
dbo.ItemMaster.DiamondCutGrade,
dbo.ItemMaster.DiamondPolish, 
dbo.ItemMaster.DiamondSymmetry, 
dbo.ItemMaster.DiamondFluor, 
dbo.ItemMaster.StoneSize,
dbo.ItemMaster.WholesalePerUnitSell, 
dbo.ItemMaster.DiamondDepthPct, 
dbo.ItemMaster.DiamondTablePct, 
dbo.ItemMaster.DiamondCulet AS CuletSize, 
dbo.ItemMaster.UCBO2
FROM            
dbo.ItemMaster LEFT JOIN dbo.Inventory ON dbo.ItemMaster.ItemNo = dbo.Inventory.ItemNo
LEFT OUTER JOIN dbo.Transactions ON dbo.ItemMaster.ItemNo = dbo.Transactions.ItemNo
FULL OUTER JOIN dbo.InvoiceDetail ON dbo.ItemMaster.ItemNo = dbo.InvoiceDetail.ItemNo 
FULL OUTER JOIN dbo.InvoiceHeader ON dbo.InvoiceHeader.InvoiceNo = dbo.InvoiceDetail.InvoiceNo
FULL OUTER JOIN dbo.tblCustomers ON dbo.tblCustomers.CustomerID = dbo.InvoiceHeader.CustIDNo
WHERE
AND (dbo.Transactions.TransDate >= 'YYYY-MM-DD')
AND (dbo.ItemMaster.Type = 'CD') 
AND (dbo.Inventory.Quantity > 0)
AND (dbo.Transactions.OrdNo = 'Stock') 
AND (dbo.ItemMaster.ItemNo <> 'CERTS HOLD') 
AND LEFT(dbo.ItemMaster.CertNo,1) <> '*'
AND (
LEFT(dbo.Transactions.TransType, 19) = 'DiaTrans CERTS HOLD' 
OR LEFT(dbo.Transactions.TransType, 24) = 'DiaTrans from CERTS HOLD' 
OR LEFT(dbo.Transactions.TransType, 17) = 'DiaTrans EGL HOLD' 
OR LEFT(dbo.Transactions.TransType, 22) = 'DiaTrans from CERTS HOLD'
OR LEFT(dbo.Transactions.TransType, 28) = 'DiaTrans from Sanghvi & Sons' 
OR LEFT(dbo.Transactions.TransType, 27) = 'DiaTrans from Ritesh Export'
OR LEFT(dbo.Transactions.TransType, 19) = 'DiaTrans from TRLCL'
OR LEFT(dbo.Transactions.TransType, 17) = 'DiaTrans B25W1C9'
OR LEFT(dbo.Transactions.TransType, 29) = 'DiaTrans from ROSY BLUE INDIA'
OR LEFT(dbo.Transactions.TransType, 7) = 'DiaTrans P093011'
OR LEFT(dbo.Transactions.TransType, 22) = 'DiaTrans from Rapaport'
OR LEFT(dbo.Transactions.TransType, 26) = 'DiaTrans from Hari Krishna'
OR LEFT(dbo.Transactions.TransType, 18) = 'DiaTrans B25W1C9'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans B25WH99'
OR RIGHT(dbo.Transactions.TransType, 10) = dbo.ItemMaster.ItemNo
OR LEFT(dbo.Transactions.TransType, 22) = 'DiaTrans from EGL HOLD'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R509999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans O50Y2L9'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R609999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R709999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R809999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R909999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans RC19999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R40W2L9'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans B25W1C9'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans P100711'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R30Y1C9'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R40W2R9'
OR LEFT(dbo.Transactions.TransType, 17) = 'DiaTrans QUANTITY'
OR LEFT(dbo.Transactions.TransType, 21) = 'DiaTrans Mackley & Co'
OR LEFT(dbo.Transactions.TransType, 12) = 'MemoPurchase'
OR LEFT(dbo.Transactions.TransType, 24) = 'DiaTrans Justin Stannard'
OR LEFT(dbo.Transactions.TransType, 22) = 'DiaTrans S. Juwal & Co'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans F999999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R50W2V9'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans R409999'
OR LEFT(dbo.Transactions.TransType, 29) = 'DiaTrans from CAPITAL & ASSAY'
OR LEFT(dbo.Transactions.TransType, 14) = 'DiaTrans TRLCL'
OR LEFT(dbo.Transactions.TransType, 15) = 'DiaTrans R50W2C'
OR LEFT(dbo.Transactions.TransType, 21) = 'DiaTrans from RCR9999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans RCR9999'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans RC29999'
OR LEFT(dbo.Transactions.TransType, 21) = 'DiaTrans from RC19999'
OR LEFT(dbo.Transactions.TransType, 29) = 'DiaTrans from BECKERS JEWELRY'
OR LEFT(dbo.Transactions.TransType, 27) = 'DiaTrans from E-Z PAWN CORP'
OR LEFT(dbo.Transactions.TransType, 26) = 'DiaTrans VINCENTS JEWELERS'
OR LEFT(dbo.Transactions.TransType, 16) = 'DiaTrans pc1y1v9'
)
--GROUP BY dbo.ItemMaster.ItemNo




#Notes on results: If a was sold, then credited, then resold, then there will be duplicate records. 
#Dump the data into excel, then use this: =MIN(IF($A$2:$A$11588=A2,$D$2:$D$11588)) to find min Date Added and Max Date sold
#Remove duplicates, then recalculate days to sell manually
#Need to deal with multiple sell prices and take the max date sell price as well. 