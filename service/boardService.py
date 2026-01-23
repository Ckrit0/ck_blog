def shortTitle(boardTitle):
        if len(boardTitle) > 15:
            boardTitle = boardTitle[0:15] + '...'
        return boardTitle