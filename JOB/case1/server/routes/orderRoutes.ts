import { Router } from 'express';
import { checkout, getOrderHistory } from '../controllers/OrderController';
import { authenticate } from '../controllers/AuthController';

const router = Router();

router.post('/checkout', authenticate, checkout);
router.get('/history', authenticate, getOrderHistory);

export default router;
