"""Gera index.html (Kersevani) a partir de index.original.html (modelo Justic)."""
import re, sys, os

ROOT = sys.argv[1]
src = open(os.path.join(ROOT, '_modelo-original', 'index.original.html'), encoding='utf-8', errors='surrogateescape').read()
s = src


def el_range(s, data_id):
    m = re.search(r'<(section|div|footer|header)\b[^>]*data-id="%s"' % re.escape(data_id), s)
    assert m, 'nao achei ' + data_id
    tag, start = m.group(1), m.start()
    depth, pos = 0, start
    pat = re.compile(r'<(/?)%s\b' % tag)
    while True:
        t = pat.search(s, pos)
        assert t, 'sem fechamento ' + data_id
        depth += -1 if t.group(1) else 1
        pos = t.end()
        if depth == 0:
            end = s.index('>', t.start()) + 1
            return start, end


def remove(data_id):
    global s
    a, b = el_range(s, data_id)
    s = s[:a] + s[b:]


def edit(data_id, fn):
    global s
    a, b = el_range(s, data_id)
    s = s[:a] + fn(s[a:b]) + s[b:]


def txt(chunk, old, new, n=1):
    """Troca n nós de texto que começam com `old`."""
    pat = re.compile(r'(>\s*)' + re.escape(old) + r'[^<]*')
    out, k = pat.subn(lambda m: m.group(1) + new, chunk, count=n)
    assert k == n, f'texto "{old}" achado {k}x (esperado {n})'
    return out


def texts(data_id, *pairs):
    def fn(c):
        for p in pairs:
            c = txt(c, *p)
        return c
    edit(data_id, fn)


def hrefs(data_id, *urls):
    """Define os href das <a> do elemento, em ordem."""
    def fn(c):
        it = iter(urls)
        def rep(m):
            try:
                return m.group(1) + 'href="' + next(it) + '"'
            except StopIteration:
                return m.group(0)
        c2 = re.sub(r'(<a\b[^>]*?)href="[^"]*"', rep, c)
        return c2
    edit(data_id, fn)


def add_id(data_id, new_id):
    global s
    a, _ = el_range(s, data_id)
    s = s[:a] + s[a:].replace('<section ', f'<section id="{new_id}" ', 1)


TBD_MAIL = 'E-mail a definir'
TBD_TEL = 'Telefone a definir'
TBD_END = 'Endereço a definir'

# ---------------- <head> ----------------
s = s.replace('<html lang="en-US">', '<html lang="pt-BR">', 1)
NL = chr(10)
s = re.sub(r'<title>.*?</title>', ('<title>Kersevani Advogados</title>' + NL +
           '<meta name="description" content="Kersevani Advogados — Direito Público, Empresarial, Previdenciário, Trabalhista e Civil.">' + NL +
           '<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="Kersevani Advogados">' + NL +
           '<meta property="og:title" content="Kersevani Advogados"><meta property="og:description" content="Advocacia especializada em Direito Público, Empresarial, Previdenciário, Trabalhista e Civil.">' + NL +
           '<meta property="og:url" content="https://juliopk543.github.io/kersevani-advogados/"><meta property="og:image" content="https://juliopk543.github.io/kersevani-advogados/images/previa-link.png">' + NL +
           '<meta property="og:image:type" content="image/png"><meta property="og:image:width" content="405"><meta property="og:image:height" content="295"><meta property="og:image:alt" content="Kersevani Advogados — advocacia especializada">' + NL +
           '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Kersevani Advogados"><meta name="twitter:image" content="https://juliopk543.github.io/kersevani-advogados/images/previa-link.png">').replace('NL_', ''), s, count=1, flags=re.S)
