```mermaid
sequenceDiagram
participant main
participant rautatietori
participant ratikka6
participant bussi244
participant laitehallinto
participant lippu_luukku
participant kallen_kortti

main->>rautatietori: Lataajalaite()
main->>ratikka6: Lukijalaite()
main->>bussi244: Lukijalaite()

main->>laitehallinto: lisaa_lataaja(rautatietori)
main->>laitehallinto: lisaa_lukija(ratikka6)
main->>laitehallinto: lisaa_lukija(bussi244)

main->>lippu_luukku: Kioski()
main->>lippu_luukku: osta_matkakortti("Kalle")
lippu_luukku->>kallen_kortti: Matkakortti("Kalle")
kallen_kortti-->>lippu_luukku: arvo: 0

lippu_luukku->>main: kallen_kortti

main->>rautatietori: lataa_arvoa(kallen_kortti, 3)
rautatietori->>kallen_kortti: kasvata_arvoa(3)

main->>ratikka6: osta_lippu(kallen_kortti, 0)
kallen_kortti-->>ratikka6: arvo: 3
ratikka6->>kallen_kortti: vahenna_arvoa(1.5)
ratikka6-->>main: true

main->>bussi244: osta_lippu(kallen_kortti, 2)
kallen_kortti-->>bussi244: arvo: 1.5
bussi244-->>main: false
```
