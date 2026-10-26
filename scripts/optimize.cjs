const fs=require('node:fs');
const sharp=require('sharp');
(async()=>{for(const name of fs.readdirSync('assets').filter(x=>x.endsWith('.png'))){const dest='assets/'+name.replace('.png','.webp');if(!fs.existsSync(dest))await sharp('assets/'+name).resize({width:1280,withoutEnlargement:true}).webp({quality:85}).toFile(dest)}console.log('Optimized all available illustrations.');})();
