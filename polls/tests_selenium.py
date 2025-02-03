from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")  # Para ejecución en GitHub Actions
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_create_questions_and_choices(self):
        self.selenium.get(f"{self.live_server_url}/admin/")

        # Iniciar sesión
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("isard")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("pirineus")
        password_input.send_keys(Keys.RETURN)

        # Esperar que cargue la página principal del admin
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Questions"))
        )

        # Ir a la sección de Questions y crear la primera
        self.selenium.find_element(By.LINK_TEXT, "Questions").click()
        self.selenium.find_element(By.LINK_TEXT, "Add Question").click()

        # Crear la primera pregunta con 2 choices
        self.selenium.find_element(By.NAME, "question_text").send_keys("¿Quién ganará la liga este año?")
        self.selenium.find_element(By.NAME, "pub_date").send_keys("2025-02-03 12:00:00")

        # Añadir las choices en el menú inline
        self.selenium.find_element(By.NAME, "choice_set-0-choice_text").send_keys("El Barça porque es el mejor jejej")
        self.selenium.find_element(By.NAME, "choice_set-1-choice_text").send_keys("El Madrid, por supuesto")
        self.selenium.find_element(By.NAME, "_save").click()  # Guardar la pregunta

        # Esperar que se guarde y luego crear la segunda pregunta
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Add Question"))
        )
        
        self.selenium.find_element(By.LINK_TEXT, "Add Question").click()
        self.selenium.find_element(By.NAME, "question_text").send_keys("¿Tortilla con o sin cebolla?")
        self.selenium.find_element(By.NAME, "pub_date").send_keys("2025-02-03 12:30:00")

        self.selenium.find_element(By.NAME, "choice_set-0-choice_text").send_keys("Sin cebolla, ¡qué ascooo!")
        self.selenium.find_element(By.NAME, "choice_set-1-choice_text").send_keys("Con cebolla, ¡me encanta!")
        self.selenium.find_element(By.NAME, "_save").click()

        # Comprobar que existen 4 Choices en el menú "Choices"
        self.selenium.find_element(By.LINK_TEXT, "Choices").click()
        choices = self.selenium.find_elements(By.CLASS_NAME, "field-choice_text")
        assert len(choices) >= 4, "No se encontraron las 4 Choices esperadas"

        print("✔ Se crearon correctamente 2 Questions y 4 Choices con respuestas graciosas")

