from matplotlib import transforms
from postprocessing import Postprocessor
from matrix import Matrix

class Cycle:

    @staticmethod
    def processing(data: tuple, file_name):
        heidenhain = Postprocessor(file_name)
        Cycle().__head(heidenhain)

        center = Matrix([data[0:3]])
        center.transpose()
        angleB = 90
        radius = data[3] / 2
        # Q263 Q264 Q261 Q320 Q272 Q267 Q260 Q281 Q288 Q289 Q309 Q330
        params_Q = [0, 0, 0, 5, 3, -1, 0, 0, radius + 5, radius - 5, 0, 0]
        
        rotB = Matrix.transformation3D([0,1,0], angleB)

        for i in range(int(data[4])):
            angleC = data[5] + data[6] * i
            transform = rotB * Matrix.transformation3D([0,0,1], angleC)
            point = transform * center
            coord = point[0,0],point[1,0],point[2,0]
            params_Q[0] = coord[0]
            params_Q[1] = coord[1]
            params_Q[2] = coord[2]
            params_Q[6] = coord[2] + radius + 53

            Cycle.__plane_spatial(heidenhain, 0, angleB, angleC)
            Cycle.__rot_motion(heidenhain, None, angleB, angleC)
            Cycle.__line_motion(heidenhain, y = coord[1], z = coord[2] + radius + 150, feed = 0)
            Cycle.__line_motion(heidenhain, coord[0], feed = 0)
            Cycle.__line_motion(heidenhain, z = params_Q[6] - 3, feed = 1000)
            Cycle.__cycle(heidenhain, params_Q)
            Cycle.__line_motion(heidenhain, z = coord[2] + radius + 150, feed = 0)
            Cycle.__plane_spatial(heidenhain)

        Cycle().__tail(heidenhain)

    @staticmethod
    def __head(post:Postprocessor):
        post.write_line('BEGIN PGM PROBING MM')
        Cycle.__plane_spatial(post)
        post.write_line('L Z-1 R0 FMAX M91')
        post.write_line('L X-1300 Y-1 R0 FMAX M91')
        post.write_line('L B0 C0 FMAX')
        post.write_line('TOOL CALL 30 Z S10')
        post.write_line('M570')
        post.write_line('CYCLE DEF 247 NAZN.KOORD.BAZ.TOCH ~')
        post.write_line('\tQ339=+1\t;NOMER TOCHKI ODN.', withnumber = False)

    @staticmethod
    def __line_motion(post:Postprocessor, x = None,y = None,z = None,feed = None):
        adresses = list()
        if x != None:
            adresses.append('X{:+.3f}'.format(x).rstrip('0'))
        if y != None:
            adresses.append('Y{:+.3f}'.format(y).rstrip('0'))
        if z != None:
            adresses.append('Z{:+.3f}'.format(z).rstrip('0'))
        if feed != None:
            if feed > 0:
                adresses.append('F{:d}'.format(int(feed)))
            else:
                adresses.append('FMAX')
        post.write_line('L', ' '.join(adresses))

    @staticmethod
    def __rot_motion(post:Postprocessor, a = None, b = None,c = None,feed = None):
        adresses = list()
        if a != None:
            adresses.append('A{:+.3f}'.format(a).rstrip('0'))
        if b != None:
            adresses.append('B{:+.3f}'.format(b).rstrip('0'))
        if c != None:
            adresses.append('C{:+.3f}'.format(c).rstrip('0'))
        if feed != None:
            if feed > 0:
                adresses.append('F{:d}'.format(int(feed)))
            else:
                adresses.append('FMAX')
        post.write_line('L', ' '.join(adresses))
    
    @staticmethod
    def __plane_spatial(post:Postprocessor, a = 0, b = 0, c = 0):
        if a or b or c:
            adresses = list()
            adresses.append('SPA{:+.3f}'.format(a).rstrip('0'))
            adresses.append('SPB{:+.3f}'.format(b).rstrip('0'))
            adresses.append('SPC{:+.3f}'.format(c).rstrip('0'))
            adresses.append('SEQ+')
            post.write_line('PLANE SPATIAL', ' '.join(adresses))
        else:
            post.write_line('PLANE RESET STAY')

    @staticmethod
    def __cycle(post: Postprocessor, q: list):
        post.write_line('TCH PROBE 427 IZMERENIE KOORDINATA ~')
        post.write_line('\tQ263={:+.3f}'.format(q[0]).rstrip('0'),  '\t;1-A KOOR. 1-J TOCHKI ~', withnumber = False)
        post.write_line('\tQ264={:+.3f}'.format(q[1]).rstrip('0'),  '\t;2-A KOOR. 1-J TOCHKI ~', withnumber = False)
        post.write_line('\tQ261={:+.3f}'.format(q[2]).rstrip('0'),  '\t;WYSOTA IZMERENIA ~', withnumber = False)
        post.write_line('\tQ320={:+.3f}'.format(q[3]).rstrip('0'),  '\t;BEZOPASN.RASSTOYANIE ~', withnumber = False)
        post.write_line('\tQ272={:+d}'.format(q[4]),                '\t;OS IZMERENIA ~', withnumber = False)
        post.write_line('\tQ267={:+d}'.format(q[5]),                '\t;NAPRAWLENJE PEREM. ~', withnumber = False)
        post.write_line('\tQ260={:+.3f}'.format(q[6]).rstrip('0'),  '\t;B.WYSOTA ~', withnumber = False)
        post.write_line('\tQ281={:+d}'.format(q[7]),                '\t;PROTOKOL IZMERENIA ~', withnumber = False)
        post.write_line('\tQ288={:+.3f}'.format(q[8]).rstrip('0'),  '\t;MAKSIMALNYJ RAZZMER ~', withnumber = False)
        post.write_line('\tQ289={:+.3f}'.format(q[9]).rstrip('0'),  '\t;MINIMALNYJ RAZMER ~', withnumber = False)
        post.write_line('\tQ309={:+d}'.format(q[10]),               '\t;PGM- STOP DOPUSK ~', withnumber = False)
        post.write_line('\tQ330={:+d}'.format(q[11]),               '\t;INSTRUMENT ~', withnumber = False)

    @staticmethod
    def __tail(post:Postprocessor):
        Cycle.__plane_spatial(post)
        post.write_line('L X-1300 Y-1 R0 FMAX M91')
        post.write_line('L B0 C0 FMAX')
        post.write_line('FN 16: F-PRINT TEMPLATE.A / SCREEN')
        post.write_line('END PGM PROBING MM')
