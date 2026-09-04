from machine import Pin, PWM

# - Ponte H conectada ao ESP32 sem os pinos especiais para o PWM.

class Hbridge:
    

# - Denomina os pinos quando chama a classe sendo, em ordem: n1; n2; n3; n4.
#
# Exemplo: Hbridge(12, 14, 27, 26)

    def __init__(self, n1, n2, n3, n4):
        self.n1 = PWM(Pin(n1), freq=5000, duty=0)
        self.n2 = PWM(Pin(n2), freq=5000, duty=0)
        self.n3 = PWM(Pin(n3), freq=5000, duty=0)
        self.n4 = PWM(Pin(n4), freq=5000, duty=0)
        self.min_speed = 0
        

    
# - Função para o motor ligar, girar em sentindo horário ou anti-horário, e alterar sua velocidade;
#
# - Para chama-lá, precisa fornecer os valores de Nome do Motor em string (Direito ['right'] ou ['r'],
#  Esquerdo: ['left'] ou ['l'], ou Todos: ['all'] ou ['a']) * , qual o Sentido de Giro em string (Horário ['cw'] ou
#  Antihorário ['ccw']) * , e qual a Porcentagem da Velocidade de Rotação em inteiros (0 a 100);
#
#   * não há problemas no aparecimento de letras MAIÚSCULAS nas strings.
#
# Exemplo:
#               Hbridge.Run("Right", "CCW", 70)

    def Run(self, motor, direction, speed_percent):

        if motor.lower() in ("left", "l"):

            self.percent_to_pwm(speed_percent)

            if direction.lower() == "ccw":
                self.n2.duty(self.speed)
                self.n1.duty(0)
            elif direction.lower() == "cw":
                self.n2.duty(0)
                self.n1.duty(self.speed)
            else:
                print(f"{direction} - valor da Direção não válido")
                
        elif motor.lower() in ("right", "r"):

            self.percent_to_pwm(speed_percent)

            if direction.lower() == "cw":
                self.n4.duty(self.speed)
                self.n3.duty(0)
            elif direction.lower() == "ccw":
                self.n4.duty(0)
                self.n3.duty(self.speed)
            else:
                print(f"{direction} - valor da Direção não válido")

        elif motor.lower() in ("all", "a"):

            self.percent_to_pwm(speed_percent)

            if direction.lower() == "cw":
                self.n2.duty(0)
                self.n1.duty(self.speed)
                self.n4.duty(self.speed)
                self.n3.duty(0)
            elif direction.lower() == "ccw":
                self.n2.duty(self.speed)
                self.n1.duty(0)
                self.n4.duty(0)
                self.n3.duty(self.speed)
            else:
                print(f"{direction} - valor da Direção não válido")

        else:
            print(f"{motor} - valor do Motor não válido")
            self.n2.duty(0)
            self.n1.duty(0)
            self.n4.duty(0)
            self.n3.duty(0)
    
    


# - Para o motor quando chamada com a string do Nome do Motor (Direito: ['right'] ou ['r'],
#  Esquerdo: ['left'] ou ['l'], ou Todos: ['all'] ou ['a']) * ;
#
#   * não há problemas no aparecimento de letras MAIÚSCULAS nas strings.
#
# Exemplo:
#               Hbridge.Stop('all')

    def Stop(self, motor):
        
        if motor.lower() in ("left", "l"):
            self.n1.duty(0)
            self.n2.duty(0)

        elif motor.lower() in ("right", "r"):
            self.n3.duty(0)
            self.n4.duty(0)

        elif motor.lower() in ("all", "a"):
            self.n1.duty(0)
            self.n2.duty(0)
            self.n3.duty(0)
            self.n4.duty(0)

        else:
            print(f"{motor} - valor do Motor não válido")
            self.n2.duty(0)
            self.n1.duty(0)
            self.n4.duty(0)
            self.n3.duty(0)
             




# - Utiliza-se para determinar o valor de velocidade mínimo que o motor suporta.
#
# Exemplo:
#               Hbridge.min_speed_config(200)
#
# ---quando o valor de velocidade escolhido for 1, o valor do duty do PWM será 200---

    def min_speed_config(self, min_speed_value):
        self.min_speed = min(max(min_speed_value, 0), 1023)


    
#
# - Faz a converção da velocidade em porcentagem para escala 10 bits utilizando o valor mínimo de velocidade.
#

    def percent_to_pwm(self, speed_percent):
        sp = max(min(speed_percent, 100), 0)
        if sp <= 0:
            self.speed = 0
        else:
            self.speed = int(self.min_speed + (sp - 1) * (1023 - self.min_speed) / 99)
