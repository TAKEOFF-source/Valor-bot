const { Client, GatewayIntentBits } = require('discord.js');
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
let players = {};
function getPlayer(name){
 let key=name.toLowerCase().trim();
 if(!players[key]) players[key]={name:name.trim(), tag:key, points:500, rank:"LT5", wins:0, losses:0, tier:"Overall"};
 return players[key];
}
function updateRank(p){
 if(p.points>=1200) p.rank="HT1"; else if(p.points>=1000) p.rank="HT2"; else if(p.points>=800) p.rank="HT3"; else if(p.points>=600) p.rank="LT1"; else if(p.points>=400) p.rank="LT2"; else p.rank="LT3";
}
function parseResult(c){ let m=c.match(/(\w+)\s+(?:beat|won|defeated|>\s*)\s+(\w+)/i); return m?{winner:m[1],loser:m[2]}:null; }
app.get('/api/leaderboard',(req,res)=>{ let arr=Object.values(players); arr.sort((a,b)=>b.points-a.points); res.json(arr); });
app.get('/',(req,res)=>res.sendFile(__dirname+'/index.html'));
app.listen(PORT,()=>console.log("Live "+PORT));
const client=new Client({intents:[GatewayIntentBits.Guilds,GatewayIntentBits.GuildMessages,GatewayIntentBits.MessageContent]});
client.on('ready',async()=>{
 const guild=await client.guilds.fetch('1506313155226112093');
 const channels=await guild.channels.fetch();
 const ch=channels.find(c=>c.name&&c.name.includes('results'));
 if(!ch) return; let lastId=null; let after=new Date('2026-08-30').getTime();
 while(true){ let msgs=await ch.messages.fetch({limit:100,before:lastId}).catch(()=>null); if(!msgs||msgs.size==0) break;
  for(let msg of msgs.values()){ if(msg.createdTimestamp<after) break; let p=parseResult(msg.content); if(p){ let w=getPlayer(p.winner),l=getPlayer(p.loser); w.wins++; w.points+=25; updateRank(w); l.losses++; l.points=Math.max(0,l.points-15); updateRank(l); } }
  lastId=msgs.last().id; if(msgs.last().createdTimestamp<after) break;
 }
});
client.on('messageCreate',msg=>{
 if(msg.guildId!=='1506313155226112093') return; if(!msg.channel.name.includes('results')) return; if(msg.author.bot) return;
 let p=parseResult(msg.content); if(!p) return; let w=getPlayer(p.winner),l=getPlayer(p.loser); w.wins++; w.points+=50; updateRank(w); l.losses++; l.points=Math.max(0,l.points-20); updateRank(l);
});
client.login(process.env.TOKEN);
