# Buienradar Regenradar voor Home Assistant

Deze integratie toont de actuele regenradar van Buienradar als een camera entiteit in Home Assistant.

## Installatie

### HACS (Home Assistant Community Store)
1. Voeg deze repository toe als een custom repository in HACS
2. Installeer de integratie

### Handmatige installatie
1. Kopieer de bestanden in de `custom_components/buienradar_radar` map naar je Home Assistant `/config/custom_components/buienradar_radar` map
2. Herstart Home Assistant

## Configuratie

Voeg het volgende toe aan je `configuration.yaml`:

```yaml
camera:
  - platform: buienradar_radar
    name: Regenradar
    image_refresh_seconds: 300  # optioneel, standaard is 300 seconden (5 minuten)
```

## Parameters

| Parameter | Type | Vereist | Standaard | Beschrijving |
| --------- | ---- | ------- | --------- | ------------ |
| name | string | nee | Buienradar Regenradar | Naam van de camera entiteit |
| image_refresh_seconds | integer | nee | 300 | Interval in seconden tussen het verversen van de afbeelding |