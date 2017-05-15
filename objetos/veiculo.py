from tkinter import Canvas
class Veiculo:

    def __init__(self):

        self.velocidade = 0
        self.torque = 0
        self.largura = 8            # 1.9 metros x 4 pixels
        self.comprimento = 16       # 4 metros x 4 pixels
        self.dist_pass = 4   # distancia do passeio/guia

    def adicionar(self, master: Canvas, x, y):
        """
        Insere uma representação gráfica do veículo em um canvas
        :param master: conteiner canvas que abrigara o veiculo
        :param x:   posicao inicial x
        :param y:   posicao inicial y
        :return:    veiculo inserido
        """
        veiculo = master.create_rectangle(x + self.dist_pass, y,
                                          x + self.dist_pass + self.largura, y + self.comprimento,
                                          fill='blue')

        return veiculo
