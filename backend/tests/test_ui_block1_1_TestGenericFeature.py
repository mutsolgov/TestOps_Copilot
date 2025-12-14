import pytest
import allure

@allure.manual
@allure.label("owner", "qa_user")
@allure.feature("GenericFeature")
@allure.story("Story: GenericFeature")
@allure.suite("UI")
@pytest.mark.manual
class TestGenericFeature:
    @allure.title("Test based on requirements")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        with allure.step("Открыть главную страницу сервиса"):
            pass

        # Act

        # Assert
        with allure.step("Отображение главной страницы с пояснительным текстом."):
            pass

