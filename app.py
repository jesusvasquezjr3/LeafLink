from flask import Flask, request, jsonify, render_template
import pandas as pd
import openai
import os
from dotenv import load_dotenv
import re

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def load_catalog():
    try:
        df = pd.read_csv('leaflink_catalogo.csv')
        return df
    except Exception as e:
        print(f"Error al cargar el catalogo: {e}")
        return None

def filter_relevant_products(df, user_question):
    """Filtrar productos relevantes basado en la pregunta del usuario"""
    if df is None:
        return []
    
    # Convertir la pregunta a minúsculas para búsqueda
    question_lower = user_question.lower()
    
    # Palabras clave para plantas
    plant_keywords = [
        'planta', 'plantas', 'suculenta', 'suculentas', 'monstera', 'poto', 'palma', 
        'helecho', 'cactus', 'calathea', 'ficus', 'interior', 'exterior', 'jardín',
        'verde', 'hoja', 'hojas', 'maceta', 'cuidado', 'riego', 'luz', 'sombra',
        'resistente', 'purifica', 'aire', 'tropical', 'decorativa'
    ]
    
    # Palabras clave para aromaterapia
    aroma_keywords = [
        'aromaterapia', 'aceite', 'aceites', 'esencial', 'esenciales', 'vela', 'velas',
        'difusor', 'spray', 'roll-on', 'lavanda', 'eucalipto', 'limón', 'naranja',
        'relajante', 'energético', 'estrés', 'ansiedad', 'sueño', 'concentración',
        'aromático', 'fragancia', 'olor', 'huele'
    ]
    
    # Determinar si la pregunta es sobre plantas o aromaterapia
    is_about_plants = any(keyword in question_lower for keyword in plant_keywords)
    is_about_aroma = any(keyword in question_lower for keyword in aroma_keywords)
    
    # Si no hay palabras clave específicas, buscar en todos los productos
    if not is_about_plants and not is_about_aroma:
        # Buscar en todos los campos del catálogo
        relevant_products = []
        for _, row in df.iterrows():
            # Crear texto combinado de todos los campos relevantes
            combined_text = f"{row['nombre']} {row['atributo_1']} {row['descripcion']}".lower()
            if any(keyword in combined_text for keyword in question_lower.split()):
                relevant_products.append(row)
    else:
        # Filtrar por tipo de producto
        if is_about_plants and is_about_aroma:
            # Buscar en ambos tipos
            relevant_products = df[df['tipo'].isin(['planta', 'aromaterapia'])].to_dict('records')
        elif is_about_plants:
            relevant_products = df[df['tipo'] == 'planta'].to_dict('records')
        else:  # is_about_aroma
            relevant_products = df[df['tipo'] == 'aromaterapia'].to_dict('records')
    
    # Si no se encontraron productos específicos, devolver todos los productos
    if not relevant_products:
        relevant_products = df.to_dict('records')
    
    # Limitar a máximo 10 productos para no sobrecargar el contexto
    return relevant_products[:10]

def format_products_for_ai(products):
    """Formatea los productos para enviarlos a la IA."""
    if not products:
        return "No hay productos disponibles en el catalogo."

    formatted_text = "Catalogo de productos LeafLink:\n\n"

    for product in products:
        formatted_text += f"Tipo: {product['tipo']}\n"
        formatted_text += f"Nombre: {product['nombre']}\n"
        formatted_text += f"Nombre cientifico/atributo: {product['atributo_1']}\n"
        formatted_text += f"Descripcion: {product['descripcion']}\n"
        formatted_text += f"Precio: ${product['precio_mxn']} MXN\n"
        formatted_text += f"Stock disponible: {product['stock']}\n"
        if product['atributo_2']:
            formatted_text += f"Caracteristicas: {product['atributo_2']}\n"
        if product['atributo_3']:
            formatted_text += f"Uso recomendado: {product['atributo_3']}\n"
        formatted_text += "\n" + "=" * 50 + "\n\n"

    return formatted_text

def generate_ai_response(user_question, relevant_products):
    """Generar respuesta usando OpenAI con los productos relevantes"""
    try:
        # Formatear los productos para el contexto
        catalog_context = format_products_for_ai(relevant_products)
        
        # Crear el prompt para OpenAI
        prompt = f"""
Eres un asistente virtual especializado de LeafLink, una empresa que vende plantas de interior y productos de aromaterapia.

INFORMACION DEL CATALOGO:
{catalog_context}

INSTRUCCIONES IMPORTANTES:
1. Solo puedes responder preguntas relacionadas con los productos del catalogo mostrado arriba.
2. NO inventes precios, nombres de productos o caracteristicas que no esten en el catalogo.
3. Si la pregunta no se puede responder con la informacion del catalogo, responde: "Lo siento, solo puedo ayudarte con informacion sobre nuestros productos de plantas y aromaterapia. Hay algo especifico sobre nuestros productos que te gustaria saber?"
4. Se amable, util y profesional.
5. Si mencionas precios, usa exactamente los precios del catalogo (en MXN).
6. Responde en español.

PREGUNTA DEL CLIENTE: {user_question}

RESPUESTA:"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente virtual especializado en plantas y aromaterapia de LeafLink."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        error_message = str(e)
        print(f"Error al generar respuesta con OpenAI: {error_message}")
        if "quota" in error_message.lower():
            return ("Lo siento, estamos experimentando un problema temporal con nuestro proveedor "
                    "de IA. Por favor, intenta mas tarde.")
        return "Lo siento, hubo un error al procesar tu consulta. Por favor, intentalo de nuevo."

@app.route('/')
def index():
    """Servir la página principal"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para procesar mensajes del chatbot"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'response': 'Por favor, escribe un mensaje.'}), 400
        
        # Cargar el catálogo
        catalog_df = load_catalog()
        if catalog_df is None:
            return jsonify({'response': 'Lo siento, no puedo acceder al catálogo en este momento.'}), 500
        
        # Filtrar productos relevantes
        relevant_products = filter_relevant_products(catalog_df, user_message)
        
        # Generar respuesta con IA
        ai_response = generate_ai_response(user_message, relevant_products)
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        print(f"Error en endpoint /chat: {e}")
        return jsonify({'response': 'Lo siento, hubo un error al procesar tu mensaje.'}), 500

@app.route('/health')
def health():
    """Endpoint de salud para verificar que el servidor funciona"""
    return jsonify({'status': 'OK', 'message': 'LeafLink Bot está funcionando correctamente'})

if __name__ == '__main__':
    # Verificar que la API key está configurada
    if not os.getenv('OPENAI_API_KEY'):
        print("ADVERTENCIA: OPENAI_API_KEY no está configurada en el archivo .env")
        print("El chatbot no podrá generar respuestas hasta que se configure la clave.")
    
    # Verificar que el archivo CSV existe
    if not os.path.exists('leaflink_catalogo.csv'):
        print("ERROR: No se encontró el archivo leaflink_catalogo.csv")
        print("Asegúrate de que el archivo está en el mismo directorio que app.py")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
