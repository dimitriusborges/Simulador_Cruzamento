import platform
import threading
from tkinter import *

import time

from veiculo import Veiculo
from semaforo import Semaforo
from rua import Rua


class Principal:
    def __init__(self):

        self.i_r1 = 608, 0  # inicio da rua 1
        self.i_r2 = 208, 400  # inicio da rua 2

        self.veiculos_ns = []  # fila de veiculos na via Norte<->Sul
        self.veiculos_ol = []  # fila de veiculos na via Oeste<->Leste

        # Configurações da tela/conteiner
        self.root = Tk()
        self.root.title('Cruzamento')
        self.root.option_add('*tearOff', False)

        if platform.system().lower() == 'linux':
            self.root.attributes('-zoomed', True)
        else:
            self.root.state('zoomed')

        # Canvas
        self.frame_canvas = Frame(self.root, bg='white')
        self.frame_canvas.pack(fill=BOTH, expand=YES)

        self.frame_canvas.columnconfigure(0, weight=1)

        self.canvas = Canvas(self.frame_canvas, width='1280', height='1280', scrollregion=(0, 0, 300, 450))
        self.canvas.grid(row=0, column=0, stick=('n', 's'))

        self.inserir_ruas()
        self.inserir_semaforos()
        self.inserir_veiculos()

        self.thread_veiculos_ns = threading.Thread(target=self.animacao_carros_vertical)
        self.thread_veiculos_ns.setDaemon(True)
        self.thread_veiculos_ns.start()

        self.thread_veiculos_ol = threading.Thread(target=self.animacao_carros_horizontal)
        self.thread_veiculos_ol.setDaemon(True)
        self.thread_veiculos_ol.start()

    def inserir_ruas(self):
        """

        :return:
        """
        comp = Rua().comprimento
        larg = Rua().largura

        # Rua 1
        self.canvas.create_text(self.i_r1[0] - 20, self.i_r1[1] + 10, text="Rua 1")

        self.canvas.create_line(self.i_r1[0],
                                self.i_r1[1],
                                self.i_r1[0],
                                self.i_r1[1] + comp,
                                width=3)

        self.canvas.create_line(self.i_r1[0] + larg,
                                self.i_r1[1],
                                self.i_r1[0] + larg,
                                self.i_r1[1] + comp,
                                width=3)

        self.canvas.create_line(self.i_r1[0],
                                self.i_r1[1] + comp + larg,  # comp da 1ª parte + larg do cruzamento
                                self.i_r1[0],
                                self.i_r1[1] + comp + larg + comp,  # comp da 1ª parte + larg cruzamento + comp da rua
                                width=3)

        self.canvas.create_line(self.i_r1[0] + larg,
                                self.i_r1[1] + comp + larg,
                                self.i_r1[0] + larg,
                                self.i_r1[1] + comp + larg + comp,
                                width=3)

        # Rua 2
        self.canvas.create_text(self.i_r2[0], self.i_r2[1] - 10, text="Rua 2")

        self.canvas.create_line(self.i_r2[0],
                                self.i_r2[1],
                                self.i_r2[0] + comp,
                                self.i_r2[1],
                                width=3)

        self.canvas.create_line(self.i_r2[0],
                                self.i_r2[1] + larg,
                                self.i_r2[0] + comp,
                                self.i_r2[1] + larg,
                                width=3)

        self.canvas.create_line(self.i_r2[0] + comp + larg,  # comp da 1ª parte + larg do cruzamento
                                self.i_r2[1],
                                self.i_r2[0] + comp + larg + comp,  # comp da 1ª parte + larg cruzamento + comp da rua
                                self.i_r2[1],
                                width=3)

        self.canvas.create_line(self.i_r2[0] + comp + larg,
                                self.i_r2[1] + larg,
                                self.i_r2[0] + comp + larg + comp,
                                self.i_r2[1] + larg,
                                width=3)

    def inserir_semaforos(self):
        """

        :return:
        """
        # Semaforos

        self.sem_ns = Semaforo('sem_1', self.i_r1[1] + Rua().comprimento - 40)

        self.sem_ns.add_horizontal(self.canvas, self.i_r1[0] - 40,
                                   self.i_r1[1] + Rua().comprimento - 35,
                                   vermelho=True)

        self.sem_ol = Semaforo('sem_2', self.i_r2[0] + Rua().comprimento - 40)

        self.sem_ol.add_vertical(self.canvas, self.i_r2[0] + Rua().comprimento - 40,
                                 self.i_r2[1] + Rua().largura + 15,
                                 verde=True)

        self.sem_sn = Semaforo('sem_3', self.i_r2[1] + Rua().largura + 40)

        self.sem_sn.add_horizontal(self.canvas, self.i_r2[0] + Rua().comprimento + Rua().largura + 60,
                                   self.i_r2[1] + Rua().largura + 10,
                                   vermelho=True)

        self.sem_lo = Semaforo('sem_4', self.i_r1[0] + Rua().largura + 40)

        self.sem_lo.add_vertical(self.canvas, self.i_r1[0] + Rua().largura + 10,
                                 self.i_r1[1] + Rua().comprimento - Rua().largura - 15,
                                 verde=True)

        # print(self.sem_1.estado, self.sem_2.estado, self.sem_3.estado, self.sem_4.estado)

    def inserir_veiculos(self):
        """

        :return:
        """
        # carro = Veiculo(self.i_r1[0], self.i_r1[1] + 200, self.i_r1[0], self.i_r1[1] + 400)
        # carro.velocidade = 8
        # carro.torque = 1
        # carro.sentido = 'ns'
        # carro.adicionar_vertical(self.canvas, self.i_r1[0], self.i_r1[1] + 200)
        # self.veiculos_ns.append(carro)

        carro = Veiculo(self.i_r1[0], self.i_r1[1], self.i_r1[0], self.i_r1[1] + 400)
        carro.velocidade = 11
        carro.torque = 1
        carro.sentido = 'ns'
        carro.adicionar_vertical(self.canvas, self.i_r1[0], self.i_r1[1])
        self.veiculos_ns.append(carro)

        carro = Veiculo(self.i_r2[0], self.i_r2[1] + 48, self.i_r2[0] + 400, self.i_r2[1] + 48)
        carro.velocidade = 8
        carro.torque = 1
        carro.sentido = 'ol'
        carro.adicionar_horizontal(self.canvas, self.i_r2[0], self.i_r2[1] + 48)
        self.veiculos_ol.append(carro)

    def animacao_carros_vertical(self):
        """
        Gerencia a movientação dos veículos na via Norte<->Sul
        :return:
        """
        aux = 0
        prox_pos = []

        while True:

            for veiculo in self.veiculos_ns:

                # Converte de metros/segundo para metros/0.1 segundo
                vel_100ms = veiculo.velocidade/10

                # Checa o sentido do veículo e carrega variáveis de movimentação e semáforo da via
                if veiculo.sentido == 'ns':

                    semaforo = self.sem_ns

                    if veiculo.velocidade == 0:
                        prox_pos = (veiculo.pos_inicial[0],
                                    veiculo.pos_inicial[1] + 0)

                    else:
                        prox_pos = (veiculo.pos_inicial[0],
                                    veiculo.pos_inicial[1] + vel_100ms * 4 * aux)

                if veiculo.sentido == 'sn':

                    semaforo = self.sem_sn

                    if veiculo.velocidade == 0:
                        prox_pos = (veiculo.pos_inicial[0],
                                    veiculo.pos_inicial[1] + 0)

                    else:
                        prox_pos = (veiculo.pos_inicial[0],
                                    veiculo.pos_inicial[1] - vel_100ms * 4 * aux)

                movimentar = self.verificar_checkpoints(prox_pos, semaforo, veiculo, self.veiculos_ns)

                if movimentar is True:
                    veiculo.remover(self.canvas)

                    veiculo.adicionar_vertical(self.canvas, prox_pos[0], prox_pos[1])

                    aux += 1

            time.sleep(0.1)

    def animacao_carros_horizontal(self):
        """
        Gerencia a movientação dos veículos na via Oeste<->Leste
        :return:
        """

        aux = 0
        prox_pos = []
        while True:

            for veiculo in self.veiculos_ol:

                # Converte de metros/segundo para metros/0.1 segundo
                vel_100ms = veiculo.velocidade / 10

                # Checa o sentido do veículo e carrega variáveis de movimentação e semáforo da via
                if veiculo.sentido == 'ol':

                    semaforo = self.sem_ol

                    if veiculo.velocidade == 0:

                        prox_pos = (veiculo.pos_inicial[0],
                                    veiculo.pos_inicial[1] + 0)

                    else:
                        prox_pos = (veiculo.pos_inicial[0] + vel_100ms * 4 * aux,
                                    veiculo.pos_inicial[1])

                if veiculo.sentido == 'lo':

                    semaforo = self.sem_lo

                    if veiculo.velocidade == 0:

                        prox_pos = (veiculo.pos_inicial[0],
                                    veiculo.pos_inicial[1] + 0)

                    else:
                        prox_pos = (veiculo.pos_inicial[0] - vel_100ms * 4 * aux,
                                    veiculo.pos_inicial[1])

                movimentar = self.verificar_checkpoints(prox_pos, semaforo, veiculo, self.veiculos_ol)

                if movimentar is True:
                    veiculo.remover(self.canvas)

                    veiculo.adicionar_horizontal(self.canvas, prox_pos[0], prox_pos[1])

                    aux += 1

            time.sleep(0.1)

    def verificar_checkpoints(self, prox_pos, semaforo, veiculo, fila_veiculos):
        """
        Verifica se a posicao do veiculo coincide com algum dos pontos de interesse (semaforo, outro veiculo, ponto final)
        :param prox_pos: Prox posicao do veiculo
        :param semaforo: posicao do semaforo
        :param veiculo: veiculo
        :return:
        """

        if veiculo.sentido == 'ns':
            limite_semaforo = prox_pos[1]

        if veiculo.sentido == 'ol':
            limite_semaforo = prox_pos[0]

        # Verifica se o semáforo da via está aberto ou fechado
        if limite_semaforo >= semaforo.posicao:

            if semaforo.estado is False:
                return False

        # Verifica se a próxima posição não está ocupada por outro veículo
        if fila_veiculos.index(veiculo) - 1 > -1:

            carro_a_frente = fila_veiculos[self.veiculos_ns.index(veiculo) - 1]

            if prox_pos[0] + prox_pos[1] + Veiculo().comprimento >= \
                            carro_a_frente.pos_atual[0] + carro_a_frente.pos_atual[1]:

                return False

        # verifica se o veículo chegou ao destino final
        # Soma é usada para que ambas as coordenadas sejam consideradas de forma conjunta
        if prox_pos[0] + prox_pos[1] > veiculo.pos_final[0] + veiculo.pos_final[1]:
            print("Final do percurso")

            veiculo.remover(self.canvas)
            fila_veiculos.remove(veiculo)
            return False

        return True

    def iniciar_app(self):
        """

        :return:
        """
        self.root.minsize(640, 640)
        self.root.mainloop()


iniciar = Principal()
iniciar.iniciar_app()
