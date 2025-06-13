# modelos/avaliacao.py

class Avaliacao:
    """
    Representa uma avaliação feita por um cliente a um restaurante.

    Attributes:
        _cliente (str): Nome do cliente que realizou a avaliação.
        _nota (float): Nota atribuída ao restaurante.
    """

    def __init__(self, cliente: str, nota: float):
        """
        Inicializa uma instância de Avaliacao.

        Inputs:
        - cliente (str): Nome do cliente que fez a avaliação.
        - nota (float): Nota atribuída ao restaurante (entre 1 e 5).

        Raises:
        - ValueError: Se a nota não for um número entre 1 e 5.
        """
        self._cliente = cliente
        self._nota = nota
