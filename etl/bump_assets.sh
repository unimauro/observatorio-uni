#!/bin/sh
# Cambia la versión de app.js y de los CSS en todas las páginas para que los navegadores no usen la copia vieja.
cd "$(dirname "$0")/.." && V=$(date +%Y%m%d%H%M)
for f in *.html; do sed -i '' -E "s#(app\.js|assets/styles\.css|assets/uni2036\.css)(\?v=[0-9]+)?\"#\1?v=$V\"#g" "$f"; done
echo "assets v=$V"
