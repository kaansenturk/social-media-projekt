# social-media-projekt



## Frontend mit Vue.js:

- Erstellen einer Hauptkomponente, die das grundlegende Layout deiner Social-Media-Plattform enthält, wie z.B. eine Navigationsleiste, einen Seiteninhalt und einen Fußzeilenbereich.

- Definieren einer separaten Komponenten für verschiedene Ansichten, z.B. für die Startseite, den News-Feed, Benutzerprofile, Benachrichtigungen usw.

- Implementieren von Routing mit vue-router, um zwischen den verschiedenen Ansichten zu navigieren.

- Verwendung von Vuex oder einer ähnlichen State-Management-Lösung, um den Anwendungsstatus zu verwalten, Benutzerdaten zu speichern und die Kommunikation zwischen den Komponenten zu erleichtern.


## Backend mit FastAPI:
- Backend im src Ordner. Von dort starten mit

    ´´´uvicorn app:app --reload´´´

- Definieren von notwendigen Modellen, um Daten in der SQLite-Datenbank zu speichern, z.B. Benutzerprofile, Beiträge, Kommentare usw.

- Implementieren von Routen oder Endpunkten, um die erforderlichen Funktionen bereitzustellen, wie z.B. die Registrierung und Anmeldung von Benutzern, das Erstellen und Abrufen von Beiträgen, die Verwaltung von Freundschaftsanfragen usw.

- Verarbeiten von Anfragen im Backend, validieren und speichern der Daten in der Datenbank.

- Implementierung der notwendigen Sicherheitsmaßnahmen, wie z.B. Authentifizierung und Autorisierung, um sicherzustellen, dass nur authentifizierte Benutzer auf geschützte Funktionen zugreifen können.

- Nutzung von FastAPI oder Django Admin, um das Admin-Backend für die Verwaltung von Daten und Benutzern bereitzustellen.


## SQLite-Datenbank:

- Entwurg eines Datenbankschemas, das die erforderlichen Tabellen und Beziehungen für das Social-Media-Projekt abbildet.

- Verwendung von SQL-Alter-Befehlen, um das Schema entsprechend den Anforderungen der Anwendung zu aktualisieren, wenn sich die Datenmodellierung ändert.

- Implementierung von Abfragen und Operationen, um Daten aus der Datenbank abzurufen, zu aktualisieren und zu löschen.


## Admin-Backend:

- Nutzung der eingebauten Funktionen von FastAPI oder Django Admin, um ein Admin-Backend bereitzustellen.

- Definierung der erforderlichen ModelAdmin-Klassen, um die Verwaltung von Benutzern, Beiträgen, Kommentaren usw. zu ermöglichen.

- Modulare anpassung des Admin-Backend nach Bedarf, um zusätzliche Funktionen oder Ansichten hinzuzufügen.


- Verwendung von RESTful-APIs oder GraphQL, um die Kommunikation zwischen Frontend und Backend zu erleichtern.