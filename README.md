# CRM System — PyQt5 + PostgreSQL

Десктопное CRM-приложение, написанное на Python + PyQt5, предназначенное для работы с клиентами и заказами.
Поддерживает авторизацию, поиск клиентов, привязку заказов к клиентам, просмотр собственных заказов и добавление новых записей.

# Возможности
# Работа с клиентами

добавление новых клиентов (ФИО, телефон, email, дата, примечание);
хранение телефонов в нормализованном виде;
поиск по:

ФИО

телефону

email

частичному совпадению

отображение всех клиентов в таблице;

просмотр заказов клиента по двойному нажатию.

# Алгоритм работы программы
<img width="1060" height="960" alt="diagram (3)" src="https://github.com/user-attachments/assets/f0c8be36-d137-4ba1-b676-37f9aad3834b" />


# Работа с заказами

добавление нового заказа (клиент, описание, вес, дата);

просмотр всех заказов;

просмотр только своих заказов;

автоматическое обновление таблицы после изменений.

# Авторизация пользователей
<img width="356" height="217" alt="image" src="https://github.com/user-attachments/assets/b5d3fdcf-9f95-44ae-b35d-70e21b06b00e" />

Авторизация происходит через таблицу клиентов:

логин — ID клиента

пароль — телефон (внутренний формат)

После успешного входа показывается основное окно CRM.

# Интерфейс
<img width="1094" height="702" alt="image" src="https://github.com/user-attachments/assets/5511c368-aeac-40bf-b63f-894499756265" />

современный тёмный дизайн;

вкладки: Клиенты / Заказы;

удобные таблицы;

кнопки действий расположены сверху;

диалоговые окна для добавления данных.

# Структура проекта
project/

│

├── db/

│   ├── __init__.py

│   ├── db.py                # функция connection()

│

├── gui/

│   ├── __init__.py

│   ├── login_window.py      # окно авторизации

│   ├── database_window.py   # главное окно CRM (клиенты/заказы)

│   ├── add_client_dialog.py # диалог добавления клиента

│   ├── add_order_dialog.py  # диалог добавления заказа

│

├── utils/

│   ├── __init__.py

│   ├── normalize.py         # функции normalize_phone / format_phone_for_db

│

├── main.py                  # точка входа

├── README.md

└── requirements.txt

# Установка и запуск
1. Установить зависимости
pip install -r requirements.txt

2. Настроить базу данных PostgreSQL
Создать базу и записать параметры в db/db.py:


DB_NAME = "your_db"

DB_USER = "user"

DB_PASSWORD = "password"

DB_HOST = "localhost"

DB_PORT = "5432"

3. Выполнить миграции (инициализация таблиц)

Выполняется автоматически при первом запуске, если таблиц нет:
python main.py

# Структура таблиц
# Таблица clients
<img width="1007" height="48" alt="image" src="https://github.com/user-attachments/assets/91d415ad-e6d9-4d86-99af-6844b1f23cbe" />

колонка	тип	описание

  id	SERIAL PK	ID клиента
  
  full_name	varchar	ФИО
  
  phone	varchar	телефон (нормализованный)
  
  mail	varchar	email
  
  request_date	date	дата обращения
  
  note	text	примечание
# Таблица zakazi
<img width="660" height="51" alt="image" src="https://github.com/user-attachments/assets/e6c5e1f0-e184-4e90-83eb-900b19c4eb0c" />

колонка	тип	описание

  id	SERIAL PK	ID заказа
  
  client_id	int FK	ID клиента
  
  description	text	описание заказа
  
  weight	float	вес
  
  created_at	date	дата создания

# Работа баз данных между собой, а также алгоритм работы программы
<img width="790" height="450" alt="diagram (1)" src="https://github.com/user-attachments/assets/99da99d3-1b5b-4eee-8d33-1df44b9c6cde" />

<img width="440" height="165" alt="diagram (2)" src="https://github.com/user-attachments/assets/00937652-56f4-45b4-be06-68d74534fc24" />

# Запуск приложения
  python main.py
