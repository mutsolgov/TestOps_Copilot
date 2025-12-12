import pytest
import allure

@allure.manual
@allure.label("owner", "qa_user")
@allure.feature("ProductConfiguration")
@allure.story("Story: ProductConfiguration")
@allure.suite("UI")
@pytest.mark.manual
class TestProductConfiguration:
    @allure.title("Test based on requirements")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        with allure.step("Выбрать продукт и перейти на экран конфигурации"):
            pass

        # Act
        with allure.step('Нажать на кнопку "Добавить сервис"'):
            pass

        # Assert
        with allure.step('Убедиться, что кнопка "добавить сервис" доступна и доступна и кликабельна.'):
            pass
        with allure.step("Отображение главной страницы с пояснительным текстом."):
            pass
        with allure.step("Отображение шагов процесса (добавление → конфигурация → подключение)."):
            pass
        with allure.step("Отображение текущей общей стоимости (с указанием «в месяц с НДС»)."):
            pass
        with allure.step("Отображение дисклеймера об отсутствии офертности."):
            pass


