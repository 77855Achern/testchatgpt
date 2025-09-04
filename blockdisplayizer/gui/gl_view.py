"""Minimal ModernGL viewport for preview."""
from __future__ import annotations

from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
import moderngl
import numpy as np


class GLViewWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ctx: moderngl.Context | None = None
        self.program = None
        self.vbo = None
        self.rotation = np.eye(4)

    def initializeGL(self) -> None:
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)
        vertices = np.array(
            [
                -0.5,
                -0.5,
                -0.5,
                0.5,
                -0.5,
                -0.5,
                0.0,
                0.5,
                -0.5,
            ],
            dtype="f4",
        )
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.program = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec3 in_pos;
                uniform mat4 M;
                void main(){
                    gl_Position = M * vec4(in_pos,1.0);
                }
            """,
            fragment_shader="""
                #version 330
                out vec4 f_color;
                void main(){ f_color = vec4(0.8,0.8,0.8,1.0); }
            """,
        )

    def paintGL(self) -> None:
        if not self.ctx:
            return
        self.ctx.clear(0.2, 0.2, 0.25, 1.0)
        if self.program and self.vbo:
            self.program["M"].write(self.rotation.astype("f4").tobytes())
            vao = self.ctx.simple_vertex_array(self.program, self.vbo, "in_pos")
            vao.render(moderngl.TRIANGLES)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        event.accept()
