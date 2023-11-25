import glm 

from numpy import array, float32

from OpenGL.GL import *

from Obj import Obj

from pygame import image

class Model(object):
        
    def __init__(self, objName, textureName, textureName2 = None):
        self.model = Obj(objName)

        self.createVertexBuffer()

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)
        
        self.textureSurface = image.load(textureName)
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)
        
        textureName2 = textureName if textureName2 == None else textureName2
        self.textureSurface2 = image.load(textureName2)
        self.textureData2 = image.tostring(self.textureSurface2, "RGB", True)
        self.texture2 = glGenTextures(1)
        
    def createVertexBuffer(self):
        buffer = []

        self.polycount = 0

        for face in self.model.faces:
            self.polycount += 1

            for i in range(3):
                # positions
                pos = self.model.vertices[face[i][0] - 1]
                buffer.append(pos[0])
                buffer.append(pos[1])
                buffer.append(pos[2])

                # texcoords
                uvs = self.model.texcoords[face[i][1] - 1]
                buffer.append(uvs[0])
                buffer.append(uvs[1])

                # normals
                norm = self.model.normals[face[i][2] - 1]
                buffer.append(norm[0])
                buffer.append(norm[1])
                buffer.append(norm[2])

            if len(face) == 4:

                self.polycount += 1

                for i in [0,2,3]:
                    # positions
                    pos = self.model.vertices[face[i][0] - 1]
                    buffer.append(pos[0])
                    buffer.append(pos[1])
                    buffer.append(pos[2])

                    # texcoords
                    uvs = self.model.texcoords[face[i][1] - 1]
                    buffer.append(uvs[0])
                    buffer.append(uvs[1])

                    # normals
                    norm = self.model.normals[face[i][2] - 1]
                    buffer.append(norm[0])
                    buffer.append(norm[1])
                    buffer.append(norm[2])


        self.vertBuffer = array(buffer, dtype = float32)
        
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

    def get_model_matrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        yaw   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        roll  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMat = pitch * yaw * roll

        scaleMat = glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def render(self):

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        glBufferData(GL_ARRAY_BUFFER,           
                     self.vertBuffer.nbytes,    
                     self.vertBuffer,           
                     GL_STATIC_DRAW)           

        glVertexAttribPointer(0,                
                              3,                
                              GL_FLOAT,          
                              GL_FALSE,          
                              4 * 8,             
                              ctypes.c_void_p(0)) 

        glEnableVertexAttribArray(0)

        # Atributo de texcoords
        glVertexAttribPointer(1,               
                              2,                
                              GL_FLOAT,          
                              GL_FALSE,          
                              4 * 8,             
                              ctypes.c_void_p(4*3)) 

        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2,                
                              3,               
                              GL_FLOAT,         
                              GL_FALSE,         
                              4 * 8,            
                              ctypes.c_void_p(4*5))

        glEnableVertexAttribArray(2)


        glActiveTexture( GL_TEXTURE0 )
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D,                     
                     0,                                 
                     GL_RGB,                            
                     self.textureSurface.get_width(),   
                     self.textureSurface.get_height(),  
                     0,                                 
                     GL_RGB,                           
                     GL_UNSIGNED_BYTE,                  
                     self.textureData)                  
        glGenerateMipmap(GL_TEXTURE_2D)
        
        glActiveTexture( GL_TEXTURE1 )
        glBindTexture(GL_TEXTURE_2D, self.texture2)
        glTexImage2D(GL_TEXTURE_2D,                     # Texture Type
                     0,                                 # Positions
                     GL_RGB,                            # Format
                     self.textureSurface2.get_width(),   # Width
                     self.textureSurface2.get_height(),  # Height
                     0,                                 # Border
                     GL_RGB,                            # Format
                     GL_UNSIGNED_BYTE,                   
                     self.textureData2)                  # Data
        glGenerateMipmap(GL_TEXTURE_2D)
        

        glDrawArrays(GL_TRIANGLES, 0, self.polycount * 3 )