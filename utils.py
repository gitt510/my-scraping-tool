
def scrape_stock_prices_from_irbank(code):
    # request html
    url = f'https://irbank.net/{code}/chart'
    response = requests.get(url)

    # parse response 
    soup = BeautifulSoup(response.content, 'html.parser')

    # get table that shows stock prices chart 
    table = soup.find('table', {'id': 'tbc'})

    # process all rows in table
    data = []
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        # skip the first row, as it's unnecessary
        if i == 0:
            continue

        # get all td element
        cols = row.find_all('td')
        if len(cols) == 1: # if nb of td is 1, it represents year of follwing date
            year = cols[0].text.strip()
            continue
        else:
            cols = [col.text.strip() for col in cols]

        # filter and edit content
        cols = cols[:5]
        cols[0] = datetime.strptime(f"{year}/{cols[0]}", "%Y/%m/%d").strftime("%Y-%m-%d")

        # append the processed row data to list
        data.append(cols)

    # convert result into dataframe
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close'])

    return df