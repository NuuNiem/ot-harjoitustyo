# Arkkitehtuurikuvaus
## Rakenne

Ohjelma noudattaa kolmitasoista kerrosarkkitehtuuria. Koodin pakkausrakenne seuraavanlainen: 
*kuva tulossa*

## Käyttöliittymä

Käyttöliittymässä on neljä eri näkymää:

- kirjautuminen
- uuden käyttäjän rekisteröinti
- valikko
- budjettien hallinta
- budjettien visualisointi

Näkymistä yksi on aina kerrallaan näkyvissä. Näkymien hallinnasta vastaa BudgetingUI-luokka. Käyttöliittymä on pyritty eristämään sovelluslogiikasta: se ainoastaan kutsuu BudgetingService-luokan metodeja.

Kun sovelluksen tila muuttuu (esim. käyttäjä kirjautuu, budjetti tai kulu lisätään/poistetaan), näkymä päivitetään kutsumalla näkymän omaa päivitysmetodia, joka hakee tarvittavat tiedot sovelluslogiikalta ja rendaa näkymän uudelleen.
  
## Luokkakaavio
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
        validate_and_create_budget()
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

## Sekvenssikaavio
Uuden budjetin luominen
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant BudgetingService
  participant BudgetRepository

  User->>UI: click "New Budget" button
  UI->UI: show_create_budget_view()
  User->>UI: input budget name "Vuokra"
  User->>UI: input budget amount "1000"
  User->>UI: click "Create" button
  UI->>BudgetingService: validate_and_create_budget("Vuokra", 1000, "Keijo")
  BudgetingService->>BudgetingService: validate budget data
  BudgetingService->>BudgetRepository: create("Vuokra", 1000, "Keijo")
  BudgetRepository-->>BudgetingService: new_budget
  BudgetingService-->>UI: new_budget
  UI->UI: show_budget_view(new_budget.id)
  UI->UI: display remaining budget: 1000
```
