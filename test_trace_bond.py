from trace_bonds import OnlineReader, LocaleDAO
from datetime import datetime

DATE_FORMAT = "%d/%m/%Y"

test_data = """
    <html>
        <body>
            <table data-filedate="03/10/2023" width="100%">
                <tbody>
                    <tr>
                        <th> </th>
                        <th class="algn_rt">All Issues</th>
                        <th class="algn_rt">Investment Grade</th>
                        <th class="algn_rt">High Yield</th>
                        <th class="algn_rt">Convertible</th>
                    </tr>
                    <th class="algn_lt" style="width:20%;white-space:nowrap;">Total Issues Traded</th>
                    <td class="algn_rt">8781</td>
                    <td class="algn_rt">6894</td>
                    <td class="algn_rt">1657</td>
                    <td class="algn_rt">230</td>
                    <th class="algn_lt" style="width:20%;white-space:nowrap;">Advances</th>
                    <td class="algn_rt">6359</td>
                    <td class="algn_rt">5710</td>
                    <td class="algn_rt">612</td>
                    <td class="algn_rt">37</td>
                    <th class="algn_lt" style="width:20%;white-space:nowrap;">Declines</th>
                    <td class="algn_rt">2020</td>
                    <td class="algn_rt">1009</td>
                    <td class="algn_rt">827</td>
                    <td class="algn_rt">184</td>
                    <th class="algn_lt" style="width:20%;white-space:nowrap;">Unchanged</th>
                    <td class="algn_rt">56</td>
                    <td class="algn_rt">28</td>
                    <td class="algn_rt">23</td>
                    <td class="algn_rt">5</td>
                    <th class="algn_lt" style="width:20%;white-space:nowrap;">52 Week High</th>
                    <td class="algn_rt">135</td>
                    <td class="algn_rt">92</td>
                    <td class="algn_rt">41</td>
                    <td class="algn_rt">2</td>
                    <th class="algn_lt" style="width:20%;white-space:nowrap;">52 Week Low</th>
                    <td class="algn_rt">208</td>
                    <td class="algn_rt">77</td>
                    <td class="algn_rt">121</td>
                    <td class="algn_rt">10</td>
                    <th class="algn_lt" style="width:20%;white-space:nowrap;">Dollar Volume*</th>
                    <td class="algn_rt">25156</td>
                    <td class="algn_rt">18229</td>
                    <td class="algn_rt">5817</td>
                    <td class="algn_rt">1109</td>
                </tbody>
            </table>
        </body>
    </html>
    """

valid_result = {'date': 20230310, 'bond_data': {'All Issues': {'Total Issues Traded': 8781, 'Advances': 6359, 'Declines': 2020, 'Unchanged': 56, '52 Week High': 135, '52 Week Low': 208}, 'Investment Grade': {'Total Issues Traded': 6894, 'Advances': 5710, 'Declines': 1009, 'Unchanged': 28, '52 Week High': 92, '52 Week Low': 77}, 'High Yield': {'Total Issues Traded': 1657, 'Advances': 612, 'Declines': 827, 'Unchanged': 23, '52 Week High': 41, '52 Week Low': 121}, 'Convertible': {'Total Issues Traded': 230, 'Advances': 37, 'Declines': 184, 'Unchanged': 5, '52 Week High': 2, '52 Week Low': 10}}}

def test_online():
    request_date = datetime.fromisoformat('2023-03-10')
    online_reader = OnlineReader()
    data = online_reader.request_data(request_date)
    assert data["date"] == 20230310
    local_dao = LocaleDAO()
    local_dao.write(data)

def test_return_data():
    online_reader = OnlineReader()
    assert online_reader.return_data(test_data) == valid_result

def test_request_data():
    request_date = datetime.fromisoformat('2023-01-31')
    data = OnlineReader().request_data(request_date)
    assert data["date"] == 20230131

def test_read_data_limit():
    local_dao = LocaleDAO()
    result = local_dao.read(100)
    assert len(result) == 100

def test_read_data_dates():
    local_dao = LocaleDAO()
    result = local_dao.read_by_dates(20210101, 20220101)
    assert len(result) == 252

def test_read_data_date():
    local_dao = LocaleDAO()
    result = local_dao.read_by_date(20230308)
    assert result["date"] == 20230308
