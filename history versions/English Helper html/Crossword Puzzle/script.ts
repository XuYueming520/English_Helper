const version = "0.0.0";
const build = "2024.6.15";
const author = "XuYueming";

var rand = function () {
    var seed = 736520 | 0x7365200001314;
    function rand() {
        seed ^= seed >> 10;
        seed ^= seed << 9;
        seed ^= seed >> 25;
        return seed;
    }
    
    /**
     * @description generate random number between l and r (both inclusive)
     * @param {Number} l - lower bound
     * @param {Number} r - upper bound
     * @returns {Number} - random number
     */
    return function (l = 1, r = 5201314) {
        if (l > r) return 0;
        return rand() % (r - l + 1) + l;
    }
} ();

const WHITE = 1, HIDE = 2, WORD = 3;

type dirc_t = number;  // gfdfdgfdgdgfdgfdgfdgfdgfgf
type type_t = number;  // gfdfdgfdgdgfdgfdgfdgfdgfgf
type ptd_t = number;  // gfdfdgfdgdgfdgfdgfdgfdgfgf

class Word {
    type: type_t;
    word: String;
    dirc: dirc_t;
    ptd:  ptd_t;
    multi: boolean;
    
    /**
     * @param {type_t} tp - type of the word, should be WHITE, HIDE, WORD
     * @param {String} word - the character
     * @param {dirc_t} dirc - the direction of the word: 0b10 -> in row, 0b01 -> in column
     * @param {ptd_t} ptd - is the endpoint of the word? 0b0000 no, 0b0001 right-pt, 0b0010 left-pt, 0b0100 bottom-pt, 0b1000 top-pt
     * @param {Boolean} multi - big-letter and small-letter both exist?
     */
    constructor (tp: type_t, word: string = ' ', dirc: dirc_t = 0b00, ptd: ptd_t = 0b0000, multi: boolean = false) {
        this.type = tp;
        this.word = word;
        this.dirc = dirc;
        this.ptd = ptd;
        this.multi = multi;
    }
    
    /**
     * @description is thw word in a row?
     */
    inrow() {
        return Boolean(this.dirc & 0b10);
    }
    
    /**
     * @description is thw word in a column?
     */
    incol() {
        return Boolean(this.dirc & 0b01);
    }
    
    /**
     * @description is the endpoint of the word on the left?
     */
    faceleft() {
        return Boolean(this.ptd & 0b0001);
    }
    
    /**
     * @description is the endpoint of the word on the right?
     */
    faceright() {
        return Boolean(this.ptd & 0b0010);
    }
    
    /**
     * @description is the endpoint of the word on the top?
     */
    faceup() {
        return Boolean(this.ptd & 0b0100);
    }
    
    /**
     * @description is the endpoint of the word on the bottom?
     */
    facedown() {
        return Boolean(this.ptd & 0b1000);
    }
}

/**
 * @description English Crossword Puzzle maker
 * @author XuYueming
*/
class Crossword_puzzle_maker {
    row: number;
    col: number;
    list: Array<any>; // dsads
    puzzle: Array<Array<Word>>;
    prompt: any;  //
    
    /**
     * @param {number} row - number of rows in the puzzle
     * @param {number} col - number of columns in the puzzle
    */
    constructor (row = 13, col = 13) {
        this.row = row;
        this.col = col;
        this.list = [];
        this.puzzle = [];
        this.prompt = [{}, {}];
        
        for (var i = 0; i < row; ++i)
        for (var j = 0; j < col; ++j)
            this.puzzle[i][j] = new Word(WHITE);
    }
    
