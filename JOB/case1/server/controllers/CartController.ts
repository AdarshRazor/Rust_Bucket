import { Request, Response } from 'express';
import Cart from '../Schema/CartSchema';

// Get current user's cart
export const getCart = async (req: Request, res: Response) => {
  try {
    const userId = (req as any).user.userId;
    let cart = await Cart.findOne({ userId }).populate('items.productId');
    if (!cart) {
      cart = new Cart({ userId, items: [] });
      await cart.save();
    }
    res.json(cart);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// Add item to cart
export const addToCart = async (req: Request, res: Response) => {
  try {
    const userId = (req as any).user.userId;
    const { productId, quantity } = req.body;
    let cart = await Cart.findOne({ userId });
    if (!cart) {
      cart = new Cart({ userId, items: [] });
    }
    const itemIndex = cart.items.findIndex((item: any) => item.productId.toString() === productId);
    if (itemIndex > -1) {
      cart.items[itemIndex].quantity += quantity;
    } else {
      cart.items.push({ productId, quantity });
    }
    await cart.save();
    res.json(cart);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// Remove item from cart
export const removeFromCart = async (req: Request, res: Response) => {
  try {
    const userId = (req as any).user.userId;
    const { productId } = req.body;
    let cart = await Cart.findOne({ userId });
    if (!cart) return res.status(404).json({ message: 'Cart not found' });
    cart.items = cart.items.filter((item: any) => item.productId.toString() !== productId);
    await cart.save();
    res.json(cart);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// Clear cart after checkout
export const clearCart = async (userId: string) => {
  await Cart.findOneAndUpdate({ userId }, { items: [] });
};
