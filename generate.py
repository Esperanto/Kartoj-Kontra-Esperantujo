import jinja2, yaml, os, html
import subprocess, textwrap, cairosvg

def generate_kartaro(kartoj, antauxpado_de_sxablono=""):
    """
    * args:
        kartoj - { "verdaj":
                       "bildo": "../img/verdaj_kartoj.png",
                       "fontkoloro": "#008000",
                       "antauxpado": "verda",
                       "kartoj":
                           ["teksto": "", ... ]
                 }
    """
    for nomo, kartarero in kartoj.items():
        for k in kartarero["kartoj"]: #trancxu tekston al sammlongaj lineoj
            k["teksto"] = [html.escape(s) for s in textwrap.wrap(k["teksto"], 20)]
        pagxoj = [kartarero["kartoj"][i:i+9] for i in range(0, len(kartarero["kartoj"]), 9)] #disigas la kartaro en pagxojn po de 9 kartoj

        for i, pagxo in enumerate(pagxoj):
            template_str = open(antauxpado_de_sxablono+"templates/sxablono.svg.jinja2").read()
            t = jinja2.Template(template_str)
            kartoj_offsets = zip(pagxo, [(0,0), (61,0), (122,0), (0,91), (61,91), (122,91), (0,182), (61,182), (122,182)])
            r = t.render(kartoj_offsets=kartoj_offsets, piedbildo=kartarero["bildo"], fontkoloro=kartarero["fontkoloro"])
            open(antauxpado_de_sxablono+'svg/{}.svg'.format(kartarero["antauxpado"]+str(i)), "w").write(r)
            print(i, 'svg/{}.svg'.format(kartarero["antauxpado"]+str(i)))
            cairosvg.svg2png(
                url=antauxpado_de_sxablono+'svg/{}.svg'.format(kartarero["antauxpado"]+str(i)),
                write_to=antauxpado_de_sxablono+'img/{}.png'.format(kartarero["antauxpado"]+str(i)),
                dpi=300
            )
        subprocess.check_output([
            'convert', antauxpado_de_sxablono+'img/{}[0-9].png'.format(kartarero["antauxpado"]),
            kartarero["antauxpado"]+'_kartaro.pdf'
        ])

if __name__ == '__main__':
    kartoj = yaml.safe_load(open("kartoj.yaml").read())   # listo de kartoj
    generate_kartaro(kartoj)
