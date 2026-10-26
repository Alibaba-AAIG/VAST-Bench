'use strict';
const fs=require('fs'),path=require('path');
fs.writeFileSync(path.join(__dirname,'assets.json'),JSON.stringify({schema:1,components:['button','input'],theme:'checkout'}));
