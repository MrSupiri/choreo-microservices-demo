const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

// Echo endpoint
app.post('/echo', (req, res) => {
    res.json(req.body);
});

// Proxy endpoint
app.post('/proxy', async (req, res) => {
    try {
        const { url, method, body } = req.body;
        const response = await axios({ url, method, data: body });
        res.set(response.headers);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Error proxying request' });
    }
});

// Log payload endpoint
app.post('/log', (req, res) => {
    const level = req.body.level || 'info';
    console[level](req.body.payload);
    res.json({ message: 'Logged successfully' });
});

// Healthz endpoint
app.get('/healthz', (req, res) => {
    res.json({ status: 'Healthy' });
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on port ${port}`));
