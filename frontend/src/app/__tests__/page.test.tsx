import { render, screen } from '@testing-library/react';
import HomePage from '../page';

// Mock Next.js Link component
jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => {
    return <a href={href}>{children}</a>;
  };
});

describe('HomePage', () => {
  it('renders the main heading', () => {
    render(<HomePage />);
    
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('AI-Driven Supply Chain Analysis');
  });

  it('renders the start analysis button', () => {
    render(<HomePage />);
    
    const startButton = screen.getByRole('link', { name: /start analysis/i });
    expect(startButton).toBeInTheDocument();
    expect(startButton).toHaveAttribute('href', '/analyze');
  });

  it('renders the learn more button', () => {
    render(<HomePage />);
    
    const learnButton = screen.getByRole('link', { name: /learn more/i });
    expect(learnButton).toBeInTheDocument();
    expect(learnButton).toHaveAttribute('href', '/about');
  });

  it('renders feature cards', () => {
    render(<HomePage />);
    
    expect(screen.getByText('Global Supply Mapping')).toBeInTheDocument();
    expect(screen.getByText('Carbon Footprint Analysis')).toBeInTheDocument();
    expect(screen.getByText('Interactive Visualizations')).toBeInTheDocument();
  });

  it('renders call-to-action section', () => {
    render(<HomePage />);
    
    expect(screen.getByText('Ready to Analyze Your Product?')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /start your analysis/i })).toBeInTheDocument();
  });
});