s = re.sub(r'<link rel="(profile|pingback|alternate|https://api.w.org/|EditURI|shortlink|canonical)"[^>]*>\s*', '', s)
s = s.replace('</head>', '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/kersevani.css">
</head>''', 1)
s = s.replace('</body>', '<script src="js/kersevani.js"></script></body>', 1)

# ---------------- Cabeçalho ----------------
s = re.sub(r'<img[^>]*src="images/PJmkoIc5rsmE\.png"[^>]*>',
           '<img width="964" height="746" src="images/logo-kersevani.svg" class="attachment-full size-full" alt="Kersevani Advogados" decoding="async">', s)
s = re.sub(r'<img[^>]*src="images/nKVxXEIe0JqR\.png"[^>]*>',
           '<img width="1000" height="272" src="images/logo-kersevani-h.svg" class="attachment-full size-full" alt="Kersevani Advogados" decoding="async">', s)
texts('0f5e891', ('justic@support.com', TBD_MAIL), ('+62 478-2240-190', TBD_TEL))

menu = ('<ul id="menu-menu" class="jkit-menu jkit-menu-direction-flex jkit-submenu-position-top">'
        '<li class="menu-item current-menu-item"><a href="#inicio">Início</a></li>'
        '<li class="menu-item"><a href="#sobre">Sobre</a></li>'
        '<li class="menu-item"><a href="#areas">Áreas de atuação</a></li>'
        '<li class="menu-item"><a href="#contato">Contato</a></li></ul>')
s, k = re.subn(r'<ul id="menu-menu".*?</ul></div>', menu + '</div>', s, count=1, flags=re.S)
assert k == 1
s = s.replace('href="https://templatekit.jegtheme.com/justic" class="jkit-nav-logo"', 'href="#inicio" class="jkit-nav-logo"')
remove('f89e554')  # busca (enviava para o site do modelo)

# ---------------- Hero ----------------
add_id('465f6ace', 'inicio')
texts('465f6ace',
      ('We Fight For Justice', 'Escritório de Advocacia'),
      ('Always Uphold The Truth', 'Defendemos o seu direito com a lei'),
      ('Get Started', 'Fale conosco'),
      ('Learn More', 'Saiba mais'))
remove('50b8de44')  # parágrafo do banner
hrefs('465f6ace', '#contato', '#sobre')
_ov = '<div class="elementor-background-overlay"></div>'
_bg = '<div class="kv-hero-bg" aria-hidden="true"><span></span><span></span><span></span></div>'
def _hero_bg(c):
    assert c.count(_ov) >= 1
    return c.replace(_ov, _bg + _ov, 1)
edit('465f6ace', _hero_bg)

# ---------------- Destaques ----------------
a, b = el_range(s, 'b34b884')  # logos de prêmios fictícios -> texto
s = s[:a] + ('<div class="elementor-element kv-faixa"><p class="kv-faixa__kicker">Kersevani Advogados</p>'
             '<p class="kv-faixa__txt">Direito Público · Empresarial · Previdenciário · Trabalhista · Civil</p></div>') + s[b:]
remove('cde133b')  # coluna "Atuamos em 5 Áreas do Direito"
texts('e3ab767',
      ('Managed Centrally', 'Onde atendemos'),
      ('Lorem ipsum', '<span class="kv-uf"><b>AL</b><span>Maceió, Paripueira e Barra de Santo Antônio</span></span><span class="kv-uf"><b>SP</b><span>Itanhaém</span></span>'),
      )
edit('e3ab767', lambda c: re.sub(r'<div class="icon-box-button\s*">\s*<div class="btn-wrapper.*?</div>\s*</div>', '', c, flags=re.S))  # sem botão "Contato"

# ---------------- Sobre ----------------
add_id('2d34f5a8', 'sobre')
remove('05a3d5d')  # ícone (balança e pilastra) acima de "Agende sua consulta"
remove('000cbbc')  # contador "29+ anos de experiência"
edit('e7c9504', lambda c: re.sub(r'(<img[^>]*>)', lambda m: m.group(1) + '<div class="kv-anos"><b>26</b><span>anos de<br>atividade</span></div>', c, count=1))  # selo sobre a foto
_a, _b = el_range(s, '54dc5a50')  # dois boxes de ícone -> princípios do manifesto
s = s[:_a] + (
    '<div class="elementor-element kv-slider" data-kv-slider><button type="button" class="kv-prev" aria-label="Anterior">&#8249;</button><button type="button" class="kv-next" aria-label="Próximo">&#8250;</button><div class="kv-slides">'
    '<article class="kv-slide"><div class="kv-louro"><img src="images/louro.svg" alt=""><b>01</b></div><strong>Justiça</strong><span>Defendemos cada cliente com a verdade e dentro da lei.</span></article>'
    '<article class="kv-slide"><div class="kv-louro"><img src="images/louro.svg" alt=""><b>02</b></div><strong>Ética e sigilo</strong><span>Cada caso é tratado com confidencialidade e respeito.</span></article>'
    '<article class="kv-slide"><div class="kv-louro"><img src="images/louro.svg" alt=""><b>03</b></div><strong>Transparência</strong><span>Você sabe o que está acontecendo, quanto custa e o que esperar.</span></article>'
    '<article class="kv-slide"><div class="kv-louro"><img src="images/louro.svg" alt=""><b>04</b></div><strong>Dedicação</strong><span>Cada demanda é analisada individualmente, sem fórmulas prontas.</span></article>'
    '</div><div class="kv-dots"><button type="button" aria-label="Princípio 1"></button><button type="button" aria-label="Princípio 2"></button><button type="button" aria-label="Princípio 3"></button><button type="button" aria-label="Princípio 4"></button></div></div>') + s[_b:]
texts('2d34f5a8',
      ('about corporate', 'Sobre o escritório'),
      ('The Simple Choice', 'Manifesto do escritório Kersevani'),
      ('Lorem ipsum dolor sit amet, consectetur', 'Acreditamos que a advocacia é, antes de tudo, um compromisso com a verdade e com a justiça. Este é o nosso código de conduta: a forma como trabalhamos e o que você pode esperar de nós.'),
      )
remove('0c3e889')  # assinatura
remove('665f260')  # "Fundador · Kersevani Advogados"

# ---------------- Fundador (antigo "Skills") ----------------
remove('1f6fe08b')  # seção "Nosso fundador" removida a pedido

# ---------------- Áreas de atuação ----------------
add_id('4b54dd5', 'areas')
areas = [
    ('Business Law', 'Direito Empresarial', 'Suporte jurídico para empresas: contratos, questões societárias e prevenção de riscos.'),
    ('Education Law', 'Direito Público', 'Atuação junto à administração pública, licitações, concursos e servidores.'),
    ('Criminal Law', 'Direito Previdenciário', 'Aposentadorias, auxílios e benefícios junto ao INSS, na via administrativa e judicial.'),
    ('Tax Law', 'Direito Trabalhista', 'Relações de trabalho, verbas rescisórias e defesa de direitos do trabalhador.'),
    ('Real Estate Law', 'Direito Civil', 'Contratos, responsabilidade civil, indenizações e demandas cíveis em geral.'),
    ('Insurance Law', 'Outras demandas', 'Não encontrou o seu caso? Conte-nos a sua situação e indicaremos o melhor caminho.'),
]
pairs = []
for old, new, desc in areas:
    pairs += [(old, new), ('Lorem ipsum', desc), ('View Details', 'Saiba mais')]
texts('4b54dd5', *pairs)
edit('4b54dd5', lambda c: c.replace('aria-label="View Details"', 'aria-label="Saiba mais"'))
hrefs('4b54dd5', *['#contato'] * 6)

# ---------------- Galeria de casos (imagens não condizem) ----------------
remove('a3fd4b9')

# ---------------- Por que escolher (removido a pedido) ----------------
remove('244d3b5')

# ---------------- Depoimentos (fictícios) ----------------
remove('79eb67e2')

# ---------------- Contato (antigo "vagas") ----------------
add_id('7e2b5dc', 'contato')
texts('7e2b5dc', ('We Hiring For New Interns', 'Agende sua consulta'))
for wid in ('6f5e0b3', 'ae526c0'):
    texts(wid, ('Kapten Japa', TBD_END), ('justic@support.com', TBD_MAIL), ('+62 478-2240-190', TBD_TEL))
remove('8a7c9d5')  # formulário Mailchimp do modelo
remove('4b5e319')

# ---------------- Notícias (fictícias) ----------------
remove('1344cc6e')

# ---------------- Rodapés (desktop e mobile) ----------------
for heads, quick, serv, about, cons in (
        (None, 'd833659', 'c4da404', '84dc6ad', ('56d3166', '90ed1d1', 'd547922', '0918cc9')),
        (None, '2b1560c', '4207704', '8963789', ('8ee8ee6', '4da9903', '785dff7', '7906c89'))):
    texts(quick, ('About', 'Início'), ('Services', 'Sobre'), ('Blog', 'Áreas de atuação'), ('Contact', 'Fundador'), ('Product', 'Contato'))
    hrefs(quick, '#inicio', '#sobre', '#areas', '#fundador', '#contato')
    edit(quick, lambda c: re.sub(r'<li class="elementor-icon-list-item">\s*<a href="#fundador">.*?</li>', '', c, flags=re.S))
    texts(serv, ('Privacy Policy', 'Direito Público'), ('Support', 'Direito Empresarial'), ('Disclaimer', 'Direito Previdenciário'), ('FAQ', 'Direito Trabalhista'), ('Terms', 'Direito Civil'))
    hrefs(serv, *['#areas'] * 5)
    texts(about, ('Sed ut perspiciatis', 'Advocacia especializada em Direito Público, Empresarial, Previdenciário, Trabalhista e Civil.'))
    texts(cons[0], ('Free For Consultation', 'Agende sua consulta'))
    texts(cons[1], ('+62 478-2240-190', TBD_TEL))
    texts(cons[2], ('justic@support.com', TBD_MAIL), ('+62 478-2240-190', TBD_TEL))
    texts(cons[3], ('Copyright', '© 2026 Kersevani Advogados. Todos os direitos reservados.'))
for wid in ('1d8bfae', 'cc069df'):
    texts(wid, ('Quick Links', 'Links rápidos'))
for wid in ('2255727', 'a3f2a21'):
    texts(wid, ('Service Links', 'Áreas'))

# ---------------- Links restantes para o site do modelo ----------------
s = re.sub(r'href="https://templatekit\.jegtheme\.com/justic[^"]*"', 'href="#inicio"', s)

# atributo quebrado no HTML salvo do modelo (aparecia como texto ">)
assert s.count('data-item-indicator="<i aria-hidden=" true"="">"&gt;') == 1
s = s.replace('data-item-indicator="<i aria-hidden=" true"="">"&gt;', 'data-item-indicator="">')
# <i> quebrados do carrossel de logos (HTML salvo do modelo): deixavam o resto da página em itálico
_bad = re.compile(r'<i aria-hidden="\\&quot;true\\&quot;" class="\\&quot;fas" fa-angle-(?:left|right)\\"="">')
_n = len(_bad.findall(s)); s = _bad.sub('', s)
_out, _pos, _depth = [], 0, 0
for _m in re.finditer(r'<i[\s>][^>]*>|</i>', s):
    if _m.group(0) != '</i>': _depth += 1; continue
    if _depth: _depth -= 1; continue
    _out.append(s[_pos:_m.start()]); _pos = _m.end(); _n -= 1
_out.append(s[_pos:]); s = ''.join(_out)
assert _n == 0, _n
assert len(re.findall(r'<i[\s>]', s)) == s.count('</i>')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', errors='surrogateescape', newline='').write(s)

# Verificação: textos do modelo que sobraram
body = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s[s.find('<body'):], flags=re.S)
left = [w for w in ('Justic', 'Lorem', 'justic@', '+62', 'Read More', 'View Details', 'Bali') if w in body]
print('OK, sobras:', left, '| tamanho', len(s))
