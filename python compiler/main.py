from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    code = request.json.get('code')
    try:
        result = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT, timeout=5, universal_newlines=True)
        return jsonify({'output': result})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out.'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
