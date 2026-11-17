# Dashboard Multimédia com IA - código Python que corre no browser (PyScript)
# Baseado nas fichas de Python de outubro (old/python.ipynb e old/parte2.ipynb)

import random
from html import escape
from math import gcd

from pyscript import document, when, window


def el(id):
    # atalho para ir buscar um elemento da página pelo id
    return document.getElementById(id)


# =====================================================================
# WIDGET 1 - Analisador Poético
# Baseado na ficha 6.1 (contagem de palavras) e 7 (nuvem de palavras)
# =====================================================================

STOPWORDS = {
    "a", "o", "as", "os", "e", "é", "de", "do", "da", "dos", "das", "em", "no",
    "na", "nos", "nas", "um", "uma", "uns", "umas", "que", "se", "por", "para",
    "com", "ao", "à", "aos", "às", "eu", "tu", "ele", "ela", "me", "te", "lhe",
    "mais", "mas", "como", "este", "esta", "isto", "esse", "essa", "não", "já",
    "meu", "minha", "seu", "sua", "pé",
}

# dicionário de sinónimos poéticos (sugestão gerada com ajuda da IA)
SINONIMOS = {
    # os sinónimos têm o mesmo género da palavra original (o mar -> o oceano)
    "mar": ["oceano", "abismo azul", "infinito azul"],
    "esforço": ["empenho", "labor", "afã"],
    "grande": ["imenso", "vasto", "colossal"],
    "pequeno": ["ínfimo", "breve", "humilde"],
    "homem": ["ser", "mortal", "navegante"],
    "navegador": ["marinheiro", "viajante", "argonauta"],
    "areal": ["areão", "litoral", "arenal"],
    "moreno": ["dourado", "queimado", "trigueiro"],
    "padrão": ["marco", "símbolo", "monumento"],
    "noite": ["escuridão", "treva", "sombra"],
    "dia": ["amanhecer", "alvorecer", "raiar"],
    "sol": ["astro", "astro-rei", "fogo celeste"],
    "amor": ["afeto", "querer", "bem-querer"],
    "triste": ["melancólico", "sombrio", "saudoso"],
    "feliz": ["radiante", "alegre", "sereno"],
    "vida": ["existência", "jornada", "travessia"],
    "morte": ["partida", "despedida", "finitude"],
    "céu": ["firmamento", "éter", "infinito"],
    "terra": ["pátria", "planície", "natureza"],
    "sonho": ["devaneio", "delírio", "anseio"],
    "tempo": ["momento", "instante", "fado"],
    "coração": ["peito", "âmago", "íntimo"],
    "vento": ["sopro", "vendaval", "zéfiro"],
    "luz": ["claridade", "centelha", "aurora"],
}

PALETAS = {
    "viridis": ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"],
    "oceano": ["#03045e", "#0077b6", "#00b4d8", "#48cae4", "#90e0ef"],
    "fogo": ["#6a040f", "#d00000", "#e85d04", "#faa307", "#ffba08"],
    "pastel": ["#cdb4db", "#ffc8dd", "#ffafcc", "#bde0fe", "#a2d2ff"],
}


def limpar_palavras(texto):
    # tira a pontuação e divide o texto em palavras (como na ficha 6.1)
    for sinal in ".,;:!?«»\"'()—-":
        texto = texto.replace(sinal, " ")
    return texto.lower().split()


def contar_frequencia(palavras):
    frequencia = {}
    for palavra in palavras:
        if palavra not in STOPWORDS:
            frequencia[palavra] = frequencia.get(palavra, 0) + 1
    return frequencia


def desenhar_nuvem(frequencia):
    max_palavras = int(el("nuvem-max").value)
    cores = PALETAS[el("nuvem-paleta").value]

    # ordena da mais frequente para a menos frequente
    ordenadas = sorted(frequencia.items(), key=lambda item: item[1], reverse=True)
    ordenadas = ordenadas[:max_palavras]

    if not ordenadas:
        el("nuvem").innerHTML = '<p class="text-tinta/60">Sem palavras para mostrar.</p>'
        return

    maior = ordenadas[0][1]
    menor = ordenadas[-1][1]
    random.shuffle(ordenadas)  # baralha para parecer uma nuvem

    html = ""
    for palavra, quantidade in ordenadas:
        if maior == menor:
            tamanho = 22
        else:
            tamanho = 14 + (quantidade - menor) / (maior - menor) * 30
        cor = random.choice(cores)
        html += (
            f'<span class="inline-block px-1 font-bold hover:-translate-y-1" '
            f'style="font-size:{tamanho:.0f}px; color:{cor}" '
            f'title="{escape(palavra)}: {quantidade}x">{escape(palavra)}</span> '
        )
    el("nuvem").innerHTML = html


