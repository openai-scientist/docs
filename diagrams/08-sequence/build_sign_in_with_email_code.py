"""Build the standalone Email Code view from the shared sequence definition."""
from pathlib import Path
import xml.etree.ElementTree as E
from build_sequence_groups import draw_page
from sequence_flows import GROUPS

OUT = Path(__file__).resolve().parent
NAME = 'Sequence-Diagram-Sign-In-With-Email-Code'


def build():
    mx = E.Element('mxfile', host='drawio', version='26.0.0')
    mx.append(draw_page(GROUPS[0]['flows'][0], 'email-code'))
    E.indent(mx, space='  ')
    path = OUT / f'{NAME}.drawio'
    E.ElementTree(mx).write(path, encoding='utf-8', xml_declaration=True)
    print(path)


if __name__ == '__main__':
    build()
