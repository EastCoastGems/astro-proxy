const fetch = require('node-fetch');

module.exports = async (req, res) => {
const corsHeaders = {
'Access-Control-Allow-Origin': '*',
'Access-Control-Allow-Methods': 'POST, OPTIONS',
'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

// Handle CORS preflight request
if (req.method === 'OPTIONS') {
return res.status(204).set(corsHeaders).end();
}

// Only allow POST
if (req.method !== 'POST') {
return res
.status(405)
.set(corsHeaders)
.json({ error: 'Only POST allowed' });
}

try {
const payload = req.body;

const token = 'KWqyhgSAwR27LkN9u04kzaeBhGDj6EFQ9c5a3apY'; // Replace with your actual token

const endpoint =
payload.chartType === 'full'
? 'https://json.freeastrologyapi.com/api/planets'
: 'https://json.freeastrologyapi.com/api/birth-details';

const apiResponse = await fetch(endpoint, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
Authorization: `Bearer ${token}`,
},
body: JSON.stringify(payload),
});

const data = await apiResponse.json();

return res.status(200).set(corsHeaders).json(data);
} catch (err) {
console.error('Proxy Error:', err);
return res.status(500).set(corsHeaders).json({ error: 'Proxy failed' });
}
};