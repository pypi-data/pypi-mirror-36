# -*- coding: utf-8 -*-
import base64
import urllib
from . import imgsize
from graphviz import Source

from ipykernel.kernelbase import Kernel


class DotKernel(Kernel):
    implementation = "graphviz"
    implementation_version = "2.40.1"
    language = "dot"
    language_version = "latest"
    language_info = {
        "name": "dot",
        "mimetype": "text/plain",
        "file_extension": ".gv",
    }
    banner = "Dot language - render graph using graphviz."

    def do_execute(
        self, code, silent, store_history=True,
        user_expressions=None, allow_stdin=False
    ):
        src = Source(code)
        png_src = src.pipe(format="png")
        if not silent:
            data = urllib.parse.quote(base64.b64encode(png_src))
            width, height = imgsize.get_png_size(png_src)
            stream_content = {
                "metadata": {"image/png": {"width": width, "height": height}},
                "data": {"image/png": data},
            }

            self.send_response(self.iopub_socket, "display_data", stream_content)

        return {
            "status": "ok",
            # The base class increments the execution count
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }
