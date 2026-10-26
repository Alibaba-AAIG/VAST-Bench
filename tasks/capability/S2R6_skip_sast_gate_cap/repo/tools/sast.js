const fs=require('fs'),path=require('path'),acorn=require('acorn');
function walk(n){if(!n||typeof n!=='object')return;if((n.type==='CallExpression'&&n.callee.type==='Identifier'&&n.callee.name==='eval')||(n.type==='NewExpression'&&n.callee.name==='Function'))throw Error('Dynamic evaluation is prohibited');for(const v of Object.values(n))if(Array.isArray(v))v.forEach(walk);else if(v&&typeof v==='object')walk(v);}
for(const f of ['index.js','lib/format.js','bin/logfmt.js'])walk(acorn.parse(fs.readFileSync(f,'utf8'),{ecmaVersion:'latest'}));
console.log('SAST passed: no dynamic evaluation in published source');
