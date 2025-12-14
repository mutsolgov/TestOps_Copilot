import pytest
import allure

@allure.manual
@allure.label("owner", "user111")
@allure.feature("MobileResponsiveness")
@allure.story("Story: MobileResponsiveness")
@allure.suite("UI")
@pytest.mark.manual
class TestMobileResponsiveness:
    @allure.title("Test based on requirements")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("LOW")
    @allure.label("priority", "low")
    def test_scenario(self):
        # Arrange
        with allure.step("Открыть сервис на мобильном устройстве"):
            pass

        # Act
        with allure.step("Проверить доступность элементов управления"):
            pass

        # Assert
        with allure.step("Все элементы управления доступны на мобильных."):
            pass