@when("click", "#btn-analisar")
def clicar_analisar(event):
    analisar_poema()


def analisar_poema():
    texto = el("poema").value
    palavras = limpar_palavras(texto)
    frequencia = contar_frequencia(palavras)

    # estatísticas (funções embutidas nas strings - ficha 6)
    linhas = [l for l in texto.split("\n") if l.strip() != ""]
    el("stat-palavras").innerText = str(len(palavras))
    el("stat-versos").innerText = str(len(linhas))
    el("stat-unicas").innerText = str(len(set(palavras)))
    if frequencia:
        mais_usada = max(frequencia, key=frequencia.get)
        el("stat-top").innerText = mais_usada
    else:
        el("stat-top").innerText = "-"

    desenhar_nuvem(frequencia)

    # sinónimos encontrados no poema
    encontrados = [p for p in sorted(set(palavras)) if p in SINONIMOS]
    if encontrados:
        html = ""
        for p in encontrados:
            html += (
                f'<li><span class="font-semibold text-coral">{escape(p)}</span>'
                f' → {", ".join(SINONIMOS[p])}</li>'
            )
        el("sinonimos").innerHTML = html
    else:
        el("sinonimos").innerHTML = '<li class="text-tinta/60">Nenhuma palavra com sinónimos conhecidos.</li>'


@when("click", "#btn-reescrever")
def reescrever_poema(event):
    # troca cada palavra que tem sinónimo por um sinónimo ao calhas
    novas_linhas = []
    for linha in el("poema").value.split("\n"):
        novas = []
        for palavra in linha.split(" "):
            base = limpar_palavras(palavra)
            if len(base) == 1 and base[0] in SINONIMOS:
                sinonimo = random.choice(SINONIMOS[base[0]])
                if palavra[:1].isupper():
                    sinonimo = sinonimo.capitalize()
                palavra = palavra.replace(palavra.strip(".,;:!?«»\"'()"), sinonimo)
            novas.append(palavra)
        novas_linhas.append(" ".join(novas))
    el("poema-novo").innerText = "\n".join(novas_linhas)


# =====================================================================
# WIDGET 2 - Validador de Resoluções, Proporções e Cores
# Baseado no exercício 1.3.1 (resolução do ecrã) da parte 2
# =====================================================================

PROPORCOES = {
    "16:9": 16 / 9,
    "4:3": 4 / 3,
    "1:1": 1,
    "21:9": 21 / 9,
    "9:16": 9 / 16,
    "3:2": 3 / 2,
    "4:5": 4 / 5,
}


def categoria_resolucao(largura):
    if largura < 1280:
        return "SD (baixa resolução)", "bg-coral text-branco"
    elif largura < 1920:
        return "HD (720p)", "bg-pessego text-tinta"
    elif largura < 2560:
        return "Full HD (1080p)", "bg-sol text-tinta"
    elif largura < 3840:
        return "2K / QHD", "bg-azul text-tinta"
    else:
        return "4K UHD ou superior", "bg-ceu text-branco"


@when("click", "#btn-validar")
def clicar_validar(event):
    validar_resolucao()


def validar_resolucao():
    try:
        largura = int(el("res-largura").value)
        altura = int(el("res-altura").value)
    except ValueError:
        el("res-resultado").innerHTML = '<p class="font-semibold text-coral">Introduz números inteiros válidos.</p>'
        return

    if largura <= 0 or altura <= 0:
        el("res-resultado").innerHTML = '<p class="font-semibold text-coral">Por favor introduz uma resolução válida.</p>'
        return

    categoria, cores = categoria_resolucao(max(largura, altura))

    # proporção exata usando o máximo divisor comum
    divisor = gcd(largura, altura)
    exata = f"{largura // divisor}:{altura // divisor}"

    # proporção conhecida mais próxima
    racio = largura / altura
    nome_proximo = min(PROPORCOES, key=lambda nome: abs(PROPORCOES[nome] - racio))
    if abs(PROPORCOES[nome_proximo] - racio) < 0.02:
        proporcao = nome_proximo
    else:
        proporcao = f"{exata} (perto de {nome_proximo})"

    megapixeis = largura * altura / 1_000_000

    el("res-resultado").innerHTML = f"""
        <span class="inline-block border-2 border-tinta px-3 py-1 text-sm font-semibold {cores}">{categoria}</span>
        <dl class="mt-3 grid grid-cols-2 gap-2 text-sm">
            <dt class="text-tinta/60">Proporção</dt><dd class="font-semibold">{proporcao}</dd>
            <dt class="text-tinta/60">Megapíxeis</dt><dd class="font-semibold">{megapixeis:.2f} MP</dd>
            <dt class="text-tinta/60">Total de píxeis</dt><dd class="font-semibold">{largura * altura:,}</dd>
        </dl>
    """

    # pré-visualização com a proporção certa
    preview = el("res-preview")
    preview.style.aspectRatio = f"{largura} / {altura}"
    preview.innerText = f"{largura}×{altura}"


