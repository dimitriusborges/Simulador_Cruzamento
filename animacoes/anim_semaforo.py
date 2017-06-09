import threading
from tkinter import Canvas

import time


class AnimSemaforos(threading.Thread):

    def __init__(self, master: Canvas, lista_semaforos: list):
        """
        Gerenciao os estados de cada foco, de acordo com os tempos configurados

        :param master: Conteiner onde se encontram os objetos animados dos semaforos
        :param lista_semaforos: lista de todos os semaforos adicionados ao sistema
        """
        self.master = master
        self.semaforos = lista_semaforos

        self.contadores = []  # Timer de cada foco

        # Tempos de cada foco (verde, amarelo, vermelho). Configuração de plano padrão
        self.matriz_principal = [[0, 0, 40],  # NS
                                 [40, 0, 0],  # OL
                                 [0, 0, 40],  # SN 10 2 28
                                 [40, 0, 0]]  # LO

        # Configuração de plano atuado
        self.matriz_atuado = [[20, 2, 8],  # NS
                              [2, 2, 26],  # OL
                              [20, 2, 8],  # SN
                              [2, 2, 26]]  # LO

        self.matriz_cor_inicial = []
        self.matriz_cor_inicial_atuado = []

        for semaforo in self.semaforos:
            self.matriz_cor_inicial.append(semaforo.cor_inicial)
            self.matriz_cor_inicial_atuado.append(semaforo.cor_inicial)

        # Matrizes auxiliares. A leitura dos tempos e cores durante a animação são feitas nelas
        self.matriz_cor_inicial_operante = list(self.matriz_cor_inicial)
        self.matriz_operante = list(self.matriz_principal)

        self.seq_cores = {"verde": "amarelo",  # Sequencia de cores que o foco deve assumir (verde->amarelo->vermelho)
                          "amarelo": "vermelho",
                          "vermelho": "verde"}

        self.indice_cor = {"verde": 0,  # Posicao que do tempo de cada cor na coluna da matriz
                           "amarelo": 1,
                           "vermelho": 2}

        # Variaveis para determinar o fim de um ciclo
        self.cor_inicial = self.semaforos[0].estado
        self.flag_ciclo = False

        self.flag_atuado = False  # Variável de controle do sinal atuado

        threading.Thread.__init__(self)

    def run(self):
        """
        Executa as ações de animação para cada semáforo
        :return:
        """

        # Repetição inicial - preenche as variavéis
        while True:

            self.contadores.clear()

            # Preenche a lista de timers com o tempo da cor inicial de cada foco
            # Altera o estado e o foco de cada semaforo para o da cor inicial
            for semaforo in self.semaforos:

                semaforo.estado = self.matriz_cor_inicial_operante[self.semaforos.index(semaforo)]
                semaforo.mudar_foco(self.master, semaforo.estado)

                indice_tempo = self.indice_cor[semaforo.estado]

                self.contadores.append((self.matriz_operante[self.semaforos.index(semaforo)])[indice_tempo] * 10)

            # Repetição principal - executado até o fim do ciclo do semáforo
            while True:
                pointer = 0  # Variavel navegadora auxiliar, que relaciona a posicao do contador com a posicao
                # do controlador

                #  Faz a contagem regressiva no timer da cor atual de cada um dos semaforos.
                for contador in self.contadores:

                    # Fim do timer = mudança de estado e novo tempo no contador
                    if contador == 0:

                        semaforo = self.semaforos[pointer]

                        prox_estado = self.seq_cores[semaforo.estado]
                        indice_tempo = self.indice_cor[prox_estado]
                        self.contadores[pointer] = (self.matriz_operante[pointer])[indice_tempo] * 10

                        # Se uma cor não tiver sido ignorada (tempo = 0) e não for fim de ciclo
                        #  altera a representação gráfica do semáforo. Caso contrário, ignora
                        if self.contadores[pointer] > 0 and self.flag_ciclo is False:
                            semaforo.mudar_foco(self.master, prox_estado)

                        semaforo.estado = prox_estado

                        # Todos os semáforos são controlados por um mesmo plano, com mesmo ciclo.
                        # Portanto, basta observar apenas um para identificar o fim do ciclo
                        if semaforo == self.semaforos[0]:
                            # Se o estado seguinte for igual ao inicial, indica reinicio de ciclo
                            if self.cor_inicial == prox_estado:
                                self.flag_ciclo = True

                    else:
                        self.contadores[pointer] -= 1

                    pointer += 1

                time.sleep(0.1)

                # Se o controlador está entrando em um novo ciclo
                if self.flag_ciclo is True:

                    self.flag_ciclo = False
                    self.matriz_operante.clear()
                    self.matriz_cor_inicial_operante.clear()

                    # Se foi feito um pedido de plano atuado
                    if self.flag_atuado is True:

                        self.flag_atuado = False

                        # Recarrega a matriz com os tempos do plano atuado
                        self.matriz_operante = list(self.matriz_atuado)
                        self.matriz_cor_inicial_operante = list(self.matriz_cor_inicial_atuado)
                        break

                    # Se não foi feito pedido de plano atuado, mantem os tempos do plano principal
                    elif self.flag_atuado is False:

                        # Recarrega os tempos do plano principal
                        self.matriz_operante = list(self.matriz_principal)
                        self.matriz_cor_inicial_operante = list(self.matriz_cor_inicial)
                        break
