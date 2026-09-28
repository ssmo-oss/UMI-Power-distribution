import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';

const input=process.argv[2]||'work/jlc_combined_parts.json';
const output=process.argv[3]||'outputs/UMI_D3/UMI_All_Parts.xlsx';
const raw=JSON.parse(await fs.readFile(input,'utf8'));
const parts=Array.isArray(raw)?raw:raw.parts;
const isD5=raw.revision==='D5';
const isD6=raw.revision==='D6';
if(!Array.isArray(parts)||!parts.length)throw Error('Missing parts records');
const keys=['board','refs','qty_per_pair','mpn','manufacturer','value','assembly','jlc_code','current_stock','status','checked_utc','source_url','proposed_alternative','required_10_pairs'];
const headers=['Board','References','Qty per pair','Manufacturer part number','Manufacturer','Value / description','Assembly','JLC code','Current stock','Availability status','Checked (UTC)','Source URL','Change / procurement notes','Required for 10 pairs'];
if(isD5){headers[2]='Qty per 3-board set';headers[13]='Required for 10 sets';}
if(isD6){headers[2]='Qty per 3-board set';headers[8]='JLC observed stock';headers[13]='Installed for 10 sets';keys.push('purchase_quantity','purchase_supplier','purchase_stock','purchase_url','purchase_basis');headers.push('Planned buy quantity','Buy from','Supplier observed stock','Purchase link','Quantity basis');}
const rows=parts.map((p,i)=>keys.map(k=>{
 const v=p[k];
 if(k==='qty_per_pair'||k==='required_10_pairs'){if(typeof v!=='number'||v<0)throw Error(`Invalid quantity row ${i}`);return v;}
 if(k==='current_stock')return typeof v==='number'?v:null;
 if(k==='purchase_quantity'||k==='purchase_stock')return typeof v==='number'?v:null;
 if(k==='checked_utc')return v?new Date(v):null;
 return v==null?'':Array.isArray(v)?v.join(', '):String(v);
}));
const wb=Workbook.create(),s=wb.worksheets.add('All parts');
s.showGridLines=false;s.tabColor='#24364B';
const last=rows.length+5;
s.getRange(`A1:N${last}`).format.font={name:'Arial',size:10,color:'#202B36'};
s.getRange(`A1:M${last}`).format.verticalAlignment='center';
s.getRange('A2').values=[['UMI combined parts list']];
s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:'#24364B'};
s.getRange('A3').values=[['D4 SOURCING: preorder and manual procurement unresolved. Quantities for 10 pairs exclude assembly attrition. Stock is not reserved.']];
if(isD5){s.getRange('A3').values=[['D5: 10 each of MAIN, POE and USB boards; quantities exclude attrition. Preorder/manual procurement unresolved; stock not reserved.']];s.getRange('A4').values=[['173.55 W nominal maximum across two mutually exclusive configurations. Fuse values remain provisional.']];}
if(isD6){s.getRange('A3').values=[['D6: 10 each of MAIN, POE and USB. SMT at JLC; loose manual parts sourced separately. Stock is not reserved.']];s.getRange('A4').values=[['Purchase quantities include planning allowances. Repeated manual MPNs are purchased once; zero means included in an earlier row.']];}
s.getRange('A3').format.font={name:'Arial',size:10,italic:true,color:'#546170'};
const end=isD6?'S':'N';
s.getRange(`A5:${end}${last}`).values=[headers,...rows];
const table=s.tables.add(`A5:${end}${last}`,true,'AllParts');table.showFilterButton=true;table.style='TableStyleMedium2';
s.getRange('A5:M5').format={fill:'#24364B',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true,rowHeight:34};
const widths=[18,25,13,33,25,37,20,15,16,48,19,64,72,20];
if(isD6)widths.push(20,27,21,70,74);
widths.forEach((w,i)=>s.getRangeByIndexes(0,i,last,1).format.columnWidth=w);
s.getRange(`A6:M${last}`).format.rowHeight=34;
s.getRange(`A6:M${last}`).format.wrapText=true;
s.getRange('N5').format={fill:'#24364B',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true};
s.getRange(`N6:N${last}`).setNumberFormat('#,##0');
rows.forEach((r,i)=>{const lines=Math.max(...r.map((v,c)=>Math.ceil(String(v??'').length/(widths[c]*0.95))));s.getRange(`A${i+6}:M${i+6}`).format.rowHeight=Math.max(34,lines*14+8);});
if(isD6){s.getRange(`O5:S${last}`).format.font={name:'Arial',size:10,color:'#202B36'};s.getRange('O5:S5').format={fill:'#24364B',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};s.getRange(`O6:S${last}`).format.wrapText=true;s.getRange(`O6:S${last}`).format.verticalAlignment='center';s.getRange(`O6:O${last}`).setNumberFormat('#,##0');s.getRange(`Q6:Q${last}`).setNumberFormat('#,##0');s.getRange(`R6:R${last}`).format.font={name:'Arial',size:10,color:'#245B92'};}
s.getRange(`C6:C${last}`).setNumberFormat('#,##0');
s.getRange(`I6:I${last}`).setNumberFormat('#,##0');
s.getRange(`K6:K${last}`).setNumberFormat('yyyy-mm-dd hh:mm');
s.getRange(`C6:C${last}`).format.horizontalAlignment='right';
s.getRange(`I6:I${last}`).format.horizontalAlignment='right';
s.getRange(`L6:L${last}`).format.font={name:'Arial',size:10,color:'#245B92'};
s.getRange(`J6:J${last}`).conditionalFormats.add('containsText',{text:'unverified',format:{fill:'#FFF0C2',font:{color:'#7B4C00'}}});
s.getRange(`I6:I${last}`).conditionalFormats.add('cellIs',{operator:'equal',formula:0,format:{fill:'#FCE4E4',font:{color:'#9D2424'}}});
s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(2);
wb.recalculate();
const inspect=await wb.inspect({kind:'table',range:'All parts!A5:M11',include:'values,formulas',tableMaxRows:7,tableMaxCols:13,maxChars:5000});
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:30},summary:'Formula errors'});
await fs.mkdir(path.dirname(output),{recursive:true});
await fs.writeFile('work/combined_parts_inspect.json',JSON.stringify({rows:parts.length,quantity:parts.reduce((n,p)=>n+p.qty_per_pair,0),inspect:inspect.ndjson,errors:errors.ndjson},null,2));
for(const [name,range] of [['left','A1:I15'],['right','J5:M15'],['bottom',`A${Math.max(5,last-10)}:M${last}`]]){
 const image=await wb.render({sheetName:'All parts',range,scale:1,format:'png'});
 await fs.writeFile(`work/combined_parts_${name}.png`,new Uint8Array(await image.arrayBuffer()));
}
if(isD6){const image=await wb.render({sheetName:'All parts',range:'N5:S15',scale:1,format:'png'});await fs.writeFile('work/combined_parts_purchase.png',new Uint8Array(await image.arrayBuffer()));}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(output);
console.log(JSON.stringify({output,records:parts.length,quantity:parts.reduce((n,p)=>n+p.qty_per_pair,0)}));
