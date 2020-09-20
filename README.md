# Dulzumat Site

Website para la web de Dulzumat.

Website construido con [Hugo](https://gohugo.io/), publicado en [Netlify](https://www.netlify.com/). 

## Trabajo en local

Para trabajar en local, [instalar Hugo](https://gohugo.io/getting-started/installing/) y ejecutar `hugo server` en la raíz del proyecto para obtener un servidor local en <http://localhost:1313>. Los cambios en los ficheros del proyecto se reflejarán automáticamente en el servidor local.

Cualquier editor sirve pero [Visual Studio Code](https://code.visualstudio.com/) junto con el plugin [Hugo Helper](https://marketplace.visualstudio.com/items?itemName=rusnasonov.vscode-hugo) hacen una combinación bastante buena.

## Publicación automática

La [configuración de Netlify](https://app.netlify.com/sites/clever-pare-22cc01/overview) está conectada al repositorio. Cada push al repositorio provocará que el site se reconstruya y se republique. Este proceso puede llegar a tardar algunos minutos dependiendo de la carga en Netlify.

Por el momento, la web se pulica en <https://dulzumat.ge.org.es>. Más adelante, este entorno quedará como "staging" y la web se publicará en <https://www.dulzumat.es>.

## Edición de contenidos

La edición de contenidos se realiza con [Netlify CMS](https://www.netlifycms.org/) en la [URL de administración](https://dulzumat.ge.org.es/admin). La autenticación se configura en [el servicio "Identity" de Netlify](https://app.netlify.com/sites/clever-pare-22cc01/identity).

## Personalización del tema

- Carpeta de imágenes: static/images
- Carpeta de estilos: themes/hargo/assets/scss