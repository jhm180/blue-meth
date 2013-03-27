use sells;
load data local infile '/home/oliver/rapnet_data/Rapnet_20130301_Main.csv' into table sells_tmp
fields terminated by ',' enclosed by '"' escaped by '\\'
ignore 1 lines
(             
     Seller,
     SellerId,
     SellerCode,
     Shape,
     Carat,
     Color,
     Clarity,
     CutGrade,
     Price,
     PctRap,
     Cert,
     Depth,
     `Table`,
     Girdle,
     Culet,
     Polish,
     Sym,
     Fluor,
     Meas,
     `Comment`,
     NumStones,
     CertNum,
     StockNum,
     Make,
     @dateVal,
     City,
     State,
     Country,
     Image
)
set Date = str_to_date(@dateVal, '%m/%d/%Y %h:%i:%s %p');