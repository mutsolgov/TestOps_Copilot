import pytest
import allure

@allure.manual
@allure.label("owner", "user3")
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
        with allure.step("Удаление сервиса из конфигурации."):
            pass

