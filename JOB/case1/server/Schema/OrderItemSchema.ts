import mongoose, { Schema, Document, Types } from 'mongoose';

export interface IOrderItem extends Document {
  productId: Types.ObjectId;
  quantity: number;
  price: number;
}

export const OrderItemSchema: Schema = new Schema<IOrderItem>({
  productId: { type: Schema.Types.ObjectId, ref: 'Product', required: true },
  quantity: { type: Number, required: true },
  price: { type: Number, required: true },
}); 