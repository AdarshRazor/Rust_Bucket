import { Request, Response } from 'express';
import Product from '../Schema/ProductSchema';

// Create a new product
export const createProduct = async (req: Request, res: Response) => {
  try {
    const { name, description, price, category, imageUrl, stock } = req.body;
    const product = new Product({ name, description, price, category, imageUrl, stock });
    await product.save();
    res.status(201).json(product);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// Get all products with search, filter, and pagination
export const getProducts = async (req: Request, res: Response) => {
  try {
    const { page = 1, limit = 10, search = '', category } = req.query;
    const query: any = {};
    if (search) {
      query.name = { $regex: search, $options: 'i' };
    }
    if (category) {
      query.category = category;
    }
    const products = await Product.find(query)
      .skip((+page - 1) * +limit)
      .limit(+limit);
    const total = await Product.countDocuments(query);
    res.json({ products, total });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// Get a single product by ID
export const getProductById = async (req: Request, res: Response) => {
  try {
    const product = await Product.findById(req.params.id);
    if (!product) return res.status(404).json({ message: 'Product not found' });
    res.json(product);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// Update a product by ID
export const updateProduct = async (req: Request, res: Response) => {
  try {
    const product = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!product) return res.status(404).json({ message: 'Product not found' });
    res.json(product);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};

// Delete a product by ID
export const deleteProduct = async (req: Request, res: Response) => {
  try {
    const product = await Product.findByIdAndDelete(req.params.id);
    if (!product) return res.status(404).json({ message: 'Product not found' });
    res.json({ message: 'Product deleted' });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
};