def usar_preset(largura, altura):
    el("res-largura").value = str(largura)
    el("res-altura").value = str(altura)
    validar_resolucao()


@when("click", "[data-preset]")
def clicar_preset(event):
    largura, altura = event.currentTarget.dataset.preset.split("x")
    usar_preset(int(largura), int(altura))


def hex_para_rgb(cor):
    return int(cor[1:3], 16), int(cor[3:5], 16), int(cor[5:7], 16)


def rgb_para_hex(r, g, b):
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def misturar(cor, outra, quantidade):
    # mistura duas cores (quantidade de 0 a 1)
    r1, g1, b1 = hex_para_rgb(cor)
    r2, g2, b2 = hex_para_rgb(outra)
    return rgb_para_hex(
        r1 + (r2 - r1) * quantidade,
        g1 + (g2 - g1) * quantidade,
        b1 + (b2 - b1) * quantidade,
    )


@when("input", "#cor-base")
def mudar_cor(event):
    gerar_paleta()


def gerar_paleta():
    base = el("cor-base").value
    r, g, b = hex_para_rgb(base)
    complementar = rgb_para_hex(255 - r, 255 - g, 255 - b)

    paleta = [
        ("Escura", misturar(base, "#000000", 0.6)),
        ("Sombra", misturar(base, "#000000", 0.3)),
        ("Base", base),
        ("Clara", misturar(base, "#ffffff", 0.4)),
        ("Suave", misturar(base, "#ffffff", 0.75)),
        ("Complementar", complementar),
    ]

    html = ""
    for nome, cor in paleta:
        # texto escuro em cores claras e texto claro em cores escuras
        cr, cg, cb = hex_para_rgb(cor)
        texto = "#1b1926" if (cr * 0.299 + cg * 0.587 + cb * 0.114) > 150 else "#ffffff"
        html += f"""
            <button data-cor="{cor}" title="Copiar {cor}"
                class="amostra flex h-20 flex-col justify-end p-2 text-left text-sm"
                style="background:{cor}; color:{texto}">
                <span class="font-semibold">{nome}</span>
                <span>{cor}</span>
            </button>"""
    el("paleta").innerHTML = html

    for botao in document.querySelectorAll("[data-cor]"):
        botao.onclick = copiar_cor


def copiar_cor(event):
    cor = event.currentTarget.dataset.cor
    window.navigator.clipboard.writeText(cor)
    el("cor-aviso").innerText = f"{cor} copiado!"


# =====================================================================
# WIDGET 3 - Jogo Adivinha o Número
# Baseado no JOGO DA ADIVINHA da parte 2
# =====================================================================

jogo = {
    "secreto": 0,
    "tentativas": 0,
    "total": 0,
    "minimo": 1,
    "maximo": 100,
    "ativo": False,
    "historico": [],
}


def mostrar_mensagem(texto, cor="text-tinta"):
    el("jogo-mensagem").className = f"min-h-12 {cor}"
    el("jogo-mensagem").innerHTML = texto


def atualizar_jogo():
    restantes = jogo["total"] - jogo["tentativas"]
    el("jogo-restantes").innerText = str(restantes)
    el("jogo-intervalo").innerText = f"{jogo['minimo']} – {jogo['maximo']}"

    percentagem = 0 if jogo["total"] == 0 else restantes / jogo["total"] * 100
    el("jogo-barra").style.width = f"{percentagem}%"

    html = ""
    for numero, cor in jogo["historico"]:
        html += f'<span class="border-2 border-tinta px-2 py-1 text-sm font-semibold {cor}">{numero}</span>'
    el("jogo-historico").innerHTML = html


@when("click", "#btn-comecar")
def comecar_jogo(event):
    nivel = el("jogo-nivel").value
    if nivel == "1":
        jogo["total"] = 20
    elif nivel == "2":
        jogo["total"] = 10
    else:
        jogo["total"] = 5

    jogo["secreto"] = 0  # 0 = ainda não escolhido (só escolhemos depois do 1.º chute)
    jogo["tentativas"] = 0
    jogo["minimo"] = 1
    jogo["maximo"] = 100
    jogo["ativo"] = True
    jogo["historico"] = []

    el("jogo-chute").disabled = False
    el("btn-tentar").disabled = False
    el("jogo-chute").value = ""
    el("jogo-chute").focus()
    mostrar_mensagem(f"Pensei num número entre 1 e 100. Tens {jogo['total']} tentativas. Boa sorte! 🍀")
    atualizar_jogo()


