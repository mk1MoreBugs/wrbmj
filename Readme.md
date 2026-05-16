# WRBMJ — совместное редактирование заметок в реальном времени (MVP)

Приложение для создания и редактирования заметок с синхронизацией изменений между несколькими клиентами через WebSocket.  
Бэкенд написан на **FastAPI**, данные хранятся в **PostgreSQL** и кэшируются в **Redis**. Фронтенд — **Vue 3 + TypeScript + Pinia**.

## Основные возможности

- ✏️ Создание, редактирование и удаление заметок
- 🔄 Автоматическое сохранение изменений
- ⚡ Real‑time обновление списка и содержимого заметки через WebSocket
- 🔐 Аутентификация по JWT
- 🐳 Бэкенд полностью контейнеризирован (Docker Compose)


## WebSocket — синхронизация в реальном времени

При открытии заметки (URL `/notes/{id}/edit`) фронтенд устанавливает WebSocket‑соединение с бэкендом:

```text
ws://localhost:8000/api/v1/notes/{id}/edit?token=<JWT>
```

**Поток данных:**

1. Клиент аутентифицируется по токену (передаётся как query‑параметр).

2. Бэкенд сохраняет соединение в `WsConnectionManager`.

3. При любом изменении текста или заголовка заметки фронтенд отправляет обновлённый объект `NoteContent`.

4. Сервер валидирует данные, сохраняет в Redis и широковещательно рассылает новое содержимое всем клиентам, подключённым к серверу (_MVP_).

5. Другие устройства получают сообщение и обновляют соответствующую заметку.

Таким образом, изменения заметки видны сразу на всех открытых экземплярах без перезагрузки страницы.

## Стек технологий

| Компонент     | Технологии                                                                             |
|---------------|----------------------------------------------------------------------------------------|
| Бэкенд        | FastAPI, SQLAlchemy, Alembic, Pydantic, Redis, WebSockets                              |
| Фронтенд      | Vue 3 (Composition API), TypeScript, Pinia, Vue Router, Tailwind CSS                   |
| База данных   | PostgreSQL                                                                             |
| Кэш / брокер  | Redis (хранение состояния заметок для синхронизации WebSocket и управление клиентами)  |
| Оркестрация   | Docker, Docker Compose, Make                                                           |

## Требования

- **Linux**
- **Docker** и **Docker Compose**
- **Node.js**, **npm**
- **Make**

## Первый запуск запуск

### 1. Создайте файл с паролем для базы данных
```bash
touch ./db_password.txt
# или
echo "my_strong_password" > ./db_password.txt
```

### 2. Запустите бэкенд (через Docker) и выполните миграции базы данных
```bash
make up
make migrate
```

### 3. Запустите фронтенд
```bash
cd frontend
npm install
npm run dev
```

После этого фронтенд будет доступен по адресу http://localhost:8080.

# Eng:

# WRBMJ — real-time collaborative note editing (MVP)
Application for creating and editing notes with real-time synchronization between multiple clients via WebSocket.
The backend is built with **FastAPI**, data is stored in **PostgreSQL** and cached in **Redis**. The frontend uses **Vue 3 + TypeScript + Pinia**.

## Main features
- ✏️ Create, edit, and delete notes

- 🔄 Auto-save changes

- ⚡ Real-time updates of the note list and note content via WebSocket

- 🔐 JWT authentication

- 🐳 Fully containerized backend (Docker Compose)

## WebSocket — real-time synchronization
When a note is opened (URL `/notes/{id}/edit`), the frontend establishes a WebSocket connection to the backend:

```text
ws://localhost:8000/api/v1/notes/{id}/edit?token=<JWT>
```

**Data flow:**

1. The client authenticates using a token (passed as a query parameter).

2. The backend stores the connection in `WsConnectionManager`.

3. On any change to the note text or title, the frontend sends an updated `NoteContent` object.

4. The server validates the data, saves it in Redis, and broadcasts the new content to all clients connected to the server (*MVP*).

5. Other devices receive the message and update the corresponding note.

This way, note changes are immediately visible on all open instances without reloading the page.

##  Technology stack

| Component      | Technologies                                                             |
|----------------|--------------------------------------------------------------------------|
| Backend	     | FastAPI, SQLAlchemy, Alembic, Pydantic, Redis, WebSockets                |
| Frontend	     | Vue 3 (Composition API), TypeScript, Pinia, Vue Router, Tailwind CSS     |
| Database	     | PostgreSQL                                                               |
| Cache / broker |	Redis (storing note state for WebSocket sync and managing clients)      |
| Orchestration  | Docker, Docker Compose, Make                                             |

## Requirements

- **Linux**
- **Docker** and **Docker Compose**
- **Node.js**, **npm**
- **Make**


## First launch launch
1. Create a database password file
```bash
touch ./db_password.txt
# or
echo "my_strong_password" > ./db_password.txt
```
2. Start the backend (via Docker) and run database migrations
```bash
make up
make migrate
```
3. Start the frontend
```bash
cd frontend
npm install
npm run dev
```
After that, the frontend will be available at http://localhost:8080.
