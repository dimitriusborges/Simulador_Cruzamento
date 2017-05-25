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
        self.matriz_tempos = [[10, 2, 28],  # NS
                              [15, 2, 23],  # OL
                              [10, 2, 28],  # SN
                              [15, 2, 23]]  # LO

        # Configuração de plano atuado
        self.matriz_atuado = [[4, 1, 8],  # NS
                              [4, 1, 8],  # OL
                              [4, 1, 8],  # SN
                              [4, 1, 8]]  # LO

        self.matriz_operante = list(
            self.matriz_tempos)  # Matriz auxiliar. A leitura dos tempos durante a animação é feita nela

        self.seq_estados = {"verde": "amarelo",  # Sequencia de cores que o foco deve assumir (verde->amarelo->vermelho)
                            "amarelo": "vermelho",
                            "vermelho": "verde"}

        self.estado_indice = {"verde": 0,  # Posicao que do tempo de cada cor na coluna da matriz
                              "amarelo": 1,
                              "vermelho": 2}

        self.cor_inicial = self.semaforos[0].estado  # Variaveis para determinar o fim de um ciclo
        self.flag_ciclo = False

        self.flag_atuado = False  # Variável de controle do sinal atuado

        threading.Thread.__init__(self)

    def run(self):
        """
        Executa as ações de animação para cada semáforo
        :return:
        """
        # Repetição secundária
        while True:

            self.contadores.clear()

            # Preenche a lista de timers com o tempo da cor inicial de cada foco
            for semaforo in self.semaforos:
                estado = semaforo.estado

                indice_tempo = self.estado_indice[estado]

                self.contadores.append((self.matriz_operante[self.semaforos.index(semaforo)])[indice_tempo] * 1)

            # Repetição principal
            while True:

                pointer = 0  # navegador auxiliar

                # Faz a contagem regressiva no timer de cada um dos semaforos
                for contador in self.contadores:

                    # Fim do timer = mudança de estado e novo tempo no contador
                    if contador == 0:

                        semaforo = self.semaforos[pointer]

                        prox_estado = self.seq_estados[semaforo.estado]
                        semaforo.mudar_estado(self.master, prox_estado)
                        indice_tempo = self.estado_indice[prox_estado]

                        self.contadores[self.contadores.index(contador)] = (self.matriz_operante[pointer])[indice_tempo] * 1

                        # Todos os semáforos são controlados por um mesmo plano, com mesmo ciclo.
                        # Portanto, basta observar apenas um para identificar o fim do ciclo
                        if semaforo == self.semaforos[0]:

                            # Se o estado seguinte for igual ao inicial, indica reinicio de ciclo
                            if self.cor_inicial == prox_estado:
                                self.flag_ciclo = True

                    else:
                        self.contadores[pointer] -= 1

                    pointer += 1

                time.sleep(1)

                # Se o controlador está entrando em um novo ciclo
                if self.flag_ciclo is True:

                    self.flag_ciclo = False
                    self.matriz_operante.clear()

                    # Se foi feito um pedido de plano atuado
                    if self.flag_atuado is True:

                        self.flag_atuado = False

                        # Recarrega a matriz com os tempos do plano atuado
                        self.matriz_operante = list(self.matriz_atuado)
                        break

                    # Se não foi feito pedido de plano atuado, mantem os tempos do plano principal
                    elif self.flag_atuado is False:

                        # Recarrega os tempos do plano principal
                        self.matriz_operante = list(self.matriz_tempos)
                        break