# ============================================================================================
# ⚙️ Конфигурация
# ============================================================================================

# Основные Compose файлы
COMPOSE_FILE = docker-compose.yaml
COMPOSE_FILE_PROD = docker-compose.prod.yaml
COMPOSE_FILE_TEST = docker-compose.test.yaml

# Названия сервисов (должны совпадать с именами в compose)
BACKEND = backend

# ============================================================================================
# 🚀 Локальная разработка
# ============================================================================================

## Поднимает контейнеры с пересборкой
up-build:
	docker compose -f $(COMPOSE_FILE) up --build

## Останавливает контейнеры (без удаления volumes)
down:
	docker compose -f $(COMPOSE_FILE) down

## Останавливает контейнеры и удаляет volumes
down-with-volumes:
	docker compose -f $(COMPOSE_FILE) down -v

## Перезапускает всё окружение
restart: down up-build

## Просмотр логов backend-сервиса
logs:
	docker compose -f $(COMPOSE_FILE) logs -f $(BACKEND)

# ============================================================================================
# 🏗️ Production
# ============================================================================================

## Запуск production-окружения
up-build-prod:
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_PROD) up -d --build

# ============================================================================================
# 🧩 Миграции (Alembic)
# ============================================================================================

m ?= Auto migration

## Применяет все миграции
migrate:
	docker compose -f $(COMPOSE_FILE) exec $(BACKEND) alembic upgrade head

## Создаёт новую миграцию с автогенерацией
makemigrations:
	docker compose -f $(COMPOSE_FILE) exec $(BACKEND) alembic revision --autogenerate -m "$(m)"

# ============================================================================================
# 🧪 Тестирование
# ============================================================================================

## Запускает тесты в тестовом окружении и удаляет контейнеры после завершения
test-backend:
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_TEST) up --build --abort-on-container-exit
	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_TEST) down

# ============================================================================================
# 🧹 Утилиты
# ============================================================================================

## Показывает состояние контейнеров
ps:
	docker compose ps


include_volumes ?= false
## Очистка системы от неиспользуемых ресурсов (include_volumes=false по умолчанию)
clean:
	docker system prune -f $(if $(filter true 1,$(include_volumes)),--volumes)

## Вывод справки по каждой команде
help:
	@awk '\
		/^[[:space:]]*##[[:space:]]*/ { desc = substr($$0, match($$0, /##[[:space:]]*/)+RLENGTH); next } \
		/^[[:space:]]*$$/ { next } \
		/^[a-zA-Z0-9_.-]+[[:space:]]*:/ { \
			split($$0, a, ":"); \
			target = a[1]; \
			sub(/^[[:space:]]+/, "", desc); \
			sub(/[[:space:]]+$$/, "", desc); \
			printf "\033[92m%-20s\033[0m %s\n", target, desc; \
			desc = ""; \
		} \
	' $(MAKEFILE_LIST)


