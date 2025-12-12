# Руководство по тестированию TestOps Copilot

Этот документ содержит инструкции и тестовые данные для проверки генерации UI и API тестов.

## Предварительные требования
Убедитесь, что бэкенд запущен с последними изменениями:
```bash
docker-compose restart backend
```

---

## КЕЙС 1: UI-тестирование (Калькулятор и Конфигуратор)

### Сценарий 1.1: Главная страница (Calculator)
**Входные данные:**
*   **Test Type:** UI (Frontend)
*   **Owner:** qa_user
*   **Priority:** CRITICAL
*   **Requirements:**
    ```text
    Блок 1. Начальная страница

    • Отображение главной страницы с пояснительным текстом.
    • Кнопка "Добавить сервис" доступна и кликабельна.
    • Отображение шагов процесса (добавление → конфигурация → подключение).
    • Отображение текущей общей стоимости (с указанием «в месяц с НДС»).
    • Отображение дисклеймера об отсутствии офертности.
    ```

**Ожидаемый результат (Code Review):**
1.  **Class Name:** `TestPriceCalculatorUI`
2.  **Context:** `Arrange` -> `with allure.step("Открыть главную страницу сервиса"):`
3.  **AAA Structure:**
    *   **Act:** `with allure.step("Нажать на кнопку 'Добавить сервис'"):`
    *   **Assert:** В начале проверок: `with allure.step("Убедиться, что кнопка 'Добавить сервис' доступна и кликабельна."):`
4.  **Meta:** Декоратор `@allure.link("...", name="Related Task")` присутствует.

---

### Сценарий 1.2: Управление Конфигурацией
**Входные данные:**
*   **Test Type:** UI (Frontend)
*   **Requirements:**
    ```text
    Блок 4. Управление конфигурацией

    • Добавление нескольких сервисов в одну конфигурацию.
    • Удаление сервиса из конфигурации.
    • Сравнительный режим (2–3 конфигурации).
    • Скачивание расчета (PDF/JSON).
    • Поделиться ссылкой на конфигурацию.
    • Кнопка «Подключить» для каждого продукта (кроме Arenadata DB).
    • Free Tier можно добавить только один раз.
    ```

**Ожидаемый результат:**
1.  **Class Name:** `TestConfigurationManagement`
2.  **Arrange:** `with allure.step("Перейти к управлению конфигурацией"):`
3.  **Act:** `with allure.step("Добавить или удалить сервис из конфигурации"):` (Fallback action)

---

## КЕЙС 2: API-тестирование (Evolution Compute)

### Сценарий 2.1: Получение списка ВМ
**Входные данные:**
*   **Test Type:** Manual Test (или API)
*   **Requirements (Скопируйте полностью):**
    ```text
    Получение списка виртуальных машин
    Authorizations:
    userPlaneApiToken
    HTTP Authorization Scheme: Bearer

    query Parameters
    project_id required string <uuid> Идентификатор проекта.
    limit integer Default: 50 Максимальное количество элементов в списке.

    Responses
    200 Successful Response
    items required Array of objects (PublicVmResponseItem)
    total required integer Общее количество доступных элементов.
    ```

**Ожидаемый результат:**
1.  **Class Name:** `TestVirtualMachinesAPI`
2.  **Arrange:**
    *   `with allure.step("Подготовить заголовки: Authorization Bearer token"):`
    *   `with allure.step("Подготовить параметры запроса: project_id (UUID), limit=50"):`
3.  **Act:**
    *   `with allure.step("Отправить GET запрос на получение списка ВМ"):`
4.  **Assert:**
    *   `with allure.step("Проверить статус-код 200"):`
    *   `with allure.step("Валидация структуры ответа: items (array), total (int), limit (int), offset (int)"):`
    *   `with allure.step("Проверить, что 'items' не пуст и содержит объекты с полями: id, name, state"):`
    *   `with allure.step("Проверить вложенные объекты: flavor, interfaces, availability_zone"):`

### Сценарий 2.2: Изменение статуса ВМ (PUT)
**Входные данные:**
*   **Test Type:** API (Backend)
*   **Requirements:**
    ```text
    Изменение статуса виртуальной машины
    Authorizations:
    userPlaneApiToken
    HTTP Authorization Scheme: Bearer

    Request Body schema: application/json
    required Array
    id required string <uuid>
    state required string Enum: "stopped" "running"

    Responses
    204 Successful Response
    ```

**Ожидаемый результат:**
1.  **Class Name:** `TestVMStatusManagement`
2.  **Act:** `response = requests.put(..., json=payload)`
3.  **Assert:** `assert response.status_code == 204`

---
