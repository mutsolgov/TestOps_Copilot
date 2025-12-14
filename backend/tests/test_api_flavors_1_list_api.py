import pytest
import allure
import requests
import os
import json

@allure.feature("FlavorsListAPI")
@allure.story("Story: FlavorsListAPI")
@allure.suite("API")
@allure.link("https://jira.cloud.ru/browse/TASK-API-FLAVORS-LIST", name="API Docs")
class TestFlavorsListAPI:
    @allure.title("API Test: Get Flavors List")
    @allure.link("https://jira.cloud.ru/browse/TASK-PENDING", name="Related Task")
    @allure.tag("NORMAL")
    @allure.label("priority", "normal")
    def test_scenario(self):
        # Arrange
        base_url = "https://compute.api.cloud.ru"
        endpoint = "/api/v1/flavors"
        
        # Configuration
        token = os.getenv("CLOUD_API_TOKEN")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "limit": 10,
            "order_by": "created_time",
            "order_desc": "true"
        }

        # Act
        with allure.step(f"GET {endpoint}"):
            response = requests.get(base_url + endpoint, headers=headers, params=params)

        # Assert
        with allure.step("Check Status Code 200"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        with allure.step("Attach API Response Data"):
            # 1. Форматируем JSON для красивого отображения
            formatted_data = json.dumps(data, indent=4, ensure_ascii=False) 
            
            # 2. Прикрепляем данные к отчету Allure
            allure.attach(
                formatted_data, 
                name="Flavors List Full JSON Response", 
                attachment_type=allure.attachment_type.JSON
            )
            
            # 3. Прикрепляем первые элементы списка для быстрого просмотра
            if data["items"]:
                sample_data = data["items"][:2]
                sample_formatted = json.dumps(sample_data, indent=4, ensure_ascii=False)
                allure.attach(
                    sample_formatted,
                    name=f"Flavors List Sample (First {len(sample_data)} items)",
                    attachment_type=allure.attachment_type.JSON
                )

        with allure.step("Validate Response Schema"):
            assert "items" in data, "Response missing 'items' field"
            assert isinstance(data["items"], list), "'items' must be a list"
            assert "total" in data, "Response missing 'total' field"
            assert "limit" in data
            assert "offset" in data
            
        with allure.step("Validate Flavor Item Structure"):
            if data["items"]:
                flavor = data["items"][0]
                assert "id" in flavor, "Flavor missing 'id'"
                assert "name" in flavor, "Flavor missing 'name'"
                assert "cpu" in flavor, "Flavor missing 'cpu'"
                assert "ram" in flavor, "Flavor missing 'ram'"
                assert "type" in flavor, "Flavor missing 'type'"
                assert "availability_zones" in flavor, "Flavor missing 'availability_zones'"
        

