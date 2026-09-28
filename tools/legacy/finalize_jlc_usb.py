import csv,json
from pathlib import Path
from datetime import datetime,timezone

p=Path('work'); rows=json.loads((p/'jlc_usb_known.json').read_text())
extra=[('GRM32ER71A476ME15L','GRM32ER71A476ME15L','C415541','Murata Electronics','1210',741),('CNA6P1X7R1H106K','CNA6P1X7R1H106KT000A','C694544','TDK','1210',1024),('EEE-FK1E470P','EEEFK1E470P','C178545','Panasonic','6.3x5.8mm',12963),('RT0603BRD07102KL','RT0603BRD07102KL','C861068','YAGEO','0603',10762)]
for bom,mpn,code,brand,package,stock in extra:
 rows.append(dict(mpn=bom,catalog_mpn=mpn,jlc_code=code,url='https://jlcpcb.com/partdetail/'+code,checked_utc=datetime.now(timezone.utc).isoformat(),checked_time_note='Report assembly time; root browser verified during this audit session.',exact_match=bom==mpn,componentBrandEn=brand,componentSpecificationEn=package,componentLibraryType='expand',overseasStockCount=stock,canPresaleNumber=None,evidence='Root agent live JLC search browser row; min purchase 1',minimum_purchase=1))
bom=list(csv.DictReader(Path('outputs/UMI_D3/USB_POWER/BOM_grouped.csv').open(encoding='utf-8-sig')))
for r in rows:
 bs=[b for b in bom if b['Manufacturer part number']==r['mpn']]
 r['references']=','.join(b['Reference'] for b in bs)
 r['quantity_per_board']=sum(int(b['Quantity per board']) for b in bs)
 r['assembly']='SMT';r['library_class']='Extended';r['displayed_stock']=r['overseasStockCount']
 r.setdefault('catalog_mpn',r['mpn']);r.setdefault('evidence','Public JLC product page embedded product data; saved HTML/JSON in work/jlc_evidence')
 if r['mpn']=='CNA6P1X7R1H106K':
  r['match_note']='BOM uses incomplete base MPN. TDK maps electrical part CNA6P1X7R1H106K250AE to delivery part CNA6P1X7R1H106KT***A; specify full stocked delivery MPN CNA6P1X7R1H106KT000A.'
  r['manufacturer_source']='https://product.tdk.cn/zh/search/capacitor/ceramic/mlcc/info?part_no=CNA6P1X7R1H106K250AE'
 if r['mpn']=='EEE-FK1E470P':r['match_note']='Panasonic catalog punctuation normalized: EEE-FK1E470P = EEEFK1E470P.'
 r['stock_risk']='low displayed stock; reconfirm at order' if r['displayed_stock']<100 else 'reconfirm at order'
rows.sort(key=lambda r:r['references'])
data={'scope':'USB_POWER D3 exact SMT BOM; manual through-hole parts excluded','checked_date_utc':'2026-09-26','unique_mpn_count':len(rows),'smt_placements':sum(r['quantity_per_board'] for r in rows),'status':'All 16 intended SMT parts have live stocked JLC catalog matches; complete TDK orderable suffix required. Stock is not reserved and assembly order acceptance not yet tested.','parts':rows}
(p/'jlc_usb.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
md=['# USB_POWER JLCPCB availability audit','',data['status'],'','31 SMT placements, 16 distinct parts. All catalog entries are Extended. Checked 26 September 2026 UTC. No board or BOM source was edited.','','| References | Qty | Full catalog MPN | JLC code | Package | Displayed stock |','|---|---:|---|---|---|---:|']
for r in rows:md.append(f"| {r['references']} | {r['quantity_per_board']} | {r['catalog_mpn']} | [{r['jlc_code']}]({r['url']}) | {r['componentSpecificationEn']} | {r['displayed_stock']:,} |")
md+=['','## Required sourcing correction','','C1/C2: replace incomplete base CNA6P1X7R1H106K with **CNA6P1X7R1H106KT000A**, C694544. [TDK product record](https://product.tdk.cn/zh/search/capacitor/ceramic/mlcc/info?part_no=CNA6P1X7R1H106K250AE) explicitly gives delivery MPN pattern CNA6P1X7R1H106KT***A, 10µF±10%, 50V, X7R, 3.2×2.5×2.5mm. The alternative electrical-record code C2182452 is zero-stock; use stocked delivery code C694544. Panasonic EEE-FK1E470P is the same punctuation-normalized catalog MPN EEEFK1E470P.','','## Stock and evidence limits','','R8 has 26 pieces displayed and zero presale count; U4 has 37 and U1 has 64. These are the limiting per-board parts and must be reconfirmed for the intended order quantity and assembly attrition. No unsupported substitute is proposed: current exact parts are stocked, and no batch quantity is specified.','','Displayed stock comes from the JLC field overseasStockCount, verified against root browser rows. canPresaleNumber is retained separately in JSON and is not displayed stock. preMinPurchaseNum is a pre-order minimum, not assembly minimum. Root live browser confirmed minimum 1 for the four additional parts and TPSM63610RDFR/TPS2557DRBR. Public page evidence for the initial twelve parts is saved under work/jlc_evidence; the other four are root browser observations. Stock alone does not reserve inventory or establish final assembly-order acceptance.','','J1 and J2/J3 remain user-fit through-hole parts and are excluded from this SMT audit. The old U1 BOM note saying LCSC-only is obsolete: live JLC C7125816 explicitly shows stock64.']
(p/'jlc_usb.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'parts':len(rows),'placements':data['smt_placements']}))
