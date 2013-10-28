DELIMITER ;
drop schema if exists rapnet_listings;
create schema rapnet_listings;
use rapnet_listings;

create table listing (
LotNum bigint primary key,
Owner text,
Shape text,
Carat text,
Color text,
Clarity text,
CutGrade text,
Price text,
PctRap text,
Cert text,
Depth text,
TableWidth text,
Girdle text,
Culet text,
Polish text,
Sym text,
Fluor text,
Meas text,
RapnetComment text,
NumStones text,
CertNum text,
StockNum text,
Make text,
Date datetime,
City text,
State text,
Country text,
Image text
);

create table active_listing like listing;
create table listing_tmp like listing;

create table listing_event_code
(
Code int primary key auto_increment,
Description text not null
);

insert into listing_event_code (Description) values
    ('Added'), ('Removed'), ('PriceChanged'), ('ReAdded');

create table listing_event (
EventId bigint NOT NULL AUTO_INCREMENT,
LotNum bigint NOT NULL,
Price text,
Date datetime,
EventDate datetime,
EventCode int NOT NULL,
PRIMARY KEY (EventId),
INDEX USING HASH (LotNum),
INDEX USING HASH (EventCode)
);

-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE PROCEDURE `track_changes`(loadDate datetime)
BEGIN

-- must only be called after bulk load into listing_tmp
-- add 'removed' event for old active listing that aren't in new active listing
-- add 'price changed' event for listing with price changes
set @removeCode = (select Code from listing_event_code c where c.Description = 'Removed');
set @readdCode  = (select Code from listing_event_code c where c.Description = 'ReAdded');
set @priceCode = (select Code from listing_event_code c where c.Description = 'PriceChanged');
insert into listing_event
    (LotNum, Price, `EventDate`, EventCode)
    select s.LotNum, s.Price, @loadDate, @removeCode
        from active_listing s where s.lotnum not in
            (select lotnum from listing_tmp);
    
insert into listing 
    select * from listing_tmp where lotnum not in 
        (select lotnum from listing s);
        
-- insert a 'readd' event for entries in listing_tmp
-- that are currently marked as 'removed' in the listing_event table            
insert into listing_event
    (LotNum, Price, `EventDate`, EventCode)
    select s.LotNum, s.Price, @loadDate, @readdCode
        from (select s.LotNum, s.Price from listing s
                join (select LotNum, max(EventDate) from listing_event where EventCode = @removeCode) se
                    on s.lotnum = se.lotnum
            ) s
        join listing_tmp a
            on s.lotnum = a.lotnum;

-- insert a price-change event for prices that have changed
insert into listing_event
    (LotNum, Price, `EventDate`, EventCode)
    select s.LotNum, a.Price, @loadDate, @priceCode
        from listing s
        join listing_tmp a
            on s.lotnum = a.lotnum
        where not s.price = a.price;

drop table active_listing;
rename table listing_tmp to active_listing;
END$$

DELIMITER ;