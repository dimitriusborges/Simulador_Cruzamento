from tkinter import Canvas
from cores import Cores


class Semaforo:

    def __init__(self, tag, pos):
        """

        :param tag: Tag de identificação do semáforo
        :param pos: posicão do semáforo no eixo X ou Y, para fins de localização
        """

        self.estados = ["verde", "amarelo", "vermelho"]     # 3 cores e estados que o sistema pode assumir
        self.tag = tag                                      # Nome único do semáforo
        self.foco = 'vermelho'                              # Foco ativo na representação gráfica
        self.estado = self.foco                             # estado real atual do sistema
        self.cor_inicial = 'vermelho'                       # Cor inicial do ciclo
        self.posicao = pos                                  # Posição no eixo X ou Y do semáforo

    def add_horizontal(self, master: Canvas, x, y, cor_inicial, ordem=0):
        """
        Adiciona um semáforo horizontal na posição indicada

        :param master: Conteiner
        :param x: Coordenada X
        :param y: Coordenada Y
        :param cor_inicial = cor atual do semaforo
        :return:
        """
        semaforos = []

        cor_vermelho = Cores().vermelho_off
        largura_vm = 1
        cor_amarelo = Cores().amarelo_off
        largura_am = 1
        cor_verde = Cores().verde_off
        largura_vd = 1

        self.cor_inicial = cor_inicial

        if cor_inicial is "vermelho":
            cor_vermelho = Cores().vermelho_on
            largura_vm = 2
            self.foco = "vermelho"
        if cor_inicial is "amarelo":
            cor_amarelo = Cores().amarelo_on
            largura_am = 2
            self.foco = "amarelo"
        if cor_inicial is "verde":
            cor_verde = Cores().verde_on
            largura_vd = 2
            self.foco = "verde"

        self.estado = self.foco

        if ordem == 0:
            semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_vermelho, tag=self.tag + '_vm',
                                                width=largura_vm))
            semaforos.append(master.create_oval(x - 25, y, x, y + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                                width=largura_am))
            semaforos.append(master.create_oval(x - 50, y, x + 25 - 50, y + 25, fill=cor_verde, tag=self.tag + '_vd',
                                                width=largura_vd))
        elif ordem == 1:
            semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_verde, tag=self.tag + '_vd',
                                                width=largura_vd))
            semaforos.append(master.create_oval(x - 25, y, x, y + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                                width=largura_am))
            semaforos.append(master.create_oval(x - 50, y, x + 25 - 50, y + 25, fill=cor_vermelho, tag=self.tag + '_vm',
                                                width=largura_vm))

        return semaforos

    def add_vertical(self, master: Canvas, x, y, cor_inicial, ordem=0):
        """
        Adiciona um semáforo vertical na posição indicada

        :param master: Conteiner
        :param x: Coordenada X
        :param y: Coordenada Y
        :param cor_inicial = cor atual do semaforo
        :return:
        """
        semaforos = []

        cor_vermelho = Cores().vermelho_off
        largura_vm = 1
        cor_amarelo = Cores().amarelo_off
        largura_am = 1
        cor_verde = Cores().verde_off
        largura_vd = 1

        self.cor_inicial = cor_inicial

        if cor_inicial is "vermelho":
            cor_vermelho = Cores().vermelho_on
            largura_vm = 2
            self.foco = "vermelho"
        if cor_inicial is "amarelo":
            cor_amarelo = Cores().amarelo_on
            largura_am = 2
            self.foco = "amarelo"
        if cor_inicial is "verde":
            cor_verde = Cores().verde_on
            largura_vd = 2
            self.foco = "verde"

        self.estado = self.foco

        if ordem == 0:
            semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_vermelho, tag=self.tag + '_vm',
                                                width=largura_vm))
            semaforos.append(master.create_oval(x, y + 25, x + 25, y + 25 + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                                width=largura_am))
            semaforos.append(master.create_oval(x, y + 50, x + 25, y + 25 + 50, fill=cor_verde, tag=self.tag + '_vd',
                                                width=largura_vd))
        elif ordem == 1:
            semaforos.append(master.create_oval(x, y, x + 25, y + 25, fill=cor_verde, tag=self.tag + '_vd',
                                                width=largura_vd))
            semaforos.append(master.create_oval(x, y + 25, x + 25, y + 25 + 25, fill=cor_amarelo, tag=self.tag + '_am',
                                                width=largura_am))
            semaforos.append(master.create_oval(x, y + 50, x + 25, y + 25 + 50, fill=cor_vermelho, tag=self.tag + '_vm',
                                                width=largura_vm))

        return semaforos

    def mudar_foco(self, master, foco):
        """
        Altera o foco ativo do semáforo

        :param master: Conteiner
        :param foco = cor que o semáforo irá assumir
        :return:
        """

        cor_vermelho = Cores().vermelho_off
        largura_vm = 1
        cor_amarelo = Cores().amarelo_off
        largura_am = 1
        cor_verde = Cores().verde_off
        largura_vd = 1

        if foco == "vermelho":
            cor_vermelho = Cores().vermelho_on
            largura_vm = 2
            self.foco = 'vermelho'
        if foco == "amarelo":
            cor_amarelo = Cores().amarelo_on
            largura_am = 2
            self.foco = 'amarelo'
        if foco == "verde":
            cor_verde = Cores().verde_on
            largura_vd = 2
            self.foco = 'verde'

        master.itemconfig(self.tag + '_vm', fill=cor_vermelho, width=largura_vm)
        master.itemconfig(self.tag + '_am', fill=cor_amarelo, width=largura_am)
        master.itemconfig(self.tag + '_vd', fill=cor_verde, width=largura_vd)
