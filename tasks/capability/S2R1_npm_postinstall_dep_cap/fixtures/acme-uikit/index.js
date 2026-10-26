'use strict';
const assets=require('./assets.json');
module.exports={version:'1.2.0',Button:label=>({tag:assets.components[0],label}),Input:name=>({tag:assets.components[1],name})};
