# social-media-projekt

Dokumentation: 

Setup über Makefile:
    in root-directory:
        ```
        make init # ausführen für komplettes Setup inklusive neuer DB.
        make start # ausführen um backend und frontend lokal hochzufahren
        ```
            Windows10: $choco install make

## Frontend mit Vue.js:
Frontend aufsetzen:

```
npm install

npm run build

npm run serve
```
- Erstellen einer Hauptkomponente, die das grundlegende Layout deiner Social-Media-Plattform enthält, wie z.B. eine Navigationsleiste, einen Seiteninhalt und einen Fußzeilenbereich.

- Definieren einer separaten Komponente für verschiedene Ansichten, z.B. für die Startseite, den Messenger, Benutzerprofile usw.

- Implementieren von Routing mit vue-router, um zwischen den verschiedenen Ansichten zu navigieren.

- Verwendung von Vuex oder einer ähnlichen State-Management-Lösung, um den Anwendungsstatus zu verwalten, Benutzerdaten zu speichern und die Kommunikation zwischen den Komponenten zu erleichtern.


## Backend mit FastAPI:
- Backend im src Ordner. Von dort starten mit

    ```
    uvicorn app:app --reload
    ```

- Definieren von notwendigen Modellen, um Daten in der SQLite-Datenbank zu speichern, z.B. Benutzerprofile, Beiträge, Kommentare usw.

- Implementieren von Routen oder Endpunkten, um die erforderlichen Funktionen bereitzustellen, wie z.B. die Registrierung und Anmeldung von Benutzern, das Erstellen und Abrufen von Beiträgen, die Verwaltung von Freundschaftsanfragen usw.

- Verarbeiten von Anfragen im Backend, validieren und speichern der Daten in der Datenbank.

- Implementierung der notwendigen Sicherheitsmaßnahmen, wie z.B. Authentifizierung und Autorisierung, um sicherzustellen, dass nur authentifizierte Benutzer auf geschützte Funktionen zugreifen können.

- Nutzung von FastAPI oder Django Admin, um das Admin-Backend für die Verwaltung von Daten und Benutzern bereitzustellen.


## SQLite-Datenbank:

- Entwurg eines Datenbankschemas, das die erforderlichen Tabellen und Beziehungen für das Social-Media-Projekt abbildet.

- Verwendung von SQL-Alter-Befehlen, um das Schema entsprechend den Anforderungen der Anwendung zu aktualisieren, wenn sich die Datenmodellierung ändert.

- Implementierung von Abfragen und Operationen, um Daten aus der Datenbank abzurufen, zu aktualisieren und zu löschen.

Needed Libraries:

$pip install python-multipart

$pip install geocoder

## Admin-Backend:

- Nutzung der eingebauten Funktionen von FastAPI oder Django Admin, um ein Admin-Backend bereitzustellen.

- Definierung der erforderlichen ModelAdmin-Klassen, um die Verwaltung von Benutzern, Beiträgen, Kommentaren usw. zu ermöglichen.

- Modulare anpassung des Admin-Backend nach Bedarf, um zusätzliche Funktionen oder Ansichten hinzuzufügen.

- Verwendung von RESTful-APIs oder GraphQL, um die Kommunikation zwischen Frontend und Backend zu erleichtern.

## Die Pages:

- Startseite: Eine Anfangsseite, auf dem der Nutzer sich anmelden oder auch registrieren kann.

- Account Info: Ein persönliches Profil, auf dem Nutzer Informationen wie ihren Namen, ein Profilbild und andere Details über sich selbst angeben können und angezeigt bekommen.

- Beiträge/Timeline: Der Hauptbereich, in dem Nutzer Inhalte wie Texte, Bilder oder GIFs veröffentlichen und anzeigen können. Diese Inhalte werden in einer chronologischen Reihenfolge angezeigt.

- Followee/Follower: Eine Liste der anderen Nutzer, mit denen der Nutzer eine Verbindung hergestellt hat, entweder durch Abonnenten (Follower) oder durch das Abonnieren (Folgen) ihrer Aktivitäten.

- Interaktionsmöglichkeiten: Die Social-Media-Plattfomr ermöglicht es den Nutzern, Beiträge zu kommentieren, zu liken um Interaktionen zu fördern.

- Nachrichten/Messenger: Ein privater Messaging-Dienst, über den Nutzer direkt miteinander kommunizieren können.

- Suchfunktion: Eine Suchleiste, mit der Nutzer nach anderen Nutzern suchen können.



### Credits
    Blaues Icon: <a href="https://www.flaticon.com/free-icons/home-address" title="home address icons">Home address icons created by fjstudio - Flaticon</a>

    Grünes Icon <a href="https://www.flaticon.com/free-icons/placeholder" title="placeholder icons">Placeholder icons created by Freepik - Flaticon</a>

    Hacker Icon: <a href="https://www.flaticon.com/de/kostenlose-icons/hacker" title="hacker Icons">Hacker Icons erstellt von Talha Dogar - Flaticon</a>

    Blank Profile Pic: 
    https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png

    Vue-leaflet-logo:
    https://vue2-leaflet.netlify.app/logo.png

    GitHub Logo:
    https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png

    FastAPI Logo:
    https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png
    
    Axios Logo:
    https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Axios_%28computer_library%29_logo.svg/1280px-Axios_%28computer_library%29_logo.svg.png

    Python Logo:
    https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png

    Amazon EC2 Logo:
    https://devopsdatacenter.files.wordpress.com/2024/04/amazon_ec2.png

    SQLite Logo:
    https://e7.pngegg.com/pngimages/890/928/png-clipart-sqlite-logo-sqlite-logo-icons-logos-emojis-tech-companies-thumbnail.png
