# swisshydrodata

swisshydrodata is a library that allow you to request data from the Swiss Federal Office for the Environment FOEN.

## Example
```
from swisshydrodata import SwissHydroData 

sh = SwissHydroData()
s.load_station_data(2143)
s.get_latest_level()
s.get_latest_temperature()
s.get_latest_discharge()
```

