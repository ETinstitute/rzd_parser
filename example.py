from RZD_Parser import RZDParser

start_date = '01.01.2014'
# end_date = '01.01.2024'

parser = RZDParser()

df = parser.parse_data(date_publication_0=start_date)
df.to_csv('example_parsed_data.csv')


# df = pd.read_csv('test.csv', index_col='Unnamed: 0')
# parser.df = df
#
# print(df.head())
#
# df = parser.update_data()
#
# print(df.head())
