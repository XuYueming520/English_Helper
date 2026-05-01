const version = "1.0.0";
const build = "2026.05.01";
const GENERATION_TIMEOUT_MS = 3000;

const WHITE = 1;
const HIDE = 2;
const WORD = 3;

class WordCell {
    constructor(tp, word = " ", dirc = 0b00, ptd = 0b0000, multi = false) {
        this.type = tp;
        this.word = word;
        this.dirc = dirc;
        this.ptd = ptd;
        this.multi = multi;
    }

    inrow() {
        return Boolean(this.dirc & 0b10);
    }

    incol() {
        return Boolean(this.dirc & 0b01);
    }

    faceleft() {
        return Boolean(this.ptd & 0b0001);
    }

    faceright() {
        return Boolean(this.ptd & 0b0010);
    }

    faceup() {
        return Boolean(this.ptd & 0b0100);
    }

    facedown() {
        return Boolean(this.ptd & 0b1000);
    }
}

class CrosswordPuzzleMaker {
    constructor(row = 30, col = 30, entries = []) {
        this.row = row;
        this.col = col;
        this.originalEntries = entries.map((entry) => ({ ...entry }));
        this.entries = entries.map((entry) => ({ ...entry }));
        this.usedEntries = [];
        this.puzzle = [];
        this.prompt = [{}, {}];
        this.resetGrid();
    }

    resetGrid() {
        this.puzzle = Array.from({ length: this.row }, () =>
            Array.from({ length: this.col }, () => new WordCell(WHITE))
        );
        this.prompt = [{}, {}];
        this.usedEntries = [];
        this.placedWords = [];
    }

    cloneCell(cell) {
        return new WordCell(cell.type, cell.word, cell.dirc, cell.ptd, cell.multi);
    }

    cloneCells(cells) {
        return cells.map((cell) => this.cloneCell(cell));
    }

    normalizeClue(word, clue) {
        const upperWord = word.toUpperCase();
        const replaced = Array.from(clue.toUpperCase().replaceAll(upperWord, "_".repeat(word.length)).toLowerCase());
        for (let i = 0; i < replaced.length; i += 1) {
            if (clue[i] && clue[i] === clue[i].toUpperCase() && clue[i] !== clue[i].toLowerCase()) {
                replaced[i] = replaced[i].toUpperCase();
            }
        }
        return replaced.join("");
    }

    canPutUp(word, dirc, pos, mustCross) {
        let cross = false;

        if (dirc === 1) {
            if (pos[0] + word.length - 1 >= this.row) {
                return false;
            }
            if (pos[0] + word.length !== this.row && this.puzzle[pos[0] + word.length][pos[1]].type !== WHITE) {
                return false;
            }
            if (pos[0] !== 0 && this.puzzle[pos[0] - 1][pos[1]].type !== WHITE) {
                return false;
            }

            for (let i = 0; i < word.length; i += 1) {
                const current = this.puzzle[pos[0] + i][pos[1]];
                if (current.type !== WHITE) {
                    if (current.incol()) {
                        return false;
                    }
                    if (current.word.toLowerCase().charAt(0) !== word[i].toLowerCase()) {
                        return false;
                    }
                    cross = true;
                }
                if (pos[1] !== 0) {
                    const left = this.puzzle[pos[0] + i][pos[1] - 1];
                    if (left.type !== WHITE && (left.incol() || left.faceleft())) {
                        return false;
                    }
                }
                if (pos[1] !== this.col - 1) {
                    const right = this.puzzle[pos[0] + i][pos[1] + 1];
                    if (right.type !== WHITE && (right.incol() || right.faceright())) {
                        return false;
                    }
                }
            }
        } else {
            if (pos[1] + word.length - 1 >= this.col) {
                return false;
            }
            if (pos[1] + word.length !== this.col && this.puzzle[pos[0]][pos[1] + word.length].type !== WHITE) {
                return false;
            }
            if (pos[1] !== 0 && this.puzzle[pos[0]][pos[1] - 1].type !== WHITE) {
                return false;
            }

            for (let i = 0; i < word.length; i += 1) {
                const current = this.puzzle[pos[0]][pos[1] + i];
                if (current.type !== WHITE) {
                    if (current.inrow()) {
                        return false;
                    }
                    if (current.word.toLowerCase().charAt(0) !== word[i].toLowerCase()) {
                        return false;
                    }
                    cross = true;
                }
                if (pos[0] !== 0) {
                    const up = this.puzzle[pos[0] - 1][pos[1] + i];
                    if (up.type !== WHITE && (up.inrow() || up.faceup())) {
                        return false;
                    }
                }
                if (pos[0] !== this.row - 1) {
                    const down = this.puzzle[pos[0] + 1][pos[1] + i];
                    if (down.type !== WHITE && (down.inrow() || down.facedown())) {
                        return false;
                    }
                }
            }
        }

        if (mustCross && !cross) {
            return false;
        }
        return true;
    }

