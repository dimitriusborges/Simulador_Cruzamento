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

        self.thread_veiculos_ns = threading.Thread(target=self.animacao_carros_ns)
        self.thread_veiculos_ns.setDaemon(True)
        self.thread_veiculos_ns.start()

        self.thread_veiculos_sn = threading.Thread(target=self.animacao_carros_sn)
        self.thread_veiculos_sn.setDaemon(True)
        self.thread_veiculos_sn.start()

        self.thread_veiculos_ol = threading.Thread(target=self.animacao_carros_ol)
        self.thread_veiculos_ol.setDaemon(True)
        self.thread_veiculos_ol.start()

        self.thread_veiculos_lo = threading.Thread(target=self.animacao_carros_lo)
        self.thread_veiculos_lo.setDaemon(True)
        self.thread_veiculos_lo.start()

        self.thread_seeder_veiculos = threading.Thread(target=self.seeder_veiculos)
        self.thread_seeder_veiculos.setDaemon(True)
        self.thread_seeder_veiculos.start()

        self.thread_semaforos = threading.Thread(target=self.animacao_semaforos)
        self.thread_semaforos.setDaemon(True)
        self.thread_semaforos.start()

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

    def animacao_semaforos(self):
        """
        Gerenciao os estados de cada foco, de acordo com os tempos configurados
        :return:
        """
        semaforos = self.sem_ns, self.sem_ol, self.sem_sn, self.sem_lo

        contadores = []                             # Timer de cada foco

        # Tempos de cada foco (verde, amarelo, vermelho). Configuração de plano padrão
        matriz_tempos = [[10, 2, 28],               # NS
                         [15, 2, 23],               # OL
                         [10, 2, 28],               # SN
                         [15, 2, 23]]               # LO

        # Configuração de plano atuado
        matriz_atuado = [[4, 1, 8],                 # NS
                         [4, 1, 8],                 # OL
                         [4, 1, 8],                 # SN
                         [4, 1, 8]]                 # LO

        matriz_operante = list(matriz_tempos)       # Matriz auxiliar. A leitura dos tempos durante a animação é feita nela

        seq_estados = {"verde": "amarelo",          # Sequencia de cores que o foco deve assumir (verde->amarelo->vermelho)
                       "amarelo": "vermelho",
                       "vermelho": "verde"}

        estado_indice = {"verde": 0,                # Posicao que do tempo de cada cor na coluna da matriz
                         "amarelo": 1,
                         "vermelho": 2}

        cor_inicial = self.sem_ns.estado            # Variaveis para determinar o fim de um ciclo
        flag_ciclo = False

        flag_atuado = False                         # Variável de controle do sinal atuado


        # Repetição secundária
        while True:

            contadores.clear()

            # Preenche a lista de timers com o tempo da cor inicial de cada foco
            for semaforo in semaforos:

                estado = semaforo.estado

                indice_tempo = estado_indice[estado]

                contadores.append((matriz_operante[semaforos.index(semaforo)])[indice_tempo] * 1)

            # Repetição principal
            while True:

                pointer = 0     # navegador auxiliar

                # Faz a contagem regressiva no timer de cada um dos semaforos
                for contador in contadores:

                    # Fim do timer = mudança de estado e novo tempo no contador
                    if contador == 0:

                        semaforo = semaforos[pointer]

                        prox_estado = seq_estados[semaforo.estado]
                        semaforo.mudar_estado(self.canvas, prox_estado)
                        indice_tempo = estado_indice[prox_estado]

                        contadores[contadores.index(contador)] = (matriz_operante[pointer])[indice_tempo] * 1

                        # Todos os semáforos são controlados por um mesmo plano, com mesmo ciclo.
                        # Portanto, basta observar apenas um para identificar o fim do ciclo
                        if semaforo == self.sem_ns:

                            # Se o estado seguinte for igual ao inicial, indica reinicio de ciclo
                            if cor_inicial == prox_estado:
                                flag_ciclo = True

                    else:
                        contadores[pointer] -= 1

                    pointer += 1

                time.sleep(1)

                # Se o controlador está entrando em um novo ciclo
                if flag_ciclo is True:

                    flag_ciclo = False

                    # Se foi feito um pedido de plano atuado
                    if flag_atuado is True:

                        flag_atuado = False

                        # Recarrega a matriz com os tempos do plano atuado
                        matriz_operante.clear()
                        matriz_operante = list(matriz_atuado)
                        break

                    # Se não foi feito pedido de plano atuado, mantem os tempos do plano principal
                    elif flag_atuado is False:

                        # Recarrega os tempos do plano principal
                        matriz_operante.clear()
                        matriz_operante = list(matriz_tempos)
                        break

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
                              self.i_r1[1] + Rua().comprimento + Rua().largura + Rua().comprimento)
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
                              self.i_r1[1])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.sentido = sentidos[sentido]
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
                              self.i_r2[1] + 48)

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.sentido = sentidos[sentido]
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
                              self.i_r2[1])

            veiculo.velocidade = self.velocidades[velocidade]
            veiculo.torque = 1
            veiculo.sentido = sentidos[sentido]
            veiculo.adicionar_horizontal(self.canvas,
                                         self.i_r2[0] + Rua().comprimento + Rua().largura + Rua().comprimento,
                                         self.i_r2[1])
            self.veiculos_lo.append(veiculo)

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
                                veiculo.pos_atual[1] + vel_100ms * 4)

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
                    prox_pos = (veiculo.pos_atual[0] + vel_100ms * 4,
                                veiculo.pos_inicial[1])

                movimentar = self.verificar_checkpoints(prox_pos, semaforo, veiculo, self.veiculos_ol)

                if movimentar is True:
                    veiculo.remover(self.canvas)

                    veiculo.adicionar_horizontal(self.canvas, prox_pos[0], prox_pos[1])

            time.sleep(0.1)

    def animacao_carros_lo(self):
        """
        Gerencia a movientação dos veículos na via Leste->Oeste
        :return:
        """

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
                    prox_pos = (veiculo.pos_atual[0] - vel_100ms * 4,
                                veiculo.pos_inicial[1])

                movimentar = self.verificar_checkpoints(prox_pos, semaforo, veiculo, self.veiculos_lo)

                if movimentar is True:
                    veiculo.remover(self.canvas)

                    veiculo.adicionar_horizontal(self.canvas, prox_pos[0], prox_pos[1])

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

                    if semaforo.estado is not "verde":
                        return False

        # Sentido de - no plano usa <=
        elif veiculo.sentido == 'sn' or veiculo.sentido == 'lo':

            if atual >= semaforo.posicao:

                if limite_semaforo - Veiculo().comprimento <= semaforo.posicao:
                    if semaforo.estado is not "verde":
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

            if veiculo.sentido == 'ol':
                if prox_pos[0] + Veiculo().comprimento + Rua().metro >= veiculo_a_frente.pos_atual[0]:
                    veiculo.velocidade = veiculo_a_frente.velocidade
                    #print("ocupado")
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

    def iniciar_app(self):
        """
        Inicia a aplicação
        :return:
        """
        self.root.minsize(640, 640)
        self.root.mainloop()

iniciar = Principal()
iniciar.iniciar_app()
