import Data.Set (Set, map, fromList, findMin, findMax, member)
import Data.List (intercalate, intersperse)

gliderBoard = fromList [(0, 2), (1, 2), (2, 2), (2, 1), (1, 0), 
                        (10, 10), (10, 11), (11, 10), (11, 11),
                        (-10, -10), (-10, -11), (-11, -10), (-11, -11)]
glider = fromList [(0, 2), (1, 2), (2, 2), (2, 1), (1, 0)]
pentomino = fromList [(0, 0), (0, 1), (0, 2), (1, 2), (-1, 1)]

neighbors (x, y) = [(x+dx, y+dy) | dx <- [-1, 0, 1], dy <- [-1, 0, 1], dx /= 0 || dy /= 0]

-- >>> neighbors (0, 0)
-- [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
-- >>> neighbors (10, 10)
-- [(9,9),(9,10),(9,11),(10,9),(10,11),(11,9),(11,10),(11,11)]

liveNeighbors board (x, y) = length [n | n <- neighbors (x, y), member n board]

-- >>> liveNeighbors gliderBoard (10, 10)
-- 3

step board = Data.Set.fromList [p | p <- concatMap neighbors board, liveNeighbors board p == 3 || (member p board && liveNeighbors board p == 2)]

run board 0 = board
run board n = step (run board (n-1))

showLive :: Set (Integer, Integer) -> [Char]
showLive board = intercalate "\n" [intersperse ' ' [if member (x, y) board then 'X' else '.' | x <- [minX..maxX]] | y <- [minY..maxY]]
    where maxX = findMax (Data.Set.map fst board)
          maxY = findMax (Data.Set.map snd board)
          minX = findMin (Data.Set.map fst board)
          minY = findMin (Data.Set.map snd board)

showWindow (minX, maxX) (minY, maxY) board = intercalate "\n" 
    [intersperse ' ' 
        [if member (x, y) board then 'X' else '.' | x <- [minX..maxX]] | y <- [minY..maxY]]


displayLive = putStrLn . showLive

displayWindow xRange yRange = putStrLn . showWindow xRange yRange

runLive 0 board = displayLive board
runLive n board = displayLive board >> putStrLn "" >> runLive (n - 1) (step board)

runWindow xRange yRange 0 board = displayWindow xRange yRange board
runWindow xRange yRange n board = displayWindow xRange yRange board >> putStrLn "" >> runWindow xRange yRange (n-1) (step board) 

main = runWindow (-20, 20) (-20, 20) 150 pentomino
