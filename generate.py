import jinja2, yaml, os
import subprocess, textwrap

kartoj = yaml.safe_load(open("kartoj.yaml").read())   # listo de kartoj

for nomo, kartarero in kartoj.items():
    for k in kartarero["kartoj"]: #trancxu tekston al sammlongaj lineoj
        k["teksto"] = textwrap.wrap(k["teksto"], 20)
    pagxoj = [kartarero["kartoj"][i:i+9] for i in range(0, len(kartarero["kartoj"]), 9)] #disigas la kartaro en pagxojn po de 9 kartoj

    for i, pagxo in enumerate(pagxoj):
        template_str = open("templates/sxablono.svg.jinja2").read()
        t = jinja2.Template(template_str)
        kartoj_offsets = zip(pagxo, [(0,0), (61,0), (122,0), (0,91), (61,91), (122,91), (0,182), (61,182), (122,182)])
        r = t.render(kartoj_offsets=kartoj_offsets, piedbildo=kartarero["bildo"], fontkoloro=kartarero["fontkoloro"])
        open('svg/{}.svg'.format(kartarero["antauxpado"]+str(i)), "w").write(r)
        subprocess.check_output(['inkscape','-z', '--export-dpi', '300', 'svg/{}.svg'.format(kartarero["antauxpado"]+str(i)), '-e', 'img/{}.png'.format(kartarero["antauxpado"]+str(i))])
    subprocess.check_output(['convert', 'img/{}[0-9].png'.format(kartarero["antauxpado"]), kartarero["antauxpado"]+'_kartaro.pdf'])
