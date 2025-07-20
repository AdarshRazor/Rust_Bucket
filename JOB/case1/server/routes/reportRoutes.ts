import { Router } from 'express';
import { salesByCategory, topSpendingUsers } from '../controllers/ReportController';
import { authenticate } from '../controllers/AuthController';

const router = Router();

router.get('/sales-by-category', authenticate, salesByCategory);
router.get('/top-spending-users', authenticate, topSpendingUsers);

export default router;