    putUp(word, clue, dirc, pos) {
        const normalizedClue = this.normalizeClue(word, clue);
        const cells = [];
        if (dirc === 1) {
            this.puzzle[pos[0]][pos[1]].ptd |= 0b1000;
            this.puzzle[pos[0] + word.length - 1][pos[1]].ptd |= 0b0100;
            if (!this.prompt[1][pos[1]]) {
                this.prompt[1][pos[1]] = [];
            }
            this.prompt[1][pos[1]].push(normalizedClue);

            for (let i = 0; i < word.length; i += 1) {
                const cell = this.puzzle[pos[0] + i][pos[1]];
                cells.push([pos[0] + i, pos[1]]);
                if (cell.type === WHITE) {
                    cell.type = HIDE;
                    cell.word = word[i];
                } else {
                    cell.type = WORD;
                    if (cell.word !== word[i]) {
                        cell.multi = true;
                        cell.word = `${word[i].toUpperCase()}/${word[i].toLowerCase()}`;
                    } else {
                        cell.word = word[i];
                    }
                }
                cell.dirc |= 0b01;
            }
        } else {
            this.puzzle[pos[0]][pos[1]].ptd |= 0b0010;
            this.puzzle[pos[0]][pos[1] + word.length - 1].ptd |= 0b0001;
            if (!this.prompt[0][pos[0]]) {
                this.prompt[0][pos[0]] = [];
            }
            this.prompt[0][pos[0]].push(normalizedClue);

            for (let i = 0; i < word.length; i += 1) {
                const cell = this.puzzle[pos[0]][pos[1] + i];
                cells.push([pos[0], pos[1] + i]);
                if (cell.type === WHITE) {
                    cell.type = HIDE;
                    cell.word = word[i];
                } else {
                    cell.type = WORD;
                    if (cell.word !== word[i]) {
                        cell.multi = true;
                        cell.word = `${word[i].toUpperCase()}/${word[i].toLowerCase()}`;
                    } else {
                        cell.word = word[i];
                    }
                }
                cell.dirc |= 0b10;
            }
        }

        this.placedWords.push({
            word,
            clue: normalizedClue,
            direction: dirc === 1 ? "column" : "row",
            start: [pos[0], pos[1]],
            cells
        });
        this.usedEntries.push({ word, clue });
    }

