export default async function handler(req, res) {
// Enable CORS
res.setHeader('Access-Control-Allow-Origin', '*');
res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

// Handle preflight OPTIONS request
if (req.method === 'OPTIONS') {
return res.status(200).end();
}

if (req.method !== 'POST') {
return res.status(405).json({ error: 'Only POST allowed' });
}

try {
const payload = req.body;

const token = 'KWqyhgSAwR27LkN9u04kzaeBhGDj6EFQ9c5a3apY'; // Your actual token here

const endpoint =
payload.chartType === 'full'
? 'https://json.freeastrologyapi.com/api/planets'
: 'https://json.freeastrologyapi.com/api/birth-details';

const response = await fetch(endpoint, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
'Authorization': 'Bearer KWqyhgSAwR27LkN9u04kzaeBhGDj6EFQ9c5a3apY'
},
body: JSON.stringify(payload),
});

const data = await response.json();

res.status(200).json(data);
} catch (error) {
console.error('Proxy Error:', error);
res.status(500).json({ error: 'Proxy failed' });
}
}