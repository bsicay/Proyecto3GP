import glm 
from numpy import array, float32

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.filled_mode()

        self.scene = []
        self.active_shader = None

        self.point_light = glm.vec3(0,0,0)
        self.time = 0
        self.value = 0;

        self.target = glm.vec3(0,0,0)
        self.angle_x = 0
        self.angle_y = 0
        self.cam_distance = 5

        # ViewMatrix
        self.cam_position = glm.vec3(0,0,0)
        self.cam_rotation = glm.vec3(0,0,0)
        self.viewMatrix = self.getViewMatrix()

        # Projection Matrix
        self.projectionMatrix = glm.perspective(
            glm.radians(60),        
            self.width/self.height, 
            0.1,                    
            1000
        )
        
    def filled_mode(self):
        glPolygonMode(GL_FRONT, GL_FILL)

    def wireframe_mode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def getViewMatrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.cam_position)

        pitch = glm.rotate(identity, glm.radians(self.cam_rotation.x), glm.vec3(1,0,0))
        yaw   = glm.rotate(identity, glm.radians(self.cam_rotation.y), glm.vec3(0,1,0))
        roll  = glm.rotate(identity, glm.radians(self.cam_rotation.z), glm.vec3(0,0,1))

        rotationMat = pitch * yaw * roll

        camMatrix = translateMat * rotationMat

        return glm.inverse(camMatrix)


    def set_shaders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.active_shader = compileProgram( 
                compileShader(vertexShader, GL_VERTEX_SHADER),
                compileShader(fragmentShader, GL_FRAGMENT_SHADER)
            )
        else:
            self.active_shader = None

    def update(self):
        self.viewMatrix = glm.lookAt(self.cam_position, self.target, glm.vec3(0,1,0))

    def render(self):
        glClearColor(0.2,0.2,0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.active_shader is not None:
            glUseProgram(self.active_shader)

            glUniformMatrix4fv( glGetUniformLocation(self.active_shader, "viewMatrix"),
                                1, GL_FALSE, glm.value_ptr(self.viewMatrix))

            glUniformMatrix4fv( glGetUniformLocation(self.active_shader, "projectionMatrix"),
                                1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

            glUniform1i( glGetUniformLocation(self.active_shader, "tex"), 0)
            
            glUniform1i( glGetUniformLocation(self.active_shader, "tex2"), 1)

            glUniform1f( glGetUniformLocation(self.active_shader, "time"), self.time)

            glUniform3fv( glGetUniformLocation(self.active_shader, "pointLight"), 1, glm.value_ptr(self.point_light))

        for obj in self.scene:
            if self.active_shader is not None:
                glUniformMatrix4fv( 
                    glGetUniformLocation(self.active_shader, "modelMatrix"),
                    1, GL_FALSE, glm.value_ptr(obj.get_model_matrix())
                )

            obj.render()
