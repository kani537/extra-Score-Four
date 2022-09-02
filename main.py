import threading
import time
import tkinter
import tkinter.messagebox


CANVAS_SIZE = 800

NUM_MASS = 5

# 色の設定
BOARD_COLOR = 'burlywood3'
YOUR_COLOR = 'black'
COM_COLOR = 'white'

# プレイヤーを示す値
YOU = 1
COM = 2

class Gobang():
    def __init__(self, master,Button):
        '''コンストラクタ'''

        self.master = master
        self.player = YOU
        self.board = None
        self.color = {
            YOU : YOUR_COLOR,
            COM : COM_COLOR
        }
        self.nextDisk = None

        self.createWidgets()
        self.setEvents(Button)

        self.initGobang()


    def createWidgets(self):

        # キャンバスの作成
        self.canvas = tkinter.Canvas(
            self.master,
            bg=BOARD_COLOR,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

    def setEvents(self,Button):
        self.canvas.bind('<ButtonPress>', self.click)
        Button.bind("<Button-1>",self.revolution)

    def initGobang(self):

        self.board = [[None] * (NUM_MASS + 1) for i in range(NUM_MASS + 1)]

        self.interval = CANVAS_SIZE // (NUM_MASS + 2)

        self.offset_x = self.interval
        self.offset_y = self.interval

        for x in range(NUM_MASS + 1):
            xs = x * self.interval + self.offset_x
            ys = self.offset_y
            xe = xs
            ye = (NUM_MASS) * self.interval + self.offset_y
                
            self.canvas.create_line(
                xs, ys,
                xe, ye,
            )

        for y in range(NUM_MASS + 1):
            # 線の開始・終了座標を計算
            xs = self.offset_x
            ys = y * self.interval + self.offset_y
            xe = (NUM_MASS) * self.interval + self.offset_x
            ye = ys
                
            self.canvas.create_line(
                xs, ys,
                xe, ye,
            )

    def drawDisk(self, x, y, color):
        center_x = x * self.interval + self.interval
        center_y = y * self.interval + self.interval

        xs = center_x
        ys = center_y
        xe = center_x - (self.interval)
        ye = center_y - (self.interval)
        
        tag_name = 'disk_' + str(x) + '_' + str(y)
        self.canvas.create_oval(
            xs, ys,
            xe, ye,
            fill=color,
            tags=str(x) + str(y) + "a"
        )

        return tag_name

    def getIntersection(self, x, y):
        ix = x // self.interval
        iy = y // self.interval

        return ix, iy

    def click(self, event):
        if self.player != YOU:
            return

        x, y = self.getIntersection(event.x, event.y)
        self.placed = True

        if x <= 0 or x >= NUM_MASS + 1 or y <= 0 or y >= NUM_MASS + 1:
            return

        if not self.board[y][x]:
            self.player = COM
            self.place(x, y, YOUR_COLOR)
    
    def deleteDist(self, x, y, color):
        time.sleep(0.5)
        self.canvas.delete(str(x) + str(y) + "a")
        self.place(x,y + 1,color)

    def down(self, x, y, color):
        if y < 5:
            if self.board[y + 1][x] != YOUR_COLOR:
                if self.board[y + 1][x] != COM_COLOR:
                    threading.Thread(target=self.deleteDist,args=(x,y,color)).start()
                    return True

    

    def place(self, x, y, color):
        index = False
        self.drawDisk(x, y, color)
        index = self.down(x,y,color)
        if index:
            return

        self.board[y][x] = color
        
        if self.count(x, y, color) >= 4:
            self.showResult(color)
            return
        if self.player == COM:
            self.canvas.bind('<ButtonPress>', self.com)
        else:
            self.canvas.bind('<ButtonPress>', self.click)

    def count(self, x, y, color):
        count_dir = [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
        ]

        max = 0
        for i, j in count_dir:
            count_num = 1
            for s in range(1, NUM_MASS + 1):
                
                xi = x + i * s
                yj = y + j * s

                if xi < 0 or xi >= NUM_MASS + 1 or yj < 0 or yj >= NUM_MASS + 1:
                    break

                if self.board[yj][xi] != color:
                    break

                count_num += 1

            for s in range(-1, -(NUM_MASS + 1), -1):
                xi = x + i * s
                yj = y + j * s

                if xi < 0 or xi >= NUM_MASS + 1 or yj < 0 or yj >= NUM_MASS + 1:
                    break

                if self.board[yj][xi] != color:
                    break

                count_num += 1

            if max < count_num:
                max = count_num
        
        return max

    def showResult(self,color):
        if color == YOUR_COLOR:
            winner = COM
        else:
            winner = YOU
        if winner == YOU:
            tkinter.messagebox.showinfo('結果', '白の勝ちです!!!')
        else:
            tkinter.messagebox.showinfo('結果', '黒の勝ちです!!!')

    def com(self,event):

        if self.player == YOU:
            return

        x, y = self.getIntersection(event.x, event.y)
        self.placed = True

        if x <= 0 or x >= NUM_MASS + 1 or y <= 0 or y >= NUM_MASS + 1:
            return

        if not self.board[y][x]:

            self.player = YOU
            self.place(x, y, COM_COLOR)
    
    def rotate(self,x,y):
        if y == 1 : ix = 5
        if y == 2 : ix = 4
        if y == 3 : ix = 3
        if y == 4 : ix = 2
        if y == 5 : ix = 1
        if x == 1 : iy = 1
        if x == 2 : iy = 2
        if x == 3 : iy = 3
        if x == 4 : iy = 4
        if x == 5 : iy = 5

        return ix,iy
    
    def romove(self,x,y):
        time.sleep(2)
        if self.board[y + 1][x] != YOUR_COLOR:
            if self.board[y + 1][x] != COM_COLOR:
                self.board[y][x] = None

    def downRotated(self):
        for e in range(1,NUM_MASS + 1):
            for i in range(NUM_MASS,0,-1):
                time.sleep(0.01)
                index = False
                if self.tmpBoard[i][e] != None:
                    index = self.down(e,i,self.tmpBoard[i][e])
                if index:
                    continue
                self.board[i][e] = self.tmpBoard[i][e]
                self.tmpBoard[i][e] = None
    
    def revolution(self,event):
        # self.tmpBoard = None
        self.tmpBoard = [[None] * (NUM_MASS + 1) for i in range(NUM_MASS + 1)]
        for xs in range(1,NUM_MASS + 1):
            for ys in range(1,NUM_MASS + 1):
                if self.board[ys][xs] == YOUR_COLOR:
                    self.canvas.delete(str(xs) + str(ys) + "a")
                    x, y = self.rotate(xs, ys)
                    self.board[ys][xs] = None
                    self.drawDisk(x, y, YOUR_COLOR)
                    self.tmpBoard[y][x] = YOUR_COLOR
                if self.board[ys][xs] == COM_COLOR:
                    self.canvas.delete(str(xs) + str(ys) + "a")
                    x, y = self.rotate(xs, ys)
                    self.board[ys][xs] = None
                    self.drawDisk(x, y, COM_COLOR)
                    self.tmpBoard[y][x] = COM_COLOR
        
        threading.Thread(target=self.downRotated,args=()).start()
        
        Button.bind("<Button-1>",self.revolution)
        if self.placed:
            self.placed = False
            if self.player == COM:
                self.player = YOU
            else:
                self.player = COM


app = tkinter.Tk()
app.title('五目並べ')
Button = tkinter.Button(text=u'回転',width=5,height=1)
Button.pack()
gobang = Gobang(app,Button)
app.mainloop()