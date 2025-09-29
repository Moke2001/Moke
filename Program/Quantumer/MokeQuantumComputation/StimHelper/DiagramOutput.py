from svglib.svglib import svg2rlg
import pathlib


def DiagramOutput(circuit,filename,path,method):

    svg_src = str(circuit.diagram(type=method))

    out_dir = pathlib.Path(path)  # 换成你想放的目录
    out_file = out_dir / (filename+".svg")

    # 4. 写入文件
    out_file.write_text(svg_src, encoding='utf-8')

    drawing = svg2rlg(filename+".svg")