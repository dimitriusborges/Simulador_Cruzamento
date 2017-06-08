import threading

import time
from turtle import Canvas

from rua import Rua
from veiculo import Veiculo


class AnimVeiculos(threading.Thread):

    def __init__(self, master: Canvas, semaforo, veiculos, sentido):
        """
        Gerencia a movimentação e paradas de cada veículo, de acordo com o sentido da via
        :param master: Conteiner onde se encontram os objetos animados dos veiculos
        :param semaforo: Semaforo que faz o controle da via
        :param veiculos: Veiculos a serem animados
        :param sentido: Sentido que os veiculos estão percorrendo
        """
        self.master = master
        self.semaforo = semaforo
        self.veiculos = veiculos

        self.sentidos = ["ns", "sn", "ol", "lo"]

        self.sentido = sentido

        if self.sentido not in self.sentidos:
            raise ValueError("%s não é um sentido válido. Deveria ser %s ou %s ou %s ou %s"
                             % (self.sentido, self.sentidos[0], self.sentidos[1], self.sentidos[2], self.sentidos[3]))

        threading.Thread.__init__(self)

    def run(self):
        """
        Executa as ações de movimentação dos veículos
        :return:
        """
        prox_pos = []

        # Ccarrega variáveis de movimentação e semáforo da via

        while True:

            for veiculo in self.veiculos:
                # Converte de metros/segundo para metros/0.1 segundo
                vel_100ms = veiculo.velocidade / 10

                if veiculo.velocidade == 0:
                    prox_pos = (veiculo.pos_inicial[0],
                                veiculo.pos_inicial[1])

                else:

                    if self.sentido == 'ns':

                        prox_pos = (veiculo.pos_inicial[0],
                                    veiculo.pos_atual[1] + vel_100ms * 4)

                    elif self.sentido == 'sn':
                        prox_pos = (veiculo.pos_inicial[0],
                                    veiculo.pos_atual[1] - vel_100ms * 4)

                    elif self.sentido == 'ol':
                        prox_pos = (veiculo.pos_atual[0] + vel_100ms * 4,
                                    veiculo.pos_inicial[1])

                    elif self.sentido == 'lo':
                        prox_pos = (veiculo.pos_atual[0] - vel_100ms * 4,
                                    veiculo.pos_inicial[1])

                movimentar = self.verificar_checkpoints(prox_pos, self.semaforo, veiculo, self.veiculos)

                if movimentar is True:

                    # Remove para depois readiciona-lo em nova posição
                    veiculo.remover(self.master)

                    if self.sentido == 'ns' or self.sentido == 'sn':
                        veiculo.adicionar_vertical(self.master, prox_pos[0], prox_pos[1])

                    elif self.sentido == 'ol' or self.sentido == 'lo':
                        veiculo.adicionar_horizontal(self.master, prox_pos[0], prox_pos[1])

            time.sleep(0.1)

    def verificar_checkpoints(self, prox_pos, semaforo, veiculo, fila_veiculos):
        """
        Verifica se a posicao do veiculo coincide com algum dos pontos de interesse
        (semaforo, outro veiculo, ponto final)
        :param prox_pos: Prox posicao do veiculo
        :param semaforo: posicao do semaforo
        :param veiculo: veiculo
        :return:
        """

        if veiculo.sentido == 'ns' or veiculo.sentido == 'sn':
            atual = veiculo.pos_atual[1]
            limite_semaforo = prox_pos[1]

        if veiculo.sentido == 'ol' or veiculo.sentido == 'lo':
            atual = veiculo.pos_atual[0]
            limite_semaforo = prox_pos[0]

        # Verifica se o semáforo da via está aberto ou fechado

        # Sentido de + no plano usa >=
        if veiculo.sentido == 'ns' or veiculo.sentido == 'ol':

            if atual <= semaforo.posicao:

                if limite_semaforo >= semaforo.posicao:
                    if semaforo.foco is not "verde":
                        return False

        # Sentido de - no plano usa <=
        elif veiculo.sentido == 'sn' or veiculo.sentido == 'lo':

            if atual >= semaforo.posicao:

                if limite_semaforo - Veiculo().comprimento <= semaforo.posicao:
                    if semaforo.foco is not "verde":
                        return False

        # Verifica se a próxima posição não está ocupada por outro veículo
        if fila_veiculos.index(veiculo) - 1 > -1:

            veiculo_a_frente = fila_veiculos[fila_veiculos.index(veiculo) - 1]

            if veiculo.sentido == 'ns':

                if prox_pos[1] + Veiculo().comprimento + Rua().metro >= veiculo_a_frente.pos_atual[1]:
                    veiculo.velocidade = veiculo_a_frente.velocidade
                    return False

            if veiculo.sentido == 'sn':

                if prox_pos[1] - Veiculo().comprimento - Rua().metro <= \
                   veiculo_a_frente.pos_atual[1]:
                    veiculo.velocidade = veiculo_a_frente.velocidade
                    return False

            if veiculo.sentido == 'ol':
                if prox_pos[0] + Veiculo().comprimento + Rua().metro >= veiculo_a_frente.pos_atual[0]:
                    veiculo.velocidade = veiculo_a_frente.velocidade
                    return False

            if veiculo.sentido == 'lo':
                if prox_pos[0] - Veiculo().comprimento - Rua().metro <= veiculo_a_frente.pos_atual[0]:
                    veiculo.velocidade = veiculo_a_frente.velocidade
                    return False

        # verifica se o veículo chegou ao destino final
        # Soma é usada para que ambas as coordenadas sejam consideradas de forma conjunta

        # Sentido de + no plano usa >
        if veiculo.sentido == 'ns' or veiculo.sentido == 'ol':

            if prox_pos[0] + prox_pos[1] > veiculo.pos_final[0] + veiculo.pos_final[1]:
                #print("Final do percurso")

                veiculo.remover(self.master)
                fila_veiculos.remove(veiculo)
                return False

        # Sentido de - no plano usa <
        elif veiculo.sentido == 'sn' or veiculo.sentido == 'lo':

            if prox_pos[0] + prox_pos[1] < veiculo.pos_final[0] + veiculo.pos_final[1]:
                #print("Final do percurso")

                veiculo.remover(self.master)
                fila_veiculos.remove(veiculo)
                return False

        return True
