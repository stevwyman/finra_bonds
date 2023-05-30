import argparse
from trace_bonds import LocaleDAO, ad_chart, update
from datetime import date

def main():
    parser = argparse.ArgumentParser(description="read and display corporate high yield bonds")
    parser.add_argument(
        "-t",
        type=str,
        default="update",
        help="the task to perform, default update, others: chart"
    )
    args = parser.parse_args()

    if args.t == "update":
        #update_range("01/01/2019", "12/31/2019")
        update()    
    elif args.t == "chart":
        local_dao = LocaleDAO()
        # all = local_dao.read(500)
        all = local_dao.read(250)
        # all = local_dao.read_by_dates(20210101, 20230311)
        # all = local_dao.read_all()
        # print(f"found {all} entries")
        ad_chart(all)   


if __name__ == "__main__":
    main()
     