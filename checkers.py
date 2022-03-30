
from constants import *

class Piece():
    #avatar can be a cirle sufrace or an image
    def __init__(self, avatar, type,row, col, x = None, y = None):
        self.avatar = avatar
        
        self.type = type

        self.boardRow = row
        self.boardColumn = col

        self.x = x
        self.y = y
        
        self.isKing = False

    def __repr__(self,):
        return self.type[0]

    def move(self):
        pass

    def getRect(self):
        return 



class InternalBoard():

    def __init__(self, ):

        self.board = [ [None]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.pieces = []
        self.init = False
        self.boxColors = WHITE, RED
        self.populateBoard()

    def populateBoard(self,):
        if self.init: return
        #fill upper part
        for row in range(LEVELS):
            for col in range(GRID_SIZE):
                if (row+col)%2:
                    self.board[row][col] = Piece(None, SIDES[0], row, col)
        
        #fill Lower parts
        for row in range(GRID_SIZE-LEVELS, GRID_SIZE):
            for col in range(GRID_SIZE):
                if (row+col)%2:
                    self.board[row][col] = Piece(None, SIDES[1], row, col)
        self.init = True

    def movePiece(self, from_, to) -> None:
        row, col = from_
        rowTo, colTo = to
        if (isinstance(self.board[rowTo][colTo], Piece)):
            return
        if to not in self.getPossibleMoves(*from_):
            return
        self.board[rowTo][colTo] = self.board[row][col]
        self.board[row][col] = None

        if(rowTo == 0 or rowTo == GRID_SIZE -1):
            self.board[rowTo][colTo].isKing = True

        #remove captured pawns
        self.removeCapturedPieces(from_, to)

        return True

    def removeCapturedPieces(self, from_: tuple, to:tuple)->None:
        row, col = from_
        rowTo, colTo = to

        #leading diagonal
        if (row < rowTo and col < colTo) or (row > rowTo and col > colTo):
            i, j = min(row, rowTo)+1, min(col, colTo)+1
            while(i < max(row, rowTo) and j < max(col, colTo) ):
                self.board[i][j] = None
                i += 1
                j+=1

        #alternate diagonal
        elif (row < rowTo and col > colTo) or (row > rowTo and col < colTo):
            i, j = min(row, rowTo)+1, max(col, colTo)-1
            while(i < max(row, rowTo) and j > min(col, colTo) ):
                self.board[i][j] = None
                i += 1
                j -= 1



    def getPiece(self, row, col):
        return self.board[row][col]

    def getPossibleMoves(self, row, col):
        piece = self.board[row][col]
        if not isinstance(piece, Piece):
            return []

        allMoves : list = []
        if piece.type == SIDES[1]: #moving up
            if row > 0 :
                #right side
                if col -1 >= 0:
                    if not isinstance(self.board[row-1][col-1], Piece):
                        allMoves.append((row-1, col-1))
                    elif isinstance(self.board[row-1][col-1], Piece) and self.board[row-1][col-1].type != SIDES[1]:
                        if row > 1:
                            if col -2 >= 0:
                                if not isinstance(self.board[row-2][col-2], Piece):
                                    allMoves.append((row-2, col-2))
                #left side
                if col + 1 < GRID_SIZE:
                    if not isinstance(self.board[row-1][col + 1], Piece):
                        allMoves.append((row-1, col+1))
                    elif isinstance(self.board[row-1][col + 1], Piece) and self.board[row-1][col + 1].type != SIDES[1]:
                        if row > 1:
                            if col + 2 < GRID_SIZE:
                                if not isinstance(self.board[row-2][col+2], Piece):
                                    allMoves.append((row-2, col+2))
            if piece.isKing:
                #right-forward
                i = row - 1
                j = col + 1
                byPass = False
                while(i >= 0 and j < GRID_SIZE):
                    if self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        break
                    if byPass and self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        break
                    if self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        byPass = True
                    if not isinstance(self.board[i][j], Piece):
                        allMoves.append((i,j))
                    i, j = i-1, j+1
                    

                
                #left-forward
                i = row - 1
                j = col - 1
                byPass = False
                while(i >= 0 and j >= 0):
                    if self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        break
                    if byPass and self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        break
                    if self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        byPass = True
                    if not isinstance(self.board[i][j], Piece):
                        allMoves.append((i,j))
                    i, j = i-1, j-1


                #right side forward
                i = row + 1
                j = col + 1
                byPass = False
                while(i < GRID_SIZE and j < GRID_SIZE):
                    if self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        break
                    if byPass and self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        break
                    if self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        byPass = True
                    if not isinstance(self.board[i][j], Piece):
                        allMoves.append((i,j))
                    i, j = i+1, j+1

                
                #left side forward
                i = row + 1
                j = col - 1
                byPass = False
                while(i < GRID_SIZE and j >= 0):
                    if self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        break
                    if byPass and self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        break
                    if self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        byPass = True
                    if not isinstance(self.board[i][j], Piece):
                        allMoves.append((i,j))
                    i, j = i+1, j-1


        if piece.type == SIDES[0]: #moving down
            if row + 1 < GRID_SIZE:
                #right side downward
                if col - 1 >= 0:
                    if not isinstance(self.board[row+1][col-1], Piece):
                        allMoves.append((row+1, col-1))
                    elif isinstance(self.board[row+1][col-1], Piece) and  self.board[row+1][col-1].type!=SIDES[0]:
                        if row +2 < GRID_SIZE:
                            if col -2 >= 0:
                                if not isinstance(self.board[row+2][col-2], Piece):
                                    allMoves.append((row+2, col-2))
                #left side forward
                if col + 1 < GRID_SIZE:
                    if not isinstance(self.board[row+1][col + 1], Piece):
                        allMoves.append((row+1, col+1))
                    elif isinstance(self.board[row+1][col + 1], Piece) and self.board[row+1][col + 1].type != SIDES[0]:
                        if row +2 < GRID_SIZE:
                            if col + 2 < GRID_SIZE:
                                if not isinstance(self.board[row+2][col+2], Piece):
                                    allMoves.append((row+2, col+2))
            if piece.isKing:

                #right side forward
                i = row + 1
                j = col + 1
                byPass = False
                while(i < GRID_SIZE and j < GRID_SIZE):
                    if self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        break
                    if byPass and self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        break
                    if self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        byPass = True
                    if not isinstance(self.board[i][j], Piece):
                        allMoves.append((i,j))
                    i, j = i+1, j+1

                

                #left side forward
                i = row + 1
                j = col - 1
                byPass = False
                while(i < GRID_SIZE and j >= 0):
                    if self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        break
                    if byPass and self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        break
                    if self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        byPass = True
                    if not isinstance(self.board[i][j], Piece):
                        allMoves.append((i,j))
                    i, j = i+1, j-1


                #right-forward
                i = row - 1
                j = col + 1
                byPass = False
                while(i >= 0 and j < GRID_SIZE):
                    if self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        break
                    if byPass and self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        break
                    if self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        byPass = True
                    if not isinstance(self.board[i][j], Piece):
                        allMoves.append((i,j))
                    i, j = i-1, j+1

                

                #left-forward
                i = row - 1
                j = col - 1
                byPass = False
                while(i >= 0 and j >= 0):
                    if self.board[i][j] and self.board[i][j].type == SIDES[0]:
                        break
                    if byPass and self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        break
                    if self.board[i][j] and self.board[i][j].type == SIDES[1]:
                        byPass = True
                    if not isinstance(self.board[i][j], Piece):
                        allMoves.append((i,j))
                    i, j = i-1, j-1


        return allMoves
    
    def checkBoardState(self,) -> tuple:
        players: list = []
        opponents: list = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                piece = self.board[i][j]
                if piece and isinstance(piece, Piece):
                    if piece.type == SIDES[0]:
                        players.append((i,j))
                    else:
                        opponents.append((i,j))

        if players == [] or opponents == []:
            return CHECKMATE

        noMove:bool  = True

        for i, j in players:
            if self.getPossibleMoves(i,j) != []:
                noMove = False
                break
        if noMove:
            return STALEMATE
        
        noMove = True
        for i, j in opponents:
            if self.getPossibleMoves(i,j) != []:
                noMove = False
                break
        if noMove:
            return STALEMATE

        return UNFINISHED






class UIBoard():

    def __init__(self, window):
        self.internalBoard = InternalBoard()
        self.boardToSreenMapping = []
        self.window = window
        self.boxColors = WHITE, RED

        self.init()

    def init(self, ):
        for row in range(GRID_SIZE):
            rowMap = []
            for col in range(GRID_SIZE):
                rowMap.append((WINDOW_MARGIN_X+col*BOX_SIZE + BOX_SIZE//2, WINDOW_MARGIN_Y+row*BOX_SIZE+BOX_SIZE//2))
            self.boardToSreenMapping.append(rowMap)

    def drawBoard(self, ):
        
        pygame.draw.rect(self.window, BORDER_COLOR, 
        (WINDOW_MARGIN_X - GRID_BORDER, WINDOW_MARGIN_Y - GRID_BORDER, 
        BOX_SIZE*GRID_SIZE + GRID_BORDER*2, BOX_SIZE*GRID_SIZE + GRID_BORDER*2))

        for row in range(GRID_SIZE):
            color = self.boxColors[0] if row%2 else self.boxColors[1]
            for col in range(GRID_SIZE):
                pygame.draw.rect(self.window, color, 
                (WINDOW_MARGIN_X+col*BOX_SIZE, WINDOW_MARGIN_Y+row*BOX_SIZE, BOX_SIZE, BOX_SIZE))
                color = self.boxColors[0] if color==self.boxColors[1] else self.boxColors[1]
    
    def drawPieces(self):
        pieceBorder = 4
        margin = 5
        pieceBorderColor = BLACK
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                piece = self.internalBoard.getPiece(row, col)
                if not isinstance(piece, Piece):
                    continue
                
                color = piece.type[1]
                pygame.draw.circle(self.window,BLACK, self.boardToSreenMapping[row][col], (BOX_SIZE//2 - margin)  )
                pygame.draw.circle(self.window,color, self.boardToSreenMapping[row][col], (BOX_SIZE//2 - margin-pieceBorder)  )
                if piece.isKing:
                    pygame.draw.circle(self.window,GREEN, self.boardToSreenMapping[row][col], (BOX_SIZE//2 - margin*4-pieceBorder)  )

            
    def showMoves(self, mousePosition, whoseTurn):
        x, y = mousePosition

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                pos = self.boardToSreenMapping[i][j]
                box = pygame.Rect(pos[0]-BOX_SIZE//2, pos[1]-BOX_SIZE//2,BOX_SIZE, BOX_SIZE)
                if pygame.Rect.collidepoint(box, x, y) and isinstance(self.internalBoard.getPiece(i, j), Piece):
                    if self.internalBoard.getPiece(i, j).type != whoseTurn:
                        continue
                    possibleMoves = self.internalBoard.getPossibleMoves(i,j)
                    for (row, col) in possibleMoves:
                        center = self.boardToSreenMapping[row][col]
                        centerX, centerY = center
                        alphaCirle(self.window, pygame.Color(255, 128, 0, 100), center, BOX_SIZE//2 - 10)

    def onPiece(self,mousePosition):
        x, y = mousePosition
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                pos = self.boardToSreenMapping[i][j]
                box = pygame.Rect(pos[0]-BOX_SIZE//2, pos[1]-BOX_SIZE//2,BOX_SIZE, BOX_SIZE)
                if pygame.Rect.collidepoint(box, x, y):
                    return (i, j)
        return False

    def movePieceTo(self, selectPiecePosition, mousePosition,whoseTurn):
        from_= self.onPiece(selectPiecePosition)
        to = self.onPiece(mousePosition)
        movingPiece = self.internalBoard.getPiece(*from_) 
        if not (from_ and to) or movingPiece is None:
            return None
        if movingPiece.type != whoseTurn:
            return False
        return self.internalBoard.movePiece(from_, to)
    
    def computerMove(self, whoseTurn, isAI = False):
        if isAI:
            print("Minimax Algorithmn not implemented yet!!")
        #get all players with on `whoseTurn` side, choose a random player
        #and choose a random spot to play at
        myPawnsPositions = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                piece = self.internalBoard.getPiece(i, j)
                if piece and piece.type==whoseTurn and self.internalBoard.getPossibleMoves(i,j):
                    myPawnsPositions.append((i,j))
        #will be handled in a game checker
        if len(myPawnsPositions)==0: return
        randomPosition = random.choice(myPawnsPositions)
        randomPositionTo= random.choice(self.internalBoard.getPossibleMoves(*randomPosition))
       
        return self.internalBoard.movePiece(randomPosition, randomPositionTo)

    def checkBoardState(self, opponent):
        state = self.internalBoard.checkBoardState()
        if state== UNFINISHED:
            return False
        
        color = (YELLOW if state == STALEMATE else GREEN)
       
        surface = font.render(state, 1, color)
        return surface

    def updateUI(self):
        self.drawBoard()
        self.drawPieces()

#[GAME LOOP]
def alphaCirle(surf, color, center, r):
    re = pygame.Rect(center, (0, 0)).inflate(r*2, r*2)
    s = pygame.Surface(re.size, pygame.SRCALPHA)
    pygame.draw.circle(s, color, (r,r), r)
    surf.blit(s, re)

#ex: alphaCirle(self.window, pygame.Color(0, 255, 0, 50), (WINDOW_MARGIN_X+col*BOX_SIZE + BOX_SIZE//2, WINDOW_MARGIN_Y+row*BOX_SIZE+BOX_SIZE//2),(BOX_SIZE//2 - margin))

def runGame():

    clock = pygame.time.Clock()
    running = True

    gameBoard = UIBoard(WINDOW)

    pieceSelected = False
    clickPosition = None
    selectedPiecePosition = None
    whoseTurn = SIDES[1]

    conclusion = None

    PLAYER_ONE = whoseTurn
    PLAYER_TWO = SIDES[0]

    OPPONENT = COMPUTER_RANDOM

    timeDelta = 0

    while running:

        clock.tick(FPS)
        WINDOW.fill(BACKGROUND_COLOR)

        mousePosition = pygame.mouse.get_pos()
        moved = False
        
        conclusion = gameBoard.checkBoardState(OPPONENT)
        if conclusion:
            running = False 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    pieceSelected = True #not pieceSelected
                    clickPosition = event.pos
                    # if pieceSelected:
                    #     #SELECT.play()
                    #     selectedPiecePosition = event.pos
                    # clickPosition = event.pos

                    # if gameBoard.onPiece(mousePosition) and not pieceSelected:
                    #     moved = gameBoard.movePieceTo(selectedPiecePosition,  clickPosition, whoseTurn)
                    #     print(moved)
                    #     if moved:
                    #         PLAY.play()
                    #         whoseTurn = SIDES[0] if whoseTurn == SIDES[1] else SIDES[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if pieceSelected:
                        pieceSelected = False
                        selectedPiecePosition = event.pos
                        if gameBoard.onPiece(selectedPiecePosition ):
                            #moved = gameBoard.movePieceTo(selectedPiecePosition,  clickPosition, whoseTurn)
                            
                            if whoseTurn == PLAYER_ONE:
                                moved = gameBoard.movePieceTo(clickPosition,selectedPiecePosition , whoseTurn)
        if whoseTurn == PLAYER_TWO:
            if OPPONENT == HUMAN:
                moved = gameBoard.movePieceTo(clickPosition,selectedPiecePosition , whoseTurn)
            elif time.time() - timeDelta > IMPRESSION_TIME:
                isAI = OPPONENT == COMPUTER_AI
                moved = gameBoard.computerMove(whoseTurn, isAI)
        
        if moved:
            PLAY.play()
            timeDelta = time.time()
            whoseTurn = SIDES[0] if whoseTurn == SIDES[1] else SIDES[1]



        gameBoard.updateUI()
            
        if not pieceSelected:
           gameBoard.showMoves(mousePosition, whoseTurn)
        else:
            gameBoard.showMoves(clickPosition, whoseTurn)

        pygame.display.update()
    
    if conclusion:
        pygame.mixer.music.stop()
        GAME_END.play()
        pygame.draw.rect(WINDOW, WHITE, conclusion.get_rect().move(int(WINDOW_MARGIN_X*1.2), WINDOW_HEIGHT//2-60))
        WINDOW.blit(conclusion, (int(WINDOW_MARGIN_X*1.2), WINDOW_HEIGHT//2-60))
        pygame.display.update()
        pygame.time.wait(int(8000))
    pygame.time.wait(int(1000))
    print(conclusion)
    pygame.quit()