# -*- encoding: utf-8 -*-
"""
    Servidor del juego de snake 

    Todo el código lo haré en inglés pero los comentarios
    serán en español
"""

import sys

from PyQt4 import QtGui, QtCore, uic


class Snake():
    """
        Serán las serpientes que utilizaran los usuarios.
    """
    # red, green, blue son utilizados para definir el color de la serpiente
    # de forma
    def __init__(self, red, green, blue):
        """
            Constructor de la clase Snake
            
            red, green, blue son utilizados para definir el color de la serpiente
            de forma que sea como código rgba
        """
        # Los guardamos en una tupla y así representamos el color
        self.color = (red, green, blue)
        # Representaremos la serpiente como una lista de listas de 2 elementos
        self.body = [[1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0], [8,0],
            [9, 0]
        ]
        # Esto lo hacemos para evitar estar calculando siempre el tamaño del
        # cuerpo de la serpiente
        self.body_len = len(self.body)
        # De esta manero sabremos hacia donde está mirando la serpiente
        # 0: Arriba
        # 1: Derecha
        # 2: Abajo
        # 3: Izquierda
        self.direction = 2


class ServerWindow(QtGui.QMainWindow):
    """
        Ventana principal del servidor.
    """

    def __init__(self):
        """
            Constructor de la clase.
        """
        super(ServerWindow, self).__init__()
        uic.loadUi('servidor.ui', self)

        # Vamos a poner unos atributos a la clase
        # Variables para saber el estado del juego
        self.game_started = self.game_paused = False
        # Para que la ventana tenga contadores
        self.timer = None
        # Lista con todas las serpientes del juego
        self.snakes = []
        self.snakes_len = len(self.snakes)
 
        # Que no resalten las celdas al dar click
        self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
        # Método para expandir las celdas de la tabla de forma que estén bien
        # acomodadas
        self.expand_table_cells()
        # Pondremos items en toda la tabla para poder pintarla como queramos
        self.fill_table()

        # Conectamos que se cambie las columnas y filas de la tabla al método
        # update_table
        # Columnas
        self.spinBox_2.valueChanged.connect(self.update_table)
        # Filas
        self.spinBox_3.valueChanged.connect(self.update_table)

        # Conectamos que se cambie la velocidad de las serpientes al método
        # update_timer
        self.spinBox.valueChanged.connect(self.update_timer)

        # Conectamos el boton de iniciar juego al método de start_game
        self.pushButton_2.clicked.connect(self.change_game_state)
        # Enconderemos el boton de terminar juego ya que este sólo
        # aparece cuando se inicia el juego
        self.pushButton_3.hide()
        # Conectamos el boton de terminar juego al método de game_over
        self.pushButton_3.clicked.connect(self.game_over)
        
        # Mostramos la ventana
        self.show()

    def fill_table(self):
        """
            Se encarga de llenar la tabla con items en cada celda
        """
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i, j, QtGui.QTableWidgetItem())
                self.tableWidget.item(i,j).setBackground(
                    QtGui.QColor(255,255,255)
                )

    def expand_table_cells(self):
        """
            Se encarga de poner en el tamaño correcto las celdas    
        """
        self.tableWidget.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch
        )
        self.tableWidget.verticalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch
        )

    def update_table(self):
        """
            Actualiza la tabla si se incremente el numero de filas o de
            columnas
        """
        # Obtenemos los valores de los spinBox y actualizamos el número
        # de columnas y filas
        rows = self.spinBox_3.value()
        columns = self.spinBox_2.value()
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(columns)
        self.fill_table()

    def update_timer(self):
        """
            Este método se encarga de cambiar la velocidad de la serpiente
            si es que la cambia el jugador en el spinBox
        """
        value = self.spinBox.value()
        self.timer.setInterval(value)
    
    def change_game_state(self):
        """
            Inicializa o pausa el juego
        """
        if not self.game_started:
            # Mostramos el boton de terminar el juego
            self.pushButton_3.show()
            # Ponemos el boton de iniciar juego a pausar juego
            self.pushButton_2.setText('Pausar el Juego')

            # Creamos la primer serpiente y la agregamos nuestra lista de
            # serpientes en el juego
            snake = Snake(0, 0, 0)
            self.snakes.append(snake)
            self.snakes_len += 1
            # La pintamos en la tabla
            self.draw_snakes()
            # Le asignamos la velocidad
            self.timer = QtCore.QTimer(self)
            # Para cada timer se le conecta con el metodo move_snakes
            self.timer.timeout.connect(self.move_snakes)
            self.timer.start(200)
            # Le ponemos un EventFilter para escuchar a la
            # tabla
            self.tableWidget.installEventFilter(self)
            # Si no hay ningun error, ponemos que el juego ha sido
            # empezado
            self.game_started = True

        # Esto es para cuando el juego ha empezado y no está pausado
        elif self.game_started and not self.game_paused:
            # Paramos el timer
            self.timer.stop()
            self.game_paused = True
            self.pushButton_2.setText("Continuar juego")
        
        # Al final cuando el juego esta pausado
        elif self.game_started and self.game_paused:
            # Continuamos el timer
            self.timer.start()
            self.game_paused = False
            self.pushButton_2.setText("Pausar Juego")

    def game_over(self):
        """
            Termina el juego
        """
        # Paramos el timer
        self.timer.stop()
        # Borramos todas la serpientes
        self.snakes = []
        self.game_started = False
        self.game_paused = False
        # Volvemos a esconder el boton de terminar juego
        self.pushButton_3.hide()
        self.pushButton_2.setText('Iniciar Juego')
        # Volvemos a llenar la tabla
        self.fill_table()

    def draw_snakes(self):
        """
            Dibuja todas las serpientes en la tabla
        """
        for snake in self.snakes:
            for body_part in snake.body:
                self.tableWidget.item(body_part[0], body_part[1]).\
                    setBackground(QtGui.QColor(
                        snake.color[0], snake.color[1], snake.color[2]
                ))

    def move_snakes(self):
        """
            Hace el movimiento de las serpientes
        """
        for snake in self.snakes:
            if self.check_snake_has_crash(snake):
                # Quitamos la serpiente si es que ha chocado
                self.snakes.remove(snake)
                self.snakes_len -= 1
                if self.snakes_len == 0:
                    self.game_over()
                    return
                # Debemos de rellenar la tabla
                self.fill_table()

            # Poner de blanco el item donde estaba la cola de la serpiente
            self.tableWidget.item(
                snake.body[0][0],snake.body[0][1]
            ).setBackground(QtGui.QColor(255,255,255))

            aux = 1
            # Cada parte del cuerpo debe de moverse a donde está la
            # siguiente
            for body_part in snake.body[0:-1]:
                body_part[0] = snake.body[aux][0]
                body_part[1] = snake.body[aux][1]
                aux += 1

            # Vemos la dirección hacía donde se dirige la serpiente y
            # verificamos si la cabeza llega al borde de la tabla
            if snake.direction == 0:
                if snake.body[-1][0] != 0:
                    snake.body[-1][0] -= 1
                else:
                    snake.body[-1][0] = self.tableWidget.rowCount()-1
            elif snake.direction == 1:
                if snake.body[-1][1] < self.tableWidget.columnCount()-1:
                    snake.body[-1][1] += 1
                else:
                    snake.body[-1][1] = 0
            elif snake.direction == 2:
                if snake.body[-1][0] < self.tableWidget.rowCount()-1:
                    snake.body[-1][0] += 1
                else:
                    snake.body[-1][0] = 0
            elif snake.direction == 3:
                if snake.body[-1][1] != 0:
                    snake.body[-1][1] -= 1
                else:
                    snake.body[-1][1] = self.tableWidget.columnCount()-1
        # Al final de todo se vuelven a dibujar las serpientes
        self.draw_snakes()

    def check_snake_has_crash(self, snake):
        """
            Checa que la serpiente no haya chocado.
        """
        for current_snake in self.snakes:
            # Checamos 2 casos, si la serpiente actual es la serpiente
            # que estamos iterando ahora y si no. Esto es para que
            # una serpiente no choque con su misma cabeza ya que esto es
            # imposible
            if snake != current_snake:
                # Verificamos si chocaron ambas cabezas
                if snake.body[-1][0] == current_snake.body[-1][0] and (
                    snake.body[-1][1] == current_snake.body[-1][1]):
                    return True
            # Aquí ya verificamos todo el cuerpo excepto la cabeza
            for body_part in current_snake.body[0:-1]:
                if snake.body[-1][0] == body_part[0] and (
                    snake.body[-1][1] == body_part[1]):
                    return True
            return False

    def eventFilter(self, source, event):
        """
            Este método lo utilizaremos para los eventos cuando oprimamos
            las teclas y que la serpiente se mueva
        """
        if (event.type() == QtCore.QEvent.KeyPress) and (
            source is self.tableWidget):

            #Obtenemos que tecla es la que fue presionada
            key = event.key()
            # Checamos los casos cuando la tecla presionada es una de las
            # flechas
            if (key == QtCore.Qt.Key_Up and
                source is self.tableWidget):
                for snake in self.snakes:
                    if snake.direction != 2:
                        snake.direction = 0
            elif (key == QtCore.Qt.Key_Down and
                source is self.tableWidget):
                for snake in self.snakes:
                    if snake.direction != 0:
                        snake.direction = 2
            elif (key == QtCore.Qt.Key_Right and
                source is self.tableWidget):
                for snake in self.snakes:
                    if snake.direction != 3:
                        snake.direction = 1
            elif (key == QtCore.Qt.Key_Left and
                source is self.tableWidget):
                for snake in self.snakes:
                    if snake.direction != 1:
                        snake.direction = 3
        return QtGui.QMainWindow.eventFilter(self, source, event)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv) 
    window = ServerWindow()
    sys.exit(app.exec_())
