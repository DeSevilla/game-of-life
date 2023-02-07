import Data.Map ( Map, empty, foldrWithKey, insertWith, filterWithKey, member, fromList, keys )
import Data.List ( intercalate, intersperse )
import Data.Char (ord)
import System.Environment ( getArgs )

type Point = (Int, Int)
type Board = Map Point Int

neighbors :: Point -> [Point]
neighbors (x, y) = [(x+dx, y+dy) | dx <- [-1..1], dy <-[-1..1], dx /= 0 || dy /= 0]

incrementNeighbors :: Point -> Int -> Board -> Board
incrementNeighbors p _ board = foldr (\x -> insertWith (+) x 1) board (neighbors p)

countLiveNeighbors :: Board -> Board
countLiveNeighbors = foldrWithKey incrementNeighbors empty

liveNext :: Board -> Point -> Int -> Bool
liveNext board p live = live == 3 || p `member` board && live == 2

step :: Board -> Board
step board = filterWithKey (liveNext board) (countLiveNeighbors board)

run :: Board -> Int -> Board
run board 0 = board
run board n = run (step board) (n-1)

showLive :: Board -> String
showLive board = intercalate "\n" [[if member (x, y) board then 'X' else '.' | x <- [minX..maxX]] | y <- [minY..maxY]]
    where maxX = maximum (map fst (keys board))
          maxY = maximum (map snd (keys board))
          minX = minimum (map fst (keys board))
          minY = minimum (map snd (keys board))

makeBoard :: [Point] -> Board
makeBoard ps = fromList (zip ps [0,0..])

stringToPoints :: String -> [Point]
stringToPoints (x:y:xs) = (ord x, ord y):stringToPoints xs
stringToPoints [x] = [(ord x, 0)]
stringToPoints [] = []

main :: IO ()
main = do
    args <- getArgs
    contents <- readFile (head args)
    let board = makeBoard $ stringToPoints contents
    putStrLn $ showLive board
    putStrLn "<><><><><><><><><><><><><><><><><><><><><><><>"
    putStrLn $ showLive $ run board 100
