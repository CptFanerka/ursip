# Тестовое задание для компании URSiP
> Создать парсер excel файла (во вложении) на Python.
> Создать таблицу согласно нормам реляционных баз данных (внести все значения в одну таблицу).
> Добавить расчетный тотал по Qoil, Qliq, сгруппированный по датам (даты можете указать свои, добавив программно, не изменяя исходный файл, при условии, что дни будут разные, а месяц и год одинаковые)
# Установка и запуск
**Вариант 1: Docker**
```
git clone https://github.com/cptfanerka/ursip.git
cd ursip
docker build -t python_parser_image .
docker run python_parser_image
```
**Вариант 2: Python**
```
git clone https://github.com/cptfanerka/ursip.git
cd ursip
pip install -r requirements.txt
cd src
python excel_file_parser.py
```
