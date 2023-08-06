# Markdown to TeX, Notebook to Markdown
#   https://pypi.python.org/pypi/md2tex
# pip install md2tex
import glob, os, re, requests, sys, time
from collections import namedtuple

def to_bib(s):
    out = [r'\begin{thebibliography}{99}']
    for line in s.splitlines()[1:]:
        m = re.match('^- ([^#]+)#(.+)$', line)
        if m:
            g1, g2 = m.groups()
            out.append(f'\\bibitem{{{g2}}} {g1}')
        else:
            out.append(line)
    out.append(r'\end{thebibliography}')
    return '\n'.join(out)

def re_sub(t, ptn3, ptn4, ptn5, ptn6, ptn7, ptn8, ptn9, ptnm, ptnf):
    t = ptn3.sub('\\\\textbf{\\1}', t)
    t = ptn4.sub('\\\\ref{\\1}', t)
    t = ptn5.sub(to_index, t)
    t = ptn6.sub('\\\\verb|\\1|', t)
    t = ptn7.sub('$\\1$', t)
    t = ptn8.sub('\\\\texttt{\\1}', t)
    t = ptn9.sub('\\\\cite{\\1}', t)
    t = ptnm.sub('$\\1$', t)
    t = ptnf.sub('\\\\footnote{\\1}', t)
    return t

to_header_count = 0
def to_header(m):
    global to_header_count
    g1, g2, g3, g4 = m.groups()
    if g2.startswith('-'):
        return ''
    c = 'chapter' if g1 == '#' else 'section'
    ex, g2 = '', g2.split('_')[-1]
    if g3 == '+':
        g3 = '*'
        to_header_count += 1
        ex = ('\n\\addcontentsline{toc}{chapter}{%s}\n'%g2
              + '\\setcounter{chapter}{%d}\n'%to_header_count
              + ('\\renewcommand{\\thechapter}{\\Alph{chapter}}'
              if to_header_count == 1 else '')
              + '\\setcounter{section}{0}')
    l = '\\label{%s}' % g4 if g4 else ''
    return '\\%s%s{%s%s}%s' % (c, g3, g2, l, ex)

def to_index(m):
    g1, g2 = m.groups()
    return f'\\index{{{g2+"@"+g1 if g2 else g1}}}'

def to_tex(s):
    s = s.replace('# 00_はじめに\n',
        '\\chapter*{はじめに}\n\\thispagestyle{empty}\n')
    ptn1 = re.compile(r'^(#{1,2}) (.+?)((?:\*|\+)?)(?:|#(.+))$', re.M)
    ptn2 = re.compile(r'^\*\*(.+?)(\*?)\*\*$', re.M)
    ptn3 = re.compile(r'\*\*(.+?)\*\*')
    ptn4 = re.compile(r'<&(.+?)>')
    ptn5 = re.compile(r'<#(.+?)(?:|｜(.+?))>')
    ptn6 = re.compile(r'`(.+?)`')
    ptn7 = re.compile(r'$$(.+?)$$')
    ptn8 = re.compile(r'<=(.+?)>')
    ptn9 = re.compile(r'<@(.+?)>')
    ptnm = re.compile(r'\$\$([^$]+)\$\$')
    ptnf = re.compile(r'<%(.+?)>')
    ptni = re.compile(r'^((?:In|Out) \[[\d ]+\]:)$', re.M)
    ptnh = re.compile(r'^----------$', re.M)
    ptnx = re.compile(r'!\[(.*?)(?:|#(.*?))(?:|~(.*?))\]\((.*?)\)')
    ptns = [ptn3, ptn4, ptn5, ptn6, ptn7, ptn8, ptn9, ptnm, ptnf]
    out = []
    for lnormal, lcode, lindent, ltable, lquote in split_code(s):
        if lnormal:
            t = '\n\n'.join(lnormal)
            t = ptn1.sub(to_header, t)
            t = ptn2.sub('\\\\subsection\\2{\\1}', t)
            t = re_sub(t, *ptns)
            t = ptnh.sub('\\\\hrulefill', t)
            t = ptni.sub('\\\\verb|\\1|', t)
            t = ptnx.sub(to_fig, t)
            out.append((t + '\n\n') if t else '\n')
        if lcode:
            out.append('\\begin{lstlisting}[basicstyle=\\ttfamily'
                       '\\small, frame=single]\n'
                     + '\n'.join(t[4:] for t in lcode)
                     + '\n\end{lstlisting}\n')
        for lst, fnc in zip([lindent, ltable, lquote],
                            [to_indent, to_table, to_quote]):
            if lst:
                t = fnc(lst)
                t = re_sub(t, *ptns)
                out.append(t + '\n')
    return ''.join(out)

