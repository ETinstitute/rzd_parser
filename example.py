from RZD_Parser import RZDParser

start_date = '01.01.2014'
end_date = '01.01.2024'

parser = RZDParser()

df = parser.parse_data(date_publication_0=start_date, date_publication_1=end_date)
df.to_csv('example_parsed_data.csv')

df = parser.update_data(csv_filepath='example_parsed_data.csv')
df.to_csv('example_parsed_data.csv')
