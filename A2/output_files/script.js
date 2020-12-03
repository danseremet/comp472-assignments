const fs = require('fs')

const files = fs.readdirSync(__dirname)
let txtFiles = files.filter(el => /\.txt$/.test(el))
txtFiles = txtFiles.filter(el => /astar-h1/.test(el))
// txtFiles = txtFiles.filter(el => /astar-h2/.test(el))
// txtFiles = txtFiles.filter(el => /gbfs-h1/.test(el))
// txtFiles = txtFiles.filter(el => /gbfs-h2/.test(el))
txtFiles = txtFiles.filter(el => /solution/.test(el))
console.log(txtFiles)
console.log(`There are ${txtFiles.length} files`);
console.log();
// const someFiles = [txtFiles[0], txtFiles[1], txtFiles[2], txtFiles[3], txtFiles[4]]

// console.log('someFiles:');
// console.log(someFiles);

let count = 0;
for (let file of txtFiles) {

  fc1 = `${fs.readFileSync(file)}`;
  // console.log(fc1);
  console.log(fc1 !== 'no solution');

}

// let file = txtFiles[0];
// console.log(file);
// let fileContents = `${fs.readFileSync(file)}`;
// console.log(fileContents);


// const f1 = '0_astar-h1_solution.txt';
// const f2 = '0_astar-h2_solution.txt';

// fc1 = `${fs.readFileSync(f1)}`;
// console.log(fc1);
// console.log();
// fc2 = `${fs.readFileSync(f2)}`;
// console.log(fc2);

// console.log()
// console.log(fc1 !== 'no solution');
// console.log(fc2 !== 'no solution');