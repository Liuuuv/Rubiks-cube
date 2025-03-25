# From the rotating cube code :
# GitHub:
# https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_3D.md
#
# Stack Overflow:
# https://stackoverflow.com/questions/56285017/pygame-rotating-cubes-around-axis/56286203#56286203

import math
import pygame
import numpy as np

TURN_SPEED = 10

def project(vector, w, h, fov, distance):
    factor = math.atan(fov / 2 * math.pi / 180) / (distance + vector.z)
    x = vector.x * factor * w + w / 2
    y = -vector.y * factor * w + h / 2
    return pygame.math.Vector3(x, y, vector.z)

def rotate_vertices(vertices, angle, axis):
    return [v.rotate(angle, axis) for v in vertices]
def scale_vertices(vertices, s):
    return [pygame.math.Vector3(v[0]*s[0], v[1]*s[1], v[2]*s[2]) for v in vertices]
def translate_vertices(vertices, t):
    return [v + pygame.math.Vector3(t) for v in vertices]
def project_vertices(vertices, w, h, fov, distance):
    return [project(v, w, h, fov, distance) for v in vertices]

class Mesh():

    def __init__(self, vertices, faces, faces_color):
        self.__vertices = [pygame.math.Vector3(v) for v in vertices]
        self.__faces = faces
        self.__faces_color = faces_color

    def rotate(self, angle, axis):
        self.__vertices = rotate_vertices(self.__vertices, angle, axis)
    def scale(self, s):
        self.__vertices = scale_vertices(self.__vertices, s)
    def translate(self, t):
        self.__vertices = translate_vertices(self.__vertices, t)

    def calculate_average_z(self, vertices):
        return [(i, sum([vertices[j].z for j in f]) / len(f)) for i, f in enumerate(self.__faces)]

    def get_face(self, index):
        return self.__faces[index]
    def get_vertices(self):
        return self.__vertices
    def get_face_color(self, index):
        return self.__faces_color[index]

    def create_polygon(self, face, vertices):
        return [(vertices[i].x, vertices[i].y) for i in [*face, face[0]]]
       
class Scene:
    def __init__(self, meshes, rubikscube, fov, distance):
        self.meshes = meshes
        self.rubikscube = rubikscube
        self.fov = fov
        self.distance = distance 
        self.euler_angles = [0, 0, 0]

    def transform_vertices(self, vertices, width, height):
        transformed_vertices = vertices
        axis_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        for angle, axis in reversed(list(zip(list(self.euler_angles), axis_list))):
            transformed_vertices = rotate_vertices(transformed_vertices, angle, axis)
        transformed_vertices = project_vertices(transformed_vertices, width, height, self.fov, self.distance)
        return transformed_vertices

    def draw(self, surface):
        
        polygons = []
        for mesh in self.meshes:
            transformed_vertices = self.transform_vertices(mesh.get_vertices(), *surface.get_size())
            avg_z = mesh.calculate_average_z(transformed_vertices)
            for z in avg_z:
            #for z in sorted(avg_z, key=lambda x: x[1], reverse=True):
                pointlist = mesh.create_polygon(mesh.get_face(z[0]), transformed_vertices)
                polygons.append((pointlist, z[1], mesh.get_face_color(z[0])))
                #pygame.draw.polygon(surface, (128, 128, 192), pointlist)
                #pygame.draw.polygon(surface, (0, 0, 0), pointlist, 3)

        for poly in sorted(polygons, key=lambda x: x[1], reverse=True):
            # pygame.draw.polygon(surface, (128, 128, 192), poly[0])
            pygame.draw.polygon(surface, poly[2], poly[0])
            pygame.draw.polygon(surface, (0, 0, 0), poly[0], 3)

