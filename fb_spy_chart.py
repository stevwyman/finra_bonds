from trace_bonds import LocaleDAO, ad_spy_chart
from online_data import PolygonIO

online_dao = PolygonIO()

answer = online_dao.lookupHistory("SPY", "2022-05-23", "2023-05-23")
spy_data = answer["results"]

local_dao = LocaleDAO()
ad_data = local_dao.read_by_dates(20220523, 20230523)

ad_spy_chart(ad_data, spy_data)