    async makePuzzle(mustCross = true, maxRemain = 0, timeoutMs = GENERATION_TIMEOUT_MS) {
        this.entries = this.originalEntries.map((entry) => ({ ...entry }));
        this.resetGrid();
        const startedAt = Date.now();
        let timedOut = false;
        let stepCounter = 0;

        const yieldControl = async () => new Promise((resolve) => {
            window.setTimeout(resolve, 0);
        });

        const generatePuzzle = async (firstRun = true) => {
            if (Date.now() - startedAt > timeoutMs) {
                timedOut = true;
                return false;
            }
            if (this.entries.length <= maxRemain) {
                return true;
            }

            for (let now = 0; now < this.entries.length; now += 1) {
                const entry = this.entries[now];
                for (let i = 0; i < this.row; i += 1) {
                    for (let j = 0; j < this.col; j += 1) {
                        for (let d = 0; d < 2; d += 1) {
                            stepCounter += 1;
                            if (stepCounter % 2048 === 0) {
                                await yieldControl();
                            }
                            if (!this.canPutUp(entry.word, d, [i, j], firstRun ? false : mustCross)) {
                                continue;
                            }

                            let saver;
                            if (d === 1) {
                                saver = this.cloneCells(Array.from({ length: entry.word.length }, (_, offset) => this.puzzle[i + offset][j]));
                            } else {
                                saver = this.cloneCells(this.puzzle[i].slice(j, j + entry.word.length));
                            }

                            this.putUp(entry.word, entry.clue, d, [i, j]);
                            const removed = this.entries.splice(now, 1)[0];

                            if (await generatePuzzle(false)) {
                                return true;
                            }

                            this.entries.splice(now, 0, removed);
                            this.usedEntries.pop();
                            this.placedWords.pop();

                            if (d === 1) {
                                this.prompt[1][j].pop();
                                if (this.prompt[1][j].length === 0) {
                                    delete this.prompt[1][j];
                                }
                                for (let t = 0; t < saver.length; t += 1) {
                                    this.puzzle[i + t][j] = this.cloneCell(saver[t]);
                                }
                            } else {
                                this.prompt[0][i].pop();
                                if (this.prompt[0][i].length === 0) {
                                    delete this.prompt[0][i];
                                }
                                for (let t = 0; t < saver.length; t += 1) {
                                    this.puzzle[i][j + t] = this.cloneCell(saver[t]);
                                }
                            }

                            if (timedOut) {
                                return false;
                            }
                        }
                    }
                }
            }

            return false;
        };

        const success = await generatePuzzle(true);
        if (!success) {
            return {
                success: false,
                timedOut,
                elapsedMs: Date.now() - startedAt,
                usedEntries: [],
                remainingEntries: this.entries.map((entry) => ({ ...entry })),
                prompt: [{}, {}],
                solved: [],
                puzzle: [],
                placements: []
            };
        }

        this.prompt[0] = Object.fromEntries(Object.entries(this.prompt[0]).sort((a, b) => Number(a[0]) - Number(b[0])));
        this.prompt[1] = Object.fromEntries(Object.entries(this.prompt[1]).sort((a, b) => Number(a[0]) - Number(b[0])));

        const solved = this.puzzle.map((row) =>
            row.map((cell) => {
                if (cell.type === WHITE) {
                    return "";
                }
                return cell.word.charAt(0);
            })
        );

        const hidden = this.puzzle.map((row) =>
            row.map((cell) => {
                if (cell.type === WHITE) {
                    return "";
                }
                if (cell.type === HIDE) {
                    return "";
                }
                return cell.word.charAt(0);
            })
        );

        return {
            success: true,
            timedOut: false,
            elapsedMs: Date.now() - startedAt,
            usedEntries: this.usedEntries.map((entry) => ({ ...entry })),
            remainingEntries: this.entries.map((entry) => ({ ...entry })),
            prompt: this.prompt,
            solved,
            puzzle: hidden,
            cells: this.puzzle,
            placements: this.placedWords.map((placement) => ({
                word: placement.word,
                clue: placement.clue,
                direction: placement.direction,
                start: [...placement.start],
                cells: placement.cells.map((cellPos) => [...cellPos])
            }))
        };
    }
}

