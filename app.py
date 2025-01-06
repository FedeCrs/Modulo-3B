from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        # Obtener los datos enviados desde Streamlit
        data = request.get_json()

        # Verificar que los datos necesarios estén presentes
        required_fields = ['patient_name', 'age', 'gender', 'symptoms', 'test_results', 'diagnosis', 'recommendations']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f"Campo requerido faltante: {field}"}), 400

        # Extraer información
        patient_name = data['patient_name']
        age = data['age']
        gender = data['gender']
        symptoms = data['symptoms']
        test_results = data['test_results']
        diagnosis = data['diagnosis']
        recommendations = data['recommendations']

        # Crear el informe médico
        report = f"""
        **Informe Médico**
        ------------------------------
        **Nombre del Paciente:** {patient_name}
        **Edad:** {age}
        **Género:** {gender}

        **Síntomas Principales:**
        {symptoms}

        **Resultados de Pruebas:**
        {test_results if test_results else "No especificados"}

        **Diagnóstico Preliminar:**
        {diagnosis if diagnosis else "No especificado"}

        **Recomendaciones Iniciales:**
        {recommendations}
        ------------------------------
        """

        # Devolver el informe como respuesta JSON
        return jsonify({'detailed_report': report}), 200

    except Exception as e:
        return jsonify({'error': f'Error al procesar la solicitud: {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
