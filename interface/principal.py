import platform
import threading
import random
from tkinter import *

import time

from veiculo import Veiculo
from semaforo import Semaforo
from rua import Rua


class Principal:
    def __init__(self):

        self.i_r1 = 608, 0  # inicio da rua 1
        self.i_r2 = 208, 400  # inicio da rua 2

        self.veiculos_ns = []  # fila de veiculos na via Norte->Sul
        self.veiculos_sn = []  # fila de veiculos na via Sul->Norte
        self.veiculos_ol = []  # fila de veiculos na via Oeste->Leste
        self.veiculos_lo = []  # fila de veiculos na via Leste->Oeste

        self.velocidades = [5, 8, 11]   # 20km/h, 30km/h, 40km/h, em metros por segundo, valores aproximados

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
        #self.inserir_veiculos()

        self.thread_veiculos_ns = threading.Thread(target=self.animacao_carros_ns)
        self.thread_veiculos_ns.setDaemon(True)
        self.thread_veiculos_ns.start()

        self.thread_veiculos_sn = threading.Thread(target=self.animacao_carros_sn)
        self.thread_veiculos_sn.setDaemon(True)
        self.thread_veiculos_sn.start()

        # self.thread_veiculos_ol = threading.Thread(target=self.animacao_carros_ol)
        # self.thread_veiculos_ol.setDaemon(True)
        # self.thread_veiculos_ol.start()
        #
        # self.thread_veiculos_lo = threading.Thread(target=self.animacao_carros_lo)
        # self.thread_veiculos_lo.setDaemon(True)
        # self.thread_veiculos_lo.start()

        self.thread_seeder_veiculos = threading.Thread(target=self.seeder_veiculos)
        self.thread_seeder_veiculos.setDaemon(True)
        self.thread_seeder_veiculos.start()

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
                                 vermelho=True)

        self.sem_sn = Semaforo('sem_3', self.i_r2[1] + Rua().largura + 40)

        self.sem_sn.add_horizontal(self.canvas, self.i_r2[0] + Rua().comprimento + Rua().largura + 60,
                                   self.i_r2[1] + Rua().largura + 10,
                                   vermelho=True)

        self.sem_lo = Semaforo('sem_4', self.i_r1[0] + Rua().largura + 40)

        self.sem_lo.add_vertical(self.canvas, self.i_r1[0] + Rua().largura + 10,
                                 self.i_r1[1] + Rua().comprimento - Rua().largura - 15,
                                 vermelho=True)

    def inserir_veiculos(self):
        """

        :return:
        """
        # carro = Veiculo(self.i_r1[0], self.i_r1[1] + 200, self.i_r1[0], self.i_r1[1] + 400)
        # carro.velocidade = 0
        # carro.torque = 1
        # carro.sentido = 'ns'
        # carro.adicionar_vertical(self.canvas, self.i_r1[0], self.i_r1[1] + 200)
        # self.veiculos_ns.append(carro)
        #
        # carro = Veiculo(self.i_r1[0], self.i_r1[1], self.i_r1[0], self.i_r1[1] + 400)
        # carro.velocidade = 11
        # carro.torque = 1
        # carro.sentido = 'ns'
        # carro.adicionar_vertical(self.canvas, self.i_r1[0], self.i_r1[1])
        # self.veiculos_ns.append(carro)
        #
        # carro = Veiculo(self.i_r2[0], self.i_r2[1] + 48, self.i_r2[0] + 400, self.i_r2[1] + 48)
        # carro.velocidade = 5
        # carro.torque = 1
        # carro.sentido = 'ol'
        # carro.adicionar_horizontal(self.canvas, self.i_r2[0], self.i_r2[1] + 48)
        # self.veiculos_ol.append(carro)
        #
        # carro = Veiculo(self.i_r1[0] + 48, self.i_r1[1] + 400 + 64 + 400, self.i_r1[0] + 48, self.i_r1[1] + 400)
        # carro.velocidade = 8
        # carro.torque = 1
        # carro.sentido = 'sn'
        # carro.adicionar_vertical(self.canvas, self.i_r1[0] + 48, self.i_r1[1] + 400 + 64 + 400)
        # self.veiculos_sn.append(carro)

    def animacao_carros_ns(self):
        """
        Gerencia a movientação dos veículos na via Norte->Sul
        :return:
        """
        prox_pos = []

        # Ccarrega variáveis de movimentação e semáforo da via
        semaforo = self.sem_ns

        while True:

            for veiculo in self.veiculos_ns:
                # Converte de metros/segundo para metros/0.1 segundo
                vel_100ms = veiculo.velocidade/10

                if veiculo.velocidade == 0:
                    prox_pos = (veiculo.pos_inicial[0],
                                veiculo.pos_inicial[1] + 0)

                else:
                    prox_pos = (veiculo.pos_inicial[0],
                                veiculo.pos_atual[1] + veiculo.pos_inicial[1] + vel_100ms * 4)

                movimentar = self.verificar_checkpoints(prox_pos, semaforo, veiculo, self.veiculos_ns)

                if movimentar is True:
                    veiculo.remover(self.canvas)

                    veiculo.adicionar_vertical(self.canvas, prox_pos[0], prox_pos[1])

            time.sleep(0.1)

    def animacao_carros_sn(self):
        """
        Gerencia a movientação dos veículos na via Sul->Norte
        :return:
        """
        prox_pos = []

        while True:

            for veiculo in self.veiculos_sn:
                # Converte de metros/segundo para metros/0.1 segundo
                vel_100ms = veiculo.velocidade / 10

                # Carrega variáveis de movimentação e semáforo da via

                semaforo = self.sem_sn

                if veiculo.velocidade == 0:
                    prox_pos = (veiculo.pos_inicial[0],
                                veiculo.pos_inicial[1] + 0)

                else:
                    prox_pos = (veiculo.pos_inicial[0],
                                veiculo.pos_atual[1] - vel_100ms * 4)

                movimentar = self.verificar_checkpoints(prox_pos, semaforo, veiculo, self.veiculos_sn)

                if movimentar is True:
                    veiculo.remover(self.canvas)

                    veiculo.adicionar_vertical(self.canvas, prox_pos[0], prox_pos[1])

            time.sleep(0.1)

    def animacao_carros_ol(self):
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

                # Carrega variáveis de movimentação e semáforo da via
                semaforo = self.sem_ol

                if veiculo.velocidade == 0:

                    prox_pos = (veiculo.pos_inicial[0],
                                veiculo.pos_inicial[1] + 0)

                else:
                    prox_pos = (veiculo.pos_inicial[0] + vel_100ms * 4 * aux,
                                veiculo.pos_inicial[1])

                movimentar = self.verificar_checkpoints(prox_pos, semaforo, veiculo, self.veiculos_ol)

                if movimentar is True:
                    veiculo.remover(self.canvas)

                    veiculo.adicionar_horizontal(self.canvas, prox_pos[0], prox_pos[1])

                    aux += 1

            time.sleep(0.1)

    def animacao_carros_lo(self):
        """
        Gerencia a movientação dos veículos na via Leste->Oeste
        :return:
        """

        aux = 0
        prox_pos = []
        while True:

            for veiculo in self.veiculos_lo:

                # Converte de metros/segundo para metros/0.1 segundo
                vel_100ms = veiculo.velocidade / 10

                # Carrega variáveis de movimentação e semáforo da via
                semaforo = self.sem_lo

                if veiculo.velocidade == 0:

                    prox_pos = (veiculo.pos_inicial[0],
                                veiculo.pos_inicial[1] + 0)

                else:
                    prox_pos = (veiculo.pos_inicial[0] - vel_100ms * 4 * aux,
                                veiculo.pos_inicial[1])

                movimentar = self.verificar_checkpoints(prox_pos, semaforo, veiculo, self.veiculos_lo)

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

        if veiculo.sentido == 'ns' or veiculo.sentido == 'sn':
            limite_semaforo = prox_pos[1]

        if veiculo.sentido == 'ol' or veiculo.sentido == 'lo':
            limite_semaforo = prox_pos[0]

        # Verifica se o semáforo da via está aberto ou fechado

        # Sentido de + no plano usa >=
        if veiculo.sentido == 'ns' or veiculo.sentido == 'ol':

            if limite_semaforo >= semaforo.posicao:
                if semaforo.estado is False:
                    return False

        # Sentido de - no plano usa <=
        elif veiculo.sentido == 'sn' or veiculo.sentido == 'lo':

            if limite_semaforo - Veiculo().comprimento <= semaforo.posicao:
                if semaforo.estado is False:
                    return False

        # Verifica se a próxima posição não está ocupada por outro veículo
        if fila_veiculos.index(veiculo) - 1 > -1:

            veiculo_a_frente = fila_veiculos[fila_veiculos.index(veiculo) - 1]

            if veiculo.sentido == 'ns':

                if prox_pos[1] + Veiculo().comprimento + Rua().metro >= veiculo_a_frente.pos_atual[1]:
                    veiculo.velocidade = veiculo_a_frente.velocidade
                    #print("ocupado")
                    return False

            if veiculo.sentido == 'sn':

                if prox_pos[1] - Veiculo().comprimento - Rua().metro <= \
                   veiculo_a_frente.pos_atual[1]:

                    veiculo.velocidade = veiculo_a_frente.velocidade
                    #print("ocupado")
                    return False

        # verifica se o veículo chegou ao destino final
        # Soma é usada para que ambas as coordenadas sejam consideradas de forma conjunta

        # Sentido de + no plano usa >
        if veiculo.sentido == 'ns' or veiculo.sentido == 'ol':

            if prox_pos[0] + prox_pos[1] > veiculo.pos_final[0] + veiculo.pos_final[1]:
                #print("Final do percurso")

                veiculo.remover(self.canvas)
                fila_veiculos.remove(veiculo)
                return False

        # Sentido de - no plano usa <
        elif veiculo.sentido == 'sn' or veiculo.sentido == 'lo':

            if prox_pos[0] + prox_pos[1] < veiculo.pos_final[0] + veiculo.pos_final[1]:
                #print("Final do percurso")

                veiculo.remover(self.canvas)
                fila_veiculos.remove(veiculo)
                return False

        return True

    def seeder_veiculos(self):
        """

        :return:
        """

        seeder_ns = 0
        seeder_ol = 0

        while True:

            if seeder_ns == 0:

                seeder_ns = 1
                self.inserir_veiculo_vertical()

            else:
                seeder_ns -= 1

            if seeder_ol == 0:
                seeder_ol = 300
                # Gera veiculo

            else:
                seeder_ol -= 1

            time.sleep(0.5)

    def inserir_veiculo_vertical(self):
        """

        :return:
        """

        sentidos = ['ns', 'sn']

        sentido = random.randint(0, 1)
        velocidade = random.randint(0, 2)

        if sentidos[sentido] == 'ns':

            for veiculo in self.veiculos_ns:

                if veiculo.pos_atual[1] <= self.i_r1[1] + Veiculo().comprimento + Rua().metro:
                    return

            veiculo = Veiculo(self.i_r1[0], self.i_r1[1], self.i_r1[0], self.i_r1[1] + Rua().comprimento)
            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.sentido = sentidos[sentido]
            veiculo.adicionar_vertical(self.canvas, self.i_r1[0], self.i_r1[1])
            self.veiculos_ns.append(veiculo)

        elif sentidos[sentido] == 'sn':

            for veiculo in self.veiculos_sn:

                if veiculo.pos_atual[1] + Veiculo().comprimento + Rua().metro \
                        >= self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - Veiculo().comprimento:
                    return

            veiculo = Veiculo(self.i_r1[0] + Rua().largura - 16,
                              self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - Veiculo().comprimento,
                              self.i_r1[0] + Rua().largura - 16,
                              self.i_r1[1] + Rua().comprimento)

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.sentido = sentidos[sentido]
            veiculo.adicionar_vertical(self.canvas, self.i_r1[0] + Rua().largura - 16,
                                       self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - Veiculo().comprimento)
            self.veiculos_sn.append(veiculo)

    def iniciar_app(self):
        """

        :return:
        """
        self.root.minsize(640, 640)
        self.root.mainloop()


iniciar = Principal()
iniciar.iniciar_app()
