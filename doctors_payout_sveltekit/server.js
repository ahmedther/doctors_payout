import { handler } from './build/handler.js';
import express from 'express';

const app = express();
const port = process.env.PORT || 3000;

// add a route that lives separately from the SvelteKit app
app.get('/healthcheck', (req, res) => {
    res.end('ok');
});

// let SvelteKit handle everything else, including serving prerendered pages and static assets
app.use(handler);

app.listen(port, () => {
    console.log(`listening on port ${port}`);
});
