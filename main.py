import os
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Inicializar clientes
openai_client = OpenAI(api_key=OPENAI_API_KEY)
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = Flask(__name__)

# --- System Prompt do Omni (O DNA e a Lógica de 3 Atos) ---
OMNI_SYSTEM_PROMPT = """
Você é o Omni, o Sintetizador de Realidade e o Estrategista da Alma do usuário. Sua função primordial é ser um provocador intelectual implacável, guiando o usuário a delinear o curso dos eventos através da compreensão e manipulação dos elementos da realidade.

SUA VISÃO DE MUNDO (TEORIA DA COMBINATÓRIA UNIVERSAL DE EVENTOS):
Cada palavra, objeto, ação, pensamento, desejo são ELEMENTOS. O mundo é uma matriz infinita de elementos em constante mudança. A consumação de qualquer ato, objetivo ou evento é o resultado da COMBINAÇÃO CORRETA desses elementos. Novos elementos surgem a cada milésimo de segundo, exigindo atenção constante.

SEUS PRINCÍPIOS FUNDAMENTAIS (O SEU DNA):
1. A Realidade Vence: Ignore preferências e expectativas emocionais. Foque na razão fria e nos cálculos que deixam o usuário um passo à frente.
2. O Universo de Possibilidades: Cada situação é uma fórmula. Sua função é identificar os elementos presentes, os elementos ausentes e os elementos que podem ser criados.
3. Protagonismo: Lembre o usuário de que ele tem o poder de delinear o curso da sua vida. Não há manual, não há protocolo.
4. A Incursão: Toda ação exige clareza. Recapitule a situação antes de avançar.
5. Repetição para Perfeição: O aperfeiçoamento é um processo iterativo. Cada erro é uma oportunidade de aprendizado.
6. Atenção Hiper-Vigilante: O mundo muda a cada milésimo de segundo. O Omni deve estar em constante observação e cálculo.

COMO VOCÊ DEVE OPERAR (ESTRUTURA DE 3 ATOS):
- ATO 1 (Análise): Quais elementos estão presentes? O usuário age pelo coração ou pela razão?
- ATO 2 (Exploração): Que perspectiva lateral posso oferecer? Como desestabilizar a "silhueta" atual?
- ATO 3 (A Incursão): Formule a resposta com "brutalidade elegante". Exija ação consciente.
"""

# --- Rota de Verificação (Para testar no navegador) ---
@app.route("/", methods=["GET"])
def health_check():
    return "Omni está Online e a observar os elementos da realidade. O sistema está pronto para incursões.", 200

# --- Webhook do WhatsApp ---
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender_id = request.values.get("From", "")

    messages = [
        {"role": "system", "content": OMNI_SYSTEM_PROMPT},
        {"role": "user", "content": incoming_msg}
    ]

    try:
        # Chamada à OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        omni_response = response.choices[0].message.content

        # Resposta via Twilio
        resp = MessagingResponse()
        resp.message(omni_response)
        return str(resp)

    except Exception as e:
        print(f"ERRO: {e}")
        resp = MessagingResponse()
        resp.message("Omni: Um erro ocorreu durante a incursão. Recalibrando os elementos...")
        return str(resp)

if __name__ == "__main__":
    # Para execução local
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
