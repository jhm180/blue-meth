

select dbo.memoheader.memodate, dbo.memodetail.MemoNo , dbo.memodetail.LineNum , dbo.memodetail.ItemNo , dbo.memodetail.qty , dbo.memodetail.Description , dbo.memodetail.SellPrice
from dbo.memodetail 
full outer join dbo.memoheader on dbo.memodetail.memono = dbo.memoheader.memono
where dbo.memodetail.memono = 14984
order by dbo.memodetail.itemno