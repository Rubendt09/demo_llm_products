import React from 'react';

interface FormattedTextProps {
  text: string;
}

export const FormattedText: React.FC<FormattedTextProps> = ({ text }) => {
  // Función para procesar texto con formato Markdown básico
  const processText = (text: string) => {
    // Dividir el texto en partes, manteniendo los delimitadores
    const parts = text.split(/(\*\*.*?\*\*|\*.*?\*)/g);
    
    return parts.map((part, index) => {
      // Texto en negrita (**texto**)
      if (part.startsWith('**') && part.endsWith('**')) {
        const content = part.slice(2, -2);
        return (
          <strong key={index} className="font-bold">
            {content}
          </strong>
        );
      }
      
      // Texto en cursiva (*texto*)
      if (part.startsWith('*') && part.endsWith('*') && !part.startsWith('**')) {
        const content = part.slice(1, -1);
        return (
          <em key={index} className="italic">
            {content}
          </em>
        );
      }
      
      // Texto normal
      return <span key={index}>{part}</span>;
    });
  };

  return <>{processText(text)}</>;
};

export default FormattedText;