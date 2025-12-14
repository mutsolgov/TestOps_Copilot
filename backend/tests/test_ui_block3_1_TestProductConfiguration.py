import pytest
import allure

@allure.manual
@allure.label("owner", "user333")
@allure.feature("ProductConfiguration")
@allure.story("Story: ProductConfiguration")
@allure.suite("UI")
@pytest.mark.manual
class TestProductConfiguration:
    @allure.title("Test based on requirements")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("LOW")
    @allure.label("priority", "low")
    def test_scenario(self):
        # Arrange
        with allure.step("Выбрать продукт и перейти на экран конфигурации"):
            pass

        # Act
        with allure.step("Изменить параметры конфигурации (CPU/RAM)"):
            pass

        # Assert
        with allure.step("Отображение параметров (CPU, RAM, диск, регион, тариф)."):
            pass

