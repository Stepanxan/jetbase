import React, { useState } from 'react';
import './App.css';


const NumberForm = () => {
  const [N, setN] = useState(10000000000);
  const [results, setResults] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/find-missing', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ N }),
    });
    const data = await response.json();
    console.log('Received data:', data);
    setResults(data);
  };

  return (
    <div className="App">
      <h1>Пошук пропущених чисел</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Максимальне число для діапазону від 1 до
            <input type="number" value={N} onChange={(e) => setN(parseInt(e.target.value, 10))} />
          </label>
        </div>
        <button type="submit" className="button">Пошук пропущених чисел</button>
      </form>

      {results && (
        <div>
          <h2>Результат:</h2>
          <p>Пропущене число №1: {results.missing1}</p>
          <p>Пропущене число №2: {results.missing2}</p>
          <p>Метод суми квадратів: {results.sum_squares[0].join(', ')} (Час: {results.sum_squares[1]}с)</p>
          {/*<p>Лінійне порівняння: {results.linear[0].join(', ')} (Time: {results.linear[1]}s)</p>*/}
          {/*<p>Метод "XOR": {results.xor[0].join(', ')} (Time: {results.xor[1]}s)</p>*/}
        </div>
      )}
    </div>
  );
}

export default NumberForm;