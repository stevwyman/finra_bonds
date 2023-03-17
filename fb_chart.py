from trace_bonds import LocaleDAO, ad_chart
from datetime import date

local_dao = LocaleDAO()
# all = local_dao.read(500)
all = local_dao.read(250)
# all = local_dao.read_by_dates(20210101, 20230311)
# all = local_dao.read_all()
print(f"found {len(all)} entries")

ad_chart(all)