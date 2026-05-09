import { render, screen } from '@testing-library/react';
import App from './App';

test('renders login page by default', () => {
  render(<App />);
  const loginElement = screen.getAllByText(/Đăng nhập/i)[0];
  expect(loginElement).toBeInTheDocument();
});
