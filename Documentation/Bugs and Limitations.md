# Bugs and Limitations

I know of the following bugs and limitations. Due to time constraints I will
probably not be able to fix all of them, but I will try nevertheless. 

## Bugs

### SQL TRIGGER

**Severity:** low

**Probability of occurrence:** very low

Flight Control uses SQL Triggers to increment the AircraftLocation,
AircraftPower and FlightData ids grouped by the drone id. It is *theoretically*
possible that if two new datasets of the same type with the same drone id
arrive at the exact same time, that the id of these two new datasets are updated
to be the same. This is very unlikely, but still possible.
