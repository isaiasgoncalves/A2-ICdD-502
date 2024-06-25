import os
import platform


def prog_bar(valor_atual, valor_total, msg):

    limpar_tela()

    # Calcula a porcentagem
    percentual = (valor_atual / valor_total) * 100
    
    # Define o número de blocos da barra de progresso
    total_blocos = 50
    
    # Calcula o número de blocos preenchidos
    blocos_preenchidos = int((percentual / 100) * total_blocos)
    
    # Cria a barra de progresso
    barra = '[' + '#' * blocos_preenchidos + ' ' * (total_blocos - blocos_preenchidos) + ']'
    
    # Imprime a barra de progresso com a porcentagem
    print(f"\n\n{msg}\n{barra}", end='\r')


def limpar_tela():
    if os.getenv('TERM') is not None:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")