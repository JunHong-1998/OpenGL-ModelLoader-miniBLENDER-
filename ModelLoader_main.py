import os
import random
from pygame.locals import *
from OpenGL.GLU import *
from ModelLoader_UserInterface import*
from ModelLoader_ObjLoader import*
UI = UserInterface()
class Model_main:
    def __init__(self):
        self.MDL_list = 0
        self.MDL = []
        self.MDLH = []
        self.MDLS = []
        self.app = False
        self.pos = []
        self.LoadEnd = False

    def Select_Detection(self, pos):
        if UI.Mdl_list>0 and 220 < pos[0] < 250 and 45 < pos[1] < 211:
            if 45 < pos[1] < 75 and UI.Mdl_list>=1:
                UI.LP_Mdl_Del = 0
            elif 78 < pos[1] < 110 and UI.Mdl_list>=2:
                UI.LP_Mdl_Del = 1
            elif 113 < pos[1] < 145 and UI.Mdl_list>=3:
                UI.LP_Mdl_Del = 2
            elif 145 < pos[1] < 177 and UI.Mdl_list>=4:
                UI.LP_Mdl_Del = 3
            elif 178 < pos[1] < 210 and UI.Mdl_list==5:
                UI.LP_Mdl_Del = 4
            else:
                UI.LP_Mdl_Del = -1
        else:
            UI.LP_Mdl_Del = -1

    def EnvRot(self, rx, ry):
        if rx==0 and ry==0:
            UI.ortho = 1
        elif rx==270 and ry==0:
            UI.ortho = 3
        elif rx==0 and ry==90:
            UI.ortho = 7
        elif rx==0 and ry==270:
            UI.ortho = 9
        else:
            UI.ortho = 0

    def Rot_clear(self, rot):
        final = rot
        if rot>360 or rot<-360:
            n = rot/360
            final = rot-360*int(n)
        return final

    def LoadOBJ_internal(self):
        for i in range(len(UI.MdlH)):
            self.MDLH.append(OBJ("ext/Internal/", UI.MdlH[i]))
            self.MDLH[i].create_gl_list()
            UI.MdlH_TexOn.append(self.MDLH[i].Tex_ON)
            UI.MdlH_Alpha.append(1)
            UI.MdlH_TexFile.append(self.MDLH[i].file)
            UI.MdlH_RGBA.append([int(self.MDLH[i].color[0]*255),int(self.MDLH[i].color[1]*255),int(self.MDLH[i].color[2]*255),self.MDLH[i].color[3]])
            UI.MdlH_POS.append([self.MDLH[i].center[0], self.MDLH[i].center[1],self.MDLH[i].center[2]])
            UI.MdlH_POS_ORI.append([self.MDLH[i].center[0], self.MDLH[i].center[1],self.MDLH[i].center[2]])
            UI.MdlH_DEG.append([0,0,0])
            UI.MdlH_SCL.append([1,1,1])

    def LoadOBJ(self):
        self.MDL.clear()
        self.MDL_list = UI.Mdl_list
        for i in range(self.MDL_list):
            if i==0 and UI.int:
                fdir = 'ext/Internal/'
            else:
                fdir = 'ext/'
            self.MDL.append(OBJ(fdir, UI.Mdl[i]))
            self.MDL[i].create_gl_list()
            if UI.LP_Mdl_Del==-1 and self.MDL_list-1==i:
                UI.Mdl_TexFile.append(self.MDL[i].file)
                UI.Mdl_TexOn.append(self.MDL[i].Tex_ON)
                UI.Mdl_POS.append([self.MDL[i].center[0], self.MDL[i].center[1],self.MDL[i].center[2]])
                UI.Mdl_POS_ORI.append([self.MDL[i].center[0], self.MDL[i].center[1], self.MDL[i].center[2]])
                UI.Mdl_RGBA.append([int(self.MDL[i].color[0]*255),int(self.MDL[i].color[1]*255),int(self.MDL[i].color[2]*255),self.MDL[i].color[3]])
                UI.Mdl_DEG.append([0,0,0])
                UI.Mdl_SCL.append([1,1,1])
                UI.Mdl_Alpha.append(1)
            UI.LP_Mdl_Slc = self.MDL_list-1
            if UI.int:
                UI.LP_intMdl_Slc = -1
                if UI.Mdl_list>1:
                    UI.LP_Hrc_Slc = -1

    def RELoadOBJ(self):
        if UI.int and UI.LP_Mdl_Slc==0:
            if UI.LP_Hrc_Slc==0:
                for i in range(len(self.MDLH)):
                    self.MDLH[i].ReLoad = True
            else:
                self.MDLH[UI.LP_intMdl_Slc].ReLoad = True
        else:
            self.MDL[UI.LP_Mdl_Slc].ReLoad = True
        if UI.RP_Slc==6:
            if UI.int and UI.LP_Mdl_Slc==0:
                clr = UI.MdlH_RGBA[UI.LP_intMdl_Slc]
            else:
                clr = UI.Mdl_RGBA[UI.LP_Mdl_Slc]
            if UI.int and UI.LP_Mdl_Slc==0:
                if UI.LP_Hrc_Slc==0:
                    for i in range(len(self.MDLH)):
                        clr = UI.MdlH_RGBA[i]
                        if self.MDLH[i].color_new:
                            self.MDLH[i].color = clr[0] / 255, clr[1] / 255, clr[2] / 255, clr[3]
                            self.MDLH[i].create_gl_list()
                        else:
                            self.MDLH[i].create_gl_list()
                            clr[0], clr[1], clr[2], clr[3] = int(self.MDLH[i].color[0] * 255), int(self.MDLH[i].color[1] * 255), int(self.MDLH[i].color[2] * 255), self.MDLH[i].color[3]
                elif self.MDLH[UI.LP_intMdl_Slc].color_new:
                    self.MDLH[UI.LP_intMdl_Slc].color = clr[0] / 255, clr[1] / 255, clr[2] / 255, clr[3]
                    self.MDLH[UI.LP_intMdl_Slc].create_gl_list()
                else:
                    self.MDLH[UI.LP_intMdl_Slc].create_gl_list()
                    clr[0], clr[1], clr[2], clr[3] = int(self.MDLH[UI.LP_intMdl_Slc].color[0] * 255), int(self.MDLH[UI.LP_intMdl_Slc].color[1] * 255), int(self.MDLH[UI.LP_intMdl_Slc].color[2] * 255), self.MDLH[UI.LP_intMdl_Slc].color[3]
            else:
                if self.MDL[UI.LP_Mdl_Slc].color_new:
                    self.MDL[UI.LP_Mdl_Slc].color = clr[0] / 255, clr[1] / 255, clr[2] / 255, clr[3]
                    self.MDL[UI.LP_Mdl_Slc].create_gl_list()
                else:
                    self.MDL[UI.LP_Mdl_Slc].create_gl_list()
                    clr[0], clr[1], clr[2], clr[3] = int(self.MDL[UI.LP_Mdl_Slc].color[0] * 255), int(self.MDL[UI.LP_Mdl_Slc].color[1] * 255), int(self.MDL[UI.LP_Mdl_Slc].color[2] * 255), self.MDL[UI.LP_Mdl_Slc].color[3]  
        elif UI.RP_Slc==7:
            if UI.int and UI.LP_Mdl_Slc==0:
                if UI.LP_Hrc_Slc==0:
                    for i in range(len(self.MDLH)):
                        self.MDLH[i].Alpha = UI.MdlH_Alpha[i]
                        self.MDLH[i].Tex_ON = UI.MdlH_TexOn[i]
                        self.MDLH[i].create_gl_list()
                else:
                    self.MDLH[UI.LP_intMdl_Slc].Alpha = UI.MdlH_Alpha[UI.LP_intMdl_Slc]
                    self.MDLH[UI.LP_intMdl_Slc].Tex_ON = UI.MdlH_TexOn[UI.LP_intMdl_Slc]
                    self.MDLH[UI.LP_intMdl_Slc].create_gl_list()
            else:
                self.MDL[UI.LP_Mdl_Slc].Alpha = UI.Mdl_Alpha[UI.LP_Mdl_Slc]
                self.MDL[UI.LP_Mdl_Slc].Tex_ON = UI.Mdl_TexOn[UI.LP_Mdl_Slc]
                self.MDL[UI.LP_Mdl_Slc].create_gl_list()

    def LoadOBJ_screen(self):
        props = ["Leave2.obj","Leave.obj","Leave1.obj","Leave2.obj","Leave.obj","Leave1.obj","Leave2.obj","Leave.obj","Leave1.obj","Leave2.obj",
                 "Leave.obj","Leave1.obj","Leave2.obj","Leave.obj","Leave1.obj","Leave2.obj","Leave.obj","Leave1.obj","Leave4.obj","Leave3.obj"]
        for i in range(len(props)):
            self.MDLS.append(OBJ("ext/Internal/", props[i]))
            if i == len(props)-1:
                self.MDLS[i].Alpha = 0
            self.MDLS[i].create_gl_list()
            if i<len(props)-2:
                x = random.randint(-5,5)
                y = random.randint(-20,0)
                z = random.randint(5,10)
                self.pos.append([x, y, z])
            else:
                self.pos.append([0,-20,8,0])
        self.MDLS[-1].ReLoad = True

    def LoadScreen(self):
        glClearColor(0,0,0, 1)
        Delete_list = []
        for i in range(len(self.MDLS)):
            if Delete_list and len(self.MDLS)==2:
                break
            pos = self.pos[i]
            if pos[1]>-48:
                glPushMatrix()
                glTranslate(pos[0], pos[1], -20)
                glRotate(pos[1] * pos[2]/100, 0, 0, 1)
                glRotate(pos[1] * pos[2], 0, 1, 0)
                glCallList(self.MDLS[i].gl_list)
                pos[1] -= pos[2]/500
                glPopMatrix()
            else:
                Delete_list.append(i)
        if Delete_list:
            if len(Delete_list)==len(self.MDLS):
                del self.MDLS[0:len(self.MDLS)-2]
        if len(self.MDLS)==2:
            self.MDLS[-1].Alpha +=0.005
            self.MDLS[-1].create_gl_list()
        for i in range(-2,0):
            pos = self.pos[i]
            if pos[1]<=-48:
                glPushMatrix()
                glTranslate(pos[0], pos[1], -20)
                glRotate(pos[1] * pos[2] / 100, 0, 0, 1)
                glRotate(pos[1] * pos[2], 0, 1, 0)
                glCallList(self.MDLS[i].gl_list)
                glPopMatrix()
                if len(self.MDLS)==2:
                    pos[3] = 1
            elif len(self.MDLS)==2 and pos[1]<-30 and pos[3]==1:
                glPushMatrix()
                glTranslate(pos[0], pos[1], -20)
                glRotate(pos[1] * pos[2] / 100, 0, 0, 1)
                glRotate(pos[1] * pos[2], 0, 1, 0)
                glCallList(self.MDLS[i].gl_list)
                glPopMatrix()
            elif len(self.MDLS) == 2 and pos[1] >-40 and pos[3]==2:
                y = pos[1]-(pos[1]+30)
                glPushMatrix()
                glTranslate(pos[0], y, -20)
                glRotate(pos[1] * pos[2] / 100, 0, 0, 1)
                glRotate(pos[1] * pos[2], 0, 1, 0)
                glCallList(self.MDLS[i].gl_list)
                glPopMatrix()
            elif pos[3] == 3:
                y = pos[1] - (pos[1] + 46)
                glPushMatrix()
                glTranslate(0, y, -20)
                glScale(1.4, 1.4, 1.4)
                glRotate(pos[2], 0, 1, 0)
                glCallList(self.MDLS[i].gl_list)
                glPopMatrix()
                glColor3ub(212, 175, 55)
                glPushMatrix()
                glScalef(0.15, 0.1 / 2, 1)
                glTranslatef(-480, -200, -80)
                for ch in "MODEL LOADER":
                    glutStrokeCharacter(GLUT_STROKE_ROMAN, ctypes.c_int(ord(ch)))
                glPopMatrix()
                glWindowPos2f(530, 280)
                for ch in "LOW JUN HONG":
                    glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ctypes.c_int(ord(ch)))
            if self.MDLS[-1].Alpha>0.03:
                pos[1] += pos[2] / 50
                if pos[1]>0.3:
                    pos[3] = 3
                    pos[2] += 0.8
                    self.LoadEnd = True
                elif pos[1]>=-30:
                    pos[3] = 2

    def main(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mixer.init()
        glutInit()
        display = (1250, 750)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('MODEL LOADER by Low Jun Hong BS18110173')
        glViewport(0, 0, display[0], display[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, (display[0] / display[1]), 0.1, 1000)
        glMatrixMode(GL_MODELVIEW)
        self.LoadOBJ_screen()
        self.LoadOBJ_internal()
        self.LoadOBJ()
        shift = ax = ay = az = roller = crop = False
        tsf = rlr = -1
        rx, ry, rz = 0, 0, 0
        tx, ty, tz = 0, 0, 0
        sx, sy, sz = 1, 1, 1
        xrot, yrot = 0,0
        ratx, raty = [0,0], [0,0]
        while True:
            if UI.exit==2:
                pygame.quit()
                quit()
            Cursor = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif not self.app:
                    if self.LoadEnd:
                        if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
                            self.app = True
                            self.MDLS.clear()
                        else:
                            break
                    else:
                        break
                elif UI.exit==1:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            UI.exit = 2
                            break
                        elif event.key == K_ESCAPE:
                            UI.exit = 0
                            UI.RP_Slc = -1
                            break
                    elif event.type == MOUSEBUTTONDOWN:
                        UI.exit = 0
                        UI.RP_Slc = -1
                        break
                elif event.type == MOUSEBUTTONDOWN:
                    if UI.image[3]:
                        UI.image[3]=False
                    if event.button == 1:
                        if 1200<Cursor[0]<1243 and 5<Cursor[1]<520: # RightPanel
                            if 5<Cursor[1]<50:
                                UI.RP_Slc = 0
                                UI.exit = 1
                            elif 55<Cursor[1]<100:
                                UI.RP_Slc = 1
                            elif 110<Cursor[1]<155:
                                UI.RP_Slc = 2
                            elif 160<Cursor[1]<205 and UI.Mdl:
                                UI.RP_Slc = 3
                            elif 215<Cursor[1]<260 and UI.Mdl:
                                if not UI.LP_Hrc_Slc == 0:
                                    UI.RP_Slc = 4
                            elif 265<Cursor[1]<310 and UI.Mdl:
                                if not UI.LP_Hrc_Slc == 0:
                                    UI.RP_Slc = 5
                            elif 320<Cursor[1]<365 and UI.Mdl:
                                UI.RP_Slc = 6
                            elif 370<Cursor[1]<415 and UI.Mdl:
                                UI.RP_Slc = 7
                            elif 425<Cursor[1]<470:
                                UI.RP_Slc = 8
                            elif 475<Cursor[1]<525:
                                UI.RP_Slc = 9
                        elif 5<Cursor[0]<211 and 45<Cursor[1]<211:
                            if 45<Cursor[1]<75:
                                UI.LP_Mdl_Slc = 0
                                if UI.int:
                                    UI.LP_Hrc_Slc = 0
                            elif 78<Cursor[1]<110 and UI.Mdl_list>=2:
                                UI.LP_Mdl_Slc = 1
                                UI.LP_intMdl_Slc = UI.LP_Hrc_Slc = -1
                            elif 113 < Cursor[1] < 145 and UI.Mdl_list>=3:
                                UI.LP_Mdl_Slc = 2
                                UI.LP_intMdl_Slc = UI.LP_Hrc_Slc = -1
                            elif 145 < Cursor[1] < 177 and UI.Mdl_list>=4:
                                UI.LP_Mdl_Slc = 3
                                UI.LP_intMdl_Slc = UI.LP_Hrc_Slc = -1
                            elif 178 < Cursor[1] < 210 and UI.Mdl_list>=5:
                                UI.LP_Mdl_Slc = 4
                                UI.LP_intMdl_Slc = UI.LP_Hrc_Slc = -1
                        elif 5 < Cursor[0] < 250 and 472 < Cursor[1] < 489 and UI.int and UI.LP_Mdl_Slc==0:
                            if 5<Cursor[0]<85:
                                UI.LP_Hrc_Slc = 0
                                UI.LP_intMdl_Slc = -1
                            elif 89<Cursor[0]<166:
                                UI.LP_Hrc_Slc = 1
                            elif 171<Cursor[0]<250:
                                UI.LP_Hrc_Slc = 2
                        elif 5 < Cursor[0] < 250 and 493 < Cursor[1] < 747 and UI.int and UI.LP_Mdl_Slc == 0:
                            if UI.LP_Hrc_Slc == 1:
                                if 5 < Cursor[0] < 128 and 493 < Cursor[1] < 749:
                                    if 493 < Cursor[1] < 518:
                                        UI.LP_intMdl_Slc = 0
                                    elif 519 < Cursor[1] < 544:
                                        UI.LP_intMdl_Slc = 1
                                    elif 545 < Cursor[1] < 570:
                                        UI.LP_intMdl_Slc = 2
                                    elif 571 < Cursor[1] < 596:
                                        UI.LP_intMdl_Slc = 3
                                    elif 597 < Cursor[1] < 622:
                                        UI.LP_intMdl_Slc = 4
                                    elif 623 < Cursor[1] < 649:
                                        UI.LP_intMdl_Slc = 5
                                    elif 650 < Cursor[1] < 675:
                                        UI.LP_intMdl_Slc = 6
                                    elif 676 < Cursor[1] < 700:
                                        UI.LP_intMdl_Slc = 7
                                    elif 701 < Cursor[1] < 727:
                                        UI.LP_intMdl_Slc = 8
                                    elif 728 < Cursor[1] < 749:
                                        UI.LP_intMdl_Slc = 9
                                elif 129 < Cursor[0] < 250 and 493 < Cursor[1] < 727:
                                    if 493 < Cursor[1] < 518:
                                        UI.LP_intMdl_Slc = 10
                                    elif 519 < Cursor[1] < 544:
                                        UI.LP_intMdl_Slc = 11
                                    elif 545 < Cursor[1] < 570:
                                        UI.LP_intMdl_Slc = 12
                                    elif 571 < Cursor[1] < 596:
                                        UI.LP_intMdl_Slc = 13
                                    elif 597 < Cursor[1] < 622:
                                        UI.LP_intMdl_Slc = 14
                                    elif 623 < Cursor[1] < 649:
                                        UI.LP_intMdl_Slc = 15
                                    elif 650 < Cursor[1] < 675:
                                        UI.LP_intMdl_Slc = 16
                                    elif 676 < Cursor[1] < 700:
                                        UI.LP_intMdl_Slc = 17
                                    elif 701 < Cursor[1] < 727:
                                        UI.LP_intMdl_Slc = 18
                            elif UI.LP_Hrc_Slc == 2:
                                if 5 < Cursor[0] < 250 and 493 < Cursor[1] < 716:
                                    if 493 < Cursor[1] < 524:
                                        UI.LP_intMdl_Slc = 19
                                    elif 525 < Cursor[1] < 557:
                                        UI.LP_intMdl_Slc = 20
                                    elif 559 < Cursor[1] < 589:
                                        UI.LP_intMdl_Slc = 21
                                    elif 590 < Cursor[1] < 620:
                                        UI.LP_intMdl_Slc = 22
                                    elif 621 < Cursor[1] < 652:
                                        UI.LP_intMdl_Slc = 23
                                    elif 653 < Cursor[1] < 683:
                                        UI.LP_intMdl_Slc = 24
                                    elif 684 < Cursor[1] < 716:
                                        UI.LP_intMdl_Slc = 25
                        if UI.Mdl_Add:
                            UI.Reset_Selection()
                        elif UI.LP_Mdl_Del>-1:          ### MDL del del 1st, UI.int false, hrc_slc=-1, intMdl=-1, clear UI.MDLH
                            UI.Mdl.pop(UI.LP_Mdl_Del)
                            UI.Mdl_POS.pop(UI.LP_Mdl_Del)
                            UI.Mdl_POS_ORI.pop(UI.LP_Mdl_Del)
                            UI.Mdl_RGBA.pop(UI.LP_Mdl_Del)
                            UI.Mdl_DEG.pop(UI.LP_Mdl_Del)
                            UI.Mdl_SCL.pop(UI.LP_Mdl_Del)
                            UI.Mdl_TexFile.pop(UI.LP_Mdl_Del)
                            UI.Mdl_Alpha.pop(UI.LP_Mdl_Del)
                            UI.Mdl_TexOn.pop(UI.LP_Mdl_Del)
                            UI.Mdl_list -= 1
                            UI.LP_Mdl_Slc = -1
                            if UI.LP_Mdl_Del ==0 and UI.int:
                                UI.int = False
                                UI.LP_Hrc_Slc = UI.LP_intMdl_Slc = -1
                                UI.MdlH.clear()
                                self.MDLH.clear()
                                UI.MdlH_POS.clear()
                                UI.MdlH_POS_ORI.clear()
                                UI.MdlH_RGBA.clear()
                                UI.MdlH_DEG.clear()
                                UI.MdlH_SCL.clear()
                                UI.MdlH_TexFile.clear()
                                UI.MdlH_Alpha.clear()
                                UI.MdlH_TexOn.clear()
                            self.LoadOBJ()
                        elif UI.LP_Mdl_Add:
                            if 5 < Cursor[0] < 250 and 45 < Cursor[1] < 211:
                                if UI.Mdl_list==0 and 45 < Cursor[1] < 75 or UI.Mdl_list==1 and 78 < Cursor[1] < 110 or UI.Mdl_list==2 and 112 < Cursor[1] < 145\
                                    or UI.Mdl_list==3 and 145 < Cursor[1] < 177 or UI.Mdl_list==4 and  178 < Cursor[1] < 211:
                                    UI.Mdl_Add = True
                                    UI.Mdl_Add_Complete = False
                        if 5<Cursor[0]<250 and 411<Cursor[1]<435:
                            if UI.RP_Slc==6:
                                self.MDL[UI.LP_Mdl_Slc].color_new = False
                                self.RELoadOBJ()
                            elif UI.RP_Slc==7:
                                self.MDL[UI.LP_Mdl_Slc].Alpha = 1
                                if not UI.Mdl_TexOn[UI.LP_Mdl_Slc]==-1:
                                    self.MDL[UI.LP_Mdl_Slc].Tex_ON = 1
                                self.RELoadOBJ()
                            UI.Reset_Tool()
                        elif UI.color_picker==0 and 258<Cursor[0]<572 and 218<Cursor[1]<436:
                            if 258<Cursor[0]<281:
                                if 218<Cursor[1]< 241:
                                    UI.color_picked = 0
                                elif 243<Cursor[1]< 265:
                                    UI.color_picked = 1
                                elif 267<Cursor[1]< 289:
                                    UI.color_picked = 2
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 3
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 4
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 5
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 6
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 7
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 8
                            elif 282 < Cursor[0] < 305:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 9
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 10
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 11
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 12
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 13
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 14
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 15
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 16
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 17
                            elif 307 < Cursor[0] < 329:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 18
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 19
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 20
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 21
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 22
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 23
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 24
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 25
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 26
                            elif 331 < Cursor[0] < 353:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 27
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 28
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 29
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 30
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 31
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 32
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 33
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 34
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 35
                            elif 355 < Cursor[0] < 377:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 36
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 37
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 38
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 39
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 40
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 41
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 42
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 43
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 44
                            elif 379 < Cursor[0] < 403:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 45
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 46
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 47
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 48
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 49
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 50
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 51
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 52
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 53
                            elif 404 < Cursor[0] < 427:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 54
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 55
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 56
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 57
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 58
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 59
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 60
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 61
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 62
                            elif 428 < Cursor[0] < 450:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 63
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 64
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 65
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 66
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 67
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 68
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 69
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 70
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 71
                            elif 452 < Cursor[0] < 475:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 72
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 73
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 74
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 75
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 76
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 77
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 78
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 79
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 80
                            elif 477 < Cursor[0] < 499:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 81
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 82
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 83
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 84
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 85
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 86
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 87
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 88
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 89
                            elif 501 < Cursor[0] < 525:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 90
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 91
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 92
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 93
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 94
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 95
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 96
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 97
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 98
                            elif 527 < Cursor[0] < 548:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 99
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 100
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 101
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 102
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 103
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 104
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 105
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 106
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 107
                            elif 550 < Cursor[0] < 572:
                                if 218 < Cursor[1] < 241:
                                    UI.color_picked = 108
                                elif 243 < Cursor[1] < 265:
                                    UI.color_picked = 109
                                elif 267 < Cursor[1] < 289:
                                    UI.color_picked = 110
                                elif 293 < Cursor[1] < 314:
                                    UI.color_picked = 111
                                elif 316 < Cursor[1] < 337:
                                    UI.color_picked = 112
                                elif 341 < Cursor[1] < 363:
                                    UI.color_picked = 113
                                elif 365 < Cursor[1] < 386:
                                    UI.color_picked = 114
                                elif 389 < Cursor[1] < 410:
                                    UI.color_picked = 115
                                elif 414 < Cursor[1] < 436:
                                    UI.color_picked = 116

                        elif UI.RP_Slc == 1:
                            if 61 < Cursor[0] < 194 and 261 < Cursor[1] < 400:
                                if 261 < Cursor[1] < 301:
                                    UI.info = 0
                                elif 312 < Cursor[1] < 351:
                                    UI.info = 1
                                elif 360 < Cursor[1] < 400:
                                    UI.info = 2
                        elif UI.RP_Slc == 2:                                   #Pref
                            if UI.RGB_Pref>-1 or UI.cursor_3D_Pref>-1 or UI.music or UI.color_picker==0:
                                UI.Reset_Selection()
                            elif 48<Cursor[0]<250 and 255<Cursor[1]<290:
                                if 48<Cursor[0]<148:
                                    UI.Shading = 0
                                elif 153 < Cursor[0] < 250:
                                    UI.Shading = 1
                            elif 48 < Cursor[0] < 207 and 295 < Cursor[1] < 328:
                                if 48 < Cursor[0] < 100:
                                    UI.RGB_Pref = 0
                                elif 103 < Cursor[0] < 153:
                                    UI.RGB_Pref = 1
                                elif 157 < Cursor[0] < 207:
                                    UI.RGB_Pref = 2
                            elif 48 < Cursor[0] < 207 and 335 < Cursor[1] < 368:
                                if 48 < Cursor[0] < 100:
                                    UI.cursor_3D_Pref = 0
                                elif 103 < Cursor[0] < 153:
                                    UI.cursor_3D_Pref = 1
                                elif 157 < Cursor[0] < 207:
                                    UI.cursor_3D_Pref = 2
                            elif 212 < Cursor[0] < 250 and 335 < Cursor[1] < 368:
                                if UI.cursor_3D==1:
                                    UI.cursor_3D = 0
                                else:
                                    UI.cursor_3D = 1
                            elif 212 < Cursor[0] < 250 and 373 < Cursor[1] < 408:
                                if UI.Mute==0:
                                    if UI.BGM:
                                        UI.Mute = 1
                                        UI.Music_play()
                                    else:
                                        UI.music = True
                                else:
                                    UI.Mute = 0
                                    pygame.mixer.music.stop()
                            elif 48 < Cursor[0] < 207 and 373 < Cursor[1] < 408:
                                if not UI.music:
                                    UI.music = True
                                else:
                                    UI.music = False
                            elif 212 < Cursor[0] < 250 and 294 < Cursor[1] < 330:
                                if UI.color_picker==-1:
                                    UI.color_picker = 0
                                    UI.color_picked = -1
                        elif 3<=UI.RP_Slc<=5:
                            if UI.transform>-1:
                                UI.Reset_Selection()
                            elif 81 < Cursor[0] < 250 and 262 < Cursor[1] < 398 and not UI.LP_Hrc_Slc==0:
                                    if 262 < Cursor[1] < 302:
                                        UI.transform = 0
                                    elif 311 < Cursor[1] < 350:
                                        UI.transform = 1
                                    elif 360 < Cursor[1] < 398:
                                        UI.transform = 2
                        elif UI.RP_Slc==6:
                            if UI.RGBA>-1 or UI.color_picker==0 and UI.color_picked==-1:
                                UI.Reset_Selection()
                            elif 44 < Cursor[0] < 118 and 255 < Cursor[1] < 407 and not UI.LP_Hrc_Slc==0 and not UI.LP_intMdl_Slc==-1:
                                    if 255 < Cursor[1] < 288:
                                        UI.RGBA = 0
                                    elif 292 < Cursor[1] < 327:
                                        UI.RGBA = 1
                                    elif 332 < Cursor[1] < 366:
                                        UI.RGBA = 2
                                    elif 371 < Cursor[1] < 407:
                                        UI.RGBA = 3
                            elif 126 < Cursor[0] < 250 and 291 < Cursor[1] < 328 and not UI.LP_Hrc_Slc==0 and not UI.LP_intMdl_Slc==-1:
                                    UI.RGBA = 4
                            elif 126 < Cursor[0] < 250 and 333 < Cursor[1] < 407 :
                                if UI.color_picker == -1:
                                    UI.color_picker = 0
                                    UI.color_picked = -1
                                else:
                                    UI.color_picker = -1
                                    if UI.int and UI.LP_Mdl_Slc==0:
                                        if UI.LP_Hrc_Slc==0 and UI.LP_Mdl_Slc==0:
                                            for i in range(len(self.MDLH)):
                                                self.MDLH[i].color_new = True
                                        else:
                                            self.MDLH[UI.LP_intMdl_Slc].color_new = True
                                    else:
                                        self.MDL[UI.LP_Mdl_Slc].color_new = True
                                    self.RELoadOBJ()
                        elif UI.RP_Slc == 7:
                            if 167 < Cursor[0] < 245 and 256 < Cursor[1] < 406:
                                if 167 < Cursor[0] < 204:
                                    if UI.int and UI.LP_Mdl_Slc==0 and not UI.MdlH_TexOn[UI.LP_intMdl_Slc]==-1:
                                        if UI.LP_Hrc_Slc>0 and not UI.LP_intMdl_Slc>-1:
                                            pass
                                        else:
                                            roller = True
                                    elif not UI.Mdl_TexOn[UI.LP_Mdl_Slc]==-1:
                                        roller = True
                                elif 207< Cursor[0] <245:
                                    if UI.int and UI.LP_Mdl_Slc==0:
                                        if UI.LP_Hrc_Slc==0:
                                            for i in range(len(self.MDLH)):
                                                if UI.MdlH_TexOn[i] == 1:
                                                    UI.MdlH_TexOn[i] = 0
                                                elif UI.MdlH_TexOn[i] == 0:
                                                    UI.MdlH_TexOn[i] = 1
                                        elif UI.LP_intMdl_Slc>-1:
                                            if UI.MdlH_TexOn[UI.LP_intMdl_Slc] == 1:
                                                UI.MdlH_TexOn[UI.LP_intMdl_Slc] = 0
                                            elif UI.MdlH_TexOn[UI.LP_intMdl_Slc] == 0:
                                                UI.MdlH_TexOn[UI.LP_intMdl_Slc] = 1
                                    else:
                                        if UI.Mdl_TexOn[UI.LP_Mdl_Slc] == 1:
                                            UI.Mdl_TexOn[UI.LP_Mdl_Slc] = 0
                                        elif UI.Mdl_TexOn[UI.LP_Mdl_Slc] == 0:
                                            UI.Mdl_TexOn[UI.LP_Mdl_Slc] = 1
                                    self.RELoadOBJ()
                        elif UI.RP_Slc == 8:
                            if UI.Light_Set>-1:
                                UI.Reset_Selection()
                            elif 6 < Cursor[0] < 126 and 271 < Cursor[1] < 408:
                                if 271 < Cursor[1] < 289:
                                    rlr = 0
                                    UI.Light_Set = 0
                                elif 309 < Cursor[1] < 329:
                                    if 6 < Cursor[0] < 35:
                                        rlr = 0
                                        UI.Light_Set = 10
                                    elif 38 < Cursor[0] <66:
                                        rlr = 1
                                        UI.Light_Set = 11
                                    elif 67 < Cursor[0] <95:
                                        rlr = 2
                                        UI.Light_Set = 12
                                    elif 97 < Cursor[0] <126:
                                        rlr = 3
                                        UI.Light_Set = 13
                                elif 348 < Cursor[1] < 368:
                                    if 6 < Cursor[0] < 35:
                                        rlr = 0
                                        UI.Light_Set = 20
                                    elif 38 < Cursor[0] <66:
                                        rlr = 1
                                        UI.Light_Set = 21
                                    elif 67 < Cursor[0] <95:
                                        rlr = 2
                                        UI.Light_Set = 22
                                    elif 97 < Cursor[0] <126:
                                        rlr = 3
                                        UI.Light_Set = 23
                                elif 388 < Cursor[1] < 408:
                                    if 6 < Cursor[0] < 45:
                                        UI.Light_Set = 30
                                    elif 47 < Cursor[0] <86:
                                        UI.Light_Set = 31
                                    elif 87 < Cursor[0] <126:
                                        UI.Light_Set = 32
                            elif 130 < Cursor[0] < 250 and 271 < Cursor[1] < 408:
                                if 271 < Cursor[1] < 289:
                                    if 130 < Cursor[0] < 160:
                                        rlr = 0
                                        UI.Light_Set = 40
                                    elif 160 < Cursor[0] < 189:
                                        rlr = 1
                                        UI.Light_Set = 41
                                    elif 190 < Cursor[0] < 219:
                                        rlr = 2
                                        UI.Light_Set = 42
                                    elif 221 < Cursor[0] < 408:
                                        rlr = 3
                                        UI.Light_Set = 43
                                elif 309 < Cursor[1] < 329:
                                    if 130 < Cursor[0] < 160:
                                        rlr = 0
                                        UI.Light_Set = 50
                                    elif 160 < Cursor[0] < 189:
                                        rlr = 1
                                        UI.Light_Set = 51
                                    elif 190 < Cursor[0] < 219:
                                        rlr = 2
                                        UI.Light_Set = 52
                                    elif 221 < Cursor[0] < 408:
                                        rlr = 3
                                        UI.Light_Set = 53
                                elif 348 < Cursor[1] < 368:
                                    if 130 < Cursor[0] < 160:
                                        rlr = 0
                                        UI.Light_Set = 60
                                    elif 160 < Cursor[0] < 189:
                                        rlr = 1
                                        UI.Light_Set = 61
                                    elif 190 < Cursor[0] < 219:
                                        rlr = 2
                                        UI.Light_Set = 62
                                    elif 221 < Cursor[0] < 408:
                                        rlr = 3
                                        UI.Light_Set = 63
                                elif 371 < Cursor[1] < 408:
                                    if UI.Light_Props[7]==0:
                                        UI.Light_Props[7] = 1
                                    else:
                                        UI.Light_Props[7] = 0
                        elif UI.RP_Slc == 9:
                            if UI.Ba_Slc>-1:
                                UI.Reset_Selection()
                            elif 5 < Cursor[0] < 60 and 254 < Cursor[1] < 408:
                                if 5 < Cursor[0] < 32:
                                    UI.Ba_Slc = 18
                                    ratx, raty = [0, 0], [0, 0]
                                elif 32 < Cursor[0] < 60:
                                    UI.Ba_Slc = 19
                            elif 61 < Cursor[0] < 128 and 271 < Cursor[1] < 330:
                                if 61 < Cursor[0] < 81:
                                    if UI.Back[0]==0:
                                        UI.Back[0] = 1
                                    elif UI.Back[0]==1:
                                        UI.Back[0] = 0
                                elif 82 < Cursor[0] < 128:
                                    if 271 < Cursor[1] < 313:
                                        UI.Ba_Slc = 16
                                    elif 314 < Cursor[1] < 330:
                                        if UI.Back[2] == 0:
                                            UI.Back[2] = 1
                                        elif UI.Back[2] == 1:
                                            UI.Back[2] = 0
                            elif 61 < Cursor[0] < 128 and 332 < Cursor[1] < 408:
                                if 61 < Cursor[0] < 81:
                                    if UI.Base[0]==0:
                                        UI.Base[0] = 1
                                    elif UI.Base[0]==1:
                                        UI.Base[0] = 0
                                elif 82 < Cursor[0] < 128:
                                    if 332 < Cursor[1] < 391:
                                        UI.Ba_Slc = 17
                                    elif 392 < Cursor[1] < 408:
                                        if UI.Base[2] == 0:
                                            UI.Base[2] = 1
                                        elif UI.Base[2] == 1:
                                            UI.Base[2] = 0
                            elif 130 < Cursor[0] < 250 and 271 < Cursor[1] < 290:
                                if 130 < Cursor[0] < 160:
                                    UI.Ba_Slc = 0
                                elif 160 < Cursor[0] < 189:
                                    UI.Ba_Slc = 1
                                elif 190 < Cursor[0] < 220:
                                    UI.Ba_Slc = 2
                                elif 221 < Cursor[0] < 250:
                                    UI.Ba_Slc = 3
                            elif 130 < Cursor[0] < 250 and 308 < Cursor[1] < 331:
                                if 130 < Cursor[0] < 160:
                                    UI.Ba_Slc = 4
                                    rlr = 0
                                elif 160 < Cursor[0] < 189:
                                    UI.Ba_Slc = 5
                                    rlr = 1
                                elif 190 < Cursor[0] < 220:
                                    UI.Ba_Slc = 6
                                    rlr = 2
                                elif 221 < Cursor[0] < 250:
                                    UI.Ba_Slc = 7
                                    if UI.color_picker == -1:
                                        UI.color_picker = 0
                                        UI.color_picked = -1
                            elif 130 < Cursor[0] < 250 and 349 < Cursor[1] < 368:
                                if 130 < Cursor[0] < 160:
                                    UI.Ba_Slc = 8
                                elif 160 < Cursor[0] < 189:
                                    UI.Ba_Slc = 9
                                elif 190 < Cursor[0] < 220:
                                    UI.Ba_Slc = 10
                                elif 221 < Cursor[0] < 250:
                                    UI.Ba_Slc = 11
                            elif 130 < Cursor[0] < 250 and 388 < Cursor[1] < 408:
                                if 130 < Cursor[0] < 160:
                                    UI.Ba_Slc = 12
                                    rlr = 0
                                elif 160 < Cursor[0] < 189:
                                    UI.Ba_Slc = 13
                                    rlr = 1
                                elif 190 < Cursor[0] < 220:
                                    UI.Ba_Slc = 14
                                    rlr = 2
                                elif 221 < Cursor[0] < 250:
                                    UI.Ba_Slc = 15
                                    if UI.color_picker == -1:
                                        UI.color_picker = 0
                                        UI.color_picked = -1
                    elif event.button == 2:
                        if shift:
                            tsf = 0
                        else:
                            tsf = 2
                    elif event.button == 3:
                        if UI.RP_Slc==3:
                            tsf = 1
                        elif UI.RP_Slc==4:
                            tsf = 3
                        elif UI.RP_Slc==5:
                            tsf = 4
                        elif UI.Ba_Slc ==3 or UI.Ba_Slc ==11:
                            tsf = 5
                        elif UI.Ba_Slc == 18 and not crop:
                            ratx[0] = Cursor[0] / 1249 * 33.3
                            raty[0] = Cursor[1] / 749 * 19.9
                            crop = True
                    elif event.button == 4:
                        UI.cursor_3D_pos[2] += 1
                    elif event.button == 5:
                        UI.cursor_3D_pos[2] -= 1
                elif event.type == MOUSEBUTTONUP:
                    if tsf==0 or tsf==1:
                        if tsf==1 and UI.LP_intMdl_Slc>-1 or tsf==1 and UI.LP_Mdl_Slc>-1 or tsf==1 and UI.LP_Hrc_Slc==0:
                            if UI.int and UI.LP_Mdl_Slc==0:
                                if UI.LP_Hrc_Slc == 0:
                                    for i in range(len(self.MDLH)):
                                        pos = UI.MdlH_POS[i]
                                        pos[0] += tx / 5
                                        pos[1] += ty / 5
                                        pos[2] += tz / 5
                                    tx = ty = tz = 0
                                elif UI.LP_intMdl_Slc==-1 and UI.LP_Hrc_Slc>0:
                                    break
                                else:
                                    pos = UI.MdlH_POS[UI.LP_intMdl_Slc]
                                    pos[0] += tx / 5
                                    pos[1] += ty / 5
                                    pos[2] += tz / 5
                                    tx = ty = tz = 0
                            elif UI.LP_Mdl_Slc > -1:
                                pos = UI.Mdl_POS[UI.LP_Mdl_Slc]
                                pos[0] += tx / 5
                                pos[1] += ty / 5
                                pos[2] += tz / 5
                                tx = ty = tz = 0
                        else:
                            shift = False
                    elif tsf==3 and UI.LP_intMdl_Slc>-1 or tsf==3 and UI.LP_Mdl_Slc>-1:
                        if UI.int and UI.LP_Mdl_Slc==0:
                            deg = UI.MdlH_DEG[UI.LP_intMdl_Slc]
                        elif UI.LP_Mdl_Slc>-1:
                            deg = UI.Mdl_DEG[UI.LP_Mdl_Slc]
                        deg[0] += ry
                        deg[1] += rx
                        deg[2] += rz
                        for i in range(3):
                            if deg[i]>360 or deg[i]<-360:
                                n = deg[i] / 360
                                final = deg[i] - 360 * int(n)
                                deg[i] = final
                        rx = ry = rz = 0
                    elif tsf==4 and UI.LP_intMdl_Slc>-1 or tsf==4 and UI.LP_Mdl_Slc>-1:
                        if UI.int and UI.LP_Mdl_Slc==0:
                            scl = UI.MdlH_SCL[UI.LP_intMdl_Slc]
                        elif UI.LP_Mdl_Slc > -1:
                            scl = UI.Mdl_SCL[UI.LP_Mdl_Slc]
                        scl[0] += sx/500
                        scl[1] += sy/500
                        scl[2] += sz/500
                        for i in range(3):
                            if scl[i]<0:
                                scl[i] = 0
                        sx = sy = sz = 0
                    elif tsf == 5:
                        if UI.Ba_Slc==3:
                            pos = UI.Back[3]
                        elif UI.Ba_Slc==11:
                            pos = UI.Base[3]
                        pos[2] += int(ty/10)
                        if pos[2]>999:
                            pos[2] =999
                        elif pos[2]<-999:
                            pos[2] = -999
                        ty = 0
                    elif roller:
                        roller = False
                        self.RELoadOBJ()
                    elif rlr>-1:
                        rlr = -1
                        if UI.Light_Set>-1:
                            UI.Light_Set = -10
                        elif UI.Ba_Slc>-1:
                            UI.Ba_Slc = -1
                    elif UI.Ba_Slc == 18 and crop:
                        ratx[1] = Cursor[0]/1249*33.3
                        raty[1] = Cursor[1]/749*19.9
                        UI.Ba_Slc = -1
                        crop = False
                    ax = ay = az = False
                    UI.axis = -1
                    tsf = -1
                elif event.type == MOUSEMOTION:
                    i,j = event.rel
                    if tsf==0:
                        if shift:
                            UI.cursor_3D_pos[0] += i
                            UI.cursor_3D_pos[1] -= j
                    elif tsf==1:
                        if 0<=yrot<45 or 315<=yrot<=360 or -45<=yrot<0 or -360<=yrot<-315:
                            if 0 <= xrot < 45 or 315 <= xrot <= 360 or -45 <= xrot < 0 or -360 <= xrot < -315:
                                if ax:
                                    tx += i
                                elif ay:
                                    ty -= j
                                elif az:
                                    tz -= i
                                else:
                                    tx += i
                                    ty -= j
                            elif 45<=xrot<135 or -315<=xrot<-225:
                                if ax:
                                    tx += i
                                elif ay:
                                    ty -= j
                                elif az:
                                    tz += i
                                else:
                                    tz += i
                                    ty -= j
                            elif 135 <= xrot < 225 or -225 <= xrot < -135:
                                if ax:
                                    tx -= i
                                elif ay:
                                    ty -= j
                                elif az:
                                    tz += i
                                else:
                                    tx -= i
                                    ty -= j
                            elif 225<=xrot<315 or -135<=xrot<-45:
                                if ax:
                                    tx -= i
                                elif ay:
                                    ty -= j
                                elif az:
                                    tz -= i
                                else:
                                    tz -= i
                                    ty -= j
                        elif 45 <= yrot < 135 or -315 <= yrot < -225:
                            if 0 <= xrot < 45 or 315 <= xrot <= 360 or -45 <= xrot < 0 or -360 <= xrot < -315:
                                if ax:
                                    tx += i
                                elif ay:
                                    ty -= i
                                elif az:
                                    tz += j
                                else:
                                    tx += i
                                    tz += j
                            elif 45 <= xrot < 135 or -315 <= xrot < -225:
                                if ax:
                                    tx -= j
                                elif ay:
                                    ty -= i
                                elif az:
                                    tz += i
                                else:
                                    tz += i
                                    tx -= j
                            elif 135 <= xrot < 225 or -225 <= xrot < -135:
                                if ax:
                                    tx -= i
                                elif ay:
                                    ty -= i
                                elif az:
                                    tz -= j
                                else:
                                    tx -= i
                                    tz -= j
                            elif 225 <= xrot < 315 or -135 <= xrot < -45:
                                if ax:
                                    tx += j
                                elif ay:
                                    ty -= i
                                elif az:
                                    tz -= i
                                else:
                                    tz -= i
                                    tx += j
                        elif 135 <= yrot < 225 or -225 <= yrot < -135:
                            if 0 <= xrot < 45 or 315 <= xrot <= 360 or -45 <= xrot < 0 or -360 <= xrot < -315:
                                if ax:
                                    tx += i
                                elif ay:
                                    ty += j
                                elif az:
                                    tz += i
                                else:
                                    tx += i
                                    ty += j
                            elif 45<=xrot<135 or -315<=xrot<-225:
                                if ax:
                                    tx -= i
                                elif ay:
                                    ty += j
                                elif az:
                                    tz += i
                                else:
                                    tz += i
                                    ty += j
                            elif 135 <= xrot < 225 or -225 <= xrot < -135:
                                if ax:
                                    tx -= i
                                elif ay:
                                    ty += j
                                elif az:
                                    tz -= i
                                else:
                                    tx -= i
                                    ty += j
                            elif 225<=xrot<315 or -135<=xrot<-45:
                                if ax:
                                    tx += i
                                elif ay:
                                    ty += j
                                elif az:
                                    tz -= i
                                else:
                                    tz -= i
                                    ty += j
                        elif 225 <= yrot < 315 or -135 <= yrot < -45:
                            if 0 <= xrot < 45 or 315 <= xrot <= 360 or -45 <= xrot < 0 or -360 <= xrot < -315:
                                if ax:
                                    tx += i
                                elif ay:
                                    ty += i
                                elif az:
                                    tz -= j
                                else:
                                    tx += i
                                    tz -= j
                            elif 45 <= xrot < 135 or -315 <= xrot < -225:
                                if ax:
                                    tx += j
                                elif ay:
                                    ty += i
                                elif az:
                                    tz += i
                                else:
                                    tz += i
                                    tx += j
                            elif 135 <= xrot < 225 or -225 <= xrot < -135:
                                if ax:
                                    tx -= i
                                elif ay:
                                    ty += i
                                elif az:
                                    tz += j
                                else:
                                    tx -= i
                                    tz += j
                            elif 225 <= xrot < 315 or -135 <= xrot < -45:
                                if ax:
                                    tx -= j
                                elif ay:
                                    ty += i
                                elif az:
                                    tz -= i
                                else:
                                    tz -= i
                                    tx -= j
                    elif tsf==2:
                        xrot += i
                        yrot += j
                    elif tsf==3:
                        if ax:
                            ry -= j
                        elif ay:
                            rx -= i
                        elif az:
                            rz += i
                        else:
                            rx -= i
                            ry -= j
                    elif tsf==4:
                        if ax:
                            sx += i
                        elif ay:
                            sy += i
                        elif az:
                            sz += i
                        else:
                            sx += i
                            sy += i
                            sz += i
                    elif tsf==5:
                        ty -= j
                    elif roller:
                        if UI.int and UI.LP_Mdl_Slc==0:
                            if UI.LP_Hrc_Slc==0:
                                for i in range(len(self.MDLH)):
                                    if 0 <= UI.MdlH_Alpha[i] <= 1:
                                        UI.MdlH_Alpha[i] += j / 100
                                        if UI.MdlH_Alpha[i] < 0:
                                            UI.MdlH_Alpha[i] = 0
                                        elif UI.MdlH_Alpha[i] > 1:
                                            UI.MdlH_Alpha[i] = 1
                            else:
                                if 0<=UI.MdlH_Alpha[UI.LP_intMdl_Slc]<=1:
                                    UI.MdlH_Alpha[UI.LP_intMdl_Slc] += j/100
                                    if UI.MdlH_Alpha[UI.LP_intMdl_Slc]<0:
                                        UI.MdlH_Alpha[UI.LP_intMdl_Slc] = 0
                                    elif UI.MdlH_Alpha[UI.LP_intMdl_Slc]>1:
                                        UI.MdlH_Alpha[UI.LP_intMdl_Slc] = 1
                        else:
                            if 0<=UI.Mdl_Alpha[UI.LP_Mdl_Slc]<=1:
                                UI.Mdl_Alpha[UI.LP_Mdl_Slc] += j/100
                                if UI.Mdl_Alpha[UI.LP_Mdl_Slc]<0:
                                    UI.Mdl_Alpha[UI.LP_Mdl_Slc] = 0
                                elif UI.Mdl_Alpha[UI.LP_Mdl_Slc]>1:
                                    UI.Mdl_Alpha[UI.LP_Mdl_Slc] = 1
                    elif rlr > -1:
                        if UI.Light_Set == 0:
                            UI.Light_Props[UI.Light_Set] += i
                            if UI.Light_Props[UI.Light_Set]<0:
                                UI.Light_Props[UI.Light_Set] = 0
                            elif UI.Light_Props[UI.Light_Set]>128:
                                UI.Light_Props[UI.Light_Set] = 128
                        else:
                            if UI.Light_Set>0:
                                Props = UI.Light_Props[int(UI.Light_Set/10)]
                                Props[rlr] += i/100
                                if Props[rlr]<0:
                                    Props[rlr] = 0
                                elif Props[rlr]>1:
                                    Props[rlr] = 1
                            elif 4<=UI.Ba_Slc<=6 or 12<=UI.Ba_Slc<=14:
                                if 4<=UI.Ba_Slc<=6:
                                    RGB = UI.Back[4]
                                else:
                                    RGB = UI.Base[4]
                                RGB[rlr] += i
                                if RGB[rlr]>255:
                                    RGB[rlr] = 255
                                elif RGB[rlr]<0:
                                    RGB[rlr]=0

                elif event.type == pygame.KEYDOWN:
                    ### Data Amend ######
                    if event.key == K_ESCAPE:
                        if tsf==1 or tsf==3 or tsf==4:
                            tx = ty = tz = sx = sy = sz = rx = ry = rz = 0
                            break
                        elif UI.Mdl_Add or UI.RGB_Pref>-1 or UI.cursor_3D_Pref>-1 or UI.music or UI.color_picker==0 or UI.transform>-1 or UI.RGBA>-1 or\
                                UI.Light_Set>-1 or UI.Ba_Slc>-1:
                            UI.Reset_Selection()
                        else:
                            UI.RP_Slc = 0
                            UI.exit = 1
                    elif UI.Data_Amend:
                        if UI.RGB_Pref>-1 or UI.RGBA>-1 or 0<=UI.Ba_Slc<=2 or 8<=UI.Ba_Slc<=10:
                            if event.key == pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                                if UI.RGB_Pref>-1:
                                    UI.RGB_Pref = -1
                                elif UI.RGBA>-1:
                                    if UI.int:
                                        self.MDLH[UI.LP_intMdl_Slc].color_new = True
                                    else:
                                        self.MDL[UI.LP_Mdl_Slc].color_new = True
                                    self.RELoadOBJ()
                                    UI.RGBA = -1
                                elif 0<=UI.Ba_Slc<=2 or 8<=UI.Ba_Slc<=10:
                                    UI.Ba_Slc = -1
                                UI.Data_Amend = False
                            elif event.key == pygame.K_BACKSPACE:
                                UI.Data_New = UI.Data_New[:-1]
                            elif UI.RGBA==3 and len(UI.Data_New)<4:
                                if K_0 <= event.key <= K_9 or K_KP0 <= event.key <= K_KP9:
                                    UI.Data_New += event.unicode
                                elif event.key == K_PERIOD and '.' not in UI.Data_New or event.key == K_KP_PERIOD and '.' not in UI.Data_New:
                                    if len(UI.Data_New) == 0:
                                        UI.Data_New = "0" + event.unicode
                                    else:
                                        UI.Data_New += event.unicode
                                if float(UI.Data_New) > 1.0:
                                    UI.Data_New = "1.00"
                            elif UI.RGBA == 4 and len(UI.Data_New) < 6:
                                if K_0 <= event.key <= K_9 or K_KP0<=event.key<=K_KP9 or K_a <= event.key <= K_f:
                                    UI.Data_New += event.unicode.upper()
                            elif len(UI.Data_New)<4:
                                if K_0 <= event.key <= K_9 or K_KP0<=event.key<=K_KP9:
                                    if not 0<=UI.Ba_Slc<=2 and not 8<=UI.Ba_Slc<=10 and len(UI.Data_New)>3:
                                        pass
                                    else:
                                        UI.Data_New += event.unicode
                                    if not 0<=UI.Ba_Slc<=2 and not 8<=UI.Ba_Slc<=10 and int(UI.Data_New)>255:
                                        UI.Data_New = "255"
                                elif UI.Ba_Slc==2 or UI.Ba_Slc==10:
                                    if event.key == K_MINUS and '-' not in UI.Data_New and len(UI.Data_New) == 0 or event.key == K_KP_MINUS and '-' not in UI.Data_New and len(UI.Data_New) == 0:
                                        UI.Data_New += event.unicode
                        elif UI.cursor_3D_Pref > -1:
                            if event.key == pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                                UI.cursor_3D_Pref = -1
                                UI.Data_Amend = False
                            elif event.key == pygame.K_BACKSPACE:
                                UI.Data_New = UI.Data_New[:-1]
                            elif '.' in UI.Data_New and len(UI.Data_New)<5 or '-' in UI.Data_New and len(UI.Data_New)<4 or len(UI.Data_New)<3:
                                if K_0<=event.key<=K_9 or K_KP0<=event.key<=K_KP9:
                                    UI.Data_New += event.unicode
                                elif event.key == K_PERIOD and '.' not in UI.Data_New or event.key == K_KP_PERIOD and '.' not in UI.Data_New:
                                    if len(UI.Data_New)==0 :
                                        UI.Data_New = "0"+event.unicode
                                    elif '-' in UI.Data_New and len(UI.Data_New)==1:
                                        UI.Data_New = "-0" + event.unicode
                                    else:
                                        UI.Data_New += event.unicode
                                elif event.key == K_MINUS and '-' not in UI.Data_New and len(UI.Data_New)==0 or event.key == K_KP_MINUS and '-' not in UI.Data_New and len(UI.Data_New)==0:
                                    UI.Data_New += event.unicode
                        elif UI.transform > -1 or UI.Light_Set>=30:
                            if event.key == pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                                if UI.transform>-1:
                                    UI.transform = -1
                                elif UI.Light_Set>=30:
                                    UI.Light_Set = -10
                                UI.Data_Amend = False
                            elif event.key == pygame.K_BACKSPACE:
                                UI.Data_New = UI.Data_New[:-1]
                            elif len(UI.Data_New)<15:
                                if K_0<=event.key<=K_9 or K_KP0<=event.key<=K_KP9:
                                    if UI.Light_Set>=30 and len(UI.Data_New)>=5:
                                        pass
                                    else:
                                        UI.Data_New += event.unicode
                                elif event.key == K_PERIOD and '.' not in UI.Data_New or event.key == K_KP_PERIOD and '.' not in UI.Data_New:
                                    if UI.Light_Set >= 30 and len(UI.Data_New)>=5:
                                        pass
                                    else:
                                        if len(UI.Data_New)==0 :
                                            UI.Data_New = "0"+event.unicode
                                        elif '-' in UI.Data_New and len(UI.Data_New)==1:
                                            UI.Data_New = "-0" + event.unicode
                                        else:
                                                UI.Data_New += event.unicode
                                elif event.key == K_MINUS and '-' not in UI.Data_New and len(UI.Data_New)==0 or event.key == K_KP_MINUS and '-' not in UI.Data_New and len(UI.Data_New)==0:
                                    if UI.RP_Slc==5:
                                        pass
                                    elif UI.Light_Set>=30 and len(UI.Data_New)>=5:
                                        pass
                                    else:
                                        UI.Data_New += event.unicode
                                if UI.RP_Slc==4 and len(UI.Data_New)>2:
                                    if float(UI.Data_New)>360.0:
                                        UI.Data_New = '360.0'
                                    elif float(UI.Data_New)<-360.0:
                                        UI.Data_New = '-360.0'
                        elif UI.music or UI.Mdl_Add or 16<=UI.Ba_Slc<=17 or UI.Ba_Slc==19:
                            if UI.fDIR_check==3:
                                UI.fDIR_check = 0
                            elif event.key == pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                                if UI.fDIR_check==2:
                                    UI.fDIR_check = 0
                                    if UI.music:
                                        UI.music = False
                                    elif UI.Mdl_Add:
                                        UI.Mdl_Add  = False
                                        self.LoadOBJ()
                                    elif 16<=UI.Ba_Slc<=17:
                                        UI.Ba_Slc = -1
                                    UI.Data_Amend = False
                                elif UI.Ba_Slc == 19:
                                    if len(UI.Data_New)==0:
                                        UI.Data_New = "Untitled"
                                    UI.Ba_Slc = -1
                                    UI.image[1] = UI.Data_New
                                    UI.image[2] = True
                                    UI.Data_Amend = False
                                else:
                                    UI.fDIR_check = 3
                                    UI.Data_New = ""
                            elif event.key == pygame.K_BACKSPACE:
                                if UI.Ba_Slc==19 and UI.Data_New=="Untitled":
                                    UI.Data_New = ""
                                else:
                                    UI.fDIR_check = 0
                                    UI.Data_New = UI.Data_New[:-1]
                            else:
                                if UI.Ba_Slc==19:
                                    if K_0<=event.key<=K_9 or K_KP0<=event.key<=K_KP9 or K_a<=event.key<=K_z or event.key==K_UNDERSCORE or event.key==K_MINUS or event.key==K_PERIOD or event.key==K_KP_MINUS or event.key==K_KP_PERIOD:
                                        UI.Data_New += event.unicode
                                else:
                                    UI.Data_New += event.unicode
                    elif tsf==1 or tsf==3 or tsf==4:
                        if K_x<=event.key<=K_z:
                            tx = ty = tz = sx = sy = sz = rx = ry = rz = 0
                        if event.key == K_x:
                            ax = True
                            ay = az = False
                            UI.axis = 0
                        elif event.key == K_y:
                            ay = True
                            ax = az = False
                            UI.axis = 1
                        elif event.key == K_z:
                            az = True
                            ay = ax = False
                            UI.axis = 2
                    else:
                        if event.key == K_i:
                            UI.RP_Slc = 1
                        elif event.key == K_SPACE:
                            UI.RP_Slc = 2
                        elif event.key == K_g and UI.Mdl:
                            UI.RP_Slc = 3
                        elif event.key == K_r:
                            if not UI.LP_Hrc_Slc==0 and UI.Mdl:
                                UI.RP_Slc = 4
                        elif event.key == K_s and UI.Mdl:
                            if not UI.LP_Hrc_Slc == 0:
                                UI.RP_Slc = 5
                        elif event.key == K_c and UI.Mdl:
                            UI.RP_Slc = 6
                        elif event.key == K_t and UI.Mdl:
                            UI.RP_Slc = 7
                        elif event.key == K_l:
                            UI.RP_Slc = 8
                        elif event.key == K_o:
                            UI.RP_Slc = 9
                        elif event.key == K_q:
                            if UI.Hide:
                                UI.Hide = False
                            else:
                                UI.Hide = True
                        elif event.key == K_1 or event.key == K_KP1:
                            UI.ortho = 1
                            xrot = yrot = 0
                        elif event.key == K_2 or event.key == K_KP2:
                            yrot += 30
                        elif event.key == K_3 or event.key == K_KP3:
                            UI.ortho = 3
                            xrot, yrot = 270, 0
                        elif event.key == K_4 or event.key == K_KP4:
                            xrot -= 30
                        elif event.key == K_5 or event.key == K_KP5:
                            xrot = yrot = UI.cursor_3D_pos[0] = UI.cursor_3D_pos[1] = UI.cursor_3D_pos[2] = 0
                        elif event.key == K_6 or event.key == K_KP6:
                            xrot += 30
                        elif event.key == K_7 or event.key == K_KP7:
                            UI.ortho = 7
                            xrot, yrot = 0, 90
                        elif event.key == K_8 or event.key == K_KP8:
                            yrot -= 30
                        elif event.key == K_9 or event.key == K_KP9:
                            UI.ortho = 9
                            xrot, yrot = 0, 270
                elif event.type == pygame.KEYUP:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        shift = False
            keys = pygame.key.get_pressed()     #press hold
            if keys[K_LSHIFT] or keys[K_RSHIFT]:
                shift = True

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glClearColor(int(UI.BGC[0])/255, int(UI.BGC[1])/255, int(UI.BGC[2])/255, 1)
            glClearDepthf(1)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LEQUAL)
            glShadeModel(GL_SMOOTH)
            if not self.app:
                self.LoadScreen()
            else:
                xrot = self.Rot_clear(xrot)
                yrot = self.Rot_clear(yrot)
                self.Select_Detection(Cursor)
                self.EnvRot(xrot, yrot)
                UI.Cursor_3D(xrot, yrot)
                glPushMatrix()
                glTranslate(UI.cursor_3D_pos[0], UI.cursor_3D_pos[1], UI.cursor_3D_pos[2]-20)
                UI.Lighting_SetUp()
                UI.Background(ty)
                glRotate(yrot, 1, 0, 0)
                glRotate(xrot, 0, 1, 0)
                if UI.Shading == 1:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                    glLineWidth(1)
                if UI.LP_Hrc_Slc==0 and UI.LP_Mdl_Slc==0:
                    for i in range(len(self.MDLH)):
                        pos_ori = UI.MdlH_POS_ORI[i]
                        pos = UI.MdlH_POS[i]
                        rot = UI.MdlH_DEG[i]
                        scl = UI.MdlH_SCL[i]
                        glPushMatrix()
                        glTranslate(pos[0] + tx / 5, pos[1] + ty / 5, pos[2] + tz / 5)
                        glScale(scl[0], scl[1], scl[2])
                        glRotate(rot[0], 1, 0, 0)
                        glRotate(rot[1], 0, 1, 0)
                        glRotate(rot[2], 0, 0, 1)
                        glTranslate(-pos_ori[0], -pos_ori[1], -pos_ori[2])  # Back to Origin
                        glCallList(self.MDLH[i].gl_list)
                        glPopMatrix()
                if UI.int:
                    n = 2
                else:
                    n = 1
                for k in range(n):
                    if k==0:
                        lst = self.MDL_list
                        callst = self.MDL
                    else:
                        lst = len(self.MDLH)
                        callst = self.MDLH
                    for i in range(lst):
                        if UI.int and k==0 and i==0 or UI.int and UI.LP_Hrc_Slc==0 and k==1:
                            pass
                        else:
                            if k == 0:
                                pos_ori = UI.Mdl_POS_ORI[i]
                                pos = UI.Mdl_POS[i]
                                rot = UI.Mdl_DEG[i]
                                scl = UI.Mdl_SCL[i]
                            else:
                                pos_ori = UI.MdlH_POS_ORI[i]
                                pos = UI.MdlH_POS[i]
                                rot = UI.MdlH_DEG[i]
                                scl = UI.MdlH_SCL[i]
                            glPushMatrix()
                            if k==0 and UI.LP_Mdl_Slc==i or k==1 and UI.LP_intMdl_Slc==i:
                                glTranslate(pos[0] + tx / 5, pos[1] + ty / 5, pos[2] + tz / 5)
                                glScale(scl[0] + sx / 500, scl[1] + sy / 500, scl[2] + sz / 500)
                                glRotate(rot[0] + ry, 1, 0, 0)
                                glRotate(rot[1] + rx, 0, 1, 0)
                                glRotate(rot[2] + rz, 0, 0, 1)
                            else:
                                glTranslate(pos[0], pos[1], pos[2])
                                glScale(scl[0], scl[1], scl[2])
                                glRotate(rot[0], 1, 0, 0)
                                glRotate(rot[1], 0, 1, 0)
                                glRotate(rot[2], 0, 0, 1)
                            glTranslate(-pos_ori[0], -pos_ori[1], -pos_ori[2])  # Back to Origin
                            glCallList(callst[i].gl_list)
                            glPopMatrix()
                glPopMatrix()
                glDisable(GL_LIGHT0)
                glDisable(GL_LIGHT1)
                glDisable(GL_LIGHTING)
                glDisable(GL_COLOR_MATERIAL)
                glDisable(GL_NORMALIZE)
                glDisable(GL_DEPTH_TEST)
                UI.ImageSave()
                if UI.Shading==1:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                UI.Update()
                UI.Crop(ratx, raty, crop)
            pygame.display.flip()

if __name__ == "__main__":
    ModelLoader = Model_main()
    ModelLoader.main()
    del UI
