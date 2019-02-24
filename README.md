# pingis-bokning
Our excellent system for checking if the table tennis table is free and for making reservations

## Endpoints
*/api/status [GET]* -- Returns current status of tables

*api/book [POST]* -- Reserve either table

*api/sensor_data* -- Gets input from sensors and determines whether tables now are free or occupied.