# 🐾 Proyecto Lynko - Frontend
 
Armamos este documento para explicarte, de forma muy natural y directa, exactamente en dónde quedaron metidos los **5** requisitos técnicos que nos pediste para la entrega a lo largo de nuestra arquitectura de hojas de estilo (`.css`). ¡Cero rodeos!

---

## Rquisitos tecnicos

### 1. Ids, Clases y Selectores de Etiqueta
Para que el diseño no fuera un caos, organizamos el CSS usando los tres selectores de cajón en todos nuestros archivos:
* **Selectores de Etiqueta:** Los usamos para darle un estilo global y base a las vistas sin repetir código. Los verás aplicados en etiquetas primarias como `body`, `header`, `footer`, `table`, `th`, `td` y los títulos `h1, h2, h3, h4` en archivos base como `landing.css`, `admin.css`, `login.css` y `registro.css`.
* **Selectores de ID (`#`):** Son para los bloques únicos estructurales que no se repiten. Por ejemplo, el menú de navegación (`#main-header`) y la pantalla de bienvenida (`#hero-section`) en `landing.css`, o los contenedores principales de los formularios en `login.css` y `registro.css`.
* **Selectores de Clase (`.`):** Los usamos para los componentes modulares y repetibles. Los mejores ejemplos son las tarjetas de rendimiento (`.subject-performance-card`) en `progreso.css`, las tarjetas de las materias (`.feature-card`) en `landing.css`, y las alertas o botones de gestión en `admin-gestion.css`, `preguntas.css` y `expediente.css`.

### 2. El Modelo de Cajas (Box Model)
Todo en la web son cajitas, y aquí las controlamos al derecho y al revés en cada vista:
* Lo primero que hicimos fue asegurar el flujo limpio poniendo `box-sizing: border-box;` en el `body` global (`landing.css`, `admin.css`). Esto es un salvavidas para que cuando añadamos padding o bordes a los contenedores, el tamaño no se deforme.
* Si miras las cajas de las preguntas en `preguntas.css`, las tarjetas de perfil en `perfil.css` o los contenedores de premios en `recompensa.css`, verás un manejo explícito de `width`, `height`, `padding` (el espacio para que los textos respiren por dentro), `margin` (para que las cajas no se peguen entre sí) y los `border` redondeados estilo videojuego.

### 3. Flexbox por Todos Lados
Para que la página sea responsiva, se adapte a cualquier pantalla y todo quede alineado perfectamente en el centro (¡como las flechas de la trivia!), usamos Flexbox como nuestro sistema de alineación principal:
* En `landing.css` lo usamos en el `#main-header` y el `#hero-section` con `display: flex; justify-content: space-between; align-items: center;`. Así los logos quedan a la izquierda, los botones a la derecha y todo centrado verticalmente.
* En `progreso.css` y `expediente.css` lo aplicamos en las estructuras de las tarjetas para alinear de forma horizontal los avatares decorativos junto a las barras de progreso y los textos informativos sin que nada se descuadre.
* También se usa en `admin-gestion.css` y `materias.css` para organizar las grillas de datos y los botones de acción de manera flexible.

### 4. Posicionamiento Avanzado (Sticky Header)
Queríamos que el usuario pudiera navegar por la landing page o el panel de administración sin perder de vista los accesos rápidos o menús superiores.
* Lo logramos aplicando posicionamiento en `#main-header` (`landing.css`) y en las barras superiores de control en `admin.css` mediante las propiedades: `position: sticky; top: 0; z-index: 100;`. Esto hace que los menús se queden "pegados" en la parte de arriba del navegador mientras haces scroll.

### 5. Google Fonts e Imágenes en DIVs
* **Tipografías con personalidad:** Enlazamos Google Fonts en el header de nuestros estilos. Usamos `'Fredoka'` para los títulos, preguntas de juego y feedbacks (en `landing.css`, `progreso.css`, `recompensa.css`) porque es redondita y muy infantil, y `'Nunito'` para los párrafos, formularios y botones comunes (en `login.css`, `registro.css`, `perfil.css`) porque es súper limpia y fácil de leer.
* **Manejo de Imágenes en DIVs:** Para evitar que las imágenes se deformen o rompan el diseño responsivo, en lugar de usar etiquetas `<img>` rígidas, usamos contenedores `<div>` (como en `.hero-imagen-div` de `landing.css`) y los controlamos desde el CSS con propiedades de fondo:
  * `background-image: url('...');` para cargar la foto usamos tmb la base de datos para que con el url guardado lo ponga ahí.
  * `background-size: cover;` para que la imagen llene el espacio perfectamente adaptándose al tamaño del contenedor.
  * `background-position: center;` para que no se corte lo importante y quede siempre centrada.

---

##Organización de nuestros archivos CSS
Para que el proyecto sea mantenible y escalable, dividimos los estilos por módulos claros:
* **Páginas Públicas:** `landing.css`, `login.css`, `registro.css`.
* **Panel de Estudiante:** `progreso.css`, `perfil.css`, `recompensa.css`, `materias.css`.
* **Panel de Administración:** `admin.css`, `admin-gestion.css`, `preguntas.css`, `expediente.css`.
