from search import answer_question
import sys

def main():
    """
    Main function for the CLI chat interface.
    """
    print("=== Sistema de Busca Semântica ===")
    print("Digite 'sair' para encerrar o chat.")
    print()
    
    while True:
        # Get user input
        try:
            user_input = input("Você: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando o chat. Até logo!")
                break
                
            # Skip empty input
            if not user_input:
                continue
                
            # Process the question
            print("Processando sua pergunta...")
            answer = answer_question(user_input)
            
            # Display the answer
            print("\nResposta:")
            print("-" * 50)
            print(answer)
            print("-" * 50)
            print()
            
        except KeyboardInterrupt:
            print("\n\nEncerrando o chat. Até logo!")
            sys.exit(0)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            print("Por favor, tente novamente.")
            print()

if __name__ == "__main__":
    main()
