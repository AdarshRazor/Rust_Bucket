import { OrderItem } from './OrderItem';

export interface Order {
  id: string;
  userId: string;
  total: number;
  status: 'pending' | 'paid' | 'shipped' | 'completed' | 'cancelled';
  items: OrderItem[];
  createdAt: Date;
  updatedAt: Date;
}
