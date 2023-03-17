from trace_bonds import LocaleDAO, ad_spy_chart
from online_data import PolygonIO

online_dao = PolygonIO()
answer = online_dao.lookupHistory("SPY", "2021-01-01", "2023-03-14")
spy_data = answer["results"]

local_dao = LocaleDAO()
ad_data = local_dao.read_by_dates(20210101, 20230314)

ad_spy_chart(ad_data, spy_data)