# Dulzumat Site

Website para la web de Dulzumat.

Website construido con [Hugo](https://gohugo.io/), publicado en [Netlify](https://www.netlify.com/).

[![Netlify Status](https://api.netlify.com/api/v1/badges/288f22d4-c339-48d4-8a02-0578833b1e6a/deploy-status)](https://app.netlify.com/sites/clever-pare-22cc01/deploys)

![CI](https://github.com/llyorshch/dulzumat/workflows/CI/badge.svg?branch=master)

## Trabajo en local

Para trabajar en local, [instalar Hugo](https://gohugo.io/getting-started/installing/) y ejecutar `hugo server` en la raíz del proyecto para obtener un servidor local en <http://localhost:1313>. Los cambios en los ficheros del proyecto se reflejarán automáticamente en el servidor local.

Cualquier editor sirve pero [Visual Studio Code](https://code.visualstudio.com/) junto con el plugin [Hugo Helper](https://marketplace.visualstudio.com/items?itemName=rusnasonov.vscode-hugo) hacen una combinación bastante buena.

## Edición de contenidos

La edición de contenidos se realiza con [Netlify CMS](https://www.netlifycms.org/) en la [URL de administración](https://dulzumat.ge.org.es/admin). La autenticación se configura en [el servicio "Identity" de Netlify](https://app.netlify.com/sites/clever-pare-22cc01/identity).

La edición de la galería se realiza simplemente añadiendo y quitando ficheros en la carpeta [/static/images/galeria](static/images/galeria/).

## Publicación automática en el entorno de staging

La [configuración de Netlify](https://app.netlify.com/sites/clever-pare-22cc01/overview) está conectada al repositorio. Cada push al repositorio provocará que el site se reconstruya y se publique en <https://dulzumat.ge.org.es>. Este proceso puede llegar a tardar algunos minutos dependiendo de la carga en Netlify.

## Publicación manual en el entorno final

Este repositorio tiene configurada [una acción de Github](https://github.com/llyorshch/dulzumat/actions?query=workflow%3ACI) para construir el sitio y subirlo al FTP del hosting desde el que se sirve el dominio <https://www.dulzumat.com>.

Para lanzar [la acción](https://github.com/llyorshch/dulzumat/actions?query=workflow%3ACI) sólo hay que ejecutarla con el botón `Run workflow` sobre la rama `master`. 

## Personalización del tema

- Carpeta de imágenes: static/images
- Carpeta de estilos: themes/hargo/assets/scss