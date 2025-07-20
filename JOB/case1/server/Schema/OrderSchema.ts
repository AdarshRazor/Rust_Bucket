import mongoose, { Schema, Document, Types } from 'mongoose';
import { IOrderItem, OrderItemSchema } from './OrderItemSchema';

export interface IOrder extends Document {
  userId: Types.ObjectId;
  total: number;
  status: 'pending' | 'paid' | 'shipped' | 'completed' | 'cancelled';
  items: IOrderItem[];
  createdAt: Date;
  updatedAt: Date;
}

const OrderSchema: Schema = new Schema<IOrder>({
  userId: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  total: { type: Number, required: true },
  status: { type: String, enum: ['pending', 'paid', 'shipped', 'completed', 'cancelled'], default: 'pending' },
  items: { type: [OrderItemSchema], required: true },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now },
});

export default mongoose.model<IOrder>('Order', OrderSchema); 