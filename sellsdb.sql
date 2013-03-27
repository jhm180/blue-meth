use sells;
drop table if exists sells;

create table sells (
Seller text,
SellerId bigint,
SellerCode text,
Shape text,
Weight numeric,
Color text,
FancyColor text,
FancyIntensity text,
FancyOvertone text,
Clarity text,
CutGrade text,
Polish text,
Symmetry text,
FluorescenceColor text,
FluorescenceIntensity text,
Fluorescence text,
Measurements text,
MeasLength numeric,
MeasWidth numeric,
MeasDepth numeric,
Ratio numeric,
Lab text,
CertNum text,
StockNum text,
Treatment text,
Price decimal,
DiscountPrice decimal,
CashPrice decimal,
CashDiscountPct decimal,
CashTotalPrice decimal,
Availability text,
DepthPct decimal,
TablePct decimal,
Girdle text,
GirdleMin text,
GirdleMax text,
Culet text,
CuletSize text,
CuletCondition text,
CrownHeight numeric,
PavilionDepth numeric,
Comment text,
City text,
State text,
Country text,
IsMatchedPairSeparable boolean,
PairStockNum text,
ParcelNumStones int,
CertificateURL text,
LotNum bigint primary key,
RecordDate datetime
);

drop table if exists sells_event_codes;
create table sells_event_codes
(
Code int primary key auto_increment,
Description text not null
);

insert into sells_event_codes (Description) values
    ('Added'), ('Removed'), ('PriceChanged');

drop table if exists sells_events;
create table sells_events (
EventId bigint NOT NULL AUTO_INCREMENT,
LotNum bigint NOT NULL,
Price decimal,
Date datetime,
EventDate datetime,
EventCode int NOT NULL,
PRIMARY KEY (EventId),
INDEX USING HASH (LotNum),
INDEX USING HASH (EventCode)
);

drop procedure track_changes if exists
-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `track_changes`(loadDate datetime)
BEGIN
DECLARE EXIT HANDLER
    FOR SQLEXCEPTION, SQLWARNING, NOT FOUND
        ROLLBACK;
-- must only be called after bulk load into sells_tmp
-- add 'removed' event for old active sells that aren't in new active sells
-- add 'price changed' event for sells with price changes
start transaction;
set @removeCode = (select Code from sells_event_codes c where c.Description = 'Removed');
set @readdCode  = (select Code from sells_event_codes c where c.Description = 'ReAdded');
set @priceCode = (select Code from sells_event_codes c where c.Description = 'PriceChanged');
insert into sells_events
    (LotNum, Price, `EventDate`, EventCode)
    select s.LotNum, s.Price, @loadDate, @removeCode
        from active_sells s where s.lotnum not in
            (select lotnum from sells_tmp);
    
insert into sells 
    select * from sells_tmp where lotnum not in 
        (select lotnum from sells s);
        
-- insert a 'readd' event for entries in sells_tmp
-- that are currently marked as 'removed' in the sells_events table            
insert into sells_events
    (LotNum, Price, `EventDate`, EventCode)
    select s.LotNum, s.Price, @loadDate, @readdCode
        from (select s.LotNum, s.Price from sells s
                join (select LotNum, max(EventDate) from sells_events where EventCode = @removeCode) se
                    on s.lotnum = se.lotnum
            ) s
        join sells_tmp a
            on s.lotnum = a.lotnum;

-- insert a price-change event for prices that have changed
insert into sells_events
    (LotNum, Price, `EventDate`, EventCode)
    select s.LotNum, a.Price, @loadDate, @priceCode
        from sells s
        join sells_tmp a
            on s.lotnum = a.lotnum
        where not s.price = a.price

drop table active_sells;
rename table sells_tmp to active_sells;
commit;
END

