import { Router } from 'express';
import { getCart, addToCart, removeFromCart } from '../controllers/CartController';
import { authenticate } from '../controllers/AuthController';

const router = Router();

router.get('/', authenticate, getCart);
router.post('/add', authenticate, addToCart);
router.post('/remove', authenticate, removeFromCart);

export default router;
