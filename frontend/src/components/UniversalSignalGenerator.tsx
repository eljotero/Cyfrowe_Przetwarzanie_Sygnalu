import { useState } from 'react';
import './UniversalSignalGenerator.css';

export const UniversalSignalGenerator = (props: any) => {
  const [formData, setFormData] = useState({});

  function onClick() {
    const data = encodeURIComponent(
      JSON.stringify({ signalId: props.signalId, formData })
    );
    const url = `/chart/${data}`;
    window.open(url, '_blank');
  }

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = event.target;
    setFormData({ ...formData, [id]: value });
  };

  return (
    <div className='container'>
      <button onClick={onClick}>{props.text}</button>
      {props.params.map((param: string) => (
        <div key={param} className='mb-3'>
          <label htmlFor={param} className='form-label'>
            {param}:
          </label>
          <input
            id={param}
            type='number'
            step='any'
            onChange={handleInputChange}
            className='form-control form-control-sm '
          />
        </div>
      ))}
    </div>
  );
};
