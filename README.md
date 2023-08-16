![maintained](https://img.shields.io/maintenance/yes/2023.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# SSAM Hämtschema
A simple integration to provide information about when SSAM (Södra Smålands Avfall och Miljö) is next emptying your waste bin(s).
## Installation
### Manual installation
1. Download the [latest release](https://github.com/kverqus/hassam/releases/latest).
2. Unpack the release and copy the `custom_components/hassam` directory into the `custom_components` directory of your Home Assistant installation.
3. Restart Home Assistant.
4. Configure the `hassam` integration.
## Configuration
To configure the integration you must supply it with an address in the correct format. The string will include some additional information, not only the address of your house. The address string can be collected from https://ssam.se/mitt-ssam/hamtdagar.html or by using the service `hassam.find_address` which is part of the integration.
### Search for your address string
To search for your address string using the supplied service you should first open two tabs of the Home Assistant Developer Tools view. 

In the first tab:
Go to `Developer Tools`/`Events`, enter "hassam" into the "Event to subscribe to" input box and click "Start Listening"

In the second tab:
Go to `Developer Tools`/`Services`, search for "hassam.find_address" in the "Service" input box and click the search result. Check the "Address" checkbox, input your address and click "Call service".

After clicking the "Call service" button the result will be available in the tab with your active listener. The SSAM API will return a list with a maximum of 10 results. Copy the entire string (without the quotation marks)
### Configure the integration
Go to `Settings`/`Devices & Services`, click on the `+ ADD INTEGRATION` button, select `SSAM Hämtschema` and configure the integration.

If you would like to add more than one collection schedule click on the `+ ADD INTEGRATION` button again and configure the integration.

## Data
The configured entity (`sensor.ssam_schedule_<name>`) will create a list of entries inside its attributes per row retrieved from the SSAM API.

### Example entry
```
{
    'next_waste_pickup': '2023-08-17',
    'days_from_today': 1,
    'waste_pickups_per_year': 52,
    'waste_type': 'Hushållsavfall',
    'waste_pickup_frequency': 'Tömning varje torsdag helår',
    'bin_code': 'K370',
    'bin_size': 370,
    'bin_unit': 'L',
    'bin_type': 'Kärl',
    'number_of_bins': 1,
    'calculated_cost': 0,
    'is_active': true,
    'description': 'Restavfall Kärl 400 l 1 ggr per vecka 0-15m kundägt verksamh',
    'id': 58492,
    'building_id': 20556
}
```