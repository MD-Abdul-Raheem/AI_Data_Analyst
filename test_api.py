from flask import Flask, request, jsonify
from app import DataAnalyst, load_data
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/test_analyze', methods=['POST'])
def test_analyze():
    try:
        file = request.files['file']
        df = load_data(file)
        
        analyst = DataAnalyst(df)
        understanding = analyst.understand_data()
        cleaning = analyst.clean_data()
        eda = analyst.perform_eda()
        insights, detailed = analyst.generate_insights()
        
        result = {
            'status': 'success',
            'shape': understanding['shape'],
            'columns': understanding['columns'],
            'insights_count': len(insights),
            'insights': insights,
            'cleaning': {
                'duplicates': cleaning['duplicates_removed'],
                'missing': len(cleaning['missing_values'])
            }
        }
        
        print("Returning result:", result)
        return jsonify(result)
    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting test API on http://localhost:5001")
    app.run(debug=True, port=5001)
