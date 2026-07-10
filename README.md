# Boom API 🚀

Backend escalable y seguro desarrollado en Django y Django Rest Framework (DRF), diseñado específicamente para soportar una aplicación orientada al público infantil. Utiliza PostgreSQL como base de datos persistente y Redis para la gestión de caché de alta velocidad, optimización de sesiones y control de tráfico (*throttling*).

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.14+
* **Framework Principal:** Django 6.0.7 & Django Rest Framework 3.17.1
* **Base de Datos Principal:** PostgreSQL 17+
* **Caché y Sesiones:** Redis 5.2.1
* **Frontend Compatible:** Angular (Puerto 4200)

---

## 🔒 Pilares de Seguridad (Enfoque Infantil)

Dado que la aplicación está diseñada para niños, el backend implementa las siguientes medidas de seguridad desde su inicialización:
1.  **Minimización de Datos:** No se recopilan ni almacenan nombres reales, correos de menores ni datos de geolocalización. La identificación se maneja por nombres de usuario anónimos/apodos.
2.  **Throttling Estricto:** Limitación de peticiones por minuto (`30/min` para anónimos, `120/min` para autenticados) gestionada mediante Redis para evitar abusos o clicks repetitivos en la interfaz.
3.  **Cookies Seguras:** Configuración de `HttpOnly` y protección contra CSRF/Session Hijacking automatizada para entornos de producción.

---

## 🚀 Guía de Instalación y Despliegue Local

Sigue estos pasos para clonar y levantar el entorno de desarrollo en tu máquina local (optimizado para Arch Linux):

### 1. Clonar el proyecto y entrar al directorio
```bash
cd ~/Desktop/bacckendBoom