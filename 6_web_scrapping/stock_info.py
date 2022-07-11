"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with the youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.
Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...
About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet
Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

from bs4 import BeautifulSoup
import requests
from operator import itemgetter

most_active_url = 'https://finance.yahoo.com/most-active'
most_active_page = requests.get(most_active_url)
soup = BeautifulSoup(most_active_page.content, 'html.parser')

base_url = 'https://finance.yahoo.com'

# urls to pages from most-active
main_tab = soup.find_all('a', class_='Fw(600) C($linkColor)')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}


def ceo_year_born_data():
    """Function that scraps and return a list of companies from most-active page
    with data necessary to make the youngest-ceos sheet"""

    ceo_year_born_tab = []

    for a in main_tab:
        # general
        first, second = a['href'].split('?')
        company_code = f'{first[7:]}'
        print(company_code)

        if company_code != 'ENIA':  # line used when any of pages currently doesn't work, I print company code to verify which one, use 'N/A' if everything works fine
            company_profile_url = base_url + first + '/profile?' + second
            company_profile_page = requests.get(company_profile_url, headers=headers)
            company_soup = BeautifulSoup(company_profile_page.content, 'html.parser')

            # year born
            row = company_soup.find('tbody').find_all('tr')[0]
            ceo_line = row.find_all('td')
            year_born = str(ceo_line[4].text)

            # ceo name
            ceo_name = str(ceo_line[0].text)

            # company name
            name = str(company_soup.find('h3', class_='Fz(m) Mb(10px)').text)

            # country
            country_line = str(company_soup.find('p', class_='D(ib) W(47.727%) Pend(40px)'))
            country_substring = '<br/>'
            country_start_index = country_line.find(country_substring, country_line.find(country_substring) + 1) \
                                  + len(country_substring)
            country_end_index = country_line.find(country_substring, country_start_index)
            country = country_line[country_start_index:country_end_index]

            # employees
            employees = str(company_soup.find('p', class_="D(ib) Va(t)").find_all('span')[-1].text)

            ceo_year_born_tab.append([name, company_code, country, employees, ceo_name, year_born])

    return ceo_year_born_tab


def first_five_ceo_year_born():
    """Function that from all companies from most-active returns first 5 with the youngest CEOs"""

    ceo_year_born_tab = ceo_year_born_data()
    youngest_ceos = sorted(ceo_year_born_tab, key=itemgetter(5), reverse=True)
    # deleting items with 'N/A'
    for i in youngest_ceos:
        if i[5] == 'N/A':
            youngest_ceos.remove(i)
        else:   # it's sorted, so they appear only on first positions, I use break
            break

    return youngest_ceos[:5]


def week_change_data():
    """Function that scraps and return a list of companies from most-active page
    with data necessary to make the week-change sheet"""

    week_change_tab = []

    for a in main_tab:
        # general
        first, second = a['href'].split('?')
        company_code = f'{first[7:]}'
        print(company_code)

        if company_code != 'ENIA':
            company_statistics_url = base_url + first + '/key-statistics?' + second
            company_statistics_page = requests.get(company_statistics_url, headers=headers)
            company_soup = BeautifulSoup(company_statistics_page.content, 'html.parser')

            # 52 week change
            stock_price_history = company_soup.find('div', class_='Fl(end) W(50%) smartphone_W(100%)')
            change_string = stock_price_history.find_all('tr')[1].find('td',
                                                                       class_='Fw(500) Ta(end) Pstart(10px) Miw(60px)').text
            if change_string != 'N/A':
                change = float(change_string[:-1])

                # total cash
                financial_highlights = company_soup.find('div', class_='Mb(10px) Pend(20px) smartphone_Pend(0px)')
                balance_sheet = financial_highlights.find_all('div', class_='Pos(r) Mt(10px)')[4]
                total_cash = balance_sheet.find('td', class_='Fw(500) Ta(end) Pstart(10px) Miw(60px)').text

                # company name
                name = company_soup.find('h1', class_='D(ib) Fz(18px)').text[:-(len(company_code) + 3)]

                week_change_tab.append([name, company_code, change, total_cash])

    return week_change_tab