    /**
     * Generate the puzzle
     * @param {Boolean} must_cross the puzzle must have cross
     * @param {Number} max_remain the max num of the left words
     */
    make_puzzle(must_cross = true, max_remain = 0) {
        console.log(`%c Start generating the crossword puzzle (${this.list.length} words).`,
            'color: blue');
        
        var start_time = 114;
        
        /**
         * can put up a word in the puzzle
         * @param {string} word the input word
         * @param {Number} dirc the word's direction
         * @param {list[Number, Number]} pos the start point's position
         * @param {Boolean} must_cross the word must cross a word or not
         */
        function can_putup(word: string, dirc, pos, must_cross: boolean){  //////////////////
            /*
            考虑以下几种情况：
                1. 出界
                2. 单词后一个位置和前一个位置有单词
                3. 和原先同向单词相交
                4. 和原先异向单词有交叉，且不是同一个字母
                5. 两侧有没有原先异向的单词的一端
                6. 两侧有没有同向单词
            */
            var cross = false;
            
            if (dirc == 1) {
                if (pos[0] + word.length - 1 >= this.row)
                    return false;
                
                if (pos[0] + word.length != this.row && this.puzzle[pos[0] + word.length][pos[1]].type != WHITE)
                    return false;
                if (pos[0] != 0 && this.puzzle[pos[0] - 1][pos[1]].type != WHITE)
                    return false;
                
                for (let i = 0; i < word.length; ++i){
                    if (this.puzzle[pos[0] + i][pos[1]].type != WHITE){
                        if (this.puzzle[pos[0] + i][pos[1]].incol())
                            return false;
                        if (this.puzzle[pos[0] + i][pos[1]].word.lower() != word[i].lower())
                            return false;
                        cross = true;
                    }
                    if (pos[1] != 0 && this.puzzle[pos[0] + i][pos[1] - 1].type != WHITE) {
                        if (this.puzzle[pos[0] + i][pos[1] - 1].incol())
                            return false;
                        if (this.puzzle[pos[0] + i][pos[1] - 1].faceleft())
                            return false;
                    }
                    if (pos[1] != this.col - 1 && this.puzzle[pos[0] + i][pos[1] + 1].type != WHITE) {
                        if (this.puzzle[pos[0] + i][pos[1] + 1].incol())
                            return false;
                        if (this.puzzle[pos[0] + i][pos[1] + 1].faceright())
                            return false;
                    }
                }
            } else {
                if (pos[1] + word.length - 1 >= this.col)
                    return false;
                
                if (pos[1] + word.length != this.col && this.puzzle[pos[0]][pos[1] + word.length].type != WHITE)
                    return false;
                if (pos[1] != 0 && this.puzzle[pos[0]][pos[1] - 1].type != WHITE)
                    return false;
                
                for (let i = 0; i < word.length; ++i){
                    if (this.puzzle[pos[0]][pos[1] + i].type != WHITE){
                        if (this.puzzle[pos[0]][pos[1] + i].inrow())
                            return false;
                        if (this.puzzle[pos[0]][pos[1] + i].word.lower() != word[i].lower())
                            return false;
                        cross = true;
                    }
                    if (pos[0] != 0 && this.puzzle[pos[0] - 1][pos[1] + i].type != WHITE){
                        if (this.puzzle[pos[0] - 1][pos[1] + i].inrow())
                            return false;
                        if (this.puzzle[pos[0] - 1][pos[1] + i].faceup())
                            return false;
                    }
                    if (pos[0] != this.row - 1 && this.puzzle[pos[0] + 1][pos[1] + i].type != WHITE){
                        if (this.puzzle[pos[0] + 1][pos[1] + i].inrow())
                            return false;
                        if (this.puzzle[pos[0] + 1][pos[1] + i].facedown())
                            return false;
                    }
                }
            }
            
            if (must_cross && !cross) return false;
            return true;
        }
        
        // function putup(word: string, idx: int)
    }
    
};

window.onload = function() {
    console.log(`%c Crossword Puzzle maker %c V${version} `,
        'padding: 2px 1px; border-radius: 3px 0 0 3px; color: #fff; background: #606060; font-weight: bold;',
        'padding: 2px 1px; border-radius: 0 3px 3px 0; color: #fff; background: #42c02e; font-weight: bold;');
    var ver = document.getElementById("version-number"),
        bud = document.getElementById("build-time");
    if (ver !== null) ver.innerHTML = version;
    if (bud !== null) bud.innerHTML = build;
    
    var tester = new Crossword_puzzle_maker(30, 30);
    
}