def dica_extra():
    # dicas personalizadas que aparecem depois de errar algumas vezes
    secreto = jogo["secreto"]
    tentativa = jogo["tentativas"]

    if tentativa == 2:
        return "O número é " + ("par." if secreto % 2 == 0 else "ímpar.")
    if tentativa == 3:
        for divisor in (10, 5, 3, 7):
            if secreto % divisor == 0:
                return f"O número é múltiplo de {divisor}."
        return "O número não é múltiplo de 3, 5, 7 nem 10."
    if tentativa == 4 and secreto > 10:
        return f"A soma dos algarismos é {sum(int(a) for a in str(secreto))}."
    return ""


def mensagem_motivacional():
    restantes = jogo["total"] - jogo["tentativas"]
    if restantes == 1:
        return "Última tentativa! Respira fundo... 😬"
    if restantes <= jogo["total"] * 0.3:
        return "Está a apertar, mas ainda dá! 💪"
    if jogo["maximo"] - jogo["minimo"] <= 10:
        return "Já estás mesmo quase! 🔥"
    return random.choice([
        "Continua, vais no bom caminho!",
        "Boa estratégia, não desistas!",
        "Cada erro dá-te mais pistas 🧠",
    ])


@when("click", "#btn-tentar")
def clicar_tentar(event):
    tentar()


def tentar():
    if not jogo["ativo"]:
        return

    try:
        chute = int(el("jogo-chute").value)
    except ValueError:
        mostrar_mensagem("Digita um número inteiro!", "font-semibold text-coral")
        return

    if chute < 1 or chute > 100:
        mostrar_mensagem("Por favor, digita um número entre 1 e 100!", "font-semibold text-coral")
        return

    # no primeiro chute, escolhe o número secreto, mas nunca igual ao chute
    if jogo["secreto"] == 0:
        numero = random.randrange(1, 101)
        while numero == chute:
            numero = random.randrange(1, 101)
        jogo["secreto"] = numero

    jogo["tentativas"] += 1
    secreto = jogo["secreto"]
    el("jogo-chute").value = ""
    el("jogo-chute").focus()

    if chute == secreto:
        jogo["ativo"] = False
        jogo["historico"].append((chute, "bg-tinta text-sol"))
        if jogo["tentativas"] == 1:
            elogio = "À primeira?! És um génio! 🤯"
        elif jogo["tentativas"] <= 4:
            elogio = "Excelente raciocínio! 🏆"
        else:
            elogio = "Conseguiste! 🎉"
        mostrar_mensagem(
            f"<b>UAU, acertaste!</b> O número secreto era {secreto}. "
            f"Precisaste de {jogo['tentativas']} tentativa(s). {elogio}",
            "border-2 border-tinta bg-sol p-2",
        )
        terminar_jogo()
        return

    # atualiza o intervalo onde o número pode estar
    if chute > secreto:
        jogo["maximo"] = min(jogo["maximo"], chute - 1)
        direcao = f"O {chute} é <b>maior</b> que o número secreto. ⬇️"
    else:
        jogo["minimo"] = max(jogo["minimo"], chute + 1)
        direcao = f"O {chute} é <b>menor</b> que o número secreto. ⬆️"

    # quente ou frio
    distancia = abs(chute - secreto)
    if distancia <= 3:
        temperatura = "🔥 A ferver!"
        cor = "bg-coral text-branco"
    elif distancia <= 10:
        temperatura = "♨️ Quente"
        cor = "bg-pessego text-tinta"
    elif distancia <= 25:
        temperatura = "🌤️ Morno"
        cor = "bg-sol text-tinta"
    else:
        temperatura = "❄️ Frio"
        cor = "bg-ceu text-branco"
    jogo["historico"].append((chute, cor))

    if jogo["tentativas"] >= jogo["total"]:
        jogo["ativo"] = False
        mostrar_mensagem(
            f"Perdeste! O número secreto era <b>{secreto}</b>. Tenta outra vez! 🔁",
            "border-2 border-tinta bg-coral p-2 text-branco",
        )
        terminar_jogo()
        return

    dica = dica_extra()
    texto = f"{direcao} {temperatura}<br>"
    if dica:
        texto += f"💡 Dica: {dica}<br>"
    texto += f"<span class='text-tinta/60'>{mensagem_motivacional()}</span>"
    mostrar_mensagem(texto)
    atualizar_jogo()


@when("keydown", "#jogo-chute")
def tecla_enter(event):
    if event.key == "Enter":
        tentar()


def terminar_jogo():
    el("jogo-chute").disabled = True
    el("btn-tentar").disabled = True
    atualizar_jogo()


# =====================================================================
# Arranque: prepara a página e esconde o ecrã de carregamento
# =====================================================================
analisar_poema()
usar_preset(1920, 1080)
gerar_paleta()
el("loading").remove()