const sampleEntries = [
    { word: "baby", clue: "I have a baby brother." },
    { word: "book", clue: "I read lots of books yesterday." },
    { word: "bring", clue: "But bring an umbrella with you, it is rainy outside." },
    { word: "build", clue: "Look! There are some buildings." },
    { word: "calm", clue: "Calm down! Don't be angry!" },
    { word: "capital", clue: "Beijing is the capital of China." },
    { word: "celebrate", clue: "He cannot return home to celebrate her birthday." },
    { word: "conversion", clue: "These are good ways to start a conversion." },
    { word: "dear", clue: "I love you! My dear!" },
    { word: "die", clue: "You are going to die!" },
    { word: "do", clue: "I'm doing homework." },
    { word: "especially", clue: "It is especially famous for its university." },
    { word: "excellent", clue: "Excellent! I agree with you." },
    { word: "favorite", clue: "My favorite color is white." },
    { word: "feast", clue: "It's a big feast of rock and pop music." },
    { word: "fever", clue: "You are having a fever!" },
    { word: "fire", clue: "Fire is very dangerous!" },
    { word: "forty", clue: "There are forty students in my class." },
    { word: "has", clue: "He has two eyes." },
    { word: "hello", clue: "Hello world!" },
    { word: "island", clue: "He found the boat near the island." },
    { word: "language", clue: "English and Esperanto are languages." },
    { word: "lesson", clue: "Try to do something they didn't do before the lesson." },
    { word: "let", clue: "She let students think." },
    { word: "love", clue: "I always love you!" },
    { word: "lover", clue: "We're lovers." },
    { word: "March", clue: "Today is March 1st!" },
    { word: "monitor", clue: "I want to run for the class monitor." },
    { word: "most", clue: "You will need it most days." },
    { word: "motorcycle", clue: "Look! A man is riding a motorcycle behind you!" },
    { word: "natural", clue: "It is natural to forget new words." },
    { word: "newspaper", clue: "I'm going to buy a newspaper." },
    { word: "photo", clue: "There's a photo." },
    { word: "popular", clue: "Do you know the popular song?" },
    { word: "population", clue: "That is larger than the population of many other cities in China." },
    { word: "prefer", clue: "I prefer slow music because I think it's good for my study." },
    { word: "promise", clue: "I promise to help you!" },
    { word: "sorry", clue: "Sorry? Can you say that again?" },
    { word: "successful", clue: "He was very successful." },
    { word: "suggest", clue: "I suggest you should do homework right now." },
    { word: "telephone", clue: "What's your telephone number?" },
    { word: "theater", clue: "He's the manager of a theater." },
    { word: "through", clue: "I get to know a lot about the world through reading." },
    { word: "unreal", clue: "Computer games are unreal!" },
    { word: "used", clue: "I used to study hard." },
    { word: "vocabulary", clue: "The third question is about vocabulary." },
    { word: "Wednesday", clue: "Today is Wednesday." },
    { word: "well", clue: "I can get on well with everyone." },
    { word: "work", clue: "My favorite writer is Mark Twain for his well-known work The Prince and The Pauper." },
    { word: "writer", clue: "Mark Twain was a famous writer in America." },
    { word: "young", clue: "He was the class monitor in class when he was young." },
    { word: "XuYueming", clue: "My name is XuYueming" },
    { word: "YZH", clue: "YZH is so cute!" },
    { word: "are", clue: "Are you OK?!" },
    { word: "beach", clue: "Little Pig Beach is a very famous cartoon." },
    { word: "crossword", clue: "This a generator of crossword puzzle." },
    { word: "China", clue: "We are in China." },
    { word: "fall", clue: "I'm falling love with you." },
    { word: "flower", clue: "I love flowers." },
    { word: "good", clue: "Good job! You did well." },
    { word: "happy", clue: "Happy birthday!" },
    { word: "help", clue: "I need your help." },
    { word: "house", clue: "I live in a small house." },
    { word: "man", clue: "Man and woman are friends." },
    { word: "music", clue: "I like listening to music." },
];

let lastResult = null;
let showAnswer = false;
let entriesCollapsed = false;
const gridHoverState = {
    highlightedCells: [],
    tooltip: null
};
const INPUT_DEFAULTS = {
    rows: { min: 5, max: 40, value: 30 },
    cols: { min: 5, max: 40, value: 30 },
    maxRemain: { min: 0, max: 20, value: 0 },
    seed: "12345",
    autoSeed: true,
    mustCross: true
};

function seedToUint32(seedText) {
    let hashed = 2166136261;
    for (let i = 0; i < seedText.length; i += 1) {
        hashed ^= seedText.charCodeAt(i);
        hashed = Math.imul(hashed, 16777619);
    }
    return (hashed >>> 0) || 1;
}

