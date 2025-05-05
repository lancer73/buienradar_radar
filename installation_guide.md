# Buienradar Regenradar Integratie voor Home Assistant

Deze integratie toont de actuele regenradar van Buienradar als een camera-entiteit in je Home Assistant-dashboard.

## Installatie-instructies

### Optie 1: Installatie via HACS (aanbevolen)

1. Zorg ervoor dat je [HACS (Home Assistant Community Store)](https://hacs.xyz/) hebt geïnstalleerd.
2. Ga naar HACS in je Home Assistant interface.
3. Klik op "Integraties".
4. Klik op de drie puntjes rechtsboven en kies "Custom repositories".
5. Voeg de volgende informatie toe:
   - Repository URL: `https://github.com/jouw-gebruikersnaam/buienradar-radar`
   - Categorie: Integratie
6. Klik op "Toevoegen".
7. Zoek naar "Buienradar Regenradar" en installeer de integratie.
8. Herstart Home Assistant.

### Optie 2: Handmatige installatie

1. Maak een nieuwe map aan in je Home Assistant configuratiemap:
   ```
   /config/custom_components/buienradar_radar/
   ```

2. Download alle bestanden van de integratie en plaats ze in deze map:
   - `__init__.py`
   - `camera.py`
   - `config_flow.py`
   - `manifest.json`
   - `strings.json`
   - En de map `translations/` met daarin `en.json` en `nl.json`

3. Herstart Home Assistant.

## Configuratie

### Optie 1: Via de gebruikersinterface (aanbevolen)

1. Ga naar Home Assistant Configuratie -> Integraties.
2. Klik op de knop "Integratie toevoegen" rechtsonder.
3. Zoek naar "Buienradar" en selecteer de integratie.
4. Volg de stappen in de configuratiewizard:
   - Geef een naam voor de radar (standaard: "Buienradar Regenradar")
   - Stel het verversingsinterval in seconden in (standaard: 300 seconden)

### Optie 2: Via configuration.yaml (oudere methode)

Je kunt de integratie ook nog steeds configureren via configuration.yaml:

```yaml
camera:
  - platform: buienradar_radar
    name: Regenradar
    image_refresh_seconds: 300  # optioneel, standaard is 300 seconden (5 minuten)
```

### Configuratie-opties

| Parameter | Type | Vereist | Standaard | Beschrijving |
| --------- | ---- | ------- | --------- | ------------ |
| name | string | nee | Buienradar Regenradar | Naam van de camera-entiteit |
| image_refresh_seconds | integer | nee | 300 | Interval in seconden tussen het verversen van de afbeelding |

## De radar toevoegen aan je dashboard

Na het installeren en configureren van de integratie:

1. Ga naar je Lovelace dashboard.
2. Klik op "Bewerken" en dan op "Kaart toevoegen".
3. Kies "Camera" kaart.
4. Selecteer de "Buienradar Regenradar" camera-entiteit.
5. Pas eventueel de titel en andere instellingen aan.
6. Klik op "Opslaan".

## Probleemoplossing

Als je problemen ondervindt:

1. Controleer je Home Assistant logbestanden voor eventuele foutmeldingen.
2. Zorg ervoor dat Home Assistant toegang heeft tot internet om de Buienradar API te bereiken.
3. Als de radar niet wordt bijgewerkt, probeer dan de verversingstijd te verlagen.

## Benodigde afhankelijkheden

Deze integratie maakt gebruik van de standaard Python-bibliotheken die al in Home Assistant beschikbaar zijn. Er zijn geen extra afhankelijkheden nodig.