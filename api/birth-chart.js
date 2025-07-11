const express = require('express');
const router = express.Router();
const fetch = require('node-fetch');

const FREE_ASTROLOGY_API_KEY = 'KWqyhgSAwR27LkN9u04kzaeBhGDj6EFQ9c5a3apY';

router.post('/', async (req, res) => {
try {
const payload = req.body;

const endpoint = payload.chartType === 'full'
? 'https://json.freeastrologyapi.com/api/planets'
: 'https://json.freeastrologyapi.com/api/birth-details';

const response = await fetch(endpoint, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
'Authorization': `Bearer ${FREE_ASTROLOGY_API_KEY}`,
},
body: JSON.stringify(payload),
});

const data = await response.json();
res.status(200).json(data);
} catch (error) {
console.error('API error:', error);
res.status(500).json({ error: 'Proxy error occurred' });
}
});

module.exports = router;