def to_indent(lindent):
    lvl, out = [], []
    for nl, isitm, s in lindent:
        while len(lvl) < nl + 1:
            lvl.append('itemize' if isitm else 'enumerate')
            out.append(r'%*s\begin{%s}' % (len(lvl)*2-2, '', lvl[-1]))
        while len(lvl) > nl + 1:
            out.append(r'%*s\end{%s}' % (len(lvl)*2-2, '', lvl[-1]))
            lvl.pop()
        out.append(r'%*s\item %s' % (len(lvl)*2, '', s))
    while len(lvl) > 0:
        out.append(r'%*s\end{%s}' % (len(lvl)*2-2, '', lvl[-1]))
        lvl.pop()
    return '\n'.join(out)

def multicolumn_conv(m):
    g1, g2, g3 = m.groups()
    return fr'\multicolumn{{{g1}}}{{{g2.replace("!", "|")}}}{{{g3}}}'

def to_table(ltable):
    global table_info
    ptnu = re.compile(r'<\+(\d)([^>]+)>([^|]+)')
    s = ltable[0]
    if s.startswith('| |') and len(ltable) == 1:
        table_info = TableInfo(*re.match('([^#]+)(?:#(.+)|)$', s[3:]).groups())
        return ''
    st = ['l'] * (s.count('|') - 1)
    ss = s.split('|')[1:-1]
    for i in range(len(ss)):
        m = re.match('^\\s*<~(.+?)>(.*)$', ss[i])
        if m:
            g1, g2 = m.groups()
            st[i] = f'p{{{g1}}}'
            ss[i] = ' ' + g2 + ' '
    out = ['\\begin{table}[htb]']
    if table_info.caption:
        out.append(f'  \\caption{{{table_info.caption}}}')
    if table_info.label:
        out.append(f'  \\label{{{table_info.label}}}')
    table_info = TableInfo('', '')
    out.append('  \\begin{tabular}{%s} \hline' % '|'.join(st))
    for s in ['|'.join(ss)] + ltable[2:]:
        tt = [ptnu.sub(multicolumn_conv, t.strip())
              for t in s[1:-1].split('|') if t.strip() != r'\empty']
        out.append('    ' + '&'.join(tt) + r'\\ \hline')
    out.append('  \\end{tabular}')
    out.append('\\end{table}')
    return '\n'.join(out)

def to_quote(lquote):
    return ('\\begin{quote}\n'
          + '\n\n'.join(s[2:] for s in lquote)
          + '\n\\end{quote}')

def to_fig(m):
    global figdc
    g1, g2, g3, g4 = m.groups()
    c = r'\caption{%s}' % g1 if g1 else ''
    l = r'\label{%s}' % g2 if g2 else ''
    if l and not c:
        print(f'\033[31mFigure #{g2} has no caption.\033[0m')
    w = g3 if g3 else '0.9'
    if g4 not in figdc:
        figdc[g4] = get_fig(g4)
    f = figdc[g4]
    return """\
\\begin{figure}[htb]
\\centering
\\includegraphics[keepaspectratio=true,width=%s\\linewidth,height=0.25\\paperheight]{%s}
%s%s
\\end{figure}""" % (w, f, c, l)

def get_fig(s):
    if not os.path.isdir('fig'):
        os.mkdir('fig')
    n = 0
    while True:
        n += 1
        fnam = f'fig/img{n:02d}.png'
        if not os.path.isfile(fnam):
            break
    r = requests.get(s)
    with open(fnam, 'wb') as fp:
        fp.write(r.content)
    time.sleep(0.5)
    return fnam

def yield_list(lnormal, lcode, lindent, ltable, lquote):
    yield lnormal, lcode, lindent, ltable, lquote
    lnormal[:], lcode[:], lindent[:], ltable[:], lquote[:] = [], [], [], [], []

