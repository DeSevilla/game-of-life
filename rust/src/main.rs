use std::collections::{HashSet, HashMap};

struct Life {
    board: HashSet<(i64, i64)>
}

impl Life {
    fn step(&mut self) {
        let mut counts: HashMap<(i64, i64), i8> = HashMap::new();
        for &(x, y) in &self.board {
            for i in -1..=1 {
                for j in -1..=1 {
                    if i != 0 || j != 0 {
                        let count = counts.entry((x+i, y+j)).or_insert(0);
                        *count += 1;
                    }
                }
            }
        }
        for (loc, &live) in &counts {
            if live == 3 {
                self.board.insert(*loc);
            } else if live != 2 && self.board.contains(loc) {
                self.board.remove(loc);
            }
        }
    }

    fn print_board(&self) {
        let mut min_x = std::i64::MAX;
        let mut max_x = std::i64::MIN;
        let mut min_y = std::i64::MAX;
        let mut max_y = std::i64::MIN;
        for &(x, y) in &self.board {
            if x < min_x {
                min_x = x;
            } else if x > max_x {
                max_x = x;
            }
            if y < min_y {
                min_y = y;
            } else if y > max_y {
                max_y = y;
            }
        }
        for y in min_y..max_y+1 {
            for x in min_x..max_x+1 {
                let disp = if self.board.contains(&(x, y)) {
                    'X'
                } else {
                    '.' 
                };
                print!("{disp} ");
            }
            println!("");
        }
    }
}

fn main() {
    let mut starting_board = HashSet::new();
    starting_board.insert((0, 0));
    starting_board.insert((0, 1));
    starting_board.insert((0, 2));
    starting_board.insert((1, 2));
    starting_board.insert((-1, 1));
    // starting_board.insert((0, 2));
    // starting_board.insert((1, 2));
    // starting_board.insert((2, 1));
    // starting_board.insert((2, 2));
    // starting_board.insert((1, 0));
    let mut gol = Life {
        board: starting_board
    };
    gol.print_board();
    println!("______");
    for _ in 0..20 {
        gol.step();
        gol.step();
        gol.step();
        gol.step();
        gol.step();
        gol.print_board();
        println!("");
    }
}
