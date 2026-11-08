import array
import json
import math
import os
import random
import shutil
import sys

import pygame

LARGURA, ALTURA = 1280, 720

AZUL_ESCURO = (16, 34, 64)
LIMAO = (212, 225, 87)
AZUL_CLARO = (125, 185, 220)
AZUL = (58, 80, 176)
BRANCO = (240, 244, 248)
SOMBRA = (8, 18, 36)
PAINEL = (12, 26, 50)
VERMELHO = (226, 42, 62)
VERMELHO_APAGADO = (96, 28, 44)
RAIO_BOTAO = 18

if getattr(sys, "frozen", False):
    PASTA = os.path.dirname(sys.executable)
else:
    PASTA = os.path.dirname(os.path.abspath(__file__))
ARQ_RECEITAS = os.path.join(PASTA, "receitas.json")
ARQ_CONFIG = os.path.join(PASTA, "config.json")
ARQ_RANKING = os.path.join(PASTA, "ranking.json")
ARQ_FOTO = os.path.join(PASTA, "creditos.png")
ARQ_CHAO = os.path.join(PASTA, "chao.png")
PASTA_IMG = os.path.join(PASTA, "imagens")
PASTA_AUDIO = os.path.join(PASTA, "audios")
ARQ_FONTE = os.path.join(PASTA, "fonte", "PressStart2P-Regular.ttf")

TELAS = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), None]
NOMES_TELA = ["960 x 540", "1280 x 720", "1600 x 900", "1920 x 1080", "TELA CHEIA"]
EVENTOS_SOM = [
    ("acerto", "SOM DE ACERTO"),
    ("erro", "SOM DE ERRO"),
    ("vitoria", "SOM DE VITÓRIA"),
    ("derrota", "SOM DE DERROTA"),
]

ITENS_CENARIO = [
    ("ceu", "CENÁRIO DE FUNDO"),
    ("sol", "SOL"),
    ("montanhas", "MONTANHAS DE FUNDO"),
    ("chao", "CHÃO"),
]
DICAS_CENARIO = {
    "ceu": "IMAGEM QUE PREENCHE A TELA TODA",
    "sol": "PNG COM FUNDO TRANSPARENTE",
    "montanhas": "PNG TRANSPARENTE, LARGURA DA TELA",
    "chao": "TEXTURA REPETIDA NA FAIXA DO CHÃO",
}

VIDAS_INICIAIS = 3
VIDAS_MAX = 5
ACERTOS_POR_VIDA = 4
CONTINUES_MAX = 1
SEGUNDOS_POR_ETAPA = 8
PONTOS_ACERTO = 100
BONUS_TEMPO_MAX = 1000
BONUS_PERFEITO = 500
PERIODO_DIA = 80.0
TEMPO_OCIOSO = 15000
ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CODIGO_SECRETO = [
    pygame.K_UP,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_DOWN,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_UP,
]
CREDITOS_PARAGRAFOS = [
    "Esta foi a Semana da Qualidade da UPP-1, feita por toda a equipe!",
    "Ao público, esperamos que tenham gostado. E à nossa equipe, espero que curtam o momento e que, acima de tudo, tenham aproveitado todo o aprendizado.",
    "Tenho certeza de que houve perrengues até chegarmos aqui, mas tenho orgulho de todos vocês e, principalmente, do esforço de cada dia, apesar de todas as adversidades.",
    "Parabéns a todos pelo excelente trabalho!",
]
ASSINATURA = "Mauricio Stuart"

CORACAO = [
    "01100110",
    "11111111",
    "11111111",
    "11111111",
    "01111110",
    "00111100",
    "00011000",
]

CURSOR = [
    "X...........",
    "XX..........",
    "XWX.........",
    "XWWX........",
    "XWWWX.......",
    "XWWWWX......",
    "XWWWWWX.....",
    "XWWWWWWX....",
    "XWWWWWWWX...",
    "XWWWWWXXXX..",
    "XWWXWWX.....",
    "XWX.XWWX....",
    "XX..XWWX....",
    "X....XWWX...",
    ".....XWWX...",
    "......XX....",
]

RECEITAS_PADRAO = [
    {
        "nome": "Xarope simples",
        "etapas": [
            "Pesar a água purificada",
            "Aquecer a água a 60 graus",
            "Dissolver o açúcar sob agitação",
            "Resfriar a solução à temperatura ambiente",
            "Filtrar o xarope",
            "Envasar e identificar o lote",
        ],
    },
    {
        "nome": "Sabonete líquido",
        "etapas": [
            "Pesar as matérias-primas",
            "Misturar a água com o tensoativo",
            "Adicionar a fragrância e o corante",
            "Ajustar o pH da mistura",
            "Aprovar a amostra no controle de qualidade",
            "Envasar nos frascos",
            "Rotular e embalar",
        ],
    },
    {
        "nome": "Tinta acrílica branca",
        "etapas": [
            "Carregar a água no tanque",
            "Adicionar o dispersante sob agitação",
            "Incorporar o pigmento branco",
            "Dispersar em alta rotação",
            "Adicionar a resina acrílica",
            "Ajustar viscosidade e pH",
            "Filtrar e envasar",
        ],
    },
]


def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


CORES_CANO = [
    ("verde", "VERDE", {"L": (82, 254, 48), "G": (0, 120, 4)}),
    ("azul", "AZUL", {"L": (96, 196, 255), "G": (16, 70, 170)}),
    ("vermelho", "VERMELHO", {"L": (255, 110, 96), "G": (150, 24, 24)}),
]


def carregar_config():
    base = {
        "volume": 0.7,
        "tela": 1,
        "crt": True,
        "cano": 0,
        "musica_menu": "",
        "musica_jogo": "",
        "audio": {chave: "" for chave, _ in EVENTOS_SOM},
        "visual": {chave: "" for chave, _ in ITENS_CENARIO},
    }
    try:
        with open(ARQ_CONFIG, encoding="utf-8") as f:
            dados = json.load(f)
        base["volume"] = min(1.0, max(0.0, float(dados.get("volume", base["volume"]))))
        base["tela"] = min(len(TELAS) - 1, max(0, int(dados.get("tela", base["tela"]))))
        base["crt"] = bool(dados.get("crt", True))
        base["cano"] = min(len(CORES_CANO) - 1, max(0, int(dados.get("cano", 0))))
        base["musica_menu"] = str(dados.get("musica_menu", dados.get("musica", "")))
        base["musica_jogo"] = str(dados.get("musica_jogo", ""))
        base["audio"].update(dados.get("audio", {}))
        for k, v in dados.get("visual", {}).items():
            if k in base["visual"]:
                base["visual"][k] = str(v)
    except Exception:
        pass
    return base


def carregar_receitas():
    if not os.path.exists(ARQ_RECEITAS):
        salvar_json(ARQ_RECEITAS, RECEITAS_PADRAO)
        return [dict(r) for r in RECEITAS_PADRAO]
    try:
        with open(ARQ_RECEITAS, encoding="utf-8") as f:
            dados = json.load(f)
        return [r for r in dados if r.get("nome") and len(r.get("etapas", [])) >= 2]
    except Exception:
        return []


def carregar_ranking():
    try:
        with open(ARQ_RANKING, encoding="utf-8") as f:
            dados = json.load(f)
        lista = [
            {
                "nome": str(r["nome"])[:3].upper(),
                "pontos": int(r["pontos"]),
                "receita": str(r.get("receita", "")),
            }
            for r in dados
        ]
        lista.sort(key=lambda r: -r["pontos"])
        return lista[:10]
    except Exception:
        return []


pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass
pygame.display.set_caption("Semana da Qualidade - Monte a Receita")

tela = pygame.Surface((LARGURA, ALTURA))
relogio = pygame.time.Clock()
cfg = carregar_config()
receitas = carregar_receitas()
ranking = carregar_ranking()
fila = []
sons = {}
sinteticos = {}
janela = None
cache_texto = {}
transicao = None
T_FECHAR = 500
T_CARTAO = 1800
T_ABRIR = 550
DUR_TRANSICAO = T_FECHAR + T_CARTAO + T_ABRIR
PENDENTE = {"pontos": 0, "receita": "", "destino": "menu"}
RANK_DESTAQUE = -1
RANK_DESTINO = "menu"
menu_sel = 0

tremor_ate = 0
tremor_dur = 1
tremor_forca = 0
flash_ate = 0
flash_dur = 1
flash_cor = (255, 255, 255)
flash_alfa = 120

particulas = []
popups = []

if os.path.exists(ARQ_FONTE):
    FONTE = pygame.font.Font(ARQ_FONTE, 8)
else:
    FONTE = pygame.font.Font(None, 14)

VEU = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
VEU.fill((8, 18, 36, 215))


def qualifica(p):
    return p > 0 and (len(ranking) < 10 or p > ranking[-1]["pontos"])


def registrar(nome, pontos, receita):
    entrada = {"nome": nome, "pontos": int(pontos), "receita": receita}
    ranking.append(entrada)
    ranking.sort(key=lambda r: -r["pontos"])
    del ranking[10:]
    salvar_json(ARQ_RANKING, ranking)
    for i, r in enumerate(ranking):
        if r is entrada:
            return i
    return -1


def varrer(f0, f1, ms, passos=8):
    return [(f0 + (f1 - f0) * k / (passos - 1), ms / passos) for k in range(passos)]