def split_code(s):
    lnormal, lcode, lindent, ltable, lquote = [], [], [], [], []
    flag = False  # 前行がlindentかどうか
    for t in s.splitlines():
        if flag and t.startswith('  ') and not re.match('  (  |- |\d\.)', t):
            lindent[-1][-1] += r'\\' + t.lstrip()
            continue
        m = re.match(r'^((?:  ){0,3})(-|\d\.) (.+)$', t)
        flag = False
        if m:
            flag = True
            g1, g2, g3 = m.groups()
            if lnormal or lcode or ltable or lquote:
                yield from yield_list(lnormal, lcode, lindent, ltable, lquote)
            lindent.append([len(g1) // 2, g2 == '-', g3])
        elif t.startswith('    '):
            if lnormal or lindent or ltable or lquote:
                yield from yield_list(lnormal, lcode, lindent, ltable, lquote)
            lcode.append(t)
        elif t.startswith('| '):
            if lnormal or lcode or lindent or lquote:
                yield from yield_list(lnormal, lcode, lindent, ltable, lquote)
            ltable.append(t)
        elif t.startswith('> '):
            if lnormal or lcode or lindent or ltable:
                yield from yield_list(lnormal, lcode, lindent, ltable, lquote)
            lquote.append(t)
        else:
            if lcode or lindent or ltable or lquote:
                yield from yield_list(lnormal, lcode, lindent, ltable, lquote)
            lnormal.append(t)
    if lnormal or lcode or lindent or ltable or lquote:
        yield lnormal, lcode, lindent, ltable, lquote

def make_main_tex(fmain):
    with open(fmain, 'w') as fp:
        fp.write("""\
\\documentclass{jsbook}
\\usepackage[top=40truemm,bottom=38truemm,left=46truemm,right=45truemm]{geometry}
\\usepackage[dvipdfmx]{graphicx,color}
\\usepackage{color}
\\usepackage{listings}
\\usepackage{makeidx}
\\makeindex
\\begin{document}
\\title{\\huge TITLE}
\\author{AUTHOR}
\\date{\\today}
\\maketitle
%\\input{INST.tex}
\\tableofcontents
%\\input{CHAP1.tex}
\\printindex
\\end{document}
""")
    print(f'Output {fmain}')

def read_fig(ffig):
    lines = []
    if os.path.isfile(ffig):
        with open(ffig, encoding='utf8') as fp:
            lines = fp.readlines()
    return dict([s.split() for s in lines])
def write_fig(ffig, figdc):
    with open(ffig, 'w', encoding='utf8') as fp:
        for k, v in figdc.items():
            fp.write(f'{k} {v}\n')

figdc = {}  # URI -> fig file
TableInfo = namedtuple('TableInfo', ['caption', 'label'])
table_info = TableInfo('', '')

def main():
    global figdc, table_info
    fmain, ffig = 'main.tex', 'fig.txt'  # このファイルは常にカレント
    ptnx = re.compile(r'!\[(.*?)(?:|#(.*?))(?:|~(.*?))\]\((.*?)\)')
    mrkflg = (sys.argv + [''])[1] == '--mark'  # 「、。」→「，．」
    delfig = (sys.argv + [''])[1] == '--delete'  # 不要なpngを削除
    fndfig = set()
    if not delfig and not os.path.isfile(fmain):
        make_main_tex(fmain)
    figdc = read_fig(ffig)
    ntop = int(mrkflg) + int(delfig) + 1
    top = sys.argv[ntop] if len(sys.argv) > ntop else '.'
    for dr, _, fils in os.walk(top):
        for fil in fils:
            if not fil.endswith('.md'):
                continue
            fnam = os.path.join(dr, fil)
            with open(fnam, encoding='utf8') as fp:
                s = fp.read()
                if mrkflg:
                    s = s.replace('、', '，').replace('。', '．')
            if delfig:
                for g in ptnx.findall(s):
                    fndfig.add(g[3])
            else:
                s = to_bib(s) if '参考文献' in s[:10] else to_tex(s)
                tnam = fnam[:-3] + '.tex'
                with open(tnam, 'w', encoding='utf8') as fp:
                    fp.write(s)
                print(f'Output {tnam}')
    if delfig:
        for k in list(figdc):
            if k not in fndfig:
                del figdc[k]  # mdに存在しない値を削除
        for f in set(glob.glob('fig/*')) - set(figdc.values()):
            print(f'Delete {f}')
            os.remove(f)
    write_fig(ffig, figdc)

def nb2md(ptn, nb, fp):
    """Notebook to Markdown"""
    for ce in nb.get('cells', []):
        ct = ce.get('cell_type')
        sc = ce.get('source')
        if ct == 'markdown':
            sc = ptn.sub(r'**\2**', sc)
            fp.write(f'{sc}\n')
        elif ct == 'code':
            ec = ce.get('execution_count') or ' '
            fp.write(f'In [{ec}]:\n\n')
            for s in sc.splitlines():
                fp.write(f'    {s}\n')
            fp.write('\n')
            ops = []
            for op in ce.get('outputs', []):
                tt = op.get('text')
                if tt:
                    fp.write(f'> {tt}\n')
                dc = op.get('data', {})
                if 'image/png' not in dc:
                    for k, v in dc.items():
                        ops.append(v)
            if ops:
                fp.write(f'Out [{ec}]:\n\n    ')
                fp.write('\n    '.join(ops))
                fp.write('\n\n')

def nb2md_all():
    """Notebook to Markdown"""
    import nbformat
    ptn = re.compile(r'^(#{3,}) (.+?)$', re.M)
    kw = 'text/plain'
    top = sys.argv[1] if len(sys.argv) > 1 else '.'
    for dr, _, fils in os.walk(top):
        if dr.endswith('.ipynb_checkpoints'):
            continue
        for fil in fils:
            if not fil.endswith('.ipynb'):
                continue
            fnam = os.path.join(dr, fil)
            with open(fnam, encoding='utf8') as fp:
                nb = nbformat.read(fp, 4)
            tnam = fnam[:-6] + '.md'
            with open(tnam, 'w', encoding='utf8') as fp:
                nb2md(ptn, nb, fp)
            print(f'Output {tnam}')

if __name__ == '__main__':
    main()
