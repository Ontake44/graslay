
import math
import pyxel
import gcommon

class Drawing:
    hexTable = ['0', '1', '2', '3', '4', '5', '6', '7','8','9','A','B','C','D','E','F']
    
    @classmethod
    def setRotateImage(cls, imgx :int, imgy :int, img :int, workData :[], srcImage :[], rad:float, backColor:int):
        width = len(srcImage[0])
        height = len(srcImage)
        dx = math.cos(rad)
        dy = math.sin(rad)
        ddx = -math.sin(rad)
        ddy = math.cos(rad)
        px0 = width/2
        py0 = height/2
        ox = -(width/2 * dx - height/2 * dy)
        oy = -(height/2 * dy + width/2 * dx)
        tbl =  cls.hexTable
        backColorStr = tbl[backColor]
        for desty in range(height):
            px = px0
            py = py0
            line = ''
            for destx in range(width):
                x = int(px + ox)
                y = int(py + oy)
                if x >= 0 and x < width and y >= 0 and y < height:
                    line += tbl[srcImage[y][x]]
                else:
                    line += backColorStr
                px += dx
                py += dy
            px0 += ddx
            py0 += ddy
            workData[desty] = line
        pyxel.image(img).set(imgx, imgy, workData)
