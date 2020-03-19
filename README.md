# Coronagotchi

A small handheld Corona Virus / COVID-19 tracker for Australia.

Runs on an RPi Zero and outputs to a Waveshare E-Ink display:

![Output](https://github.com/obsoletenerd/Coronagotchi/blob/master/CoronagotchiEPD.jpg)

Run locally it outputs the raw data (after it has been filtered by the script to only show Australian states), and generates a graph using matplotlib:

![Output](https://github.com/obsoletenerd/Coronagotchi/blob/master/CoronagotchiOutput.png)

## Status

Currently in progress and an utter mess. I'll tidy up the code and the repository to allow other people to replicate the project soon. At the moment the script assumes you already have the Waveshare screen running, and that the script + the CSVs are in a folder parallel to the lib/ and pic/ folders that come with the EPD. Over the next few days I'll tidy this up so it's a complete package ready to copy to any RPi with a Waveshare plugged in.

## Todo

- Clean up the script itself, lots of sections could be done better.

- Set up the Pi to scrape new CSVs daily with a cron job.

- 3D print a nice case for it.