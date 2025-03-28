import React from "react";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  children: React.ReactNode;
};

export function Button({ children, className = "", ...props }: ButtonProps) {
  return (
    <button
      {...props}
      className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 ${className}`}
    >
      {children}
    </button>
  );
}