class RubiksCube:
    def __init__(self, corner_list, algorithm):
        self.corner_list = corner_list
        self.is_turning = False
        self.current_movement = ""
        self.turn_count = 0
        self.MAX_TURN_COUNT = int(90 / TURN_SPEED)
        
        self.algorithm = algorithm
        self.index_algorithm = 0
        self.is_doing_algorithm = False
    
    def r_movement(self):
        if self.is_turning:
            return
        self.current_movement = "R"
        self.is_turning = True
        self.corner_list[1], self.corner_list[2], self.corner_list[6], self.corner_list[7] = self.corner_list[6], self.corner_list[1], self.corner_list[7], self.corner_list[2]
    def rp_movement(self):
        if self.is_turning:
            return
        self.current_movement = "R'"
        self.is_turning = True
        for _ in range(3):
            self.corner_list[1], self.corner_list[2], self.corner_list[6], self.corner_list[7] = self.corner_list[6], self.corner_list[1], self.corner_list[7], self.corner_list[2]

    def u_movement(self):
        if self.is_turning:
            return
        self.current_movement = "U"
        self.is_turning = True
        self.corner_list[0], self.corner_list[1], self.corner_list[2], self.corner_list[3] = self.corner_list[1], self.corner_list[2], self.corner_list[3], self.corner_list[0]
    def up_movement(self):
        if self.is_turning:
            return
        self.current_movement = "U'"
        self.is_turning = True
        for _ in range(3):
            self.corner_list[0], self.corner_list[1], self.corner_list[2], self.corner_list[3] = self.corner_list[1], self.corner_list[2], self.corner_list[3], self.corner_list[0]
    
    def f_movement(self):
        if self.is_turning:
            return
        self.current_movement = "F"
        self.is_turning = True
        self.corner_list[0], self.corner_list[1], self.corner_list[5], self.corner_list[6] = self.corner_list[5], self.corner_list[0], self.corner_list[6], self.corner_list[1]
    def fp_movement(self):
        if self.is_turning:
            return
        self.current_movement = "F'"
        self.is_turning = True
        for _ in range(3):
            self.corner_list[0], self.corner_list[1], self.corner_list[5], self.corner_list[6] = self.corner_list[5], self.corner_list[0], self.corner_list[6], self.corner_list[1]
    
    def d_movement(self):
        if self.is_turning:
            return
        self.current_movement = "D"
        self.is_turning = True
        self.corner_list[4], self.corner_list[5], self.corner_list[6], self.corner_list[7] = self.corner_list[7], self.corner_list[4], self.corner_list[5], self.corner_list[6]
    def dp_movement(self):
        if self.is_turning:
            return
        self.current_movement = "D'"
        self.is_turning = True
        for _ in range(3):
            self.corner_list[4], self.corner_list[5], self.corner_list[6], self.corner_list[7] = self.corner_list[7], self.corner_list[4], self.corner_list[5], self.corner_list[6]
    
    def b_movement(self):
        if self.is_turning:
            return
        self.current_movement = "B"
        self.is_turning = True
        self.corner_list[2], self.corner_list[3], self.corner_list[4], self.corner_list[7] = self.corner_list[7], self.corner_list[2], self.corner_list[3], self.corner_list[4]
    def bp_movement(self):
        if self.is_turning:
            return
        self.current_movement = "B'"
        self.is_turning = True
        for _ in range(3):
            self.corner_list[2], self.corner_list[3], self.corner_list[4], self.corner_list[7] = self.corner_list[7], self.corner_list[2], self.corner_list[3], self.corner_list[4]
    
    def l_movement(self):
        if self.is_turning:
            return
        self.current_movement = "L"
        self.is_turning = True
        self.corner_list[0], self.corner_list[3], self.corner_list[4], self.corner_list[5] = self.corner_list[3], self.corner_list[4], self.corner_list[5], self.corner_list[0]
    def lp_movement(self):
        if self.is_turning:
            return
        self.current_movement = "L'"
        self.is_turning = True
        for _ in range(3):
            self.corner_list[0], self.corner_list[3], self.corner_list[4], self.corner_list[5] = self.corner_list[3], self.corner_list[4], self.corner_list[5], self.corner_list[0]
    
    def update(self):
        if self.is_turning:
            self.turn_count += 1
            if self.turn_count >= self.MAX_TURN_COUNT:
                self.is_turning = False
                self.turn_count = 0
            if self.current_movement == "R":
                for index in [1,2,6,7]:
                    self.corner_list[index].rotate(TURN_SPEED,(1,0,0))
            if self.current_movement == "R'":
                for index in [1,2,6,7]:
                    self.corner_list[index].rotate(-TURN_SPEED,(1,0,0))
            
            if self.current_movement == "U":
                for index in [0,1,2,3]:
                    self.corner_list[index].rotate(TURN_SPEED,(0,1,0))
            if self.current_movement == "U'":
                for index in [0,1,2,3]:
                    self.corner_list[index].rotate(-TURN_SPEED,(0,1,0))
            
            if self.current_movement == "F":
                for index in [0,1,5,6]:
                    self.corner_list[index].rotate(TURN_SPEED,(0,0,-1))
            if self.current_movement == "F'":
                for index in [0,1,5,6]:
                    self.corner_list[index].rotate(-TURN_SPEED,(0,0,-1))
            
            if self.current_movement == "D":
                for index in [4,5,6,7]:
                    self.corner_list[index].rotate(TURN_SPEED,(0,-1,0))
            if self.current_movement == "D'":
                for index in [4,5,6,7]:
                    self.corner_list[index].rotate(-TURN_SPEED,(0,-1,0))
            
            if self.current_movement == "B":
                for index in [2,3,4,7]:
                    self.corner_list[index].rotate(TURN_SPEED,(0,0,1))
            if self.current_movement == "B'":
                for index in [2,3,4,7]:
                    self.corner_list[index].rotate(-TURN_SPEED,(0,0,1))
            
            if self.current_movement == "L":
                for index in [0,3,4,5]:
                    self.corner_list[index].rotate(TURN_SPEED,(-1,0,0))
            if self.current_movement == "L'":
                for index in [0,3,4,5]:
                    self.corner_list[index].rotate(-TURN_SPEED,(-1,0,0))
        
        if self.is_doing_algorithm:
            self.do_algorithm()
    
    
    def do_algorithm(self):        
        if self.index_algorithm < len(self.algorithm) and not self.is_turning:
            if self.index_algorithm < len(self.algorithm) - 1 and self.algorithm[self.index_algorithm+1] == "'":
                X = self.algorithm[self.index_algorithm] + "'"
                self.index_algorithm += 2
            else:
                X = self.algorithm[self.index_algorithm]
                self.index_algorithm += 1
        
            
            if X == "R":
                self.r_movement()
            elif X == "R'":
                self.rp_movement()
            
            elif X == "U":
                self.u_movement()
            elif X == "U'":
                self.up_movement()
            
            elif X == "F":
                self.f_movement()
            elif X == "F'":
                self.fp_movement()
            
            elif X == "D":
                self.d_movement()
            elif X == "D'":
                self.dp_movement()
            
            elif X == "B":
                self.b_movement()
            elif X == "B'":
                self.bp_movement()
            
            elif X == "L":
                self.l_movement()
            elif X == "L'":
                self.lp_movement()

        
        if self.index_algorithm == len(self.algorithm):
            self.index_algorithm = 0
            self.is_doing_algorithm = False


