import os
from datetime import timedelta, date
from urllib.request import urlopen
from bs4 import BeautifulSoup


class AgriDataScrapper:

    def url_maker(self, sed):
        urlname = 'http://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=23&Tx_State=MH&Tx_District=0&Tx_Market=0&DateFrom=' + sed + '&DateTo=' + sed + \
                  '&Fr_Date=01-Jan-2014&To_Date=01-Jan-2014&Tx_Trend=2&Tx_CommodityHead=Onion&Tx_StateHead=Maharashtra&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
        return urlname

    def make_soup(self, urlo):
        thepage = urlopen(urlo)
        soupdata = BeautifulSoup(thepage.read(), 'lxml')
        return soupdata


if __name__ == '__main__':

    agrids = AgriDataScrapper()
    date_list = []
    data_list = []


    def daterange(date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + timedelta(n)


    start_dt = date(2014, 2, 1)
    end_dt = date(2014, 12, 31)
    for dt in daterange(start_dt, end_dt):
        date_list.append(dt.strftime("%d-%b-%Y"))

    for date_loop in date_list:

        uname = agrids.url_maker(date_loop)
        sobj = agrids.make_soup(uname)

        for record in sobj.findAll('tr'):
            combData = ''
            for data in record.findAll('td'):
                combData = combData + ';' + data.text
            data_list.append(combData[1:])

        for i in range(len(data_list) - 2):
            print(data_list[i])

        with open("OninoMaharshtra.csv", "a") as op:
            for i in range(len(data_list) - 2):
                op.write("%s\n" % data_list[i])

        del data_list[:]

    # headerList = "State_Name;District_Name;Market_Name;Variety;Group;Arrivals;Min_Price;Max_Price;Modal_Price;Reported_Date"
    # with open(os.path.expanduser("OninoMaharshtra.csv"), "wb") as op:
    #     op.write(bytes(headerList,encoding="ascii",errors='ignore'))
