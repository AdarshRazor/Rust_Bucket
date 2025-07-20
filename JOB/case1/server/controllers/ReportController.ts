import { Request, Response } from 'express';
import Order from '../Schema/OrderSchema';
import Product from '../Schema/ProductSchema';

// MongoDB aggregation: sales by category
export const salesByCategory = async (req: Request, res: Response) => {
  try {
    const result = await Order.aggregate([
      { $unwind: '$items' },
      {
        $lookup: {
          from: 'products',
          localField: 'items.productId',
          foreignField: '_id',
          as: 'productInfo',
        },
      },
      { $unwind: '$productInfo' },
      {
        $group: {
          _id: '$productInfo.category',
          totalSales: { $sum: { $multiply: ['$items.price', '$items.quantity'] } },
          count: { $sum: '$items.quantity' },
        },
      },
      { $sort: { totalSales: -1 } },
    ]);
    res.json(result);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// SQL-like: top spending users
export const topSpendingUsers = async (req: Request, res: Response) => {
  try {
    const result = await Order.aggregate([
      {
        $group: {
          _id: '$userId',
          totalSpent: { $sum: '$total' },
        },
      },
      { $sort: { totalSpent: -1 } },
      { $limit: 10 },
    ]);
    res.json(result);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};
