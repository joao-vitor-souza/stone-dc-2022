import warnings

from gerador import Gerador

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    gerador = Gerador()
    gerador.dadosLimpos()
