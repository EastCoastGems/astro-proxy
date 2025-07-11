// Vercel Serverless Function Entry — /api endpoint

const corsHeaders = {
'Access-Control-Allow-Origin': '*',
'Access-Control-Allow-Methods': 'POST, OPTIONS',
'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export default async function handler(req, res) {
if (req.method === 'OPTIONS') {
res.writeHead(200, corsHeaders);
res.end()'
return;
}

if (req.method !== 'POST') {
return res.status(405).set(corsHeaders).json({ error: 'Only POST allowed' });
}

const token = 'KWqyhgSAwR27LkN9u04kzaeBhGDj6EFQ9c5a3apY'; // Replace with your real key
const payload = req.body;

const endpoint =
payload.chartType === 'full'
? 'https://json.freeastrologyapi.com/api/planets'
: 'https://json.freeastrologyapi.com/api/birth-details';

try {
const astroRes = await fetch(endpoint, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
Authorization: `Bearer ${token}`,
},
body: JSON.stringify(payload),
});

const data = await astroRes.json();
res.status(200).set(corsHeaders).json(data);
} catch (err) {
console.error('🔴 Proxy Error:', err);
res.status(500).set(corsHeaders).json({ error: 'Proxy failed' });
}
}