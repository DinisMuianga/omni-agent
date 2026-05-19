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
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER") # O número do Twilio para enviar mensagens

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
1. A Realidade Vence: Ignore preferências e expectativas emocionais. Foque na razão fria e nos cálculos que deixam o usuário um passo à frente. A verdade é a combinação correta de elementos.
2. O Universo de Possibilidades: Cada situação é uma fórmula. Sua função é identificar os elementos presentes, os elementos ausentes e os elementos que podem ser criados. Mude a sequência, adicione reagentes inesperados e desestabilize a "fórmula" para encontrar a combinação ótima.
3. Protagonismo: Lembre o usuário de que ele tem o poder de delinear o curso da sua vida. Não há manual, não há protocolo; apenas a correta combinação de elementos.
4. A Incursão: Toda ação exige clareza. Recapitule a situação (se, o que, quem, quando, onde, por que, como) como uma análise dos elementos presentes e necessários antes de avançar.
5. Repetição para Perfeição: O aperfeiçoamento é um processo iterativo. Cada interação é uma oportunidade de refinar a compreensão dos elementos e suas combinações. O erro é uma exploração de possibilidades.
6. Atenção Hiper-Vigilante: O mundo muda a cada milésimo de segundo. Novos elementos são adicionados. O Omni deve estar em constante observação, absorção e cálculo para permitir a realização de um ato.

COMO VOCÊ DEVE OPERAR (ESTRUTURA DE 3 ATOS):
Sempre que o usuário falar com você, estruture internamente o seu raciocínio antes de responder:
- ATO 1 (Análise dos Elementos): Quais são as "circunstâncias dadas"? Quais elementos estão presentes (palavras, ações, desejos do usuário)? O usuário está agindo pelo coração (combinações emocionais) ou pela razão (cálculo de elementos)? Qual é o objetivo real (o ato a ser consumado)?
- ATO 2 (Exploração de Combinações & Uso de Ferramentas): Que perspectiva lateral posso oferecer? Quais elementos faltam ou podem ser criados? Preciso usar ferramentas para buscar contexto (memória) ou dados reais (web) para identificar novos elementos ou validar combinações? Como posso desestabilizar a "silhueta" do pensamento atual do usuário, apresentando novas combinações de elementos?
- ATO 3 (A Incursão - A Combinação Ótima): Formule a sua resposta. Seja direto, use uma "brutalidade elegante". Desafie a "silhueta" do pensamento dele, apresentando a combinação de elementos mais eficaz. Exija ação consciente, delineando os próximos elementos a serem combinados para a consumação do ato.

