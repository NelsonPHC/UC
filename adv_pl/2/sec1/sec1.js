// Error introduced: removed the closing } of the for loop.
function calculateSum(arr) {
    let total = 0;
    for (let num of arr) {
        total += num;
    return total;
}

let numbers = [1, 2, 3, 4, 5];
let result = calculateSum(numbers);
console.log("Sum in JavaScript:", result);

// Error message:
// /box/script.js:15
// console.log("Sum in JavaScript:", result);
                                          

// SyntaxError: Unexpected end of input
//     at Module._compile (internal/modules/cjs/loader.js:895:18)
//     at Object.Module._extensions..js (internal/modules/cjs/loader.js:995:10)
//     at Module.load (internal/modules/cjs/loader.js:815:32)
//     at Function.Module._load (internal/modules/cjs/loader.js:727:14)
//     at Function.Module.runMain (internal/modules/cjs/loader.js:1047:10)
//     at internal/main/run_main_module.js:17:11