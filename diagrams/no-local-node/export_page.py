"""Export one named page of a multi-page .drawio to PNG.

Usage: python3 export_page.py <file.drawio> <page name> <out.png> [scale]
"""
import copy, os, subprocess, sys, tempfile
import xml.etree.ElementTree as ET

src, name, out = sys.argv[1:4]
scale = sys.argv[4] if len(sys.argv) > 4 else '2'
page = next(d for d in ET.parse(src).getroot().iter('diagram') if d.get('name') == name)
mx = ET.Element('mxfile'); mx.append(copy.deepcopy(page))
fd, tmp = tempfile.mkstemp(suffix='.drawio', dir=os.path.dirname(os.path.abspath(out))); os.close(fd)
ET.ElementTree(mx).write(tmp, encoding='utf-8')
subprocess.run(['/Applications/draw.io.app/Contents/MacOS/draw.io', '-x', '-f', 'png', '-s', scale, '-b', '20', '-o', out, tmp], capture_output=True)
os.remove(tmp)
print(out)
