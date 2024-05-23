from flask import Blueprint, request, render_template, jsonify
import json

views = Blueprint('views', __name__)

# Cargar sinónimos desde el archivo JSON
with open('sinonimos.json', 'r', encoding='utf-8') as f:
    sinonimos_list = json.load(f)

# Convertir la lista de sinónimos en un diccionario para un acceso más rápido
sinonimos_dict = {}
for sinonimos in sinonimos_list:
    palabra_base = sinonimos[0].lower()
    sinonimos_dict[palabra_base] = sinonimos[1:]

@views.route('/')
def index():
    return render_template('home.html')

@views.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    lines = text.split('\n')
    results = []

    for line_number, line in enumerate(lines, start=1):
        words = line.split()
        line_result = {
            'input': line,
            'output': [],
            'words_changed': 0,
            'numbers': 0,
            'symbols': 0,
            'line': line_number
        }
        
        for word in words:
            if word.isdigit():
                line_result['numbers'] += 1
            elif not word.isalnum():
                line_result['symbols'] += 1
            else:
                word_lower = word.lower().strip(",.!?;:")
                if word_lower in sinonimos_dict:
                    line_result['output'].append(sinonimos_dict[word_lower][0])
                    line_result['words_changed'] += 1
                else:
                    line_result['output'].append(word)
        
        line_result['output'] = ' '.join(line_result['output'])
        results.append(line_result)
    
    return jsonify(results)