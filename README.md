![Maintenance](https://img.shields.io/maintenance/yes/2024?color=blue)
![GitHub release (with filter)](https://img.shields.io/github/v/release/kverqus/hassam?color=blue)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# SSAM Hämtschema
A simple integration to provide information about when SSAM (Södra Smålands Avfall och Miljö) is next emptying your waste bin(s).
## Installation
### HACS
1. Search for HASSAM or SSAM in HACS.
2. Choose install.
3. Restart Home Assistant.
4. Configure the `hassam` integration.
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
Once the integration has been configured and initialised it will create one new entity for each of your garbage bins. Available attributes include: 
* next_waste_pickup
* days_from_today
* waste_pickups_per_year
* waste_type
* waste_pickup_frequency
* bin_code
* bin_size
* bin_unit
* number_of_bins
* calculated_cost
* is_active
* description
* id
* building_id