def first_ten_week_change():
    """Function that from all companies from most-active returns first 10 with the best week-change"""

    week_change_tab = week_change_data()
    result = sorted(week_change_tab, key=itemgetter(2), reverse=True)
    return result[:10]


def holds_data():
    """Function that scraps and return a list of companies from most-active page
        with data necessary to make the holds sheet"""
    holds_tab = []

    for a in main_tab:
        # general
        first, second = a['href'].split('?')
        company_code = f'{first[7:]}'
        print(company_code)

        if company_code != 'ENIA':
            company_statistics_url = base_url + first + '/holders?' + second
            company_statistics_page = requests.get(company_statistics_url, headers=headers)
            company_soup = BeautifulSoup(company_statistics_page.content, 'html.parser')

            holders_all = company_soup.find_all('tr',
                                                class_='BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)')
            for holder in holders_all:
                if holder.find_all('td')[0].text == 'Blackrock Inc.':
                    holders = holder.find_all('td')

                    # company name
                    name = company_soup.find('h1', class_='D(ib) Fz(18px)').text[:-(len(company_code) + 3)]

                    # shares
                    shares = holders[1].text

                    # date reported
                    date_reported = holders[2].text

                    # %out
                    out = holders[3].text

                    # value
                    value = int(holders[4].text.replace(',', ''))

                    holds_tab.append([name, company_code, shares, date_reported, out, value])

    if len(holds_tab) != 0:
        return holds_tab


def first_ten_holds():
    """Function that from all companies from most-active returns the biggest Blackrock inc. holds"""

    holds_tab = holds_data()
    result = sorted(holds_tab, key=itemgetter(5), reverse=True)
    return result[:10]


def ceo_year_born_sheet_print():
    """Function that prints the sheet for the data given by first_five_ceo_year_born"""

    first_five_ceo_year_born_data = first_five_ceo_year_born()
    print('=' * 61, '5 stocks with the youngest CEOs', '=' * 61)
    print('| Name                                      | Code    | Country'
          '                        | Employees    | CEO Name                          | CEO Year Born |')
    print('-' * 155)
    for verse in first_five_ceo_year_born_data:
        print('|', verse[0], ' ' * (39 - len(verse[0])),
              ' |', verse[1], ' ' * (5 - len(verse[1])),
              ' |', verse[2], ' ' * (28 - len(verse[2])),
              ' |', verse[3], ' ' * (10 - len(verse[3])),
              ' |', verse[4], ' ' * (31 - len(verse[4])),
              ' |', verse[5], ' ' * (12 - len(str(verse[5]))), '|')


def week_change_sheet_print():
    """Function that prints the sheet for the data given by first_ten_week_change"""

    first_ten_week_change_data = first_ten_week_change()
    print('=' * 23, '10 stocks with best 52-Week Change', '=' * 23)
    print('| Name                                   | Code    | 52-week change | Total Cash |')
    print('-' * 82)
    for verse in first_ten_week_change_data:
        print('|', verse[0], ' ' * (36 - len(verse[0])),
              ' |', verse[1], ' ' * (5 - len(verse[1])),
              ' |', verse[2], '%', ' ' * (10 - len(str(verse[2]))),
              ' |', verse[3], ' ' * (9 - len(verse[3])), '|')


def holds_sheet_print():
    """Function that prints the sheet for the data given by first_ten_holds"""

    first_ten_holds_data = first_ten_holds()
    print('=' * 37, '10 largest holds of Blackrock Inc.', '=' * 37)
    print('| Name                            | Code    | Shares            | Data Reported  | % Out '
          '   | Value          |')
    print('-' * 110)
    for verse in first_ten_holds_data:
        print('|', verse[0], ' ' * (29 - len(verse[0])),
              ' |', verse[1], ' ' * (5 - len(verse[1])),
              ' |', verse[2], ' ' * (15 - len(verse[2])),
              ' |', verse[3], ' ' * (9 - len(verse[3])),
              ' |', verse[4], ' ' * (6 - len(verse[4])),
              ' |', verse[5], ' ' * (13 - len(str(verse[5]))), '|')


if __name__ == "__main__":

    ceo_year_born_sheet_print()

    week_change_sheet_print()

    holds_sheet_print()
