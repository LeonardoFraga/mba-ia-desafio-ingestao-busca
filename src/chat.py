import os
from search import search_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from utils.enviroment_variables_validator import validate_variables

load_dotenv()
OPENAI_TEMPERATURE = 0.2

def main():
    """
    Inicia um chat interativo com o usuário, respondendo perguntas com base em documentos ingeridos.
    """

    validate_variables()

    print("Olá! Como posso ajudar você hoje?")

    while True:
        question = input("Digite sua pergunta (ou 'sair' para encerrar): ").strip()

        if question.lower() == 'sair':
            break

        if not question:
            print("Nenhuma pergunta foi digitada. Encerrando o chat.")
            return

        model = ChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL"), temperature=OPENAI_TEMPERATURE)

        chain = search_prompt(question) | model

        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return

        try:
            response = chain.invoke({"pergunta": question})
            print(response.content)
        except Exception as e:
            print(f"Erro ao processar a pergunta: {e}")

if __name__ == "__main__":
    main()