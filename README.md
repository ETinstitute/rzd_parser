# Парсер РЖД

Парсер собирает данные по поставкам в pandas.DataFrame с [сайта РЖД](https://company.rzd.ru/ru/9397/page/13307)


## Начало работы
Первым делом, клонируйте репозиторий к себе следующей командой:
```bash
git clone https://github.com/ETinstitute/rzd_parser
```
Далее, прежде чем начать работу с этой библиотекой, следует загрузить все зависимости. Для этого исполните следующую команду в терминале
```bash
pip install -r requirements.txt
```
## Пример работы
Для начала работы нужно создать экземпляр парсера. 

В качестве параметра `date_publication_0`, нужно передать дату левой границы. 
Правая граница по умолчанию сегодняшний день. Можно передавать как строку, в формате DD.MM.YYYY, так и обьекты datetime 
```Python
from RZD_Parser import RZDParser


parser = RZDParser()

start_date = '01.06.2022'
end_date = '01.12.2023'

df = parser.parse_data(date_publication_0=start_date, date_publication_1=end_date)
```
# Обновление данных

Одним из преимуществ данного парсера является способность автоматически обновлять данные

## Первый способ

если у вас уже есть инстанс спарсенного df, то можно просто вызвать функцию update_data
```python
updated_df = parser.update_data()
```
## Второй способ

Если у вас есть csv файл с этими данными, то можно указать путь до этого файла

```python
updated_df = parser.update_data(csv_filepath='data.csv')
```
