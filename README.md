# Курсовая работа №1 
## Описание: 
### Приложение для анализа банковских операций
Реализованы функции для веб-страниц: 
- Главная 
> в файле views.py реализованы функции:
> - [x] greeting - функция приветствия в зависимости от значение времени 
> - [x] expenses - функция возвращающая номера карт со списком расходов
> - [x] total_expenses - функция возвращающая общую сумму расходов по каждой карте
> - [x] top5 - функция возвращающая топ 5 транзакций по сумме платежа"
> - [x] greeting - функция приветствия в зависимости от значение времени
> - [x] get_transactions - получает данные из Excel файла
> - [x] search_transactions - функция поиска данных о банковских операциях
> - [x] search_tr_in_data - функция поиска данных о банковских операциях на диапазон дат
> - [x] str_to_data - преобразует дату формата 31.12.2021 в формат date
> - [x] cashback - функция возвращающая расчёт суммы кэшбэка с расходов по каждой карте


- События

Для  
Транзакции получены в Excel-файле, приложение генерирует JSON-файл для веб-страниц, формирует
excel-отчеты и предоставляет другие сервисы:
- Рассчитывает сумму на счету инвесткопилки по заданному порогу округления;
- Выводит информацию о 5 топ транзакциях по сумме платежа
- Выводит информацию по каждой карте (последние 4 цифры карты, общая сумма расходов, кэшбэк)
- Выводит текущий курс валют: USD, EUR.
Виджет банковских операций клиента показывает несколько последних успешных банковских 
операций клиента. 
Виджет имеет функцию вывода суммы транзакции в рублях, включая перевод в рубли по текущему 
курсу в случае, если транзакция была в валюте. 
Виджет логирует функции маскирования номеров карт и счетов, и вывода суммы транзакции в рублях. 
Виджет может работать с файлами в форматах json, CSV и excel.
## Тесты: Содержит тесты функционала.
## Установка:
Клонируйте репозиторий: git clone https://github.com/Legalesnoy/Sky_bank
## Установите зависимости:
pip install -r requirements.txt
## Документация: - вся необходимая инофрмация указана в Docstrings
## Лицензия: -  SkyPro