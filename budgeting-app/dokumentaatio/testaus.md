# Testikattavuus
Sovelluksen testaus on toteutettu sekä automaattisilla yksikkötesteillä että manuaalisesti.

## Yksikkötestaus
Repositories: Testit varmistavat tietokantaoperaatioiden toimivuuden

- UserRepository: käyttäjien luonti, haku ja poistaminen
- BudgetRepository: budjettien ja kulujen hallinta

Sovelluslogiikka: BudgetingService-luokan testit kattavat

Käyttäjien rekisteröinnin ja kirjautumisen
- Budjettien luomisen ja validoinnin
- Kulujen lisäämisen ja käsittelyn
- Testeissä hyödynnetään SQLiten muistissa toimivaa tietokantaa, jolloin testit eivät vaikuta varsinaiseen tietokantaan.

Esimerkiksi BudgetRepository-testeissä testataan:

- Budjettien luominen ja tarkistus käyttäjille
- Virheellisten syötteiden käsittely
- Budjettirajojen noudattaminen kulujen lisäyksessä
- Kulujen ja budjettien poistaminen
- Testauksen ulkopuolelle jätetyt osat
- Käyttöliittymän Tkinter-komponentteja ei testata automaattisesti. Sen toimintaa on testattu manuaalisesti eri käyttötilanteissa.

## Kattavuus
