import pytest

from carrinho import CarrinhoDeCompras


def carrinho_com(*precos):
    carrinho = CarrinhoDeCompras()
    for i, preco in enumerate(precos):
        carrinho.adicionar_item(f"item{i}", preco)
    return carrinho


# ---------- Fluxos principais ----------

def test_compra_sem_desconto_com_frete_padrao():
    c = carrinho_com(50.0)
    assert c.calcular_total_produtos() == pytest.approx(50.0)
    assert c.calcular_desconto() == 0.0
    assert c.calcular_frete() == 20.0
    assert c.calcular_total_final() == pytest.approx(70.0)


def test_soma_de_varios_itens():
    c = carrinho_com(10.0, 20.5, 30.0)
    assert c.calcular_total_produtos() == pytest.approx(60.5)
    assert c.calcular_total_final() == pytest.approx(80.5)


def test_desconto_10_por_cento_com_frete_pago():
    c = carrinho_com(150.0)
    assert c.calcular_desconto() == pytest.approx(15.0)
    assert c.calcular_frete() == 20.0
    assert c.calcular_total_final() == pytest.approx(155.0)


def test_desconto_10_por_cento_com_frete_gratis():
    c = carrinho_com(300.0)
    assert c.calcular_desconto() == pytest.approx(30.0)
    assert c.calcular_frete() == 0.0
    assert c.calcular_total_final() == pytest.approx(270.0)


def test_desconto_20_por_cento_com_frete_gratis():
    c = carrinho_com(1000.0)
    assert c.calcular_desconto() == pytest.approx(200.0)
    assert c.calcular_frete() == 0.0
    assert c.calcular_total_final() == pytest.approx(800.0)


# ---------- Valores limite: faixa de desconto ----------

@pytest.mark.parametrize(
    "preco, desconto_esperado",
    [
        (99.99, 0.0),
        (100.00, 10.0),
        (499.99, 49.999),
        (500.00, 100.0),
    ],
)
def test_limites_faixa_de_desconto(preco, desconto_esperado):
    assert carrinho_com(preco).calcular_desconto() == pytest.approx(desconto_esperado)


def test_total_final_em_99_99():
    assert carrinho_com(99.99).calcular_total_final() == pytest.approx(119.99)


def test_total_final_em_100_00():
    assert carrinho_com(100.00).calcular_total_final() == pytest.approx(110.0)


def test_total_final_em_499_99():
    assert carrinho_com(499.99).calcular_total_final() == pytest.approx(449.991)


def test_total_final_em_500_00():
    assert carrinho_com(500.00).calcular_total_final() == pytest.approx(400.0)


# ---------- Valores limite: frete grátis ----------

@pytest.mark.parametrize(
    "preco, frete_esperado",
    [
        (199.99, 20.0),
        (200.00, 0.0),
    ],
)
def test_limites_frete_gratis(preco, frete_esperado):
    assert carrinho_com(preco).calcular_frete() == frete_esperado


def test_total_final_em_199_99():
    assert carrinho_com(199.99).calcular_total_final() == pytest.approx(199.99 * 0.9 + 20.0)


def test_total_final_em_200_00():
    assert carrinho_com(200.00).calcular_total_final() == pytest.approx(180.0)


# ---------- Exceções ----------

@pytest.mark.parametrize("preco", [0, -0.01, -10.0])
def test_adicionar_item_com_preco_invalido_lanca_value_error(preco):
    c = CarrinhoDeCompras()
    with pytest.raises(ValueError, match="maior que zero"):
        c.adicionar_item("produto", preco)
    assert c.itens == []


def test_calcular_total_final_em_carrinho_vazio_lanca_value_error():
    with pytest.raises(ValueError, match="vazio"):
        CarrinhoDeCompras().calcular_total_final()


def test_carrinho_vazio_tem_total_desconto_e_frete_zerados():
    c = CarrinhoDeCompras()
    assert c.calcular_total_produtos() == 0
    assert c.calcular_desconto() == 0.0
    assert c.calcular_frete() == 0.0