function createXorRandom(seed) {
    let state = seed >>> 0;
    if (state === 0) {
        state = 1;
    }
    return () => {
        state ^= state << 13;
        state ^= state >>> 17;
        state ^= state << 5;
        return (state >>> 0) / 4294967296;
    };
}

function shuffledEntriesWithSeed(entries, seedText) {
    const shuffled = entries.map((entry) => ({ ...entry }));
    const random = createXorRandom(seedToUint32(seedText));
    for (let i = shuffled.length - 1; i > 0; i -= 1) {
        const j = Math.floor(random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

function createRandomSeedText() {
    const randomPart = Math.floor(Math.random() * 4294967296).toString(36);
    return `${Date.now().toString(36)}-${randomPart}`.toUpperCase();
}

function applyAutoSeedState() {
    const autoSeedInput = byId("auto-seed-input");
    const seedInput = byId("seed-input");
    if (autoSeedInput.checked) {
        seedInput.value = createRandomSeedText();
        seedInput.readOnly = true;
    } else {
        seedInput.readOnly = false;
    }
}

function byId(id) {
    const element = document.getElementById(id);
    if (!element) {
        throw new Error(`Missing required element: ${id}`);
    }
    return element;
}

function getOrCreateClueTooltip() {
    if (!gridHoverState.tooltip) {
        const tooltip = document.createElement("div");
        tooltip.className = "clue-tooltip hidden";
        document.body.appendChild(tooltip);
        gridHoverState.tooltip = tooltip;
    }
    return gridHoverState.tooltip;
}

function clearGridHover() {
    gridHoverState.highlightedCells.forEach((cell) => {
        cell.classList.remove("cell-hover-highlight");
    });
    gridHoverState.highlightedCells = [];
    if (gridHoverState.tooltip) {
        gridHoverState.tooltip.classList.add("hidden");
        gridHoverState.tooltip.textContent = "";
    }
}

function cellKey(row, col) {
    return `${row},${col}`;
}

function buildPlacementLookup(placements) {
    const lookup = new Map();
    placements.forEach((placement, placementIndex) => {
        placement.cells.forEach(([row, col]) => {
            const key = cellKey(row, col);
            if (!lookup.has(key)) {
                lookup.set(key, []);
            }
            lookup.get(key).push(placementIndex);
        });
    });
    return lookup;
}

function formatPlacementClue(placement) {
    const [row, col] = placement.start;
    if (placement.direction === "row") {
        return `Row ${row + 1}: ${placement.clue}`;
    }
    return `Column ${col + 1}: ${placement.clue}`;
}

function showClueTooltip(placements, mouseEvent) {
    const tooltip = getOrCreateClueTooltip();
    tooltip.innerHTML = placements.map((placement) =>
        `<div class="clue-tooltip-line">${formatPlacementClue(placement)}</div>`
    ).join("");
    tooltip.classList.remove("hidden");
    positionClueTooltip(mouseEvent);
}

function positionClueTooltip(mouseEvent) {
    if (!gridHoverState.tooltip || gridHoverState.tooltip.classList.contains("hidden")) {
        return;
    }
    gridHoverState.tooltip.style.left = `${mouseEvent.clientX + 14}px`;
    gridHoverState.tooltip.style.top = `${mouseEvent.clientY + 14}px`;
}

function setStatus(message, type = "") {
    const status = byId("status-message");
    status.textContent = message;
    status.className = "status-message";
    if (type) {
        status.classList.add(type);
    }
}

function setControlsDisabled(disabled) {
    const controlsPanel = document.querySelector(".controls-panel");
    if (!controlsPanel) {
        return;
    }
    const interactiveElements = controlsPanel.querySelectorAll("input, textarea, button");
    interactiveElements.forEach((element) => {
        element.disabled = disabled;
    });
}

function updateEntriesCollapsedUi() {
    const entriesTable = byId("entries-table");
    const toggleButton = byId("toggle-entries-visibility-button");
    entriesTable.classList.toggle("is-collapsed", entriesCollapsed);
    toggleButton.textContent = entriesCollapsed ? "Expand" : "Collapse";
}

function toggleEntriesCollapsed() {
    entriesCollapsed = !entriesCollapsed;
    updateEntriesCollapsedUi();
}

function createEntryRow(entry = { word: "", clue: "" }) {
    const tbody = byId("entries-body");
    const tr = document.createElement("tr");

    const wordCell = document.createElement("td");
    const wordInput = document.createElement("input");
    wordInput.type = "text";
    wordInput.value = entry.word;
    wordInput.placeholder = "word";
    wordInput.className = "entry-word";
    wordCell.appendChild(wordInput);

    const clueCell = document.createElement("td");
    const clueInput = document.createElement("textarea");
    clueInput.value = entry.clue;
    clueInput.placeholder = "Clue sentence containing the answer word";
    clueInput.className = "entry-clue";
    clueCell.appendChild(clueInput);

    const actionCell = document.createElement("td");
    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.textContent = "Remove";
    removeButton.className = "entry-remove-button";
    removeButton.addEventListener("click", () => {
        tr.remove();
    });
    actionCell.appendChild(removeButton);

    tr.appendChild(wordCell);
    tr.appendChild(clueCell);
    tr.appendChild(actionCell);
    tbody.appendChild(tr);
}

function loadSampleEntries() {
    const tbody = byId("entries-body");
    tbody.innerHTML = "";
    sampleEntries.forEach((entry) => createEntryRow(entry));
}

function collectEntries() {
    const rows = Array.from(byId("entries-body").querySelectorAll("tr"));
    const entries = [];
    const seen = new Set();

    for (const row of rows) {
        const wordInput = row.querySelector(".entry-word");
        const clueInput = row.querySelector(".entry-clue");
        if (!wordInput || !clueInput) {
            continue;
        }
        const word = wordInput.value.trim();
        const clue = clueInput.value.trim().replace(/\s+/g, " ");

        if (!word && !clue) {
            continue;
        }
        if (!word || !clue) {
            throw new Error("Each filled row needs both a word and a clue sentence.");
        }
        if (word.length <= 1) {
            throw new Error(`"${word}" is too short. Words must be at least 2 letters.`);
        }
        const normalizedWord = word.replace(/\s+/g, "");
        const key = normalizedWord.toLowerCase();
        if (seen.has(key)) {
            throw new Error(`"${normalizedWord}" is duplicated. Each word must be unique.`);
        }
        seen.add(key);
        entries.push({ word: normalizedWord, clue });
    }

    if (entries.length === 0) {
        throw new Error("Add at least one word before generating a puzzle.");
    }

    return entries;
}

function renderPrompts(promptMap, targetId, label) {
    const target = byId(targetId);
    target.innerHTML = "";
    const keys = Object.keys(promptMap);
    if (keys.length === 0) {
        const li = document.createElement("li");
        li.textContent = `No ${label.toLowerCase()} clues yet.`;
        target.appendChild(li);
        return;
    }

    keys.forEach((key) => {
        const li = document.createElement("li");
        const title = document.createElement("span");
        title.className = "prompt-label";
        title.textContent = `${label} ${Number(key) + 1}: `;
        li.appendChild(title);
        li.append(document.createTextNode(promptMap[key].join(" | ")));
        target.appendChild(li);
    });
}

function renderGrid(result) {
    const wrapper = byId("puzzle-wrapper");
    clearGridHover();
    wrapper.innerHTML = "";

    if (!result || !result.success) {
        return;
    }

    const table = document.createElement("table");
    table.className = "puzzle-grid";
    const grid = showAnswer ? result.solved : result.puzzle;
    const placementLookup = buildPlacementLookup(result.placements || []);
    const cellElementMap = new Map();

    const handleCellHover = (row, col, mouseEvent) => {
        const placementIndexes = placementLookup.get(cellKey(row, col)) || [];
        if (placementIndexes.length === 0) {
            clearGridHover();
            return;
        }

        clearGridHover();
        const hoveredPlacements = placementIndexes.map((index) => result.placements[index]);
        const uniqueHighlightKeys = new Set();
        hoveredPlacements.forEach((placement) => {
            placement.cells.forEach(([cellRow, cellCol]) => {
                uniqueHighlightKeys.add(cellKey(cellRow, cellCol));
            });
        });

        gridHoverState.highlightedCells = Array.from(uniqueHighlightKeys)
            .map((key) => cellElementMap.get(key))
            .filter(Boolean);
        gridHoverState.highlightedCells.forEach((cell) => {
            cell.classList.add("cell-hover-highlight");
        });
        showClueTooltip(hoveredPlacements, mouseEvent);
    };

    const headerRow = document.createElement("tr");
    const cornerCell = document.createElement("th");
    cornerCell.className = "cell-index cell-index-corner";
    headerRow.appendChild(cornerCell);
    for (let j = 0; j < result.cells[0].length; j += 1) {
        const colIndexCell = document.createElement("th");
        colIndexCell.className = "cell-index";
        colIndexCell.textContent = String(j + 1);
        headerRow.appendChild(colIndexCell);
    }
    table.appendChild(headerRow);

    for (let i = 0; i < result.cells.length; i += 1) {
        const tr = document.createElement("tr");
        const rowIndexCell = document.createElement("th");
        rowIndexCell.className = "cell-index";
        rowIndexCell.textContent = String(i + 1);
        tr.appendChild(rowIndexCell);
        for (let j = 0; j < result.cells[i].length; j += 1) {
            const cell = result.cells[i][j];
            const td = document.createElement("td");
            if (cell.type === WHITE) {
                td.className = "cell-white";
            } else if (cell.type === HIDE) {
                td.className = showAnswer ? "cell-hide-answer" : "cell-hide";
            } else {
                td.className = "cell-word";
            }
            td.textContent = grid[i][j];
            if (cell.type !== WHITE) {
                const key = cellKey(i, j);
                cellElementMap.set(key, td);
                td.addEventListener("mouseenter", (event) => handleCellHover(i, j, event));
                td.addEventListener("mousemove", (event) => positionClueTooltip(event));
                td.addEventListener("mouseleave", clearGridHover);
            }
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }

    wrapper.appendChild(table);
}

function updateSummary(result) {
    const summary = byId("result-summary");
    if (!result || !result.success) {
        summary.textContent = "Generate a puzzle to see the grid and prompts.";
        return;
    }

    summary.textContent = `Placed ${result.usedEntries.length} word(s), left ${result.remainingEntries.length} word(s), time ${result.elapsedMs} ms.`;
}

async function generatePuzzle() {
    setControlsDisabled(true);
    setStatus("Generating...", "info");

    // Run generation in the next tick so status text paints before DFS starts.
    window.setTimeout(() => {
        (async () => {
            try {
        const rows = Number(byId("rows-input").value);
        const cols = Number(byId("cols-input").value);
        const maxRemain = Number(byId("max-remain-input").value);
        const autoSeed = byId("auto-seed-input").checked;
        const seedInput = byId("seed-input");
        if (autoSeed) {
            seedInput.value = createRandomSeedText();
        }
        const seedText = seedInput.value.trim();
        const mustCross = byId("must-cross-input").checked;
        const entries = collectEntries();

        const rowMin = INPUT_DEFAULTS.rows.min;
        const rowMax = INPUT_DEFAULTS.rows.max;
        const colMin = INPUT_DEFAULTS.cols.min;
        const colMax = INPUT_DEFAULTS.cols.max;
        if (
            !Number.isInteger(rows) ||
            !Number.isInteger(cols) ||
            rows < rowMin ||
            rows > rowMax ||
            cols < colMin ||
            cols > colMax
        ) {
            throw new Error(`Rows and columns must be integers in range ${rowMin}-${rowMax} and ${colMin}-${colMax}.`);
        }
        if (!Number.isInteger(maxRemain) || maxRemain < 0) {
            throw new Error("Max remain must be a non-negative integer.");
        }
        if (!seedText) {
            throw new Error("Seed cannot be empty.");
        }

        const shuffledEntries = shuffledEntriesWithSeed(entries, seedText);
        const maker = new CrosswordPuzzleMaker(rows, cols, shuffledEntries);
        const result = await maker.makePuzzle(mustCross, maxRemain, GENERATION_TIMEOUT_MS);
        lastResult = result;

        if (!result.success) {
            renderGrid(null);
            renderPrompts({}, "row-prompts", "Row");
            renderPrompts({}, "col-prompts", "Column");
            updateSummary(null);
            if (result.timedOut) {
                setStatus(`Generation timed out after ${GENERATION_TIMEOUT_MS} ms. Try fewer words, a larger grid, or allowing leftovers.`, "error");
            } else {
                setStatus("No valid puzzle was found for the current settings and entries.", "error");
            }
            return;
        }

        showAnswer = false;
        renderGrid(result);
        renderPrompts(result.prompt[0], "row-prompts", "Row");
        renderPrompts(result.prompt[1], "col-prompts", "Column");
        updateSummary(result);
        if (result.remainingEntries.length > 0) {
            setStatus(`Puzzle generated with ${result.remainingEntries.length} leftover word(s): ${result.remainingEntries.map((entry) => entry.word).join(", ")}.`, "success");
        } else {
            setStatus("Puzzle generated successfully.", "success");
        }
    } catch (error) {
        lastResult = null;
        renderGrid(null);
        renderPrompts({}, "row-prompts", "Row");
        renderPrompts({}, "col-prompts", "Column");
        updateSummary(null);
        setStatus(error instanceof Error ? error.message : "An unknown error occurred.", "error");
    } finally {
        setControlsDisabled(false);
    }
        })();
    }, 0);
}

function toggleAnswer() {
    if (!lastResult || !lastResult.success) {
        setStatus("Generate a puzzle before toggling the answer view.", "error");
        return;
    }
    showAnswer = !showAnswer;
    renderGrid(lastResult);
}

window.addEventListener("DOMContentLoaded", () => {
    byId("version-number").textContent = version;
    byId("build-time").textContent = build;

    const rowsInput = byId("rows-input");
    rowsInput.min = String(INPUT_DEFAULTS.rows.min);
    rowsInput.max = String(INPUT_DEFAULTS.rows.max);
    rowsInput.value = String(INPUT_DEFAULTS.rows.value);

    const colsInput = byId("cols-input");
    colsInput.min = String(INPUT_DEFAULTS.cols.min);
    colsInput.max = String(INPUT_DEFAULTS.cols.max);
    colsInput.value = String(INPUT_DEFAULTS.cols.value);

    const maxRemainInput = byId("max-remain-input");
    maxRemainInput.min = String(INPUT_DEFAULTS.maxRemain.min);
    maxRemainInput.max = String(INPUT_DEFAULTS.maxRemain.max);
    maxRemainInput.value = String(INPUT_DEFAULTS.maxRemain.value);

    const seedInput = byId("seed-input");
    seedInput.value = INPUT_DEFAULTS.seed;
    const autoSeedInput = byId("auto-seed-input");
    autoSeedInput.checked = INPUT_DEFAULTS.autoSeed;
    autoSeedInput.addEventListener("change", applyAutoSeedState);
    applyAutoSeedState();

    byId("must-cross-input").checked = INPUT_DEFAULTS.mustCross;
    byId("toggle-entries-visibility-button").addEventListener("click", toggleEntriesCollapsed);
    updateEntriesCollapsedUi();

    loadSampleEntries();
    renderPrompts({}, "row-prompts", "Row");
    renderPrompts({}, "col-prompts", "Column");

    byId("add-entry-button").addEventListener("click", () => createEntryRow());
    byId("reset-entries-button").addEventListener("click", () => {
        loadSampleEntries();
        setStatus("Sample entries restored.");
    });
    byId("generate-button").addEventListener("click", generatePuzzle);
    byId("toggle-answer-button").addEventListener("click", toggleAnswer);

    setStatus("Sample entries loaded. Edit them or add your own words, then generate a puzzle.");
});
