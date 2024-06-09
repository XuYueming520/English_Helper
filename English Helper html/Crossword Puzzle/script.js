var rand = function () {
    var seed = 736520 | 0x7365200001314;
    function rand() {
        seed ^= seed >> 10;
        seed ^= seed << 9;
        seed ^= seed >> 25;
        return seed;
    }
    return function (l = 1, r = 5201314) {
        if (l > r) return 0;
        return rand() % (r - l + 1) + l;
    }
} ();

window.onload = function() {
    console.log(rand());
}
