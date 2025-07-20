import { Request, Response } from 'express';
import Order from '../Schema/OrderSchema';
import Cart from '../Schema/CartSchema';
import Product from '../Schema/ProductSchema';
import { clearCart } from './CartController';

// Checkout: create order from cart and clear cart
export const checkout = async (req: Request, res: Response) => {
  try {
    const userId = (req as any).user.userId;
    const cart = await Cart.findOne({ userId });
    if (!cart || cart.items.length === 0) {
      return res.status(400).json({ message: 'Cart is empty.' });
    }
    let total = 0;
    for (const item of cart.items) {
      const product = await Product.findById(item.productId);
      if (!product) return res.status(404).json({ message: 'Product not found.' });
      total += product.price * item.quantity;
    }
    const order = new Order({
      userId,
      total,
      status: 'pending',
      items: cart.items.map(item => ({
        productId: item.productId,
        quantity: item.quantity,
        price: undefined // will be set below
      })),
    });
    // Set price for each order item
    for (let i = 0; i < order.items.length; i++) {
      const product = await Product.findById(order.items[i].productId);
      order.items[i].price = product ? product.price : 0;
    }
    await order.save();
    await clearCart(userId);
    res.status(201).json(order);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// Get order history for current user
export const getOrderHistory = async (req: Request, res: Response) => {
  try {
    const userId = (req as any).user.userId;
    const orders = await Order.find({ userId }).sort({ createdAt: -1 });
    res.json(orders);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};
