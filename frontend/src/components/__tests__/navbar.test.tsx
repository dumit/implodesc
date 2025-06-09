import { render, screen } from '@testing-library/react';
import { Navbar } from '../navbar';

// Mock Next.js Link component
jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => {
    return <a href={href}>{children}</a>;
  };
});

describe('Navbar', () => {
  it('renders the logo and brand name', () => {
    render(<Navbar />);
    
    const brandLink = screen.getByRole('link', { name: /implodesc/i });
    expect(brandLink).toBeInTheDocument();
    expect(brandLink).toHaveAttribute('href', '/');
  });

  it('renders navigation links', () => {
    render(<Navbar />);
    
    const analyzeLink = screen.getByRole('link', { name: /analyze/i });
    expect(analyzeLink).toBeInTheDocument();
    expect(analyzeLink).toHaveAttribute('href', '/analyze');
  });

  it('renders sign in and sign up buttons when not authenticated', () => {
    render(<Navbar />);
    
    const signInButton = screen.getByRole('link', { name: /sign in/i });
    const signUpButton = screen.getByRole('link', { name: /sign up/i });
    
    expect(signInButton).toBeInTheDocument();
    expect(signInButton).toHaveAttribute('href', '/sign-in');
    
    expect(signUpButton).toBeInTheDocument();
    expect(signUpButton).toHaveAttribute('href', '/sign-up');
  });

  it('does not render dashboard link when not authenticated', () => {
    render(<Navbar />);
    
    const dashboardLink = screen.queryByRole('link', { name: /dashboard/i });
    expect(dashboardLink).not.toBeInTheDocument();
  });
});