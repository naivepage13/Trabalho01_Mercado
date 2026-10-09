# Carrinho de Compras – Testes Unitários (ISO/IEC 25010)

Trabalho prático de Qualidade e Teste de Software. Implementa a classe
`CarrinhoDeCompras` (`carrinho.py`) e uma suíte de testes unitários
(`test_carrinho.py`) cobrindo fluxos principais, valores limite e exceções.

## Regras de negócio

- Desconto de 10% para total de produtos >= R$ 100,00
- Desconto de 20% para total de produtos >= R$ 500,00
- Frete grátis para total >= R$ 200,00; abaixo disso, frete fixo de R$ 20,00
- `ValueError` para item com preço <= 0 e para checkout de carrinho vazio

## Como executar

Requisitos: Python 3.8+.

```bash
pip install pytest
pytest -v
```

Alternativa sem pytest não é suportada (os testes usam `pytest.approx` e `parametrize`).

## Estrutura

- `carrinho.py` – classe `CarrinhoDeCompras`
- `test_carrinho.py` – suíte de testes unitários
