import re,json
from pathlib import Path
for f in Path('work/jlc_live').glob('*.html'):
 s=f.read_text(encoding='utf8');chunks=re.findall(r'self\.__next_f\.push\((.*?)\)</script>',s);t='\n'.join(str(json.loads(c)[1]) for c in chunks);Path(str(f)+'.decoded').write_text(t,encoding='utf8');print(f.name);print('\n'.join(re.findall('.{0,70}(?:stockCount|stockNumber|stockNum|stockQuantity|stock:|stock\\"|componentLibraryType|componentModel|minimum|purchaseNum|minPurchaseNum).{0,100}',t)[-18:]))
