import requests
from bs4 import BeautifulSoup

class us_cpi_reader():

    def soup_bureau_of_labor_cpi_table1(self):
        r = requests.get(self.target_url)         #requestsを使って、webから取得
        soup = BeautifulSoup(r.text,"html.parser")
        return(soup)

    def __init__(self):

        # set up the insatance variables that will be needed
        self.target_url = 'https://www.bls.gov/news.release/cpi.t01.htm'
        self.header = []
        self.item_names = []
        self.item_values = []

        #run the procedure
        self.soup = self.soup_bureau_of_labor_cpi_table1()

    #method to get table values
    def get_values(self):
        tags = self.soup.find_all('tbody')[0].find_all('tr')

        for tag in tags:
            onerow = []
            # there are some <tr> tags only for sepleater line
            # which do not contain <th> tags
            # avoiding those
            if tag.find('th'):
                self.item_names.append(tag.find('th').text)
                tokens = tag.find_all('td')
                for token in tokens:
                    onerow.append(float(token.text.replace(",","")))
                self.item_values.append(onerow)

        nrow = len(self.item_names)

        for i in range(0,nrow):
            print(self.item_names[i],self.item_values[i])

    #method to get table header
    def table_header(self):
        tags = self.soup.find_all('thead')[0].find_all('tr')

        #get first row of header
        tag = tags[0]
        tokens = tag.find_all("th")
        for token in tokens:
            counter = 0
            colnum = 1
            if 'colspan' in token.attrs:
                colnum = int(token['colspan'])
            while counter < colnum:
                self.header.append(token.text)
                counter += 1

        #get the second row
        tag = tags[1]
        tokens = []
        tokens = tag.find_all("th")
        counter = 0
        for token in tokens:
            self.header[counter] = self.header[counter] + token.text
            counter += 1

        # print( self.header )


    def print_all_thead(self):

        soup = self.soup_bureau_of_labor_cpi_table1()
        table_head = soup.find_all("thead")
        print (table_head[0])
        print (self.target_url)



a = us_cpi_reader()
a.get_values()