algorithm = "RUR'U'R'FRRU'R'U'RUR'F'"



# rouge devant, bleu droite, blanc haut
vertices = [(-1,1,-1), (1,1,-1), (1,1,1), (-1,1,1), (-1,-1,1), (-1,-1,-1), (1,-1,-1), (1,-1,1)]
# vertices = [(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1), (-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1)]
faces = [(0,1,6,5), (1,2,7,6), (2,3,4,7), (3,0,5,4), (0,1,2,3), (4,5,6,7)]

cube_origins = [(-.5, .5, -.5), (.5, .5, -.5), (.5, .5, .5), (-.5, .5, .5), (-.5, -.5, .5), (-.5, -.5, -.5), (.5, -.5, -.5), (.5, -.5, .5)]     # ordre bon

# devant, droite, derriere, gauche, haut, bas
BLACK = [0,0,0]
RED = [255,0,0]
BLUE = [0,0,255]
ORANGE = [255,127,0]
GREEN = [0,255,0]
WHITE = [255,255,255]
YELLOW = [255,255,0]

faces_color = [[RED,BLACK,BLACK,GREEN,WHITE,BLACK],
                [RED,BLUE,BLACK,BLACK,WHITE,BLACK],
                [BLACK,BLUE,ORANGE,BLACK,WHITE,BLACK],
                [BLACK,BLACK,ORANGE,GREEN,WHITE,BLACK],
                [BLACK,BLACK,ORANGE,GREEN,BLACK,YELLOW],
                [RED,BLACK,BLACK,GREEN,BLACK,YELLOW],
                [RED,BLUE,BLACK,BLACK,BLACK,YELLOW],
                [BLACK,BLUE,ORANGE,BLACK,BLACK,YELLOW]
]

corner_list = []
meshes = []
for i,origin in enumerate(cube_origins):
    cube = Mesh(vertices, faces, faces_color[i])
    cube.scale((0.5, 0.5, 0.5))
    cube.translate(origin)
    meshes.append(cube)
    corner_list.append(cube)

scene = Scene(meshes, RubiksCube(corner_list, algorithm), 90, 5)

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)
    scene.rubikscube.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                scene.rubikscube.r_movement()
            if event.key == pygame.K_t:
                scene.rubikscube.rp_movement()
            if event.key == pygame.K_u:
                scene.rubikscube.u_movement()
            if event.key == pygame.K_i:
                scene.rubikscube.up_movement()
            if event.key == pygame.K_d:
                scene.rubikscube.d_movement()
            if event.key == pygame.K_s:
                scene.rubikscube.dp_movement()
            if event.key == pygame.K_f:
                scene.rubikscube.f_movement()
            if event.key == pygame.K_g:
                scene.rubikscube.fp_movement()
            if event.key == pygame.K_b:
                scene.rubikscube.b_movement()
            if event.key == pygame.K_n:
                scene.rubikscube.bp_movement()
            if event.key == pygame.K_l:
                scene.rubikscube.l_movement()
            if event.key == pygame.K_m:
                scene.rubikscube.lp_movement()
            
            if event.key == pygame.K_a:
                scene.rubikscube.is_doing_algorithm = not scene.rubikscube.is_doing_algorithm
    
    ROTATION_SPEED = 2
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_8]:
        scene.euler_angles[0] += ROTATION_SPEED
    if keys[pygame.K_KP_5]:
        scene.euler_angles[0] -= ROTATION_SPEED
    if keys[pygame.K_KP_4]:
        scene.euler_angles[1] -= ROTATION_SPEED
    if keys[pygame.K_KP_6]:
        scene.euler_angles[1] += ROTATION_SPEED
    if keys[pygame.K_KP_7]:
        scene.euler_angles[2] += ROTATION_SPEED
    if keys[pygame.K_KP_9]:
        scene.euler_angles[2] -= ROTATION_SPEED

    window.fill((255, 255, 255))
    scene.draw(window)
    # scene.euler_angles[1] -= 1
    # scene.euler_angles[0] += 1
    pygame.display.flip()

pygame.quit()
exit()