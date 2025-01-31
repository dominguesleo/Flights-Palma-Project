from selenium import webdriver

def get_options():
    options = webdriver.ChromeOptions()
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Evita que se abra el navegador
    options.add_argument('--window-size=1920,1080') # Tamaño de la ventana
    options.add_argument('--disable-extensions')  # Deshabilitar extensiones
    options.add_argument('--disable-dev-shm-usage')  # Deshabilitar el uso compartido de memoria
    options.add_argument('--disable-gpu')  # Deshabilitar la aceleración de hardware
    options.add_argument('--no-sandbox')  # Añadir esta opción si estás ejecutando en un entorno de contenedor
    options.add_argument('--disable-notifications')  # Deshabilitar notificaciones
    options.add_argument('--disable-infobars')  # Deshabilitar la barra de información de Chrome
    options.add_argument('--disable-blink-features=AutomationControlled')  # Deshabilitar la automatización de Chrome
    options.add_argument('--disable-popup-blocking')  # Deshabilitar el bloqueo de ventanas emergentes
    options.add_argument('--disable-default-apps')  # Deshabilitar las aplicaciones predeterminadas de Chrome
    options.add_argument('--disable-features=TranslateUI')  # Deshabilitar la interfaz de traducción
    options.add_argument('--disable-prompt-on-repost')  # Deshabilitar el aviso de reenvío
    options.add_argument('--disable-sync')  # Deshabilitar la sincronización
    options.add_argument('--disable-background-networking')  # Deshabilitar la red en segundo plano
    options.add_argument('--disable-component-extensions-with-background-pages')  # Deshabilitar extensiones con páginas en segundo plano
    options.add_argument('--disable-background-timer-throttling')  # Deshabilitar la limitación de temporizadores en segundo plano
    options.add_argument('--disable-renderer-backgrounding')  # Deshabilitar el renderizado en segundo plano
    options.add_argument('--disable-device-discovery-notifications')  # Deshabilitar las notificaciones de descubrimiento de dispositivos
    options.add_argument('--disable-translate')  # Deshabilitar la traducción
    options.add_argument('--disable-client-side-phishing-detection')  # Deshabilitar la detección de phishing del lado del cliente
    options.add_argument('--disable-component-update')  # Deshabilitar la actualización de componentes
    options.add_argument('--disable-domain-reliability')  # Deshabilitar la fiabilidad del dominio
    options.add_argument('--disable-print-preview')  # Deshabilitar la vista previa de impresión
    options.add_argument('--disable-speech-api')  # Deshabilitar la API de voz
    options.add_argument('--disable-web-security')  # Deshabilitar la seguridad web
    options.add_argument('--disable-site-isolation-trials')  # Deshabilitar las pruebas de aislamiento de sitios
    options.add_argument('--disable-remote-fonts')  # Deshabilitar las fuentes remotas
    options.add_argument('--disable-remote-playback-api')  # Deshabilitar la API de reproducción remota
    options.add_argument('--disable-remote-playback')  # Deshabilitar la reproducción remota
    options.add_argument('--disable-remote-debugging')  # Deshabilitar la depuración remota
    options.add_argument('--disable-remote-extensions')  # Deshabilitar las extensiones remotas
    options.add_argument('--enable-unsafe-webgl') # Habilitar WebGL inseguro
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")  # Evita el bloqueo por parte de la página
    return options