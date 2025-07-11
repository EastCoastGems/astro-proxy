const fetch = require('node-fetch');

module.exports = async (req, res) => {
const corsHeaders = {
'Access-Control-Allow-Origin': '*',
'Access-Control-Allow-Methods': 'POST, OPTIONS',
'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

if (req.method === 'OPTIONS') {
return res.status(204).set(corsHeaders).end();
}

if (req.method !== 'POST') {
return res.status(405).set(corsHeaders).json({ error: 'Only POST allowed' });
}

try {
const payload = req.body;
if (!payload) {
throw new Error('Missing request body');
}

const token = 'KWqyhgSAwR27LkN9u04kzaeBhGDj6EFQ9c5a3apY'; // Put your token here!

const endpoint =
payload.chartType === 'full'
? 'https://json.freeastrologyapi.com/api/planets'
: 'https://json.freeastrologyapi.com/api/birth-details';

const response = await fetch(endpoint, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
Authorization: `Bearer ${token}`,
},
body: JSON.stringify(payload),
});

if (!response.ok) {
const errorText = await response.text();
throw new Error(`API error: ${response.status} ${errorText}`);
}

const data = await response.json();

return res.status(200).set(corsHeaders).json(data);
} catch (err) {
console.error('Proxy Error:', err.message || err);
return res.status(500).set(corsHeaders).json({ error: 'Proxy failed', details: err.message || err });
}
};
