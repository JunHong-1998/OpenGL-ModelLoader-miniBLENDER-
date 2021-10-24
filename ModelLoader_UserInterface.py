import math
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from os import path
from PIL import Image

class UserInterface:
    def __init__(self):
        self.Shading = 0
        self.RGB_Pref = -1
        self.RGBA = -1
        self.Hex = None
        self.cursor_3D_Pref = -1
        self.transform = -1
        self.axis = -1
        self.cursor_3D_pos = [0,0,0]
        self.cursor_3D = 1
        self.Mute = 0
        self.music = False
        self.BGM = None
        self.BGC = ["84", "84", "84"]
        self.MdlH = ["Head.obj", "Hair.obj", "Eye_Left.obj","Eye_Right.obj","Neck.obj","Body_Upper.obj","Body_Lower.obj", "Arm_Upper_Left.obj", "Arm_Upper_Right.obj",
                     "Arm_Lower_Left.obj", "Arm_Lower_Right.obj", "Hand_Left.obj", "Hand_Right.obj", "Leg_Upper_Left.obj", "Leg_Upper_Right.obj", "Leg_Lower_Left.obj",
                     "Leg_Lower_Right.obj", "Foot_Left.obj", "Foot_Right.obj",
                     "BioHelmet.obj", "Armor_Body_Upper.obj", "Armor_Body_Lower.obj", "Armor_Arm_Left.obj", "Armor_Arm_Right.obj", "Armor_Leg_Left.obj", "Armor_Leg_Right.obj"]
        self.MdlH_TexOn = []
        self.MdlH_Alpha = []
        self.MdlH_TexFile = []
        self.MdlH_RGBA = []
        self.MdlH_POS = []
        self.MdlH_POS_ORI = []
        self.MdlH_DEG = []
        self.MdlH_SCL = []
        self.int = True
        self.LP_intMdl_Slc = -1
        self.LP_Hrc_Slc = 0
        self.Mdl = ["Predator.obj"]
        self.Mdl_TexOn = []
        self.Mdl_Alpha = []
        self.Mdl_TexFile = []
        self.Mdl_RGBA = []
        self.Mdl_POS = []
        self.Mdl_POS_ORI = []
        self.Mdl_DEG = []
        self.Mdl_SCL = []
        self.Mdl_list = 1
        self.Mdl_Add = False
        self.Mdl_Add_Complete = False
        self.LP_Mdl_Slc = 0
        self.LP_Mdl_Del = -1
        self.LP_Mdl_Add = True
        self.RP_Slc = -1 #-1
        self.Data_New = None
        self.Data_Backup = None
        self.Data_Amend = False
        self.fDIR_check = 0
        self.color_picker = -1
        self.color_picked = -1
        self.ortho = 0
        self.Light_Props = [64,[0.18, 0.18, 0.18, 0.18],[0.3, 0.3, 0.3, 0.05],[-100, 100, 50, 0.0],[0.85, 0.85, 0.8, 0.85],[0.85, 0.85, 0.85, 0.85],[0, 0, 0, 0],0]
        self.Light_Set = -10
        self.Back = [0,"",0,[150,100,50],[255,255,255]]
        self.Base = [0, "", 0, [150, 100, -1], [255, 255, 255]]
        self.Ba_Slc = -1
        self.image = [[0,0,1250,750],"", False, False]
        self.Hide = False
        self.info = 0
        self.exit = 0

    def Update(self):
        if not self.Mdl:
            self.Mdl_list = 0
            self.RP_Slc = -1
        else:
            self.Mdl_list = len(self.Mdl)
        if self.Mdl_Add:
            self.LP_Mdl_Add = False
        elif 0<=self.Mdl_list<5:
            self.LP_Mdl_Add = True
        else:
            self.LP_Mdl_Add = False
        if not self.Hide:
            self.Data_update()
            self.Color_Ramp()
            self.LeftPanel()
            self.RightPanel()

    def Crop(self, ratx, raty, crop):
        if not crop:
            glColor3f(1,0,0)
            glPointSize(5)
            glBegin(GL_LINE_LOOP)
            glVertex3f(-16.65+ratx[0],9.95-raty[0],-10)
            glVertex3f(-16.65+ratx[1], 9.95-raty[0], -10)
            glVertex3f(-16.65+ratx[1], 9.95-raty[1], -10)
            glVertex3f(-16.65+ratx[0], 9.95-raty[1], -10)
            glEnd()
        else:
            w = -16.65+ratx[1]--16.65+ratx[0]
            h = 9.95-raty[1]-9.95-raty[0]
            if w>0 and h>0:
                pos = self.image[0]
                pos[0] = -16.65+ratx[0]
                pos[1] = 9.95-raty[0]
                pos[2] = w
                pos[3] = h

    def Reset_Selection(self):
        if self.Mdl_Add:
            self.Mdl_Add = False
            if self.Mdl_Add_Complete:
                self.Mdl.pop()
            self.fDIR_check = 0
        elif self.RP_Slc==2:
            if self.RGB_Pref>-1:
                self.BGC[self.RGB_Pref] = self.Data_Backup
                self.RGB_Pref = -1
            elif self.cursor_3D_Pref>-1:
                self.cursor_3D_pos[self.cursor_3D_Pref] = self.Data_Backup
                self.cursor_3D_Pref = -1
            elif self.music:
                self.music = False
                self.BGM = self.Data_Backup
                self.fDIR_check = 0
            elif self.color_picker==0:
                self.color_picker = -1
        elif 3<=self.RP_Slc<=5:
            if self.transform>-1:
                if self.RP_Slc==3:
                    if self.int and self.LP_Mdl_Slc==0:
                        pos = self.MdlH_POS[self.LP_intMdl_Slc]
                    else:
                        pos = self.Mdl_POS[self.LP_Mdl_Slc]
                    pos[self.transform] = self.Data_Backup
                elif self.RP_Slc==4:
                    if self.int and self.LP_Mdl_Slc==0:
                        deg = self.MdlH_DEG[self.LP_intMdl_Slc]
                    else:
                        deg = self.Mdl_DEG[self.LP_Mdl_Slc]
                    deg[self.transform] = self.Data_Backup
                elif self.RP_Slc==5:
                    if self.int and self.LP_Mdl_Slc==0:
                        scl = self.MdlH_SCL[self.LP_intMdl_Slc]
                    else:
                        scl = self.Mdl_SCL[self.LP_Mdl_Slc]
                    scl[self.transform] = self.Data_Backup
                self.transform = -1
        elif self.RP_Slc==6:
            if self.RGBA>-1:
                if self.int and self.LP_Mdl_Slc==0:
                    clr = self.MdlH_RGBA[self.LP_intMdl_Slc]
                else:
                    clr = self.Mdl_RGBA[self.LP_Mdl_Slc]
                if self.RGBA==4:
                    clr[0], clr[1], clr[2] = self.Data_Backup[0], self.Data_Backup[1], self.Data_Backup[2]
                else:
                    clr[self.RGBA] = self.Data_Backup
                self.RGBA = -1
            elif self.color_picker == 0:
                self.color_picker = -1
        elif self.RP_Slc == 8:
            if self.Light_Set>-1:
                if 30<=self.Light_Set<=33:
                    props = self.Light_Props[3]
                    props[self.Light_Set - 30] = self.Data_Backup
                self.Light_Set = -10
        elif self.RP_Slc == 9:
            if self.Ba_Slc>-1:
                if self.Ba_Slc==16:
                    self.Back[1]=self.Data_Backup
                elif self.Ba_Slc==17:
                    self.Base[1]=self.Data_Backup
                elif self.color_picker == 0:
                    self.color_picker = -1
                self.Ba_Slc=-1
        self.Data_Amend = False

    def Reset_Tool(self):
        if self.RP_Slc==2:
            self.Shading = 0
            self.BGC = ["84", "84", "84"]
            self.cursor_3D_pos = [0,0,0]
            self.cursor_3D = 1
            self.Mute = 0
            self.BGM = None
            pygame.mixer.music.stop()
        elif self.RP_Slc==3:
            if self.int and self.LP_Mdl_Slc==0:
                if self.LP_Hrc_Slc==0:
                    for i in range(len(self.MdlH)):
                        pos = self.MdlH_POS[i]
                        pos_ori = self.MdlH_POS_ORI[i]
                        pos[0], pos[1], pos[2] = pos_ori[0], pos_ori[1], pos_ori[2]
                else:
                    pos = self.MdlH_POS[self.LP_intMdl_Slc]
                    pos_ori = self.MdlH_POS_ORI[self.LP_intMdl_Slc]
            else:
                pos = self.Mdl_POS[self.LP_Mdl_Slc]
                pos_ori = self.Mdl_POS_ORI[self.LP_Mdl_Slc]
            pos[0], pos[1], pos[2] = pos_ori[0], pos_ori[1], pos_ori[2]
        elif self.RP_Slc==4:
            if self.int and self.LP_Mdl_Slc==0:
                deg = self.MdlH_DEG[self.LP_intMdl_Slc]
            else:
                deg = self.Mdl_DEG[self.LP_Mdl_Slc]
            deg[0] = deg[1] = deg[2] = 0
        elif self.RP_Slc==5:
            if self.int and self.LP_Mdl_Slc==0:
                scl = self.MdlH_SCL[self.LP_intMdl_Slc]
            else:
                scl = self.Mdl_SCL[self.LP_Mdl_Slc]
            scl[0] = scl[1] = scl[2] = 1
        elif self.RP_Slc == 7:
            if self.int and self.LP_Mdl_Slc==0:
                self.MdlH_Alpha[self.LP_intMdl_Slc] = 1
            else:
                self.Mdl_Alpha[self.LP_Mdl_Slc] = 1
            if self.int and self.LP_Mdl_Slc==0:
                if not self.MdlH_TexOn[self.LP_intMdl_Slc] == -1:
                    self.MdlH_TexOn[self.LP_intMdl_Slc] = 1
            else:
                if not self.Mdl_TexOn[self.LP_Mdl_Slc]==-1:
                    self.Mdl_TexOn[self.LP_Mdl_Slc] = 1
        elif self.RP_Slc == 8:
            self.Light_Props = [64, [0.18, 0.18, 0.18, 0.18], [0.3, 0.3, 0.3, 0.05], [-100, 100, 50, 0.0], [0.85, 0.85, 0.8, 0.85], [0.85, 0.85, 0.85, 0.85], [0, 0, 0, 0], 0]
        elif self.RP_Slc == 9:
            self.Back = [0, "", 0, [150, 100, 50], [255, 255, 255]]
            self.Base = [0, "", 0, [150, 100, -1], [255, 255, 255]]
    def RightPanel(self):
        color = [42 / 255, 42 / 255, 42 / 255], [0.188, 0.835, 0.784]
        self.Square2DMulti(15.3, 9.9, -10, 1.2, 1.2, 0.2, color, 10, True, self.RP_Slc)
        Xo,Yo,Zo,w,h = 15.9,9.3,-10,0.25,0.35   #Exit
        Vtx_Ext1 = [(Xo+w, Yo+h/2, Zo), (Xo+w,Yo+h,Zo), (Xo-w,Yo+h,Zo), (Xo-w,Yo-h,Zo), (Xo+w,Yo-h,Zo), (Xo+w,Yo-h/2,Zo)]
        Vtx_Ext2 = [(Xo,Yo,Zo), (Xo+2*w, Yo,Zo), (Xo+1.5*w, Yo+0.3*h, Zo), (Xo+2*w, Yo,Zo), (Xo+1.5*w, Yo-0.3*h, Zo)]
        glLineWidth(3)
        glColor3f(1,1,1)
        glBegin(GL_LINE_STRIP)
        for vtx in Vtx_Ext1:
            glVertex3fv(vtx)
        glEnd()
        glBegin(GL_LINE_STRIP)
        for vtx in Vtx_Ext2:
            glVertex3fv(vtx)
        glEnd()
        Xo, Yo, Zo, w, h = 15.92, 8.2, -10, 0.1, 0.6  # Info
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(Xo, Yo, Zo)
        for i in range(181):
            x = w*1.2 * math.cos(math.radians(i*5)) + Xo
            y = w*1.2 * math.sin(math.radians(i*5)) + Yo
            glVertex3f(x, y, Zo)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(Xo-w, Yo-w*2, Zo)
        glVertex3f(Xo + w, Yo - w * 2, Zo)
        glVertex3f(Xo + w, Yo - w -h, Zo)
        glVertex3f(Xo - w, Yo - w - h, Zo)
        glEnd()
        Xo, Yo, Zo, w, h = 15.9, 6.48, -10, 0.45, 0.25  # Pref
        Vtx_Pref1 = [(Xo-w, Yo+h, Zo), (Xo+w, Yo+h, Zo), (Xo-w, Yo, Zo), (Xo+w, Yo, Zo), (Xo-w, Yo-h, Zo), (Xo+w, Yo-h, Zo)]
        Vtx_Pref2 = [(Xo-w*0.8, Yo+h*1.4, Zo), (Xo-w*0.3, Yo+h*1.4, Zo), (Xo-w*0.3, Yo+h*0.6, Zo), (Xo-w*0.8, Yo+h*0.6, Zo),
                     (Xo+w*0.4, Yo+0.09, Zo), (Xo+w*0.8, Yo+0.09, Zo), (Xo+w*0.8, Yo-0.09, Zo), (Xo+w*0.4, Yo-0.09, Zo),
                     (Xo-w*0.2, Yo-h*1.4, Zo), (Xo+w*0.2, Yo-h*1.4, Zo), (Xo+w*0.2, Yo-h*0.6, Zo), (Xo-w*0.2, Yo-h*0.6, Zo)]
        glLineWidth(2)
        glBegin(GL_LINES)
        for vtx in Vtx_Pref1:
            glVertex3fv(vtx)
        glEnd()
        glBegin(GL_QUADS)
        for vtx in Vtx_Pref2:
            glVertex3fv(vtx)
        glEnd()
        Xo, Yo, Zo, w, h = 15.92, 5.1, -10, 0.4, 0.2  # Tsl
        Vtx_Tsl = [(Xo, Yo+w, Zo), (Xo-h, Yo+h, Zo), (Xo+h, Yo+h, Zo),
                   (Xo, Yo-w, Zo), (Xo-h, Yo-h, Zo), (Xo+h, Yo-h, Zo),
                   (Xo-w, Yo, Zo), (Xo-h, Yo+h, Zo), (Xo-h, Yo-h, Zo),
                   (Xo+w, Yo, Zo), (Xo+h, Yo+h, Zo), (Xo+h, Yo-h, Zo),]
        glBegin(GL_TRIANGLES)
        for vtx in Vtx_Tsl:
            glVertex3fv(vtx)
        glEnd()
        Xo, Yo, Zo, w, h = 15.92, 3.7, -10, 0.33, 0.2  # Rot
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        for i in range(180):
            x = w * math.cos(math.radians(i*2)) + Xo
            y = w * math.sin(math.radians(i*2)) + Yo
            glVertex3f(x, y, Zo)
        glEnd()
        Vtx_Rot = [(Xo-w, Yo-h/4, Zo), (Xo-w-h/2, Yo+h, Zo), (Xo-w+h, Yo+h*.6, Zo),
                   (Xo+w, Yo+h/4, Zo), (Xo+w-h, Yo-h*.6, Zo), (Xo+w+h/2, Yo-h, Zo)]
        glBegin(GL_TRIANGLES)
        for vtx in Vtx_Rot:
            glVertex3fv(vtx)
        glEnd()
        Xo, Yo, Zo, w = 15.92, 2.3, -10, 0.35 # Scl
        glBegin(GL_LINE_LOOP)
        glVertex3f(Xo-w*.8, Yo+w, Zo)
        glVertex3f(Xo + w, Yo + w, Zo)
        glVertex3f(Xo + w, Yo - w*.8, Zo)
        glVertex3f(Xo - w*.8, Yo - w*.8, Zo)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(Xo - w, Yo - w/8, Zo)
        glVertex3f(Xo - w/8, Yo -w/8, Zo)
        glVertex3f(Xo - w/8, Yo - w, Zo)
        glVertex3f(Xo - w, Yo - w, Zo)
        glEnd()
        glBegin(GL_LINE_STRIP)
        glVertex3f(Xo - w/9, Yo -w/8, Zo)
        glVertex3f(Xo + w *.7, Yo +w*.7, Zo)
        glVertex3f(Xo + w * .6, Yo + w * .15, Zo)
        glVertex3f(Xo + w * .7, Yo + w * .7, Zo)
        glVertex3f(Xo + w * .15, Yo + w * .6, Zo)
        glEnd()
        Xo, Yo, Zo = 15.92, 1.25, -10    #Colour
        a,b = 0.15,0.375
        glBegin(GL_LINE_STRIP)
        for t in range(360):
            x = a*(1-math.sin(t))*math.cos(t) + Xo
            y = b*(math.sin(t)-1) + Yo
            glVertex3f(x,y, Zo)
        glEnd()
        glPointSize(10)
        glBegin(GL_POINTS)
        glVertex3f(15.92, 0.7, -10)
        glEnd()
        Xo, Yo, Zo, w = 15.92, -.5, -10, 0.35  # Tex
        glBegin(GL_LINE_LOOP)
        glVertex3f(Xo - w, Yo + w, Zo)
        glVertex3f(Xo + w, Yo + w, Zo)
        glVertex3f(Xo + w, Yo - w, Zo)
        glVertex3f(Xo - w, Yo - w, Zo)
        glEnd()
        Vtx_Tex = [(Xo - w*.3, Yo + w, Zo), (Xo + w*.3, Yo + w, Zo), (Xo + w*.3, Yo + w*.3, Zo), (Xo - w*.3, Yo + w*.3, Zo),
                   (Xo - w*.3, Yo - w, Zo), (Xo + w*.3, Yo - w, Zo), (Xo + w*.3, Yo - w*.3, Zo), (Xo - w*.3, Yo - w*.3, Zo),
                   (Xo - w, Yo + w*.3, Zo), (Xo - w*.3, Yo + w*.3, Zo), (Xo - w*.3, Yo - w*.3, Zo), (Xo - w, Yo - w*.3, Zo),
                   (Xo + w, Yo + w*.3, Zo), (Xo + w*.3, Yo + w*.3, Zo), (Xo + w*.3, Yo - w*.3, Zo), (Xo + w, Yo - w*.3, Zo)]
        glBegin(GL_QUADS)
        for vtx in Vtx_Tex:
            glVertex3fv(vtx)
        glEnd()
        Xo, Yo, Zo, r = 15.92, -1.75, -10, 0.25  # Light
        glLineWidth(3)
        glBegin(GL_LINE_STRIP)
        glVertex3f(Xo-r*.5,Yo-1.5*r,Zo)
        for i in range(150):
            x = r * math.cos(math.radians(i * 2-60)) + Xo
            y = r * math.sin(math.radians(i * 2-60)) + Yo
            glVertex3f(x, y, Zo)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(Xo-r*.5,Yo-2*r,Zo)
        glVertex3f(Xo + r * .6, Yo-r*1.3, Zo)
        glVertex3f(Xo - r * .3, Yo - 2.5 * r, Zo)
        glVertex3f(Xo + r * .3, Yo - r * 2.1, Zo)
        glEnd()
        Xo, Yo, Zo, w = 15.92, -3.35, -10, 0.35  # Camera
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex3f(Xo - w, Yo + w*.8, Zo)
        glVertex3f(Xo + w, Yo + w*.8, Zo)
        glVertex3f(Xo + w, Yo - w*.8, Zo)
        glVertex3f(Xo - w, Yo - w*.8, Zo)
        glEnd()
        glBegin(GL_LINE_LOOP)
        for i in range(180):
            x = w/2 * math.cos(math.radians(i * 2)) + Xo
            y = w/2 * math.sin(math.radians(i * 2)) + Yo
            glVertex3f(x, y, Zo)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(Xo - w/2, Yo + w * 1.25, Zo)
        glVertex3f(Xo + w/2, Yo + w * 1.25, Zo)
        glVertex3f(Xo + w/2, Yo + w*.8, Zo)
        glVertex3f(Xo - w/2, Yo + w*.8, Zo)
        glEnd()
        self.DisplayText("Viewport : ", (1133, 7), (1, 1, 1), 3)
        if self.ortho==1:
            self.DisplayText("FRONT", (1192, 7), (1, 1, 1), 3)
        elif self.ortho==3:
            self.DisplayText("RIGHT", (1192, 7), (1, 1, 1), 3)
        elif self.ortho==7:
            self.DisplayText("TOP", (1192, 7), (1, 1, 1), 3)
        elif self.ortho == 9:
            self.DisplayText("BOTTOM", (1192, 7), (1, 1, 1), 3)
        else:
            self.DisplayText("USER", (1192, 7), (1, 1, 1), 3)

    def Color_Ramp(self):
        if self.color_picker==0:
            x,y, n,k = -9.5,3.9, 0,0
            glColor3f(131/255, 148/255, 161/255)
            glBegin(GL_QUADS)
            glVertex3f(x-0.4, y+0.4, -10)
            glVertex3f(x + 8.2, y+0.4, -10)
            glVertex3f(x + 8.2, y - 5.6, -10)
            glVertex3f(x-0.4, y - 5.6, -10)
            glEnd()
            glPointSize(25)
            glBegin(GL_POINTS)
            glColor3f(0.005, 0.005, 0.005)
            for i in range(13):
                X = x + i * 0.65
                if k>self.color_picked:
                    break
                for j in range(9):
                    Y = y - j * 0.65
                    if self.color_picked==k:
                        glVertex3f(X, Y, -10)
                        k += 1
                        break
                    k += 1
            glEnd()
            glPointSize(22)
            glBegin(GL_POINTS)
            glColor3f(0,0,0)
            for i in range(13):
                X = x + i * 0.65
                for j in range(9):
                    Y = y - j * 0.65
                    glVertex3f(X, Y, -10)
            glEnd()
            color = [(51,0,0), (102,0,0), (153,0,0), (204,0,0), (255,0,0), (255,51,51), (255,102,102), (255,153,153), (255,204,204),
                     (51,25,0), (102,51,0), (153,76,0), (204,102,0), (255,128,0), (255,153,51), (255,178,102), (255,204,153), (255,229,204),
                     (51,51,0), (102,102,0), (153,153,0), (204,204,0), (255,255,0), (255,255,51), (255,255,102), (255,255,153), (255,255,204),
                     (25,51,0), (51,102,0), (76,153,0), (102,204,0), (128,255,0), (153,255,51), (178,255,102), (204,255,153), (229,255,204),
                     (0,51,0), (0,102,0), (0,153,0), (0,204,0), (0,255,0), (51,255,51), (102,255,102), (153,255,153), (204,255,204),
                     (0,51,25), (0,102,51), (0,153,76), (0,204,102), (0,255,128), (51,255,153), (102,255,178), (153,255,204), (204,255,229),
                     (0,51,51), (0,102,102), (0,153,153), (0,204,204), (0,255,255), (51,255,255), (102,255,255), (153,255,255), (204,255,255),
                     (0,25,51), (0,51,102), (0,76,153), (0,102,204), (0,128,255), (51,153,255), (102,178,255), (153,204,255), (204,229,255),
                     (0,0,51), (0,0,102), (0,0,153), (0,0,204), (0,0,255), (51,51,255), (102,102,255), (153,153,255), (204,204,255),
                     (25,0,51), (51,0,102), (76,0,153), (102,0,204), (127,0,255), (153,51,255), (178,102,255), (204,153,255), (229,204,255),
                     (51,0,51), (102,0,102), (153,0,153), (204,0,204), (255,0,255), (255,51,255), (255,102,255), (255,153,255), (255,204,255),
                     (51,0,25), (102,0,51), (153,0,76), (204,0,102), (255,0,127), (255,51,153), (255,102,178), (255,153,204), (255,204,229),
                     (0,0,0), (32,32,32), (64,64,64), (96,96,96), (128,128,128), (160,160,160), (192,192,192), (224,224,224), (255,255,255)]
            if self.color_picked>-1:
                RGB = color[self.color_picked]
                if self.RP_Slc==2:
                    self.BGC[0], self.BGC[1], self.BGC[2] = str(RGB[0]), str(RGB[1]),str(RGB[2])
                elif self.RP_Slc==6:
                    if self.int and self.LP_Mdl_Slc==0:
                        if self.LP_Hrc_Slc==0:
                            for i in range(len(self.MdlH)):
                                clr = self.MdlH_RGBA[i]
                                clr[0], clr[1], clr[2] = RGB[0], RGB[1], RGB[2]
                        else:
                            clr = self.MdlH_RGBA[self.LP_intMdl_Slc]
                    else:
                        clr = self.Mdl_RGBA[self.LP_Mdl_Slc]
                    clr[0], clr[1], clr[2] = RGB[0], RGB[1], RGB[2]
                elif self.Ba_Slc==7 or self.Ba_Slc==15:
                    if self.Ba_Slc==7:
                        clr = self.Back[4]
                    else:
                        clr = self.Base[4]
                    clr[0], clr[1], clr[2] = RGB[0], RGB[1], RGB[2]
            glPointSize(20)
            glBegin(GL_POINTS)
            for i in range(13):
                X = x + i*0.65
                for j in range(9):
                    Y = y - j*0.65
                    c = color[n]
                    glColor3ub(c[0], c[1], c[2])
                    glVertex3f(X, Y, -10)
                    n += 1
            glEnd()

    def DIR_box(self):
        glBegin(GL_QUADS)
        glColor3f(42 / 255, 42 / 255, 42 / 255)
        glVertex3f(-5.2, 9.9, -10)
        glVertex3f(10.8, 9.9, -10)
        glVertex3f(10.8, 8.8, -10)
        glVertex3f(-5.2, 8.8, -10)
        glColor3f(1, 204 / 255, 0)
        glVertex3f(-5, 9.5, -10)
        glVertex3f(-4.2, 9.5, -10)
        glVertex3f(-4.2, 9, -10)
        glVertex3f(-5, 9, -10)
        glColor3f(0.2157, 0.2985, 0.4858)
        glVertex3f(-4, 9.7, -10)
        glVertex3f(10.6, 9.7, -10)
        glVertex3f(10.6, 9, -10)
        glVertex3f(-4, 9, -10)
        glEnd()
        glColor3f(1, 204 / 255, 0)
        glBegin(GL_LINE_STRIP)
        glVertex3f(-5, 9.55, -10)
        glVertex3f(-5, 9.75, -10)
        glVertex3f(-4.5, 9.75, -10)
        glVertex3f(-4.5, 9.6, -10)
        glVertex3f(-4.2, 9.6, -10)
        glVertex3f(-4.2, 9.52, -10)
        glEnd()
        self.DisplayText("ext/", (480, 719), (1, 1, 1), 2)
        if not self.Data_New:
            disp = "Please enter filename here"
        else:
            disp = self.Data_New
        self.DisplayText(disp, (513, 719), (1, 1, 1), 2)
        if self.fDIR_check==0 and not self.Ba_Slc==19:
            if self.music:
                if self.Data_New[-4:]==".wav":
                    self.fDIR_check = 1
            elif self.Mdl_Add:
                if self.Data_New[-4:]==".obj":
                    self.fDIR_check = 1
            elif 16<=self.Ba_Slc<=17:
                if self.Data_New[-4:]==".png":
                    self.fDIR_check = 1
        if self.fDIR_check ==1:
            if path.exists("ext/"+ self.Data_New):
                self.fDIR_check = 2
            else:
                self.fDIR_check = 0
        elif self.fDIR_check==2:
            glLineWidth(3)
            glColor3f(0, 1, 0)
            glBegin(GL_LINE_STRIP)
            glVertex3f(10.5, 9.6, -10)
            glVertex3f(10.3, 9.1, -10)
            glVertex3f(10.1, 9.3, -10)
            glVertex3f(10.2, 9.3, -10)
            glVertex3f(10.3, 9.1, -10)
            glEnd()
            if self.music:
                self.BGM = self.Data_New
            elif self.Mdl_Add and not self.Mdl_Add_Complete:
                self.Mdl.append(self.Data_New)
                self.Mdl_Add_Complete = True
            elif self.Ba_Slc==16:
                self.Back[1] = self.Data_New
            elif self.Ba_Slc==17:
                self.Base[1] = self.Data_New
        elif self.fDIR_check==3:
            if self.music or 16<=self.Ba_Slc<=17:
                glBegin(GL_QUADS)
                glColor3f(42 / 255, 42 / 255, 42 / 255)
                glVertex3f(-5.2, 8, -10)
                glVertex3f(10.8, 8, -10)
                glVertex3f(10.8, 0, -10)
                glVertex3f(-5.2, 0, -10)
                glEnd()
                glLineWidth(5)
                glBegin(GL_LINE_LOOP)
                glColor3f(1,0,0)
                glVertex3f(-5.2, 8, -10)
                glVertex3f(10.8, 8, -10)
                glVertex3f(10.8, 0, -10)
                glVertex3f(-5.2, 0, -10)
                glEnd()
                self.DisplayText("ERROR", (450, 640), (1, 0, 0), 1)
                if self.music:
                    self.DisplayText("Follow steps to proper plug-in music :", (450, 600), (1, 0, 0), 2)
                    self.DisplayText("1. Music file format :   .wav", (454, 565), (1, 0, 0), 2)
                    self.DisplayText("4. Include  '.wav'  at the end of filename", (454, 490), (1, 0, 0), 2)
                else:
                    self.DisplayText("Follow steps to proper plug-in image :", (450, 600), (1, 0, 0), 2)
                    self.DisplayText("1. Image file format :   .png", (454, 565), (1, 0, 0), 2)
                    self.DisplayText("4. Include  '.png'  at the end of filename", (454, 490), (1, 0, 0), 2)
                self.DisplayText("2. Save your file in folder :  ext/", (454, 540), (1, 0, 0), 2)
                self.DisplayText("3. Type filename correctly in system", (454, 515), (1, 0, 0), 2)
                self.DisplayText("5. System will show green tick if file exists", (454, 465), (1, 0, 0), 2)
                self.DisplayText("6. Enter to complete plug-in", (454, 440), (1, 0, 0), 2)
                self.DisplayText("Press any keys to continue ...", (454, 400), (1, 1, 1), 2)
            elif self.Mdl_Add:
                glBegin(GL_QUADS)
                glColor3f(42 / 255, 42 / 255, 42 / 255)
                glVertex3f(-5.2, 8, -10)
                glVertex3f(10.8, 8, -10)
                glVertex3f(10.8, -2, -10)
                glVertex3f(-5.2, -2, -10)
                glEnd()
                glLineWidth(5)
                glBegin(GL_LINE_LOOP)
                glColor3f(1, 0, 0)
                glVertex3f(-5.2, 8, -10)
                glVertex3f(10.8, 8, -10)
                glVertex3f(10.8, -2, -10)
                glVertex3f(-5.2, -2, -10)
                glEnd()
                self.DisplayText("ERROR", (450, 640), (1, 0, 0), 1)
                self.DisplayText("Follow steps to proper plug-in model :", (450, 600), (1, 0, 0), 2)
                self.DisplayText("1. Model file format :   .obj", (454, 565), (1, 0, 0), 2)
                self.DisplayText("2. Save your file in folder :  ext/", (454, 540), (1, 0, 0), 2)
                self.DisplayText("3. Type filename correctly in system", (454, 515), (1, 0, 0), 2)
                self.DisplayText("4. Include  '.obj'  at the end of filename", (454, 490), (1, 0, 0), 2)
                self.DisplayText("5. System will show green tick if file exists", (454, 465), (1, 0, 0), 2)
                self.DisplayText("6. Enter to complete plug-in", (454, 440), (1, 0, 0), 2)
                self.DisplayText("Note :", (452, 400), (1, 0, 0), 2)
                self.DisplayText("# check Triangulate surface (blender export)", (454, 375), (1, 0, 0), 2)
                self.DisplayText("Press any keys to continue ...", (454, 325), (1, 1, 1), 2)
        elif self.Ba_Slc==19:
            glBegin(GL_QUADS)
            glColor3f(42 / 255, 42 / 255, 42 / 255)
            glVertex3f(-5.2, 8, -10)
            glVertex3f(10.8, 8, -10)
            glVertex3f(10.8, 0, -10)
            glVertex3f(-5.2, 0, -10)
            glEnd()
            glLineWidth(5)
            glBegin(GL_LINE_LOOP)
            glColor3f(0.5, 0, 1)
            glVertex3f(-5.2, 8, -10)
            glVertex3f(10.8, 8, -10)
            glVertex3f(10.8, 0, -10)
            glVertex3f(-5.2, 0, -10)
            glEnd()
            self.DisplayText("INFORMATION", (450, 640), (0.5,0,1), 1)
            self.DisplayText("Follow steps to proper save image :", (450, 600), (0.5,0,1), 2)
            self.DisplayText("1. Image file format :   .png", (454, 565), (0.5,0,1), 2)
            self.DisplayText("2. Free to create own filename", (454, 540), (0.5,0,1), 2)
            self.DisplayText("3. Only with available characters", (454, 515), (0.5,0,1), 2)
            self.DisplayText("4. Exclude  '.png'  at the end of filename", (454, 490), (0.5,0,1), 2)
            self.DisplayText("5. Enter to complete saving image", (454, 465), (0.5,0,1), 2)
            self.DisplayText("Note :", (452, 425), (0.5,0,1), 2)
            self.DisplayText("# Backspace to start insert filename", (454, 400), (0.5,0,1), 2)

    def Data_update(self):
        if self.Mdl_Add:
            if not self.Data_Amend:
                self.Data_Amend = True
                self.Data_New = ""
                self.fDIR_check = 0
            self.DIR_box()
        elif self.RP_Slc == 2:    #Pref mode
            if self.RGB_Pref>-1:    #RGB_pref slc
                if not self.Data_Amend:
                    self.Data_Amend = True
                    self.Data_Backup = self.BGC[self.RGB_Pref]
                    self.Data_New = ""
                if len(self.Data_New)>0:
                    self.BGC[self.RGB_Pref] = self.Data_New
            elif self.cursor_3D_Pref>-1:
                if not self.Data_Amend:
                    self.Data_Amend = True
                    self.Data_Backup = self.cursor_3D_pos[self.cursor_3D_Pref]
                    self.Data_New = ""
                if len(self.Data_New) > 0:
                    if '-' in self.Data_New and len(self.Data_New) == 1:
                        pass
                    else:
                        self.cursor_3D_pos[self.cursor_3D_Pref] = float(self.Data_New)
            elif self.music:
                if not self.Data_Amend:
                    self.Data_Amend = True
                    self.Data_New = ""
                    self.fDIR_check = 0
                    if self.BGM:
                        self.Data_Backup = self.BGM
                    else:
                        self.Data_Backup = ""
                self.DIR_box()
        elif 3<=self.RP_Slc<=5:
            if self.transform>-1:
                if not self.Data_Amend:
                    self.Data_Amend = True
                    self.Data_New = ""
                    if self.RP_Slc==3:
                        if self.int and self.LP_Mdl_Slc==0:
                            pos = self.MdlH_POS[self.LP_intMdl_Slc]
                        else:
                            pos = self.Mdl_POS[self.LP_Mdl_Slc]
                        self.Data_Backup = pos[self.transform]
                    elif self.RP_Slc==4:
                        if self.int and self.LP_Mdl_Slc==0:
                            deg = self.MdlH_DEG[self.LP_intMdl_Slc]
                        else:
                            deg = self.Mdl_DEG[self.LP_Mdl_Slc]
                        self.Data_Backup = deg[self.transform]
                    elif self.RP_Slc==5:
                        if self.int and self.LP_Mdl_Slc==0:
                            scl = self.MdlH_SCL[self.LP_intMdl_Slc]
                        else:
                            scl = self.Mdl_SCL[self.LP_Mdl_Slc]
                        self.Data_Backup = scl[self.transform]
                if len(self.Data_New) > 0:
                    if '-' in self.Data_New and len(self.Data_New) == 1:
                        pass
                    else:
                        if self.RP_Slc==3:
                            if self.int and self.LP_Mdl_Slc==0:
                                pos = self.MdlH_POS[self.LP_intMdl_Slc]
                            else:
                                pos = self.Mdl_POS[self.LP_Mdl_Slc]
                            pos[self.transform] = float(self.Data_New)
                        elif self.RP_Slc==4:
                            if self.int and self.LP_Mdl_Slc==0:
                                deg = self.MdlH_DEG[self.LP_intMdl_Slc]
                            else:
                                deg = self.Mdl_DEG[self.LP_Mdl_Slc]
                            deg[self.transform] = float(self.Data_New)
                        elif self.RP_Slc==5:
                            if self.int and self.LP_Mdl_Slc==0:
                                scl = self.MdlH_SCL[self.LP_intMdl_Slc]
                            else:
                                scl = self.Mdl_SCL[self.LP_Mdl_Slc]
                            scl[self.transform] = float(self.Data_New)
        elif self.RP_Slc == 6:
            if self.RGBA>-1:
                if not self.Data_Amend:
                    self.Data_Amend = True
                    self.Data_New = ""
                    if self.int and self.LP_Mdl_Slc==0:
                        clr = self.MdlH_RGBA[self.LP_intMdl_Slc]
                    else:
                        clr = self.Mdl_RGBA[self.LP_Mdl_Slc]
                    if self.RGBA == 4:
                        self.Data_Backup = [clr[0], clr[1], clr[2]]
                    else:
                        self.Data_Backup = clr[self.RGBA]
                if len(self.Data_New)>0:
                    if self.int and self.LP_Mdl_Slc==0:
                        clr = self.MdlH_RGBA[self.LP_intMdl_Slc]
                    else:
                        clr = self.Mdl_RGBA[self.LP_Mdl_Slc]
                    if self.RGBA==3:
                        clr[self.RGBA] = float(self.Data_New)
                    elif self.RGBA==4:
                        self.Hex = self.Data_New
                        if len(self.Hex)>0:
                            newData = self.Data_New
                            if len(newData)<6:
                                for i in range(6-len(newData)):
                                    newData += '0'
                            RGB = tuple(int(newData[i:i + 2], 16) for i in (0, 2, 4))
                            clr[0], clr[1], clr[2] = RGB[0], RGB[1], RGB[2]
                    else:
                        clr[self.RGBA] = int(self.Data_New)
        elif self.RP_Slc == 8:
            if 30<=self.Light_Set<=33:
                props = self.Light_Props[3]
                if not self.Data_Amend:
                    self.Data_Amend = True
                    self.Data_New = ""
                    self.Data_Backup = props[self.Light_Set-30]
                if len(self.Data_New) > 0:
                    if '-' in self.Data_New and len(self.Data_New) == 1:
                        pass
                    else:
                        props[self.Light_Set - 30] = float(self.Data_New)
        elif self.RP_Slc==9:
            if 16 <= self.Ba_Slc <= 17 or self.Ba_Slc==19:
                if not self.Data_Amend:
                    self.Data_Amend = True
                    self.Data_New = ""
                    self.fDIR_check = 0
                    if self.Ba_Slc==16:
                        if self.Back[1]:
                            self.Data_Backup = self.Back[1]
                        else:
                            self.Data_Backup = ""
                    elif self.Ba_Slc==17:
                        if self.Base[1]:
                            self.Data_Backup = self.Back[1]
                        else:
                            self.Data_Backup = ""
                    else:
                        self.Data_New = "Untitled"
                self.DIR_box()
            elif 0<=self.Ba_Slc<=2 or 8<=self.Ba_Slc<=10:
                if not self.Data_Amend:
                    self.Data_Amend = True
                    self.Data_New = ""
                    if 0<=self.Ba_Slc<=2:
                        pos = self.Back[3]
                        self.Data_Backup = pos[self.Ba_Slc]
                    else:
                        pos = self.Base[3]
                        self.Data_Backup = pos[self.Ba_Slc-8]
                if len(self.Data_New) > 0:
                    if '-' in self.Data_New and len(self.Data_New) == 1:
                        pass
                    else:
                        if 0 <= self.Ba_Slc <= 2:
                            pos = self.Back[3]
                            pos[self.Ba_Slc] = int(self.Data_New)
                        else:
                            pos = self.Base[3]
                            pos[self.Ba_Slc - 8] = int(self.Data_New)

    def Info_box(self):
        if self.info==0:
            glLineWidth(4)
            glBegin(GL_LINES)
            glVertex3f(-3.2, 7.7, -10)
            glVertex3f(8.8, 7.7, -10)
            glVertex3f(1.8, 7.7, -10)
            glVertex3f(1.8, 4, -10)
            glVertex3f(-3.2, 2.8, -10)
            glVertex3f(8.8, 2.8, -10)
            glVertex3f(0.8, 2.8, -10)
            glVertex3f(0.8, -4.8, -10)
            glVertex3f(-3.2, -6.2, -10)
            glVertex3f(8.8, -6.2, -10)
            glVertex3f(-0.2, -6.2, -10)
            glVertex3f(-0.2, -8.4, -10)
            glEnd()
            self.DisplayText("MOUSE", (680, 673), (1, 1, 1), 1)
            self.DisplayText("Left", (535, 635), (1, 1, 1), 2)
            self.DisplayText("Right", (535, 610), (1, 1, 1), 2)
            self.DisplayText("Middle", (535, 585), (1, 1, 1), 2)
            self.DisplayText("Hold", (535, 560), (1, 1, 1), 2)
            self.DisplayText("Shift + Middle", (535, 535), (1, 1, 1), 2)
            self.DisplayText("Select option", (730, 635), (1, 1, 1), 2)
            self.DisplayText("Begin action (transform)", (730, 610), (1, 1, 1), 2)
            self.DisplayText("Rotate view", (730, 585), (1, 1, 1), 2)
            self.DisplayText("Adjust transformation", (730, 560), (1, 1, 1), 2)
            self.DisplayText("Translate view", (730, 535), (1, 1, 1), 2)

            self.DisplayText("HOTKEYS", (670, 490), (1, 1, 1), 1)
            self.DisplayText("esc", (540, 450), (1, 1, 1), 2)
            self.DisplayText("I", (540, 425), (1, 1, 1), 2)
            self.DisplayText("spacebar", (540, 400), (1, 1, 1), 2)
            self.DisplayText("G", (540, 375), (1, 1, 1), 2)
            self.DisplayText("R", (540, 350), (1, 1, 1), 2)
            self.DisplayText("S", (540, 325), (1, 1, 1), 2)
            self.DisplayText("C", (540, 300), (1, 1, 1), 2)
            self.DisplayText("T", (540, 275), (1, 1, 1), 2)
            self.DisplayText("L", (540, 250), (1, 1, 1), 2)
            self.DisplayText("O", (540, 225), (1, 1, 1), 2)
            self.DisplayText("Q", (540, 200), (1, 1, 1), 2)

            self.DisplayText("Exit / Cancel action", (695, 450), (1, 1, 1), 2)
            self.DisplayText("Information", (695, 425), (1, 1, 1), 2)
            self.DisplayText("Preferences :", (695, 400), (1, 1, 1), 2)
            self.DisplayText("Mode|3DPivot|RGB|Music", (810, 401), (1, 1, 1), 3)
            self.DisplayText("Grab : Translate object", (695, 375), (1, 1, 1), 2)
            self.DisplayText("Rotate : Rotate object", (695, 350), (1, 1, 1), 2)
            self.DisplayText("Scaling : Scale object", (695, 325), (1, 1, 1), 2)
            self.DisplayText("Colour : Colour shade", (695, 300), (1, 1, 1), 2)
            self.DisplayText("Texture : uvTexture Map", (695, 275), (1, 1, 1), 2)
            self.DisplayText("Lighting : Illumination", (695, 250), (1, 1, 1), 2)
            self.DisplayText("Render : Rendering object", (695, 225), (1, 1, 1), 2)
            self.DisplayText("Panel : Hide / Unhide", (695, 200), (1, 1, 1), 2)

            self.DisplayText("ADDITION HOTKEYS", (600, 155), (1, 1, 1), 1)
            self.DisplayText("X", (548, 115), (1, 1, 1), 2)
            self.DisplayText("Y", (548, 90), (1, 1, 1), 2)
            self.DisplayText("Z", (548, 65), (1, 1, 1), 2)
            self.DisplayText("Transform clipping to X-axis (Hold)", (655, 115), (1, 1, 1), 2)
            self.DisplayText("Transform clipping to Y-axis (Hold)", (655, 90), (1, 1, 1), 2)
            self.DisplayText("Transform clipping to Z-axis (Hold)", (655, 65), (1, 1, 1), 2)
        elif self.info == 1:
            glLineWidth(4)
            glBegin(GL_LINES)
            glVertex3f(2.8, 8.5, -10)
            glVertex3f(2.8, -8.5, -10)
            glVertex3f(-3.2, 17/6, -10)
            glVertex3f(8.8, 17 / 6, -10)
            glVertex3f(-3.2, -17 / 6, -10)
            glVertex3f(8.8, -17 / 6, -10)
            glEnd()
            self.DisplayText("Transformation :", (510, 665), (1, 1, 1), 1)
            self.DisplayText("> Translation (G)", (530, 625), (1, 1, 1), 2)
            self.DisplayText("> Rotation     (R)", (530, 600), (1, 1, 1), 2)
            self.DisplayText("> Scaling       (S)", (530, 575), (1, 1, 1), 2)
            self.DisplayText("# Select object from", (520, 530), (1, 1, 1), 2)
            self.DisplayText("  Model Panel to", (520, 510), (1, 1, 1), 2)
            self.DisplayText("  transform", (520, 490), (1, 1, 1), 2)
            self.DisplayText("Shading :", (510, 450), (1, 1, 1), 1)
            self.DisplayText("> Color     (C)", (530, 410), (1, 1, 1), 2)
            self.DisplayText("> Texture  (T)", (530, 385), (1, 1, 1), 2)
            self.DisplayText("> Lighting  (L)", (530, 360), (1, 1, 1), 2)
            self.DisplayText("# Adjust object RGBA", (520, 325), (1, 1, 1), 2)
            self.DisplayText("# Adjust illumination by", (520, 300), (1, 1, 1), 2)
            self.DisplayText("Diffuse,Specular,Ambient", (520, 278), (1, 1, 1), 2)
            self.DisplayText("Render(O) :", (510, 237), (1, 1, 1), 1)
            self.DisplayText("> Add Background", (530, 200), (1, 1, 1), 2)
            self.DisplayText("> Add Base Plane", (530, 175), (1, 1, 1), 2)
            self.DisplayText("> Save image", (530, 150), (1, 1, 1), 2)
            self.DisplayText("# Add colour / image to", (520, 120), (1, 1, 1), 2)
            self.DisplayText("  Background, Baseplane", (520, 100), (1, 1, 1), 2)
            self.DisplayText("# Crop image before save", (520, 75), (1, 1, 1), 2)
            self.DisplayText("Import :", (750, 665), (1, 1, 1), 1)
            self.DisplayText("> Model  (.obj)", (770, 625), (1, 1, 1), 2)
            self.DisplayText("> Music  (.wav)", (770, 600), (1, 1, 1), 2)
            self.DisplayText("> Image  (.png)", (770, 575), (1, 1, 1), 2)
            self.DisplayText("# To proper plug-in,", (760, 530), (1, 1, 1), 2)
            self.DisplayText("  include file format", (760, 510), (1, 1, 1), 2)
            self.DisplayText("  at the end of filename", (760, 490), (1, 1, 1), 2)
            self.DisplayText("View :", (750, 450), (1, 1, 1), 1)
            self.DisplayText("> RightPanel : Tools", (770, 410), (1, 1, 1), 2)
            self.DisplayText("> LeftPanel : Model, Info,", (770, 385), (1, 1, 1), 2)
            self.DisplayText("Hierarchy", (878, 360), (1, 1, 1), 2)
            self.DisplayText("# Adjust view to ease", (760, 325), (1, 1, 1), 2)
            self.DisplayText("  transform, shade and", (760, 302), (1, 1, 1), 2)
            self.DisplayText("  render (key : 1-9)", (760, 278), (1, 1, 1), 2)
            self.DisplayText("Preferences(spacebar) :", (750, 237), (1, 1, 1), 1)
            self.DisplayText("> Shading mode", (770, 200), (1, 1, 1), 2)
            self.DisplayText("> 3D Pivot Point", (770, 175), (1, 1, 1), 2)
            self.DisplayText("> Background colour", (770, 150), (1, 1, 1), 2)
            self.DisplayText("> Background music", (770, 125), (1, 1, 1), 2)
            self.DisplayText("# Adjust preferences to ", (760, 98), (1, 1, 1), 2)
            self.DisplayText("  suit your style", (760, 75), (1, 1, 1), 2)
        elif self.info == 2:
            self.DisplayText("STEPS TO PLUG-IN ...", (450, 670), (1, 1, 1), 1)
            self.DisplayText("# Ensure plug-in in right tool/panel :", (450, 635), (1, 1, 1), 2)
            self.DisplayText("1. Model Panel > model", (463, 600), (1, 1, 1), 2)
            self.DisplayText("2. Preferences > music", (463, 575), (1, 1, 1), 2)
            self.DisplayText("3. Render > image", (463, 550), (1, 1, 1), 2)
            self.DisplayText("# Ensure correct file format use :", (450, 500), (1, 1, 1), 2)
            self.DisplayText("1. Model > Wavefront(.obj)", (463, 465), (1, 1, 1), 2)
            self.DisplayText("2. Music > Windows Wave(.wav)", (463, 437), (1, 1, 1), 2)
            self.DisplayText("3. Image > Portable Network Graphics(.png)", (463, 408), (1, 1, 1), 2)
            self.DisplayText("# Ensure file is save/loacte in correct folder :", (450, 355), (1, 1, 1), 2)
            self.DisplayText("1. fDIR > ext", (464, 322), (1, 1, 1), 2)
            self.DisplayText("2. ext folder comes with the program folder", (464, 297), (1, 1, 1), 2)
            self.DisplayText("# Addition to plug-in model :", (450, 250), (1, 1, 1), 2)
            self.DisplayText("1. Do not rename any filename of the model", (463, 225), (1, 1, 1), 2)
            self.DisplayText("2. Place all relevant file: Obj, Mtl, Tex in /ext folder", (463, 200), (1, 1, 1), 2)
            self.DisplayText("# How to load file :", (450, 150), (1, 1, 1), 2)
            self.DisplayText("1. Type filename exactly", (463, 125), (1, 1, 1), 2)
            self.DisplayText("2. Include file format at end of filename", (463, 100), (1, 1, 1), 2)
            self.DisplayText("3. System will indicate with green tick if file exist", (463, 75), (1, 1, 1), 2)

    def Detail(self):
        self.Square2DSingle(-16.5, 4.2, -10, 6.5, 0.85, (0.188, 0.835, 0.784))
        color = [42 / 255, 42 / 255, 42 / 255], [0.188-0.5, 0.835-0.5, 0.784-0.5]
        color_switch = [0,204/255,102/255], [238/255, 62/255, 64/255]
        if self.RP_Slc == 0:
            self.DisplayText("EXIT", (103, 509), (1, 1, 1), 2)
            if self.exit==1:
                glBegin(GL_QUADS)
                glColor3f(42 / 255, 42 / 255, 42 / 255)
                glVertex3f(-3, 1.1, -10)
                glVertex3f(8.6, 1.1, -10)
                glVertex3f(8.6, -1.1, -10)
                glVertex3f(-3, -1.1, -10)
                glEnd()
                glLineWidth(8)
                glBegin(GL_LINE_LOOP)
                glColor3f(1, 0,0)
                glVertex3f(-3, 1.1, -10)
                glVertex3f(8.6, 1.1, -10)
                glVertex3f(8.6, -1.1, -10)
                glVertex3f(-3, -1.1, -10)
                glEnd()
                self.DisplayText("Press ENTER to confirm exit !", (580, 370), (1, 1, 1), 1)
        elif self.RP_Slc == 1:
            self.DisplayText("INFORMATION", (64, 509), (1, 1, 1), 2)
            self.Square2DMulti(-15, 3, -10, 3.5, 1, 0.3, color, 3, True, self.info)
            self.DisplayText("Keys", (100, 460), (1, 1, 1), 1)
            self.DisplayText("Functions", (80, 411), (1, 1, 1), 1)
            self.DisplayText("Import", (94, 363), (1, 1, 1), 1)
            glBegin(GL_QUADS)
            glColor3f(42 / 255, 42 / 255, 42 / 255)
            glVertex3f(-5.2, 9, -10)
            glVertex3f(10.8, 9, -10)
            glVertex3f(10.8, -9, -10)
            glVertex3f(-5.2,-9, -10)
            glEnd()
            glLineWidth(5)
            glBegin(GL_LINE_LOOP)
            glColor3f(1,127/255,80/255)
            glVertex3f(-5.2, 9, -10)
            glVertex3f(10.8, 9, -10)
            glVertex3f(10.8, -9, -10)
            glVertex3f(-5.2, -9, -10)
            glEnd()
            self.Info_box()
        elif self.RP_Slc==2:
            self.DisplayText("PREFERENCE", (69, 509), (1, 1, 1), 2)
            self.Square2DMulti(-16.5, 3.2, -10, 1, 0.9, 0.15, color, 4, True, -1)
            self.Square2DMulti(-15.35, 3.2, -10, 2.63, 0.9, 0.1, color, 2, False, self.Shading) #Solid/Wire
            self.Square2DMulti(-15.35, 2.15, -10, 1.335, 0.9, 0.1, color, 3, False, self.RGB_Pref) #RGB
            self.Square2DMulti(-11, 2.15, -10, 1, 0.9, 0.1, color, 1, False, self.color_picker)
            self.Square2DMulti(-15.35, 1.1, -10, 1.335, 0.9, 0.1, color, 3, False, self.cursor_3D_Pref)  # 3D XYZ
            self.Square2DMulti(-11, 1.1, -10, 1, 0.9, 0.15, color_switch, 1, True, self.cursor_3D)
            self.Square2DSingle(-15.35, 0.05, -10, 4.2, 0.9, (0.2157, 0.2985, 0.4858)) #bgm
            self.Square2DMulti(-11, 0.05, -10, 1, 0.9, 0.15, color_switch, 1, True, self.Mute)
            # Icon
            Xo, Yo, Zo, r = -10.5, 1.7, -10, 0.3
            glColor3ub(int(self.BGC[0]), int(self.BGC[1]), int(self.BGC[2]))
            glBegin(GL_QUADS)
            glVertex3f(Xo + r, Yo + r, Zo)
            glVertex3f(Xo + r, Yo - r, Zo)
            glVertex3f(Xo - r, Yo - r, Zo)
            glVertex3f(Xo - r, Yo + r, Zo)
            glEnd()
            glColor3f(1,1,1)
            glLineWidth(1)
            Xo, Yo, Zo, r = -16, 2.75, -10, 0.25
            glBegin(GL_LINE_STRIP)
            for i in range(90):
                x = r * math.cos(math.radians(i * 2+270)) + Xo
                y = r * math.sin(math.radians(i * 2+270)) + Yo
                glVertex3f(x, y, Zo)
            glEnd()
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(Xo, Yo, Zo)
            for i in range(90):
                x = r * math.cos(math.radians(i * 2 + 90)) + Xo
                y = r * math.sin(math.radians(i * 2 + 90)) + Yo
                glVertex3f(x, y, Zo)
            glEnd()
            Xo, Yo, Zo, r = -16, 1.7, -10, 0.25
            glBegin(GL_POLYGON)
            glVertex3f(Xo + r, Yo - r, Zo)
            glVertex3f(Xo - r, Yo - r, Zo)
            glVertex3f(Xo - r, Yo + r/5, Zo)
            glVertex3f(Xo - r*.4, Yo + r*.8, Zo)
            glVertex3f(Xo, Yo - r / 3, Zo)
            glVertex3f(Xo + r*.65, Yo+r/3, Zo)
            glEnd()
            glBegin(GL_LINE_STRIP)
            glVertex3f(Xo + r, Yo - r, Zo)
            glVertex3f(Xo + r, Yo+r, Zo)
            glVertex3f(Xo - r, Yo + r, Zo)
            glVertex3f(Xo - r, Yo - r, Zo)
            glEnd()
            Xo, Yo, Zo, r = -16, 0.65, -10, 0.23
            glBegin(GL_LINE_STRIP)
            for i in range(180):
                x = r * math.cos(math.radians(i * 2)) + Xo
                y = r * math.sin(math.radians(i * 2)) + Yo
                glVertex3f(x, y, Zo)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(Xo - 1.5*r, Yo, Zo)
            glVertex3f(Xo + 1.5*r, Yo, Zo)
            glVertex3f(Xo, Yo + 1.5*r, Zo)
            glVertex3f(Xo, Yo - 1.5 * r, Zo)
            glEnd()
            Xo, Yo, Zo, r = -16, -0.4, -10, 0.23
            glBegin(GL_POLYGON)
            glVertex3f(Xo+r/3, Yo+r, Zo)
            glVertex3f(Xo + r*1.5, Yo + r, Zo)
            glVertex3f(Xo + r * .8, Yo + r/2, Zo)
            glVertex3f(Xo, Yo-r*1.2, Zo)
            glEnd()
            glBegin(GL_TRIANGLE_FAN)
            for i in range(180):
                x = r/2 * math.cos(math.radians(i * 2)) + Xo-r/2
                y = r/2 * math.sin(math.radians(i * 2)) + Yo-r*.7
                glVertex3f(x, y, Zo)
            glEnd()
            if not self.BGM and not self.music:
                glLineWidth(3)
                glBegin(GL_LINES)
                glVertex3f(Xo+r*12, Yo+r, Zo)
                glVertex3f(Xo+r*12, Yo-r, Zo)
                glVertex3f(Xo + r * 11, Yo, Zo)
                glVertex3f(Xo + r * 13, Yo, Zo)
                glEnd()
            # Word
            self.DisplayText("Solid", (75, 470), (1, 1, 1), 2)
            self.DisplayText("Wired", (175, 470), (1, 1, 1), 2)

            Display_RGB = [self.BGC[0], self.BGC[1], self.BGC[2]]
            Display_3Dpos = [str(self.cursor_3D_pos[0]), str(self.cursor_3D_pos[1]), str(self.cursor_3D_pos[2])]
            if self.RGB_Pref>-1:
                Display_RGB[self.RGB_Pref] = self.Data_New
            elif self.cursor_3D_Pref>-1:
                Display_3Dpos[self.cursor_3D_Pref] = self.Data_New
            self.DisplayText(Display_RGB[0], (59, 432), (1, 1, 1), 2)
            self.DisplayText(Display_RGB[1], (113, 432), (1, 1, 1), 2)
            self.DisplayText(Display_RGB[2], (167, 432), (1, 1, 1), 2)
            self.DisplayText(Display_3Dpos[0], (51, 393), (1, 1, 1), 2)
            self.DisplayText(Display_3Dpos[1], (105, 393), (1, 1, 1), 2)
            self.DisplayText(Display_3Dpos[2], (159, 393), (1, 1, 1), 2)
            BGM = self.BGM
            if self.BGM:
                BGM = BGM[:-4]
                if len(BGM)>13:
                    BGM = BGM[:(13-len(BGM))]
            if self.music:
                if self.fDIR_check==2 and self.BGM:
                    self.DisplayText(BGM, (51, 353), (1, 1, 1), 2)
                else:
                    self.DisplayText("Loading...", (51, 353), (1, 1, 1), 2)
            else:
                if self.BGM:
                    self.DisplayText(BGM, (51, 353), (1, 1, 1), 2)
            if self.cursor_3D==1:
                self.DisplayText("On", (218, 393), (1, 1, 1), 2)
            elif self.cursor_3D==0:
                self.DisplayText("Off", (217, 393), (1, 1, 1), 2)
            if self.Mute==0:
                self.DisplayText("Off", (217, 353), (1, 1, 1), 2)
            elif self.Mute==1:
                self.DisplayText("On", (218, 353), (1, 1, 1), 2)
        elif 3<=self.RP_Slc<=5:
            display = []
            self.Square2DMulti(-16.5, 3, -10, 1.7, 1, 0.3, color, 3, True, self.axis)
            self.Square2DMulti(-14.5, 3, -10, 4.5, 1, 0.3, color, 3, True, self.transform)
            self.DisplayText("X", (30, 460), (1, 1, 1), 1)
            self.DisplayText("Y", (30, 411), (1, 1, 1), 1)
            self.DisplayText("Z", (30, 363), (1, 1, 1), 1)
            if self.RP_Slc==3:
                self.DisplayText("LOCATION", (78, 509), (1, 1, 1), 2)
                if self.Mdl_list>0 and self.Mdl_POS:
                    if self.int and self.LP_Mdl_Slc==0:
                        pos = self.MdlH_POS[self.LP_intMdl_Slc]
                    else:
                        pos = self.Mdl_POS[self.LP_Mdl_Slc]
                    display = [str(pos[0]), str(pos[1]), str(pos[2])]
                    if self.transform>-1:
                        display[self.transform] = self.Data_New
            elif self.RP_Slc==4:
                self.DisplayText("ROTATION", (78, 509), (1, 1, 1), 2)
                if self.Mdl_list > 0 and self.Mdl_DEG:
                    if self.int and self.LP_Mdl_Slc==0:
                        deg = self.MdlH_DEG[self.LP_intMdl_Slc]
                    else:
                        deg = self.Mdl_DEG[self.LP_Mdl_Slc]
                    display = [str(deg[0]), str(deg[1]), str(deg[2])]
                    self.DisplayText("o", (240, 475), (1, 1, 1), 3)
                    self.DisplayText("o", (240, 425), (1, 1, 1), 3)
                    self.DisplayText("o", (240, 377), (1, 1, 1), 3)
                    if self.transform>-1:
                        display[self.transform] = self.Data_New
            elif self.RP_Slc==5:
                self.DisplayText("SCALING", (85, 509), (1, 1, 1), 2)
                if self.Mdl_list > 0 and self.Mdl_SCL:
                    if self.int and self.LP_Mdl_Slc==0:
                        scl = self.MdlH_SCL[self.LP_intMdl_Slc]
                    else:
                        scl = self.Mdl_SCL[self.LP_Mdl_Slc]
                    display = [str(scl[0]), str(scl[1]), str(scl[2])]
                    if self.transform>-1:
                        display[self.transform] = self.Data_New
            if self.int and self.LP_Mdl_Slc==0 and self.LP_intMdl_Slc == -1:
                display = ['N/A', 'N/A', 'N/A']
            if display:
                for i in range(3):
                    if len(display[i])>15:
                        display[i] = display[i][:(15-len(display[i]))]
                self.DisplayText(display[0], (93, 462), (1, 1, 1), 2)
                self.DisplayText(display[1], (93, 413), (1, 1, 1), 2)
                self.DisplayText(display[2], (93, 365), (1, 1, 1), 2)
        elif self.RP_Slc==6:
            self.DisplayText("COLOUR", (88, 509), (1, 1, 1), 2)
            self.Square2DMulti(-16.5, 3.23, -10, 0.9, 0.9, 0.15, color, 4, True, self.RGBA)
            self.Square2DMulti(-15.5, 3.23, -10, 2, 0.9, 0.15, color, 4, True, self.RGBA)
            self.Square2DMulti(-13.3, 3.23, -10, 3.31, 1.95, 0.15, color, 1, True, self.RGBA-4)
            self.Square2DSingle(-13.3, 1.13, -10, 2.3, 1.95, (42/255, 42/255, 42/255))
            self.Square2DMulti(-11, 1.13, -10, 1, 1.95, 0.15, color, 1, True, self.color_picker)
            self.DisplayText("R", (13, 471), (1, 1, 1), 1)
            self.DisplayText("G", (13, 431), (1, 1, 1), 1)
            self.DisplayText("B", (13, 392), (1, 1, 1), 1)
            self.DisplayText("A", (13, 353), (1, 1, 1), 1)
            self.DisplayText("HEX", (161, 471), (1, 1, 1), 1)
            if self.int and self.LP_Mdl_Slc==0:
                clr = self.MdlH_RGBA[self.LP_intMdl_Slc]
            else:
                clr = self.Mdl_RGBA[self.LP_Mdl_Slc]
            self.Hex = '%02x%02x%02x' % (clr[0], clr[1], clr[2])
            display = [str(clr[0]),str(clr[1]),str(clr[2]),str(clr[3]), self.Hex.upper()]
            if self.RGBA>-1:
                display[self.RGBA] = self.Data_New
            self.DisplayText(display[0], (65, 472), (1, 1, 1), 2)
            self.DisplayText(display[1], (65, 432), (1, 1, 1), 2)
            self.DisplayText(display[2], (65, 393), (1, 1, 1), 2)
            self.DisplayText(display[3], (65, 354), (1, 1, 1), 2)
            self.DisplayText("#", (138, 431), (1, 1, 1), 1)
            self.DisplayText(display[4], (158, 433), (1, 1, 1), 2)
            glLineWidth(3)
            glBegin(GL_LINES)
            glVertex3f(-13.3, 2.25, -10)
            glVertex3f(-10, 2.25, -10)
            glVertex3f(-11, 1.0, -10)
            glVertex3f(-11, -0.7, -10)
            glEnd()
            glBegin(GL_TRIANGLES)
            if self.color_picker==-1:
                glVertex3f(-10.7, 0.65, -10)
                glVertex3f(-10.2, 0.15, -10)
                glVertex3f(-10.7, -0.35, -10)
            else:
                glVertex3f(-10.2, 0.65, -10)
                glVertex3f(-10.7, 0.15, -10)
                glVertex3f(-10.2, -0.35, -10)
            glEnd()
            glColor4f(clr[0]/255, clr[1]/255, clr[2]/255, clr[3])
            glBegin(GL_QUADS)
            glVertex3f(-13, 0.9, -10)
            glVertex3f(-11.3, 0.9, -10)
            glVertex3f(-11.3, -0.6, -10)
            glVertex3f(-13, -0.6, -10)
            glEnd()
        elif self.RP_Slc == 7:
            self.DisplayText("TEXTURE", (83, 509), (1, 1, 1), 2)
            glColor3f(0, 0, 0)
            glBegin(GL_QUADS)
            glVertex3f(-16.38, 3.2, -10)
            glVertex3f(-12.38, 3.2, -10)
            glVertex3f(-12.38, -0.8, -10)
            glVertex3f(-16.38, -0.8, -10)
            glEnd()
            if self.Mdl_TexFile[self.LP_Mdl_Slc] or self.int and self.MdlH_TexFile[self.LP_intMdl_Slc]:
                if self.int and self.LP_Mdl_Slc==0:
                    self.loadTexture('ext/Internal/' + self.MdlH_TexFile[self.LP_intMdl_Slc])
                else:
                    self.loadTexture('ext/'+self.Mdl_TexFile[self.LP_Mdl_Slc])
                glBegin(GL_QUADS)
                glTexCoord2f(0,1)
                glVertex3f(-16.38, 3.2,-10)
                glTexCoord2f(1, 1)
                glVertex3f(-12.38, 3.2, -10)
                glTexCoord2f(1, 0)
                glVertex3f(-12.38, -0.8, -10)
                glTexCoord2f(0, 0)
                glVertex3f(-16.38, -0.8, -10)
                glEnd()
                glDisable(GL_TEXTURE_2D)
            self.Square2DSingle(-12.25, 3.2, -10, 1, 4, color[0])
            clr_slc = color_switch
            if self.int and self.LP_Mdl_Slc==0:
                Mdl_TexOn = self.MdlH_TexOn[self.LP_intMdl_Slc]
                Mdl_Alpha = self.MdlH_Alpha[self.LP_intMdl_Slc]
            else:
                Mdl_TexOn = self.Mdl_TexOn[self.LP_Mdl_Slc]
                Mdl_Alpha = self.Mdl_Alpha[self.LP_Mdl_Slc]
            if Mdl_TexOn ==-1:
                clr_slc = color
            self.Square2DMulti(-11.15, 3.2, -10, 1, 4, 0.15, clr_slc, 1, True, Mdl_TexOn)
            self.Square2DSingle(-12.25, 3.2, -10, 1, Mdl_Alpha*4,(0.2157, 0.2985, 0.4858))
            if Mdl_TexOn==0:
                self.DisplayText("O", (219, 437), (1, 1, 1), 2)
                self.DisplayText("F", (221, 412), (1, 1, 1), 2)
                self.DisplayText("F", (221, 387), (1, 1, 1), 2)
            elif Mdl_TexOn==1:
                self.DisplayText("O", (219, 425), (1, 1, 1), 2)
                self.DisplayText("N", (220, 400), (1, 1, 1), 2)
            else:
                self.DisplayText("N", (219, 430), (1, 1, 1), 2)
                self.DisplayText("/", (223, 413), (1, 1, 1), 2)
                self.DisplayText("A", (220, 395), (1, 1, 1), 2)
            self.DisplayText("A", (178, 462), (1, 1, 1), 2)
            self.DisplayText("L", (180, 437), (1, 1, 1), 2)
            self.DisplayText("P", (179, 412), (1, 1, 1), 2)
            self.DisplayText("H", (178, 387), (1, 1, 1), 2)
            self.DisplayText("A", (178, 362), (1, 1, 1), 2)
        elif self.RP_Slc == 8:
            self.DisplayText("LIGHTING", (83, 509), (1, 1, 1), 2)
            self.Square2DMulti(-16.5, 3.25, -10, 3.2, 0.4, 0.65, color, 4, True, int(self.Light_Set/10))    #Title
            self.Square2DMulti(-16.5, 2.8, -10, 3.2, 0.5, 0, color, 1, True, self.Light_Set)     #Shine
            self.Square2DMulti(-16.5, 1.75, -10, 0.7775, 0.5, 0.03, color, 4, False, self.Light_Set-10)
            self.Square2DMulti(-16.5, 0.7, -10, 0.7775, 0.5, 0.03, color, 4, False, self.Light_Set - 20)
            self.Square2DMulti(-16.5, -0.35, -10, 157/150, 0.5, 0.03, color, 3, False, self.Light_Set-30)  #Pos
            self.Square2DMulti(-13.2, 3.25, -10, 3.2, 0.4, 0.65, color, 3, True, int(self.Light_Set/10)-4)  #Title
            self.Square2DMulti(-13.2, 2.8, -10, 0.7775, 0.5, 0.03, color, 4, False, self.Light_Set - 40)
            self.Square2DMulti(-13.2, 1.75, -10, 0.7775, 0.5, 0.03, color, 4, False, self.Light_Set - 50)
            self.Square2DMulti(-13.2, 0.7, -10, 0.7775, 0.5, 0.03, color, 4, False, self.Light_Set - 60)
            self.Square2DSingle(-16.5, 2.8, -10, 3.2*self.Light_Props[0]/128, 0.5,(0.9, 0.2985, 0.4858))  # Shine
            for k in range(1,3):
                for i in range(4):
                    Props = self.Light_Props[k]
                    self.Square2DSingle(-16.5+(0.7775+0.03)*i, 1.75-(0.5+0.55)*(k-1), -10, 0.7775 * Props[i], 0.5, (0.9, 0.2985, 0.4858))
            Pos = self.Light_Props[3]
            Display = [str(Pos[0]), str(Pos[1]), str(Pos[2])]
            if 30 <= self.Light_Set <= 33:
                Display[self.Light_Set - 30] = self.Data_New
            for i in range(3):
                if len(Display[i]) > 5:
                    Display[i] = Display[i][:(5 - len(Display[i]))]
            self.DisplayText(Display[0], (6, 348), (1, 1, 1), 3)
            self.DisplayText(Display[1], (48, 348), (1, 1, 1), 3)
            self.DisplayText(Display[2], (88, 348), (1, 1, 1), 3)
            for k in range(4,7):
                for i in range(4):
                    Props = self.Light_Props[k]
                    self.Square2DSingle(-13.2+(0.7775+0.03)*i, 2.8-(0.5+0.55)*(k-4), -10, 0.7775 * Props[i], 0.5, (0.9, 0.2985, 0.4858))
            self.Square2DMulti(-13.2, 0.1, -10, 3.2, 0.95, 0.1, color_switch, 1, True, self.Light_Props[7])
            self.DisplayText("Shininess", (38, 487), (1, 1, 1), 3)
            self.DisplayText("Diffuse", (170, 487), (1, 1, 1), 3)
            self.DisplayText("Mat_Specular", (28, 448), (1, 1, 1), 3)
            self.DisplayText("Specular", (164, 448), (1, 1, 1), 3)
            self.DisplayText("Mdl_Ambient", (28, 408), (1, 1, 1), 3)
            self.DisplayText("Ambient", (165, 408), (1, 1, 1), 3)
            self.DisplayText("Position", (43, 369), (1, 1, 1), 3)
            if self.Light_Props[7]==0:
                self.DisplayText("Off", (173, 355), (1, 1, 1), 2)
            else:
                self.DisplayText("On", (175, 355), (1, 1, 1), 2)
        elif self.RP_Slc == 9:
            self.DisplayText("RENDER", (90, 509), (1, 1, 1), 2)
            if self.Ba_Slc==18:
                slc = 1
            else:
                slc = 0
            self.Square2DMulti(-16.5, 3.25, -10, 0.7, 4.1, 0, color_switch, 1, True, slc)     #Crop
            self.Square2DSingle(-15.78, 3.25, -10, 0.7, 4.1, (0.2157, 0.2985, 0.4858))  #Save
            slc = -1
            if 0<=self.Ba_Slc<=7 or self.Ba_Slc==16:
                slc = 0
            elif 8<=self.Ba_Slc<=15 or self.Ba_Slc==17:
                slc = 1
            self.Square2DMulti(-15, 3.25, -10, 1.75, 0.4, 0, color, 1, True, slc)    #Back
            self.Square2DMulti(-15, 2.8, -10, 0.5, 1.55, 0, color_switch, 1, True, self.Back[0])
            self.Square2DSingle(-14.45, 2.8, -10, 1.2, 1.1,(0.2157, 0.2985, 0.4858))
            self.Square2DMulti(-14.45, 1.65, -10, 1.2, 0.4, 0, color_switch, 1, True, self.Back[2])
            self.Square2DMulti(-15, 1.15, -10, 1.75, 0.4, 0, color, 1, True, slc-1)   #Base
            self.Square2DMulti(-15, 0.7, -10, 0.5, 1.55, 0, color_switch, 1, True, self.Base[0])
            self.Square2DSingle(-14.45, 0.7, -10, 1.2, 1.1, (0.2157, 0.2985, 0.4858))
            self.Square2DMulti(-14.45, -0.45, -10, 1.2, 0.4, 0, color_switch, 1, True, self.Base[2])
            slc = -1
            if 0<=self.Ba_Slc<=3:
                slc = 0
            elif 4<=self.Ba_Slc<=7:
                slc = 1
            elif 8<=self.Ba_Slc<=11:
                slc = 2
            elif 12<=self.Ba_Slc<=15:
                slc = 3
            self.Square2DMulti(-13.2, 3.25, -10, 3.2, 0.4, 0.65, color, 4, True, slc)     #title
            self.Square2DMulti(-13.2, 2.8, -10, 0.7775, 0.5, 0.03, color, 4, False, self.Ba_Slc)  #pos
            self.Square2DMulti(-13.2, 1.75, -10, 0.7775, 0.5, 0.03, color, 4, False, self.Ba_Slc-4) #rgb
            self.Square2DMulti(-13.2, 0.7, -10, 0.7775, 0.5, 0.03, color, 4, False,  self.Ba_Slc-8)  #pos
            self.Square2DMulti(-13.2, -0.35, -10, 0.7775, 0.5, 0.03, color, 4, False, self.Ba_Slc-12)    #rgb
            for k in range(2):
                if k==0:
                    clr = self.Back[4]
                else:
                    clr = self.Base[4]
                for i in range(3):
                    self.Square2DSingle(-13.2+(0.7775+0.03)*i, 1.75-2.1*k, -10, 0.7775*clr[i]/255, 0.5, (0.9, 0.2985, 0.4858))  # rgb
            glColor3f(1,1,1)
            glLineWidth(3)
            if not self.Back[1]:
                glBegin(GL_LINES)
                glVertex3f(-13.85, 2.5, -10)
                glVertex3f(-13.85, 2, -10)
                glVertex3f(-14.1, 2.25, -10)
                glVertex3f(-13.6, 2.25, -10)
                glEnd()
            if not self.Base[1]:
                glBegin(GL_LINES)
                glVertex3f(-13.85, 0.4, -10)
                glVertex3f(-13.85, -0.1, -10)
                glVertex3f(-14.1, 0.15, -10)
                glVertex3f(-13.6, 0.15, -10)
                glEnd()
            glBegin(GL_TRIANGLES)
            glVertex3f(-10.35,2.72,-10)
            glVertex3f(-10.05, 2.58, -10)
            glVertex3f(-10.65, 2.58, -10)
            glVertex3f(-10.35, 2.38, -10)
            glVertex3f(-10.62, 2.52, -10)
            glVertex3f(-10.07, 2.52, -10)
            glVertex3f(-10.35, 0.62, -10)
            glVertex3f(-10.05, 0.47, -10)
            glVertex3f(-10.65, 0.47, -10)
            glVertex3f(-10.07, 0.43, -10)
            glVertex3f(-10.35, 0.28, -10)
            glVertex3f(-10.65, 0.43, -10)
            glEnd()
            glPointSize(15)
            glBegin(GL_POINTS)
            clr = self.Back[4]
            glColor3ub(clr[0], clr[1], clr[2])
            glVertex3f(-10.4,1.5,-10)
            clr = self.Base[4]
            glColor3ub(clr[0], clr[1], clr[2])
            glVertex3f(-10.4, -0.6, -10)
            glEnd()
            if self.Back[1]:
                self.loadTexture('ext/'+self.Back[1])
                glBegin(GL_QUADS)
                glTexCoord2f(0,1)
                glVertex3f(-14.35,2.7,-10)
                glTexCoord2f(1, 1)
                glVertex3f(-13.35,2.7,-10)
                glTexCoord2f(1, 0)
                glVertex3f(-13.35, 1.8, -10)
                glTexCoord2f(0, 0)
                glVertex3f(-14.35, 1.8, -10)
                glEnd()
                glDisable(GL_TEXTURE_2D)
            if self.Base[1]:
                self.loadTexture('ext/'+self.Base[1])
                glBegin(GL_QUADS)
                glTexCoord2f(0,1)
                glVertex3f(-14.35,0.6,-10)
                glTexCoord2f(1, 1)
                glVertex3f(-13.35,0.6,-10)
                glTexCoord2f(1, 0)
                glVertex3f(-13.35, -0.3, -10)
                glTexCoord2f(0, 0)
                glVertex3f(-14.35, -0.3, -10)
                glEnd()
                glDisable(GL_TEXTURE_2D)
            self.DisplayText("C", (11, 446), (1, 1, 1), 2)
            self.DisplayText("R", (12, 423), (1, 1, 1), 2)
            self.DisplayText("O", (10, 399), (1, 1, 1), 2)
            self.DisplayText("P", (12, 376), (1, 1, 1), 2)
            self.DisplayText("S", (40, 446), (1, 1, 1), 2)
            self.DisplayText("A", (40, 423), (1, 1, 1), 2)
            self.DisplayText("V", (39, 399), (1, 1, 1), 2)
            self.DisplayText("E", (41, 376), (1, 1, 1), 2)
            self.DisplayText("BACK", (78, 485), (1, 1, 1), 3)
            if self.Back[0]==0:
                self.DisplayText("O", (67, 460), (1, 1, 1), 3)
                self.DisplayText("F", (68, 445), (1, 1, 1), 3)
                self.DisplayText("F", (68, 430), (1, 1, 1), 3)
            elif self.Back[0]==1:
                self.DisplayText("O", (67, 453), (1, 1, 1), 3)
                self.DisplayText("N", (67, 438), (1, 1, 1), 3)
            if self.Back[2]==0:
                self.DisplayText("O", (92, 425), (1, 1, 1), 3)
                self.DisplayText("F", (103, 425), (1, 1, 1), 3)
                self.DisplayText("F", (112, 425), (1, 1, 1), 3)
            elif self.Back[2]==1:
                self.DisplayText("O", (95, 425), (1, 1, 1), 3)
                self.DisplayText("N", (105, 425), (1, 1, 1), 3)

            self.DisplayText("BASE", (78, 406), (1, 1, 1), 3)
            if self.Base[0] == 0:
                self.DisplayText("O", (67, 382), (1, 1, 1), 3)
                self.DisplayText("F", (68, 367), (1, 1, 1), 3)
                self.DisplayText("F", (68, 352), (1, 1, 1), 3)
            elif self.Base[0] == 1:
                self.DisplayText("O", (67, 375), (1, 1, 1), 3)
                self.DisplayText("N", (67, 360), (1, 1, 1), 3)
            if self.Base[2] == 0:
                self.DisplayText("O", (92, 346), (1, 1, 1), 3)
                self.DisplayText("F", (103, 346), (1, 1, 1), 3)
                self.DisplayText("F", (112, 346), (1, 1, 1), 3)
            elif self.Base[2] == 1:
                self.DisplayText("O", (95, 346), (1, 1, 1), 3)
                self.DisplayText("N", (105, 346), (1, 1, 1), 3)

            self.DisplayText("Position (L,H,Y)", (145, 485), (1, 1, 1), 3)
            self.DisplayText("Colour", (172, 446), (1, 1, 1), 3)
            self.DisplayText("Position (L,W,Y)", (145, 406), (1, 1, 1), 3)
            self.DisplayText("Colour", (172, 367), (1, 1, 1), 3)

            pos = self.Back[3]
            display = [str(pos[0]), str(pos[1]), str(pos[2])]
            if 0<=self.Ba_Slc<=2:
                display[self.Ba_Slc] = self.Data_New
            self.DisplayText(display[0], (131, 466), (1, 1, 1), 3)
            self.DisplayText(display[1], (161, 466), (1, 1, 1), 3)
            self.DisplayText(display[2], (192, 466), (1, 1, 1), 3)
            pos = self.Base[3]
            display = [str(pos[0]), str(pos[1]), str(pos[2])]
            if 8<=self.Ba_Slc<=10:
                display[self.Ba_Slc-8] = self.Data_New
            self.DisplayText(display[0], (131, 387), (1, 1, 1), 3)
            self.DisplayText(display[1], (161, 387), (1, 1, 1), 3)
            self.DisplayText(display[2], (192, 387), (1, 1, 1), 3)
        else:
            self.DisplayText("TOOL", (101, 509), (1, 1, 1), 2)
            self.DisplayText("Select TOOL from", (48, 460), (1, 1, 1), 2)
            self.DisplayText("RIGHT PANEL /", (60, 435), (1, 1, 1), 2)
            self.DisplayText("HOTKEYS", (78, 410), (1, 1, 1), 2)
            self.DisplayText("<<<EDIT TOOL HERE>>>", (20, 360), (1, 1, 1), 2)
        self.Square2DSingle(-16.5, -1, -10, 6.5, 0.6, (0.188 - 0.1, 0.835 - 0.1, 0.784 - 0.1))
        self.DisplayText("RESET", (95, 319), (1, 1, 1), 2)

    def LeftPanel(self):
        self.Model_Panel()
        self.Detail()
        self.Hierarchy_Panel()

    def Model_Panel(self):
        self.Square2DSingle(-16.5, 9.9, -10, 6.5, 5.58, (0.4265, 0.4265, 0.4265))
        self.Square2DSingle(-16.5, 4.32, -10, 6.5, 6, (131 / 255, 148 / 255, 161 / 255))
        self.Square2DSingle(-16.5, 9.9, -10, 6.5, 1, (42 / 255, 42 / 255, 42 / 255))
        color = [42 / 255, 42 / 255, 42 / 255], [1, 204 / 255, 0]
        color_del = [42 / 255, 42 / 255, 42 / 255], [238 / 255, 62 / 255, 64 / 255]
        self.Square2DMulti(-16.5, 8.8, -10, 5.5, 0.8, 0.1, color, self.Mdl_list, True, self.LP_Mdl_Slc)
        self.Square2DMulti(-10.8, 8.8, -10, 0.8, 0.8, 0.1, color_del, self.Mdl_list, True, self.LP_Mdl_Del)
        # Add btn
        if self.Mdl_list < 5:
            Xo, Yo, Zo, w, h, d = -16.5, 8.8, -10, 0.5, 0.5, 0.15
            Y = Yo - (1.2 * h + 2 * d) * self.Mdl_list
            self.Square2DSingle(Xo, Y, Zo, 6.5, 0.8, (0.2157, 0.2985, 0.4858))
            if not self.Mdl_Add:
                glLineWidth(3)
                glColor3f(1, 1, 1)
                glBegin(GL_LINES)
                glVertex3f(Xo + w * 6.5, Y - d, Zo)
                glVertex3f(Xo + w * 6.5, Y - h - d, Zo)
                glVertex3f(Xo + w * 6, Y - h / 2 - d, Zo)
                glVertex3f(Xo + w * 7, Y - h / 2 - d, Zo)
                glEnd()
            else:
                if self.Mdl_list == 0:
                    self.DisplayText("Loading ...", (10, 682), (1, 1, 1), 2)
                elif self.Mdl_list == 1:
                    self.DisplayText("Loading ...", (10, 649), (1, 1, 1), 2)
                elif self.Mdl_list == 2:
                    self.DisplayText("Loading ...", (10, 616), (1, 1, 1), 2)
                elif self.Mdl_list == 3:
                    self.DisplayText("Loading ...", (10, 582), (1, 1, 1), 2)
                elif self.Mdl_list == 4:
                    self.DisplayText("Loading ...", (10, 548), (1, 1, 1), 2)
        # Cross Symbol
        Xo, Yo, Zo, w, h, d = -10.6, 8.6, -10, 0.4, 0.4, 0.1
        glLineWidth(3)
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        for i in range(self.Mdl_list):
            glVertex3f(Xo, Yo - h * 2 * i - d * i, Zo)
            glVertex3f(Xo + w, Yo - h * (i + 1) - h * i - d * i, Zo)
            glVertex3f(Xo + w, Yo - h * 2 * i - d * i, Zo)
            glVertex3f(Xo, Yo - h * (i + 1) - h * i - d * i, Zo)
        glEnd()
        self.DisplayText("MODEL", (80, 720), (1, 1, 1), 1)
        y = [682, 649, 616, 582, 548]
        for i in range(self.Mdl_list):
            mdl = self.Mdl[i]
            mdl = mdl[:-4]
            if len(mdl) > 18:
                mdl = mdl[:(18 - len(mdl))]
            self.DisplayText(mdl, (10, y[i]), (1, 1, 1), 2)

    def Hierarchy_Panel(self):
        color = [42 / 255, 42 / 255, 42 / 255], [1, 204 / 255, 0]
        if self.LP_Mdl_Slc==0 and self.int:
            display = []
            self.Square2DSingle(-16.5, -1.7, -10, 6.5, 0.8, (48/255, 48/255, 48/255))
            self.Square2DMulti(-16.5, -2.55, -10, 2.1, 0.5, 0.1, color, 3, False, self.LP_Hrc_Slc) #H1,H2,H3
            if self.LP_Hrc_Slc == 0:
                self.Square2DMulti(-16.5, -3.15, -10, 6.5, 0.8, 0.05, color, 1, True, self.LP_Hrc_Slc)
                self.DisplayText("Predator_Complete", (7.5, 236), (1, 1, 1), 2)
            elif self.LP_Hrc_Slc==1:
                self.Square2DMulti(-16.5, -3.1, -10, 3.225, 0.65, 0.05, color, 10, True, self.LP_intMdl_Slc)
                self.Square2DMulti(-13.225, -3.1, -10, 3.225, 0.65, 0.05, color, 9, True, self.LP_intMdl_Slc-10)
                for i in range(19):
                    display.append(self.MdlH[i])
                    display[i] = display[i][:-4]
                    if len(display[i])>11:
                        display[i] = display[i][:(11-len(display[i]))]
                self.DisplayText(display[0], (7.5, 240), (1, 1, 1), 2)
                self.DisplayText(display[1], (7.5, 213), (1, 1, 1), 2)
                self.DisplayText(display[2], (7.5, 187), (1, 1, 1), 2)
                self.DisplayText(display[3], (7.5, 161), (1, 1, 1), 2)
                self.DisplayText(display[4], (7.5, 134), (1, 1, 1), 2)
                self.DisplayText(display[5], (7.5, 109), (1, 1, 1), 2)
                self.DisplayText(display[6], (7.5, 82), (1, 1, 1), 2)
                self.DisplayText(display[7], (7.5, 57), (1, 1, 1), 2)
                self.DisplayText(display[8], (7.5, 30), (1, 1, 1), 2)
                self.DisplayText(display[9], (7.5, 3), (1, 1, 1), 2)
                self.DisplayText(display[10], (131, 240), (1, 1, 1), 2)
                self.DisplayText(display[11], (131, 213), (1, 1, 1), 2)
                self.DisplayText(display[12], (131, 187), (1, 1, 1), 2)
                self.DisplayText(display[13], (131, 161), (1, 1, 1), 2)
                self.DisplayText(display[14], (131, 134), (1, 1, 1), 2)
                self.DisplayText(display[15], (131, 109), (1, 1, 1), 2)
                self.DisplayText(display[16], (131, 82), (1, 1, 1), 2)
                self.DisplayText(display[17], (131, 57), (1, 1, 1), 2)
                self.DisplayText(display[18], (131, 30), (1, 1, 1), 2)
            elif self.LP_Hrc_Slc==2:
                self.Square2DMulti(-16.5, -3.15, -10, 6.5, 0.8, 0.05, color, 7, True, self.LP_intMdl_Slc-19)
                for i in range(19, 26):
                    display.append(self.MdlH[i])
                    display[i-19] = display[i-19][:-4]
                    if len(display[i-19])>25:
                        display[i-19] = display[i-19][:(25-len(display[i-19]))]
                self.DisplayText(display[0], (7.5, 236), (1, 1, 1), 2)
                self.DisplayText(display[1], (7.5, 204), (1, 1, 1), 2)
                self.DisplayText(display[2], (7.5, 172), (1, 1, 1), 2)
                self.DisplayText(display[3], (7.5, 140), (1, 1, 1), 2)
                self.DisplayText(display[4], (7.5, 108), (1, 1, 1), 2)
                self.DisplayText(display[5], (7.5, 77), (1, 1, 1), 2)
                self.DisplayText(display[6], (7.5, 45), (1, 1, 1), 2)
            self.DisplayText("HIERARCHY", (60, 288), (1, 1, 1), 1)
            self.DisplayText("1", (39, 263), (1, 1, 1), 2)
            self.DisplayText("2", (124, 263), (1, 1, 1), 2)
            self.DisplayText("3", (205, 263), (1, 1, 1), 2)

    def DisplayText(self, text, pos, color, font):
        glColor3fv(color)
        glWindowPos2fv(pos)
        if font == 1:
            font = GLUT_BITMAP_TIMES_ROMAN_24
        elif font == 2:
            font = GLUT_BITMAP_HELVETICA_18
        elif font == 3:
            font = GLUT_BITMAP_HELVETICA_12
        elif font == 4:
            font = GLUT_BITMAP_HELVETICA_10
        for ch in text:
            glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

    def Square2DMulti(self, Xo, Yo, Zo, w, h, d, color, n, RC, Slc): #Row: True #Column: False
        for i in range(n):
            if Slc == i:
                glColor3fv(color[1])
            else:
                glColor3fv(color[0])
            if RC:
                X = Xo
                Y = Yo-h*i-d*i
            else:
                X = Xo+w*i+d*i
                Y = Yo
            Vtx = [(X, Y, Zo), (X + w, Y, Zo), (X + w, Y - h, Zo), (X, Y - h, Zo)]
            glBegin(GL_QUADS)
            for vtx in Vtx:
                glVertex3fv(vtx)
            glEnd()

    def Square2DSingle(self, Xo, Yo, Zo, w, h, color):
        Vtx = [(Xo, Yo, Zo), (Xo + w, Yo, Zo), (Xo + w, Yo - h, Zo), (Xo, Yo - h, Zo)]
        glColor3fv(color)
        glBegin(GL_QUADS)
        for vtx in Vtx:
            glVertex3fv(vtx)
        glEnd()

    def Cursor_3D(self, rx, ry):
        if self.cursor_3D==1:
            r = 10000000
            glPushMatrix()
            glTranslate(self.cursor_3D_pos[0], self.cursor_3D_pos[1], self.cursor_3D_pos[2]-20)
            glBegin(GL_LINE_LOOP)
            for i in range(180):
                if 0<=i<18 or 36<=i<54 or 72<=i<90 or 108<=i<126 or 144<=i<162:
                    glColor3f(1, 1, 1)
                else:
                    glColor3f(1,0,0)
                X = r / 5000000 * math.cos(math.radians(i * 2))
                Y = r / 5000000 * math.sin(math.radians(i * 2))
                glVertex3f(X, Y, 0)
            glEnd()
            glRotate(ry, 1, 0, 0)
            glRotate(rx, 0, 1, 0)
            glLineWidth(0.5)
            glBegin(GL_LINES)
            glColor3f(1,0,0)
            glVertex3f(-r, 0, 0)
            glVertex3f(r, 0, 0)
            glColor3f(0, 1, 0)
            glVertex3f(0, r, 0)
            glVertex3f(0, -r, 0)
            glColor3f(0, 0, 1)
            glVertex3f(0, 0, -r)
            glVertex3f(0, 0, r)
            glEnd()
            glPopMatrix()

    def loadTexture(self, image):
        textureSurface = pygame.image.load(image)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
        if self.RP_Slc==7:
            glColor4f(1, 1, 1, self.Mdl_Alpha[self.LP_Mdl_Slc])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    def Lighting_SetUp(self):
        if self.Light_Props[7] == 1:
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.Light_Props[1])
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, self.Light_Props[0])
            glLightfv(GL_LIGHT0, GL_AMBIENT, self.Light_Props[6])
            glLightfv(GL_LIGHT0, GL_DIFFUSE, self.Light_Props[4])
            glLightfv(GL_LIGHT0, GL_SPECULAR, self.Light_Props[5])
            glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.Light_Props[2])
            glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_FALSE)
            glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHT1)
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_NORMALIZE)
            glLightfv(GL_LIGHT0, GL_POSITION, self.Light_Props[3])

    def Music_play(self):
        pygame.mixer.music.load('ext/'+self.BGM)
        pygame.mixer.music.play(-1)

    def ImageSave(self):
        if self.image[2]:
            pos = self.image[0]
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(pos[0], pos[1], pos[2], pos[3], GL_RGBA, GL_UNSIGNED_BYTE)
            image = Image.frombytes("RGBA", (pos[2], pos[3]), data)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image.save(self.image[1]+'.png', 'PNG')
            self.image[2] = False
            self.image[3] = True
        if self.image[3]:
            glBegin(GL_QUADS)
            glColor3f(42 / 255, 42 / 255, 42 / 255)
            glVertex3f(-4.7, -9.9, -10)
            glVertex3f(4.7, -9.9, -10)
            glVertex3f(4.7, -8.8, -10)
            glVertex3f(-4.7, -8.8, -10)
            glColor3f(0.2157, 0.2985, 0.4858)
            glVertex3f(-4.5, -9.7, -10)
            glVertex3f(4.5, -9.7, -10)
            glVertex3f(4.5, -9, -10)
            glVertex3f(-4.5, -9, -10)
            glEnd()
            self.DisplayText('Image is saved successfully ...', (500, 18), (1, 1, 1), 2)

    def Background(self, ty):
        if self.Back[0]==1:
            pos = self.Back[3]
            clr = self.Back[4]
            if self.Ba_Slc==3:
                pos[2] += int(ty / 10)
                if pos[2] > 999:
                    pos[2] = 999
                elif pos[2] < -999:
                    pos[2] = -999
            glColor3ub(clr[0], clr[1], clr[2])
            if self.Back[1] and self.Back[2]==1:
                self.loadTexture('ext/'+self.Back[1])
            glBegin(GL_QUADS)
            if self.Back[1] and self.Back[2]==1:
                glTexCoord2f(0,1)
                glVertex(-pos[0], pos[2] + pos[1], -pos[2])
                glTexCoord2f(1, 1)
                glVertex(pos[0], pos[2] + pos[1], -pos[2])
                glTexCoord2f(1, 0)
                glVertex(pos[0], pos[2] - pos[1], -pos[2])
                glTexCoord2f(0, 0)
                glVertex(-pos[0], pos[2] - pos[1], -pos[2])
            else:
                glVertex(-pos[0], pos[2]+pos[1], -pos[2])
                glVertex(pos[0], pos[2]+pos[1], -pos[2])
                glVertex(pos[0], pos[2]-pos[1], -pos[2])
                glVertex(-pos[0], pos[2]-pos[1], -pos[2])
            glEnd()
            glDisable(GL_TEXTURE_2D)
        if self.Base[0]==1:
            pos = self.Base[3]
            clr = self.Base[4]
            if self.Ba_Slc==11:
                pos[2] += int(ty / 10)
                if pos[2] > 999:
                    pos[2] = 999
                elif pos[2] < -999:
                    pos[2] = -999
            glColor3ub(clr[0], clr[1], clr[2])
            if self.Base[1] and self.Base[2]==1:
                self.loadTexture('ext/'+self.Base[1])
            glBegin(GL_QUADS)
            if self.Base[1] and self.Base[2]==1:
                glTexCoord2f(0, 1)
                glVertex(-pos[0], pos[2], -pos[1])
                glTexCoord2f(1, 1)
                glVertex(pos[0], pos[2], -pos[1])
                glTexCoord2f(1, 0)
                glVertex(pos[0], pos[2], pos[1])
                glTexCoord2f(0, 0)
                glVertex(-pos[0], pos[2], pos[1])
            else:
                glVertex(-pos[0], pos[2], -pos[1])
                glVertex(pos[0], pos[2], -pos[1])
                glVertex(pos[0], pos[2], pos[1])
                glVertex(-pos[0], pos[2], pos[1])
            glEnd()
            glDisable(GL_TEXTURE_2D)