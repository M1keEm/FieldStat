from flask import Blueprint, request, jsonify, current_app
import requests

from backendFlask.config import Config

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/crops', methods=['POST', 'GET'])
def handle_crop_data():
    if request.method == 'POST':
        try:
            data = request.get_json()

            print(f"Requested Data: Year - {data['year']}, Commodity - {data['commodity']}")
            commodity = data['commodity'].upper()
            year = int(data['year'])

            current_app.config['LAST_CROP'] = commodity
            current_app.config['LAST_YEAR'] = year

            return jsonify({
                "message": f"Data saved for {data['commodity']} ({data['year']})",
                "status": "success"
            }), 200

        except Exception as e:
            return jsonify({
                "error": str(e),
                "status": "error"
            }), 400
    elif request.method == 'GET':
        commodity = request.args.get('commodity')
        year = request.args.get('year')
        return jsonify({
            "commodity": commodity,
            "year": year
        }), 200
    return None

@data_bp.route('/api/groups_commodities', methods=['GET'])
def get_groups_commodities():
    base_url = 'https://quickstats.nass.usda.gov/api/get_param_values/'
    api_url = 'https://quickstats.nass.usda.gov/api/api_GET/'
    api_key = Config.API_KEY

    try:
        # Fetch all commodity groups with non-null YIELD data
        valid_groups = set()
        valid_commodities = set()

        # First fetch all groups
        group_params = {
            'key': api_key,
            'param': 'group_desc'
        }
        group_resp = requests.get(base_url, params=group_params)
        all_groups = group_resp.json().get('group_desc', [])

        # Test each group for valid yield data (limited to 3 results per group to save time)
        for group in all_groups:
            check_params = {
                'key': api_key,
                'group_desc': group,
                'statisticcat_desc': 'YIELD',
                'year__GE': '2020',  # Last few years only to speed up queries
                'format': 'JSON',
                'limit': 3  # Just need to check if any data exists
            }

            try:
                check_resp = requests.get(api_url, params=check_params)
                data = check_resp.json().get('data', [])

                if data:
                    valid_groups.add(group)
                    # Add the commodities from this valid data
                    for item in data:
                        if item.get('commodity_desc'):
                            valid_commodities.add(item.get('commodity_desc'))
            except Exception as e:
                print(f"Error checking group {group}: {str(e)}")
                continue

        # Fetch additional commodities with yield data
        commodity_check_params = {
            'key': api_key,
            'statisticcat_desc': 'YIELD',
            'year__GE': '2020',
            'format': 'JSON',
            'limit': 500
        }

        try:
            commodity_resp = requests.get(api_url, params=commodity_check_params)
            data = commodity_resp.json().get('data', [])

            for item in data:
                if item.get('commodity_desc'):
                    valid_commodities.add(item.get('commodity_desc'))
                if item.get('group_desc'):
                    valid_groups.add(item.get('group_desc'))
        except Exception as e:
            print(f"Error checking commodities: {str(e)}")

        return jsonify({
            'groups': sorted(list(valid_groups)),
            'commodities': sorted(list(valid_commodities))
        })
    except Exception as e:
        print(f"Error fetching USDA data: {str(e)}")
        return jsonify({
            'error': f"Failed to fetch data: {str(e)}",
            'status': 'error'
        }), 500

@data_bp.route('/api/commodities_by_group', methods=['GET'])
def get_commodities_by_group():
    base_url = 'https://quickstats.nass.usda.gov/api/get_param_values/'
    api_url = 'https://quickstats.nass.usda.gov/api/api_GET/'
    api_key = Config.API_KEY
    group = request.args.get('group')

    try:
        # If no group specified, return empty list
        if not group:
            return jsonify({'commodities': []})

        # Fetch commodities filtered by group and that have yield data
        valid_commodities = set()

        # First get all commodities for this group
        param_params = {
            'key': api_key,
            'param': 'commodity_desc',
            'group_desc': group
        }
        response = requests.get(base_url, params=param_params)
        all_commodities = response.json().get('commodity_desc', [])

        # Then check which ones have yield data
        for commodity in all_commodities:
            check_params = {
                'key': api_key,
                'group_desc': group,
                'commodity_desc': commodity,
                'statisticcat_desc': 'YIELD',
                'year__GE': '2020',
                'format': 'JSON',
                'limit': 1
            }

            try:
                check_resp = requests.get(api_url, params=check_params)
                data = check_resp.json().get('data', [])

                if data:
                    valid_commodities.add(commodity)
            except Exception as e:
                print(f"Error checking commodity {commodity}: {str(e)}")
                continue

        return jsonify({
            'commodities': sorted(list(valid_commodities))
        })
    except Exception as e:
        print(f"Error fetching USDA data: {str(e)}")
        return jsonify({
            'error': f"Failed to fetch data: {str(e)}",
            'status': 'error'
        }), 500
