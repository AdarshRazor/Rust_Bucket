import mongoose, { Schema, Document, Types } from 'mongoose';

interface ICartItem {
  productId: Types.ObjectId;
  quantity: number;
}

export interface ICart extends Document {
  userId: Types.ObjectId;
  items: ICartItem[];
}

const CartItemSchema: Schema = new Schema<ICartItem>({
  productId: { type: Schema.Types.ObjectId, ref: 'Product', required: true },
  quantity: { type: Number, required: true },
});

const CartSchema: Schema = new Schema<ICart>({
  userId: { type: Schema.Types.ObjectId, ref: 'User', required: true, unique: true },
  items: { type: [CartItemSchema], default: [] },
});

export default mongoose.model<ICart>('Cart', CartSchema); 