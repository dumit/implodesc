import { render, screen } from '@testing-library/react';
import TestPage from '../../test/page';

describe('TestPage', () => {
  it('renders hello world message', () => {
    render(<TestPage />);
    
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Hello World');
  });

  it('renders working message', () => {
    render(<TestPage />);
    
    const message = screen.getByText('Frontend is working!');
    expect(message).toBeInTheDocument();
  });
});