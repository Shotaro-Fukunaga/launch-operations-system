// ログオブジェクトの型を定義
export interface Log {
  timestamp: string;
  type: 'error' | 'warning' | 'info';
  text: string;
}