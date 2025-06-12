# app.py

from modelos.restaurante import Restaurante
from modelos.cardapio.bebida import Bebida
from modelos.cardapio.prato import Prato
from modelos.cardapio.sobremesa import Sobremesa

restaurante_praca = Restaurante('praça', 'Gourmet')
bebida_suco = Bebida('Suco de Melancia', 5.0,'grande')
bebida_suco.aplicar_desconto()

prato_paozinho = Prato('Pãozinho',2.00,'O melhor pão da cidade')
prato_paozinho.aplicar_desconto()

sorvete = Sobremesa(nome="Sorvete de Chocolate", preco=12.90, descricao="Sorvete artesanal de chocolate belga", tipo="Sorvete", tamanho="Médio")
sorvete.aplicar_desconto()

restaurante_praca.adicionar_ao_cardapio(bebida_suco)
restaurante_praca.adicionar_ao_cardapio(prato_paozinho)
restaurante_praca.adicionar_ao_cardapio(sorvete)


def main():
    restaurante_praca.exibir_cardapio()

if __name__ == '__main__':
    main()