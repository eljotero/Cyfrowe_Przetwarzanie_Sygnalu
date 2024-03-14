import { UniversalSignalGenerator } from './UniversalSignalGenerator.tsx';
import './MainPage.css';

const signals = [
  {
    name: 'uniformNoise',
    params: ['A', 't1', 'd', 'f'],
    text: 'Wygeneruj szum o rozkładzie jednostajnym',
    id: 1,
  },
  {
    name: 'gaussianNoise',
    params: ['A', 't1', 'd', 'f'],
    text: 'Wygeneruj szum gaussowski',
    id: 2,
  },
  {
    name: 'fullWave',
    params: ['A', 'T', 't1', 'd', 'f'],
    text: 'Wygeneruj sygnał sinusoidalny',
    id: 3,
  },
  {
    name: 'halfWave',
    params: ['A', 'T', 't1', 'd', 'f'],
    text: 'Wygeneruj sygnał sinusoidalny wyprostowany jednopołówkowo',
    id: 4,
  },
  {
    name: 'sinusoidalSignal',
    params: ['A', 'T', 't1', 'd', 'f'],
    text: 'Wygeneruj sygnał sinusoidalny  wyprostowany dwupołówkowo',
    id: 5,
  },
  {
    name: 'squareWave',
    params: ['A', 'T', 't1', 'd', 'kw', 'f'],
    text: 'Wygeneruj sygnał prostokątny',
    id: 6,
  },
  {
    name: 'symmetricalSquareWave',
    params: ['A', 'T', 't1', 'd', 'kw', 'f'],
    text: 'Wygeneruj sygnał prostokątny symetryczny',
    id: 7,
  },
  {
    name: 'triangularWave',
    params: ['A', 'T', 't1', 't1', 'd', 'kw', 'f'],
    text: 'Wygeneruj sygnał trójkątny',
    id: 8,
  },
  {
    name: 'unitStep',
    params: ['A', 't1', 'd', 'ts', 'f'],
    text: 'Wygeneruj skok jednostkowy',
    id: 9,
  },
  {
    name: 'unitImpulse',
    params: ['A', 'ns', 'n1', 'l', 'f'],
    text: 'Wygeneruj impuls jednostkowy',
    id: 10,
  },
  {
    name: 'impulseNoise',
    params: ['A', 't1', 'd', 'f', 'p'],
    text: 'Wygeneruj szum impulsowy',
    id: 11,
  },
];

function MainPage() {
  return (
    <div className='signalsDiv'>
      {signals.map((signal) => (
        <UniversalSignalGenerator
          key={signal.id}
          name={signal.name}
          params={signal.params}
          text={signal.text}
          signalId={signal.id}
        />
      ))}
    </div>
  );
}

export default MainPage;
