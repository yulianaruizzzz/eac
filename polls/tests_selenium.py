from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):
    # no crearem una BD de test en aquesta ocasió (comentem la línia)
    #fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()
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
        self.selenium.implicitly_wait(5)

        # Ir a la sección de Questions y crear la primera
       # self.selenium.find_element(By.LINK_TEXT, "Questions").click()
        #self.selenium.find_element(By.XPATH, "//*[contains(text(),'Add question')]").click()
        self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/question/add/']").click() 
        # Crear la primera pregunta con 2 choices
        self.selenium.find_element(By.NAME, "question_text").send_keys("¿Quién ganará la liga este año?")
        self.selenium.find_element(By.NAME, "pub_date_0").send_keys("2025-02-03")
        self.selenium.find_element(By.NAME, "pub_date_1").send_keys("12:00:00")



        # Añadir las choices en el menú inline
        self.selenium.find_element(By.NAME, "choice_set-0-choice_text").send_keys("El Barça porque es el mejor jejej")
        self.selenium.find_element(By.NAME, "choice_set-1-choice_text").send_keys("El Madrid, por supuesto")
        self.selenium.find_element(By.NAME, "_save").click()  # Guardar la pregunta

        # Esperar que se guarde y luego crear la segunda pregunta
        self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/question/add/']").click()                  

 # Crear la primera pregunta con 2 choices
        self.selenium.find_element(By.NAME, "question_text").send_keys("¿Arroz con leche?")
        self.selenium.find_element(By.NAME, "pub_date_0").send_keys("2025-02-03")
        self.selenium.find_element(By.NAME, "pub_date_1").send_keys("12:00:00")



        # Añadir las choices en el menú inline
        self.selenium.find_element(By.NAME, "choice_set-0-choice_text").send_keys("si")
        self.selenium.find_element(By.NAME, "choice_set-1-choice_text").send_keys("no")
        self.selenium.find_element(By.NAME, "_save").click()  # Guardar la pregunta       
        # Esperar que se guarde y luego crear la segunda pregunta
        self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/choice/']").click()           
        choices = self.selenium.find_elements(By.XPATH, "//th[@class='field-__str__']/a")
        self.assertEqual(
            len(choices), 4, f"holapepsicola"
        )

