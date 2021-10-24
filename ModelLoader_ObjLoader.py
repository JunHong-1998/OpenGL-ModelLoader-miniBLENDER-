import numpy as np
import pygame
from OpenGL.GL import *

def MTL(fdir, filename):
    contents = {}
    mtl = file = None
    for line in open(fdir + filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        elif values[0] == 'map_Kd':
            value = ""
            for i in range(1, len(values)):
                value += values[i]
            mtl[values[0]] = value
            file = mtl['map_Kd']
            if file.count('\\') == 0:
                pass
            else:
                divider = ([pos for pos, char in enumerate(file) if char == '\\'])
                file = file[max(divider) + 1:len(file)]
            try:
                surf = pygame.image.load(fdir + file)
            except Exception:
                raise ValueError("file path incorrect", file)
            image = pygame.image.tostring(surf, 'RGBA', 1)
            ix, iy = surf.get_rect().size
            texid = mtl['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        elif values[0] == 'map_Ka' or values[0] == 'map_Ks' or values[0] == 'map_bump' or values[0] == 'bump':
            pass
        else:
            mtl[values[0]] = [float(x) for x in values[1:4]]
    return contents, file

class OBJ:
    def __init__(self, fdir, filename):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.mtl = None
        self.ReLoad = False
        self.color_new = False
        self.Tex_ON = -1
        self.Alpha = 1

        material = None
        for line in open(fdir + filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = [float(x) for x in values[1:4]]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = [float(x) for x in values[1:4]]
                self.normals.append(v)
            elif values[0] == 'vt':
                v = [float(x) for x in values[1:3]]
                self.texcoords.append(v)
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = [fdir, values[1]]
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        ps = np.array(self.vertices)
        vmin = ps.min(axis=0)
        vmax = ps.max(axis=0)
        c = ((vmax + vmin) / 2).tolist()
        self.center = round(c[0],6), round(c[1],6), round(c[2],6)

    def create_gl_list(self):
        if self.mtl and not self.ReLoad:
            self.mtl, self.file = MTL(*self.mtl)
            if self.file:
                self.Tex_ON = 1
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)

        glFrontFace(GL_CCW)

        for face in self.faces:
            vertices, normals, texture_coords, material = face
            if self.mtl:
                mtl = self.mtl[material]
                if not self.color_new:
                    self.color = mtl['Kd'][0], mtl['Kd'][1], mtl['Kd'][2], 1.00
                if self.Tex_ON==1 and 'texture_Kd' in mtl:
                    glEnable(GL_TEXTURE_2D)
                    # glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
                    glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
                    glColor4f(1, 1, 1, self.Alpha)
                else:
                    glColor4fv(self.color)

            glBegin(GL_TRIANGLES)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
