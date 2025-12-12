import pytest
import allure

@allure.manual
@allure.label("owner", "www")
@allure.feature("ConfigurationManagement")
@allure.story("Story: ConfigurationManagement")
@allure.suite("UI")
@pytest.mark.manual
class TestConfigurationManagement:
    @allure.title("Test based on requirements")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        with allure.step("Перейти к управлению конфигурацией"):
            pass

        # Act
        with allure.step("Добавить или удалить сервис из конфигурации"):
            pass

        # Assert
        with allure.step("Добавление нескольких сервисов в одну конфигурацию."):
            pass
        with allure.step("Удаление сервиса из конфигурации."):
            pass
        with allure.step("Сравнительный режим (2–3 конфигурации)."):
            pass
        with allure.step("Скачивание расчета (PDF/JSON)."):
            pass
        with allure.step("Поделиться ссылкой на конфигурацию."):
            pass
        with allure.step("Кнопка «Подключить» для каждого продукта (кроме Arenadata DB)."):
            pass
        with allure.step("Free Tier можно добавить только один раз."):
            pass


