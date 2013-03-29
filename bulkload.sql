drop table if exists listing_tmp;
create table listing_tmp like listing;
LOAD DATA LOCAL INFILE '/home/oliver/rapnet_data/Rapnet_20130303_Main.csv' INTO TABLE listing_tmp
fields terminated by ',' enclosed by '"' escaped by '\\'
ignore 1 lines
(              LotNum,
               Owner,
               Shape,
               Carat,
               Color,
               Clarity,
               CutGrade,
               Price,
               PctRap,
               Cert,
               Depth,
               TableWidth,
               Girdle,
               Culet,
               Polish,
               Sym,
               Fluor,
               Meas,
               RapnetComment,
               NumStones,
               CertNum,
               StockNum,
               Make,
               @dateVal,
               City,
               State,
               Country,
               Image)
set Date = str_to_date(@dateVal, '%m/%d/%Y %h:%i:%s %p');