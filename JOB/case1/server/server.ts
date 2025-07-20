import express, { Request, Response } from 'express';
import cors from 'cors';

import productRoutes from './routes/productRoutes';
import authRoutes from './routes/authRoutes';



const app = express();
const PORT = process.env.PORT || 3000;
app.use(cors());

app.use(express.json());
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);

app.get('/', (req: Request, res: Response) => {
  res.send('Hello, Express + TypeScript!');
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
