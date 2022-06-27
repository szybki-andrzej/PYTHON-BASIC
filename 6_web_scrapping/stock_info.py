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

most_active_url = 'https://finance.yahoo.com/most-active'
most_active_page = requests.get(most_active_url)
soup = BeautifulSoup(most_active_page.content, 'html.parser')

base_url = 'https://finance.yahoo.com'

# urls to pages from most-active
main_tab = soup.find_all('a', class_='Fw(600) C($linkColor)')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}


def ceo_year_born_all():
    ceo_year_born_tab = []

    for a in main_tab:  # to make scrapping faster now I use only 6 records
        # general
        first, second = a['href'].split('?')
        company_code = f'{first[7:]}'
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
        print(company_code)

    return ceo_year_born_tab


def ceo_year_born(ceo_year_born_tab):
    list_of_year_born = [year_born[5] for year_born in ceo_year_born_tab]
    list_of_year_born.sort(reverse=True)

    for i in list_of_year_born:
        if i == 'N/A':
            list_of_year_born.remove(i)
        else:
            break

    youngest_ceos = list_of_year_born[:5]
    youngest_ceos_tab = []
    for year in youngest_ceos:
        for data in ceo_year_born_tab:
            if year == data[5]:
                youngest_ceos_tab.append(data)

    # what when is 2 places ex aequo at the end?
    return youngest_ceos_tab[:5]


def week_change_all():
    week_change_tab = []

    for a in main_tab:
        # general
        first, second = a['href'].split('?')
        company_code = f'{first[7:]}'
        company_statistics_url = base_url + first + '/key-statistics?' + second
        company_statistics_page = requests.get(company_statistics_url, headers=headers)
        company_soup = BeautifulSoup(company_statistics_page.content, 'html.parser')

        # 52 week change
        stock_price_history = company_soup.find('div', class_='Fl(end) W(50%) smartphone_W(100%)')
        change_string = stock_price_history.find_all('tr')[1].find('td',
                                                                   class_='Fw(500) Ta(end) Pstart(10px) Miw(60px)').text
        change = float(change_string[:-1])

        # total cash
        financial_highlights = company_soup.find('div', class_='Mb(10px) Pend(20px) smartphone_Pend(0px)')
        balance_sheet = financial_highlights.find_all('div', class_='Pos(r) Mt(10px)')[4]
        total_cash = balance_sheet.find('td', class_='Fw(500) Ta(end) Pstart(10px) Miw(60px)').text

        # company name
        name = company_soup.find('h1', class_='D(ib) Fz(18px)').text[:-(len(company_code) + 3)]

        week_change_tab.append([name, company_code, change, total_cash])
        print(company_code)

    return week_change_tab


def week_change(week_change_tab):
    list_of_week_change = [change[2] for change in week_change_tab]
    list_of_week_change.sort(reverse=True)

    best_change = list_of_week_change[:10]
    best_change_tab = []
    for change in best_change:
        for data in week_change_tab:
            if change == data[2]:
                best_change_tab.append(data)

    # what when is 2 places ex aequo at the end?
    return best_change_tab[:10]


def holds_all():
    holds_tab = []

    for a in main_tab:
        # general
        first, second = a['href'].split('?')
        company_code = f'{first[7:]}'
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

        print(company_code)

    if len(holds_tab) != 0:
        return holds_tab


def holds(holds_tab):
    list_of_holds = [hold[5] for hold in holds_tab]
    list_of_holds.sort(reverse=True)

    best_hold = list_of_holds[:10]
    best_hold_tab = []
    for hold in best_hold:
        for data in holds_tab:
            if hold == data[5]:
                best_hold_tab.append(data)

    # what when is 2 places ex aequo at the end?
    return best_hold_tab[:10]


def ceo_year_born_sheet(ceo_year_born_data):
    print('=' * 61, '5 stocks with the youngest CEOs', '=' * 61)
    print('| Name                                      | Code    | Country'
          '                        | Employees    | CEO Name                          | CEO Year Born |')
    print('-' * 155)
    for verse in ceo_year_born_data:
        print('|', verse[0], ' ' * (39 - len(verse[0])),
              ' |', verse[1], ' ' * (5 - len(verse[1])),
              ' |', verse[2], ' ' * (28 - len(verse[2])),
              ' |', verse[3], ' ' * (10 - len(verse[3])),
              ' |', verse[4], ' ' * (31 - len(verse[4])),
              ' |', verse[5], ' ' * (12 - len(str(verse[5]))), '|')


def week_change_sheet(week_change_data):
    print('=' * 23, '10 stocks with best 52-Week Change', '=' * 23)
    print('| Name                                   | Code    | 52-week change | Total Cash |')
    print('-' * 82)
    for verse in week_change_data:
        print('|', verse[0], ' ' * (36 - len(verse[0])),
              ' |', verse[1], ' ' * (5 - len(verse[1])),
              ' |', verse[2], '%', ' ' * (10 - len(str(verse[2]))),
              ' |', verse[3], ' ' * (9 - len(verse[3])), '|')


def holds_sheet(holds_data):
    print('=' * 37, '10 largest holds of Blackrock Inc.', '=' * 37)
    print('| Name                            | Code    | Shares            | Data Reported  | % Out '
          '   | Value          |')
    print('-' * 110)
    for verse in holds_data:
        print('|', verse[0], ' ' * (29 - len(verse[0])),
              ' |', verse[1], ' ' * (5 - len(verse[1])),
              ' |', verse[2], ' ' * (15 - len(verse[2])),
              ' |', verse[3], ' ' * (9 - len(verse[3])),
              ' |', verse[4], ' ' * (6 - len(verse[4])),
              ' |', verse[5], ' ' * (13 - len(str(verse[5]))), '|')


if __name__ == "__main__":
    ceo_year_born_sheet(ceo_year_born(ceo_year_born_all()))

    week_change_sheet(week_change(week_change_all()))

    holds_sheet(holds(holds_all()))
