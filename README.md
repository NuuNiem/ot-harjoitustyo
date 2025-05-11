# Ohjelmistotekniikka, harjoitustyö

Sovelluksen avulla käyttäjien on mahdollista luoda, hallita ja tarkastella budjetteja.

## Dokumentaatio
- [Käyttöohje](./budgeting-app/dokumentaatio/kayttoohje.md)
- [Vaatimusmäärittely](./budgeting-app/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](./budgeting-app/dokumentaatio/arkkitehtuuri.md)
- [Testausdokumentti](./budgeting-app/dokumentaatio/testaus.md)
- [Työaikakirjanpito](./budgeting-app/dokumentaatio/tuntikirjanpito.md)
- [Changelog](./budgeting-app/dokumentaatio/changelog.md)

## Asennus

1. Siirry hakemistoon budgeting-app:

```bash
cd budgeting-app
```
2. Asenna riippuvuudet komennolla:
   
```bash
poetry install
```

3. Käynnistä sovellus komennolla:
```bash
poetry run invoke start
```

### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```
### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

### Pylint

```bash
poetry run invoke lint
```