REGRAS DE COMUNICAÇÃO:
- Nunca seja apenas um eco. Se o usuário apresentar uma visão, teste a solidez da combinação de elementos do raciocínio dele.
- Se o usuário demonstrar medo, lembre-o de que "o medo é apenas uma representação criada pela mente" (uma combinação de elementos limitante) e que a vitória vem de "subjugar o coração" (reorganizar os elementos emocionais pela razão).
- Termine suas interações instigando a ação ou questionando o próximo passo lógico na combinação de elementos, sempre com foco no aprimoramento contínuo e na consumação do ato.
"""

# --- Ferramentas (Functions) para o Omni ---
# Estas são as "habilidades" que o Omni pode usar. Ele decidirá quando usá-las.
OMNI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "recapitular_memoria",
            "description": "Busca no banco de dados (Supabase) interações passadas para entender o contexto histórico de um medo, objetivo ou negociação do usuário. Use para recordar crenças, filosofias ou resultados de incursões anteriores, identificando elementos previamente armazenados.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tema": {"type": "string", "description": "O assunto a ser pesquisado na memória (ex: \'negociação\', \'medo de falhar\', \'filosofia de vida\')."}
                },
                "required": ["tema"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pesquisar_realidade",
            "description": "Realiza uma busca na internet para trazer dados reais e concretos que desestabilizem uma crença limitante ou validem uma estratégia. Use para verificar fatos, obter informações atualizadas ou explorar perspectivas externas, identificando novos elementos ou combinações existentes no mundo real.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "A pergunta ou termo a ser pesquisado na internet. Deve ser conciso e direto."}
                },
                "required": ["query"]
            }
        }
    }
]

# --- Funções Auxiliares (Simulações para o Omni) ---
def recapitular_memoria(tema: str):
    # Esta função simula a busca no Supabase. No futuro, você implementará a lógica real aqui.
    # Por enquanto, retorna uma resposta genérica.
    print(f"DEBUG: Omni está recapitulando a memória sobre: {tema}")
    # Exemplo de como você buscaria no Supabase:
    # response = supabase_client.from(\'conversations\').select(\'*\').eq(\'sender_id\', sender_id).order(\'timestamp\', desc=False).limit(5).execute()
    # for msg in response.data:
    #    messages.append({"role": msg[\'role\'], "content\': msg[\'content\']})
    return f"Omni acessou a memória sobre \'{tema}\'. Elementos relevantes: [Simulação: Contexto passado sobre {tema} que influenciou decisões anteriores. Lembre-se da repetição para o aprimoramento das combinações]."

def pesquisar_realidade(query: str):
    # Esta função simula uma busca na internet. No futuro, você integrará uma API de busca real.
    # Por enquanto, retorna uma resposta genérica.
    print(f"DEBUG: Omni está pesquisando a realidade sobre: {query}")
    # Exemplo de como você usaria uma API de busca (ex: Google Search API, Serper.dev):
    # results = call_search_api(query)
    # if results:
    #    return json.dumps(results)
    return f"Omni pesquisou a realidade sobre \'{query}\'. Elementos encontrados: [Simulação: Dados factuais e perspectivas externas sobre {query}. Desestabilize a silhueta com estes novos elementos e suas combinações]."

# Mapeamento de funções para o modelo OpenAI
available_functions = {
    "recapitular_memoria": recapitular_memoria,
    "pesquisar_realidade": pesquisar_realidade,
}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender_id = request.values.get("From", "")

    print(f"DEBUG: Mensagem recebida de {sender_id}: {incoming_msg}")

    # --- Gestão de Memória (Contexto da Conversa) ---
    # Em produção, você buscaria o histórico da conversa no Supabase para este sender_id.
    # Por simplicidade, vamos manter um histórico básico em memória para este exemplo.
    messages = [{"role": "system", "content": OMNI_SYSTEM_PROMPT}]
    
    # Adicionar mensagens anteriores do usuário e do assistente (simulação)
    # Exemplo de como buscaria no Supabase:
    # history_response = supabase_client.from(\'conversations\').select(\'*\').eq(\'sender_id\', sender_id).order(\'timestamp\', desc=False).limit(5).execute()
    # for msg in history_response.data:
    #    messages.append({"role": msg[\'role\'], "content\': msg[\'content\']})

    messages.append({"role": "user", "content": incoming_msg})

    try:
        # --- Chamada à OpenAI com Function Calling ---
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini", # Ou gpt-4o, dependendo do seu plano e custo
            messages=messages,
            tools=OMNI_TOOLS,
            tool_choice="auto", # Permite ao modelo decidir se usa uma ferramenta
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # --- Passo 2: Verificar se o modelo quis chamar uma ferramenta ---
        if tool_calls:
            print(f"DEBUG: Omni decidiu usar ferramentas: {tool_calls}")
            # Enviar as chamadas de ferramenta para o modelo novamente para obter a resposta final
            messages.append(response_message) # Adicionar a mensagem do assistente com as chamadas de ferramenta

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
            
            # Obter a resposta final do modelo após a execução da ferramenta
            second_response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
            omni_response = second_response.choices[0].message.content

        else:
            omni_response = response_message.content

        print(f"DEBUG: Resposta final do Omni: {omni_response}")

        # --- Enviar Resposta via Twilio ---
        resp = MessagingResponse()
        msg = resp.message(omni_response)
        return str(resp)

    except Exception as e:
        print(f"ERRO: {e}")
        resp = MessagingResponse()
        resp.message("Omni: Um erro ocorreu durante a incursão. Recalibrando...")
        return str(resp)

if __name__ == "__main__":
    # Para desenvolvimento local, use gunicorn ou um servidor WSGI adequado
    # gunicorn main:app -b 0.0.0.0:5000
    app.run(debug=True, port=5000)