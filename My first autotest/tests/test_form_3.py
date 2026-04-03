import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class TestDemoBlazeImproved:

    @pytest.fixture
    def driver(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def wait_and_click(self, driver, locator, timeout=10):
        """Утилита для ожидания и клика по элементу"""
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element

    def wait_for_element(self, driver, locator, timeout=10):
        """Утилита для ожидания появления элемента"""
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def test_complete_login_flow(self, driver):
        """Полный тест процесса авторизации"""

        print("\n=== Начало теста ===")

        # Шаг 1: Открытие страницы
        print("1. Открываем страницу...")
        driver.get("https://www.demoblaze.com/index.html")
        time.sleep(2)

        # Шаг 2: Проверка заголовка
        print("2. Проверяем заголовок...")
        assert driver.title == "STORE", f"Заголовок: {driver.title}"
        print(f"   ✓ Заголовок корректен: {driver.title}")

        # Шаг 3: Открытие формы логина
        print("3. Открываем форму логина...")
        try:
            login_btn = self.wait_and_click(driver, (By.ID, "login2"))
            print("   ✓ Кнопка 'Log in' нажата")
            time.sleep(1)
        except Exception as e:
            pytest.fail(f"Не удалось открыть форму логина: {e}")

        # Шаг 4: Заполнение формы
        print("4. Заполняем форму логина...")
        try:
            # Поле логина
            username_input = self.wait_for_element(driver, (By.ID, "loginusername"))
            username_input.clear()
            username_input.send_keys("petr1")
            print("   ✓ Логин введен: petr1")

            # Поле пароля
            password_input = driver.find_element(By.ID, "loginpassword")
            password_input.clear()
            password_input.send_keys("russia")
            print("   ✓ Пароль введен")

            # Кнопка отправки
            submit_btn = driver.find_element(By.XPATH, "//div[@class='modal-footer']//button[text()='Log in']")
            submit_btn.click()
            print("   ✓ Форма отправлена")

        except Exception as e:
            driver.save_screenshot("form_fill_error.png")
            pytest.fail(f"Ошибка при заполнении формы: {e}")

        # Шаг 5: Проверка успешного входа
        print("5. Проверяем успешность входа...")
        time.sleep(2)  # Ждем обработки запроса

        try:
            # Проверяем наличие кнопки Log out
            logout_btn = self.wait_for_element(driver, (By.ID, "logout2"), timeout=15)
            assert logout_btn.is_displayed(), "Кнопка Log out не отображается"
            print("   ✓ Кнопка 'Log out' найдена")

            # Проверяем приветствие
            welcome_msg = self.wait_for_element(driver, (By.ID, "nameofuser"), timeout=10)
            assert welcome_msg.is_displayed(), "Приветствие не отображается"
            print(f"   ✓ Приветствие: {welcome_msg.text}")

            # Проверяем имя пользователя
            assert "petr1" in welcome_msg.text, f"Имя не совпадает: {welcome_msg.text}"
            print("   ✓ Имя пользователя подтверждено")

            print("\n=== ТЕСТ УСПЕШНО ПРОЙДЕН! ===\n")

        except TimeoutException:
            # Проверяем наличие ошибки в alert
            try:
                alert = driver.switch_to.alert
                error_msg = alert.text
                alert.accept()
                pytest.fail(f"Сервер вернул ошибку: {error_msg}")
            except:
                driver.save_screenshot("login_failed.png")
                print("\n=== ТЕСТ ПРОВАЛИЛСЯ ===")
                pytest.fail("Не удалось войти в систему. Проверьте логин и пароль")

        # Финальная пауза для визуального подтверждения
        time.sleep(2)


if __name__ == "__main__":
    # Запуск с подробным выводом
    pytest.main([__file__, "-v", "-s", "--tb=short", "--capture=no"])