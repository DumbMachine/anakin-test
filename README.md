# Anakin Assignment

Total Time Spent: 1.8 hours
Scrapped data stats:

```
{
   "location": 'Ground Floor, Building San Lazaro Compund, C. S. Gatmaitan Ave, Santa Cruz, Manila, 1003 Metro Manila, Philippines',
   "total_listing": 1056
}
```

FTE Assignment

TODO: Grab restro data accompanied by `latitudes and longitudes` from food.grab.com
Approach:

1. Open url and enter a predefined location:
   ```
   Marawi City Police Station - West, Matina Crossing, Davao City, Davao del Sur, Davao City, Davao Region (Region XI), 8000, Philippines
   ```
   mimicking the input and clicking of **search** button.
2. Wait `5` before pressing **load more**.
3. Scroll all the way down and press on **load more**.
4. Grab lat/long data and store temp on file.
5. Start again from `2`.

