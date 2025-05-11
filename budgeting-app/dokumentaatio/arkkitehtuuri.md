# Arkkitehtuurikuvaus
## Rakenne

Ohjelma noudattaa kolmitasoista kerrosarkkitehtuuria. Koodin pakkausrakenne seuraavanlainen: 

![image](https://github.com/user-attachments/assets/68ad9c3d-7350-4d40-b6a4-303f388c1e18)

Rakenne jakautuu seuraavasti:
- ui: Sisältää käyttöliittymästä vastaavan koodin
- services: Sisältää sovelluslogiikasta vastaavan koodin
- repositories: Sisältää tietojen pysyväistallennuksesta vastaavan koodin
- entities: Sisältää luokkia, jotka kuvastavat sovelluksen käyttämiä tietokohteita

## Käyttöliittymä

Käyttöliittymässä on neljä eri näkymää:

- kirjautuminen
- uuden käyttäjän rekisteröinti
- valikko
- budjettien hallinta

Näkymistä yksi on aina kerrallaan näkyvissä. Näkymien hallinnasta vastaa BudgetingUI-luokka. Käyttöliittymä on pyritty eristämään sovelluslogiikasta: se ainoastaan kutsuu BudgetingService-luokan metodeja. Sovelluksen tilan muuttuessa (esim. käyttäjä kirjautuu, budjetti tai kulu lisätään/poistetaan), näkymä päivitetään kutsumalla näkymän omaa päivitysmetodia, joka hakee tarvittavat tiedot sovelluslogiikalta ja rendaa näkymän uudelleen.

Budjettien hallintanäkymä on jaettu pienempiin komponentteihin selkeyden vuoksi:

- BudgetTab
- ExpenseTab
- BudgetSelector
- BudgetSummary
- ExpenseHistory


## Päätoiminnallisuudet

### Rekisteröityminen

Rekisteröityessä käyttäjä antaa käyttäjänimen sekä salasanan. Tapahtumankäsittelijä kutsuu BudgetingService-luokan metodia `register_user`, joka tarkistaa samalla UserRepositorya hyödyntäen onko käyttäjänimi jo varattu. Mikäli se ei ole varattu käyttäjä ohajataan ilmoituksen saattelemana kirjautumisnäkymään.

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant BudgetingService
  participant UserRepository
  participant newUser
  User->>UI: click "Register" button
  UI->>BudgetingService: register_user("username", "password")
  BudgetingService->>UserRepository: find_by_username("username")
  UserRepository-->>BudgetingService: None
  BudgetingService->>newUser: User("username", "password")
  BudgetingService->>UserRepository: create(username, password)
  UserRepository-->>BudgetingService: user
  BudgetingService-->>UI: user
  UI->>UI: _show_login_after_register()
```
### Kirjautuminen

Kirjautuessa käyttäjä syöttää käyttäjänimen sekä salasanan, jonka BudgetingService välittää metodille `get_user.` Metodi hyödyntää UserRepositorya, joka tarkistaa tiedot tietokannasta ja tarkastaa salasanan. Kaiken onnistuessa siirrytään päävalikkoon eli "menuun".

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant BudgetingService
  participant UserRepository
  User->>UI: click "Login" button
  UI->>BudgetingService: get_user("username", "password")
  BudgetingService->>UserRepository: find_by_username("username", "password")
  UserRepository-->>BudgetingService: user
  BudgetingService-->>UI: user
  UI->>UI: show_main_menu()
```
### Uuden budjetin luominen

Uutta budjettia luodessa käyttäjä antaa sille nimen ja summan. Nappia painaessa se kutsuu BudgetingService-luokan metodia `add_budget_to_user`, joka tarkistaa syöteen ja tallentaa sen tietokantaan. Käyttöliittymä päivittyy oikeaksi kutsumalla metodia `_load_data()`. 

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant BudgetingService
  participant BudgetRepository
  participant budget
  User->>UI: click "Add Budget"
  User->>UI: input budget name "Vuokra"
  User->>UI: input budget amount "1000"
  User->>UI: click "Add Budget"
  UI->>BudgetingService: add_budget_to_user("username", "Vuokra", 1000.0)
  BudgetingService->>BudgetRepository: create("Vuokra", 1000.0, "username")
  BudgetRepository-->>BudgetingService: budget
  BudgetingService-->>UI: budget
  UI->>UI: _load_data()
```

## Tietojen tallennus

Sovellus tallentaa tiedot SQLite-tietokantaan. Tietokannassa on kolme taulua:

- users: Käyttäjien tiedot (id, username, password)
- budgets: Budjettien tiedot ( id, name, total_amount, user_id)
- expenses: kulujen tiedot (id, description, amount, budget_id)

Tietokantaa käsittelevät luokat UserRepository ja BudgetRepository. 

## Luokkakaavio

Kaaviossa sovelluksen tärkeimmät luokat sekä niiden suhteet. Yhdellä budjetilla voi olla monta taulua, BudgetinService käyttää molepia repository-luokkia, joilla taas on omia tietueitaan. 

```mermaid
classDiagram
    class User {
        username
        password
    }

    class Budgeting {
        id
        name
        total_amount
        expenses
        get_remaining_budget()
        add_expense()
    }

    class Expense {
        id
        budget_id
        description
        amount
    }

    class BudgetingService {
        register_user()
        get_user()
        add_budget_to_user()
        get_user_budgets()
        add_expense()
    }

    class UserRepository {
        create()
        find_by_username()
        find_all()
        delete_all()
    }

    class BudgetRepository {
        create()
        find_all_by_username()
        get_budget_by_id()
        get_budget_expenses()
        add_expense()
        remove_expense()
        remove_budget()
    }

    Budgeting "1" *-- "*" Expense
    BudgetingService --> UserRepository
    BudgetingService --> BudgetRepository
    UserRepository --> User
    BudgetRepository --> Budgeting
    BudgetRepository --> Expense
```

## Heikkoudet

- resetoidessa budjetteja täytyy palata menuun tai lisätä uusi budjetti nähdäkseen muutokset
- käyttäjätunnus ja salasana voivat olla mahdottoman pitkiä (tälläisessä sovelluksessa ei vakavaa)
