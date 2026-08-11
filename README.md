# 🐶 PobarOS — GitHub IMG Builder 0.5

Tohle je verze připravená pro **GitHub Actions**.

Nemusíš mít Linux ani WSL. GitHub provede build za tebe a jako výsledek stáhneš:

`PobarOS-TV.img`

Ten pak použiješ ve Windows v Raspberry Pi Imageru přes:

**OS → Use Custom → PobarOS-TV.img**

## 1. Vytvoř GitHub repository

Například:

`PobarOS`

Nastav ho jako Private nebo Public — podle tebe.

## 2. Nahraj celý obsah tohoto ZIPu

Důležitá je struktura:

```text
PobarOS/
├── .github/
│   └── workflows/
│       └── build.yml
├── app/
│   └── main.py
├── config/
│   └── pobar.yaml
├── layer/
│   └── pobar/
│       └── pobar.yaml
└── README.md
```

## 3. Spusť build

Na GitHubu:

**Actions → Build PobarOS IMG → Run workflow**

Počkej na dokončení.

## 4. Stáhni IMG

Po úspěšném buildu otevři konkrétní běh workflow.

Dole najdeš:

**Artifacts → PobarOS-TV**

Stáhneš ZIP a uvnitř bude:

```text
PobarOS-TV.img
SHA256SUMS.txt
```

## 5. Raspberry Pi Imager

Ve Windows:

1. Otevři Raspberry Pi Imager.
2. Vyber Raspberry Pi 4.
3. OS → **Use Custom**.
4. Vyber `PobarOS-TV.img`.
5. Vyber microSD.
6. Write.

Potom:

**microSD → Raspberry Pi 4 → HDMI → TV → USB klávesnice/myš → zapnout.**

## Poznámka

Build používá oficiální Raspberry Pi `rpi-image-gen` v2.7.0. Release v2.7.0 je aktuálně označený jako Latest a obsahuje mimo jiné opravy relevantní pro kiosk example a změny v user/group konfiguraci.

Toto je první GitHub-buildable verze. Pokud GitHub build selže na konkrétní vrstvě nebo configu, pošli mi log z failed workflow a upravíme builder podle přesné chyby — není potřeba nic instalovat na Windows.
