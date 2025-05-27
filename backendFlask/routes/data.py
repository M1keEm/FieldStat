from flask import Blueprint, request, jsonify, current_app

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/crops', methods=['POST', 'GET'])
def handle_crop_data():
    if request.method == 'POST':
        try:
            data = request.get_json()

            print(f"Requested Data: Year - {data['year']}, Crop - {data['crop']}")
            crop = data['crop'].upper()
            year = int(data['year'])
            
            current_app.config['LAST_CROP'] = crop
            current_app.config['LAST_YEAR'] = year


            return jsonify({
                "message": f"Data saved for {data['crop']} ({data['year']})",
                "status": "success"
            }), 200

        except Exception as e:
            return jsonify({
                "error": str(e),
                "status": "error"
            }), 400
    elif request.method == 'GET':
        crop = request.args.get('crop')
        year = request.args.get('year')
        return jsonify({
            "crop": crop,
            "year": year
        }), 200
    return None
