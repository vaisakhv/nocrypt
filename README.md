# noCRYPT  
> A Secure and private note taking progressive webapp.
https://raw.githubusercontent.com/vaisakhv/nocrypt/master/app/static/images/icons/icon-120x120.png

noCRYPT is an encrypted note taking app. 
##Features
-Can be treated as a native app in any pltform since it is a Progressive Web App(PWA)
-Requires no personal identifiers(just a Username and a password)
-Has a simple WYSIWYG Editor
-The notes are encrypted with AES
-We don't know your password. We store your SHA-256 hash of your password.
-Since your password's hash is the encryption key for the AES encryption of the notes, if you lose or reset your password all the notes that you created with your old password 
cannot be decrypted.

![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg)
![GitHub](https://img.shields.io/github/license/vaisakhv/nocrypt)


![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/vaisakhv/nocrypt/pycryptodomex)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/vaisakhv/nocrypt/flask)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/vaisakhv/nocrypt/werkzeug)


## Links

- Repository: https://github.com/umluizlima/flask-pwa
- Issue tracker: https://github.com/umluizlima/flask-pwa/issues
- Inspiration and references:
  - [Google's Seu Primeiro PWA](https://developers.google.com/web/fundamentals/codelabs/your-first-pwapp/?hl=pt-br)
  - [Flask PWA demo](https://github.com/uwi-info3180/flask-pwa)
  - [Google's Workbox](https://developers.google.com/web/tools/workbox/)

## Licensing

This project is licensed under GPL-3.0 License.
