import os
from tkinter import Canvas
from tkinter import *

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'colecoes'))

class Veiculo:
    def __init__(self, x_i=0, y_i=0, x_f=0, y_f=0, cor='blue', sentido='ns'):
        """
        :param x_i: posicao inicial x
        :param y_i: posical inicial y
        :param x_f: posicao final x
        :param y_f: posical final y
        """
        self.veiculo = None  # Variavel que aponta para a imagem do veiculo no canvas
        self.velocidade = 0  # m/s
        self.torque = 0  # tempo de arrancada
        self.pos_atual = []  # posicao atual do veiculo
        self.pos_inicial = [x_i, y_i]  # posicao inicial do veiculo
        self.pos_final = [x_f, y_f]  # posical final do veiculo
        self.sentido = sentido
        self.cor = cor

        self.sentidos = ["ns", "sn", "ol", "lo"]

        self.sentido = sentido

        if self.sentido not in self.sentidos:
            raise ValueError("%s não é um sentido válido. Deveria ser %s ou %s ou %s ou %s"
                             % (self.sentido, self.sentidos[0], self.sentidos[1], self.sentidos[2], self.sentidos[3]))

        self.largura = 8  # 1.9 metros x 4 pixels
        self.comprimento = 16  # 4 metros x 4 pixels
        self.dist_pass = 4  # distancia do passeio/guia

    def adicionar_vertical(self, master: Canvas, x, y):
        """
        Insere uma representação gráfica do veículo em um canvas, no sentido vertical
        :param master: conteiner canvas que abrigara o veiculo
        :param x:   posicao inicial x
        :param y:   posicao inicial y
        :return:    veiculo inserido
        """
        self.pos_atual = [x, y]

        self.veiculo = master.create_rectangle(x + self.dist_pass, y,
                                               x + self.dist_pass + self.largura, y + self.comprimento,
                                               fill=self.cor)

    def adicionar_horizontal(self, master: Canvas, x, y):
        """
        Insere uma representação gráfica do veículo em um canvas, no sentido vertical
        :param master: conteiner canvas que abrigara o veiculo
        :param x:   posicao inicial x
        :param y:   posicao inicial y
        :return:    veiculo inserido
        """
        self.pos_atual = [x, y]

        self.veiculo = master.create_rectangle(x, y + self.dist_pass,
                                               x + self.comprimento, y + self.dist_pass + self.largura,
                                               fill=self.cor)

        return self.veiculo

    def remover(self, master):
        """

        :param master:
        :return:
        """
        master.delete(self.veiculo)