def sintetizar(notas, vol=0.28):
    info = pygame.mixer.get_init()
    if not info:
        return None
    taxa, formato, canais = info
    if formato not in (-16, 32784):
        return None
    amostras = array.array("h")
    for freq, ms in notas:
        n = int(taxa * ms / 1000)
        fade = max(1, min(n // 4, int(taxa * 0.012)))
        for i in range(n):
            if freq <= 0:
                s = 0
            else:
                v = 1 if (i * freq / taxa) % 1.0 < 0.5 else -1
                env = (1.0 - 0.35 * i / n) * min(1.0, (n - i) / fade)
                s = int(v * env * vol * 32767)
            amostras.extend((s,) * canais)
    try:
        return pygame.mixer.Sound(buffer=amostras.tobytes())
    except Exception:
        return None


def criar_sons_8bit():
    modelos = {
        "acerto": [(988, 60), (1319, 130)],
        "erro": varrer(240, 90, 300),
        "vitoria": [
            (523, 110),
            (659, 110),
            (784, 110),
            (1047, 230),
            (0, 40),
            (784, 100),
            (1047, 380),
        ],
        "derrota": [(392, 170), (349, 170), (330, 170), (294, 300), (262, 460)],
        "vida": [(659, 70), (784, 70), (1319, 70), (1175, 70), (1319, 70), (1568, 220)],
        "combo": [(880, 50), (1175, 50), (1480, 100)],
        "contagem": [(660, 150)],
        "vai": [(1320, 320)],
        "mover": [(520, 35)],
        "selecionar": [(780, 50), (1040, 100)],
        "recorde": [
            (784, 80),
            (988, 80),
            (1175, 80),
            (1568, 220),
            (0, 60),
            (1568, 70),
            (1760, 300),
        ],
    }
    for nome, notas in modelos.items():
        s = sintetizar(notas)
        if s is not None:
            s.set_volume(cfg["volume"])
            sinteticos[nome] = s


def tremer(ms=350, forca=8):
    global tremor_ate, tremor_dur, tremor_forca
    tremor_dur = ms
    tremor_ate = pygame.time.get_ticks() + ms
    tremor_forca = forca


def piscar_tela(cor, ms=250, alfa=120):
    global flash_ate, flash_dur, flash_cor, flash_alfa
    flash_dur = ms
    flash_ate = pygame.time.get_ticks() + ms
    flash_cor = cor
    flash_alfa = alfa


def deslocamento_tremor():
    agora = pygame.time.get_ticks()
    if agora >= tremor_ate:
        return 0, 0
    f = tremor_forca * (tremor_ate - agora) / tremor_dur
    return round(random.uniform(-f, f)), round(random.uniform(-f, f))


def soltar(x, y, n, cores, vel=260, grav=500, vida=(500, 1000), tam=(6, 10)):
    for _ in range(n):
        a = random.uniform(0, 2 * math.pi)
        v = random.uniform(vel * 0.3, vel)
        particulas.append(
            [
                x,
                y,
                math.cos(a) * v,
                math.sin(a) * v,
                random.randint(*vida),
                random.choice(cores),
                random.randint(*tam),
                0,
                grav,
            ]
        )


def chover_confete(n):
    for _ in range(n):
        particulas.append(
            [
                random.uniform(0, LARGURA),
                -10,
                random.uniform(-50, 50),
                random.uniform(120, 260),
                3200,
                random.choice(FESTA),
                random.randint(8, 12),
                0,
                40,
            ]
        )


def atualizar_particulas():
    dt = min(50, relogio.get_time())
    s = dt / 1000
    vivas = []
    for p in particulas:
        p[7] += dt
        if p[7] >= p[4]:
            continue
        p[3] += p[8] * s
        p[0] += p[2] * s
        p[1] += p[3] * s
        vivas.append(p)
    particulas[:] = vivas


def desenhar_particulas():
    for p in particulas:
        if p[7] > p[4] * 0.75 and (p[7] // 70) % 2:
            continue
        pygame.draw.rect(tela, p[5], (round(p[0]), round(p[1]), p[6], p[6]))


def aplicar_tela():
    global janela
    tamanho = TELAS[cfg["tela"]]
    if tamanho is None:
        janela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        janela = pygame.display.set_mode(tamanho)
    pygame.mouse.set_visible(False)


def escala_janela():
    jw, jh = janela.get_size()
    esc = min(jw / LARGURA, jh / ALTURA)
    return jw, jh, esc


def pos_mouse():
    mx, my = pygame.mouse.get_pos()
    jw, jh, esc = escala_janela()
    ox = (jw - LARGURA * esc) / 2
    oy = (jh - ALTURA * esc) / 2
    return ((mx - ox) / esc, (my - oy) / esc)


def sprite(grade, cores, px):
    s = pygame.Surface((len(grade[0]) * px, len(grade) * px), pygame.SRCALPHA)
    for j, linha in enumerate(grade):
        for i, c in enumerate(linha):
            if c in cores:
                pygame.draw.rect(s, cores[c], (i * px, j * px, px, px))
    return s


SPR_CURSOR = sprite(CURSOR, {"X": SOMBRA, "W": BRANCO}, 2)

IRIS_W, IRIS_H = LARGURA // 8, ALTURA // 8
IRIS_MAX = math.hypot(IRIS_W / 2, IRIS_H / 2) + 2
PASSOS_IRIS = 14


def iniciar_transicao():
    global transicao, tela
    original = tela
    foto = pygame.Surface((LARGURA, ALTURA))
    tela = foto
    fundo(True)
    desenhar_menu(pos_mouse())
    tela = original
    transicao = {"foto": foto, "ini": pygame.time.get_ticks()}


def iris(raio):
    mascara = pygame.Surface((IRIS_W, IRIS_H), pygame.SRCALPHA)
    mascara.fill((0, 0, 0, 255))
    if raio > 0:
        pygame.draw.circle(mascara, (0, 0, 0, 0), (IRIS_W // 2, IRIS_H // 2), int(raio))
    tela.blit(pygame.transform.scale(mascara, (LARGURA, ALTURA)), (0, 0))


def onda(t, amp=44, queda=6.5, freq=18.0):
    v = -amp * math.exp(-queda * t) * math.cos(freq * t)
    return round(v / 4) * 4


def texto_onda(txt, escala, cor, cx, y, ms, atraso, passo=35, sombra=False, amp=44):
    x0 = cx - largura(txt, escala) // 2
    d = max(2, escala // 2 + 1)
    for i, ch in enumerate(txt):
        if ch == " ":
            continue
        t = (ms - atraso - i * passo) / 1000
        if t < 0:
            continue
        x = x0 + (largura(txt[:i], escala) if i else 0)
        yy = y + onda(t, amp)
        if sombra:
            texto(ch, escala, SOMBRA, x + d, yy + d)
        texto(ch, escala, cor, x, yy)


def cartao_transicao(ms):
    tela.fill((0, 0, 0))
    pygame.draw.rect(tela, BRANCO, (330, 220, 620, 280), 4)
    pygame.draw.rect(tela, AZUL_CLARO, (342, 232, 596, 256), 2)
    texto_onda("PREPARE-SE!", 5, BRANCO, LARGURA // 2, 270, ms, 100)
    for i in range(3):
        t = (ms - 500 - i * 110) / 1000
        if t >= 0:
            desenhar_coracao(LARGURA // 2 - 80 + i * 60, 360 + onda(t), True)
    texto_onda("3 VIDAS", 3, AZUL_CLARO, LARGURA // 2, 430, ms, 750)


def aplicar_transicao():
    global transicao
    ms = pygame.time.get_ticks() - transicao["ini"]
    if ms >= DUR_TRANSICAO:
        transicao = None
        return
    if ms < T_FECHAR:
        passo = int(ms / T_FECHAR * (PASSOS_IRIS + 1))
        tela.blit(transicao["foto"], (0, 0))
        iris(IRIS_MAX * max(0.0, 1 - passo / PASSOS_IRIS))
    elif ms < T_FECHAR + T_CARTAO:
        cartao_transicao(ms - T_FECHAR)
    else:
        passo = int((ms - T_FECHAR - T_CARTAO) / T_ABRIR * (PASSOS_IRIS + 1))
        iris(IRIS_MAX * min(1.0, passo / PASSOS_IRIS))


def montar_crt():
    s = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    for y in range(0, ALTURA, 4):
        pygame.draw.rect(s, (0, 0, 0, 46), (0, y + 2, LARGURA, 2))
    vinheta = pygame.Surface((160, 90), pygame.SRCALPHA)
    for yy in range(90):
        for xx in range(160):
            dx = (xx - 79.5) / 80
            dy = (yy - 44.5) / 45
            d = dx * dx + dy * dy
            a = int(max(0.0, min(1.0, (d - 0.55) / 1.2)) * 150)
            vinheta.set_at((xx, yy), (0, 0, 0, a))
    s.blit(pygame.transform.smoothscale(vinheta, (LARGURA, ALTURA)), (0, 0))
    return s


CRT_SUP = montar_crt()
CRT_BANDA = pygame.Surface((LARGURA, 70), pygame.SRCALPHA)
for _i in range(70):
    pygame.draw.rect(CRT_BANDA, (255, 255, 255, int(14 * math.sin(_i / 70 * math.pi))), (0, _i, LARGURA, 1))
FLASH_SUP = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)


def desenhar_crt():
    tela.blit(CRT_SUP, (0, 0))
    y = int((pygame.time.get_ticks() / 14) % (ALTURA + 140)) - 70
    tela.blit(CRT_BANDA, (0, y))


def desenhar_flash():
    agora = pygame.time.get_ticks()
    if agora < flash_ate:
        a = int(flash_alfa * (flash_ate - agora) / flash_dur)
        FLASH_SUP.fill(flash_cor + (a,))
        tela.blit(FLASH_SUP, (0, 0))


def desenhar_cursor():
    if pygame.mouse.get_focused():
        x, y = pos_mouse()
        tela.blit(SPR_CURSOR, (int(x), int(y)))


def apresentar():
    atualizar_musica()
    if transicao is not None:
        aplicar_transicao()
    desenhar_flash()
    if cfg["crt"]:
        desenhar_crt()
    desenhar_cursor()
    jw, jh, esc = escala_janela()
    w, h = int(LARGURA * esc), int(ALTURA * esc)
    imagem = pygame.transform.scale(tela, (w, h))
    dx, dy = deslocamento_tremor()
    janela.fill((0, 0, 0))
    janela.blit(imagem, ((jw - w) // 2 + int(dx * esc), (jh - h) // 2 + int(dy * esc)))
    pygame.display.flip()


def superficie_texto(txt, escala, cor):
    if len(cache_texto) > 1500:
        cache_texto.clear()
    chave = (txt, escala, cor)
    if chave not in cache_texto:
        base = FONTE.render(txt if txt else " ", False, cor)
        cache_texto[chave] = pygame.transform.scale(
            base, (base.get_width() * escala, base.get_height() * escala)
        )
    return cache_texto[chave]


def texto(txt, escala, cor, x, y, alinhar="esq"):
    s = superficie_texto(txt, escala, cor)
    if alinhar == "centro":
        x -= s.get_width() // 2
    elif alinhar == "dir":
        x -= s.get_width()
    tela.blit(s, (x, y))


def texto_sombra(txt, escala, cor, x, y, alinhar="esq"):
    d = max(2, escala // 2 + 1)
    texto(txt, escala, SOMBRA, x + d, y + d, alinhar)
    texto(txt, escala, cor, x, y, alinhar)


def largura(txt, escala):
    return superficie_texto(txt, escala, BRANCO).get_width()


def alt_linha(escala):
    return FONTE.get_height() * escala + 4


def quebrar(txt, escala, maxw):
    linhas = []
    atual = ""
    for palavra in txt.split():
        teste = (atual + " " + palavra).strip()
        if largura(teste, escala) <= maxw or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas or [""]


def cortar(txt, escala, maxw):
    while txt and largura(txt, escala) > maxw:
        txt = txt[:-1]
    return txt


def cortar_fim(txt, escala, maxw):
    while txt and largura(txt, escala) > maxw:
        txt = txt[1:]
    return txt


def revelar(linhas, n):
    saida = []
    for linha in linhas:
        if n <= 0:
            saida.append("")
        else:
            saida.append(linha[:n])
            n -= len(linha)
    return saida


CEU = (28, 156, 240)
CEU_PONTO = (120, 200, 255)
BRILHO = (205, 240, 140)
VERDE = (88, 190, 44)
VERDE_CLARO = (150, 226, 84)
VERDE_ESCURO = (44, 138, 40)
CONTORNO = (22, 74, 34)
TERRA = (160, 98, 52)
TERRA_ESCURA = (120, 70, 36)
LARANJA = (236, 116, 44)
LARANJA_CLARO = (252, 160, 74)
CONTORNO_LARANJA = (96, 44, 14)
AMARELO = (255, 200, 40)
AMARELO_CLARO = (255, 232, 120)
CONTORNO_OURO = (130, 72, 10)
NUVEM_BORDA = (150, 204, 240)
PELE = (255, 214, 170)
CALCA = (40, 60, 130)
SAPATO = (90, 60, 40)
NAVY_TEUTO = (12, 36, 78)
CHAO_Y = 620

DOURADOS = [AMARELO, AMARELO_CLARO, BRANCO, (255, 168, 24)]
FESTA = [LIMAO, BRANCO, VERMELHO, AMARELO, AZUL_CLARO, LARANJA]

MORROS_LONGE = [(60, 170, 300), (430, 150, 260), (660, 190, 330), (960, 170, 280)]
MORROS_PERTO = [(30, 190, 400), (250, 150, 270), (900, 210, 360), (1090, 180, 250)]
ARBUSTOS = [(230, 26), (800, 24), (1040, 28)]
CORES_LONGE = ((122, 208, 104), (172, 234, 132), (58, 132, 78))
CORES_PERTO = (VERDE, VERDE_CLARO, CONTORNO)
NUVENS = [
    (0, 60, 22, 160),
    (420, 150, 14, 120),
    (800, 40, 18, 140),
    (1100, 230, 10, 100),
    (250, 330, 16, 130),
    (950, 400, 12, 110),
]
BRILHOS = [(30, 260), (180, 560), (560, 600), (1150, 280), (1230, 540), (700, 560)]
BLOCOS_CENA = [
    (40, 120, False, 0.0),
    (104, 120, True, 0.7),
    (1112, 120, True, 1.4),
    (1176, 120, False, 2.1),
]
MOEDAS_CENA = [
    (235, 335, 0.0),
    (285, 335, 0.4),
    (335, 335, 0.8),
    (945, 335, 1.2),
    (995, 335, 1.6),
    (1045, 335, 2.0),
]
CANOS_CENA = [(50, 470, 0.0), (1090, 420, 2.2)]
_alea = random.Random(5)
ESTRELAS_CEU = [
    (_alea.randrange(20, LARGURA - 20), _alea.randrange(10, 200), _alea.uniform(0, 6.28))
    for _ in range(46)
]


def abrir_imagem(caminho):
    try:
        img = pygame.image.load(caminho)
    except Exception:
        return None
    try:
        img = img.convert_alpha()
    except pygame.error:
        pass
    return img


def carregar_imagem_visual(chave):
    nome = cfg["visual"].get(chave, "")
    if not nome:
        return None
    return abrir_imagem(os.path.join(PASTA_IMG, nome))


def escalar(img, tam, suave=True):
    tam = (max(1, int(tam[0])), max(1, int(tam[1])))
    if suave:
        try:
            return pygame.transform.smoothscale(img, tam)
        except (ValueError, pygame.error):
            pass
    return pygame.transform.scale(img, tam)


def morro(w, h, cor=VERDE, listra=VERDE_CLARO, contorno=CONTORNO):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill(cor)
    for k in range(-h, w + h, 64):
        pygame.draw.line(s, listra, (k, h), (k + h, 0), 26)
    mascara = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(
        mascara,
        (255, 255, 255, 255),
        (0, 0, w, h),
        border_top_left_radius=w // 2,
        border_top_right_radius=w // 2,
    )
    s.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pygame.draw.rect(
        s,
        contorno,
        (0, 0, w, h),
        4,
        border_top_left_radius=w // 2,
        border_top_right_radius=w // 2,
    )
    return s


def arbusto(r):
    s = pygame.Surface((int(r * 5) + 8, int(r * 2.8) + 8), pygame.SRCALPHA)
    cs = ((r * 1.2, r * 1.9, r * 0.9), (r * 2.5, r * 1.5, r * 1.2), (r * 3.8, r * 1.9, r * 0.9))
    for pas, cor in ((4, CONTORNO), (0, VERDE)):
        for cx, cy, rr in cs:
            pygame.draw.circle(s, cor, (int(cx) + 4, int(cy) + 4), int(rr + pas))
    return s


def nuvem(w):
    k = w / 140
    s = pygame.Surface((w + 8, int(70 * k) + 8), pygame.SRCALPHA)
    cs = ((35, 46, 22), (65, 34, 28), (100, 44, 24))
    base = pygame.Rect(int(35 * k) + 4, int(44 * k) + 4, int(65 * k), int(24 * k))
    for pas, cor in ((4, NUVEM_BORDA), (0, BRANCO)):
        for cx, cy, r in cs:
            pygame.draw.circle(s, cor, (int(cx * k) + 4, int(cy * k) + 4), int(r * k) + pas)
        pygame.draw.rect(s, cor, base.inflate(pas * 2, pas * 2))
    return s


def montar_ceu_padrao():
    s = pygame.Surface((LARGURA, ALTURA))
    s.fill(CEU)
    aleatorio = random.Random(7)
    for _ in range(46):
        x = aleatorio.randrange(10, LARGURA - 10)
        y = aleatorio.randrange(10, CHAO_Y - 20)
        if aleatorio.random() < 0.5:
            pygame.draw.circle(s, CEU_PONTO, (x, y), 5, 2)
        else:
            pygame.draw.circle(s, CEU_PONTO, (x, y), 3)
    return s


def montar_ceu():
    img = carregar_imagem_visual("ceu")
    if img is None:
        return montar_ceu_padrao()
    esc = max(LARGURA / img.get_width(), ALTURA / img.get_height())
    w, h = round(img.get_width() * esc), round(img.get_height() * esc)
    s = pygame.Surface((LARGURA, ALTURA))
    s.blit(escalar(img, (w, h)), ((LARGURA - w) // 2, (ALTURA - h) // 2))
    return s


def montar_sol():
    img = carregar_imagem_visual("sol")
    if img is None:
        return None
    esc = 150 / max(img.get_size())
    return escalar(img, (img.get_width() * esc, img.get_height() * esc))


def montar_camada(morros, arbustos, cores):
    alt = max(m[2] for m in morros) + 14
    s = pygame.Surface((LARGURA, alt), pygame.SRCALPHA)
    for x, w, h in morros:
        s.blit(morro(w, h, *cores), (x, alt - h))
    for x, r in arbustos:
        b = arbusto(r)
        s.blit(b, (x, alt - b.get_height() + 4))
    return s


def montar_chao():
    alt = ALTURA - CHAO_Y
    img = carregar_imagem_visual("chao")
    if img is None and os.path.exists(ARQ_CHAO):
        img = abrir_imagem(ARQ_CHAO)
    if img is None:
        return montar_chao_padrao()
    larg = max(1, round(img.get_width() * alt / img.get_height()))
    bloco = escalar(img, (larg, alt), suave=False)
    espelho = pygame.transform.flip(bloco, True, False)
    s = pygame.Surface((LARGURA, alt), pygame.SRCALPHA)
    x, i = 0, 0
    while x < LARGURA:
        s.blit(bloco if i % 2 == 0 else espelho, (x, 0))
        x += larg
        i += 1
    return s


def montar_chao_padrao():
    s = pygame.Surface((LARGURA, ALTURA - CHAO_Y), pygame.SRCALPHA)
    s.fill(TERRA)
    for x in range(0, LARGURA, 72):
        pygame.draw.rect(s, TERRA_ESCURA, (x + 20, 66, 32, 10))
        pygame.draw.rect(s, TERRA_ESCURA, (x + 44, 86, 20, 8))
    for x in range(0, LARGURA + 40, 40):
        pygame.draw.circle(s, CONTORNO, (x + 20, 28), 22)
    pygame.draw.rect(s, CONTORNO, (0, 0, LARGURA, 28))
    for x in range(0, LARGURA + 40, 40):
        pygame.draw.circle(s, VERDE, (x + 20, 28), 18)
    pygame.draw.rect(s, VERDE, (0, 4, LARGURA, 24))
    pygame.draw.rect(s, VERDE_CLARO, (0, 10, LARGURA, 8))
    return s


CENA_CEU = None
CAMADA_LONGE = None
CAMADA_PERTO = None
Y_LONGE = 0
Y_PERTO = 0
CENA_CHAO = None
SPR_SOL = None


def recarregar_cenario():
    global CENA_CEU, CAMADA_LONGE, CAMADA_PERTO, Y_LONGE, Y_PERTO, CENA_CHAO, SPR_SOL
    CENA_CEU = montar_ceu()
    img = carregar_imagem_visual("montanhas")
    if img is not None:
        h = max(1, round(img.get_height() * LARGURA / img.get_width()))
        CAMADA_LONGE = None
        CAMADA_PERTO = escalar(img, (LARGURA, h))
        Y_PERTO = CHAO_Y + 10 - h
    else:
        CAMADA_LONGE = montar_camada(MORROS_LONGE, [], CORES_LONGE)
        CAMADA_PERTO = montar_camada(MORROS_PERTO, ARBUSTOS, CORES_PERTO)
        Y_LONGE = CHAO_Y + 10 - CAMADA_LONGE.get_height()
        Y_PERTO = CHAO_Y + 10 - CAMADA_PERTO.get_height()
    CENA_CHAO = montar_chao()
    SPR_SOL = montar_sol()


SPR_NUVENS = {n[3]: nuvem(n[3]) for n in NUVENS}
VEU_FUNDO = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
VEU_FUNDO.fill((8, 18, 36, 175))
NOITE_SUP = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
NOITE_CHAO = pygame.Surface((LARGURA, ALTURA - CHAO_Y), pygame.SRCALPHA)
SPR_BRILHO = pygame.Surface((18, 18), pygame.SRCALPHA)
pygame.draw.rect(SPR_BRILHO, BRILHO, (0, 6, 18, 6))
pygame.draw.rect(SPR_BRILHO, BRILHO, (6, 0, 6, 18))
SPR_ESTRELA = pygame.Surface((8, 8), pygame.SRCALPHA)
pygame.draw.rect(SPR_ESTRELA, BRANCO, (3, 0, 2, 8))
pygame.draw.rect(SPR_ESTRELA, BRANCO, (0, 3, 8, 2))


BALANCO_MOEDAS_INICIAL = 34
OURO_LATERAL = (206, 128, 14)
OURO_SOMBRA = (255, 168, 24)
ESPESSURA_MOEDA = 6


MOEDA_GRADE = [
    ".....KKKKKK.....",
    "...KKLLYYYGKK...",
    "..KLLYYYYYYGGK..",
    ".KLYYBBBBBBYYGK.",
    ".KLYBOOOOOOBYGK.",
    "KLYBOOSSSSOOBYGK",
    "KLYBOSSOOOOOBYGK",
    "KLYBOOSSSSOOBYGK",
    "KLYBOOOOOSSOBYGK",
    "KLYBOSSOOSSOBYGK",
    "KLYBOOSSSSOOBYGK",
    ".KYYBOOOOOOBGGK.",
    ".KYYYBBBBBBYGGK.",
    "..KYYYYYYYYGGK..",
    "...KKYYYYGGKK...",
    ".....KKKKKK.....",
]
MOEDA_PALETA = {
    "K": (122, 52, 56),
    "L": (255, 238, 150),
    "Y": (255, 216, 80),
    "G": (190, 140, 10),
    "B": (176, 108, 28),
    "O": (240, 168, 80),
    "S": (250, 205, 0),
}
MOEDA_LADO = (206, 148, 12)
MOEDA_LADO_ESC = (150, 96, 10)
PX_MOEDA = 3
MOEDA_N = len(MOEDA_GRADE[0])
MOEDA_ALT = len(MOEDA_GRADE) * PX_MOEDA
MOEDA_ESPESSURA = 4
VEL_GIRO_MOEDA = 4 * 0.8
_moeda_base = sprite(MOEDA_GRADE, MOEDA_PALETA, 1)
_moeda_cache = {}


def _moeda_3d(n, d, direcao):
    chave = (n, d, direcao)
    s = _moeda_cache.get(chave)
    if s is not None:
        return s
    fino = pygame.transform.scale(_moeda_base, (n, MOEDA_N))
    frente = pygame.transform.scale(fino, (n * PX_MOEDA, MOEDA_ALT))
    s = pygame.Surface((n * PX_MOEDA + d * PX_MOEDA, MOEDA_ALT), pygame.SRCALPHA)
    xf = 0 if direcao > 0 else d * PX_MOEDA
    if d:
        sil = pygame.mask.from_surface(frente, 40)
        for i in range(d, 0, -1):
            cor = MOEDA_LADO_ESC if i == d else MOEDA_LADO
            camada = sil.to_surface(setcolor=cor + (255,), unsetcolor=(0, 0, 0, 0))
            s.blit(camada, (xf + direcao * i * PX_MOEDA, 0))
    s.blit(frente, (xf, 0))
    if len(_moeda_cache) > 200:
        _moeda_cache.clear()
    _moeda_cache[chave] = s
    return s


def moeda(x, y, t, fase, sup=None, balanco=3):
    if sup is None:
        sup = tela
    ang = t * VEL_GIRO_MOEDA + fase
    n = int(abs(math.cos(ang)) * MOEDA_N + 0.5)
    y += round(math.sin(t * 2 + fase) * balanco / PX_MOEDA) * PX_MOEDA
    x, y = round(x), round(y)
    if n <= 2:
        w = MOEDA_ESPESSURA * PX_MOEDA
        K, G, L = MOEDA_PALETA["K"], MOEDA_LADO, MOEDA_PALETA["L"]
        x0 = x - w // 2
        topo = y - MOEDA_ALT // 2
        pygame.draw.rect(sup, K, (x0, topo + 2 * PX_MOEDA, w, MOEDA_ALT - 4 * PX_MOEDA))
        pygame.draw.rect(sup, K, (x0 + PX_MOEDA, topo + PX_MOEDA, w - 2 * PX_MOEDA, MOEDA_ALT - 2 * PX_MOEDA))
        pygame.draw.rect(sup, G, (x0 + PX_MOEDA, topo + 2 * PX_MOEDA, w - 2 * PX_MOEDA, MOEDA_ALT - 4 * PX_MOEDA))
        pygame.draw.rect(sup, L, (x0 + PX_MOEDA, topo + 3 * PX_MOEDA, PX_MOEDA // 2 + 1, MOEDA_ALT - 6 * PX_MOEDA))
        return
    d = int(abs(math.sin(ang)) * MOEDA_ESPESSURA + 0.5)
    direcao = 1 if math.sin(ang) > 0 else -1
    img = _moeda_3d(n, d, direcao)
    sup.blit(img, (x - img.get_width() // 2, y - MOEDA_ALT // 2))


def salto(t, fase):
    c = (t + fase) % 3.0
    if c < 0.3:
        return -round(math.sin(c / 0.3 * math.pi) * 12)
    return 0


def moeda_saindo(x, y_bloco, t, fase):
    ciclo = (t + fase) % 3.0
    cx = x + 32
    y0 = y_bloco + 32
    alt = 110
    if ciclo < 0.5:
        p = ciclo / 0.5
        moeda(cx, y0 - round(math.sin(p * math.pi / 2) * alt), t, fase)
    elif ciclo < 0.8:
        q = (ciclo - 0.5) / 0.3
        topo = y0 - alt
        tam = 120
        base = pygame.Surface((tam, tam), pygame.SRCALPHA)
        moeda(tam // 2, tam // 2, t, fase, base)
        lado = int(tam * (1 + q * 0.35))
        img = pygame.transform.scale(base, (lado // 3 * 3, lado // 3 * 3))
        img.set_alpha(int(255 * (1 - q) ** 1.5))
        tela.blit(img, img.get_rect(center=(cx, topo)))
        lado_f = max(2, round(8 * (1 - q)))
        dist = 16 + q * 34
        for ax, ay in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            px = cx + ax * dist * 0.7
            py = topo + ay * dist * 0.7
            pygame.draw.rect(tela, AMARELO_CLARO, (round(px - lado_f / 2), round(py - lado_f / 2), lado_f, lado_f))


def tijolo(x, y):
    r = pygame.Rect(x, y, 64, 64)
    pygame.draw.rect(tela, LARANJA, r)
    pygame.draw.rect(tela, LARANJA_CLARO, (x + 4, y + 4, 22, 6))
    pygame.draw.rect(tela, CONTORNO_LARANJA, (x, y + 30, 64, 4))
    pygame.draw.rect(tela, CONTORNO_LARANJA, (x + 30, y, 4, 30))
    pygame.draw.rect(tela, CONTORNO_LARANJA, (x + 14, y + 34, 4, 30))
    pygame.draw.rect(tela, CONTORNO_LARANJA, (x + 46, y + 34, 4, 30))
    pygame.draw.rect(tela, CONTORNO_LARANJA, r, 4)


def pergunta(x, y):
    r = pygame.Rect(x, y, 64, 64)
    pygame.draw.rect(tela, AMARELO, r)
    pygame.draw.rect(tela, AMARELO_CLARO, (x + 4, y + 4, 56, 8))
    for dx, dy in ((8, 8), (52, 8), (8, 52), (52, 52)):
        pygame.draw.rect(tela, CONTORNO_OURO, (x + dx - 2, y + dy - 2, 6, 6))
    pygame.draw.rect(tela, CONTORNO_OURO, r, 4)
    texto("?", 4, CONTORNO_OURO, r.centerx + 3, y + 19, "centro")
    texto("?", 4, BRANCO, r.centerx, y + 16, "centro")


PX_CANO = 5
CANO_PALETA = {"K": (0, 0, 0), "L": (82, 254, 48), "G": (0, 120, 4)}
CANO_TAMPA = [
    "KKKKKKKKKKKKKKKKKKKKKKKKKK",
    "KLLLLLLLLLLLLLLLLLLLLLLLLK",
    "KGGGGLLLLGGGGGGGGGGGGGGGGK",
    "KLLGGLLLLGLLGGGGGGGLGLLLGK",
    "KLLGGLLLLGLLGGGGGGGGLGLLGK",
    "KLLGGLLLLGLLGGGGGGGLGLLLGK",
    "KLLGGLLLLGLLGGGGGGGGLGLLGK",
    "KLLGGLLLLGLLGGGGGGGLGLLLGK",
    "KLLGGLLLLGLLGGGGGGGGLGLLGK",
    "KLLGGLLLLGLLGGGGGGGLGLLLGK",
    "KLLGGLLLLGLLGGGGGGGGLGLLGK",
    "KLLGGLLLLGLLGGGGGGGLGLLLGK",
    "KKKKKKKKKKKKKKKKKKKKKKKKKK",
]
CANO_SOMBRA = ".KKKKKKKKKKKKKKKKKKKKKKKK."
CANO_CORPO = [
    "..KLLGGLLLLGGGGGGGLGLLGK..",
    "..KLLGGLLLLGGGGGGLGLLLGK..",
]
CANO_W = 26 * PX_CANO
CANO_TAMPA_H = len(CANO_TAMPA) * PX_CANO
SPRS_CANO = []
for _, _, _pal in CORES_CANO:
    _p = dict(CANO_PALETA)
    _p.update(_pal)
    SPRS_CANO.append(
        (
            sprite(CANO_TAMPA, _p, PX_CANO),
            sprite(
                [CANO_SOMBRA] + [CANO_CORPO[i % 2] for i in range(ALTURA // PX_CANO + 1)],
                _p,
                PX_CANO,
            ),
        )
    )


def cano(x, topo, w=140):
    x += (w - CANO_W) // 2
    tampa, corpo = SPRS_CANO[cfg["cano"]]
    tela.blit(corpo, (x, topo + CANO_TAMPA_H))
    tela.blit(tampa, (x, topo))


def desenhar_sol(x, y):
    x, y = int(x), int(y)
    if SPR_SOL is not None:
        tela.blit(SPR_SOL, SPR_SOL.get_rect(center=(x, y)))
        return
    pygame.draw.circle(tela, (255, 200, 60), (x, y), 46)
    pygame.draw.circle(tela, (255, 238, 150), (x, y), 38)
    giro = pygame.time.get_ticks() / 4000
    for k in range(8):
        a = k * math.pi / 4 + giro
        pygame.draw.rect(
            tela,
            (255, 220, 100),
            (x + round(math.cos(a) * 66) - 4, y + round(math.sin(a) * 66) - 4, 8, 8),
        )


def desenhar_lua(x, y):
    x, y = int(x), int(y)
    pygame.draw.circle(tela, (255, 255, 235), (x, y), 36)
    for dx, dy, r in ((-10, -8, 8), (12, 6, 6), (-4, 14, 5)):
        pygame.draw.circle(tela, (222, 222, 196), (x + dx, y + dy), r)


def desenhar_camada(sup, y, vel, t):
    dx = int((t * vel) % LARGURA)
    tela.blit(sup, (-dx, y))
    tela.blit(sup, (LARGURA - dx, y))


def tom_do_dia(luz):
    quente = (240, 120, 50)
    noite = (6, 10, 40)
    if luz > 0.35:
        return (0, 0, 0, 0)
    if luz > 0:
        k = 1 - luz / 0.35
        return quente + (int(70 * k),)
    k = min(1.0, -luz * 4)
    return misturar(quente, noite, k) + (70 + int(85 * k),)
ILUM = {"luz": 1.0, "x": 640.0}


def fundo(vivo=False, inicial=False):
    t = pygame.time.get_ticks() / 1000
    p = (t / PERIODO_DIA + 0.12) % 1.0
    luz = math.sin(2 * math.pi * p)
    tela.blit(CENA_CEU, (0, 0))
    if p < 0.5:
        q = p / 0.5
        desenhar_sol(140 + q * 1000, 520 - math.sin(math.pi * q) * 440)
    else:
        q = (p - 0.5) / 0.5
        desenhar_lua(140 + q * 1000, 520 - math.sin(math.pi * q) * 440)
    ILUM["luz"] = luz
    ILUM["x"] = 140 + q * 1000
    if CAMADA_LONGE is not None:
        desenhar_camada(CAMADA_LONGE, Y_LONGE, 6, t)
    desenhar_camada(CAMADA_PERTO, Y_PERTO, 14, t)
    for desloc, y, vel, w in NUVENS:
        s = SPR_NUVENS[w]
        x = int((desloc + t * vel) % (LARGURA + s.get_width())) - s.get_width()
        tela.blit(s, (x, y))
    tom = tom_do_dia(luz)
    if tom[3] > 0:
        NOITE_SUP.fill(tom)
        tela.blit(NOITE_SUP, (0, 0))
    vis = max(0.0, min(1.0, (-luz - 0.1) * 3))
    if vis > 0:
        for x, y, f in ESTRELAS_CEU:
            SPR_ESTRELA.set_alpha(int(255 * vis * (0.55 + 0.45 * math.sin(t * 3 + f))))
            tela.blit(SPR_ESTRELA, (x, y))
    for i, (x, y) in enumerate(BRILHOS):
        alfa = int(255 * max(0.0, math.sin(((t * 2 + i) % 3) / 3 * math.pi)))
        if alfa > 0:
            SPR_BRILHO.set_alpha(alfa)
            tela.blit(SPR_BRILHO, (x, y))
    for x, y, com_pergunta, fase in BLOCOS_CENA:
        if com_pergunta:
            moeda_saindo(x, y, t, fase)
    for x, y, com_pergunta, fase in BLOCOS_CENA:
        yy = y + salto(t, fase)
        if com_pergunta:
            pergunta(x, yy)
        else:
            tijolo(x, yy)
    agora_ms = pygame.time.get_ticks()
    for i, (x, y, fase) in enumerate(MOEDAS_CENA):
        if agora_ms < MOEDA_VOLTA[i]:
            continue
        moeda(x, y, t, fase, balanco=BALANCO_MOEDAS_INICIAL if inicial else 3)
    for x, topo, fase in CANOS_CENA:
        cano(x, topo)
    tela.blit(CENA_CHAO, (0, CHAO_Y))
    if tom[3] > 0:
        NOITE_CHAO.fill(tom[:3] + (tom[3] // 2,))
        tela.blit(NOITE_CHAO, (0, CHAO_Y))
    if not vivo:
        tela.blit(VEU_FUNDO, (0, 0))


def caixa(x, y, w, h, cor):
    pygame.draw.rect(tela, SOMBRA, (x - 2, y - 2, w + 4, h + 4))
    pygame.draw.rect(tela, cor, (x, y, w, h))


PX_MASCOTE = 5

PALETA_MASCOTE = {
    "K": SOMBRA,
    "C": AZUL_CLARO,
    "c": (190, 226, 244),
    "S": PELE,
    "E": SOMBRA,
    "R": (255, 150, 150),
    "T": BRANCO,
    "W": BRANCO,
    "G": (205, 214, 230),
    "B": AZUL,
    "P": CALCA,
    "O": SAPATO,
}

MATERIAIS = {
    "W": ((255, 255, 255), BRANCO, (166, 180, 208)),
    "C": ((196, 232, 250), AZUL_CLARO, (74, 132, 184)),
    "S": ((255, 234, 202), PELE, (222, 164, 126)),
    "P": ((72, 98, 178), CALCA, (24, 38, 92)),
    "O": ((132, 94, 66), SAPATO, (54, 34, 24)),
}

CONTORNOS = {
    "S": (116, 66, 48),
    "W": (44, 58, 98),
    "C": (26, 62, 106),
    "c": (26, 62, 106),
    "P": (14, 22, 58),
    "O": (36, 22, 16),
}

_BAIXO = [
    "...KWWWGGWWWK...",
    "...KWWWGGWWWK...",
    "...KKKKKKKKKK...",
    "...KPPPKKPPPK...",
    "...KPPPKKPPPK...",
    "...KPPPKKPPPK...",
    "..KOOOOKKOOOOK..",
    "..KKKKK..KKKKK..",
]

_CABECA_BASE = [
    ".....KKKKKK.....",
    "...KKCCCCCCKK...",
    "..KCcCCCCCCCCK..",
    "..KCCCCCCCCCCK..",
    "..KKKKKKKKKKKK..",
    "..KSSSSSSSSSSK..",
]

MASC_NORMAL = (
    _CABECA_BASE
    + [
        "..KSSESSSSESSK..",
        "..KSSESSSSESSK..",
        "..KSSSKKKKSSSK..",
        "...KSSSSSSSSK...",
        "....KKWWWWKK....",
        ".KKWWWWWWWWWWKK.",
        "KWWKWWWGGWWWKWWK",
        "KWWKWWWGGWBWKWWK",
        "KWWKWWWGGWBWKWWK",
        "KSSKWWWGGWGGKSSK",
        ".KKKWWWGGWWWKKK.",
    ]
    + _BAIXO
)

MASC_FELIZ = (
    _CABECA_BASE
    + [
        "..KSSEESSEESSK..",
        "..KSRSSSSSSRSK..",
        "..KSSKTTTTKSSK..",
        "...KSSKKKKSSK...",
        "....KKWWWWKK....",
        ".KKWWWWWWWWWWKK.",
        "...KWWWGGWWWK...",
        "...KWWWGGWBWK...",
        "...KWWWGGWBWK...",
        "...KWWWGGWGGK...",
        "...KWWWGGWWWK...",
    ]
    + _BAIXO
)

MASC_TRISTE = (
    _CABECA_BASE
    + [
        "..KSSESSSSESSK..",
        "..KSSESSSSESSK..",
        "..KSSSSKKSSSSK..",
        "...KSSKSSKSSK...",
        "....KKWWWWKK....",
        ".KKWWWWWWWWWWKK.",
        "KWWKWWWGGWWWKWWK",
        "KWWKWWWGGWBWKWWK",
        "KWWKWWWGGWBWKWWK",
        "KWWKWWWGGWGGKWWK",
        "KSSKWWWGGWWWKSSK",
    ]
    + _BAIXO
)

_PERNAS_ABERTAS = [
    "...KPPPKKPPPK...",
    "..KPPPK..KPPPK..",
    ".KPPPK....KPPPK.",
    ".KOOOOK...KOOOOK",
    ".KKKKK....KKKKK.",
]

_BRACOS_A = [
    "KSSKWWWGGWWWKWWK",
    "KWWKWWWGGWBWKWWK",
    ".KKKWWWGGWBWKWWK",
    "...KWWWGGWGGKWWK",
    "...KWWWGGWWWKSSK",
]

_BRACOS_B = [
    "KWWKWWWGGWWWKSSK",
    "KWWKWWWGGWBWKWWK",
    "KWWKWWWGGWBWKKK.",
    "KWWKWWWGGWGGK...",
    "KSSKWWWGGWWWK...",
]

MASC_CORRE_A = MASC_NORMAL[:12] + _BRACOS_A + _BAIXO[:3] + _PERNAS_ABERTAS
MASC_CORRE_B = MASC_NORMAL[:12] + _BRACOS_B + _BAIXO[:3] + _PERNAS_ABERTAS

_CABECA_COSTAS = [
    ".....KKKKKK.....",
    "...KKCCCCCCKK...",
    "..KCcCCCCCCCCK..",
    "..KCCCCCCCCCCK..",
    "..KCCCCCCCCCCK..",
    "..KCCCCCCCCCCK..",
    "..KCCCCCCCCCCK..",
    "..KCCCCCCCCCCK..",
    "..KKCCCCCCCCKK..",
    "...KSSSSSSSSK...",
]
MASC_COSTAS = _CABECA_COSTAS + MASC_NORMAL[10:]
MASC_COSTAS_FELIZ = _CABECA_COSTAS + MASC_FELIZ[10:]

MASC_JOINHA = (
    MASC_FELIZ[:10]
    + MASC_NORMAL[10:12]
    + [l[:13] + "..." for l in MASC_NORMAL[12:17]]
    + MASC_NORMAL[17:]
)

GRADES = {
    "normal": MASC_NORMAL,
    "feliz": MASC_FELIZ,
    "triste": MASC_TRISTE,
    "corre_a": MASC_CORRE_A,
    "corre_b": MASC_CORRE_B,
    "corre_n": MASC_NORMAL,
    "costas": MASC_COSTAS,
    "costas_feliz": MASC_COSTAS_FELIZ,
    "joinha": MASC_JOINHA,
}
POSES_MAOS = ("feliz", "costas_feliz")

MASC_W = 16 * PX_MASCOTE
MASC_H = 25 * PX_MASCOTE
MX = 3 * PX_MASCOTE
LW = MASC_W + 2 * MX
LH = MASC_H

_cores_grade = {}


def colorir_grade(pose, abertos=True):
    chave = (pose, abertos)
    if chave in _cores_grade:
        return _cores_grade[chave]
    grade = GRADES[pose]
    n = len(grade)

    def tipo(j, i):
        if 0 <= j < n and 0 <= i < len(grade[j]):
            return grade[j][i]
        return "."

    def borda(j, i):
        return tipo(j, i) in ("K", ".")

    saida = []
    for j, linha in enumerate(grade):
        fila = []
        for i, c in enumerate(linha):
            cor = None
            if c == ".":
                cor = None
            elif c == "K":
                cor = SOMBRA
                for dj, di in ((-1, 0), (0, -1), (0, 1), (1, 0)):
                    v = tipo(j + dj, i + di)
                    if v in CONTORNOS:
                        cor = CONTORNOS[v]
                        break
            elif c in MATERIAIS:
                luz, base, sombra = MATERIAIS[c]
                e_cima, e_baixo = borda(j - 1, i), borda(j + 1, i)
                e_esq, e_dir = borda(j, i - 1), borda(j, i + 1)
                escura = e_baixo or e_dir
                clara = e_cima or e_esq
                if c == "S" and e_cima:
                    cor = sombra
                elif escura and clara:
                    cor = base
                elif escura:
                    cor = sombra
                elif clara:
                    cor = luz
                elif c == "W" and tipo(j, i + 1) == "G":
                    cor = misturar(base, sombra, 0.5)
                else:
                    cor = base
            elif c == "E" and not abertos:
                cor = MATERIAIS["S"][1]
            else:
                cor = PALETA_MASCOTE.get(c)
            fila.append(cor)
        saida.append(fila)
    _cores_grade[chave] = saida
    return saida


def regiao(j, i):
    if j <= 9:
        return "cabeca"
    if j >= 19:
        return "pernas"
    if 11 <= j <= 16 and (i <= 2 or i >= 13):
        return "bracos"
    return "tronco"


_camadas = {}


def camadas(pose, abertos=True):
    chave = (pose, abertos)
    if chave in _camadas:
        return _camadas[chave]
    p = PX_MASCOTE
    L = {n: pygame.Surface((LW, LH), pygame.SRCALPHA) for n in ("cabeca", "tronco", "bracos", "pernas", "maos")}
    for j, fila in enumerate(colorir_grade(pose, abertos)):
        for i, cor in enumerate(fila):
            if cor is not None:
                pygame.draw.rect(L[regiao(j, i)], cor, (MX + i * p, j * p, p, p))
    if pose in POSES_MAOS:
        ya = 3 * p
        sombra_w = MATERIAIS["W"][2]
        sombra_s = MATERIAIS["S"][2]
        for xa in (MX - 1 * p, MX + 14 * p):
            sup = L["maos"]
            pygame.draw.rect(sup, CONTORNOS["W"], (xa - p, ya, 4 * p, 10 * p))
            pygame.draw.rect(sup, BRANCO, (xa, ya + 2 * p, 2 * p, 8 * p))
            pygame.draw.rect(sup, sombra_w, (xa + p, ya + 2 * p, p, 8 * p))
            pygame.draw.rect(sup, PELE, (xa, ya, 2 * p, 2 * p))
            pygame.draw.rect(sup, sombra_s, (xa + p, ya, p, 2 * p))
    _camadas[chave] = L
    return L


_cache_comp = {}


def _compor_masc(pose, tr=0, cab=0, bra=0, mao=0, dxc=0, dxt=0, abertos=True, queda=0):
    chave = (pose, tr, cab, bra, mao, dxc, dxt, abertos, queda)
    img = _cache_comp.get(chave)
    if img is not None:
        return img
    L = camadas(pose, abertos)
    img = pygame.Surface((LW, LH), pygame.SRCALPHA)
    img.blit(L["pernas"], (0, 0))
    img.blit(L["tronco"], (dxt, tr))
    img.blit(L["bracos"], (dxt, bra))
    if pose in POSES_MAOS:
        img.blit(L["maos"], (dxt, mao))
    img.blit(L["cabeca"], (dxc, cab))
    if pose == "triste":
        p = PX_MASCOTE
        for col in (4, 11):
            pygame.draw.rect(img, AZUL_CLARO, (MX + col * p, 8 * p + queda, p, 2 * p))
    if len(_cache_comp) > 300:
        _cache_comp.clear()
    _cache_comp[chave] = img
    return img


def luz_mascote(cx):
    return (255, 255, 255), None


def aplicar_luz(img, mult, rim):
    if mult == (255, 255, 255) and rim is None:
        return img
    out = img.copy()
    if mult != (255, 255, 255):
        out.fill(mult, special_flags=pygame.BLEND_RGB_MULT)
    if rim is not None:
        cor, a, lado = rim
        m = pygame.mask.from_surface(img, 40)
        borda = pygame.mask.Mask(m.get_size())
        for d in (1, 2, 3):
            t = m.copy()
            t.erase(m, (-lado * d, 0))
            borda.draw(t, (0, 0))
        out.blit(borda.to_surface(setcolor=cor + (a,), unsetcolor=(0, 0, 0, 0)), (0, 0))
    return out


_cache_sombra = {}


def sombra_chao(cx, pes, altura=0):
    altura = max(0, altura)
    k = max(0.5, 1 - altura / 200)
    w = max(2, int(80 * k) // 2 * 2)
    h = max(2, int(16 * k) // 2 * 2)
    s = _cache_sombra.get((w, h))
    if s is None:
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (0, 0, 0, 96), (0, 0, w, h))
        _cache_sombra[(w, h)] = s
    tela.blit(s, (cx - w // 2, pes - h // 2))


_estado_masc = {}
_cache_masc = {}


def mascote(
    cx,
    pes,
    pose,
    t,
    dy=0,
    agach=0.0,
    inclina=0.0,
    escala=(1.0, 1.0),
    balanco=(0, 0, 0),
    fx=True,
    sombra=True,
    chave="m",
):
    agora = pygame.time.get_ticks()
    st = _estado_masc.get(chave)
    if st is None or agora - st["ult"] > 150:
        st = {"dy": dy, "ult": agora}
        _estado_masc[chave] = st
    st["ult"] = agora

    if fx and st["dy"] < -3 <= dy:
        soltar(cx, pes - 4, 8, POEIRA, vel=120, grav=-30, vida=(250, 450), tam=(4, 8))
    st["dy"] = dy

    abertos = not (pose in ("normal", "triste") and int(t * 1000) % 3600 < 140)
    queda = int((t * 40) % 4) * PX_MASCOTE if pose == "triste" else 0

    chave_c = ("m", pose, abertos, queda)
    img = _cache_masc.get(chave_c)
    if img is None:
        img = _compor_masc(pose, abertos=abertos, queda=queda)
        if len(_cache_masc) > 500:
            _cache_masc.clear()
        _cache_masc[chave_c] = img

    if sombra:
        sombra_chao(cx, pes, -dy)
    w, h = img.get_size()
    tela.blit(img, (cx - w // 2, pes + dy - h))


def mascote_giratorio(cx, pes, ang, pose="feliz", t=0.0, dy=0, profund=14):
    c, s = math.cos(ang), math.sin(ang)
    de_costas = c < 0
    if de_costas:
        p = "costas_feliz" if pose == "feliz" else "costas"
    else:
        p = pose
    mao = round(math.sin(t * 12) * 2) if pose == "feliz" else 0
    base = _compor_masc(p, mao=mao)
    w, h = base.get_size()
    larg = max(8, int(abs(c) * w) // 4 * 4)
    d = int(abs(s) * profund) // 2 * 2
    direcao = 1 if s > 0 else -1
    mult, rim = luz_mascote(cx)
    chave = ("giro", p, mao, larg, d, direcao, mult, rim)
    comp = _cache_masc.get(chave)
    if comp is None:
        frente = pygame.transform.scale(base, (larg, h))
        comp = pygame.Surface((larg + d, h), pygame.SRCALPHA)
        xf = 0 if direcao > 0 else d
        if d:
            lado_img = frente.copy()
            lado_img.fill((176, 182, 214), special_flags=pygame.BLEND_RGB_MULT)
            for i in range(d, 0, -2):
                comp.blit(lado_img, (xf + direcao * i, 0))
        comp.blit(frente, (xf, 0))
        comp = aplicar_luz(comp, mult, rim)
        if len(_cache_masc) > 500:
            _cache_masc.clear()
        _cache_masc[chave] = comp
    sombra_chao(cx, pes, -dy)
    tela.blit(comp, (cx - comp.get_width() // 2, pes + dy - h))


VOX = 5
PROF_VOX = {"cabeca": 6, "tronco": 5, "bracos": 3, "pernas": 4}
DMAX_VOX = 6
ELEV_VOX = 0.3
PASSO_VOX = 5
CW_VOX = 110
CH_VOX = LH + 40
_fatias_vox = {}


def _escurecer(cor, k):
    return tuple(int(v * k) for v in cor)


def fatias_voxel(pose):
    if pose in _fatias_vox:
        return _fatias_vox[pose]
    frente = colorir_grade(pose)
    tras = colorir_grade("costas_feliz" if pose == "feliz" else "costas")
    fatias = []
    for j, linha in enumerate(frente):
        s = pygame.Surface((len(linha) * VOX, DMAX_VOX * VOX), pygame.SRCALPHA)
        for i, cf in enumerate(linha):
            if cf is None:
                continue
            ct = tras[j][i] if j < len(tras) and i < len(tras[j]) and tras[j][i] is not None else cf
            d = PROF_VOX[regiao(j, i)]
            z0 = (DMAX_VOX - d) // 2
            for z in range(d):
                if z == d - 1:
                    cor = cf
                elif z == 0:
                    cor = _escurecer(ct, 0.8)
                else:
                    cor = _escurecer(cf if z >= d / 2 else ct, 0.92)
                pygame.draw.rect(s, cor, (i * VOX, (z0 + z) * VOX, VOX, VOX))
        fatias.append(s)
    _fatias_vox[pose] = fatias
    return fatias


def _montar_voxel(pose, graus):
    fatias = fatias_voxel(pose)
    n = len(fatias)
    sup = pygame.Surface((CW_VOX, CH_VOX), pygame.SRCALPHA)
    base_y = CH_VOX - 14
    for j in range(n - 1, -1, -1):
        rot = pygame.transform.rotate(fatias[j], graus)
        rw, rh = rot.get_size()
        rot = pygame.transform.scale(rot, (rw, max(1, int(rh * ELEV_VOX))))
        yc = base_y - (n - 1 - j) * PASSO_VOX
        x = CW_VOX // 2 - rw // 2
        y = yc - rot.get_height() // 2
        for k in range(PASSO_VOX - 1, -1, -1):
            sup.blit(rot, (x, y + k))
    return sup


def mascote_voxel(cx, pes, ang, pose="normal", dy=0):
    graus = int(math.degrees(ang)) % 360 // 5 * 5
    mult, rim = luz_mascote(cx)
    chave = ("vox", pose, graus, mult, rim)
    img = _cache_masc.get(chave)
    if img is None:
        img = aplicar_luz(_montar_voxel(pose, graus), mult, rim)
        if len(_cache_masc) > 500:
            _cache_masc.clear()
        _cache_masc[chave] = img
    sombra_chao(cx, pes, -dy)
    tela.blit(img, (cx - CW_VOX // 2, pes + dy - CH_VOX + 10))


PES_CORREDOR = CHAO_Y + 18
VEL_CORREDOR = 0.28
POEIRA = [(235, 225, 200), (205, 190, 160), BRANCO]

TIPOS_PASSADA = ["corre", "carro", "joia", "caixas", "teclado", "bichos", "cano_sai", "cano_entra"]
V_PASSADA = {"corre": 0.28, "carro": 0.6, "joia": 0.3, "caixas": 0.26, "teclado": 0.28, "bichos": 0.27}
MARGEM_TIPO = {"bichos": 330}
MARGEM_PASSADA = 170
PAUSA_PASSADA = 900
DISTANCIA_PULO = 260
ALTURA_PULO = 130
INTERVALO_CAIXA = 650
CAIXAS_MAX = 5
PIPE_ESQ = (CANOS_CENA[0][0] + 70, CANOS_CENA[0][1])
PIPE_DIR = (CANOS_CENA[1][0] + 70, CANOS_CENA[1][1])
FUMACA = [(150, 154, 166), (205, 208, 218), BRANCO]
PASSADA = {"tipo": "corre", "ini": 0, "dir": 1, "fila": [], "solo": True, "quadro": -1, "fumaca": 0}

ATOR = pygame.Surface((440, 720), pygame.SRCALPHA)
ATOR_CX, ATOR_PES = 220, 700

CAIXA_GRADE = [
    "KKKKKKKKKKKKKK",
    "KLLLLLTTLLLLLK",
    "KLLLLLTTLLLLLK",
    "KLLLLLTTLLLLLK",
    "KMMMMMTTMMMMMK",
    "KMMMMMMMMMMMMK",
    "KMMMMMMMMMMMMK",
    "KKKKKKKKKKKKKK",
]
SPR_CAIXA = sprite(
    CAIXA_GRADE,
    {"K": (92, 56, 24), "L": (222, 168, 96), "M": (180, 124, 64), "T": (240, 214, 150)},
    5,
)

LINHAS_TECLADO = [[(i, 1) for i in range(14)] for _ in range(4)] + [
    [(0, 1), (1, 1), (2, 1), (3, 8), (11, 1), (12, 1), (13, 1)]
]

NOMES_CARRO = ["carro_jogo.png", "carro.png"]
LARGURA_CARRO = 222
PRETO_RODA = (24, 26, 38)
ARO_RODA = (150, 156, 176)
_carro = {"img": None, "carregado": False, "rodas": [], "raio": 15}


def carro_sprite():
    if not _carro["carregado"]:
        _carro["carregado"] = True
        img = None
        for pasta in (PASTA, PASTA_IMG):
            for nome in NOMES_CARRO:
                img = abrir_imagem(os.path.join(pasta, nome))
                if img is not None:
                    break
            if img is not None:
                break
        if img is None:
            print("AVISO: carro_jogo.png nao encontrado em", PASTA)
            img = pygame.Surface((LARGURA_CARRO, 105), pygame.SRCALPHA)
            pygame.draw.rect(img, BRANCO, (0, 10, LARGURA_CARRO, 70), border_radius=12)
        else:
            caixa = img.get_bounding_rect()
            if caixa.w > 0 and caixa.h > 0:
                img = img.subsurface(caixa).copy()
            if img.get_width() != LARGURA_CARRO:
                h = round(img.get_height() * LARGURA_CARRO / img.get_width())
                img = escalar(img, (LARGURA_CARRO, h))
        w, h = img.get_size()
        _carro["img"] = img
        _carro["rodas"] = [(round(w * 0.189), round(h * 0.848)), (round(w * 0.815), round(h * 0.848))]
        _carro["raio"] = max(4, round(w * 0.0676))
    return _carro["img"]


def desenhar_roda_carro(sup, cx, cy, ang):
    r = _carro["raio"]
    pygame.draw.circle(sup, PRETO_RODA, (cx, cy), r)
    pygame.draw.circle(sup, (70, 76, 96), (cx, cy), r - 5)
    for k in range(3):
        a = ang + k * math.pi / 3
        dx, dy = math.cos(a) * (r - 5), math.sin(a) * (r - 5)
        pygame.draw.line(sup, ARO_RODA, (cx - dx, cy - dy), (cx + dx, cy + dy), 2)
    pygame.draw.circle(sup, ARO_RODA, (cx, cy), 2)


def arco_iris(h):
    return (
        int(150 + 105 * math.sin(h)),
        int(150 + 105 * math.sin(h + 2.094)),
        int(150 + 105 * math.sin(h + 4.189)),
    )


JOINHA_GRADE = [
    "...KKKK...",
    "..KSSSSK..",
    "..KSLSSK..",
    "..KSLSSK..",
    "..KSSSSK..",
    "KKKKSSSKKK",
    "KSLSSSSSSK",
    "KDDDDDDDSK",
    "KSLSSSSSSK",
    "KDDDDDDDSK",
    "KSLSSSSSSK",
    "KDDDDDDDSK",
    "KSSSSSSSSK",
    ".KKKKKKKK.",
]
JOINHA_CORES = {"K": CONTORNOS["S"], "S": PELE, "L": MATERIAIS["S"][0], "D": MATERIAIS["S"][2]}
SPR_JOINHA = sprite(JOINHA_GRADE, JOINHA_CORES, 2)
SPR_JOINHA_ESPELHO = pygame.transform.flip(SPR_JOINHA, True, False)


def desenhar_joias(cx, topo, t):
    sobe = round(math.sin(t * 10) * 2)
    alt = SPR_JOINHA.get_height()
    base = topo + 27 + sobe
    tela.blit(SPR_JOINHA, (cx - 50, base - alt))
    tela.blit(SPR_JOINHA_ESPELHO, (cx + 30, base - alt))


def desenhar_caixas(cx, topo, ms, t):
    n = min(CAIXAS_MAX, 1 + ms // INTERVALO_CAIXA)
    for k in range(n):
        tk = ms - k * INTERVALO_CAIXA
        queda = 0
        if k > 0 and tk < 240:
            queda = -round((1 - tk / 240) ** 2 * 560)
        balanco = round(math.sin(t * 6 + k * 1.1) * (1 + k * 1.2))
        tela.blit(SPR_CAIXA, (cx - 35 + balanco, topo - (k + 1) * 40 + queda))


TECLADO_W, TECLADO_H = 152, 58
TECLADO_FILAS = [
    [1] * 14,
    [1] * 14,
    [1.5] + [1] * 11 + [1.5],
    [1.75] + [1] * 10 + [2.25],
    [2, 1, 1, 6, 1, 1, 2],
]


def _escuro(cor, k):
    return tuple(int(v * k) for v in cor)


def desenhar_teclado(cx, topo, t):
    kx, ky = cx - TECLADO_W // 2, topo
    W, H = TECLADO_W, TECLADO_H

    gw, gh = W + 44, H + 44
    brilho = pygame.Surface((gw, gh), pygame.SRCALPHA)
    pulso = 0.75 + 0.25 * math.sin(t * 6)
    for k, a in enumerate((22, 34, 48)):
        m = 22 - k * 7
        pygame.draw.rect(
            brilho, arco_iris(t * 3) + (int(a * pulso),), (m, m, gw - 2 * m, gh - 2 * m), border_radius=14
        )
    tela.blit(brilho, (kx - 22, ky - 22))

    cy0 = ky + H // 2
    px = py = 0
    for k in range(18):
        x = kx - 4 - k * 4
        y = cy0 + round(math.sin(t * 8 + k * 0.7) * (2 + k * 0.35))
        pygame.draw.rect(tela, (10, 12, 22), (x - 1, y - 1, 6, 6))
        px, py = x, y
    for k in range(18):
        x = kx - 4 - k * 4
        y = cy0 + round(math.sin(t * 8 + k * 0.7) * (2 + k * 0.35))
        if (k - int(t * 14)) % 6 == 0:
            cor = arco_iris(t * 6 - k * 0.5)
        else:
            cor = (70, 76, 100)
        pygame.draw.rect(tela, cor, (x, y, 4, 4))
    pygame.draw.rect(tela, (10, 12, 22), (px - 9, py - 3, 10, 10))
    pygame.draw.rect(tela, (180, 186, 204), (px - 8, py - 2, 8, 8))
    pygame.draw.rect(tela, (60, 66, 90), (px - 6, py, 2, 4))
    pygame.draw.rect(tela, (60, 66, 90), (px - 3, py, 2, 4))

    pygame.draw.rect(tela, (10, 12, 22), (kx - 4, ky - 4, W + 8, H + 8))
    for x in range(0, W + 8, 6):
        cor = arco_iris(t * 4 + x * 0.06)
        pygame.draw.rect(tela, cor, (kx - 4 + x, ky - 4, min(6, W + 8 - x), 3))
        pygame.draw.rect(tela, cor, (kx - 4 + x, ky + H + 1, min(6, W + 8 - x), 3))
    for y in range(0, H + 8, 6):
        cor = arco_iris(t * 4 + y * 0.06 + 3)
        pygame.draw.rect(tela, cor, (kx - 4, ky - 4 + y, 3, min(6, H + 8 - y)))
        pygame.draw.rect(tela, cor, (kx + W + 1, ky - 4 + y, 3, min(6, H + 8 - y)))
    pygame.draw.rect(tela, (30, 34, 52), (kx - 1, ky - 1, W + 2, H + 2))
    pygame.draw.rect(tela, (84, 92, 128), (kx - 1, ky - 1, W + 2, 2))
    pygame.draw.rect(tela, (84, 92, 128), (kx - 1, ky - 1, 2, H + 2))
    pygame.draw.rect(tela, (16, 18, 32), (kx - 1, ky + H - 2, W + 2, 3))
    pygame.draw.rect(tela, (16, 18, 32), (kx + W - 1, ky - 1, 2, H + 2))
    pygame.draw.rect(tela, (18, 20, 34), (kx + 3, ky + 3, W - 6, H - 6))

    for j, fila in enumerate(TECLADO_FILAS):
        x = kx + 6
        for i, u in enumerate(fila):
            w = int(u * 10) - 2
            base = arco_iris(t * 3 + (x - kx) * 0.045 + j * 0.7)
            apertada = ((int(t * 11) + i * 5 + j * 3) * 7919) % 13 == 0
            y0 = ky + 5 + j * 10
            if apertada:
                topo_c = misturar(base, BRANCO, 0.6)
                yt = y0 + 2
            else:
                topo_c = base
                yt = y0
                pygame.draw.rect(tela, _escuro(base, 0.5), (x, y0 + 7, w, 2))
            pygame.draw.rect(tela, topo_c, (x, yt, w, 7))
            pygame.draw.rect(tela, misturar(topo_c, BRANCO, 0.45), (x + 1, yt, w - 2, 1))
            pygame.draw.rect(tela, _escuro(topo_c, 0.7), (x, yt + 6, w, 1))
            if u <= 2:
                pygame.draw.rect(tela, _escuro(topo_c, 0.45), (x + w // 2 - 1, yt + 3, 2, 2))
            else:
                pygame.draw.rect(tela, _escuro(topo_c, 0.55), (x + 6, yt + 3, w - 12, 2))
            x += int(u * 10)

    for hx in (kx - 11, kx + W - 3):
        pygame.draw.rect(tela, CONTORNOS["S"], (hx, ky + 16, 14, 14))
        pygame.draw.rect(tela, PELE, (hx + 2, ky + 18, 10, 10))

    for n in range(4):
        ciclo = (t * 1.3 + n * 0.25) % 1.0
        sx = kx + 18 + n * 38 + round(math.sin(t * 3 + n * 2) * 6)
        sy = ky - 8 - round(ciclo * 34)
        r = max(1, round(4 * (1 - ciclo)))
        cor = misturar(arco_iris(t * 4 + n), BRANCO, 0.5)
        pygame.draw.rect(tela, cor, (sx, sy - r, 2, 2 * r + 2))
        pygame.draw.rect(tela, cor, (sx - r, sy, 2 * r + 2, 2))


ESC_POMBO = 5
ALTURA_PAVAO = 124
POMBOS_OFFSET = (95, 165)
PAVAO_OFFSET = -125
_bichos = {"carregado": False, "pavao": None, "pombos": []}


def _achar_imagem(nome):
    for pasta in (PASTA_IMG, PASTA):
        img = abrir_imagem(os.path.join(pasta, nome))
        if img is not None:
            return img
    return None


def bichos_sprites():
    if not _bichos["carregado"]:
        _bichos["carregado"] = True
        pav = _achar_imagem("pavao_jogo.png")
        if pav is not None:
            esc = ALTURA_PAVAO / pav.get_height()
            pav = escalar(pav, (pav.get_width() * esc, ALTURA_PAVAO))
            pav = pygame.transform.flip(pav, True, False)
        else:
            print("AVISO: pavao_jogo.png nao encontrado em", PASTA_IMG)
        _bichos["pavao"] = pav
        folha = _achar_imagem("pombos_jogo.png")
        quadros = []
        if folha is not None:
            w = folha.get_width() // 4
            for i in range(4):
                q = folha.subsurface((i * w, 0, w, folha.get_height())).copy()
                q = pygame.transform.scale(q, (w * ESC_POMBO, folha.get_height() * ESC_POMBO))
                quadros.append(pygame.transform.flip(q, True, False))
        else:
            print("AVISO: pombos_jogo.png nao encontrado em", PASTA_IMG)
        _bichos["pombos"] = quadros
    return _bichos


def pulo_pombo(ms, k):
    return -round(abs(math.sin(ms / 150 + k * 1.7)) * 18)


def desenhar_bichos(cx, pes, ms):
    b = bichos_sprites()
    pav = b["pavao"]
    if pav is not None:
        dy = -6 if (ms // 110) % 2 else 0
        tela.blit(pav, (cx + PAVAO_OFFSET - pav.get_width() // 2, pes + dy - pav.get_height()))
    if b["pombos"]:
        for k, off in enumerate(POMBOS_OFFSET):
            q = b["pombos"][0 if (ms // 130 + k) % 2 == 0 else 2]
            tela.blit(q, (cx + off - q.get_width() // 2, pes + pulo_pombo(ms, k) - q.get_height()))


MOEDA_VOLTA = [0] * len(MOEDAS_CENA)
INTERVALO_MOEDA = 1500
RAIO_PEGAR_MOEDA = 30


def coletar_moedas(tipo, s):
    if tipo not in ("cano_sai", "cano_entra") or s["solo"] or s["clip"] is not None:
        return
    agora = pygame.time.get_ticks()
    for i, (mx, my, _) in enumerate(MOEDAS_CENA):
        if agora < MOEDA_VOLTA[i] or abs(s["x"] - mx) > RAIO_PEGAR_MOEDA:
            continue
        lado = [j for j, m in enumerate(MOEDAS_CENA) if (m[0] < LARGURA / 2) == (mx < LARGURA / 2)]
        ultimo = max([agora] + [MOEDA_VOLTA[j] for j in lado])
        MOEDA_VOLTA[i] = ultimo + INTERVALO_MOEDA
        soltar(mx, my, 14, DOURADOS, vel=200, grav=300, vida=(300, 600), tam=(4, 8))
        tocar("combo")


def estado_ator(x, y, pose, dy=0, clip=None, solo=True, fim=False):
    return {"x": x, "y": y, "pose": pose, "dy": dy, "clip": clip, "solo": solo, "fim": fim}


def saiu(x, d, m=MARGEM_PASSADA):
    return x > LARGURA + m if d > 0 else x < -m


def situacao(tipo, d, ms):
    chao = PES_CORREDOR
    quadro = (ms // 110) % 4
    corrida = ("corre_a", "corre_n", "corre_b", "corre_n")[quadro]
    dy_corrida = -8 if quadro % 2 else 0
    margem = MARGEM_TIPO.get(tipo, MARGEM_PASSADA)
    inicio = -margem if d > 0 else LARGURA + margem
    v = V_PASSADA["corre"]
    if tipo in V_PASSADA:
        x = inicio + d * V_PASSADA[tipo] * ms
        return estado_ator(x, chao, corrida, dy_corrida, fim=saiu(x, d, margem))
    if tipo == "cano_sai":
        px, topo = PIPE_ESQ if d > 0 else PIPE_DIR
        if ms < 1000:
            q = 1 - (1 - ms / 1000) ** 2
            return estado_ator(px, topo + 140 * (1 - q), "normal", clip=topo, solo=False)
        if ms < 1350:
            return estado_ator(px, topo, "feliz", solo=False)
        if ms < 2150:
            q = (ms - 1350) / 800
            y = topo + (chao - topo) * q - math.sin(q * math.pi) * ALTURA_PULO
            return estado_ator(px + d * DISTANCIA_PULO * q, y, "feliz", solo=False)
        x = px + d * (DISTANCIA_PULO + v * (ms - 2150))
        return estado_ator(x, chao, corrida, dy_corrida, fim=saiu(x, d))
    px, topo = PIPE_DIR if d > 0 else PIPE_ESQ
    x0 = px - d * DISTANCIA_PULO
    t1 = abs(x0 - inicio) / v
    if ms < t1:
        return estado_ator(inicio + d * v * ms, chao, corrida, dy_corrida)
    m = ms - t1
    if m < 800:
        q = m / 800
        y = chao + (topo - chao) * q - math.sin(q * math.pi) * ALTURA_PULO
        return estado_ator(x0 + d * DISTANCIA_PULO * q, y, "feliz", solo=False)
    m -= 800
    if m < 450:
        return estado_ator(px, topo, "feliz", solo=False)
    m -= 450
    if m < 1000:
        q = m / 1000
        return estado_ator(px, topo + 140 * q * q, "normal", clip=topo, solo=False)
    return estado_ator(px, topo + 140, "normal", clip=topo, solo=False, fim=True)


def nova_passada(inicio):
    if not PASSADA["fila"]:
        fila = list(TIPOS_PASSADA)
        random.shuffle(fila)
        if fila[-1] == PASSADA["tipo"]:
            fila[0], fila[-1] = fila[-1], fila[0]
        PASSADA["fila"] = fila
    PASSADA.update(
        tipo=PASSADA["fila"].pop(),
        dir=-PASSADA["dir"],
        ini=inicio,
        solo=True,
        quadro=-1,
        fumaca=0,
    )


def emitir_poeira(tipo, d, ms, s):
    anterior = PASSADA["solo"]
    PASSADA["solo"] = s["solo"]
    if s["solo"] and not anterior:
        soltar(s["x"], s["y"] - 4, 12, POEIRA, vel=140, grav=-40, vida=(250, 500), tam=(4, 9))
    if not s["solo"]:
        return
    if tipo == "carro":
        if ms // 90 != PASSADA["fumaca"]:
            PASSADA["fumaca"] = ms // 90
            soltar(s["x"] - d * 115, s["y"] - 18, 2, FUMACA, vel=50, grav=-80, vida=(300, 600), tam=(5, 10))
        return
    quadro = (ms // 110) % 4
    if quadro in (0, 2) and quadro != PASSADA["quadro"]:
        soltar(s["x"] - d * 22, s["y"] - 4, 3, POEIRA, vel=70, grav=-60, vida=(250, 450), tam=(4, 8))
    PASSADA["quadro"] = quadro


def desenhar_passada(tipo, d, ms, s):
    global tela
    t = ms / 1000
    original = tela
    tela = ATOR
    try:
        ATOR.fill((0, 0, 0, 0))
        cx, pes = ATOR_CX, ATOR_PES
        pose, dy = s["pose"], s["dy"]
        if tipo == "carro":
            dyb = -1 if (ms // 90) % 2 else 0
            img = carro_sprite()
            ox = cx - img.get_width() // 2
            oy = pes - img.get_height() + 2 + dyb
            tela.blit(img, (ox, oy))
            ang = ms * 0.02
            for rx, ry in _carro["rodas"]:
                desenhar_roda_carro(tela, ox + rx, oy + ry, ang)
        elif tipo in ("joia", "caixas"):
            dy = -6 if (ms // 140) % 2 else 0
            mascote(cx, pes, "feliz", t, dy, fx=False, sombra=False, chave="corredor")
            topo = pes + dy - MASC_H
            if tipo == "joia":
                desenhar_joias(cx, topo, t)
            else:
                desenhar_caixas(cx, topo, ms, t)
        elif tipo == "bichos":
            dy = -6 if (ms // 140) % 2 else 0
            mascote(cx, pes, "feliz", t, dy, fx=False, sombra=False, chave="corredor")
            desenhar_bichos(cx, pes, ms)
        else:
            mascote(cx, pes, pose, t, dy, fx=False, sombra=False, chave="corredor")
            if tipo == "teclado":
                desenhar_teclado(cx, pes + dy - 79, t)
    finally:
        tela = original
    imagem = ATOR if d > 0 else pygame.transform.flip(ATOR, True, False)
    x, y = int(s["x"]), int(s["y"])
    if s["solo"]:
        if tipo == "carro":
            sombra_chao(x - 55, y)
            sombra_chao(x + 55, y)
        elif tipo == "bichos":
            sombra_chao(x, y)
            sombra_chao(x + d * PAVAO_OFFSET, y)
            for k, off in enumerate(POMBOS_OFFSET):
                sombra_chao(x + d * off, y, -pulo_pombo(ms, k))
        else:
            sombra_chao(x, y)
    if s["clip"] is not None:
        tela.set_clip((0, 0, LARGURA, s["clip"]))
    tela.blit(imagem, (x - ATOR_CX, y - ATOR_PES))
    tela.set_clip(None)


def montar_bandeira():
    baixa = pygame.Surface((48, 32))
    baixa.fill(NAVY_TEUTO)
    pygame.draw.rect(baixa, AZUL_CLARO, (0, 0, 48, 32), 1)
    pygame.draw.rect(baixa, BRANCO, (6, 4, 36, 4))
    pygame.draw.rect(baixa, BRANCO, (2, 11, 44, 10))
    pygame.draw.rect(baixa, BRANCO, (6, 24, 36, 4))
    letras = FONTE.render("TEUTO", False, NAVY_TEUTO)
    baixa.blit(letras, (24 - letras.get_width() // 2, 16 - letras.get_height() // 2))
    return pygame.transform.scale(baixa, (192, 128))


SPR_BANDEIRA = montar_bandeira()
SPR_BANDEIRA_G = pygame.transform.scale(SPR_BANDEIRA, (336, 224))


def desenhar_bandeira(x, y, t, sup=None, fatia=8):
    if sup is None:
        sup = SPR_BANDEIRA
    larg, alt = sup.get_size()
    for i in range(0, larg, fatia):
        off = round(math.sin(t * 5 + i * 0.05) * 3 * (i / larg + 0.2))
        tela.blit(sup, (x + i, y + off), (i, 0, fatia, alt))


def mastro(x, topo, base):
    pygame.draw.rect(tela, SOMBRA, (x - 6, topo, 12, base - topo))
    pygame.draw.rect(tela, BRANCO, (x - 4, topo, 8, base - topo))
    pygame.draw.circle(tela, SOMBRA, (x, topo - 4), 12)
    pygame.draw.circle(tela, AMARELO, (x, topo - 4), 9)
    pygame.draw.rect(tela, SOMBRA, (x - 22, base - 14, 44, 14))
    pygame.draw.rect(tela, (150, 156, 176), (x - 20, base - 12, 40, 10))


hover = {}


def suave(chave, alvo, vel=0.25):
    v = hover.get(chave, 0.0)
    v += (alvo - v) * vel
    if abs(alvo - v) < 0.02:
        v = alvo
    hover[chave] = v
    return v


def misturar(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def botao(rect, rotulo, mouse, escala=3, destaque=False, ativo=False):
    r = pygame.Rect(rect)
    sobre = r.collidepoint(mouse) or ativo
    if destaque:
        normal = (LIMAO, AZUL_ESCURO, BRANCO)
    else:
        normal = (AZUL, BRANCO, AZUL_CLARO)
    k = suave(("botao", tuple(r), rotulo), 1.0 if sobre else 0.0)
    cor_fundo = misturar(normal[0], AZUL_CLARO, k)
    cor_txt = misturar(normal[1], AZUL_ESCURO, k)
    borda = misturar(normal[2], BRANCO, k)
    pygame.draw.rect(tela, SOMBRA, r.move(6, 6), border_radius=RAIO_BOTAO)
    pygame.draw.rect(tela, cor_fundo, r, border_radius=RAIO_BOTAO)
    pygame.draw.rect(tela, borda, r, 4, border_radius=RAIO_BOTAO)
    s = superficie_texto(rotulo, escala, cor_txt)
    tela.blit(s, (r.centerx - s.get_width() // 2, r.centery - s.get_height() // 2))


def desenhar_coracao(x, y, cheio, cor=None):
    if cor is None:
        cor = VERMELHO if cheio else VERMELHO_APAGADO
    for j, linha in enumerate(CORACAO):
        for i, c in enumerate(linha):
            if c == "1":
                pygame.draw.rect(tela, cor, (x + i * 5, y + j * 5, 5, 5))


def desenhar_vidas(vidas, perdas, ganhos, agora):
    recentes = [i for i, ini in perdas.items() if agora - ini < 700]
    n = max([VIDAS_INICIAIS, vidas] + [i + 1 for i in recentes])
    for i in range(n):
        x = 40 + i * 50
        if i >= vidas and i in perdas and agora - perdas[i] < 700:
            k = (agora - perdas[i]) // 100
            cor = BRANCO if k % 2 == 0 else VERMELHO
            desenhar_coracao(x + round(math.sin(agora / 25) * 3), 30, True, cor)
        elif i < vidas:
            dy = 0
            if i in ganhos and agora - ganhos[i] < 800:
                dy = onda((agora - ganhos[i]) / 1000, 24)
            desenhar_coracao(x, 30 + dy, True)
        elif i < VIDAS_INICIAIS:
            desenhar_coracao(x, 30, False)


def clique(e):
    return transicao is None and e.type == pygame.MOUSEBUTTONDOWN and e.button == 1


def eventos():
    lista = pygame.event.get()
    for e in lista:
        if e.type == pygame.QUIT:
            sair()
    return lista


def sair():
    pygame.quit()
    sys.exit()


def carregar_sons():
    sons.clear()
    for chave, _ in EVENTOS_SOM:
        nome = cfg["audio"].get(chave, "")
        if not nome:
            continue
        try:
            s = pygame.mixer.Sound(os.path.join(PASTA_AUDIO, nome))
            s.set_volume(cfg["volume"])
            sons[chave] = s
        except Exception:
            pass


musica_atual = None
musica_len = None
musica_ult_loop = 0
ANTECIPA_LOOP = 2.0
cache_duracao = {}


def duracao_audio(caminho):
    if caminho not in cache_duracao:
        try:
            cache_duracao[caminho] = pygame.mixer.Sound(caminho).get_length()
        except Exception:
            cache_duracao[caminho] = None
    return cache_duracao[caminho]


def tocar_musica(tipo, forcar=False):
    global musica_atual, musica_len, musica_ult_loop
    if tipo == musica_atual and not forcar:
        return
    musica_atual = tipo
    musica_len = None
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass
    if tipo is None:
        return
    nome = cfg.get("musica_" + tipo, "")
    if not nome:
        return
    try:
        caminho = os.path.join(PASTA_AUDIO, nome)
        dur = duracao_audio(caminho)
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(cfg["volume"])
        if dur and dur > ANTECIPA_LOOP * 3:
            musica_len = dur
            musica_ult_loop = pygame.time.get_ticks()
            pygame.mixer.music.play(0)
        else:
            pygame.mixer.music.play(-1)
    except Exception:
        musica_len = None


def atualizar_musica():
    global musica_ult_loop
    if musica_atual is None or not musica_len:
        return
    agora = pygame.time.get_ticks()
    if agora - musica_ult_loop < 1500:
        return
    try:
        pos = pygame.mixer.music.get_pos()
        if pos < 0 or pos >= (musica_len - ANTECIPA_LOOP) * 1000 or not pygame.mixer.music.get_busy():
            musica_ult_loop = agora
            pygame.mixer.music.play(0)
    except pygame.error:
        pass


def parar_musica():
    tocar_musica(None)


def aplicar_volume():
    for s in sons.values():
        s.set_volume(cfg["volume"])
    for s in sinteticos.values():
        s.set_volume(cfg["volume"])
    try:
        pygame.mixer.music.set_volume(cfg["volume"])
    except pygame.error:
        pass


def tocar(chave):
    s = sons.get(chave) or sinteticos.get(chave)
    if not s:
        return
    try:
        if chave in ("vitoria", "derrota"):
            pygame.mixer.stop()
        s.play()
    except pygame.error:
        pass


def escolher_arquivo(titulo, filtros, pasta):
    try:
        import tkinter
        from tkinter import filedialog

        raiz = tkinter.Tk()
        raiz.withdraw()
        raiz.attributes("-topmost", True)
        origem = filedialog.askopenfilename(title=titulo, filetypes=filtros)
        raiz.destroy()
    except Exception:
        return ""
    if not origem:
        return ""
    os.makedirs(pasta, exist_ok=True)
    nome = os.path.basename(origem)
    destino = os.path.join(pasta, nome)
    if os.path.abspath(origem) != os.path.abspath(destino):
        shutil.copy(origem, destino)
    return nome


def escolher_audio():
    return escolher_arquivo(
        "Escolha o arquivo de áudio",
        [("Áudio", "*.wav *.ogg *.mp3"), ("Todos", "*.*")],
        PASTA_AUDIO,
    )


def escolher_imagem():
    return escolher_arquivo(
        "Escolha a imagem",
        [("Imagens", "*.png *.jpg *.jpeg *.bmp *.webp"), ("Todos", "*.*")],
        PASTA_IMG,
    )


def proxima_receita():
    global fila
    if not receitas:
        return None
    if not fila:
        fila = list(receitas)
        random.shuffle(fila)
    return fila.pop()


def multiplicador(c):
    return 1 + min(3, c // 2)


def tela_mensagem(msg, destino):
    r = pygame.Rect(LARGURA // 2 - 200, 420, 400, 64)
    while True:
        mouse = pos_mouse()
        for e in eventos():
            if clique(e) and r.collidepoint(mouse):
                return destino
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "menu"
        fundo()
        texto_sombra(msg, 3, BRANCO, LARGURA // 2, 300, "centro")
        botao(r, "OK", mouse, 3)
        apresentar()
        relogio.tick(60)


MENU_ITENS = [
    ("JOGAR", "jogar"),
    ("COMO JOGAR", "como"),
    ("RANKING", "ranking"),
    ("CONFIGURAÇÕES", "config"),
    ("CADASTRAR RECEITA", "cadastro"),
    ("TELA INICIAL", "abertura"),
    ("SAIR", "sair"),
]
MENU_RETS = [pygame.Rect(LARGURA // 2 - 280, 288 + i * 57, 560, 48) for i in range(len(MENU_ITENS))]
BANNER_SUP = pygame.Surface((880, 230), pygame.SRCALPHA)
pygame.draw.rect(BANNER_SUP, (16, 34, 64, 200), (0, 0, 880, 230), border_radius=28)
PLACA_SUP = pygame.Surface((720, 210), pygame.SRCALPHA)
pygame.draw.rect(PLACA_SUP, (16, 34, 64, 195), (0, 0, 720, 210), border_radius=24)


def desenhar_banner(ms=None):
    tela.blit(BANNER_SUP, (200, 50))
    texto_sombra("SEMANA DA QUALIDADE", 3, AZUL_CLARO, LARGURA // 2, 100, "centro")
    if ms is None:
        texto_sombra("MONTE A RECEITA", 7, BRANCO, LARGURA // 2, 170, "centro")
    else:
        texto_onda("MONTE A RECEITA", 7, BRANCO, LARGURA // 2, 170, ms, 150, 45, True)

def desenhar_titulo(ms):
    texto_sombra("SEMANA DA QUALIDADE", 3, AZUL_CLARO, LARGURA // 2, 100, "centro")
    texto_onda("MONTE A RECEITA", 7, BRANCO, LARGURA // 2, 170, ms, 150, 45, True)

def desenhar_seta(x, y, cor):
    for j in range(7):
        w = (4 - abs(j - 3)) * 8
        pygame.draw.rect(tela, cor, (x, y + j * 4, w, 4))


def desenhar_menu(mouse):
    desenhar_banner()
    for i, (r, (rotulo, _)) in enumerate(zip(MENU_RETS, MENU_ITENS)):
        botao(r, rotulo, (-999, -999), 3, ativo=(i == menu_sel))
    r = MENU_RETS[menu_sel]
    if (pygame.time.get_ticks() // 300) % 2 == 0:
        desenhar_seta(r.x - 52, r.centery - 14, LIMAO)


def abertura():
    ini = pygame.time.get_ticks()
    PASSADA.update(tipo="corre", ini=ini, dir=1, fila=[], solo=True, quadro=-1, fumaca=0)
    del particulas[:]
    while True:
        agora = pygame.time.get_ticks()
        ms_c = agora - ini
        ms_p = agora - PASSADA["ini"]
        tipo, d = PASSADA["tipo"], PASSADA["dir"]
        s = None
        if ms_p >= 0:
            s = situacao(tipo, d, ms_p)
            if s["fim"]:
                nova_passada(agora + PAUSA_PASSADA)
                s = None
            else:
                emitir_poeira(tipo, d, ms_p, s)
                coletar_moedas(tipo, s)
        atualizar_particulas()
        for e in eventos():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sair()
                if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    tocar("selecionar")
                    return "menu"
            elif clique(e):
                tocar("selecionar")
                return "menu"
        fundo(True, True)
        if s is not None:
            desenhar_passada(tipo, d, ms_p, s)
        desenhar_particulas()
        tela.blit(BANNER_SUP, (280 - 80, 50))
        tela.blit(PLACA_SUP, (280, 380))
        desenhar_titulo(ms_c)
        if ms_c > 1500 and (agora // 450) % 2 == 0:
            texto_sombra("APERTE START", 4, LIMAO, LARGURA // 2, 412, "centro")
        if ranking:
            melhor = ranking[0]
            linha = f"HI-SCORE {melhor['pontos']:06d} {melhor['nome']}"
        else:
            linha = "HI-SCORE 000000 ---"
        texto_sombra(linha, 2, BRANCO, LARGURA // 2, 500, "centro")
        texto_sombra("UPP-1  -  TEUTO", 2, AZUL_CLARO, LARGURA // 2, 546, "centro")
        apresentar()
        relogio.tick(60)


def menu():
    global menu_sel
    historico = []
    ultima_acao = pygame.time.get_ticks()
    while True:
        mouse = pos_mouse()
        lista = eventos()
        agora = pygame.time.get_ticks()
        if any(e.type in (pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN) for e in lista):
            ultima_acao = agora
        if agora - ultima_acao >= TEMPO_OCIOSO:
            return "abertura"
        for e in lista:
            if e.type == pygame.MOUSEMOTION:
                for i, r in enumerate(MENU_RETS):
                    if r.collidepoint(mouse):
                        menu_sel = i
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_DOWN):
                    passo = -1 if e.key == pygame.K_UP else 1
                    menu_sel = (menu_sel + passo) % len(MENU_ITENS)
                    tocar("mover")
                    historico.append(e.key)
                    historico = historico[-len(CODIGO_SECRETO):]
                    if historico == CODIGO_SECRETO:
                        tocar("recorde")
                        return "creditos"
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    tocar("selecionar")
                    return MENU_ITENS[menu_sel][1]
                else:
                    historico = []
            elif clique(e):
                for i, r in enumerate(MENU_RETS):
                    if r.collidepoint(mouse):
                        menu_sel = i
                        tocar("selecionar")
                        return MENU_ITENS[i][1]
        fundo()
        desenhar_menu(mouse)
        apresentar()
        relogio.tick(60)


def como_jogar():
    passos = [
        "Clique em JOGAR e o jogo sorteia uma receita de fabricação.",
        "As etapas da receita aparecem embaralhadas do lado direito.",
        "Clique nas etapas na ordem correta de fabricação. Também dá para usar as setas CIMA e BAIXO e confirmar com ENTER ou ESPAÇO.",
        f"Cada acerto vale {PONTOS_ACERTO} pontos. Acertos seguidos formam COMBO e multiplicam os pontos.",
        f"Cada erro custa uma vida. Você começa com {VIDAS_INICIAIS} vidas.",
        f"A cada {ACERTOS_POR_VIDA} acertos você ganha uma vida extra (máximo de {VIDAS_MAX}).",
        f"Termine rápido: o bônus de tempo vale até {BONUS_TEMPO_MAX} pontos. Sem erros, ganha {BONUS_PERFEITO} de PERFEITO.",
        "Se as vidas acabarem, aperte CONTINUAR antes da contagem chegar a zero.",
        "Os melhores jogadores entram no RANKING com 3 iniciais.",
        "Aperte ESC a qualquer momento para voltar ao menu.",
    ]
    blocos = [(n, quebrar(passo, 2, 1060)) for n, passo in enumerate(passos, 1)]
    total_chars = sum(len(l) for _, ls in blocos for l in ls)
    r_voltar = pygame.Rect(LARGURA // 2 - 140, 630, 280, 60)
    ini = pygame.time.get_ticks()
    pulou = False
    while True:
        mouse = pos_mouse()
        agora = pygame.time.get_ticks()
        n_chars = 10**6 if pulou else int((agora - ini) * 0.06)
        for e in eventos():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "menu"
                if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    if n_chars < total_chars:
                        pulou = True
                    else:
                        return "menu"
            elif clique(e):
                if r_voltar.collidepoint(mouse):
                    tocar("selecionar")
                    return "menu"
                pulou = True
        fundo()
        texto_sombra("COMO JOGAR", 5, BRANCO, LARGURA // 2, 50, "centro")
        y = 140
        restante = n_chars
        for n, ls in blocos:
            for k, linha in enumerate(ls):
                antes = restante
                vis = linha[: max(0, antes)]
                restante = antes - len(linha)
                if k == 0 and antes > 0:
                    texto(f"{n}.", 2, AZUL_CLARO, 100, y)
                if vis:
                    texto(vis, 2, BRANCO, 150, y)
                if antes > 0 and restante <= 0 and n_chars < total_chars:
                    if (agora // 250) % 2 == 0:
                        pygame.draw.rect(tela, LIMAO, (150 + largura(vis, 2), y, 14, 16))
                y += alt_linha(2)
            y += 10
        botao(r_voltar, "VOLTAR", mouse, 3)
        apresentar()
        relogio.tick(60)


def config():
    ESP = 50
    BH = 44
    aba = 0
    msg = ""
    msg_ate = 0
    nomes_abas = ["SOM E TELA", "CENÁRIO"]
    r_abas = [
        pygame.Rect(LARGURA // 2 - 350, 82, 340, 36),
        pygame.Rect(LARGURA // 2 + 10, 82, 340, 36),
    ]
    ys = [130 + i * ESP for i in range(len(EVENTOS_SOM))]
    r_escolher = [pygame.Rect(840, y, 200, BH) for y in ys]
    r_limpar = [pygame.Rect(1060, y, 160, BH) for y in ys]
    y_mmenu = 130 + len(EVENTOS_SOM) * ESP
    y_mjogo = y_mmenu + ESP
    y_vol = y_mjogo + ESP
    y_tela = y_vol + ESP
    y_crt = y_tela + ESP
    r_menos = pygame.Rect(360, y_vol, 60, BH)
    r_mais = pygame.Rect(820, y_vol, 60, BH)
    r_tmenos = pygame.Rect(360, y_tela, 60, BH)
    r_tmais = pygame.Rect(820, y_tela, 60, BH)
    r_crt = pygame.Rect(440, y_crt, 440, BH)
    musicas = [
        ("musica_menu", "MÚSICA DO MENU", y_mmenu, "menu"),
        ("musica_jogo", "MÚSICA DO JOGO", y_mjogo, "jogo"),
    ]
    r_mus_esc = [pygame.Rect(840, m[2], 200, BH) for m in musicas]
    r_mus_lim = [pygame.Rect(1060, m[2], 160, BH) for m in musicas]
    ys_v = [140 + i * 84 for i in range(len(ITENS_CENARIO))]
    r_v_esc = [pygame.Rect(840, y, 200, BH) for y in ys_v]
    r_v_lim = [pygame.Rect(1060, y, 160, BH) for y in ys_v]
    y_cano = 140 + len(ITENS_CENARIO) * 84
    r_cmenos = pygame.Rect(360, y_cano, 60, BH)
    r_cmais = pygame.Rect(820, y_cano, 60, BH)
    r_restaurar = pygame.Rect(LARGURA // 2 - 220, 540, 440, 54)
    r_voltar = pygame.Rect(LARGURA // 2 - 140, 630, 280, 60)
    while True:
        mouse = pos_mouse()
        agora = pygame.time.get_ticks()
        for e in eventos():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "menu"
                if e.key == pygame.K_TAB:
                    aba = 1 - aba
                    tocar("mover")
            if not clique(e):
                continue
            if r_voltar.collidepoint(mouse):
                tocar("selecionar")
                return "menu"
            trocou = False
            for i, r_a in enumerate(r_abas):
                if r_a.collidepoint(mouse):
                    if aba != i:
                        aba = i
                        tocar("selecionar")
                    trocou = True
            if trocou:
                continue
            if aba == 1:
                for i, (chave, _) in enumerate(ITENS_CENARIO):
                    if r_v_esc[i].collidepoint(mouse):
                        nome = escolher_imagem()
                        if nome:
                            if abrir_imagem(os.path.join(PASTA_IMG, nome)) is None:
                                msg = "NÃO FOI POSSÍVEL ABRIR A IMAGEM"
                                msg_ate = pygame.time.get_ticks() + 2500
                            else:
                                cfg["visual"][chave] = nome
                                salvar_json(ARQ_CONFIG, cfg)
                                recarregar_cenario()
                                tocar("selecionar")
                    if r_v_lim[i].collidepoint(mouse):
                        cfg["visual"][chave] = ""
                        salvar_json(ARQ_CONFIG, cfg)
                        recarregar_cenario()
                        tocar("selecionar")
                for rect, passo in ((r_cmenos, -1), (r_cmais, 1)):
                    if rect.collidepoint(mouse):
                        cfg["cano"] = (cfg["cano"] + passo) % len(CORES_CANO)
                        salvar_json(ARQ_CONFIG, cfg)
                        tocar("selecionar")
                if r_restaurar.collidepoint(mouse):
                    for chave, _ in ITENS_CENARIO:
                        cfg["visual"][chave] = ""
                    cfg["cano"] = 0
                    salvar_json(ARQ_CONFIG, cfg)
                    recarregar_cenario()
                    tocar("selecionar")
                continue
            if r_crt.collidepoint(mouse):
                cfg["crt"] = not cfg["crt"]
                salvar_json(ARQ_CONFIG, cfg)
                tocar("selecionar")
            for i, (chave_m, _, _, tipo) in enumerate(musicas):
                if r_mus_esc[i].collidepoint(mouse):
                    nome = escolher_audio()
                    if nome:
                        cfg[chave_m] = nome
                        salvar_json(ARQ_CONFIG, cfg)
                        if tipo == "menu":
                            tocar_musica("menu", forcar=True)
                if r_mus_lim[i].collidepoint(mouse):
                    cfg[chave_m] = ""
                    salvar_json(ARQ_CONFIG, cfg)
                    if tipo == "menu":
                        tocar_musica("menu", forcar=True)
            for i, (chave, _) in enumerate(EVENTOS_SOM):
                if r_escolher[i].collidepoint(mouse):
                    nome = escolher_audio()
                    if nome:
                        cfg["audio"][chave] = nome
                        salvar_json(ARQ_CONFIG, cfg)
                        carregar_sons()
                        tocar(chave)
                if r_limpar[i].collidepoint(mouse):
                    cfg["audio"][chave] = ""
                    salvar_json(ARQ_CONFIG, cfg)
                    carregar_sons()
            for rect, passo in ((r_menos, -0.1), (r_mais, 0.1)):
                if rect.collidepoint(mouse):
                    cfg["volume"] = round(min(1.0, max(0.0, cfg["volume"] + passo)), 1)
                    salvar_json(ARQ_CONFIG, cfg)
                    aplicar_volume()
                    tocar("acerto")
            for rect, passo in ((r_tmenos, -1), (r_tmais, 1)):
                if rect.collidepoint(mouse):
                    novo = min(len(TELAS) - 1, max(0, cfg["tela"] + passo))
                    if novo != cfg["tela"]:
                        cfg["tela"] = novo
                        salvar_json(ARQ_CONFIG, cfg)
                        aplicar_tela()
        fundo()
        texto_sombra("CONFIGURAÇÕES", 5, BRANCO, LARGURA // 2, 28, "centro")
        for i, rotulo_aba in enumerate(nomes_abas):
            botao(r_abas[i], rotulo_aba, mouse, 2, destaque=(aba == i))
        if aba == 0:
            for i, (chave, rotulo) in enumerate(EVENTOS_SOM):
                y = ys[i]
                texto(rotulo, 2, BRANCO, 60, y)
                arquivo = cfg["audio"].get(chave) or "NENHUM ARQUIVO"
                texto(cortar(arquivo, 2, 740), 2, AZUL_CLARO, 60, y + 24)
                botao(r_escolher[i], "ESCOLHER", mouse, 2)
                botao(r_limpar[i], "LIMPAR", mouse, 2)
            texto("VOLUME", 2, BRANCO, 60, y_vol + 14)
            botao(r_menos, "-", mouse, 3)
            barra = pygame.Rect(440, y_vol, 360, BH)
            pygame.draw.rect(tela, SOMBRA, barra)
            pygame.draw.rect(tela, LIMAO, (barra.x, barra.y, int(barra.w * cfg["volume"]), barra.h))
            pygame.draw.rect(tela, AZUL_CLARO, barra, 4)
            botao(r_mais, "+", mouse, 3)
            texto(f"{int(cfg['volume'] * 100)}%", 2, LIMAO, 910, y_vol + 14)
            texto("TELA", 2, BRANCO, 60, y_tela + 14)
            botao(r_tmenos, "<", mouse, 3)
            texto(NOMES_TELA[cfg["tela"]], 2, LIMAO, 630, y_tela + 14, "centro")
            botao(r_tmais, ">", mouse, 3)
            texto("EFEITO CRT", 2, BRANCO, 60, y_crt + 14)
            botao(r_crt, "LIGADO" if cfg["crt"] else "DESLIGADO", mouse, 2, destaque=cfg["crt"])
            for i, (chave_m, rotulo, y, _) in enumerate(musicas):
                texto(rotulo, 2, BRANCO, 60, y)
                arq = cfg.get(chave_m) or "NENHUM ARQUIVO"
                texto(cortar(arq, 2, 740), 2, AZUL_CLARO, 60, y + 24)
                botao(r_mus_esc[i], "ESCOLHER", mouse, 2)
                botao(r_mus_lim[i], "LIMPAR", mouse, 2)
        else:
            for i, (chave, rotulo) in enumerate(ITENS_CENARIO):
                y = ys_v[i]
                texto(rotulo, 2, BRANCO, 60, y)
                arq = cfg["visual"].get(chave) or "PADRÃO"
                texto(cortar(arq, 2, 740), 2, AZUL_CLARO, 60, y + 24)
                texto(DICAS_CENARIO[chave], 2, (140, 150, 190), 60, y + 48)
                botao(r_v_esc[i], "ESCOLHER", mouse, 2)
                botao(r_v_lim[i], "PADRÃO", mouse, 2)
            texto("COR DOS CANOS", 2, BRANCO, 60, y_cano + 14)
            botao(r_cmenos, "<", mouse, 3)
            texto(CORES_CANO[cfg["cano"]][1], 2, LIMAO, 630, y_cano + 14, "centro")
            botao(r_cmais, ">", mouse, 3)
            botao(r_restaurar, "RESTAURAR TUDO", mouse, 2)
            if msg and agora < msg_ate:
                texto_sombra(msg, 2, VERMELHO, LARGURA // 2, 606, "centro")
        botao(r_voltar, "VOLTAR", mouse, 3)
        apresentar()
        relogio.tick(60)


def tela_ranking():
    global RANK_DESTAQUE, RANK_DESTINO
    destaque = RANK_DESTAQUE
    destino = RANK_DESTINO
    RANK_DESTAQUE = -1
    RANK_DESTINO = "menu"
    r_voltar = pygame.Rect(LARGURA // 2 - 140, 630, 280, 60)
    rotulo = "VOLTAR" if destino == "menu" else "CONTINUAR"
    cores = [AMARELO, (210, 216, 230), LARANJA]
    while True:
        mouse = pos_mouse()
        agora = pygame.time.get_ticks()
        for e in eventos():
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    tocar("selecionar")
                    return destino
            elif clique(e) and r_voltar.collidepoint(mouse):
                tocar("selecionar")
                return destino
        fundo()
        texto_sombra("RANKING", 5, BRANCO, LARGURA // 2, 36, "centro")
        pygame.draw.rect(tela, PAINEL, (240, 110, 800, 500))
        pygame.draw.rect(tela, AZUL, (240, 110, 800, 500), 4)
        texto("POS", 2, AZUL_CLARO, 280, 128)
        texto("NOME", 2, AZUL_CLARO, 440, 128)
        texto("PONTOS", 2, AZUL_CLARO, 1000, 128, "dir")
        if not ranking:
            if (agora // 500) % 2 == 0:
                texto("SEM RECORDES AINDA", 3, LIMAO, LARGURA // 2, 300, "centro")
                texto("SEJA O PRIMEIRO!", 3, BRANCO, LARGURA // 2, 350, "centro")
        for i, r in enumerate(ranking):
            y = 166 + i * 43
            if i == destaque and (agora // 250) % 2 == 0:
                pygame.draw.rect(tela, AZUL, (256, y - 6, 768, 38))
            cor = cores[i] if i < 3 else BRANCO
            texto(f"{i + 1:02d}.", 3, cor, 280, y)
            texto(r["nome"], 3, cor, 440, y)
            texto(f"{r['pontos']:06d}", 3, cor, 1000, y, "dir")
        botao(r_voltar, rotulo, mouse, 3)
        apresentar()
        relogio.tick(60)


def iniciais():
    global RANK_DESTAQUE, RANK_DESTINO
    letras = ["A", "A", "A"]
    pos = 0
    ini = pygame.time.get_ticks()
    r_ok = pygame.Rect(LARGURA // 2 - 170, 580, 340, 64)
    tocar("recorde")
    confirmar = False
    while True:
        mouse = pos_mouse()
        agora = pygame.time.get_ticks()
        for e in eventos():
            if e.type == pygame.KEYDOWN:
                k = e.key
                if k == pygame.K_ESCAPE:
                    return PENDENTE["destino"]
                if k in (pygame.K_UP, pygame.K_DOWN):
                    idx = ALFABETO.index(letras[pos]) + (1 if k == pygame.K_UP else -1)
                    letras[pos] = ALFABETO[idx % 26]
                    tocar("mover")
                elif k == pygame.K_LEFT:
                    pos = max(0, pos - 1)
                    tocar("mover")
                elif k == pygame.K_RIGHT:
                    pos = min(2, pos + 1)
                    tocar("mover")
                elif k == pygame.K_BACKSPACE:
                    pos = max(0, pos - 1)
                elif k in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    confirmar = True
                else:
                    ch = e.unicode.upper()
                    if len(ch) == 1 and ch in ALFABETO:
                        letras[pos] = ch
                        pos = min(2, pos + 1)
                        tocar("mover")
            elif clique(e) and r_ok.collidepoint(mouse):
                confirmar = True
        if confirmar:
            RANK_DESTAQUE = registrar("".join(letras), PENDENTE["pontos"], PENDENTE["receita"])
            RANK_DESTINO = PENDENTE["destino"]
            tocar("selecionar")
            return "ranking"
        fundo()
        if (agora // 350) % 2 == 0:
            texto_sombra("NOVO RECORDE!", 6, AMARELO, LARGURA // 2, 70, "centro")
        texto_sombra(f"SEUS PONTOS: {PENDENTE['pontos']:06d}", 3, BRANCO, LARGURA // 2, 170, "centro")
        texto_sombra("DIGITE SUAS INICIAIS", 3, AZUL_CLARO, LARGURA // 2, 230, "centro")
        for i in range(3):
            x = LARGURA // 2 - 195 + i * 140
            caixa_r = pygame.Rect(x, 320, 110, 130)
            pygame.draw.rect(tela, SOMBRA, caixa_r.move(6, 6))
            pygame.draw.rect(tela, PAINEL, caixa_r)
            ativo = i == pos
            borda = LIMAO if ativo and (agora // 250) % 2 == 0 else (BRANCO if ativo else AZUL_CLARO)
            pygame.draw.rect(tela, borda, caixa_r, 4)
            texto(letras[i], 8, BRANCO, caixa_r.centerx, caixa_r.y + 32, "centro")
            if ativo:
                pygame.draw.polygon(tela, LIMAO, [(x + 35, 308), (x + 75, 308), (x + 55, 284)])
                pygame.draw.polygon(tela, LIMAO, [(x + 35, 462), (x + 75, 462), (x + 55, 486)])
        texto_sombra("SETAS ESCOLHEM A LETRA  -  ENTER CONFIRMA", 2, BRANCO, LARGURA // 2, 520, "centro")
        botao(r_ok, "CONFIRMAR", mouse, 3, destaque=True)
        apresentar()
        relogio.tick(60)


ARQ_ASSINATURA = os.path.join(PASTA, "assinatura.png")


def carregar_assinatura():
    img = abrir_imagem(ARQ_ASSINATURA)
    if img is None:
        return None
    w = 440
    return escalar(img, (w, round(img.get_height() * w / img.get_width())))


def creditos():
    foto = None
    if os.path.exists(ARQ_FOTO):
        try:
            img = pygame.image.load(ARQ_FOTO).convert()
            esc = min(336 / img.get_width(), 224 / img.get_height())
            foto = pygame.transform.smoothscale(
                img, (int(img.get_width() * esc), int(img.get_height() * esc))
            )
        except Exception:
            foto = None
    assinatura = carregar_assinatura()
    paragrafos = [quebrar(p, 2, 660) for p in CREDITOS_PARAGRAFOS]
    linhas = [l for p in paragrafos for l in p]
    total_chars = sum(len(l) for l in linhas)
    dur_texto = int(total_chars / 0.045)
    TEMPO_LEITURA = 7000
    ini = pygame.time.get_ticks()
    prox_fogo = 0
    del particulas[:]
    tocar("recorde")
    while True:
        agora = pygame.time.get_ticks()
        ms = agora - ini
        n_chars = int(ms * 0.045)
        digitou = n_chars >= total_chars
        t_pag2 = ms - dur_texto - TEMPO_LEITURA
        pagina2 = t_pag2 >= 0
        for e in eventos():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "menu"
            avancar = (
                e.type == pygame.KEYDOWN
                and e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)
            ) or clique(e)
            if not avancar:
                continue
            if pagina2:
                return "menu"
            if not digitou:
                ini = agora - dur_texto - 1
            else:
                ini = agora - dur_texto - TEMPO_LEITURA - 1
        if pagina2 and agora >= prox_fogo:
            soltar(random.randint(120, 1160), random.randint(80, 360), 40, random.sample(FESTA, 3), vel=300)
            prox_fogo = agora + random.randint(500, 1000)
        atualizar_particulas()
        fundo()
        pygame.draw.rect(tela, PAINEL, (60, 30, 1160, 660))
        pygame.draw.rect(tela, LIMAO, (60, 30, 1160, 660), 6)
        pygame.draw.rect(tela, SOMBRA, (90, 90, 360, 270))
        if foto is not None:
            tela.blit(foto, (270 - foto.get_width() // 2, 225 - foto.get_height() // 2))
        else:
            desenhar_bandeira(102, 113, ms / 1000, SPR_BANDEIRA_G, 12)
        pygame.draw.rect(tela, BRANCO, (90, 90, 360, 270), 6)
        texto_sombra("UPP-1", 3, LIMAO, 270, 384, "centro")
        texto("SEMANA DA QUALIDADE", 2, AZUL_CLARO, 270, 424, "centro")
        mascote(270, 650, "feliz", ms / 1000, -round(abs(math.sin(ms / 280)) * 36), chave="creditos")
        pygame.draw.rect(tela, AZUL, (476, 100, 4, 550))
        texto_onda("OBRIGADO!", 4, BRANCO, 840, 62, ms, 100, 50, True)
        pygame.draw.rect(tela, LIMAO, (740, 112, 200, 4))

        if not pagina2:
            vis_linhas = revelar(linhas, n_chars)
            y = 140
            k = 0
            cursor = None
            for p in paragrafos:
                for _ in p:
                    linha = vis_linhas[k]
                    k += 1
                    if linha:
                        texto(linha, 2, BRANCO, 500, y)
                        cursor = (500 + largura(linha, 2), y)
                    y += 30
                y += 26
            if not digitou and cursor and (agora // 250) % 2 == 0:
                pygame.draw.rect(tela, LIMAO, (cursor[0] + 4, cursor[1], 14, 16))
            if digitou and (agora // 500) % 2 == 0:
                texto("APERTE ENTER PARA CONTINUAR", 2, AZUL_CLARO, 840, 655, "centro")
        else:
            texto_onda("EM NOME DE TODOS,", 3, BRANCO, 840, 160, t_pag2, 0, 30, True, 30)
            texto_onda("UM MUITO OBRIGADO!", 3, LIMAO, 840, 210, t_pag2, 500, 30, True, 30)
            if t_pag2 > 1000:
                texto("ASSINADO:", 2, AZUL_CLARO, 840, 300, "centro")
                placa = pygame.Rect(0, 0, 480, 130)
                placa.center = (840, 405)
                pygame.draw.rect(tela, SOMBRA, placa.move(6, 6), border_radius=RAIO_BOTAO)
                pygame.draw.rect(tela, BRANCO, placa, border_radius=RAIO_BOTAO)
                pygame.draw.rect(tela, AZUL_CLARO, placa, 4, border_radius=RAIO_BOTAO)
                progresso = min(1.0, max(0.0, (t_pag2 - 1400) / 1800))
                if assinatura is not None:
                    ax = placa.centerx - assinatura.get_width() // 2
                    ay = placa.centery - assinatura.get_height() // 2
                    tela.blit(
                        assinatura,
                        (ax, ay),
                        (0, 0, int(assinatura.get_width() * progresso), assinatura.get_height()),
                    )
                else:
                    texto(ASSINATURA, 3, SOMBRA, placa.centerx, placa.centery - 12, "centro")
            for i in range(5):
                desenhar_coracao(720 + i * 50, 530 + onda(max(0.0, (t_pag2 - 3600 - i * 120) / 1000), 24), True)
            if (agora // 500) % 2 == 0:
                texto("APERTE ENTER PARA VOLTAR", 2, AZUL_CLARO, 840, 650, "centro")
        desenhar_particulas()
        apresentar()
        relogio.tick(60)


def painel_vitoria(nome, resumo, ms, mouse, r_outra, r_menu, recorde, agora):
    tela.blit(VEU, (0, 0))
    pygame.draw.rect(tela, AZUL_ESCURO, (100, 80, 1080, 560))
    pygame.draw.rect(tela, LIMAO, (100, 80, 1080, 560), 6)
    base = 534
    topo = 150
    tela.blit(CENA_CHAO, (120, base), (0, 0, 280, 100))
    mastro(190, topo, base)
    sub = min(1.0, ms / 1500)
    sub = 1 - (1 - sub) ** 2
    y_ini = base - 12 - 128
    y_fim = topo + 14
    desenhar_bandeira(194, round(y_ini + (y_fim - y_ini) * sub), ms / 1000)
    mascote(320, base, "feliz", ms / 1000, -round(abs(math.sin(ms / 260)) * 40), chave="vitoria")
    texto_onda("RECEITA PRONTA!", 5, BRANCO, 790, 112, ms, 200, 35, True)
    for linha in quebrar(nome.upper(), 2, 640)[:1]:
        texto(linha, 2, AZUL_CLARO, 790, 176, "centro")
    itens = [
        ("ETAPAS", resumo["etapas"]),
        ("BÔNUS DE TEMPO", resumo["tempo"]),
        ("PERFEITO!", resumo["perfeito"]),
    ]
    for k, (rot, val) in enumerate(itens):
        if ms > 700 + k * 450:
            texto(rot, 2, AZUL_CLARO, 450, 240 + k * 52 + 6)
            texto(f"{val:06d}", 3, BRANCO, 1130, 240 + k * 52, "dir")
    if ms > 700 + 3 * 450:
        pygame.draw.rect(tela, AZUL_CLARO, (450, 404, 680, 4))
        texto_sombra("TOTAL", 3, LIMAO, 450, 430)
        texto_sombra(f"{resumo['total']:06d}", 4, LIMAO, 1130, 424, "dir")
        if recorde and (agora // 300) % 2 == 0:
            texto_sombra("NOVO RECORDE!", 3, AMARELO, 790, 490, "centro")
    botao(r_outra, "OUTRA RECEITA", mouse, 3, destaque=True)
    botao(r_menu, "MENU", mouse, 3)


def painel_continuar(c, mouse, r_cont, r_desistir, ms, agora):
    tela.blit(VEU, (0, 0))
    pygame.draw.rect(tela, AZUL_ESCURO, (240, 130, 800, 440))
    pygame.draw.rect(tela, LIMAO, (240, 130, 800, 440), 6)
    texto_sombra("FIM DE JOGO", 6, BRANCO, 640, 156, "centro")
    if (agora // 400) % 2 == 0:
        texto_sombra("CONTINUAR?", 4, LIMAO, 640, 240, "centro")
    texto_onda(str(c), 14, BRANCO, 640, 300, ms % 1000, 0, 35, True, 24)
    botao(r_cont, "CONTINUAR", mouse, 3, destaque=True)
    botao(r_desistir, "DESISTIR", mouse, 3)


def painel_derrota(nome, pontos, recorde, mouse, r_outra, r_menu, agora):
    tela.blit(VEU, (0, 0))
    pygame.draw.rect(tela, AZUL_ESCURO, (200, 170, 880, 360))
    pygame.draw.rect(tela, LIMAO, (200, 170, 880, 360), 6)
    texto_sombra("FIM DE JOGO", 6, BRANCO, 640, 196, "centro")
    y = 272
    for linha in quebrar("AS VIDAS ACABARAM. A RECEITA ERA: " + nome.upper(), 2, 800):
        texto(linha, 2, BRANCO, 640, y, "centro")
        y += alt_linha(2)
    texto_sombra(f"PONTOS {pontos:06d}", 3, AZUL_CLARO, 640, y + 12, "centro")
    if recorde and (agora // 300) % 2 == 0:
        texto_sombra("NOVO RECORDE!", 3, AMARELO, 640, y + 56, "centro")
    botao(r_outra, "OUTRA RECEITA", mouse, 3, destaque=True)
    botao(r_menu, "MENU", mouse, 3)


def desenhar_popups(agora):
    restantes = []
    for pp in popups:
        idade = agora - pp[3]
        if idade > 900:
            continue
        restantes.append(pp)
        texto_sombra(pp[0], 3, pp[4], pp[1], pp[2] - round(idade * 0.05), "centro")
    popups[:] = restantes


COMP_X0 = 40
COMP_ESP = 10
POMBOS_N = 2
QUADROS_VOO = (0, 2)
DUR_COMP = {"acerto": 750, "erro": 2000, "combo": 2000}
PRIO_COMP = {"acerto": 1, "combo": 2, "erro": 3}
PES_JOGO = 702

_comp_spr = {"pronto": False, "pavao": None, "pombos": []}
comp = {"tipo": None, "evento": None, "ini": 0, "cor_tick": {}}
coracoes = []

SPR_CORACAO_MINI = sprite(CORACAO, {"1": VERMELHO}, 2)
SPR_CORACAO_ROSA = sprite(CORACAO, {"1": (255, 140, 170)}, 2)
SPR_JOINHA_G = sprite(JOINHA_GRADE, JOINHA_CORES, 3)
PENA_VERDE = (30, 150, 120)
PENA_CONTORNO = (10, 60, 60)


def preparar_companheiros():
    b = bichos_sprites()
    if not _comp_spr["pronto"]:
        _comp_spr["pronto"] = True
        if b["pavao"] is not None:
            _comp_spr["pavao"] = pygame.transform.flip(b["pavao"], True, False)
        _comp_spr["pombos"] = [pygame.transform.flip(q, True, False) for q in b["pombos"]]
    opcoes = ["mascote"]
    if _comp_spr["pavao"] is not None:
        opcoes.append("pavao")
    if len(_comp_spr["pombos"]) >= 3:
        opcoes.append("pombos")
    comp.update(tipo=random.choice(opcoes), evento=None, ini=0, cor_tick={})
    del coracoes[:]


def comp_ms(agora):
    if comp["evento"] is None:
        return None
    ms = agora - comp["ini"]
    if ms >= DUR_COMP[comp["evento"]]:
        comp["evento"] = None
        return None
    return ms


def comp_evento(nome, agora):
    atual = comp["evento"]
    if atual and comp_ms(agora) is not None and PRIO_COMP[atual] > PRIO_COMP[nome]:
        return
    comp.update(evento=nome, ini=agora, cor_tick={})


def posicoes_comp():
    x = COMP_X0
    saida = []
    if comp["tipo"] == "pavao":
        w = _comp_spr["pavao"].get_width()
        saida.append((x + w // 2, w))
        x += w
    elif comp["tipo"] == "pombos":
        w = _comp_spr["pombos"][0].get_width()
        for _ in range(POMBOS_N):
            saida.append((x + w // 2, w))
            x += w + COMP_ESP
        x -= COMP_ESP
    return saida, x


def desenhar_leque(ax, ay, abre, agora):
    if abre <= 0:
        return
    n = 9
    t = agora / 1000
    for k in range(n):
        a = math.radians(-90 + (-75 + 150 * k / (n - 1)) * abre)
        L = (60 + 55 * abre) * (0.92 + 0.08 * math.sin(k * 1.7))
        ex, ey = ax + math.cos(a) * L, ay + math.sin(a) * L
        pygame.draw.line(tela, PENA_CONTORNO, (ax, ay), (ex, ey), 10)
        pygame.draw.line(tela, PENA_VERDE, (ax, ay), (ex, ey), 6)
        r = max(3, int(11 * abre))
        c = (round(ex), round(ey))
        pygame.draw.circle(tela, (24, 60, 120), c, r + 3)
        pygame.draw.circle(tela, (40, 120, 230), c, r)
        pygame.draw.circle(tela, AMARELO, c, max(2, r // 2))
        if (int(t * 8) + k) % 5 == 0:
            pygame.draw.rect(tela, BRANCO, (c[0] - 1, c[1] - r - 6, 3, 3))


def desenhar_pavao(cx, pes, ev, ms, agora):
    spr = _comp_spr["pavao"]
    w, h = spr.get_size()
    dx = dy = 0
    if ev is None:
        dy = -2 if (agora // 600) % 2 else 0
    elif ev == "acerto":
        dy = -round(math.sin(ms / DUR_COMP["acerto"] * math.pi) * 70)
    elif ev == "erro":
        dx = round(math.sin(ms / 45) * 2)
        dy = 4
    elif ev == "combo":
        dy = -4 if (ms // 120) % 2 else 0
        d = DUR_COMP["combo"]
        abre = min(1.0, ms / 400)
        if ms > d - 350:
            abre = max(0.0, (d - ms) / 350)
        desenhar_leque(cx + w * 0.18, pes - h * 0.45 + dy, abre, agora)
    sombra_chao(cx, pes, -dy)
    tela.blit(spr, (cx - w // 2 + dx, pes + dy - h))
    if ev == "erro":
        hx = cx - w // 2 + w * 0.2
        hy = pes + dy - h + h * 0.22
        for k in range(2):
            ciclo = ((ms / 500) + k * 0.5) % 1.0
            x, y = round(hx + k * 9), round(hy + ciclo * 42)
            pygame.draw.rect(tela, AZUL_CLARO, (x, y, 4, 7))
            pygame.draw.rect(tela, BRANCO, (x, y, 2, 3))


def desenhar_pombos(pos, pes, ev, ms, agora):
    quadros = _comp_spr["pombos"]
    for k, (cx, w) in enumerate(pos):
        dx = dy = 0
        q = quadros[QUADROS_VOO[0]]
        if ev is None:
            ciclo = (agora + k * 700) % 2600
            if ciclo < 300:
                dy = -round(math.sin(ciclo / 300 * math.pi) * 8)
        elif ev == "acerto":
            p = ms / DUR_COMP["acerto"]
            dy = -round(math.sin(p * math.pi) * 140)
            dx = round(math.sin(p * 2 * math.pi) * (30 if k == 0 else -30))
            q = quadros[QUADROS_VOO[(ms // 70 + k) % 2]]
        elif ev == "erro":
            if ms < 600:
                p = ms / 600
                dy, dx = -round(p * p * 620), round(p * (160 + 90 * k))
                q = quadros[QUADROS_VOO[(ms // 70 + k) % 2]]
            elif ms < 1400:
                continue
            else:
                p = (ms - 1400) / 600
                e = 1 - (1 - p) ** 2
                dy, dx = -round((1 - e) * 620), round((1 - e) * (160 + 90 * k))
                q = quadros[QUADROS_VOO[(ms // 70 + k) % 2]] if p < 1 else quadros[0]
        elif ev == "combo":
            dy = -6 if (ms // 140 + k) % 2 else 0
            tick = ms // 200
            if comp["cor_tick"].get(k) != tick:
                comp["cor_tick"][k] = tick
                coracoes.append([cx + random.randint(-10, 10), pes - q.get_height() - 4,
                                 agora, random.random() * 6, k % 2 == 1])
        sombra_chao(cx + dx, pes, -dy)
        tela.blit(q, (cx + dx - q.get_width() // 2, pes + dy - q.get_height()))


def desenhar_coracoes(agora):
    vivos = []
    for c in coracoes:
        idade = agora - c[2]
        if idade > 1300:
            continue
        vivos.append(c)
        spr = SPR_CORACAO_ROSA if c[4] else SPR_CORACAO_MINI
        spr.set_alpha(int(255 * min(1.0, (1300 - idade) / 500)))
        tela.blit(spr, (round(c[0] + math.sin(idade / 160 + c[3]) * 10), round(c[1] - idade * 0.08)))
    coracoes[:] = vivos


def desenhar_joinha(cx, pes, ms, dy=0):
    top = pes - MASC_H + dy
    t = ms / 1000
    oy = onda(t, 20) + round(math.sin(ms / 90) * 2)
    braco = pygame.Rect(cx + 22, top + 57 + oy, 34, 16)
    ante = pygame.Rect(cx + 42, top + 27 + oy, 16, 46)
    for r in (braco, ante):
        pygame.draw.rect(tela, CONTORNOS["W"], r.inflate(6, 6))
    for r in (braco, ante):
        pygame.draw.rect(tela, BRANCO, r)
        pygame.draw.rect(tela, MATERIAIS["W"][2], (r.x, r.bottom - 4, r.w, 4))
    tela.blit(SPR_JOINHA_G, (ante.centerx - 15, ante.y - 32))
    if (ms // 150) % 2 == 0:
        tela.blit(SPR_BRILHO, (ante.centerx + 14, ante.y - 40))


def desenhar_companheiros(agora):
    ev, ms = None, 0
    m = comp_ms(agora)
    if m is not None:
        ev, ms = comp["evento"], m
    if comp["tipo"] == "pavao":
        desenhar_pavao(posicoes_comp()[0][0][0], PES_JOGO, ev, ms, agora)
    elif comp["tipo"] == "pombos":
        desenhar_pombos(posicoes_comp()[0], PES_JOGO, ev, ms, agora)
    desenhar_coracoes(agora)


def jogar():
    hover.clear()
    receita = proxima_receita()
    if receita is None:
        return tela_mensagem("CADASTRE UMA RECEITA PRIMEIRO", "cadastro")
    etapas = receita["etapas"]
    total = len(etapas)
    ordem = list(range(total))
    random.shuffle(ordem)
    while ordem == list(range(total)):
        random.shuffle(ordem)
    del particulas[:]
    del popups[:]
    preparar_companheiros()
    colocadas = []
    vidas = VIDAS_INICIAIS
    pontos = 0
    combo = 0
    melhor_combo = 0
    acertos = 0
    erros = 0
    continues = 0
    erro_idx = -1
    erro_ate = 0
    msg_txt = ""
    msg_cor = BRANCO
    msg_ate = 0
    perdas = {}
    ganhos = {}
    pose = "normal"
    pose_ate = 0
    tempo_total = max(20, total * SEGUNDOS_POR_ETAPA) * 1000.0
    restante = tempo_total
    resultado = None
    res_ini = 0
    resumo = None
    recorde = False
    linhas_vistas = 0
    prox_fogo = 0
    fase = "contagem"
    cont_ini = pygame.time.get_ticks()
    cont_n = -1
    cont_cont = -1
    r_outra = pygame.Rect(LARGURA // 2 - 380, 440, 360, 64)
    r_menu = pygame.Rect(LARGURA // 2 + 20, 440, 360, 64)
    rv_outra = pygame.Rect(430, 540, 350, 64)
    rv_menu = pygame.Rect(810, 540, 350, 64)
    r_cont = pygame.Rect(280, 470, 340, 64)
    r_desistir = pygame.Rect(660, 470, 340, 64)
    sel = 0
    while True:
        mouse = pos_mouse()
        agora = pygame.time.get_ticks()
        dt = min(100, relogio.get_time())
        if transicao is not None:
            cont_ini = agora
        elif fase == "contagem":
            n = int((agora - cont_ini) / 800)
            if n != cont_n:
                cont_n = n
                if n <= 2:
                    tocar("contagem")
                elif n == 3:
                    tocar("vai")
            if n >= 4:
                fase = "jogando"
                tocar_musica("jogo")
        if fase == "jogando" and resultado is None:
            restante = max(0.0, restante - dt)
        disponiveis = [i for i in ordem if i not in colocadas]
        retangulos = []
        y = 180
        for idx in disponiveis:
            linhas = quebrar(etapas[idx], 2, 518)
            h = len(linhas) * alt_linha(2) + 16
            retangulos.append(pygame.Rect(680, y, 550, h))
            y += h + 8
        if disponiveis:
            sel = max(0, min(sel, len(disponiveis) - 1))
        acao = None
        escolha = None
        for e in eventos():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return "menu"
                if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and resultado is not None:
                    acao = "continuar" if resultado == "continuar" else "outra"
                elif resultado is None and fase == "jogando" and disponiveis:
                    if e.key == pygame.K_UP:
                        sel = (sel - 1) % len(disponiveis)
                        tocar("mover")
                    elif e.key == pygame.K_DOWN:
                        sel = (sel + 1) % len(disponiveis)
                        tocar("mover")
                    elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        if escolha is None:
                            escolha = (disponiveis[sel], retangulos[sel])
                continue
            if e.type == pygame.MOUSEMOTION:
                for i_m, r_m in enumerate(retangulos):
                    if r_m.collidepoint(mouse):
                        sel = i_m
                continue
            if not clique(e):
                continue
            if resultado == "continuar":
                if r_cont.collidepoint(mouse):
                    acao = "continuar"
                elif r_desistir.collidepoint(mouse):
                    acao = "desistir"
                continue
            if resultado is not None:
                ro, rm = (rv_outra, rv_menu) if resultado == "vitoria" else (r_outra, r_menu)
                if ro.collidepoint(mouse):
                    acao = "outra"
                elif rm.collidepoint(mouse):
                    acao = "menu"
                continue
            if fase != "jogando":
                continue
            for idx_c, r_c in zip(disponiveis, retangulos):
                if r_c.collidepoint(mouse):
                    if escolha is None:
                        escolha = (idx_c, r_c)
                    break
        if escolha is not None:
            idx, r = escolha
            if idx == len(colocadas):
                colocadas.append(idx)
                acertos += 1
                combo += 1
                melhor_combo = max(melhor_combo, combo)
                mult = multiplicador(combo)
                ganho = PONTOS_ACERTO * mult
                pontos += ganho
                tocar("acerto")
                soltar(r.centerx, r.centery, 28, DOURADOS)
                popups.append([f"+{ganho}", r.centerx, r.y - 6, agora, AMARELO])
                pose, pose_ate = "feliz", agora + 600
                comp_evento("acerto", agora)
                if combo >= 2 and mult > multiplicador(combo - 1):
                    tocar("combo")
                    comp_evento("combo", agora)
                    msg_txt, msg_cor, msg_ate = f"COMBO X{mult}!", LIMAO, agora + 1000
                if acertos % ACERTOS_POR_VIDA == 0 and vidas < VIDAS_MAX:
                    vidas += 1
                    ganhos[vidas - 1] = agora
                    tocar("vida")
                    msg_txt, msg_cor, msg_ate = "VIDA EXTRA!", AMARELO, agora + 1500
                    soltar(40 + (vidas - 1) * 50 + 20, 48, 24, [VERMELHO, BRANCO, AMARELO_CLARO], vel=240, grav=200)
                if len(colocadas) == total:
                    bonus_tempo = int(restante / tempo_total * BONUS_TEMPO_MAX) // 10 * 10
                    bonus_perfeito = BONUS_PERFEITO if erros == 0 else 0
                    resumo = {
                        "etapas": pontos,
                        "tempo": bonus_tempo,
                        "perfeito": bonus_perfeito,
                        "total": pontos + bonus_tempo + bonus_perfeito,
                    }
                    recorde = qualifica(resumo["total"])
                    resultado = "vitoria"
                    res_ini = agora
                    linhas_vistas = 0
                    tocar("vitoria")
            else:
                vidas -= 1
                erros += 1
                combo = 0
                perdas[vidas] = agora
                erro_idx = idx
                erro_ate = agora + 500
                msg_txt, msg_cor, msg_ate = "ETAPA ERRADA!", BRANCO, agora + 900
                pose, pose_ate = "triste", agora + 1000
                comp_evento("erro", agora)
                tocar("erro")
                tremer(420, 9)
                piscar_tela((255, 50, 50), 280)
                soltar(40 + vidas * 50 + 20, 48, 18, [VERMELHO, BRANCO, VERMELHO_APAGADO], vel=220, grav=600)
                if vidas == 0:
                    recorde = qualifica(pontos)
                    res_ini = agora
                    if continues < CONTINUES_MAX:
                        resultado = "continuar"
                        cont_cont = 9
                    else:
                        resultado = "derrota"
                        tocar("derrota")
        if acao == "continuar":
            continues += 1
            vidas = VIDAS_INICIAIS
            for i in range(VIDAS_INICIAIS):
                ganhos[i] = agora
            resultado = None
            combo = 0
            tocar("vida")
        elif acao == "desistir":
            resultado = "derrota"
            recorde = qualifica(pontos)
            res_ini = agora
            tocar("derrota")
        elif acao in ("outra", "menu"):
            destino = "jogar" if acao == "outra" else "menu"
            final = resumo["total"] if resultado == "vitoria" else pontos
            if qualifica(final):
                PENDENTE.update(pontos=final, receita=receita["nome"], destino=destino)
                return "iniciais"
            return destino
        if resultado == "continuar":
            c = 9 - int((agora - res_ini) / 1000)
            if c < 0:
                resultado = "derrota"
                res_ini = agora
                tocar("derrota")
            elif c != cont_cont:
                cont_cont = c
                tocar("contagem")
        if resultado == "vitoria":
            ms_v = agora - res_ini
            vis = sum(1 for k in range(4) if ms_v > 700 + k * 450)
            if vis > linhas_vistas:
                linhas_vistas = vis
                tocar("mover")
            if agora >= prox_fogo:
                soltar(
                    random.randint(150, 1130),
                    random.randint(120, 400),
                    46,
                    random.sample(FESTA, 3),
                    vel=320,
                    grav=260,
                    vida=(700, 1300),
                )
                prox_fogo = agora + random.randint(350, 700)
            chover_confete(1)
        if resultado in ("vitoria", "derrota"):
            parar_musica()
        atualizar_particulas()

        fundo()
        desenhar_vidas(vidas, perdas, ganhos, agora)
        texto_sombra(cortar(receita["nome"].upper(), 3, 640), 3, BRANCO, LARGURA // 2, 36, "centro")
        texto_sombra(f"{len(colocadas)}/{total}", 3, AZUL_CLARO, LARGURA - 40, 36, "dir")
        frac = restante / tempo_total
        pygame.draw.rect(tela, SOMBRA, (40, 76, LARGURA - 80, 16))
        cor_barra = LIMAO if frac > 0.4 else (AMARELO if frac > 0.2 else VERMELHO)
        if frac > 0.2 or (agora // 150) % 2 == 0:
            pygame.draw.rect(tela, cor_barra, (44, 80, int((LARGURA - 88) * frac), 8))
        pygame.draw.rect(tela, AZUL_CLARO, (40, 76, LARGURA - 80, 16), 4)
        if agora < msg_ate:
            texto_sombra(msg_txt, 2, msg_cor, LARGURA // 2, 100, "centro")
        elif combo >= 2:
            cor_combo = LIMAO if (agora // 250) % 2 == 0 else BRANCO
            texto_sombra(f"COMBO X{multiplicador(combo)}", 2, cor_combo, LARGURA // 2, 100, "centro")
        pygame.draw.rect(tela, PAINEL, (40, 120, 600, 436))
        pygame.draw.rect(tela, AZUL, (40, 120, 600, 436), 4)
        texto("SUA RECEITA", 2, AZUL_CLARO, 64, 136)
        y = 172
        for n in range(total):
            if n < len(colocadas):
                linhas = quebrar(f"{n + 1}. {etapas[n]}", 2, 550)
                cor = LIMAO
            else:
                linhas = [f"{n + 1}. ???"]
                cor = AZUL
            for linha in linhas:
                texto(linha, 2, cor, 64, y)
                y += alt_linha(2)
            y += 6
        texto("ESCOLHA A PRÓXIMA ETAPA", 2, AZUL_CLARO, 680, 138)
        for i_s, (idx, r) in enumerate(zip(disponiveis, retangulos)):
            em_erro = idx == erro_idx and agora < erro_ate
            sobre = i_s == sel and resultado is None and fase == "jogando"
            k = suave(("etapa", idx), 1.0 if sobre else 0.0)
            if em_erro:
                prog = 1 - (erro_ate - agora) / 500
                rr = r.move(round(math.sin(prog * math.pi * 6) * 8 * (1 - prog)), 0)
                cor_fundo, cor_txt, borda = AZUL_ESCURO, BRANCO, BRANCO
            else:
                rr = r
                cor_fundo = misturar(AZUL, AZUL_CLARO, k)
                cor_txt = misturar(BRANCO, AZUL_ESCURO, k)
                borda = misturar(AZUL_CLARO, LIMAO, k)
            pygame.draw.rect(tela, SOMBRA, rr.move(5, 5), border_radius=RAIO_BOTAO)
            pygame.draw.rect(tela, cor_fundo, rr, border_radius=RAIO_BOTAO)
            pygame.draw.rect(tela, borda, rr, 4, border_radius=RAIO_BOTAO)
            textos = ["???"] if fase == "contagem" else quebrar(etapas[idx], 2, 518)
            for j, linha in enumerate(textos):
                texto(linha, 2, cor_txt, rr.x + 16, rr.y + 10 + j * alt_linha(2))
            if sobre and (agora // 300) % 2 == 0:
                desenhar_seta(rr.x - 36, rr.centery - 14, LIMAO)
        pose_atual = pose if agora < pose_ate else "normal"
        dy = 0
        agach = 0.0
        if pose_atual == "feliz":
            dec = 600 - (pose_ate - agora)
            if dec < 70:
                pose_atual = "normal"
                agach = math.sin(dec / 70 * math.pi / 2)
            else:
                q = (dec - 70) / 530
                dy = -round(math.sin(min(1.0, q) * math.pi) * 46)
        if comp["tipo"] == "mascote":
            ms_comb = comp_ms(agora) if comp["evento"] == "combo" else None
            if ms_comb is not None:
                pose_atual = "joinha"
                agach = 0.0
                dy = -round(abs(math.sin(ms_comb / 220)) * 6)
            mascote(110, 702, pose_atual, agora / 1000, dy, agach=agach, chave="jogo")
            if ms_comb is not None:
                desenhar_joinha(110, 702, ms_comb, dy)
        desenhar_companheiros(agora)
        tx = max(230, posicoes_comp()[1] + 18) if comp["tipo"] in ("pavao", "pombos") else 230
        bonus_atual = int(restante / tempo_total * BONUS_TEMPO_MAX) // 10 * 10
        texto("PONTOS", 2, AZUL_CLARO, tx, 580)
        texto_sombra(f"{pontos:06d}", 4, BRANCO, tx, 604)
        mult_txt = multiplicador(combo) if combo else 1
        texto(f"COMBO X{mult_txt}", 2, LIMAO if combo >= 2 else AZUL_CLARO, tx, 648)
        texto(f"BÔNUS {bonus_atual:04d}", 2, AZUL_CLARO, tx, 676)
        desenhar_popups(agora)
        if fase == "contagem" and transicao is None:
            n = min(3, int((agora - cont_ini) / 800))
            ms_l = (agora - cont_ini) - n * 800
            tela.blit(FAIXA_SUP, (0, 230))
            if n < 3:
                texto_onda(str(3 - n), 14, BRANCO, LARGURA // 2, 270, ms_l, 0, 35, True)
            else:
                texto_onda("VAI!", 10, LIMAO, LARGURA // 2, 290, ms_l, 0, 70, True)
        if resultado == "vitoria":
            painel_vitoria(receita["nome"], resumo, agora - res_ini, mouse, rv_outra, rv_menu, recorde, agora)
        elif resultado == "continuar":
            painel_continuar(9 - int((agora - res_ini) / 1000), mouse, r_cont, r_desistir, agora - res_ini, agora)
        elif resultado == "derrota":
            painel_derrota(receita["nome"], pontos, recorde, mouse, r_outra, r_menu, agora)
        desenhar_particulas()
        apresentar()
        relogio.tick(60)


FAIXA_SUP = pygame.Surface((LARGURA, 220), pygame.SRCALPHA)
FAIXA_SUP.fill((8, 18, 36, 170))


def adicionar_etapa(est):
    t = est["etapa"].strip()
    if not t:
        return
    if len(est["etapas"]) >= 8:
        est["msg"] = "MÁXIMO DE 8 ETAPAS"
        return
    est["etapas"].append(t)
    est["etapa"] = ""
    est["msg"] = ""


def salvar_receita(est):
    global receitas, fila
    if est["etapa"].strip():
        adicionar_etapa(est)
    nome = est["nome"].strip()
    if not nome:
        est["msg"] = "DIGITE O NOME DA RECEITA"
        return
    if len(est["etapas"]) < 2:
        est["msg"] = "MÍNIMO DE 2 ETAPAS"
        return
    receitas.append({"nome": nome, "etapas": list(est["etapas"])})
    salvar_json(ARQ_RECEITAS, receitas)
    fila = []
    est.update(nome="", etapa="", etapas=[], campo=0, msg="RECEITA SALVA!")


def cadastro():
    global receitas, fila
    pygame.key.start_text_input()
    est = {"nome": "", "etapa": "", "etapas": [], "campo": 0, "msg": ""}
    deslocamento = 0
    r_nome = pygame.Rect(40, 160, 640, 56)
    r_etapa = pygame.Rect(40, 260, 640, 56)
    r_adic = pygame.Rect(40, 330, 310, 52)
    r_desf = pygame.Rect(370, 330, 310, 52)
    r_salvar = pygame.Rect(40, 626, 420, 60)
    r_voltar = pygame.Rect(480, 626, 200, 60)
    while True:
        mouse = pos_mouse()
        for e in eventos():
            chave = "nome" if est["campo"] == 0 else "etapa"
            limite = 28 if est["campo"] == 0 else 60
            if e.type == pygame.TEXTINPUT:
                if len(est[chave]) < limite:
                    est[chave] += "".join(c for c in e.text if c.isprintable())
                    est[chave] = est[chave][:limite]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.key.stop_text_input()
                    return "menu"
                if e.key == pygame.K_BACKSPACE:
                    est[chave] = est[chave][:-1]
                elif e.key == pygame.K_TAB:
                    est["campo"] = 1 - est["campo"]
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if est["campo"] == 0:
                        est["campo"] = 1
                    else:
                        adicionar_etapa(est)
            elif e.type == pygame.MOUSEWHEEL:
                deslocamento -= e.y
            elif clique(e):
                if r_nome.collidepoint(mouse):
                    est["campo"] = 0
                elif r_etapa.collidepoint(mouse):
                    est["campo"] = 1
                elif r_adic.collidepoint(mouse):
                    adicionar_etapa(est)
                elif r_desf.collidepoint(mouse):
                    if est["etapas"]:
                        est["etapas"].pop()
                elif r_salvar.collidepoint(mouse):
                    salvar_receita(est)
                elif r_voltar.collidepoint(mouse):
                    pygame.key.stop_text_input()
                    return "menu"
                else:
                    for pos in range(9):
                        i = deslocamento + pos
                        if i >= len(receitas):
                            break
                        r_del = pygame.Rect(1160, 170 + pos * 52, 70, 40)
                        if r_del.collidepoint(mouse):
                            del receitas[i]
                            salvar_json(ARQ_RECEITAS, receitas)
                            fila = []
                            break
        deslocamento = max(0, min(deslocamento, len(receitas) - 9))
        fundo()
        texto_sombra("CADASTRAR RECEITA", 4, BRANCO, 40, 36)
        texto("ETAPAS NA ORDEM CORRETA DE FABRICAÇÃO", 2, AZUL_CLARO, 40, 96)
        texto("NOME DA RECEITA", 2, BRANCO, 40, 134)
        texto("ETAPA (ENTER ADICIONA)", 2, BRANCO, 40, 234)
        piscar = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        for campo, rect, chave in ((0, r_nome, "nome"), (1, r_etapa, "etapa")):
            pygame.draw.rect(tela, SOMBRA, rect)
            pygame.draw.rect(tela, LIMAO if est["campo"] == campo else AZUL_CLARO, rect, 4)
            conteudo = est[chave] + (piscar if est["campo"] == campo else "")
            texto(cortar_fim(conteudo, 2, rect.w - 28), 2, BRANCO, rect.x + 14, rect.centery - 8)
        botao(r_adic, "ADICIONAR", mouse, 2)
        botao(r_desf, "DESFAZER", mouse, 2)
        texto(f"ETAPAS ({len(est['etapas'])}/8)", 2, AZUL_CLARO, 40, 396)
        for i, et in enumerate(est["etapas"]):
            texto(cortar(f"{i + 1}. {et}", 2, 640), 2, LIMAO, 40, 424 + i * 22)
        if est["msg"]:
            texto(est["msg"], 2, BRANCO, 40, 600)
        botao(r_salvar, "SALVAR RECEITA", mouse, 2, destaque=True)
        botao(r_voltar, "VOLTAR", mouse, 2)
        pygame.draw.rect(tela, PAINEL, (720, 120, 520, 560))
        pygame.draw.rect(tela, AZUL, (720, 120, 520, 560), 4)
        texto(f"RECEITAS ({len(receitas)})", 2, AZUL_CLARO, 740, 138)
        for pos in range(9):
            i = deslocamento + pos
            if i >= len(receitas):
                break
            y = 170 + pos * 52
            texto(cortar(receitas[i]["nome"], 2, 380), 2, BRANCO, 740, y + 12)
            botao((1160, y, 70, 40), "X", mouse, 2)
        apresentar()
        relogio.tick(60)


CENAS = {
    "abertura": abertura,
    "menu": menu,
    "jogar": jogar,
    "como": como_jogar,
    "config": config,
    "cadastro": cadastro,
    "ranking": tela_ranking,
    "iniciais": iniciais,
    "creditos": creditos,
    "sair": sair,
}

aplicar_tela()
recarregar_cenario()
carregar_sons()
criar_sons_8bit()
tocar_musica("menu")
estado = "abertura"
while True:
    anterior = estado
    estado = CENAS[estado]()
    if estado == "jogar":
        parar_musica()
    elif estado != "sair":
        tocar_musica("menu")
    if anterior == "menu" and estado == "jogar":
        iniciar_transicao()