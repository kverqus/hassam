import httpx
import json
import logging

from datetime import datetime, date

from .const import DOMAIN

_LOGGER = logging.getLogger(f'custom_components.{DOMAIN}.core')


class SSAMAPI(object):
    def __init__(self):
        self.__search_url = 'https://edpfuture.ssam.se/FutureWeb/SimpleWastePickup/SearchAdress'
        self.__schedule_url = 'https://edpfuture.ssam.se/FutureWeb/SimpleWastePickup/GetWastePickupSchedule?address='
        self.__headers = {
            'Content-Type': 'application/json'
        }

    async def search_address(self, search_string: str) -> dict:
        buildings_list = {'buildings': []}
        address = {'searchText': search_string}

        try:
            async with httpx.AsyncClient() as client:
                request = await client.post(
                    self.__search_url,
                    data=address
                )

        except Exception as err:
            _LOGGER.critical(err)
            raise err

        if request.status_code == 200:
            data = json.loads(request.text)

            if not data['Succeeded']:
                return buildings_list

            for building in data['Buildings']:
                buildings_list['buildings'].append(building)

        return json.dumps(buildings_list)

    async def get_schedule(self, building_address: str) -> list:
        schedule_list = []

        try:
            async with httpx.AsyncClient() as client:
                request = await client.get(
                    f'{self.__schedule_url}{building_address}',
                    headers=self.__headers
                )
        
        except Exception as err:
            _LOGGER.critical(err)
            raise err

        if request.status_code == 200:
            data = json.loads(request.text)
            today = date.today()

            if 'RhServices' not in data:
                return schedule_list

            for schedule in data['RhServices']:
                days_from_today = False
                try:
                    pickup = datetime.strptime(schedule['NextWastePickup'], '%Y-%m-%d').date()
                    days_from_today = (pickup - today).days
                except ValueError:
                    pass

                schedule_list.append(
                    {
                        'next_waste_pickup': schedule['NextWastePickup'],
                        'days_from_today': days_from_today,
                        'waste_pickups_per_year': schedule['WastePickupsPerYear'], 
                        'waste_type': schedule['WasteType'],
                        'waste_pickup_frequency': schedule['WastePickupFrequency'], 
                        'bin_code': schedule['BinType']['Code'], 
                        'bin_size': int(schedule['BinType']['Size']),
                        'bin_unit': schedule['BinType']['Unit'].upper() if schedule['BinType']['Unit'] is not None else '', 
                        'bin_type': schedule['BinType']['ContainerType'], 
                        'number_of_bins': int(schedule['NumberOfBins']),
                        'calculated_cost': schedule['Fee']['CalculatedCost'],
                        'is_active': schedule['IsActive'], 
                        'description': schedule['Description'], 
                        'id': schedule['ID'], 
                        'building_id': int(schedule['BuildingID'])
                    }
                )

        return sorted(schedule_list, key=lambda d: d['next_waste_pickup'])
