import platform
import threading
import random
from tkinter import *

import time

from anim_veiculo import AnimVeiculos
from veiculo import Veiculo
from semaforo import Semaforo
from anim_semaforo import AnimSemaforos
from rua import Rua


class Principal:
    def __init__(self):

        self.i_r1 = 608, 0      # inicio da rua 1
        self.i_r2 = 208, 400    # inicio da rua 2

        self.veiculos_ns = []  # fila de veiculos na via Norte->Sul
        self.veiculos_sn = []  # fila de veiculos na via Sul->Norte
        self.veiculos_ol = []  # fila de veiculos na via Oeste->Leste
        self.veiculos_lo = []  # fila de veiculos na via Leste->Oeste

        self.velocidades = [8, 8, 11]   # 20km/h, 30km/h, 40km/h, em metros por segundo, valores aproximados

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

        # self.thread_veiculos_ns = threading.Thread(target=self.animacao_carros_ns)
        # self.thread_veiculos_ns.setDaemon(True)
        # self.thread_veiculos_ns.start()
        #
        # self.thread_veiculos_sn = threading.Thread(target=self.animacao_carros_sn)
        # self.thread_veiculos_sn.setDaemon(True)
        # self.thread_veiculos_sn.start()
        #
        # self.thread_veiculos_ol = threading.Thread(target=self.animacao_carros_ol)
        # self.thread_veiculos_ol.setDaemon(True)
        # self.thread_veiculos_ol.start()
        #
        # self.thread_veiculos_lo = threading.Thread(target=self.animacao_carros_lo)
        # self.thread_veiculos_lo.setDaemon(True)
        # self.thread_veiculos_lo.start()
        #
        self.thread_seeder_veiculos = threading.Thread(target=self.seeder_veiculos)
        self.thread_seeder_veiculos.setDaemon(True)
        self.thread_seeder_veiculos.start()

        anim_veiculos_ns = AnimVeiculos(self.canvas, self.sem_ns, self.veiculos_ns, 'ns')
        anim_veiculos_ns.setDaemon(True)
        anim_veiculos_ns.start()

        anim_veiculos_sn = AnimVeiculos(self.canvas, self.sem_sn, self.veiculos_sn, 'sn')
        anim_veiculos_sn.setDaemon(True)
        anim_veiculos_sn.start()

        anim_veiculos_ol = AnimVeiculos(self.canvas, self.sem_ol, self.veiculos_ol, 'ol')
        anim_veiculos_ol.setDaemon(True)
        anim_veiculos_ol.start()

        anim_veiculos_lo = AnimVeiculos(self.canvas, self.sem_lo, self.veiculos_lo, 'lo')
        anim_veiculos_lo.setDaemon(True)
        anim_veiculos_lo.start()

        anim_semaforos = AnimSemaforos(self.canvas, [self.sem_ns, self.sem_ol, self.sem_sn, self.sem_lo])
        anim_semaforos.setDaemon(True)
        anim_semaforos.start()

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
                                   "vermelho")

        self.sem_ol = Semaforo('sem_2', self.i_r2[0] + Rua().comprimento - 40)

        self.sem_ol.add_vertical(self.canvas, self.i_r2[0] + Rua().comprimento - 40,
                                 self.i_r2[1] + Rua().largura + 15,
                                 "verde")

        self.sem_sn = Semaforo('sem_3', self.i_r2[1] + Rua().largura + 10)

        self.sem_sn.add_horizontal(self.canvas, self.i_r2[0] + Rua().comprimento + Rua().largura + 60,
                                   self.i_r2[1] + Rua().largura + 10,
                                   "vermelho", 1)

        self.sem_lo = Semaforo('sem_4', self.i_r1[0] + Rua().largura)

        self.sem_lo.add_vertical(self.canvas, self.i_r1[0] + Rua().largura + 10,
                                 self.i_r1[1] + Rua().comprimento - Rua().largura - 15,
                                 "verde", 1)

    def seeder_veiculos(self):
        """
        Gera veículos no sistema periodicamente.
        :return:
        """

        seeder_ns = 0   # Período para via Norte-Sul
        seeder_ol = 0   # Período para a via Oeste-Leste

        while True:

            if seeder_ns == 0:

                seeder_ns = 1
                self.inserir_veiculo_vertical()

            else:
                seeder_ns -= 1

            if seeder_ol == 0:
                seeder_ol = 1
                self.inserir_veiculo_horizontal()

            else:
                seeder_ol -= 1

            time.sleep(1)

    def inserir_veiculo_vertical(self):
        """
        Insere veículos na via Norte<->Sul
        :return:
        """

        sentidos = ['ns', 'sn']

        # O sentido (Norte->Sul ou Sul-> Norte) e a velocidade (20, 30 ou 40km/h) são aleatórios
        sentido = random.randint(0, 1)
        velocidade = random.randint(0, 2)

        if sentidos[sentido] == 'ns':

            # Verifica se não a via não está cheia, ou seja, se houver veículo na última posição da via,
            # cancela a inserção de um novo
            for veiculo in self.veiculos_ns:

                if veiculo.pos_atual[1] <= self.i_r1[1] + Veiculo().comprimento + Rua().metro:
                    return

            veiculo = Veiculo(self.i_r1[0],
                              self.i_r1[1],
                              self.i_r1[0],
                              self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento,
                              sentido=sentidos[sentido])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
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
                              self.i_r1[1],
                              sentido=sentidos[sentido])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.adicionar_vertical(self.canvas, self.i_r1[0] + Rua().largura - 16,
                                       self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento - Veiculo().comprimento)
            self.veiculos_sn.append(veiculo)

    def inserir_veiculo_horizontal(self):
        """
        Insere veículos na via Oeste<->Leste
        :return:
        """

        sentidos = ['ol', 'lo']

        # O sentido (Norte->Sul ou Sul-> Norte) e a velocidade (20, 30 ou 40km/h) são aleatórios
        sentido = random.randint(0, 1)
        velocidade = random.randint(0, 2)

        if sentidos[sentido] == 'ol':

            # Verifica se não a via não está cheia, ou seja, se houver veículo na última posição da via,
            # cancela a inserção de um novo
            for veiculo in self.veiculos_ol:

                if veiculo.pos_atual[0] <= self.i_r2[0] + Veiculo().comprimento + Rua().metro:
                    return

            veiculo = Veiculo(self.i_r2[0],
                              self.i_r2[1] + 48,
                              self.i_r2[0] + Rua().comprimento + Rua().largura + Rua().comprimento,
                              self.i_r2[1] + 48,
                              sentido=sentidos[sentido])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.adicionar_horizontal(self.canvas, self.i_r2[0], self.i_r2[1] + 48)
            self.veiculos_ol.append(veiculo)

        elif sentidos[sentido] == 'lo':

            for veiculo in self.veiculos_lo:

                if veiculo.pos_atual[0] + Veiculo().comprimento + Rua().metro \
                        >= self.i_r1[0] + Rua().comprimento + Rua().largura + Rua().comprimento + Veiculo().comprimento:
                    return

            veiculo = Veiculo(self.i_r2[0] + Rua().comprimento + Rua().largura + Rua().comprimento,
                              self.i_r2[1],
                              self.i_r2[0],
                              self.i_r2[1],
                              sentido=sentidos[sentido])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.adicionar_horizontal(self.canvas,
                                         self.i_r2[0] + Rua().comprimento + Rua().largura + Rua().comprimento,
                                         self.i_r2[1])
            self.veiculos_lo.append(veiculo)

    def iniciar_app(self):
        """
        Inicia a aplicação
        :return:
        """
        self.root.minsize(640, 640)
        self.root.mainloop()

iniciar = Principal()
iniciar.iniciar_app()
