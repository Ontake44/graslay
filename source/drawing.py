
import math
import pyxel
import gcommon

class Drawing:
    hexTable = ['0', '1', '2', '3', '4', '5', '6', '7','8','9','A','B','C','D','E','F']
    
    # workData : []
    # srcImage : []
    @classmethod
    def setRotateImage(cls, imgx :int, imgy :int, img :int, workData, srcImage, rad:float, backColor:int):
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
            for dummy in range(width):
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

    @classmethod
    def showTextHCenter(cls, y, s):
        l = len(s)
        cls.showText((gcommon.SCREEN_WIDTH -l*8)/2, y, s)

    @classmethod
    def showTextRateHCenter(cls, y, s, rate):
        l = len(s)
        cls.showTextRate((gcommon.SCREEN_WIDTH -l*8)/2, y, s, rate)


    @classmethod
    def showTextC(cls, x, y, s, color1, color2):
        pyxel.pal(7, color1)
        pyxel.pal(5, color2)
        cls.showText(x, y, s)
        pyxel.pal()

    # BOLDフォント
    @classmethod
    def showText(cls, x, y, s):
        for c in s:
            code = ord(c)
            if code >= 65 and code <= 90:
                pyxel.blt(x, y, 0, (code-65)*8, 128, 8, 8, gcommon.TP_COLOR)
            elif code >= 0x30 and code <= 0x39:
                # 数字
                pyxel.blt(x, y, 0, (code-48)*8, 136, 8, 8, gcommon.TP_COLOR)
            elif code >= 0x3A and code <= 0x3F:
                # :;<=>?
                pyxel.blt(x, y, 0, 208 + (code-0x3A)*8, 128, 8, 8, gcommon.TP_COLOR)
            elif code >= 0x20 and code <= 0x2F:
                # スペース - /
                pyxel.blt(x, y, 0, 80 + (code-0x20)*8, 136, 8, 8, gcommon.TP_COLOR)
            elif code == 0x40:
                # @ どくろ
                pyxel.blt(x, y, 0, 232, 136, 8, 8, gcommon.TP_COLOR)
            elif code == 0x7D:
                # 自機
                pyxel.blt(x, y, 0, 8, 32, 8, 8, gcommon.TP_COLOR)
            x += 8

    # 下から上にあがってくる文字
    # rateは 0 - 1
    @classmethod
    def showTextRate(cls, x, y, s, rate):
        p = int(8 * rate)
        if p == 0:
            return
        for c in s:
            code = ord(c)
            if code >= 65 and code <= 90:
                pyxel.blt(x, y+8-p, 0, (code-65)*8, 128, 8, p, gcommon.TP_COLOR)
            elif code >= 48 and code <= 57:
                pyxel.blt(x, y+8-p, 0, (code-48)*8, 136, 8, p, gcommon.TP_COLOR)
            x += 8

    # 上から下にさがってくる文字
    # rateは 0 - 1
    @classmethod
    def showTextRate2(cls, x, y, s, rate):
        p = int(8 * rate)
        if p == 0:
            return
        for c in s:
            code = ord(c)
            if code >= 65 and code <= 90:
                pyxel.blt(x, y, 0, (code-65)*8, 128 + 8-p, 8, p, gcommon.TP_COLOR)
            elif code >= 48 and code <= 57:
                pyxel.blt(x, y, 0, (code-48)*8, 136 + 8-p, 8, p, gcommon.TP_COLOR)
            x += 8

    # 普通フォント
    @classmethod
    def showText2(cls, x, y, s):
        if x == -999:
            x = 127 - len(s)/2 *6
        if y == -999:
            y = 192/2 - 8/2
        for c in s:
            code = ord(c)
            if code >= 65 and code <= 90:
                pyxel.blt(x, y, 0, (code-65)*8, 112, 6, 8, gcommon.TP_COLOR)
            elif code >= 48 and code <= 57:
                pyxel.blt(x, y, 0, (code-48)*8, 120, 6, 8, gcommon.TP_COLOR)
            x += 6

    @classmethod
    def showTextHCentor2(cls, y, s, clr):
        pyxel.text(128 -len(s)*2, y, s, clr)

    @classmethod
    def drawRectbs(cls, rects, clr):
        for rect in rects:
            pyxel.rectb(rect.left, rect.top, rect.getWidth(), rect.getHeight(), clr)

    @classmethod
    def stretchBlt(cls, dx, dy, dwidth, dheight, img, sx, sy, swidth, sheight):
        wx = 0
        wy = 128
        # 
        a = sheight/dheight
        py = sy
        for y in range(int(dheight)):
            #pyxel.image(img).copy(wx, wy+y, img, sx, py, swidth, 1)
            pyxel.image(img).blt(wx, wy+y, img, sx, py, swidth, 1)
            py += a
        a = swidth/dwidth
        px = wx
        pyxel.pal()
        for x in range(int(dwidth)):
            pyxel.blt(dx +x, dy, img, px, wy, 1, dheight, 0)
            px += a

    @classmethod
    def drawUpDownMarker(cls, x, y):
        pyxel.blt(x, y, 0, 0, 32, -8, 8, gcommon.TP_COLOR)
        pyxel.blt(x +26, y, 0, 0, 32, 8, 8, gcommon.TP_COLOR)

    @classmethod
    def drawUpDownMarker2(cls, x, y, min, max, value):
        cls.drawLeftMarker(x, y, min < value)
        cls.drawRightMarker(x +26, y, value < max)
        #pyxel.blt(x, y, 0, 0, 32, -8, 8, TP_COLOR)
        #pyxel.blt(x +26, y, 0, 0, 32, 8, 8, TP_COLOR)

    @classmethod
    def drawLeftMarker(cls, x, y, enabled):
        pyxel.blt(x, y, 0, 0 if enabled else 16, 32, -8, 8, gcommon.TP_COLOR)

    @classmethod
    def drawRightMarker(cls, x, y, enabled):
        pyxel.blt(x, y, 0, 0 if enabled else 16, 32, 8, 8, gcommon.TP_COLOR)

    @classmethod
    def setPolyPoints(cls, points, start, end, includeStart):
        #dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dy == 0:
            points[start[1]].append(start[0])
            points[start[1]].append(end[0])
        else:
            reverse = False
            if end[1] > start[1]:
                sx = start[0]
                sy = int(start[1])
                ex = end[0]
                ey = int(end[1])
            else:
                reverse = True
                sx = end[0]
                sy = int(end[1])
                ex = start[0]
                ey = int(start[1])
            # 逆傾きa
            a = (ex - sx)/(ey - sy)
            if includeStart:
                yy = sy
                while yy <= ey:
                    xx = sx + a * (yy -sy)
                    nx = int(xx)
                    points[yy].append(nx)
                    yy += 1
            else:
                if reverse:
                    yy = sy
                    while yy < ey:
                        xx = sx + a * (yy -sy)
                        nx = int(xx)
                        points[yy].append(nx)
                        yy += 1
                else:
                    yy = sy +1
                    while yy <= ey:
                        xx = sx + a * (yy -sy)
                        nx = int(xx)
                        points[yy].append(nx)
                        yy += 1


    # ソリッド・エリア・スキャン・コンバージョン？でポリゴンを描く
    # バンク４に描く
    # poly [x,y]配列
    @classmethod
    def drawPolygonSystemImage(cls, poly):
        points = []
        for i in range(200):
            points.append([])
        
        length = len(poly)
        prev = poly[length -2]
        current = poly[length -1]
        next = poly[0]
        for i in range(length):
            
            if (int(next[1])-int(current[1]))==0:
                pass
            else:
                includeStart = True
                if (int(current[1]) - int(prev[1]))== 0:
                    pass
                elif (current[1] - prev[1])*(next[1] - current[1]) > 0:
                    #print(str(current[0]) + " " + str(current[1]))
                    includeStart = False
                
                cls.setPolyPoints(points, current, next, includeStart)
                
            prev = current
            current = next
            if i == length -1:
                next =  poly[0]
            else:
                next = poly[i+1]
        
        y = 0
        for p in points:
            l = len(p)
            for i in range(0,l,2):
                if l & 1 == 0:
                    for i in range(0,l,2):
                        #pyxel.line(p[i], y, p[i+1], y, clr)
                        if p[i] < p[i+1]:
                            pyxel.blt(p[i], y, pyxel.screen, p[i], y, p[i+1] -p[i]+1, 1)
                        else:
                            pyxel.blt(p[i+1], y, pyxel.screen, p[i+1], y, p[i] -p[i+1]+1, 1)
            y += 1

    @classmethod
    def setBrightness1(cls):
        pyxel.pal(0, 1)
        pyxel.pal(1, 5)
        pyxel.pal(2, 4)
        pyxel.pal(3, 11)
        pyxel.pal(4, 8)
        pyxel.pal(5, 12)
        pyxel.pal(6, 7)
        pyxel.pal(7, 7)
        pyxel.pal(8, 14)
        pyxel.pal(9, 10)
        pyxel.pal(10, 7)
        pyxel.pal(11, 6)
        pyxel.pal(12, 6)
        pyxel.pal(13, 15)
        pyxel.pal(14, 15)
        pyxel.pal(15, 7)

    @classmethod
    def setUnderwaterColor(cls):
        pyxel.pal(0, 1)
        pyxel.pal(1, 5)
        pyxel.pal(2, 1)
        pyxel.pal(3, 1)
        pyxel.pal(4, 2)
        pyxel.pal(5, 1)
        pyxel.pal(6, 12)
        pyxel.pal(7, 13)
        pyxel.pal(8, 2)
        pyxel.pal(9, 4)
        pyxel.pal(10, 9)
        pyxel.pal(11, 3)
        pyxel.pal(12, 6)
        pyxel.pal(13, 5)
        pyxel.pal(14, 8)
        pyxel.pal(15, 14)

    @classmethod
    def setBrightnessMinus1(cls):
        pyxel.pal(1, 0)
        pyxel.pal(2, 1)
        pyxel.pal(3, 1)
        pyxel.pal(4, 2)
        pyxel.pal(5, 1)
        pyxel.pal(6, 12)
        pyxel.pal(7, 13)
        pyxel.pal(8, 2)
        pyxel.pal(9, 8)
        pyxel.pal(10, 9)
        pyxel.pal(11, 3)
        pyxel.pal(12, 5)
        pyxel.pal(13, 5)
        pyxel.pal(14, 8)
        pyxel.pal(15, 10)

    color_table = [
    0,1,2,8,4,5,3,9,12,13,14,11,6,10,15,7
    ]

    dark_color_table = [
    #   0  1  2  3  4  5   6   7  8  9 10 11 12 13 14  15
        0, 0, 1, 1, 2, 1, 12, 13, 2, 8, 9, 3, 5, 5, 8, 10
    ]


    # 明るさを設定する（-15～+15）
    @classmethod
    def setBrightness(cls, level):
        for c in range(16):
            if c + level > 15:
                pyxel.pal(cls.color_table[c], 7)
            elif c + level < 0:
                pyxel.pal(cls.color_table[c], 0)
            else:
                pyxel.pal(cls.color_table[c], cls.color_table[c +level])

    @classmethod
    def setBrightnessWithoutBlack(cls, level):
        for c in range(1, 15):
            if c + level > 15:
                pyxel.pal(cls.color_table[c], 7)
            elif c + level < 0:
                pyxel.pal(cls.color_table[c], 0)
            else:
                pyxel.pal(cls.color_table[c], cls.color_table[c +level])

    @classmethod
    def setBrightnessWithoutBlack2(cls, level):
        if level == 0:
            return
        tbl = [0] * 16
        for c in range(1, 15):
            tbl[c] = cls.dark_color_table[c]
        for i in range(-level-1):
            for c in range(1, 15):
                tbl[c] = cls.dark_color_table[tbl[c]]
        for c in range(1, 15):
            pyxel.pal(c, tbl[c])

    @classmethod
    def clipLine(cls, ip1, ip2, points):

        # 描画領域と端点との Y 方向の距離を求める
        if ip2[1] < gcommon.SCREEN_MIN_Y:
            dy = gcommon.SCREEN_MIN_Y - ip1[1]
        else:
            dy = gcommon.SCREEN_MAX_Y - ip1[1]
        
        # X 方向の距離に変換した上で、描画領域の端と線分の交点の X 座標を求める
        x = ( ip2[0] - ip1[0]) * dy / ( ip2[1] - ip1[1]) + ip1[0]
        # 描画領域の端と線分の交点の Y 座標
        if ip2[1] < gcommon.SCREEN_MIN_Y:
            y = gcommon.SCREEN_MIN_Y
        else:
            y = gcommon.SCREEN_MAX_Y

        points.append([x, y])
        return points

    @classmethod
    def clipPolygon(cls, vertex):
        clippedVertex = []
        vertexCnt = len(vertex)		# 頂点の数	
        i = 1
        while i<= vertexCnt:
            c0 = vertex[i-1]		# 始点
            c1 = vertex[i % vertexCnt]		# 終点
            if  c0[0] == c1[0] and c0[1] == c1[1]:
                continue
            # 始点がエリア外
            if ( ( c0[1] <gcommon.SCREEN_MIN_Y) or ( c0[1] > gcommon.SCREEN_MAX_Y ) ):
                # 終点はエリア内
                if ( ( c1[1] >= gcommon.SCREEN_MIN_Y) and ( c1[1] <= gcommon.SCREEN_MAX_Y) ):
                    clippedVertex = cls.clipLine(c1, c0, clippedVertex)
                # 終点もエリア外(クリッピング・エリアの上下境界をまたぐ)
                elif ( ( ( c0[1] < gcommon.SCREEN_MIN_Y) and ( c1[1] > gcommon.SCREEN_MAX_Y ) ) or
                        ( ( c1[1] < gcommon.SCREEN_MIN_Y ) and ( c0[1] > gcommon.SCREEN_MAX_Y) ) ):
                    clippedVertex = cls.clipLine( c1, c0, clippedVertex)
                    clippedVertex = cls.clipLine( c0, c1, clippedVertex)
                
            # 始点がエリア内
            else:
                clippedVertex.append( c0 )
                # 終点がエリア外ならクリッピングして頂点を追加
                if ( ( c1[1] < gcommon.SCREEN_MIN_Y ) or ( c1[1] > gcommon.SCREEN_MAX_Y ) ):
                    clippedVertex = cls.clipLine( c0, c1, clippedVertex)
            i += 1
        return clippedVertex


    # ただの４角形（長方形とは限らない）
    #  points = [[0,0],[1,0], [1,1],[0,1]]
    @classmethod
    def drawQuadrangle(cls, points, clr):
            pyxel.tri(points[0][0], points[0][1],
            points[1][0], points[1][1],
            points[2][0], points[2][1], clr)
            pyxel.tri(
            points[0][0], points[0][1],
            points[2][0], points[2][1],
            points[3][0], points[3][1], clr)

    # ただの４角形（長方形とは限らない）ワイヤーフレーム
    #  points = [[0,0],[1,0], [1,1],[0,1]]
    @classmethod
    def drawQuadrangleB(cls, points, clr):
            pyxel.line(points[0][0], points[0][1], points[1][0], points[1][1], clr)
            pyxel.line(points[1][0], points[1][1], points[2][0], points[2][1], clr)
            pyxel.line(points[2][0], points[2][1], points[3][0], points[3][1], clr)
            pyxel.line(points[3][0], points[3][1], points[0][0], points[0][1], clr)

    # 頂点配列、色でポリゴンを描く
    @classmethod
    def drawPolygon(cls, poly, clr):
        sx = poly[0][0]
        sy = poly[0][1]
        for i in range(len(poly)-2):
            pyxel.tri(sx, sy, 
                poly[i+1][0], poly[i+1][1],
                poly[i+2][0], poly[i+2][1], clr)	

    # 頂点配列、色でポリゴンを描く
    @classmethod
    def drawPolygonPos(cls, x, y, poly, clr):
        sx = x+poly[0][0]
        sy = y+poly[0][1]
        for i in range(len(poly)-2):
            pyxel.tri(sx, sy, 
                x+poly[i+1][0], y+poly[i+1][1],
                x+poly[i+2][0], y+poly[i+2][1], clr)	


    # 頂点配列、色でポリゴンを描く（外枠あり）
    @classmethod
    def drawPolygon2(cls, poly, clr1, clr2):
        cls.drawPolygon(poly, clr1)
        last = len(poly) -1
        for i in range(last):
            pyxel.line(poly[i][0], poly[i][1], poly[i+1][0], poly[i+1][1], clr2)
        pyxel.line(poly[last][0], poly[last][1], poly[0][0], poly[0][1], clr2)

    # Polygonクラス指定で描く
    @classmethod
    def drawPolygon3(cls, polygon):
        points = polygon.points
        if polygon.fill:
            sx = points[0][0]
            sy = points[0][1]
            for i in range(len(points)-2):
                pyxel.tri(sx, sy, 
                    points[i+1][0], points[i+1][1],
                    points[i+2][0], points[i+2][1], polygon.clr)
        else:
            # ワイヤーフレーム
            endIndex = len(points) -1
            if endIndex > 1:
                for i in range(endIndex):
                    pyxel.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], polygon.clr)
            pyxel.line(points[endIndex][0], points[endIndex][1], points[0][0], points[0][1], polygon.clr)

    # Ploygonsクラス指定で描く
    @classmethod
    def drawPolygons(cls, polys):
        for p in polys.polygons:
            cls.drawPolygon3(p)

    # 頂点配列、色でLINEを描く
    # poly[n] - poly[n+1]でLINEを描く
    @classmethod
    def drawLines(cls, points, clr):
        for i in range(0, len(points), 2):
            pyxel.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], clr)

    # 頂点配列、色でLINEを描く（各頂点を結ぶ）
    # poly[n] - poly[n+1]でLINEを描く
    @classmethod
    def drawConnectedLines(cls, points, clr):
        for i in range(len(points)-1):
            pyxel.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], clr)

    @classmethod
    def blt(cls, x, y, img, u, v, w, h, colkey=-1):
        pyxel.blt(gcommon.sint(x), gcommon.sint(y), img, u, v, w, h, colkey)

    @classmethod
    def bltm(cls, x, y, tm, u, v, w, h, colkey=None):
        #print("x:" + str(x) + " y:"+str(y) + " tm:" +str(tm) + " u:" +str(u) + " v:"+str(v) + " w:"+str(w) + " h:" +str(h) + " colkey:" + str(colkey))
        pyxel.bltm(gcommon.sint(x), gcommon.sint(y), tm, u*8, v*8, w*8, h*8, colkey)


