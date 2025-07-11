const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const birthChartRoute = require('./api/birth-chart');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use('/api/birth-chart', birthChartRoute);

app.get('/', (req, res) => {
res.send('✨ Astrology Proxy Server is running ✨');
});

app.listen(PORT, () => {
console.log(`Server is running on port ${PORT}`);
});